"""Finds the streamer's camera box in a landscape stream, for the "split" and "band" layouts (M3.4).

1. Faces are found in a dozen frames spread over the footage with OpenCV's YuNet detector (MIT licence,
   230 KB, downloaded once into models/). The streamer's face stays in one place while game characters
   move, so only a face seen in the same place in a quarter of the frames (at least 3) counts.
2. The camera box is sized around that face: some room above the head, the shoulders below, as wide as
   the layout's camera band is shaped.
3. If the stream draws a border around its camera, the box snaps to it: overlay borders are straight
   lines that stay put, so they stand out in the average of the frames' edges while moving gameplay
   blurs away.

A handcam (hands, no face) is not found; the creator draws its box in the editor. The result is a box in
frame fractions (x, y, w, h), or None."""

import urllib.request
from pathlib import Path

from ..config import ROOT
from ..jobs import log

MODEL = ROOT / "models" / "face_detection_yunet_2023mar.onnx"
MODEL_URL = ("https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/"
             "face_detection_yunet_2023mar.onnx")
SAMPLES = 12
ANALYSIS_W = 960
MIN_SCORE = 0.75
SAME_PLACE = 0.06        # face centres closer than this (fraction of frame width) are the same face
MIN_SHARE = 0.25         # seen in at least this share of the frames (streamers look down at the phone a lot)
CAM_ASPECT = 1080 / 760  # the split layout's camera band
SNAP_REACH = 0.35        # how far (fraction of the box's size) a side may move to meet a border line
EDGE_STRENGTH = 3.0      # a border pixel's edge is this many times the frame's typical edge strength


def ensure_model():
    if MODEL.exists():
        return MODEL
    try:
        MODEL.parent.mkdir(parents=True, exist_ok=True)
        tmp = MODEL.with_suffix(".part")
        urllib.request.urlretrieve(MODEL_URL, tmp)
        if tmp.stat().st_size < 100_000:
            raise RuntimeError("download too small")
        tmp.replace(MODEL)
        log("facecam: face model downloaded")
        return MODEL
    except Exception as exc:   # no network: layouts still work, just without an automatic camera box
        log(f"facecam: face model unavailable ({exc!r})")
        return None


def sample_frames(video, start=None, end=None, count=SAMPLES):
    """`count` frames spread over [start, end] seconds of the video (the whole video by default),
    scaled to ANALYSIS_W wide."""
    import cv2

    cap = cv2.VideoCapture(str(video))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    total = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps
    a, b = start or 0.0, min(end or total, total)
    frames = []
    for i in range(count):
        cap.set(cv2.CAP_PROP_POS_MSEC, (a + (b - a) * (i + 0.5) / count) * 1000)
        ok, frame = cap.read()
        if ok:
            h, w = frame.shape[:2]
            frames.append(cv2.resize(frame, (ANALYSIS_W, round(ANALYSIS_W * h / w))))
    cap.release()
    return frames


def faces(frames, model):
    """Per frame, the faces found: [(x, y, w, h) in frame fractions]."""
    import cv2

    h, w = frames[0].shape[:2]
    detector = cv2.FaceDetectorYN.create(str(model), "", (w, h), MIN_SCORE, 0.3, 50)
    found = []
    for frame in frames:
        _, rows = detector.detect(frame)
        found.append([(r[0] / w, r[1] / h, r[2] / w, r[3] / h) for r in (rows if rows is not None else [])])
    return found


def steady_face(found):
    """The face seen in the same place in at least MIN_SHARE of the frames (the largest such), or None."""
    groups = []   # [[(cx, cy, box), ...]]
    for boxes in found:
        for box in boxes:
            cx, cy = box[0] + box[2] / 2, box[1] + box[3] / 2
            for group in groups:
                gx, gy, _ = group[0]
                if abs(cx - gx) < SAME_PLACE and abs(cy - gy) < SAME_PLACE * 1.8:
                    group.append((cx, cy, box))
                    break
            else:
                groups.append([(cx, cy, box)])
    steady = [g for g in groups if len(g) >= max(3, MIN_SHARE * len(found))]
    if not steady:
        return None
    best = max(steady, key=lambda g: (len(g), sum(b[2] * b[3] for _, _, b in g)))
    import statistics

    return tuple(statistics.median(b[i] for _, _, b in best) for i in range(4))


def box_around(face, frame_aspect):
    """A camera box (frame fractions) around a face: a little room above the head, down to the chest,
    shaped like the camera band. `frame_aspect` is the frame's width / height."""
    fx, fy, fw, fh = face
    top = fy - 0.6 * fh
    height = 3.0 * fh
    width = height * CAM_ASPECT / frame_aspect
    cx = fx + fw / 2
    return [cx - width / 2, top, width, height]


def edge_map(frames):
    """The average edge strength over the frames, split into vertical and horizontal edges."""
    import cv2
    import numpy as np

    gx = np.zeros(frames[0].shape[:2], np.float32)
    gy = np.zeros_like(gx)
    for frame in frames:
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype(np.float32)
        gx += np.abs(cv2.Sobel(grey, cv2.CV_32F, 1, 0, ksize=3))
        gy += np.abs(cv2.Sobel(grey, cv2.CV_32F, 0, 1, ksize=3))
    return gx / len(frames), gy / len(frames)


