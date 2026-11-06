"""Reads BGMI's HUD.

The main signal is the "Eliminations" counter in the top-left corner: every time it goes up, the streamer
got a kill, and when it drops back to 0 a new match has started. The "Remaining" counter beside it says how
late in the match a fight happened. Both counters are located once per video (streamers' layouts and
overlays differ), then only the small number boxes are read, which is fast and far more reliable than
finding single digits in a busy frame.

When the streamer dies and spectates a teammate, BGMI shows "Spectating" and the counter switches to the
teammate's eliminations, so the counter is ignored while that text is on screen.

On-screen messages (chicken dinner, "You knocked out", accolades) are read from a wider region, but only
when bright text appears in it, plus a safety read every few seconds."""

import difflib
import os
import re
import subprocess
from collections import Counter as Tally, deque
from pathlib import Path

import numpy as np

from .jobs import log, read_json, write_json
from .media import tool

# Order matters: the first pattern that matches a line decides its kind. The game also shows mission text
# ("Eliminate 3 players with a Pistol") and pickups ("Picked up Painkillers"), so only specific phrases count.
PATTERNS = [
    ("dinner", re.compile(r"winner ?winner|chicken ?dinner")),
    ("accolade", re.compile(r"\bace ?elim|new ?ace\b")),
    ("self_knock", re.compile(r"\byou ?knock")),
    ("self_kill", re.compile(r"\byou ?(finally )?(killed|eliminated)\b|finally ?killed")),
    ("knock", re.compile(r"knocked ?out")),
    ("kill", re.compile(r"\bkilled\b|\beliminated\b|headshot")),
]
# Kill-feed kinds that only count when the line names the streamer (AIGCM_PLAYER_NAMES).
NEEDS_NAME = {"knock", "kill"}
DEDUPE_S = 8.0
SPECTATE_REGION = (0.36, 0.64, 0.28, 0.08)
# On a vertical stream the gameplay window can be anywhere and its text is tiny, so the "Spectating" text is
# first searched for (enlarged) in a wide area below the counters: x from 0.35 to 0.65 of the frame, y from
# 0.1 to 0.45 below the counter row. Once seen, only a small crop around it is read, which is fast. OCR
# catches the tiny text on only about a quarter of the frames, so the search repeats every second
# while a change looks possible (about 1 s each), and stops once the spot is known.
SPECTATE_SEARCH = (0.35, 0.1, 0.3, 0.35)
SPECTATE_SEARCH_EVERY_S = 1.0
# Once the spot is known, OCR is not used on it again (it reads the tiny text on only a quarter of the
# frames): the text's own pixels, taken at the moment OCR found it, are the template, and a frame matches
# when enough of those pixels are lit again. The text is orange in most HUDs, else bright on dark. Only
# thin strokes count, so a character's skin or sandy ground in the same colour (PABLO's zoomed window)
# neither gets into the template nor matches it.
SPECTATE_MIN_PIXELS = 40
SPECTATE_MATCH = 0.3
SPECTATE_EVERY_S = 1.0   # at most one Spectating check a second while the counter looks different
SPECTATE_HOLD_S = 6.0
# The "Spectating" text is read on only about a quarter of the frames, so a teammate's counter can slip
# through the check at the moment it changes. Checks go on for this long after any accepted Eliminations
# change, and the change is undone if the text then appears. Longer would undo a real kill made just before
# the streamer died.
SPECTATE_RETRACT_S = 12.0
LOBBY_PLAYERS = 80        # Remaining at or above this means a fresh match
LOBBY_MIN_PLAYERS = 40    # a rise of LOBBY_JUMP to at least this is a fresh match too (some lobbies fill to 50-60)
LOBBY_JUMP = 20
MAX_PLAYERS = 100
UNCONFIRMED_RESET_S = 10.0   # how long a reset must hold when there is no lobby signal
BANNER_MIN_GAP_S = 3.0       # message text is read at most this often, even while it keeps appearing
MAX_REMAINING_DROP = 30

