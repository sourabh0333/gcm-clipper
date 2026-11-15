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
LATER_CARD_S = (120.0, 900.0)   # a jump this long inside one match gets "2 SECONDS LATER…"
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


def plan(units, stream_map, duration, transcript=None, sounds=None, audio=None, facecam=None, target=comedy.TARGET_S):
    """The comedy cut's piece list from the tidied units: teaser, blocks with their punch-ins, subtitles,
    headlines and stickers, cards on long jumps, black at the end. Same shape as highlight.plan()."""
    words = hl._words(transcript)
    # The teaser (about 15 s), cards and black come on top of the units.
    chosen = comedy.select(units, (target[0] - 25, target[1] - 25))
    if not chosen:
        raise ValueError("no funny bits were found in this stream")
    shots = hl._shots(sounds, hl.GUNFIRE_QUIET)
    body, stickers = [], 0
    for k, block in enumerate(comedy.blocks(chosen)):
        start = round(max(0.0, hl.settle(block["start"], "start", words, audio)), 2)
        end = round(min(duration, hl.settle(block["end"], "end", words, audio)), 2)
        if body:
            prev = body[-1]
            gap = start - prev["end"]
            same = _in_match(start, stream_map) is not None and _in_match(start, stream_map) == _in_match(prev["end"], stream_map)
            if same and LATER_CARD_S[0] <= gap <= LATER_CARD_S[1]:
                body.append({"kind": "card", "text": LATER, "length": hl.CARD_S})
        piece = {"kind": "unit", "start": start, "end": end, "kills": 0, "sfx": [], "zooms": [],
                 "funny": max(u["funny"] for u in block["units"]),
                 "title": next((t for u in block["units"] for t in (u.get("line"), u.get("title")) if clean(t)), ""),
                 "units": [{k2: u.get(k2) for k2 in ("start", "end", "funny", "type", "line", "label", "source")}
                           for u in block["units"]]}
        punch, captions, overlays = [], [], []
        for u in block["units"]:
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
        body.append(piece)
    intro = teaser(chosen, transcript, words, audio)
    if intro:
        first = next(p for p in body if p["kind"] != "card")
        first["sfx"] = [["whoosh", 0.0]]
    pieces = intro + body + [{"kind": "card", "text": "", "length": hl.END_BLACK_S}]
    total = sum(p.get("length") or (p["end"] - p["start"]) for p in pieces)
    units_only = [p for p in body if p["kind"] != "card"]
    kept = sum(p["end"] - p["start"] for p in units_only)
    span = units_only[-1]["end"] - units_only[0]["start"]
    return {"style": "comedy", "matches": sorted({m for p in body if p["kind"] == "unit"
                                                 for m in [_in_match(p["start"], stream_map)] if m}),
            "pieces": pieces, "length": round(total, 1), "kept": round(kept / span, 3) if span else 0, "kills": 0,
            "units": len(chosen), "facecam": list(facecam) if facecam else None}


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
