"""Hook variety (12 Nov 2026): so a creator's Shorts don't all look like one template.

Since 1 October 2026 YouTube's Shorts ranking holds back "template-based bulk changes", and a feed of Shorts
with the same kind of hook every time also bores viewers. The engine already writes up to three titles per
clip, one from each family top Indian gaming Shorts use (titles.py: a stat, a Hinglish punchline, suspense),
but every clip used the first. Now:

- clips of a stream take turns: the best clip leads with its first family, the next with its second, and so on;
- a stat title that the creator has posted before gets the next number of its series ("DOUBLE FINISH #3"),
  counted from their own posts (series lift views on the same channel);
- "Make another version" saves a new edit with the next hook and the other length (moment or full fight),
  ready to export as an alternate cut.
"""

import re

from sqlalchemy import select

from ..titles import EMOJI

SUSPENSE = ("Wait for it", "Last second tak dekho", "Ye kya tha bhai")
STAT_WORDS = ("FINISH", "KNOCK", "CHICKEN DINNER", "ONE SHOT", "HEADSHOT", "LAST ZONE")
EMOJI_RE = re.compile("[" + "".join(sorted(set(EMOJI.values()))) + "\U0001F300-\U0001FAFF☀-➿️]")
NUMBER_RE = re.compile(r"\s*#\d+\s*$")


def family_of(title):
    text = (title or "").strip()
    if any(text.startswith(s) for s in SUSPENSE):
        return "suspense"
    if any(w in text for w in STAT_WORDS) and text.upper() == text:
        return "stat"
    return "punchline"


def base_of(title):
    """The title without its emoji and series number: what makes two posts "the same series"."""
    return NUMBER_RE.sub("", EMOJI_RE.sub("", title or "")).strip().upper()


def titles_of(clip):
    titles = [t for t in ((clip.details or {}).get("titles") or []) if t]
    if not titles and clip.title:
        titles = [clip.title]
    return titles


def rotated_title(clip):
    """This clip's turn in its stream: rank 1 takes the first family, rank 2 the second... so the stream's
    Shorts don't all open the same way."""
    titles = titles_of(clip)
    if not titles:
        return clip.title
    return titles[((clip.rank or 1) - 1) % len(titles)]


def next_title(clip, current):
    """The title after `current` in the clip's list, for another version."""
    titles = titles_of(clip)
    if not titles:
        return current
    try:
        i = titles.index((current or "").strip())
    except ValueError:
        i = -1
    return titles[(i + 1) % len(titles)]


def with_series(db, user_id, title):
    """A stat title gets the next number of its series on this creator's channel ("DOUBLE FINISH #3" after
    two earlier DOUBLE FINISH posts). Other families and first-time titles stay as they are."""
    from ..db.models import Post

    if family_of(title) != "stat":
        return title
    base = base_of(title)
    used = [p.title for p in db.scalars(select(Post).where(Post.user_id == user_id, Post.status != "cancelled")).all()]
    numbers = []
    for t in used:
        if base_of(t) == base:
            m = re.search(r"#(\d+)", t)
            numbers.append(int(m.group(1)) if m else 1)
    if not numbers:
        return title
    emoji = "".join(EMOJI_RE.findall(title))
    return f"{base} #{max(numbers) + 1}{(' ' + emoji) if emoji else ''}"[:100]


def alternate(edit, clip, presets, new_hook):
    """Another version of an edit: the next hook, and the other length preset (a full-fight edit becomes the
    moment, anything else the full fight). Zooms, effects and the cover outside the new cut are dropped."""
    from .edit import Segment

    total = sum(s.end - s.start for s in edit.segments)
    moment, full = presets["moment"], presets["full_fight"]
    full_len = full[1] - full[0]
    a, b = moment if abs(total - full_len) < 1.5 and full_len > (moment[1] - moment[0]) + 1.5 else full
    if abs((b - a) - total) < 1.5:              # both presets are the same length: keep the cut, vary the hook
        a, b = edit.segments[0].start, edit.segments[-1].end
    inside = lambda t: a <= t <= b               # noqa: E731
    return edit.model_copy(update={
        "segments": [Segment(start=a, end=b, speed=1.0)],
        "zooms": [z for z in edit.zooms if inside(z.t)],
        "sfx": [s for s in edit.sfx if inside(s.t)],
        "cover_t": edit.cover_t if edit.cover_t is not None and inside(edit.cover_t) else None,
        "hook": edit.hook.model_copy(update={"text": (new_hook or "")[:80], "on": bool((new_hook or "").strip())}),
    }), (a, b)
