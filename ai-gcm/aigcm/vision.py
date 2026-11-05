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
SPECTATE_EVERY_S = 1.0   # at most one Spectating check a second while the counter looks different
SPECTATE_HOLD_S = 6.0
LOBBY_PLAYERS = 80        # Remaining at or above this means a fresh match
LOBBY_JUMP = 20
MAX_PLAYERS = 100
UNCONFIRMED_RESET_S = 10.0   # how long a reset must hold when there is no lobby signal
BANNER_MIN_GAP_S = 3.0       # message text is read at most this often, even while it keeps appearing
MAX_REMAINING_DROP = 30

COUNTER_LABELS = {"elims": "eliminations", "remaining": "remaining"}
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
        boxes = _locate_counters(src, info, size, ocr, (0.0, 0.0, 1.0, 1.0), ocr.lines_hires, frames=12)
    return boxes


def icon_row(lines, frame_w, frame_h, search=ICON_SEARCH):
    """Counter boxes for BGMI's compact HUD from OCR lines of the search crop. The row is three fixed-width
    cells, each an icon with its number right-aligned (person 36 | crosshair 20 | wings 2). OCR usually reads
    the whole row as one line ("236202", icons included), and the ends of that line are stable, so the
    numbers are placed from the row's extent: cell width is a third of it, and each number ends a little
    before its cell's right edge. Returns {"remaining": box, "elims": box} in frame fractions, or {}."""
    sx, sy, sw, sh = search
    for text, conf, (x0, y0, x1, y1) in lines:
        digits = sum(ch.isdigit() for ch in text.translate(DIGIT_FIX))
        lh = y1 - y0
        if digits >= 4 and x1 - x0 >= 5 * lh and lh >= 8 and conf >= 0.5:
            cell = (x1 - x0) / 3
            boxes = {}
            for k, name in enumerate(("remaining", "elims")):
                right = x1 - (2 - k) * cell - 0.2 * lh
                boxes[name] = ((sx * frame_w + right - ICON_NUMBER_W * lh) / frame_w,
                               max(0.0, (sy * frame_h + y0 - 0.1 * lh) / frame_h),
                               (ICON_NUMBER_W * lh) / frame_w, (lh * 1.2) / frame_h)
            return boxes
    return {}


def _locate_icon_counters(src, info, size, ocr, frames=12):
    w, h = size
    found = {"remaining": [], "elims": []}
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


def _locate_counters(src, info, size, ocr, search, read, frames=CALIBRATION_FRAMES):
    w, h = size
    sx, sy, sw, sh = search
    found = {name: [] for name in COUNTER_LABELS}
    times = np.linspace(info["duration"] * 0.03, info["duration"] * 0.97, frames)
    for t in times:
        frame = grab_frame(src, float(t), size)
        if frame is None:
            continue
        for text, _, (x0, y0, x1, y1) in read(crop_region(frame, search)):
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
                return 2
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
    # Vertical streams put the gameplay window anywhere, so the whole frame is checked there.
    spectate_region = (0.0, 0.0, 1.0, 1.0) if out_h > out_w else SPECTATE_REGION
    lobby_open = False      # the Remaining counter jumped to a fresh lobby since the last Eliminations change
    history = {name: deque(maxlen=int(fps * 10)) for name in settings.regions}
    last_read = {name: -1e9 for name in settings.regions}
    recent = {}
    events, ocr_calls, index = [], 0, 0
    next_report = 600
    if saved:
        for name, state in saved["counters"].items():
            counters[name].restore(state)
        remaining = [tuple(r) for r in saved["remaining"]]
        spectating_until, last_spectate_read = saved["spectating_until"], saved["last_spectate_read"]
        lobby_open, last_read = saved["lobby_open"], saved["last_read"]
        recent = {(kind, text): t for kind, text, t in saved["recent"]}
        events, ocr_calls, index, next_report = saved["events"], saved["ocr_calls"], saved["index"], saved["next_report"]
        log(f"vision: resuming at {index / fps / 60:.0f} min from the checkpoint")
    next_checkpoint = index / fps + CHECKPOINT_EVERY_S

    def save_checkpoint():
        write_json(checkpoint, {
            "source": [str(src), info["duration"], fps], "counter_boxes": counter_boxes,
            "counters": {name: c.state() for name, c in counters.items()}, "remaining": remaining,
            "spectating_until": spectating_until, "last_spectate_read": last_spectate_read,
            "lobby_open": lobby_open, "last_read": last_read,
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
                    if name == "elims" and value is not None and value != counters[name].value:
                        # Only a changing counter can be a teammate's, so "Spectating" is looked for only
                        # then: a whole-frame read every few seconds tripled the time on vertical streams.
                        if t >= spectating_until and t - last_spectate_read >= SPECTATE_EVERY_S:
                            last_spectate_read = t
                            ocr_calls += 1
                            if any(is_spectating(line) for line, _, _ in
                                   ocr.lines(crop_region(frame, spectate_region))):
                                spectating_until = t + SPECTATE_HOLD_S
                        if t < spectating_until:
                            continue
                    # Without a Remaining counter there is no lobby signal (None): resets must last longer.
                    change = counters[name].update(t, value, lobby_open if "remaining" in counters else None)
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
                if (not appeared and t - last_read[name] < settings.ocr_every_s) or t - last_read[name] < BANNER_MIN_GAP_S:
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
            if checkpoint and t >= next_checkpoint:
                save_checkpoint()
                next_checkpoint += CHECKPOINT_EVERY_S
    finally:
        proc.stdout.close()
        proc.wait()

    if checkpoint:
        Path(checkpoint).unlink(missing_ok=True)
    events.sort(key=lambda e: e["t"])
    return {"events": events, "remaining": remaining, "counter_boxes": counter_boxes, "frames": index,
            "ocr_calls": ocr_calls, "frame_size": [out_w, out_h]}
