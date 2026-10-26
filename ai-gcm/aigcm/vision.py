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
import re
import subprocess
from collections import deque

import numpy as np

from .jobs import log
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
SPECTATE_EVERY_S = 2.0
SPECTATE_HOLD_S = 6.0
LOBBY_PLAYERS = 80        # Remaining at or above this means a fresh match
LOBBY_JUMP = 20
MAX_REMAINING_DROP = 30

COUNTER_LABELS = {"elims": "eliminations", "remaining": "remaining"}
COUNTER_SEARCH = (0.0, 0.0, 0.5, 0.12)   # top-left area searched for the counter labels
CALIBRATION_FRAMES = 24
# OCR confusions between letters and the HUD's condensed digits.
DIGIT_FIX = str.maketrans({"O": "0", "o": "0", "D": "0", "Q": "0", "U": "0", "I": "1", "l": "1", "|": "1",
                           "i": "1", "J": "1", "S": "5", "s": "5", "B": "8", "Z": "2", "z": "2", "G": "6",
                           "b": "6", "g": "9", "q": "9", "T": "7"})
MAX_KILL_JUMP = 5
ZERO_LIKE = set("口品回日囗〇OoDQ")


class Ocr:
    """RapidOCR on CPU. By default it enlarges small crops until their short side is 736 px, which makes a
    HUD strip take seconds; capping the long side instead keeps each read to a few tens of milliseconds.
    HUD text is never rotated, so the angle classifier is off."""

    def __init__(self):
        from rapidocr_onnxruntime import RapidOCR
        self.engine = RapidOCR(det_limit_type="max", det_limit_side_len=960, use_cls=False)

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


def frame_size(info, height):
    height = min(height, info["height"])
    return int(round(info["width"] * height / info["height"] / 2) * 2), height


