"""The comedy cut (Highlights Stage 2, S2.4-S2.5): about 8 minutes of a stream's funny bits in stream order,
JokerClips style (plans/Highlights Stage 2 plan.md, decisions 1-5):

- an "IN THIS VIDEO" teaser of 3-5 punchlines from the body, 10-22 s, subtitled;
- the chosen units (aigcm.comedy.select), bits under 30 s apart in the stream joined into one block, cut on
  quiet moments out of words like the kill highlight;
- the face crop-zoomed on every unit's punchline, held for the sentence, when nobody is shooting;
- one subtitle per unit for its punchline line; the biggest lines also written big at the top;
- Kaatclip's own stickers (a word and an emoji, 1-3 s) on a few units; no film or TV meme clips;
- "2 SECONDS LATER…" cards on jumps of a few minutes inside a match;
- the ending on the last punchline, then 2 s of black.

The pieces use the kill highlight's piece format, so studio.highlight.render makes the video."""

import numpy as np

from .. import comedy
from ..safety import GAALI, SLURS
from . import highlight as hl

TEASER_BEATS = (3, 5)
TEASER_S = (10.0, 22.0)
BEAT_S = 5.0
LATER_CARD_S = (300.0, 900.0)   # a jump this long inside one match gets "2 SECONDS LATER…"...
LATER_MAX = 2                    # ...at most this often a video (JokerClips uses it now and then)
NEXT_DAY = "THE NEXT DAY…"
LATER = "2 SECONDS LATER…"
HEADLINE_MIN = 9                 # a punchline rated this high is also written big at the top
HEADLINE_S = 2.5
STICKERS_MAX = 6
STICKER_S = 2.0
STICKER_EMOJI = {"roast": "🔥", "banter": "😂", "rage": "😡", "fail": "💀", "story": "👀", "reaction": "😱",
                 "chat": "💬"}
FILLER_LABELS = {"", "BHAI", "BRO", "HA", "HAHA", "LOL"}


def clean(text):
    """Whether a line may be written on screen, in a title or on a Short: no gaali, no slurs. Bits with
    swearing can stay in the video (it's what the streamer said); their words are never put up in big text."""
    return bool(text) and not GAALI.search(text) and not SLURS.search(text)


def punchline(unit, transcript):
    """The sentence a unit lands on: the last transcript segment that ends inside it (start, end, text)."""
    best = None
    for seg in (transcript or {}).get("segments", []):
        a, b = seg.get("start"), seg.get("end")
        if a is None or b is None or b <= unit["start"] + 0.5 or a >= unit["end"]:
            continue
        if b <= unit["end"] + 0.5:
            best = (float(a), float(b), seg.get("text", "").strip())
    return best


def _in_match(t, stream_map):
    return next((m["n"] for m in (stream_map or {}).get("matches", []) if m["start"] <= t <= m["end"]), None)


def teaser(chosen, transcript, words, audio):
    """3-5 of the best punchlines, each a few seconds around its line, best last, under "IN THIS VIDEO"."""
    beats = []
    for u in sorted(chosen, key=lambda u: (-u["funny"], u["start"])):
        line = punchline(u, transcript)
        if not line or not clean(line[2]):
            continue                 # the teaser is subtitled, so only lines that can be written
        a = max(u["start"], line[1] - BEAT_S + 0.6)
        b = min(u["end"], line[1] + 0.6)
        if b - a < 2.0 or any(not (b <= x["start"] or a >= x["end"]) for x in beats):
            continue
        beats.append({"start": a, "end": b, "funny": u["funny"]})
        if len(beats) >= TEASER_BEATS[1] or sum(x["end"] - x["start"] for x in beats) >= TEASER_S[1] - 3:
            break
    if len(beats) < TEASER_BEATS[0]:
        return []
    beats.sort(key=lambda x: x["funny"])
    out = []
    for i, x in enumerate(beats):
        start = hl.first_sound(x["start"], words, np.array([])) if i == 0 else hl.settle(x["start"], "start", words, audio)
        out.append({"kind": "intro", "start": round(max(0.0, start), 2),
                    "end": round(hl.settle(x["end"], "end", words, audio), 2), "text": "", "why": "funny",
                    "captions": True, "sfx": [], "kills": 0})
    out[0]["label"] = "IN THIS VIDEO"
    return out


SINGLE_S = (480.0, 720.0)        # research rule 13: a match of 8-12 minutes...
SINGLE_SPEECH = 0.8              # ...with speech in 80% of its seconds...
SINGLE_BITS = 6                  # ...and at least this many bits rated 7+ is kept almost whole
DEAD_S = 5.0                     # inside it, only stretches this long with no words and no shooting are cut