COUNTER_LABELS = {"elims": "eliminations", "remaining": "remaining"}
# BGMI's kill feed sits under the teammate list at the left edge of the gameplay window, one row per
# event: "<killer> <weapon icon> [<kneeling icon>] <victim>", no words, so OCR gives the two names as
# separate boxes on one row. The feed is placed from the counter row in units of the label height (lh):
# from the frame's left edge to 18 lh past the Remaining number, y from 4 lh to 12 lh below the row.
# A row that starts with the streamer's name without the Eliminations counter rising soon after is a
# knock; one that ends with it is the streamer going down. It is read every few seconds while any text
# shows there (each read costs about 0.3 s, whatever the crop size).
FEED_BOX_LH = (4.0, 18.0, 8.0)    # y offset, x extent past the Remaining number, height
FEED_EVERY_S = 4.0                # a row stays about 5 s, so this still sees each one
# Some layouts draw the feed too faint for OCR (GtxPreet: half-transparent rows over a bright map, no
# name read at any zoom) or hide it under an overlay (DIPENDU). After this many reads, the feed is
# given up unless enough of them produced a full "killer > victim" row.
FEED_TRIAL_READS = 120
FEED_MIN_ROW_RATE = 0.08
FEED_MIN_CONF = 0.5
FEED_KILL_WINDOW = (-2.0, 4.0)    # a feed row this close to a counter rise is the kill itself, not a knock
NAME_MATCH = 0.75                 # OCR mangles names, so they are compared loosely
COUNTER_SEARCH = (0.0, 0.0, 0.5, 0.12)   # top-left area searched for the counter labels
CALIBRATION_FRAMES = 24
VERTICAL_ANALYSIS = 1080
# BGMI's compact HUD shows the counters as icon + number (person 36, crosshair 20, wings 2) with no text
# labels, in one row at the top left. The numbers are found as a row of 2-3 short numbers; left to right
# they are players remaining, eliminations, assists.
ICON_ROW_MAX_DIGITS = 3
# The compass strip at the top centre is also a row of numbers (105, 120, 135...), so the icon row is looked
# for only in the left 30% of the frame, and only values up to 100 (players or kills) count.
ICON_SEARCH = (0.0, 0.0, 0.3, 0.1)
ICON_MAX_VALUE = 100
# A number box is this many line heights wide: room for two digits without the icon to its left.
ICON_NUMBER_W = 1.7
# OCR confusions between letters and the HUD's condensed digits.
DIGIT_FIX = str.maketrans({"O": "0", "o": "0", "D": "0", "Q": "0", "U": "0", "I": "1", "l": "1", "|": "1",
                           "i": "1", "J": "1", "S": "5", "s": "5", "B": "8", "Z": "2", "z": "2", "G": "6",
                           "b": "6", "g": "9", "q": "9", "T": "7"})
MAX_KILL_JUMP = 5
ZERO_LIKE = set("口品回日囗〇OoDQ")
# A 4-hour stream takes 1-3 hours to scan on the laptop; saving the state every 5 minutes of video means a
# crash or power cut costs a few minutes, not the whole scan.
CHECKPOINT_EVERY_S = 300


class Ocr:
    """RapidOCR on CPU. By default it enlarges small crops until their short side is 736 px, which makes a
    HUD strip take seconds; capping the long side instead keeps each read to a few tens of milliseconds.
    HUD text is never rotated, so the angle classifier is off."""

    def __init__(self, threads=None):
        from rapidocr_onnxruntime import RapidOCR
        self.threads = threads
        extra = {"intra_op_num_threads": threads} if threads else {}
        self.engine = RapidOCR(det_limit_type="max", det_limit_side_len=960, use_cls=False, **extra)
        self._hires = None

    def lines_hires(self, img, scale=2.0):
        """Like lines(), on an enlarged image with a larger detection limit: slow, but finds the tiny HUD of
        a gameplay window inside a vertical or composite stream layout. Boxes are in the original pixels."""
        import cv2
        from rapidocr_onnxruntime import RapidOCR
        if self._hires is None:
            extra = {"intra_op_num_threads": self.threads} if self.threads else {}
            self._hires = RapidOCR(det_limit_type="max", det_limit_side_len=2600, use_cls=False, **extra)
        big = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        result, _ = self._hires(big)
        out = []
        for box, text, conf in result or []:
            xs, ys = [p[0] / scale for p in box], [p[1] / scale for p in box]
            out.append((text, float(conf), (min(xs), min(ys), max(xs), max(ys))))
        return out

    def lines(self, img):
        """[(text, confidence, (x0, y0, x1, y1))] for each line of text found, in crop pixels."""
        result, _ = self.engine(img)
        out = []
        for box, text, conf in result or []:
            xs, ys = [p[0] for p in box], [p[1] for p in box]
            out.append((text, float(conf), (min(xs), min(ys), max(xs), max(ys))))
        return out

    def read_digits(self, crops):
        """Read a number from each crop, skipping text detection. The recogniser is a Chinese/English model:
        BGMI's rectangular "0" comes out as box-shaped characters (口, 品), so those count towards 0, and the
        output is decoded with only digits and the blank allowed. A step where some other character is
        clearly more likely than any digit counts as blank, so a stray letter at the crop edge doesn't turn
        into a digit."""
        rec = self.engine.text_rec
        if not hasattr(self, "_digit_ids"):
            chars = rec.postprocess_op.character
            self._digit_ids = np.array([0] + [i for i, c in enumerate(chars) if c in "0123456789"])
            self._digit_chars = [""] + [chars[i] for i in self._digit_ids[1:]]
            self._zero_col = self._digit_chars.index("0")
            self._zero_like = np.array([i for i, c in enumerate(chars) if c in ZERO_LIKE])
        _, img_h, img_w = rec.rec_image_shape[:3]
        out = []
        for crop in crops:
            h, w = crop.shape[:2]
            if h < 2 or w < 2:
                out.append(("", 0.0))      # a box that fell off the frame edge
                continue
            norm = rec.resize_norm_img(crop, max(img_w / img_h, w / h))[np.newaxis].astype(np.float32)
            probs = rec.session(norm)[0][0].copy()
            allowed = probs[:, self._digit_ids]
            allowed[:, self._zero_col] += probs[:, self._zero_like].sum(axis=1)
            probs[:, self._zero_like] = 0
            best, best_p = allowed.argmax(axis=1), allowed.max(axis=1)
            other = probs.argmax(axis=1)
            text, confs, prev = "", [], 0
            for k, p, o, row in zip(best, best_p, other, probs):
                if o not in self._digit_ids and row[o] > 0.6:
                    k = 0
                if k and k != prev:
                    text += self._digit_chars[k]
                    confs.append(float(p))
                prev = k
            out.append((text, float(np.mean(confs)) if confs else 0.0))
        return out


