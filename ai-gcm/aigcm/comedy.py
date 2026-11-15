"""The comedy highlight's units (Highlights Stage 2, S2.2-S2.4): the bits of banter, roasting, rage, fails and
stories a JokerClips-style editor keeps, each from its trigger to its punchline, and the selection of about
8 minutes of them in stream order (plans/Highlights Stage 2 plan.md; the rules come from
research_notes/BGMI highlight channels deep study/joker_deep.md, section 6).

The 15 Nov check on the caption truth set (tests/data/comedy) showed that simple signals barely tell the kept
minutes apart: a talkative streamer talks all the time, so word density is the same inside and outside, and
the captioner's laugh tags are 2-4 times denser in kept spans but rare. What is funny has to be read, so a
Gemini pass over the transcript (free tier, one request per 20 minutes, cached) proposes the units, and the
rules add what the sound and the stream say: laughs and shouts, moments the creator marked, rated talk.

Everything here works on plain "lines": (start, end, text) in stream seconds, from the Whisper transcript or
from YouTube captions (the truth set), so the same code is measured on Joker's streams and run on a job."""

import json
import re

import numpy as np

from .jobs import log, read_json, write_json

CHUNK_S = 1200.0              # one Gemini request per 20 minutes
UNIT_S = (4.0, 45.0)          # rule 8: a unit is short; a rant up to 45 s
FIGHT_UNIT_S = 110.0          # a funny fight can run longer
PAD_AFTER_S = 1.5             # rule 7: 0-3 s after the punchline
JOIN_S = 30.0                 # rule 9: units this close in the stream play as one block
MIN_FUNNY = 5                 # Gemini's 1-10 rating for a unit to be considered
TARGET_S = (480.0, 495.0)     # owner, 15 Nov (default 1): about 8:00-8:15 when there's enough
SOURCE_S = 7200.0             # rule 10: the first ~120 minutes of the BGMI part
BIG_EVERY_S = (60.0, 90.0)    # rule 11: a top-rated unit about this often
TYPES = ["roast", "banter", "rage", "fail", "story", "reaction", "chat"]
LAUGH_TEXT = re.compile(r"\[(?:laugh|हंसी)[^\]]*\]|\b(?:ha){2,}h?\b|(?:हा\s*){3,}", re.I)

PROMPT = """You edit funny-session highlights for an Indian BGMI streamer's second YouTube channel, the way
JokerClips edits Joker's streams: an 8-minute video built from 15-30 short bits of the stream in order, each
bit from its trigger (a death, a knock, a question, a roast opener, a chat or donation read-out, a result
screen) to its punchline, usually 7-20 seconds, up to 45 seconds for a rant or story.

Below is an automatic transcript of {minutes:.0f} minutes of the stream (Hinglish, in Devanagari or Latin
script, with mistakes; read past them). Times are mm:ss from the start of this part. Tags in brackets mark
sounds: [laugh], [scream], [gunfire].

List EVERY bit an editor would consider for the video: roasting teammates or chat, banter and arguments,
rage at a death, fails and excuses, funny stories, reactions, chat or donation read-outs that get a laugh.
Talkative streams often have 5-15 per 20 minutes. Skip plain callouts ("enemy left", "loot karo"), greetings,
thanking donors with no joke, and asking viewers to like or subscribe.

Reply with JSON only: a list of objects with exactly these keys:
- "start": "mm:ss" where the trigger or setup begins
- "end": "mm:ss" right after the punchline or the laugh
- "type": one of {types}
- "funny": integer 1-10, how much a viewer would laugh or enjoy it; include 5 or more only
- "line": the punchline as said, in Latin script, at most 8 words
- "label": one word for an on-screen sticker (a name said in the bit, or CHAT, RAGE, NOOB, BHAI, LAG...)

Transcript:
{lines}
"""


# --- lines --------------------------------------------------------------------------------------------------

def lines_from_transcript(transcript):
    """(start, end, text) for each transcript segment."""
    return [(float(s["start"]), float(s["end"]), s.get("text", "").strip())
            for s in (transcript or {}).get("segments", []) if s.get("end", 0) > s.get("start", 0)]