def single_match(units, stream_map, words, spans=None):
    """The match to keep almost whole (research rule 13, JokerClips' "Gun Game duo": 9.6 min became 7.7), or
    None: 8-12 minutes, speech in 80%+ of its seconds, 6+ bits rated 7 or more. The densest one wins."""
    best = None
    for m in (stream_map or {}).get("matches", []):
        length = m["end"] - m["start"]
        if not SINGLE_S[0] <= length <= SINGLE_S[1]:
            continue
        if spans and not any(a <= m["start"] < b for a, b in spans):
            continue
        talk = np.zeros(int(length) + 1, bool)
        for a, b in words:
            if b > m["start"] and a < m["end"]:
                talk[max(0, int(a - m["start"])):min(len(talk), int(b - m["start"]) + 2)] = True
        bits = [u for u in units if u["funny"] >= 7 and m["start"] <= u["start"] <= m["end"]]
        if talk.mean() >= SINGLE_SPEECH and len(bits) >= SINGLE_BITS:
            if best is None or len(bits) > best[1]:
                best = (m, len(bits))
    return best[0] if best else None


def decorate(piece, units, transcript, shots, facecam, stickers):
    """A piece's face zooms, subtitles, headlines and stickers from the units inside it; returns how many
    stickers are now used."""
    start, end = piece["start"], piece["end"]
    punch, captions, overlays = [], [], []
    for u in units:
        line = punchline(u, transcript)
        if not line:
            continue
        a, b = max(line[0], start + 0.2), min(line[1], end - 0.2)
        if b - a < 0.8:
            continue
        if clean(line[2]):
            captions.append([round(a - start, 2), round(b + 0.2 - start, 2)])
        quiet = not (len(shots) and ((shots >= a - 1.0) & (shots <= b + 0.5)).any())
        if facecam and quiet and b - a >= hl.PUNCH_SENTENCE_S[0]:
            punch.append([round(a - 0.1, 2), round(min(b, a + hl.PUNCH_SENTENCE_S[1] + 2) + 0.2, 2)])
        if u["funny"] >= HEADLINE_MIN and clean(u.get("line")):
            overlays.append({"kind": "headline", "text": u["line"].upper(), "a": round(a - start, 2),
                             "b": round(min(b - start + 0.5, a - start + HEADLINE_S), 2)})
        label = (u.get("label") or "").upper()
        if stickers < STICKERS_MAX and label not in FILLER_LABELS and clean(label) and u["funny"] >= 7:
            emoji = STICKER_EMOJI.get(u.get("type"), "😂")
            overlays.append({"kind": "sticker", "text": f"{label} {emoji}", "a": round(max(0.0, a - start - 0.3), 2),
                             "b": round(a - start - 0.3 + STICKER_S, 2)})
            stickers += 1
    piece["captions"] = captions
    if punch:
        piece["punch"] = punch
    if overlays:
        piece["overlays"] = overlays
    return stickers


def _unit_piece(start, end, units, **extra):
    return dict({"kind": "unit", "start": start, "end": end, "kills": 0, "sfx": [], "zooms": [],
                 "funny": max([u["funny"] for u in units] or [0]),
                 "title": next((t for u in units for t in (u.get("line"), u.get("title")) if clean(t)), ""),
                 "units": [{k: u.get(k) for k in ("start", "end", "funny", "type", "line", "label", "source")}
                           for u in units]}, **extra)


def _finish(intro, body, stream_map, facecam, chosen, mode):
    if intro:
        first = next(p for p in body if p["kind"] != "card")
        first["sfx"] = [["whoosh", 0.0]]
    pieces = intro + body + [{"kind": "card", "text": "", "length": hl.END_BLACK_S}]
    total = sum(p.get("length") or (p["end"] - p["start"]) for p in pieces)
    own = [p for p in body if p["kind"] != "card" and not p.get("source")]
    kept = sum(p["end"] - p["start"] for p in own)
    span = own[-1]["end"] - own[0]["start"] if own else 0
    return {"style": "comedy", "mode": mode,
            "matches": sorted({m for p in own for m in [_in_match(p["start"], stream_map)] if m}),
            "pieces": pieces, "length": round(total, 1), "kept": round(kept / span, 3) if span else 0, "kills": 0,
            "units": len(chosen), "facecam": list(facecam) if facecam else None}