def normalise(text):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", text.lower())).strip()


def classify(line, player_names=()):
    norm = normalise(line)
    for kind, pattern in PATTERNS:
        if pattern.search(norm):
            if kind in NEEDS_NAME:
                # A kill-feed line that starts with the streamer's in-game name is their own kill.
                return "self_" + kind if any(norm.startswith(n) for n in player_names) else None
            return kind
    return None


def is_spectating(text):
    """OCR mangles "Spectating" ("Spectting", "Spectsting"), so compare the first word loosely."""
    words = normalise(text).split()
    return bool(words) and difflib.SequenceMatcher(None, words[0], "spectating").ratio() >= 0.7


def parse_number(text):
    cleaned = re.sub(r"\s", "", text).translate(DIGIT_FIX)
    return int(cleaned) if re.fullmatch(r"\d{1,3}", cleaned) else None


def text_ratio(crop):
    """Share of pixels that look like HUD text: near-white, yellow or bright red."""
    r, g, b = crop[..., 2].astype(np.int16), crop[..., 1].astype(np.int16), crop[..., 0].astype(np.int16)
    white = (r > 200) & (g > 200) & (b > 200)
    yellow = (r > 200) & (g > 170) & (b < 100)
    red = (r > 190) & (g < 90) & (b < 90)
    return float((white | yellow | red).mean())


def crop_region(frame, region):
    h, w = frame.shape[:2]
    x, y, rw, rh = region
    return frame[int(y * h): int((y + rh) * h), int(x * w): int((x + rw) * w)]


def frame_size(info, short_side):
    """Analysis size: the shorter side capped at `short_side`, so vertical streams keep their detail."""
    w, h = info["width"], info["height"]
    scale = min(1.0, short_side / min(w, h))
    return int(round(w * scale / 2) * 2), int(round(h * scale / 2) * 2)