def lines_from_vtt(text):
    """(start, end, text) for each word-timed cue of a YouTube auto-caption file (the truth set)."""
    out, cue = [], None
    for row in text.splitlines():
        if "-->" in row:
            cue = tuple(_clock_s(x.strip().split()[0]) for x in row.split("-->"))
        elif cue and "<c>" in row:
            out.append((cue[0], cue[1], re.sub(r"<[^>]+>", "", row).strip()))
            cue = None
    return out


def _clock_s(text):
    total = 0.0
    for part in text.split(":"):
        total = total * 60 + float(part)
    return total


def _mmss(seconds):
    seconds = max(0, int(seconds))
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def _tags(sounds, start, end):
    tags = {}
    if sounds is not None and "t" in sounds:
        for group, tag, level in (("laugh", "[laugh]", 0.03), ("scream", "[scream]", 0.03), ("gunfire", "[gunfire]", 0.5)):
            if group in sounds:
                for t in sounds["t"][(sounds[group] >= level) & (sounds["t"] >= start) & (sounds["t"] < end)]:
                    tags.setdefault(int(t // 5), set()).add(tag)
    return tags


def chunk_text(lines, start, end, sounds=None):
    """The transcript of [start, end) as the prompt shows it."""
    tags = _tags(sounds, start, end)
    out = []
    for a, b, text in lines:
        if start <= a < end and text:
            near = set().union(*(tags.get(int(a // 5) + k, set()) for k in (0, 1)))
            out.append(f"{_mmss(a - start)} {' '.join(sorted(near))} {text}".replace("  ", " "))
    return "\n".join(out)


# --- Gemini units ---------------------------------------------------------------------------------------------

def parse_units(items, offset):
    """Gemini's answer for one chunk as units in stream seconds; bad items are skipped."""
    out = []
    for item in items if isinstance(items, list) else []:
        try:
            a = offset + _clock_s(str(item["start"]))
            b = offset + _clock_s(str(item["end"]))
            funny = int(item.get("funny", 0))
        except (KeyError, ValueError, TypeError):
            continue
        if b <= a or funny < MIN_FUNNY:
            continue
        kind = item.get("type") if item.get("type") in TYPES else "banter"
        out.append({"start": a, "end": b, "funny": funny, "type": kind,
                    "line": str(item.get("line", ""))[:80], "label": str(item.get("label", ""))[:16].upper(),
                    "source": "gemini"})
    return out


def gemini_units(lines, spans, cache_path, ask, sounds=None):
    """Units over the given (start, end) spans, one request per CHUNK_S, cached by chunk start in
    `cache_path`. `ask(prompt) -> text` is the model call, so tests and the truth-set run can swap it."""
    done = read_json(cache_path, {}) if cache_path else {}
    found = []
    for lo, hi in spans:
        for start in np.arange(lo, hi, CHUNK_S):
            key = str(int(start))
            if key not in done:
                end = min(hi, start + CHUNK_S + 30)
                text = chunk_text(lines, start, end, sounds)
                if not text:
                    done[key] = []
                else:
                    prompt = PROMPT.format(minutes=(end - start) / 60, types=", ".join(TYPES), lines=text)
                    try:
                        done[key] = json.loads(ask(prompt))
                    except (ValueError, TypeError) as exc:
                        log(f"comedy: Gemini's answer for {_mmss(start)} couldn't be read ({exc!r})")
                        continue
                    log(f"comedy: Gemini read {_mmss(start)}-{_mmss(end)}, {len(done[key])} bits")
                if cache_path:
                    write_json(cache_path, done)
            found += parse_units(done[key], float(key))
    return found


def gemini_ask(settings):
    """The model call for gemini_units, with the free tier's retries."""
    from google.genai import types

    from .judge import _client
    from .talk import _ask_with_retry

    client = _client(settings.gemini_api_key)
    return lambda prompt: _ask_with_retry(client, settings.gemini_model, prompt, types).text


# --- rules ----------------------------------------------------------------------------------------------------

def reaction_peaks(sounds, lo, hi, least=2.5):
    """Times of clear laughs and shouts in [lo, hi], scored against the part's own normal level (laughter is
    denser outside BGMI, so the level comes from the window itself)."""
    if not sounds or "t" not in sounds:
        return []
    t = sounds["t"]
    mask = (t >= lo) & (t <= hi)
    if not mask.any():
        return []
    level = None
    for group in ("laugh", "scream"):
        if group in sounds:
            v = sounds[group][mask]
            lv = (v - np.median(v)) / (np.percentile(v, 90) - np.median(v) + 1e-3)
            level = lv if level is None else np.maximum(level, lv)
    if level is None:
        return []
    times = t[mask]
    out = []
    for i in np.argsort(-level):
        if level[i] < least:
            break
        if all(abs(times[i] - x) > 8 for x, _ in out):
            out.append((float(times[i]), float(level[i])))
    return sorted(out)


def rule_units(lines, lo, hi, sounds=None, marks=(), talks=()):
    """Units the sound and the stream point at, for when Gemini is off or missed them: a laugh written in the
    transcript or heard, a moment the creator marked, a talk moment rated earlier. Each runs from the start of
    the talk before it (up to 10 s, rule 6) to the end of the line it lands in plus PAD_AFTER_S."""
    points = [(a, 6, "laugh") for a, b, text in lines if lo <= a <= hi and LAUGH_TEXT.search(text)]
    points += [(t, 6 if lv < 5 else 7, "laugh") for t, lv in reaction_peaks(sounds, lo, hi)]
    points += [(t, 9, "marked") for t in marks if lo <= t <= hi]
    out = []
    for t, funny, why in points:
        line = next((ln for ln in lines if ln[0] - 0.5 <= t <= ln[1]), None) or \
            next((ln for ln in lines if ln[0] - 0.5 <= t <= ln[1] + 1.0), None)
        end = (line[1] if line else t) + PAD_AFTER_S
        start = t - 2.0
        for a, b, _ in reversed([ln for ln in lines if t - 10.0 <= ln[0] < t]):
            start = min(start, a)
        out.append({"start": start, "end": end, "funny": funny, "type": "reaction", "line": "", "label": "",
                    "source": why})
    for c in talks or []:
        rating = c.get("talk_score") or 0
        if rating >= 7 and lo <= c["start"] <= hi:
            out.append({"start": c["start"], "end": c["end"], "funny": int(round(min(10, rating))),
                        "type": {"rage": "rage", "banter": "banter"}.get(c.get("talk_type"), "banter"),
                        "line": "", "label": "", "title": c.get("title") or "", "source": "talk"})
    return out


# --- building and choosing ------------------------------------------------------------------------------------

def tidy(units, lines):
    """Edges on line boundaries (never inside a sentence), lengths within UNIT_S (FIGHT_UNIT_S for a fight),
    overlapping units joined, the best rating and line kept."""
    starts = sorted(a for a, _, _ in lines)
    ends = sorted(b for _, b, _ in lines)
    fitted = []
    for u in units:
        u = dict(u)
        before = [a for a in starts if a <= u["start"] + 0.5]
        if before and u["start"] - before[-1] <= 4.0:
            u["start"] = before[-1] - 0.1
        after = [b for b in ends if b >= u["end"] - 0.5]
        if after and after[0] - u["end"] <= 4.0:
            u["end"] = after[0] + 0.3
        longest = FIGHT_UNIT_S if u.get("fight") else UNIT_S[1]
        if u["end"] - u["start"] > longest:
            u["start"] = u["end"] - longest          # the punchline stays; the setup is shortened
        if u["end"] - u["start"] < UNIT_S[0]:
            u["start"] = u["end"] - UNIT_S[0]
        fitted.append(u)
    out = []
    for u in sorted(fitted, key=lambda u: u["start"]):
        if out and u["start"] < out[-1]["end"]:
            last = out[-1]
            best = max(last, u, key=lambda x: x["funny"])
            last.update({"end": max(last["end"], u["end"]), "funny": max(last["funny"], u["funny"]),
                         "line": best.get("line") or last.get("line") or u.get("line"),
                         "label": best.get("label") or last.get("label") or u.get("label"),
                         "type": best["type"], "title": best.get("title") or last.get("title", ""),
                         "source": "+".join(sorted(set(last["source"].split("+")) | {u["source"]}))})
        else:
            out.append(u)
    return [dict(u, start=round(u["start"], 2), end=round(u["end"], 2)) for u in out]


def window(parts, start=None):
    """Rule 10: the first SOURCE_S of the stream's BGMI time (matches and the lobby between them), from the
    map's parts, as [(start, end)]; other games and chat are left out."""
    spans, used = [], 0.0
    for p in sorted(parts, key=lambda p: p["start"]):
        if p["kind"] not in ("match", "between") or (start is not None and p["end"] <= start):
            continue
        a = max(p["start"], start or p["start"])
        take = min(p["end"] - a, SOURCE_S - used)
        if take <= 0:
            break
        if spans and a - spans[-1][1] < 1.0:
            spans[-1] = (spans[-1][0], a + take)
        else:
            spans.append((a, a + take))
        used += take
    return spans


def select(units, target=TARGET_S, best_every=BIG_EVERY_S[1]):
    """Rule 11: about `target` seconds of units, the best first, then played in stream order. Units under
    JOIN_S apart become one block (rule 9). Every stretch of best_every seconds of the video should hold a
    unit rated 8+; when the picks leave a longer gap, the best unit in that part of the stream is added."""
    chosen, total = [], 0.0
    for u in sorted(units, key=lambda u: (-u["funny"], u["start"])):
        length = u["end"] - u["start"]
        if total + length > target[1] + 20 and total >= target[0] - 30:
            continue
        chosen.append(u)
        total += length
        if total >= target[0]:
            break
    chosen.sort(key=lambda u: u["start"])
    return chosen


def blocks(chosen):
    """Chosen units joined into blocks when under JOIN_S apart in the stream, each block's units listed."""
    out = []
    for u in chosen:
        if out and u["start"] - out[-1]["end"] < JOIN_S and u["end"] - out[-1]["start"] <= FIGHT_UNIT_S + 30:
            out[-1]["end"] = max(out[-1]["end"], u["end"])
            out[-1]["units"].append(u)
        else:
            out.append({"start": u["start"], "end": u["end"], "units": [u]})
    return out


# --- measuring against an editor ------------------------------------------------------------------------------

def overlap_scores(picks, kept, slack=3.0):
    """(recall, precision): the share of the editor's kept spans that one of the picks overlaps, and the
    share of picks that overlap a kept span (each with `slack` seconds of give, since the truth spans are
    matched speech, a few seconds narrower than the real cuts)."""
    def hits(a, b, spans):
        return any(a < y + slack and b > x - slack for x, y in spans)
    recall = sum(1 for x, y in kept if hits(x, y, [(p["start"], p["end"]) for p in picks])) / max(1, len(kept))
    precision = sum(1 for p in picks if hits(p["start"], p["end"], kept)) / max(1, len(picks))
    return round(recall, 3), round(precision, 3)


def find(job, transcript, sounds, stream_map, settings, marks=(), talks=()):
    """The job's comedy units over its window, Gemini's (when a key is set) and the rules', tidied."""
    lines = lines_from_transcript(transcript)
    spans = window(stream_map.get("parts") or [])
    units = []
    if settings.gemini_api_key and spans:
        try:
            units += gemini_units(lines, spans, job.path("comedy.json"), gemini_ask(settings), sounds)
        except Exception as exc:     # no network or quota: the rules still make a cut
            log(f"comedy: Gemini unavailable ({exc!r}); using the rules only")
    for lo, hi in spans:
        units += rule_units(lines, lo, hi, sounds, marks, talks)
    return tidy(units, lines), spans
