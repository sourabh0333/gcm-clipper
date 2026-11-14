"""Where the game and the camera sit in a vertical stream's own layout (owner, 14 Nov: Shorts and Reels are
stacked, the face cam on top and the game filling the rest; long YouTube highlights keep the stream as it is).

A vertical stream is the streamer's own collage: a landscape game picture somewhere in the middle, a camera
above or below it, and overlays (UPI, subscribe, donation goals) that hardly change. Over a match the game
area changes all the time, the camera a little and the overlays almost never, so the rows of the frame are
measured by how much they change between moments a minute apart (measured on ANJI: game rows about 50,
camera 4-13, overlays 1-2 on a 0-255 scale).
"""

import subprocess

import numpy as np

from ..media import tool

GRID_W, GRID_H = 90, 160
SAMPLES = 40
GAME_SHARE = 0.5          # rows at least half as busy as the busiest are game
CAM_SHARE = 0.06          # rows busier than this share (but not game) can be the camera
JOIN = 0.06               # camera runs this close (frame fractions) are one
GAME_JOIN = 0.02
MIN_GAME = 0.15
MIN_CAM = 0.10
CAM_PAD = 0.05


def sample_rows(source, spans, duration):
    """How much each row of the frame changes between samples taken through the matches (`spans`)."""
    spans = [s for s in spans if s[1] - s[0] > 60] or [[0.0, duration]]
    times = []
    for a, b in spans:
        times += list(np.linspace(a + 5, b - 5, max(2, int((b - a) // 60))))
    times = sorted(times)
    times = times[:: max(1, len(times) // SAMPLES)][:SAMPLES]
    frames = []
    for t in times:
        raw = subprocess.run([tool("ffmpeg"), "-v", "error", "-ss", f"{t:.1f}", "-i", str(source), "-frames:v", "1",
                              "-vf", f"scale={GRID_W}:{GRID_H},format=gray", "-f", "rawvideo", "-"],
                             capture_output=True).stdout
        if len(raw) == GRID_W * GRID_H:
            frames.append(np.frombuffer(raw, np.uint8).astype(np.float32).reshape(GRID_H, GRID_W))
    if len(frames) < 4:
        return None
    return np.abs(np.diff(np.stack(frames), axis=0)).mean(axis=(0, 2))


def _runs(mask, join_rows):
    runs = []
    for y, on in enumerate(mask):
        if not on:
            continue
        if runs and y - runs[-1][1] <= join_rows:
            runs[-1][1] = y
        else:
            runs.append([y, y])
    return [(a, b + 1) for a, b in runs]


def _narrow(rows, run, max_share, join):
    """A game picture is landscape: a band taller than the frame is wide has picked up something else that
    moves (T-REX's animated art under the game). Raise the bar until the busiest core fits."""
    a, b = run
    for share in (0.65, 0.75, 0.85):
        if (b - a) / len(rows) <= max_share:
            break
        inner = rows[a:b]
        cores = _runs(inner >= share * inner.max(), join)
        if cores:
            c = max(cores, key=lambda r: r[1] - r[0])
            a, b = a + c[0], a + c[1]
    return a, b


def layout_from_rows(rows, counter_y=None, aspect=16 / 9):
    """{"game": [0, y, 1, h], "cam": [0, y, 1, h] or None} in frame fractions, or None when no clear game
    band stands out. The game band is the busiest run of rows (the one next to the kill counter when there
    are several); the camera is the longest moderately busy run outside it."""
    if rows is None or not len(rows) or rows.max() <= 0:
        return None
    n = len(rows)
    join = max(1, int(JOIN * n))
    # The game's own rows never go quiet, so only tiny dips are bridged: T-REX's game and the animated art
    # under it are separated by a 4% band of overlay.
    games = [r for r in _runs(rows >= GAME_SHARE * rows.max(), max(1, int(GAME_JOIN * n)))
             if (r[1] - r[0]) / n >= MIN_GAME]
    if not games:
        return None
    if counter_y is not None and len(games) > 1:
        target = counter_y * n
        game = min(games, key=lambda r: 0 if r[0] - join <= target <= r[1] + join else min(abs(target - r[0]), abs(target - r[1])))
    else:
        game = max(games, key=lambda r: r[1] - r[0])
    game = _narrow(rows, game, 1.0 / aspect, join)      # aspect: the frame's height / width
    rest = (rows >= CAM_SHARE * rows.max()) & (rows < GAME_SHARE * rows.max())
    rest[max(0, game[0] - 1):min(n, game[1] + 1)] = False
    cams = [r for r in _runs(rest, join) if (r[1] - r[0]) / n >= MIN_CAM]
    cam = None
    if cams:
        a, b = max(cams, key=lambda r: r[1] - r[0])
        pad = int(CAM_PAD * n)
        a, b = max(0, a - pad), min(n, b + pad)
        if b <= game[0] or a >= game[1]:        # never into the game
            pass
        elif a < game[0]:
            b = game[0]
        else:
            a = game[1]
        cam = [0.0, round(a / n, 4), 1.0, round((b - a) / n, 4)]
    return {"game": [0.0, round(game[0] / n, 4), 1.0, round((game[1] - game[0]) / n, 4)], "cam": cam}


def find(source, info, vision=None):
    """The game and camera boxes of a vertical stream, or None (landscape, or no clear game band)."""
    if not info or info.get("height", 0) <= info.get("width", 0):
        return None
    vision = vision or {}
    boxes = vision.get("counter_boxes") or {}
    counter = boxes.get("elims") or boxes.get("remaining")
    rows = sample_rows(source, vision.get("hud") or [], info.get("duration") or 0)
    return layout_from_rows(rows, counter[1] if counter else None, info["height"] / info["width"])