def grab_frame(src, t, size):
    w, h = size
    cmd = [tool("ffmpeg"), "-v", "error", "-ss", f"{t:.2f}", "-i", str(src), "-frames:v", "1",
           "-vf", f"scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(h, w, 3) if len(raw) == w * h * 3 else None


def locate_counters(src, info, size, ocr):
    """Find the number box to the right of each counter label, as fractions of the frame. Labels are found
    on frames spread through the video and the median position is used, so a few bad reads don't matter.
    A landscape stream has them in the top-left corner; otherwise (vertical or composite layouts, where
    the gameplay is a smaller window) the whole frame is searched at higher resolution."""
    boxes = _locate_counters(src, info, size, ocr, COUNTER_SEARCH, ocr.lines)
    if not boxes:
        boxes = _locate_icon_counters(src, info, size, ocr)
    if not boxes:
        log("vision: counters not in the top-left corner, searching the whole frame")
        # Small streamers spend long stretches in lobbies with no counters on screen, so more frames are
        # sampled here than for the corner search.
        boxes = _locate_counters(src, info, size, ocr, (0.0, 0.0, 1.0, 1.0), ocr.lines_hires, frames=24)
    return drop_overlapping(boxes)


def drop_overlapping(boxes):
    """On a tiny HUD the "Remaining" label's OCR box can swallow its own number, so both counters land on
    the Eliminations number: then every "players left" read is really the kill count, no lobby is ever seen
    and a new match's reset is refused. Only the Eliminations counter is kept in that case."""
    if "elims" in boxes and "remaining" in boxes:
        ex, ey, ew, eh = boxes["elims"]
        rx, ry, rw, rh = boxes["remaining"]
        overlap = max(0.0, min(ex + ew, rx + rw) - max(ex, rx)) * max(0.0, min(ey + eh, ry + rh) - max(ey, ry))
        if overlap > 0.5 * min(ew * eh, rw * rh):
            log("vision: the Remaining counter sits on the Eliminations box, dropped")
            boxes = {"elims": boxes["elims"]}
    return boxes


def spectate_search(counter_boxes):
    """The area of a vertical frame searched for the "Spectating" text, below the counter row."""
    sx, dy, sw, sh = SPECTATE_SEARCH
    top = round(min(1.0, counter_boxes["elims"][1] + dy), 4)
    return (sx, top, sw, round(min(sh, 1.0 - top), 4))


def spectate_spot(lines, search, frame_w, frame_h):
    """A padded box (frame fractions) around the "Spectating" line among OCR lines of the `search` crop,
    or None. The text keeps its place for the whole stream, so later checks read only this box."""
    sx, sy, _, _ = search
    for text, _, (x0, y0, x1, y1) in lines:
        # The match results screen also says "Spectating: 0/10" (OCR may read "D/ID"); only the in-game
        # label counts, so a line with a digit or a slash is skipped.
        if is_spectating(text) and not re.search(r"[\d/]", text):
            px, py = (x1 - x0) * 0.3, (y1 - y0) * 1.0
            left, top = sx * frame_w + x0 - px, sy * frame_h + y0 - py
            return (round(max(0.0, left) / frame_w, 4), round(max(0.0, top) / frame_h, 4),
                    round((x1 - x0 + 2 * px) / frame_w, 4), round((y1 - y0 + 2 * py) / frame_h, 4))
    return None


def icon_row(lines, frame_w, frame_h, search=ICON_SEARCH):
    """The kill counter box for BGMI's compact HUD, from OCR lines of the search crop. The HUD is a row of
    icon + number cells (person 36 | crosshair 20 | wings 2) with no text labels. When OCR reads the numbers
    as separate lines, the second number's right edge is reliable (the icon that follows it is a separate
    glyph), so the eliminations box is anchored there, wide enough for three digits. The players-left number
    is not read: OCR merges the crosshair icon into it unpredictably, and the kill logic works without it.
    Returns {"elims": box} in frame fractions, or {}."""
    sx, sy, sw, sh = search
    numbers = []
    for text, conf, (x0, y0, x1, y1) in lines:
        digits = text.strip().translate(DIGIT_FIX)
        if (digits.isdigit() and 0 < len(digits) <= ICON_ROW_MAX_DIGITS and int(digits) <= ICON_MAX_VALUE
                and conf >= 0.5 and y1 - y0 >= 8):
            numbers.append((x0, y0, x1, y1))
    numbers.sort()
    best = []
    for i, box in enumerate(numbers):
        row = [box] + [o for o in numbers[i + 1:] if abs(o[1] - box[1]) < (box[3] - box[1]) * 0.8]
        if 2 <= len(row) <= 3 and len(row) > len(best):
            best = row
    if len(best) < 2:
        return {}
    lh = min(y1 - y0 for _, y0, _, y1 in best)
    x0, y0, x1, y1 = best[1]
    cy = (y0 + y1) / 2
    return {"elims": ((sx * frame_w + x1 - 2.3 * lh) / frame_w, max(0.0, (sy * frame_h + cy - 0.7 * lh) / frame_h),
                      (2.45 * lh) / frame_w, (lh * 1.4) / frame_h)}


def feed_region(counter_boxes, frame_w, frame_h):
    """Where the kill feed is read, as frame fractions, from the located counters (None without them)."""
    if "elims" not in counter_boxes:
        return None
    ex, ey, ew, eh = counter_boxes["elims"]
    lh = eh / 1.4                      # label height as a fraction of the frame height
    lhx = lh * frame_h / frame_w       # the same length as a fraction of the width
    rx = counter_boxes["remaining"][0] if "remaining" in counter_boxes else ex - 4.0 * lhx
    dy, w, h = FEED_BOX_LH
    y0 = ey + dy * lh
    if y0 >= 1.0:
        return None
    return (0.0, round(y0, 4), round(min(rx + w * lhx, 1.0), 4), round(min(h * lh, 1.0 - y0), 4))


def feed_rows(lines, crop_w):
    """Kill-feed rows from the OCR lines of the feed crop: (left name, right name) per row, with boxes
    grouped by their vertical centre and split at the crop's middle (the icons sit there)."""
    boxes = sorted(((x0, y0, x1, y1, text) for text, conf, (x0, y0, x1, y1) in lines if conf >= FEED_MIN_CONF),
                   key=lambda b: (b[1] + b[3]) / 2)
    rows, out = [], []
    for box in boxes:
        cy, h = (box[1] + box[3]) / 2, box[3] - box[1]
        for row in rows:
            if abs(row["cy"] - cy) < 0.6 * max(h, row["h"]):
                row["boxes"].append(box)
                break
        else:
            rows.append({"cy": cy, "h": h, "boxes": [box]})
    for row in rows:
        left = " ".join(b[4] for b in sorted(row["boxes"]) if (b[0] + b[2]) / 2 < crop_w / 2)
        right = " ".join(b[4] for b in sorted(row["boxes"]) if (b[0] + b[2]) / 2 >= crop_w / 2)
        if left or right:
            out.append((normalise(left), normalise(right)))
    return out


def feed_worth_reading(reads, full_rows):
    """False once a trial of reads shows the feed is unreadable in this layout."""
    return reads < FEED_TRIAL_READS or full_rows >= FEED_MIN_ROW_RATE * reads


def _is_name(text):
    return len(text) >= 3 and not re.fullmatch(r"\d+m?", text)


def _same_name(a, b):
    return a == b or difflib.SequenceMatcher(None, a, b).ratio() >= NAME_MATCH


def knocks_from_feed(feed, events, player_names=()):
    """Knock and down events from kill-feed rows ({"t", "left", "right", "conf"}). The streamer's in-game
    name is learned from the rows that appear when the Eliminations counter rises (their own kills name
    them on the left), unless `player_names` gives it. Returns (name, new events)."""
    kill_times = sorted(e["t"] for e in events if e["kind"] == "self_kill")
    names = [normalise(n) for n in player_names if normalise(n)]
    if not names:
        seen = Tally()
        for kt in kill_times:
            seen.update({row["left"] for row in feed if kt - 6 <= row["t"] <= kt + 3 and _is_name(row["left"])})
        groups = []   # [(representative, count)]
        for tok, n in seen.most_common():
            for i, (rep_tok, total) in enumerate(groups):
                if _same_name(tok, rep_tok):
                    groups[i] = (rep_tok, total + n)
                    break
            else:
                groups.append((tok, n))
        best = max(groups, key=lambda g: g[1], default=None)
        if best and best[1] >= 2 and best[1] >= 0.25 * max(1, len(kill_times)):
            names = [best[0]]
    if not names:
        return None, []
    out, recent = [], {}
    for row in sorted(feed, key=lambda r: r["t"]):
        left, right, t = row["left"], row["right"], row["t"]
        if _is_name(left) and any(_same_name(left, n) for n in names):
            if any(kt + FEED_KILL_WINDOW[0] <= t <= kt + FEED_KILL_WINDOW[1] for kt in kill_times):
                continue   # the kill itself; the counter already counted it
            kind = "self_knock"
        elif _is_name(right) and any(_same_name(right, n) for n in names):
            kind = "self_down"
        else:
            continue
        key = (kind, f"{left} {right}"[:40])
        if t - recent.get(key, -1e9) < DEDUPE_S:
            recent[key] = t
            continue
        recent[key] = t
        out.append({"t": round(t, 2), "kind": kind, "text": f"{left} > {right}", "region": "feed", "conf": row["conf"]})
    return names[0], out


def _orange_mask(crop):
    import cv2
    hsv = cv2.cvtColor(np.ascontiguousarray(crop), cv2.COLOR_BGR2HSV)
    return (hsv[..., 0] >= 10) & (hsv[..., 0] <= 35) & (hsv[..., 1] >= 100) & (hsv[..., 2] >= 140)


def _bright_mask(crop):
    import cv2
    grey = cv2.cvtColor(np.ascontiguousarray(crop), cv2.COLOR_BGR2GRAY).astype(float)
    return grey > grey.mean() + grey.std()


def _strokes(mask):
    """The thin parts of a mask: text strokes stay, blobs wider than about an eighth of the crop height go."""
    import cv2
    k = max(3, round(mask.shape[0] / 8))
    m = mask.astype(np.uint8)
    opened = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((k, k), np.uint8))
    return (m & ~opened).astype(bool)


