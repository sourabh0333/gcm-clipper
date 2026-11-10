"""Thumbnails for long videos (M3.7; the weekly compilation in M3.8 and stream highlights): three of them, for
YouTube's Test & Compare, in the format Indian gaming channels use (master plan 4.4, "Thumbnails and titles"):

1. the best kill frame, the streamer cut out of the camera on the right, 2-3 words of stats on the left;
2. another kill frame, the streamer on the left, other words on the right;
3. the best kill frame, closer in, no text: the clean option that often wins on mobile.

Without a camera (or a handcam) the first two are the kill frames with their words. The cut-out uses
MediaPipe's selfie segmenter (Apache 2.0, 250 KB, downloaded once into models/), taken at the streamer's
reaction just after a kill (the loudest moment), with a white sticker outline. Words are drawn by libass
with the bundled Anton font, like the hook."""

import tempfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from ..config import ROOT
from ..jobs import log

W, H = 1280, 720
MODEL = ROOT / "models" / "selfie_segmenter.tflite"
MODEL_URL = ("https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_segmenter/float16/latest/"
             "selfie_segmenter.tflite")
PERSON_H = 690          # the cut-out's height on the thumbnail
OUTLINE = 10            # the sticker outline around it
TEXT_START = 150
MIN_PERSON, MAX_PERSON = 0.08, 0.85   # share of the camera crop the person should fill


@dataclass
class Moment:
    video: Path          # the file the frame is in (the stream's source or a clip's working window)
    t: float             # seconds into that file
    kind: str            # "kill" or "reaction"
    score: float = 0.0


def ensure_segmenter():
    if MODEL.exists():
        return MODEL
    try:
        MODEL.parent.mkdir(parents=True, exist_ok=True)
        tmp = MODEL.with_suffix(".part")
        urllib.request.urlretrieve(MODEL_URL, tmp)
        tmp.replace(MODEL)
        return MODEL
    except Exception as exc:   # no network: thumbnails are made without the cut-out
        log(f"thumbs: segmenter unavailable ({exc!r})")
        return None


def grab(video, t):
    import cv2

    cap = cv2.VideoCapture(str(video))
    cap.set(cv2.CAP_PROP_POS_MSEC, max(0.0, t) * 1000)
    ok, frame = cap.read()
    cap.release()
    return frame if ok else None


def background(frame, zoom=1.0, dim=0.82):
    """The frame filling 1280x720 (centre-cropped to 16:9), zoomed in around the centre, a little darker so
    the words and the streamer stand out."""
    import cv2
    import numpy as np

    h, w = frame.shape[:2]
    want = W / H
    if w / h > want:
        cw, ch = h * want, h
    else:
        cw, ch = w, w / want
    cw, ch = cw / zoom, ch / zoom
    x0, y0 = int((w - cw) / 2), int((h - ch) / 2)
    crop = frame[y0:y0 + int(ch), x0:x0 + int(cw)]
    out = cv2.resize(crop, (W, H), interpolation=cv2.INTER_CUBIC).astype(np.float32) * dim
    alpha = np.full((H, W, 1), 255.0, np.float32)
    return np.concatenate([np.clip(out, 0, 255), alpha], axis=-1)


def cutout(frame, cam_box, segmenter):
    """The streamer cut out of the camera box as an RGBA image with a white outline, or None when no clear
    person is found (a handcam, an empty chair)."""
    import cv2
    import mediapipe as mp
    import numpy as np

    h, w = frame.shape[:2]
    x, y, bw, bh = cam_box
    crop = frame[int(y * h):int((y + bh) * h), int(x * w):int((x + bw) * w)]
    if crop.size == 0:
        return None
    scale = max(1.0, 640 / crop.shape[0])
    crop = cv2.resize(crop, (round(crop.shape[1] * scale), round(crop.shape[0] * scale)), interpolation=cv2.INTER_CUBIC)
    rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
    result = segmenter.segment(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(rgb)))
    mask = result.confidence_masks[0].numpy_view().astype(np.float32)
    if mask.ndim == 3:
        mask = mask[..., 0]
    alpha = np.clip((mask - 0.35) / 0.3, 0, 1)
    share = float((alpha > 0.5).mean())
    if not MIN_PERSON <= share <= MAX_PERSON:
        return None
    ys, xs = np.where(alpha > 0.5)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    pad = OUTLINE * 2
    person = np.zeros((y1 - y0 + 2 * pad, x1 - x0 + 2 * pad, 4), np.float32)
    person[pad:-pad, pad:-pad, :3] = crop[y0:y1, x0:x1]
    person[pad:-pad, pad:-pad, 3] = alpha[y0:y1, x0:x1] * 255
    ring = cv2.dilate((person[..., 3] > 127).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (OUTLINE * 2 + 1,) * 2))
    sticker = np.zeros_like(person)
    sticker[..., :3] = 255
    sticker[..., 3] = cv2.GaussianBlur(ring.astype(np.float32) * 255, (5, 5), 0)
    from .hook import over

    return over(person, sticker), share