BORDER_EXTENT = 0.6   # a border line must run along at least this share of the box's side


def snap(box, edges, face):
    """Move each side of the box to a steady border line nearby, never cutting into the face. Only a line
    that runs along most of that side counts: a camera's border does; the edge of a donation widget or
    some other overlay next to the camera doesn't."""
    import numpy as np

    gx, gy = edges
    h, w = gx.shape
    typical_x, typical_y = float(np.median(gx)) + 1e-3, float(np.median(gy)) + 1e-3
    x0, y0, x1, y1 = box[0] * w, box[1] * h, (box[0] + box[2]) * w, (box[1] + box[3]) * h
    fx0, fy0, fx1, fy1 = face[0] * w, face[1] * h, (face[0] + face[2]) * w, (face[1] + face[3]) * h
    reach_x, reach_y = SNAP_REACH * (x1 - x0), SNAP_REACH * (y1 - y0)

    def column_line(c):
        seg = gx[int(max(0, y0)):int(min(h, y1)), c]
        return seg.size and float(np.mean(seg > EDGE_STRENGTH * typical_x)) >= BORDER_EXTENT

    def row_line(r):
        seg = gy[r, int(max(0, x0)):int(min(w, x1))]
        return seg.size and float(np.mean(seg > EDGE_STRENGTH * typical_y)) >= BORDER_EXTENT

    def nearest(lo, hi, near, test):
        lo, hi = int(max(1, lo)), int(hi)
        candidates = [i for i in range(lo, hi) if test(i)]
        return min(candidates, key=lambda i: abs(i - near)) if candidates else None

    left = nearest(x0 - reach_x, min(x0 + reach_x, fx0 - 2), x0, column_line)
    right = nearest(max(x1 - reach_x, fx1 + 2), min(x1 + reach_x, w - 1), x1, column_line)
    top = nearest(y0 - reach_y, min(y0 + reach_y, fy0 - 2), y0, row_line)
    bottom = nearest(max(y1 - reach_y, fy1 + 2), min(y1 + reach_y, h - 1), y1, row_line)
    x0, x1 = (left if left is not None else x0), (right if right is not None else x1)
    y0, y1 = (top if top is not None else y0), (bottom if bottom is not None else y1)
    return [x0 / w, y0 / h, (x1 - x0) / w, (y1 - y0) / h]


def clamp(box):
    x, y, w, h = box
    x0, y0 = max(0.0, x), max(0.0, y)
    x1, y1 = min(1.0, x + w), min(1.0, y + h)
    return [round(x0, 4), round(y0, 4), round(x1 - x0, 4), round(y1 - y0, 4)]


def detect(video, start=None, end=None, count=SAMPLES):
    """The camera box of a landscape video as frame fractions (x, y, w, h), or None."""
    model = ensure_model()
    if model is None:
        return None
    frames = sample_frames(video, start, end, count)
    if len(frames) < 4:
        return None
    h, w = frames[0].shape[:2]
    if h >= w:
        return None   # vertical streams keep the streamer's own layout
    face = steady_face(faces(frames, model))
    if face is None:
        return None
    box = clamp(snap(clamp(box_around(face, w / h)), edge_map(frames), face))
    area = box[2] * box[3]
    if not (0.01 <= area <= 0.45) or box[2] < 0.05 or box[3] < 0.08:
        return None
    return box


STREAM_FILE = "facecam.json"
STREAM_SAMPLES = 24


def for_stream(job_folder, source=None):
    """The stream's camera box, worked out once over the whole recording (a camera rarely moves within
    a stream) and kept in the job folder as {"box": [x, y, w, h] or null, "source": "auto" or "manual"}.
    A box the creator set in the editor wins. Returns the saved dict, or None when it hasn't been worked
    out and there is no recording to work it out from."""
    from ..jobs import read_json, write_json

    path = Path(job_folder) / STREAM_FILE
    saved = read_json(path)
    if source is None or (saved is not None and "layout" in saved):
        return saved
    if saved is None:
        box = detect(source, count=STREAM_SAMPLES)
        saved = {"box": [float(v) for v in box] if box else None, "source": "auto"}
    # A vertical stream's own layout: where its game and camera bands are, for stacked Shorts (owner, 14 Nov).
    from . import gamebox

    info = read_json(Path(job_folder) / "info.json")
    saved["layout"] = gamebox.find(source, info, read_json(Path(job_folder) / "vision.json")) if info else None
    if saved["layout"] and saved["layout"].get("cam") and not saved.get("box"):
        saved["box"], saved["source"] = saved["layout"]["cam"], "layout"
    write_json(path, saved)
    log(f"facecam: {Path(job_folder).name}: {saved['box']}, layout {saved['layout']}")
    return saved


def set_manual(job_folder, box):
    from ..jobs import read_json, write_json

    saved = read_json(Path(job_folder) / STREAM_FILE) or {}
    write_json(Path(job_folder) / STREAM_FILE, {"box": [round(float(v), 4) for v in box], "source": "manual",
                                                "layout": saved.get("layout")})