def spectate_template(crop):
    """The "Spectating" text's stroke pixels in the crop where OCR just read it, to match later frames."""
    orange = _orange_mask(crop)
    if orange.sum() >= SPECTATE_MIN_PIXELS:
        return {"kind": "orange", "mask": _strokes(orange)}
    return {"kind": "bright", "mask": _strokes(_bright_mask(crop))}


def spectate_match(crop, template):
    """True when enough of the template's stroke pixels are lit in this crop of the same spot."""
    mask = _orange_mask(crop) if template["kind"] == "orange" else _bright_mask(crop)
    ref = template["mask"]
    if mask.shape != ref.shape:
        return False
    return (_strokes(mask) & ref).sum() / max(1, ref.sum()) >= SPECTATE_MATCH


def _locate_icon_counters(src, info, size, ocr, frames=12):
    w, h = size
    found = {"elims": []}
    for t in np.linspace(info["duration"] * 0.03, info["duration"] * 0.97, frames):
        frame = grab_frame(src, float(t), size)
        if frame is None:
            continue
        for name, box in icon_row(ocr.lines(crop_region(frame, ICON_SEARCH)), w, h).items():
            found[name].append(box)
    if len(found["elims"]) < 2:
        return {}
    boxes = {name: tuple(float(v) for v in np.median(np.array(items), axis=0)) for name, items in found.items() if len(items) >= 2}
    log(f"vision: compact icon HUD found ({len(found['elims'])} frames): " + ", ".join(boxes))
    return boxes


def number_box(label, numbers):
    """The crop-pixel box to read a counter's number from, given its label's OCR box and the digit-only
    OCR boxes on the frame. The number is the nearest digits just right of the label on the same row,
    and the box starts a little before its first digit and is wide enough for three digits; that keeps a
    padded label box (common in the enlarged whole-frame search) from cutting off the first digit. With
    no digits read on this frame, the number is assumed to start right at the label box's edge."""
    x0, y0, x1, y1 = label
    lh = y1 - y0
    cy = (y0 + y1) / 2
    near = [n for n in numbers if abs((n[1] + n[3]) / 2 - cy) < 0.6 * lh and -0.3 * lh <= n[0] - x1 < 2.0 * lh]
    if near:
        nx0, _, nx1, _ = min(near, key=lambda n: n[0])
        left = nx0 - 0.3 * lh
        return (left, cy - 0.7 * lh, max(2.2 * lh, nx1 + 0.3 * lh - left), 1.4 * lh)
    return (x1, cy - 0.7 * lh, 2.2 * lh, 1.4 * lh)


def _locate_counters(src, info, size, ocr, search, read, frames=CALIBRATION_FRAMES):
    w, h = size
    sx, sy, sw, sh = search
    found = {name: [] for name in COUNTER_LABELS}
    times = np.linspace(info["duration"] * 0.03, info["duration"] * 0.97, frames)
    for t in times:
        frame = grab_frame(src, float(t), size)
        if frame is None:
            continue
        lines = read(crop_region(frame, search))
        numbers = [box for text, _, box in lines if text.strip().translate(DIGIT_FIX).isdigit()]
        for text, _, label in lines:
            letters = re.sub(r"[^a-z]", "", text.lower())
            if re.search(r"\d", text) or len(letters) < 6:
                continue  # merged with its number, so the label's right edge is unreliable
            for name, target in COUNTER_LABELS.items():
                if difflib.SequenceMatcher(None, letters, target).ratio() >= 0.6:
                    bx, by, bw, bh = number_box(label, numbers)
                    found[name].append((sx * w + bx, sy * h + by, bw, bh))
    boxes = {}
    for name, items in found.items():
        if len(items) >= 3:
            x, y, bw, bh = np.median(np.array(items), axis=0)
            boxes[name] = (x / w, y / h, bw / w, bh / h)
    log(f"vision: counters found {', '.join(f'{k} ({len(found[k])} frames)' for k in boxes) or 'none'}")
    return boxes