def plan_single(match, units, stream_map, duration, transcript, sounds, audio, facecam):
    """One talk-dense match kept almost whole: only dead stretches (5 s+ with no words and no shooting) cut, no
    teaser and no cards, ending on its result and the line said about it."""
    words = hl._words(transcript)
    kills = [t for f in match.get("fights") or [] for t in f.get("kill_times") or []]
    _, end, _ = hl.ending_span(match, words, duration)
    whole = {"kind": "unit", "start": match["start"], "end": end}
    dead = hl.quiet_spans(whole["start"], whole["end"], words, sounds, least=DEAD_S, kills=kills)
    shots = hl._shots(sounds, hl.GUNFIRE_QUIET)
    inside = [u for u in units if match["start"] <= u["start"] <= end]
    body, stickers = [], 0
    for part in hl.cut_out(whole, dead, keep=0.4):
        a = round(max(0.0, hl.settle(part["start"], "start", words, audio)), 2)
        b = round(min(duration, hl.settle(part["end"], "end", words, audio)), 2)
        mine = [u for u in inside if a <= (u["start"] + u["end"]) / 2 <= b]
        piece = _unit_piece(a, b, mine)
        stickers = decorate(piece, mine, transcript, shots, facecam, stickers)
        body.append(piece)
    return _finish([], [p for p in body if p["end"] - p["start"] > 1], stream_map, facecam, inside, "single_match")


def plan(units, stream_map, duration, transcript=None, sounds=None, audio=None, facecam=None, target=comedy.TARGET_S,
         spans=None, extra=None):
    """The comedy cut's piece list from the tidied units: teaser, blocks with their punch-ins, subtitles,
    headlines and stickers, cards on long jumps, black at the end. Same shape as highlight.plan(). A
    talk-dense 8-12 minute match is kept almost whole instead (plan_single). `extra` holds another stream's
    pieces when this one is thin (see next_day); they follow a "THE NEXT DAY…" card."""
    words = hl._words(transcript)
    match = single_match(units, stream_map, words, spans)
    if match is not None:
        return plan_single(match, units, stream_map, duration, transcript, sounds, audio, facecam)
    room = sum(p["end"] - p["start"] for p in extra or []) + (hl.CARD_S if extra else 0)
    # The teaser (about 15 s), cards and black come on top of the units.
    chosen = comedy.select(units, (target[0] - 25 - room, target[1] - 25 - room))
    if not chosen:
        raise ValueError("no funny bits were found in this stream")
    # Joined blocks keep a few seconds between their bits: drop the weakest bits until it fits.
    while len(chosen) > 3 and sum(b["end"] - b["start"] for b in comedy.blocks(chosen)) > target[1] - 20 - room:
        chosen.remove(min(chosen, key=lambda u: (u["funny"], -u["start"])))
    shots = hl._shots(sounds, hl.GUNFIRE_QUIET)
    body, stickers, later = [], 0, 0
    for block in comedy.blocks(chosen):
        start = round(max(0.0, hl.settle(block["start"], "start", words, audio)), 2)
        end = round(min(duration, hl.settle(block["end"], "end", words, audio)), 2)
        if body:
            prev = body[-1]
            gap = start - prev["end"]
            same = _in_match(start, stream_map) is not None and _in_match(start, stream_map) == _in_match(prev["end"], stream_map)
            if same and LATER_CARD_S[0] <= gap <= LATER_CARD_S[1] and later < LATER_MAX:
                body.append({"kind": "card", "text": LATER, "length": hl.CARD_S})
                later += 1
        piece = _unit_piece(start, end, block["units"])
        stickers = decorate(piece, block["units"], transcript, shots, facecam, stickers)
        body.append(piece)
    if extra:
        body.append({"kind": "card", "text": NEXT_DAY, "length": hl.CARD_S})
        body += extra
    intro = teaser(chosen, transcript, words, audio)
    return _finish(intro, body, stream_map, facecam, chosen, "two_streams" if extra else "session")


THIN_S = 360.0                   # owner default 3: a stream with under ~6 minutes of bits gets another's best


def thin(units, target=comedy.TARGET_S):
    """How many seconds the stream's own bits fall short of a thin stream's limit (0 when it has enough). Only
    bits rated 7+ count: a laugh heard with nothing readable around it (rated 6) is filler, not material."""
    good = [u for u in units if u["funny"] >= 7]
    have = sum(u["end"] - u["start"] for u in comedy.select(good, target))
    return 0.0 if have >= THIN_S else target[0] - 25 - have


def next_day(need, other):
    """Pieces from another stream of the same creator (decision 3: the last 3 weeks) for a thin stream: its
    best blocks, in its own stream order, up to `need` seconds, each carrying its own file, layout, camera
    box and transcript so the renderer can cut it. `other` is {"source", "info", "transcript", "sounds",
    "audio", "units", "facecam"}."""
    if need <= 0 or not other.get("units"):
        return []
    said, words = other.get("transcript"), hl._words(other.get("transcript"))
    chosen = comedy.select(other["units"], (need - 20, need))
    shots = hl._shots(other.get("sounds"), hl.GUNFIRE_QUIET)
    duration = other["info"].get("duration") or 1e9
    out, stickers = [], 0
    for block in comedy.blocks(chosen):
        a = round(max(0.0, hl.settle(block["start"], "start", words, other.get("audio"))), 2)
        b = round(min(duration, hl.settle(block["end"], "end", words, other.get("audio"))), 2)
        piece = _unit_piece(a, b, block["units"], source=str(other["source"]),
                            info={k: other["info"].get(k) for k in ("width", "height", "has_audio", "duration")},
                            facecam=list(other["facecam"]) if other.get("facecam") else None)
        stickers = decorate(piece, block["units"], said, shots, other.get("facecam"), stickers)
        piece["said"] = {"segments": [seg for seg in (said or {}).get("segments", [])
                                      if seg.get("end", 0) > a and seg.get("start", 0) < b]}
        out.append(piece)
    return out