def place(canvas, person, side):
    """Lay the cut-out on the canvas, bottom-aligned, against the left or right edge."""
    import cv2

    from .hook import over

    scale = PERSON_H / person.shape[0]
    pw = round(person.shape[1] * scale)
    pic = cv2.resize(person, (pw, PERSON_H), interpolation=cv2.INTER_AREA)
    pw = min(pw, W)
    pic = pic[:, :pw]
    x0 = W - pw - 10 if side == "right" else 10
    y0 = H - PERSON_H
    canvas[y0:, x0:x0 + pw] = over(pic, canvas[y0:, x0:x0 + pw])
    return canvas


def words(text, colour, side, folder, room=W // 2 + 40):
    """Big stat words (Anton, 1-2 lines) as an RGBA layer for one half of the thumbnail."""
    import numpy as np

    from . import hook

    size = TEXT_START
    layer = None
    for _ in range(7):
        align, margin_l, margin_r = (4, 50, W - room) if side == "left" else (6, W - room, 50)
        ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: T,{hook.LATIN_FONT},{size},{hook.COLOURS[colour]},&H00FFFFFF&,&H00000000&,&H00000000&,0,0,0,0,100,100,1,0,1,{max(6, size // 13)},0,{align},{margin_l},{margin_r},0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:01.00,T,,0,0,0,,{hook._escape(text.upper())}
"""
        layer = hook._draw(ass, H, Path(folder), f"words_{side}", width=W)
        rows = np.where(layer[..., 3].max(axis=1) > 0)[0]
        height = (rows[-1] - rows[0] + 1) if rows.size else 0
        if height <= size * 2.6 and height < H - 80:
            break
        size = round(size * 0.86)
    return layer.astype(np.float32)


def make_set(moments, cam_box, texts, out_dir):
    """Three thumbnails (thumb_1.jpg ... thumb_3.jpg) in out_dir from the moments; returns their paths."""
    import cv2
    import numpy as np

    from .hook import over

    kills = sorted((m for m in moments if m.kind == "kill"), key=lambda m: -m.score)
    reactions = sorted((m for m in moments if m.kind == "reaction"), key=lambda m: -m.score)
    if not kills:
        kills = reactions[:]
    frames = [f for f in (grab(m.video, m.t) for m in kills[:6]) if f is not None]
    if not frames:
        raise RuntimeError("No frames could be read for thumbnails.")
    people = []
    if cam_box:
        model = ensure_segmenter()
        if model is not None:
            from mediapipe.tasks.python import BaseOptions, vision

            options = vision.ImageSegmenterOptions(base_options=BaseOptions(model_asset_path=str(model)),
                                                   output_confidence_masks=True, output_category_mask=False)
            with vision.ImageSegmenter.create_from_options(options) as segmenter:
                for m in reactions[:8] + kills[:4]:
                    frame = grab(m.video, m.t)
                    found = cutout(frame, cam_box, segmenter) if frame is not None else None
                    if found:
                        people.append(found[0])
                    if len(people) == 2:
                        break
    texts = [t for t in texts if t] or ["BGMI"]
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    plans = [(frames[0], 1.0, people[0] if people else None, "right", texts[0], "yellow"),
             (frames[1 % len(frames)], 1.12, people[1 % len(people)] if people else None, "left",
              texts[1 % len(texts)], "white"),
             (frames[0], 1.3, None, None, None, None)]
    paths = []
    with tempfile.TemporaryDirectory(prefix="kaatclip_thumbs_") as tmp:
        for i, (frame, zoom, person, side, text, colour) in enumerate(plans, start=1):
            canvas = background(frame, zoom, dim=0.82 if text else 1.0)
            if person is not None:
                canvas = place(canvas, person, side)
            if text:
                text_side = "left" if side in ("right", None) else "right"
                canvas = over(words(text, colour, text_side, tmp), canvas)
            path = out_dir / f"thumb_{i}.jpg"
            cv2.imwrite(str(path), np.clip(canvas[..., :3], 0, 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 92])
            paths.append(path)
    log(f"thumbs: {len(paths)} made, {len(people)} with the streamer cut out")
    return paths