class Counter:
    """A HUD number read every frame. A new value counts only once two reads in a row agree, and only
    plausible changes count that quickly; anything else needs several agreeing reads before it becomes the
    new baseline (and makes no kill event), so a couple of misreads can't invent kills.

    - "elims": a rise of up to 5, or a reset to 0 once a new lobby has opened (`fresh_match`).
    - "remaining": a drop of up to 30 players, or a jump to a fresh lobby. 0 is never shown in a match.
    """

    def __init__(self, kind, reads_per_second=2.0):
        self.kind = kind
        self.reset_reads = max(2, int(round(UNCONFIRMED_RESET_S * reads_per_second)))
        self.value = None
        self.pending, self.pending_t, self.pending_n = None, None, 0

    def state(self):
        return {"value": self.value, "pending": self.pending, "pending_t": self.pending_t, "pending_n": self.pending_n}

    def restore(self, state):
        self.value, self.pending = state["value"], state["pending"]
        self.pending_t, self.pending_n = state["pending_t"], state["pending_n"]
        return self

    def _reads_needed(self, old, value, fresh_match):
        """How many agreeing reads a change needs; None means never accept it."""
        if old is None:
            return 2
        if self.kind == "elims":
            if 0 < value - old <= MAX_KILL_JUMP:
                # One or two kills at once is normal; a bigger jump is usually a teammate's counter shown
                # for a moment (PABLO: "0 -> 5" twice in a row, then 0 again), so it must hold longer.
                return 2 if value - old <= 2 else 4
            if value < old:
                # Eliminations never go down within a match. A drop is a teammate's counter (spectating),
                # a transition screen or a misread, unless a new lobby has opened. With no lobby signal
                # (fresh_match is None: no Remaining counter in this layout) a reset must hold for 10 s;
                # a real new match keeps 0 for minutes, a flicker lasts a second or two.
                if value != 0:
                    return None
                if fresh_match is None:
                    return self.reset_reads
                return 2 if fresh_match else None
            return 6
        return 2 if 0 < old - value <= MAX_REMAINING_DROP or value >= LOBBY_PLAYERS else 6

    def update(self, t, value, fresh_match=True):
        """Returns (time first seen, old value, new value) when the value changes, else None."""
        # A match has 1-100 players; 141 is "41" with a stray digit from an enlarged HUD.
        if value is None or (self.kind == "remaining" and not 0 < value <= MAX_PLAYERS):
            return None
        if value == self.value:
            self.pending = None
            return None
        if value == self.pending:
            self.pending_n += 1
        else:
            self.pending, self.pending_t, self.pending_n = value, t, 1
        old = self.value
        needed = self._reads_needed(old, value, fresh_match)
        if needed is not None and self.pending_n >= needed:
            # A reset can wait minutes for the new lobby to confirm it; it happened at confirmation, not
            # when a teammate's 0 first showed up.
            when = t if self.kind == "elims" and value == 0 and old else self.pending_t
            self.value, self.pending = value, None
            return when, old, value
        return None


def counter_events(change):
    """Kill events for an Eliminations change; a reset to 0 means a new match started."""
    t, old, new = change
    if old is None:
        return []
    if new == 0 and old > 0:
        return [{"t": round(t, 2), "kind": "match_start", "text": f"eliminations {old} -> 0"}]
    if 0 < new - old <= MAX_KILL_JUMP:
        return [{"t": round(t, 2), "kind": "self_kill", "text": f"eliminations {old} -> {new}", "region": "counter"}
                for _ in range(new - old)]
    return []


def _load_checkpoint(path, src, info, fps):
    """The saved scan state, if `path` holds one for this same video and frame rate."""
    saved = read_json(path) if path else None
    if not saved or saved.get("source") != [str(src), info["duration"], fps]:
        return None
    return saved


