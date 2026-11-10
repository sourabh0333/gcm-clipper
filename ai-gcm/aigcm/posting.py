"""Posts to YouTube (M4.2): what a post may say, when it may go, and the approval that lets it go.

Rules from YouTube's API reference and the Developer Policies (see plans/M4 Plan and post plan.md, P-R2, P-R5):
titles up to 100 characters and descriptions up to 5,000 bytes, neither with < or >; tags up to 500 characters
in all; a scheduled post is uploaded private with publishAt, so the time must be in the future with room for
the upload. Nothing is uploaded without an approval that records exactly what the creator saw: the uploader
posts `post.approval`, never the editable columns, and only when `approved()` says so."""

import hashlib
import re
from datetime import timedelta

from .db.models import utcnow

TITLE_MAX = 100
DESCRIPTION_MAX_BYTES = 5000
TAGS_MAX = 500
LEAD = timedelta(minutes=15)       # a scheduled time at least this far ahead, for the upload and processing
FURTHEST = timedelta(days=365)
LIVE_STATES = ("approved", "uploading", "scheduled", "posted")   # a post that is (or will be) on YouTube
LINK = re.compile(r"^https://(www\.|m\.)?(youtube\.com/(watch\?v=|live/|shorts/)|youtu\.be/)[\w-]{11}([?&#][\w=&%.-]*)?$")


class PostError(ValueError):
    """Something the creator has to fix before approving, in plain words."""


def clean_link(link):
    link = (link or "").strip()
    if not link:
        return None
    if not LINK.match(link):
        raise PostError("Paste the stream's YouTube link (youtube.com/watch?v=…, youtube.com/live/… or youtu.be/…).")
    return link


def tags_length(tags):
    # YouTube counts the commas between tags, and the quotes it adds around a tag with a space.
    return sum(len(t) + (2 if " " in t else 0) for t in tags) + max(len(tags) - 1, 0)


def clean_tags(tags):
    out = []
    for tag in tags or []:
        tag = str(tag).strip().lstrip("#").strip()
        if tag and tag.lower() not in [t.lower() for t in out] and "<" not in tag and ">" not in tag:
            out.append(tag[:100])
    while out and tags_length(out) > TAGS_MAX:
        out.pop()
    return out


def check_text(title, description):
    title = (title or "").strip()
    if not title:
        raise PostError("Add a title.")
    if len(title) > TITLE_MAX:
        raise PostError(f"The title is {len(title)} characters; YouTube allows {TITLE_MAX}.")
    if len(description.encode("utf-8")) > DESCRIPTION_MAX_BYTES:
        raise PostError("The description is too long for YouTube (5,000 bytes). Shorten it.")
    for name, text in (("title", title), ("description", description)):
        if "<" in text or ">" in text:
            raise PostError(f"YouTube doesn't allow < or > in the {name}.")
    return title


def check_time(mode, publish_at, now=None):
    now = now or utcnow()
    if mode == "now":
        return None
    if publish_at is None:
        raise PostError("Pick when it goes live, or choose Post now.")
    if publish_at < now + LEAD:
        raise PostError("Pick a time at least 15 minutes from now (the upload needs that long), or choose Post now.")
    if publish_at > now + FURTHEST:
        raise PostError("Pick a time within the next year.")
    return publish_at


def file_hash(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def approval_record(post, channel, video, now=None):
    """Everything the creator approved, exactly as it will be sent to YouTube."""
    when = post.publish_at.isoformat() + "Z" if post.mode == "schedule" else None
    answers = {"made_for_kids": False, "synthetic": False, **(channel.settings or {})}
    return {"title": post.title, "description": post.description, "tags": list(post.tags or []),
            "channel": {"id": channel.id, "youtube_id": channel.channel_id, "title": channel.title},
            "privacy": "private" if post.mode == "schedule" else "public", "publish_at": when,
            "category": "20",   # Gaming
            "made_for_kids": bool(answers["made_for_kids"]), "synthetic": bool(answers["synthetic"]),
            "render": post.render_id, "video_sha256": file_hash(video),
            "approved_at": (now or utcnow()).isoformat() + "Z"}


def approved(post):
    """May the uploader send this post? Only an approved post whose stored approval still matches it."""
    a = post.approval or {}
    return (post.status == "approved" and post.approved_at is not None and bool(a.get("video_sha256"))
            and a.get("title") == post.title and a.get("description") == post.description
            and (a.get("channel") or {}).get("id") == post.channel_id and a.get("render") == post.render_id)