# --- titles, Shorts -------------------------------------------------------------------------------------------

CONFLICT = {"roast": "ROASTED", "rage": "TRIGGERED", "banter": "KALESH", "fail": "FAIL", "story": "STORY TIME",
            "reaction": "SHOCKED", "chat": "VS CHAT"}
NOT_NAMES = FILLER_LABELS | {"CHAT", "RAGE", "NOOB", "LAG", "GG", "BOT", "HACKER", "DONATION", "UC", "LOOT", "SORRY",
                             "TEAM", "SQUAD", "ENEMY", "CAMPER", "PRO", "OMG", "WTF", "WOW", "NO", "YES"}


def mate(the_plan):
    """A teammate's name: a sticker label that looks like a name and comes up in two or more units."""
    from collections import Counter

    labels = Counter((u.get("label") or "").upper() for p in the_plan["pieces"] if p["kind"] == "unit"
                     for u in p.get("units") or [])
    names = [(n, c) for n, c in labels.items() if c >= 2 and n.isalpha() and len(n) >= 3 and n not in NOT_NAMES and clean(n)]
    return max(names, key=lambda x: x[1])[0] if names else None


def titles_for(the_plan, streamer=""):
    """Three titles in the JokerClips pattern (research rule 22, owner default 7: names only when said
    clearly): "[streamer] & [teammate] [conflict word] 😂", the best line, "[streamer] being [streamer]"."""
    from .. import titles

    units = [u for p in the_plan["pieces"] if p["kind"] == "unit" for u in p.get("units") or []]
    top = max((u for u in units if clean(u.get("line"))), key=lambda u: u["funny"], default=None)
    line = (top.get("line") or "").upper() if top else ""
    word = CONFLICT.get(top.get("type") if top else "", "KALESH")
    who, other = (streamer or "").upper().strip(), mate(the_plan)
    out = []
    if who and other:
        out.append(f"{who} & {other} {word} 😂 | FUNNY BGMI HIGHLIGHT")
    if line:
        out.append(f"\"{line}\" 😂 | FUNNY BGMI HIGHLIGHT")
    out.append(f"{who} BEING {who} FOR 8 MINUTES 😂 | BGMI" if who else f"8 MINUTES OF PURE {word} 😂 | BGMI FUNNY MOMENTS")
    out = [titles._cut(t, titles.LONG_MAX) for t in out]
    short = " ".join(line.split()[:4]) if line else "FUNNY MOMENTS"
    return out, [short, other or "FUNNY MOMENTS"]


def quote(the_plan, most_words=7):
    """The speech-bubble line for the thumbnail: the top punchline that may be written, shortened."""
    units = [u for p in the_plan["pieces"] if p["kind"] == "unit" for u in p.get("units") or [] if clean(u.get("line"))]
    top = max(units, key=lambda u: u["funny"], default=None)
    if not top:
        return None
    words = top["line"].strip().rstrip(".").split()
    return " ".join(words[:most_words]) + ("…" if len(words) > most_words else "")


def short_moments(units, transcript=None, words=(), most=3):
    """Shorts from the best units (person moments are what these are): 20-60 s, from the setup to the laugh,
    titled with the line in 2-6 words and one emoji (viewer rules 37, 42)."""
    out = []
    for u in sorted(units, key=lambda u: (-u["funny"], u["start"])):
        a, b = u["start"], u["end"]
        if b - a < hl.SHORT_AIM_S[0]:
            a = b - hl.SHORT_AIM_S[0]
        a = max(b - hl.SHORT_S[1], a)
        a = hl.first_sound(a, words, np.array([]), within=3.0)
        if any(not (b <= o["start"] or a >= o["end"]) for o in out):
            continue
        said = next((t for t in (u.get("line"), u.get("title")) if clean(t)), "")
        title = hl.band(said, STICKER_EMOJI.get(u.get("type"), "😂"))
        out.append({"role": "funny", "kind": "funny", "start": round(max(0.0, a), 2), "end": round(b, 2), "kills": 0,
                    "match": None, "title": title if title.strip("😂🔥😡💀👀😱💬 ") else "FUNNY MOMENT 😂"})
        if len(out) >= most:
            break
    if out:
        out[0]["role"] = "teaser"
    return out