def grab_frame(src, t, size):
    w, h = size
    cmd = [tool("ffmpeg"), "-v", "error", "-ss", f"{t:.2f}", "-i", str(src), "-frames:v", "1",
           "-vf", f"scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(h, w, 3) if len(raw) == w * h * 3 else None


def locate_counters(src, info, size, ocr):
    """Find the number box to the right of each counter label, as fractions of the frame. Labels are found
    on frames spread through the video and the median position is used, so a few bad reads don't matter."""
    w, h = size
    sx, sy, sw, sh = COUNTER_SEARCH
    found = {name: [] for name in COUNTER_LABELS}
    times = np.linspace(info["duration"] * 0.03, info["duration"] * 0.97, CALIBRATION_FRAMES)
    for t in times:
        frame = grab_frame(src, float(t), size)
        if frame is None:
            continue
        for text, _, (x0, y0, x1, y1) in ocr.lines(crop_region(frame, COUNTER_SEARCH)):
            letters = re.sub(r"[^a-z]", "", text.lower())
            if re.search(r"\d", text) or len(letters) < 6:
                continue  # merged with its number, so the label's right edge is unreliable
            for name, label in COUNTER_LABELS.items():
                if difflib.SequenceMatcher(None, letters, label).ratio() >= 0.6:
                    # Detection boxes are padded, so the number starts right at the label box's edge.
                    lh = y1 - y0
                    box = (sx * w + x1, sy * h + (y0 + y1) / 2 - 0.7 * lh, 2.2 * lh, 1.4 * lh)
                    found[name].append(box)
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

    def __init__(self, kind):
        self.kind = kind
        self.value = None
        self.pending, self.pending_t, self.pending_n = None, None, 0

    def _reads_needed(self, old, value, fresh_match):
        """How many agreeing reads a change needs; None means never accept it."""
        if old is None:
            return 2
        if self.kind == "elims":
            if 0 < value - old <= MAX_KILL_JUMP:
                return 2
            if value < old:
                # Eliminations never go down within a match. A drop is a teammate's counter (spectating),
                # a transition screen or a misread, unless a new lobby has opened.
                return 2 if fresh_match and value == 0 else None
            return 6
        return 2 if 0 < old - value <= MAX_REMAINING_DROP or value >= LOBBY_PLAYERS else 6

    def update(self, t, value, fresh_match=True):
        """Returns (time first seen, old value, new value) when the value changes, else None."""
        if value is None or (self.kind == "remaining" and value == 0):
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
            self.value, self.pending = value, None
            return self.pending_t, old, value
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


def scan(src, info, settings):
    fps = settings.vision_fps
    size = frame_size(info, settings.vision_height)
    out_w, out_h = size
    ocr = Ocr()
    counter_boxes = locate_counters(src, info, size, ocr)

    cmd = [tool("ffmpeg"), "-v", "error", "-i", str(src), "-vf", f"fps={fps},scale={out_w}:{out_h}",
           "-f", "rawvideo", "-pix_fmt", "bgr24", "-"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    frame_bytes = out_w * out_h * 3

    counters = {name: Counter(name) for name in counter_boxes}
    remaining = []          # [(t, players left)] whenever it changes
    spectating_until, last_spectate_read = -1.0, -1e9
    lobby_open = False      # the Remaining counter jumped to a fresh lobby since the last Eliminations change
    history = {name: deque(maxlen=int(fps * 10)) for name in settings.regions}
    last_read = {name: -1e9 for name in settings.regions}
    recent = {}
    events, ocr_calls, index = [], 0, 0
    next_report = 600

    try:
        while True:
            buf = proc.stdout.read(frame_bytes)
            if len(buf) < frame_bytes:
                break
            frame = np.frombuffer(buf, np.uint8).reshape(out_h, out_w, 3)
            t = index / fps
            index += 1

            if "elims" in counter_boxes and t - last_spectate_read >= SPECTATE_EVERY_S:
                last_spectate_read = t
                ocr_calls += 1
                if any(is_spectating(text) for text, _, _ in ocr.lines(crop_region(frame, SPECTATE_REGION))):
                    spectating_until = t + SPECTATE_HOLD_S
            spectating = t < spectating_until

            if counter_boxes:
                names = [n for n in counter_boxes if not (n == "elims" and spectating)]
                reads = ocr.read_digits(crop_region(frame, counter_boxes[n]) for n in names)
                for name, (text, conf) in zip(names, reads):
                    value = parse_number(text) if conf >= 0.2 else None
                    # Without a Remaining counter there is no lobby signal, so resets are always allowed.
                    change = counters[name].update(t, value, lobby_open or "remaining" not in counters)
                    if not change:
                        continue
                    if name == "elims":
                        events.extend(counter_events(change))
                        lobby_open = False
                    else:
                        remaining.append((round(change[0], 2), change[2]))
                        # A real new lobby jumps by dozens of players; 79 -> 80 is just a misread.
                        if change[2] >= LOBBY_PLAYERS and (change[1] is None or change[2] - change[1] >= LOBBY_JUMP):
                            lobby_open = True

            for name, region in settings.regions.items():
                crop = crop_region(frame, region)
                ratio = text_ratio(crop)
                base = float(np.median(history[name])) if history[name] else ratio
                history[name].append(ratio)
                appeared = ratio > 0.003 and ratio > base * 1.5 + 0.002
                if not appeared and t - last_read[name] < settings.ocr_every_s:
                    continue
                last_read[name] = t
                ocr_calls += 1
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
            if t >= next_report:
                kills = sum(e["kind"] == "self_kill" for e in events)
                log(f"vision: {t / 60:.0f} min scanned, {kills} kills, {len(events)} events")
                next_report += 600
    finally:
        proc.stdout.close()
        proc.wait()

    events.sort(key=lambda e: e["t"])
    return {"events": events, "remaining": remaining, "counter_boxes": counter_boxes, "frames": index,
            "ocr_calls": ocr_calls, "frame_size": [out_w, out_h]}