def scan(src, info, settings, checkpoint=None):
    """Read the HUD through the whole video. With `checkpoint` (a file path), the scan state is saved every
    few minutes of video, and a scan that was stopped or crashed carries on from there."""
    fps = settings.vision_fps
    # Vertical sources are analysed at 1080 on the shorter side, for the same reason they are downloaded at
    # 1080: the gameplay window inside them is small.
    size = frame_size(info, max(settings.vision_height, VERTICAL_ANALYSIS) if info["height"] > info["width"]
                      else settings.vision_height)
    out_w, out_h = size
    ocr = Ocr(getattr(settings, "analysis_threads", None))
    saved = _load_checkpoint(checkpoint, src, info, fps)
    counter_boxes = ({k: tuple(v) for k, v in saved["counter_boxes"].items()} if saved
                     else locate_counters(src, info, size, ocr))

    counters = {name: Counter(name, fps) for name in counter_boxes}
    remaining = []          # [(t, players left)] whenever it changes
    spectating_until, last_spectate_read = -1.0, -1e9
    # Landscape: a fixed spot read at normal size. Vertical: the spot is found during the scan (see
    # SPECTATE_SEARCH) and read enlarged, because the gameplay window's text is tiny.
    vertical = out_h > out_w
    spectate_box = None if vertical else SPECTATE_REGION
    spectate_ref, template = None, None   # the crop OCR found the text in, and the mask made from it
    previous_elims = None   # last frame's raw Eliminations read
    last_change = None      # (t, counter state before, events before, lobby_open before) of the last change
    lobby_open = False      # the Remaining counter jumped to a fresh lobby since the last Eliminations change
    regions = dict(settings.regions)
    feed_box = feed_region(counter_boxes, out_w, out_h)
    feed = []               # every kill-feed row read: {"t", "left", "right", "conf"}
    last_feed_read, feed_reads, feed_full = -1e9, 0, 0
    history = {name: deque(maxlen=int(fps * 10)) for name in regions}
    last_read = {name: -1e9 for name in regions}
    recent = {}
    events, ocr_calls, index = [], 0, 0
    next_report = 600
    if saved:
        for name, state in saved["counters"].items():
            counters[name].restore(state)
        remaining = [tuple(r) for r in saved["remaining"]]
        spectating_until, last_spectate_read = saved["spectating_until"], saved["last_spectate_read"]
        if "spectate_box" in saved:
            spectate_box = tuple(saved["spectate_box"]) if saved["spectate_box"] else None
        if saved.get("spectate_ref"):
            spectate_ref = np.array(saved["spectate_ref"], np.uint8)
            template = spectate_template(spectate_ref)
        last_change = tuple(saved["last_change"]) if saved.get("last_change") else None
        lobby_open, last_read = saved["lobby_open"], saved["last_read"]
        feed = saved.get("feed", [])
        last_read = {name: last_read.get(name, -1e9) for name in regions}
        recent = {(kind, text): t for kind, text, t in saved["recent"]}
        events, ocr_calls, index, next_report = saved["events"], saved["ocr_calls"], saved["index"], saved["next_report"]
        log(f"vision: resuming at {index / fps / 60:.0f} min from the checkpoint")
    next_checkpoint = index / fps + CHECKPOINT_EVERY_S

    def save_checkpoint():
        write_json(checkpoint, {
            "source": [str(src), info["duration"], fps], "counter_boxes": counter_boxes,
            "counters": {name: c.state() for name, c in counters.items()}, "remaining": remaining,
            "spectating_until": spectating_until, "last_spectate_read": last_spectate_read,
            "spectate_box": spectate_box, "last_change": last_change,
            "spectate_ref": spectate_ref.tolist() if spectate_ref is not None else None,
            "lobby_open": lobby_open, "last_read": last_read, "feed": feed,
            "recent": [[kind, text, t] for (kind, text), t in recent.items()],
            "events": events, "ocr_calls": ocr_calls, "index": index, "next_report": next_report})

    # Seeking before the input is fast and frame-accurate enough here: the next frame read is frame `index`.
    seek = ["-ss", f"{index / fps:.3f}"] if index else []
    cmd = [tool("ffmpeg"), "-v", "error", *seek, "-i", str(src), "-vf", f"fps={fps},scale={out_w}:{out_h}",
           "-f", "rawvideo", "-pix_fmt", "bgr24", "-"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    frame_bytes = out_w * out_h * 3

    try:
        while True:
            buf = proc.stdout.read(frame_bytes)
            if len(buf) < frame_bytes:
                break
            frame = np.frombuffer(buf, np.uint8).reshape(out_h, out_w, 3)
            t = index / fps
            index += 1

            if counter_boxes:
                names = list(counter_boxes)
                reads = ocr.read_digits(crop_region(frame, counter_boxes[n]) for n in names)
                for name, (text, conf) in zip(names, reads):
                    value = parse_number(text) if conf >= 0.2 else None
                    if name == "elims":
                        # Only a changing counter can be a teammate's, so "Spectating" is looked for when
                        # two reads in a row agree on a new value (a teammate's counter holds steady, a lone
                        # misread of tiny digits does not), and for a while after a change was accepted.
                        # (A whole-frame read on every misread made a 30-min vertical section take 55 min.)
                        differs = value is not None and value != counters[name].value
                        steady = differs and value == previous_elims
                        if value is not None:
                            previous_elims = value
                        recent_change = last_change is not None and t - last_change[0] <= SPECTATE_RETRACT_S
                        seen = False
                        if template is not None:
                            # Known spot on a vertical stream: a pixel match, cheap enough for every frame.
                            seen = spectate_match(crop_region(frame, spectate_box), template)
                        elif ((steady or recent_change) and t >= spectating_until
                                and t - last_spectate_read >= SPECTATE_EVERY_S):
                            if spectate_box:
                                last_spectate_read = t
                                ocr_calls += 1
                                seen = any(is_spectating(line) for line, _, _ in
                                           ocr.lines(crop_region(frame, spectate_box)))
                            elif t - last_spectate_read >= SPECTATE_SEARCH_EVERY_S:
                                last_spectate_read = t
                                ocr_calls += 1
                                search = spectate_search(counter_boxes)
                                found = ocr.lines_hires(crop_region(frame, search))
                                spectate_box = spectate_spot(found, search, out_w, out_h)
                                seen = spectate_box is not None
                                found_text = next((l for l, _, _ in found if is_spectating(l)), "")
                                if seen:
                                    spectate_box = tuple(float(v) for v in spectate_box)
                                    spectate_ref = np.array(crop_region(frame, spectate_box))
                                    template = spectate_template(spectate_ref)
                                    log(f"vision: Spectating text found at {spectate_box} ({t / 60:.1f} min), "
                                        f"{template['kind']} template, read as {found_text!r}")
                                elif os.environ.get("AIGCM_DEBUG_VISION"):
                                    log(f"vision: no Spectating text at {t:.0f}s (read {value}, counter {counters[name].value})")
                        if seen:
                            spectating_until = t + SPECTATE_HOLD_S
                            if recent_change:
                                # The change just accepted was a teammate's counter: undo it.
                                counters[name].restore(last_change[1])
                                counters[name].pending, counters[name].pending_n = None, 0
                                del events[last_change[2]:]
                                lobby_open = last_change[3]
                                log(f"vision: change at {last_change[0] / 60:.1f} min was a teammate's counter, undone")
                                last_change = None
                        if differs and t < spectating_until:
                            continue
                    # Without a Remaining counter there is no lobby signal (None): resets must last longer.
                    before = counters[name].state()
                    change = counters[name].update(t, value, lobby_open if "remaining" in counters else None)
                    if not change:
                        continue
                    if name == "elims":
                        last_change = (t, before, len(events), lobby_open)
                        events.extend(counter_events(change))
                        lobby_open = False
                    else:
                        remaining.append((round(change[0], 2), change[2]))
                        # A real new lobby jumps by dozens of players; 79 -> 80 is just a misread.
                        if ((change[1] is None and change[2] >= LOBBY_PLAYERS)
                                or (change[1] is not None and change[2] >= LOBBY_MIN_PLAYERS
                                    and change[2] - change[1] >= LOBBY_JUMP)):
                            lobby_open = True

            for name, region in regions.items():
                crop = crop_region(frame, region)
                ratio = text_ratio(crop)
                base = float(np.median(history[name])) if history[name] else ratio
                history[name].append(ratio)
                appeared = ratio > 0.003 and ratio > base * 1.5 + 0.002
                if (not appeared and t - last_read[name] < settings.ocr_every_s) or t - last_read[name] < BANNER_MIN_GAP_S:
                    continue
                last_read[name] = t
                ocr_calls += 1
                if name == "feed":
                    continue   # read on its own schedule below
                for text, conf, _ in ocr.lines(crop):
                    kind = classify(text, settings.player_names)
                    # The counter is the trusted source of the streamer's own kills.
                    if not kind or conf < 0.6 or (kind == "self_kill" and "elims" in counter_boxes):
                        continue
                    key = (kind, normalise(text)[:40])
                    if t - recent.get(key, -1e9) < DEDUPE_S:
                        recent[key] = t
                        continue
                    recent[key] = t
                    events.append({"t": round(t, 2), "kind": kind, "text": text, "region": name,
                                   "conf": round(conf, 3)})
            if feed_box and t - last_feed_read >= FEED_EVERY_S:
                crop = crop_region(frame, feed_box)
                if text_ratio(crop) >= 0.002:
                    last_feed_read = t
                    ocr_calls += 1
                    feed_reads += 1
                    lines = ocr.lines(crop)
                    for left, right in feed_rows(lines, crop.shape[1]):
                        if _is_name(left) and _is_name(right):
                            feed_full += 1
                        key = ("feed", f"{left} {right}"[:40])
                        if t - recent.get(key, -1e9) < DEDUPE_S:
                            continue
                        recent[key] = t
                        conf = min((c for _, c, _ in lines), default=0.0)
                        feed.append({"t": round(t, 2), "left": left, "right": right, "conf": round(conf, 3)})
                    if not feed_worth_reading(feed_reads, feed_full):
                        log(f"vision: kill feed unreadable in this layout ({feed_full} full rows in {feed_reads} reads), skipped from here")
                        feed_box = None
            if t >= next_report:
                kills = sum(e["kind"] == "self_kill" for e in events)
                log(f"vision: {t / 60:.0f} min scanned, {kills} kills, {len(events)} events")
                next_report += 600
            if checkpoint and t >= next_checkpoint:
                save_checkpoint()
                next_checkpoint += CHECKPOINT_EVERY_S
    finally:
        proc.stdout.close()
        proc.wait()

    if checkpoint:
        Path(checkpoint).unlink(missing_ok=True)
    player_name, extra = knocks_from_feed(feed, events, settings.player_names)
    events.extend(extra)
    if feed:
        log(f"vision: kill feed: {len(feed)} rows, streamer name {player_name!r}, "
            f"{sum(e['kind'] == 'self_knock' for e in extra)} knocks, {sum(e['kind'] == 'self_down' for e in extra)} downs")
    events.sort(key=lambda e: e["t"])
    return {"events": events, "remaining": remaining, "counter_boxes": counter_boxes, "frames": index,
            "ocr_calls": ocr_calls, "frame_size": [out_w, out_h], "feed_box": feed_box, "feed": feed,
            "player_name": player_name}
