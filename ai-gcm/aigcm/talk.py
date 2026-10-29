"""Moments worth clipping for what is said rather than what is shot: jokes, roasts, banter with teammates,
rage, hype. Kills show up on the HUD; these only show up in the voices.

Two ways to find them:
- Rules, always: laughing or screaming in the audio, laughter written in the transcript ("haha"), a burst
  of loudness, and fast back-and-forth talk, each scored relative to the stream's own normal level.
- Gemini's free tier, when a key is set: it reads the whole transcript, with the sound detector's laughs,
  screams and gunfire marked in, and picks the moments a viewer would enjoy. One text request per 20
  minutes of stream; the answer is cached in talk.json.

Each moment's edges are moved to sentence boundaries, so the setup and the punchline both make it in.
"""

import json
import re

import numpy as np

from .jobs import log, read_json, write_json

LAUGH_TEXT = re.compile(r"\b(?:ha){2,}h?\b|\bhe(?:he)+\b|\bhihi+\b|\blol\b|\blmao\b", re.I)
# Fast exchanges and calling people out carry banter; these words mark it in Hinglish streams.
BANTER_TEXT = re.compile(r"\b(?:abe|oye|pagal|noob|nub|bakwas|chup|kya kar raha|kya kar rahe|kya hua|"
                         r"sorry|sori|bhaag|bachao|oh my god|what the|camper|campar|bachcha|bewakoof|"
                         r"kamina|kameena|saala|saale)\b", re.I)
# Swearing and insults mark rage and roasts, which streamers' audiences clip often. The transcript spells
# them loosely ("chhuttiyaan"), so these match on word stems.
RAGE_TEXT = re.compile(r"\b(?:ch+u+t+i*y|bhen?ch|behen ?ke|madar|maa ki|gaand|gandu|bsdk|bc\b|mc\b)", re.I)
SPIKE_FLOOR = 0.01
WINDOW_S = 10.0
STEP_S = 2.0
PEAK_GAP_S = 45.0
MIN_SCORE = 3.0
SETUP_S = 20.0
AFTER_S = 8.0
MAX_TALK_S = 45.0
LLM_CHUNK_S = 1200
TYPES = ["funny", "banter", "rage", "hype", "wholesome", "story"]

PROMPT = """You are a short-form video editor for an Indian BGMI (Battlegrounds Mobile India) streamer.
Below is an automatic transcript of {minutes:.0f} minutes of their livestream, in Hinglish. Times are
mm:ss from the start of this part. Tags in brackets come from a sound detector: [laugh], [scream] and
[gunfire] mark when those sounds were heard. The transcript has mistakes; read past them.

Find the moments a viewer would enjoy as a 15-45 second YouTube Short for what is SAID: jokes, roasting
teammates, funny excuses or fails, rage, banter, hype, wholesome moments. Skip plain callouts ("enemy left",
"loot karo"), greetings, and asking viewers to subscribe. Most streams have only a few such moments; an empty
list is a fine answer.

Reply with JSON only: a list of objects with exactly these keys:
- "start": "mm:ss" where the setup begins
- "end": "mm:ss" after the punchline or reaction
- "type": one of {types}
- "worth": integer 1-10, how likely the creator would post it; only include 6 or more
- "title": short catchy title in Hinglish (Latin script)
- "why": one English sentence on what is funny or entertaining

Transcript:
{lines}
"""


def _clock(seconds):
    return f"{int(seconds) // 60:02d}:{int(seconds) % 60:02d}"


def _seconds(text):
    minutes, _, seconds = str(text).strip().partition(":")
    return int(minutes) * 60 + float(seconds or 0)


def _series(sounds, group, grid):
    if sounds is None or group not in sounds or not len(sounds["t"]):
        return np.zeros(len(grid))
    return np.interp(grid, sounds["t"], sounds[group])


def _spikes(values):
    """How far each value rises above the stream's normal level, in units of its spread."""
    base = float(np.percentile(values, 50))
    # A floor on the spread, so near-silent noise (laugh scores of 0.002) doesn't count as a spike.
    spread = max(float(np.percentile(values, 95)) - base, SPIKE_FLOOR)
    return np.clip((values - base) / spread - 1.0, 0.0, 3.0)


def rule_scores(transcript, sounds, audio, duration):
    """A score every STEP_S seconds for how lively the talk around that time is, plus the reasons."""
    grid = np.arange(0.0, max(duration, STEP_S), STEP_S)
    laugh = _spikes(_series(sounds, "laugh", grid))
    scream = _spikes(_series(sounds, "scream", grid))
    excited = np.interp(grid, audio["t"], audio["excitement"]) if len(audio["t"]) else np.zeros(len(grid))
    words = np.zeros(len(grid))
    laugh_text = np.zeros(len(grid))
    banter = np.zeros(len(grid))
    rage = np.zeros(len(grid))
    for seg in transcript["segments"]:
        lo, hi = np.searchsorted(grid, seg["start"] - WINDOW_S / 2), np.searchsorted(grid, seg["end"] + WINDOW_S / 2)
        words[lo:hi] += len(seg["words"])
        laugh_text[lo:hi] += len(LAUGH_TEXT.findall(seg["text"]))
        banter[lo:hi] += len(BANTER_TEXT.findall(seg["text"]))
        rage[lo:hi] += len(RAGE_TEXT.findall(seg["text"]))
    talky = np.clip((words - np.percentile(words, 50)) / (np.percentile(words, 90) - np.percentile(words, 50) + 1), 0, 2)
    score = (1.5 * laugh + 1.0 * scream + 0.8 * np.clip(excited - 1.5, 0, 3) + 2.0 * np.clip(laugh_text, 0, 2)
             + 1.0 * np.clip(banter, 0, 3) + 1.5 * np.clip(rage, 0, 2) + 1.0 * talky)
    reasons = {"laughing": laugh > 0.5, "screaming": scream > 0.5, "laughs in the transcript": laugh_text > 0,
               "banter": banter >= 2, "rage or roast": rage > 0, "loud reaction": excited > 2.5,
               "fast back-and-forth": talky > 1.2}
    return grid, score, reasons


