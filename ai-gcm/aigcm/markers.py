"""Moments the creator marked while live: a button in the app, a `!clip` in chat, or saying "clip that".

The app stores markers in the job's markers.json as [{"t": seconds into the stream, "source": "button" |
"chat" | "voice", "by": who}]. Spoken markers are found in the transcript here. Every marker always
produces a clip and is a strong ranking signal, since creators mark exactly the moments automatic
detection misses: funny setups, banter, a play only they know was hard.
"""

import re

from .jobs import read_json

VOICE = re.compile(r"\b(?:clip (?:that|it|this|karo|kar|kar do|le|lo|ban(?:a|ao))|clip clip|ye clip|yeh clip|"
                   r"isko clip|iska clip|save (?:that|this) clip)\b", re.I)
SOURCES = {"button": "you marked this", "chat": "marked in chat with !clip", "voice": "you said \"clip that\""}


def load(job):
    """Markers saved by the app for this job, oldest first."""
    found = read_json(job.path("markers.json"), [])
    return sorted((m for m in found if isinstance(m.get("t"), (int, float))), key=lambda m: m["t"])


def from_transcript(transcript):
    """Spoken markers: the phrase is said just after the moment, so the marker points a little earlier."""
    found = []
    for seg in transcript.get("segments", []):
        if VOICE.search(seg["text"]):
            found.append({"t": round(max(0.0, seg["start"] - 2.0), 2), "source": "voice", "by": "streamer",
                          "text": seg["text"]})
    return found


def merge(*lists, gap_s=5.0):
    """All markers, oldest first, with repeats within gap_s (a spam of !clip) folded into one."""
    out = []
    for m in sorted((m for items in lists for m in items), key=lambda m: m["t"]):
        if out and m["t"] - out[-1]["t"] < gap_s:
            out[-1].setdefault("count", 1)
            out[-1]["count"] += 1
            continue
        out.append(dict(m))
    return out


def describe(marker):
    return SOURCES.get(marker.get("source"), "marked")
