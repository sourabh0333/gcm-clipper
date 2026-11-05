"""Post-ready titles, hashtags and descriptions for a clip.

The three title families come from a sample of about 45 Indian gaming channels' top Shorts: a stat or
record ("1v4 LAST ZONE"), a Hinglish punchline ("Ye kya tha bhai"), and suspense ("Wait for the end").
Titles stay under 45 characters with one emoji from a fixed set, and a channel-wide series counter
("1v4 #7") is reused because repeated series lift views on the same channel. Hashtags are sized to the
channel: small channels stuff them, big ones use two. Descriptions carry the stream link and Krafton's
"not endorsed" line for BGMI.
"""

import re

MAX_LEN = 45
EMOJI = {"kill": "💀", "multi": "🔥", "win": "🏆", "funny": "🤣", "rage": "😡", "shock": "😱", "clutch": "😎"}
KRAFTON_LINE = "BGMI is a trademark of KRAFTON, Inc. This video is not endorsed by or affiliated with KRAFTON."
SMALL_CHANNEL = 50_000
TAGS = {
    "bgmi": {"small": ["#bgmi", "#bgmishorts", "#bgmilive", "#shorts", "#gaming"], "big": ["#bgmi", "#shorts"]},
    "freefire": {"small": ["#freefire", "#freefiremax", "#freefireindia", "#shorts", "#gaming"], "big": ["#freefire", "#shorts"]},
}
FILLER = re.compile(r"^(?:are|arre|bhai|yaar|haan|hmm|ok|okay|to|toh|aur|phir|lo|dekho)\b[ ,]*", re.I)


def _cut(text, limit=MAX_LEN):
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0]
    return cut.rstrip(" ,.!?-") or text[:limit]


def stat_title(labels, series=None):
    """Stat or record family, from the clip's own labels."""
    kills, left, win = labels.get("kills") or 0, labels.get("players_left"), labels.get("win")
    if win:
        base, emoji = f"CHICKEN DINNER {kills} FINISHES" if kills else "CHICKEN DINNER", EMOJI["win"]
    elif kills >= 3:
        base, emoji = f"{kills} FINISHES 1 FIGHT", EMOJI["multi"]
    elif kills == 2:
        base, emoji = "DOUBLE FINISH", EMOJI["kill"]
    elif kills == 1:
        base, emoji = "PATT SE HEADSHOT" if labels.get("type") == "fight" else "ONE SHOT", EMOJI["kill"]
    else:
        return None
    if left is not None and left <= 10:
        base += " LAST ZONE"
    if series is not None:
        base += f" #{series}"
    return _cut(f"{base} {emoji}")


def punchline_title(said, labels, judge_title=None):
    """Hinglish punchline: the judge's title when there is one, else the best line the streamer said."""
    if judge_title:
        return _cut(judge_title if any(ch in judge_title for ch in EMOJI.values()) else f"{judge_title} {EMOJI['funny']}")
    lines = [FILLER.sub("", s.strip()) for s in re.split(r"[.?!]+", said or "") if len(s.split()) >= 3]
    lines = [l for l in lines if l]
    if not lines:
        return None
    best = max(lines, key=lambda l: (l.count("?"), -abs(len(l) - 28)))
    emoji = EMOJI["rage"] if labels.get("talk") == "rage" else EMOJI["funny"]
    return _cut(f"{best[0].upper() + best[1:]} {emoji}")


def suspense_title(labels):
    if labels.get("marked"):
        return f"Wait for it {EMOJI['shock']}"
    if labels.get("kills"):
        return f"Last second tak dekho {EMOJI['shock']}"
    return f"Ye kya tha bhai {EMOJI['shock']}"


def suggest(labels, said="", judge_title=None, series=None):
    """Up to three titles, best first, one per family, with no repeats."""
    out = []
    for t in (punchline_title(said, labels, judge_title) if labels.get("talk") or judge_title else None,
              stat_title(labels, series), punchline_title(said, labels, judge_title), suspense_title(labels)):
        if t and t not in out:
            out.append(t)
    return out[:3]


def hashtags(game, followers):
    group = TAGS.get(game, TAGS["bgmi"])
    return group["small"] if (followers or 0) < SMALL_CHANNEL else group["big"]


def description(stream_url, game, tags, extra=""):
    parts = []
    if stream_url:
        parts.append(f"Full stream: {stream_url}")
    if extra:
        parts.append(extra)
    if game == "bgmi":
        parts.append(KRAFTON_LINE)
    parts.append(" ".join(tags))
    return "\n\n".join(parts)


def series_counter(history, key):
    """The next number for a repeated title series on this channel, given earlier titles."""
    pattern = re.compile(re.escape(key) + r" #(\d+)")
    seen = [int(m.group(1)) for title in history for m in [pattern.search(title)] if m]
    return (max(seen) + 1) if seen else None