def _sentence_bounds(transcript, start, end, duration):
    """Widen [start, end] to whole transcript lines: begin at a line start, finish at a line end."""
    starts = [s["start"] for s in transcript["segments"] if s["start"] <= start]
    ends = [s["end"] for s in transcript["segments"] if s["end"] >= end]
    start = max(starts) if starts and start - max(starts) < 8 else start
    end = min(ends) if ends and min(ends) - end < 8 else end
    return max(0.0, start), min(duration, end)


def _fit(start, end, settings, duration):
    if end - start < settings.min_clip_s:
        pad = (settings.min_clip_s - (end - start)) / 2
        start, end = start - pad, end + pad
    if end - start > MAX_TALK_S:
        end = start + MAX_TALK_S
    shift = max(0.0, -start) - max(0.0, end - duration)
    return round(max(0.0, start + shift), 2), round(min(duration, end + shift), 2)


def from_rules(transcript, sounds, audio, settings, duration):
    grid, score, reasons = rule_scores(transcript, sounds, audio, duration)
    found = []
    for i in np.argsort(score)[::-1]:
        if score[i] < MIN_SCORE:
            break
        peak = float(grid[i])
        if peak < 10 or peak > duration - 10 or any(abs(peak - f["peak"]) < PEAK_GAP_S for f in found):
            continue
        start, end = _sentence_bounds(transcript, peak - SETUP_S, peak + AFTER_S, duration)
        start, end = _fit(start, end, settings, duration)
        why = [name for name, flags in reasons.items() if flags[max(0, i - 2):i + 3].any()]
        found.append({"start": start, "end": end, "peak": peak, "talk_score": round(float(score[i]), 2),
                      "source": "talk", "reasons": why or ["lively talk"]})
    return found


def _lines(transcript, sounds, start, end):
    tags = {}
    if sounds is not None:
        for group, tag, level in (("laugh", "[laugh]", 0.03), ("scream", "[scream]", 0.03), ("gunfire", "[gunfire]", 0.5)):
            for t in sounds["t"][(sounds[group] >= level) & (sounds["t"] >= start) & (sounds["t"] < end)]:
                tags.setdefault(int(t // 5), set()).add(tag)
    out = []
    for seg in transcript["segments"]:
        if start <= seg["start"] < end:
            near = set().union(*(tags.get(int(seg["start"] // 5) + k, set()) for k in (0, 1)))
            out.append(f"{_clock(seg['start'] - start)} {' '.join(sorted(near))} {seg['text']}".replace("  ", " "))
    return "\n".join(out)


def from_gemini(job, transcript, sounds, settings, duration):
    from google.genai import types

    from .judge import _client

    cache = job.path("talk.json")
    done = read_json(cache, {})
    client = _client(settings.gemini_api_key)
    for start in np.arange(0.0, duration, LLM_CHUNK_S):
        key = str(int(start))
        if key in done:
            continue
        end = min(duration, start + LLM_CHUNK_S + 60)
        lines = _lines(transcript, sounds, start, end)
        if not lines:
            done[key] = []
            continue
        prompt = PROMPT.format(minutes=(end - start) / 60, types=", ".join(TYPES), lines=lines)
        response = client.models.generate_content(
            model=settings.gemini_model, contents=[prompt],
            config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.2))
        done[key] = json.loads(response.text)
        write_json(cache, done)
        log(f"talk: Gemini read {_clock(start)}-{_clock(end)}, {len(done[key])} moments")
    found = []
    for key, items in done.items():
        for item in items if isinstance(items, list) else []:
            try:
                start, end = float(key) + _seconds(item["start"]), float(key) + _seconds(item["end"])
                worth = int(item.get("worth", 0))
            except (KeyError, ValueError, TypeError):
                continue
            if worth < 6 or end <= start:
                continue
            start, end = _fit(*_sentence_bounds(transcript, start, end, duration), settings, duration)
            kind = item.get("type") if item.get("type") in TYPES else "funny"
            found.append({"start": start, "end": end, "peak": (start + end) / 2, "talk_score": worth,
                          "source": "gemini", "talk_type": kind, "title": str(item.get("title", "")),
                          "reasons": [str(item.get("why", "")) or kind]})
    return found


def find(job, transcript, sounds, audio, settings, duration):
    found = from_rules(transcript, sounds, audio, settings, duration)
    if settings.gemini_api_key:
        try:
            found = from_gemini(job, transcript, sounds, settings, duration) + found
        except Exception as exc:
            log(f"talk: Gemini failed ({exc}); using the rules only")
    return found
