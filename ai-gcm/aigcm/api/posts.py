"""Posts and approvals (M4.2): "Post this?" from an export, edited as a draft, then approved one by one or as an
explicit list. Approving records exactly what the creator saw (aigcm.posting.approval_record); nothing reaches
the uploader (M4.3) without it. See plans/M4 Plan and post plan.md (P-R5, decisions 2-4)."""

from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy import select

from .. import posting
from ..db.models import AuditEntry, Clip, Post, Render, Stream, YouTubeChannel, utcnow
from ..studio import brand, lane, project
from .clips import own_clip
from .deps import current_user, get_db, own_stream

router = APIRouter()


def stamp(value):
    return value.isoformat() + "Z" if value else None


def post_stream(post):
    """The stream a post's video comes from: its clip's, or a highlight's."""
    if post.clip is not None:
        return post.clip.stream
    from sqlalchemy.orm import object_session

    db = object_session(post)
    render = db.get(Render, post.render_id) if (db is not None and post.render_id) else None
    stream_id = (render.params or {}).get("stream_id") if render is not None else None
    return db.get(Stream, stream_id) if stream_id else None


def funnel_link(post):
    """Where the Short sends viewers: the upcoming live for a teaser, else the stream it was cut from."""
    if post.teaser_for:
        return f"https://www.youtube.com/watch?v={post.teaser_for}"
    stream = post_stream(post)
    return stream.link if stream is not None else None


def studio_view(post):
    """The "Finish in Studio" checklist (M4.5): what the API can't set, ready to paste."""
    if not post.video_id:
        return None
    link = funnel_link(post)
    comment = None
    if link:
        comment = f"🔴 Watch me live: {link}" if post.teaser_for else f"Full stream 👉 {link}"
    return {"url": f"https://studio.youtube.com/video/{post.video_id}/edit", "comment": comment,
            "related": None if post.teaser_for else getattr(post_stream(post), "title", None),
            "done": bool(post.studio_done)}


def post_view(post):
    clip = post.clip
    stream = post_stream(post)
    return {"stream_link": funnel_link(post), "has_link": posting.has_link(post.description),
            "stream_title": stream.title if stream is not None else None, "studio": studio_view(post),
            "teaser_for": post.teaser_for,"id": post.id, "status": post.status, "kind": post.kind, "clip_id": post.clip_id,
            "clip_title": (clip.title if clip else None), "stream_id": stream.id if stream is not None else None,
            "render_id": post.render_id, "video": f"/media/renders/{post.render_id}" if post.render_id else None,
            "play": f"/media/renders/{post.render_id}?view=1" if post.render_id else None,
            "cover": f"/media/renders/{post.render_id}/cover" if post.render_id else None,
            "channel": ({"id": post.channel.id, "title": post.channel.title, "thumbnail": post.channel.thumbnail,
                         "status": post.channel.status} if post.channel else None),
            "title": post.title, "description": post.description, "tags": post.tags or [],
            "mode": post.mode, "publish_at": stamp(post.publish_at), "approved_at": stamp(post.approved_at),
            "video_id": post.video_id, "error": post.error, "updated_at": stamp(post.updated_at),
            "created_at": stamp(post.created_at), "posted_at": stamp(post.posted_at), "thumbnail": post.thumbnail,
            "next_try_at": stamp(post.next_try_at)}


def own_post(db, user, post_id):
    post = db.get(Post, post_id)
    if post is None or post.user_id != user.id:
        raise HTTPException(404, "Not found.")
    return post


def first_title(text):
    text = " ".join((text or "").split())
    if len(text) <= posting.TITLE_MAX:
        return text
    cut = text[:posting.TITLE_MAX + 1].rsplit(" ", 1)[0]
    return cut if len(cut) >= 40 else text[:posting.TITLE_MAX]


def draft_text(db, clip):
    """The first draft: the studio's post text (hook or title, the engine's and the kit's description and
    hashtags), with the stream link on top when the creator has given it."""
    saved = project.latest_edit(db, clip)
    hook = (saved.data.get("hook") or {}).get("text") if saved else None
    details = clip.details or {}
    text = brand.post_text(hook or clip.title, details.get("description"), details.get("hashtags"), project.kit_for(clip))
    description = posting.with_link(text["description"], clip.stream.link)
    title = text["title"] or clip.title or next(iter(details.get("titles") or []), None)
    if not title:
        from ..studio.compile import fallback_title
        from ..studio.edit import is_talk

        title = fallback_title(clip.type, 0, is_talk(clip.type, details.get("labels")), clip.spoken)
    from ..studio.variety import with_series

    return first_title(with_series(db, clip.stream.user_id, title)), description, posting.clean_tags(text["hashtags"])


class NewPost(BaseModel):
    render_id: str


@router.post("/api/posts")
def new_post(body: NewPost, request: Request, user=Depends(current_user), db=Depends(get_db)):
    """A draft from a finished export (or the creator's open draft for it)."""
    settings = request.app.state.settings
    render = db.get(Render, body.render_id)
    if render is None or render.user_id != user.id or render.kind not in ("export", "highlight"):
        raise HTTPException(404, "Not found.")
    if render.kind == "highlight":
        return post_view(highlight_draft(db, settings, user, render))
    clip = own_clip(db, user, render.clip_id)
    if render.status != "done" or lane.export_path(settings, clip, render) is None:
        raise HTTPException(409, "This export isn't finished yet.")
    open_draft = db.scalar(select(Post).where(Post.render_id == render.id, Post.status == "draft"))
    if open_draft is not None:
        return post_view(open_draft)
    channel = db.scalar(select(YouTubeChannel).where(YouTubeChannel.user_id == user.id, YouTubeChannel.status == "ok")
                        .order_by(YouTubeChannel.connected_at))
    title, description, tags = draft_text(db, clip)
    post = Post(user_id=user.id, clip_id=clip.id, render_id=render.id, channel_id=channel.id if channel else None,
                title=title, description=description, tags=tags)
    db.add(post)
    db.commit()
    return post_view(post)


def highlight_draft(db, settings, user, render, publish_at=None):
    """A draft for a highlight (a long 16:9 video), or the open draft for it: the highlight's own title and
    description, with the full-stream link when the creator has given it."""
    if render.status != "done" or lane.render_file(settings, db, render) is None:
        raise HTTPException(409, "This highlight isn't finished yet.")
    open_draft = db.scalar(select(Post).where(Post.render_id == render.id, Post.status == "draft"))
    if open_draft is not None:
        return open_draft
    stream = db.get(Stream, (render.params or {}).get("stream_id"))
    folder = lane.highlight_folder(settings, stream, render.id)
    from ..jobs import read_json

    text = read_json(folder / "post.json", {}) or {}
    names = (read_json(folder / "titles.json", {}) or {}).get("titles") or ["Highlights"]
    channel = db.scalar(select(YouTubeChannel).where(YouTubeChannel.user_id == user.id, YouTubeChannel.status == "ok")
                        .order_by(YouTubeChannel.connected_at))
    description = posting.with_link(text.get("description") or "", stream.link)
    post = Post(user_id=user.id, render_id=render.id, channel_id=channel.id if channel else None, kind="video",
                title=first_title(text.get("title") or names[0]), description=description,
                tags=posting.clean_tags(text.get("hashtags") or []), publish_at=publish_at)
    db.add(post)
    db.commit()
    return post


@router.get("/api/posts")
def list_posts(status: str | None = None, user=Depends(current_user), db=Depends(get_db)):
    query = select(Post).where(Post.user_id == user.id)
    if status:
        query = query.where(Post.status.in_(status.split(",")))
    rows = db.scalars(query.order_by(Post.publish_at.is_(None), Post.publish_at, Post.created_at.desc())).all()
    return [post_view(p) for p in rows]


@router.get("/api/posts/quota")
def quota(user=Depends(current_user), db=Depends(get_db)):
    """Today's YouTube use for the whole app (Google's day, Pacific time). The owner's view only."""
    from ..uploader import usage

    if not user.is_admin:
        raise HTTPException(403, "Only the owner can see this.")
    return usage(db)


@router.get("/api/posts/{post_id}")
def get_post(post_id: str, user=Depends(current_user), db=Depends(get_db)):
    return post_view(own_post(db, user, post_id))


class PostEdit(BaseModel):
    title: str = Field("", max_length=300)
    description: str = Field("", max_length=20000)
    tags: list[str] = Field(default_factory=list, max_length=60)
    channel_id: str | None = None
    mode: str = Field("schedule", pattern="^(schedule|now)$")
    publish_at: datetime | None = None


def utc(value):
    if value is None:
        return None
    if value.tzinfo is None:
        raise HTTPException(422, "Send the time with its time zone.")
    return value.astimezone(UTC).replace(tzinfo=None, microsecond=0)


@router.put("/api/posts/{post_id}")
def edit_post(post_id: str, body: PostEdit, user=Depends(current_user), db=Depends(get_db)):
    """Change a draft. Limits are checked on Approve, so a half-written draft can still be saved."""
    post = own_post(db, user, post_id)
    if post.status != "draft":
        raise HTTPException(409, "This post is approved; it can't be changed here any more.")
    if body.channel_id is not None:
        channel = db.get(YouTubeChannel, body.channel_id)
        if channel is None or channel.user_id != user.id:
            raise HTTPException(404, "Not found.")
    post.title, post.description = body.title.strip()[:posting.TITLE_MAX * 3], body.description
    post.tags, post.channel_id = posting.clean_tags(body.tags), body.channel_id
    post.mode, post.publish_at = body.mode, utc(body.publish_at)
    post.updated_at = utcnow()
    db.commit()
    return post_view(post)


def approve_one(db, settings, user, post_id, seen):
    """Approve one draft, if it is exactly the version the creator was shown (`seen` is its updated_at)."""
    post = own_post(db, user, post_id)
    if post.status != "draft":
        raise posting.PostError("This post is already approved." if post.status in posting.LIVE_STATES
                                else "Only drafts can be approved.")
    if seen != stamp(post.updated_at):
        raise posting.PostError("This post changed since you looked at it. Look again, then approve.")
    channel = post.channel
    if channel is None:
        raise posting.PostError("Pick the channel to post to.")
    if channel.status != "ok":
        raise posting.PostError(f"Reconnect {channel.title} in Settings first.")
    clip = post.clip
    render = db.get(Render, post.render_id) if post.render_id else None
    video = lane.render_file(settings, db, render, clip) if (render and render.status == "done") else None
    if video is None:
        raise posting.PostError("The exported video is gone. Export the clip again.")
    post.title = posting.check_text(post.title, post.description)
    post.tags = posting.clean_tags(post.tags)
    now = utcnow()
    posting.check_time(post.mode, post.publish_at, now)
    same = (Post.clip_id == post.clip_id) if post.clip_id else (Post.render_id == post.render_id)
    clash = db.scalar(select(Post).where(same, Post.channel_id == post.channel_id,
                                         Post.id != post.id, Post.status.in_(posting.LIVE_STATES)))
    if clash is not None:
        raise posting.PostError(f"This clip is already going to {channel.title}.")
    post.approval = posting.approval_record(post, channel, video, now)
    post.status, post.approved_at, post.updated_at, post.error = "approved", now, now, None
    db.add(AuditEntry(user_id=user.id, action="post_approved", detail={"post": post.id, **post.approval}))
    return post


class Approve(BaseModel):
    seen: str


@router.post("/api/posts/{post_id}/approve")
def approve(post_id: str, body: Approve, request: Request, user=Depends(current_user), db=Depends(get_db)):
    try:
        post = approve_one(db, request.app.state.settings, user, post_id, body.seen)
    except posting.PostError as exc:
        db.rollback()
        raise HTTPException(409, str(exc)) from exc
    db.commit()
    return post_view(post)


class BatchItem(BaseModel):
    id: str
    seen: str


class Batch(BaseModel):
    posts: list[BatchItem] = Field(min_length=1, max_length=50)


@router.post("/api/posts/approve")
def approve_many(body: Batch, request: Request, user=Depends(current_user), db=Depends(get_db)):
    """Approve an explicit list the creator looked at; each post on its own, so one problem holds back only that one."""
    approved, problems = [], []
    for item in body.posts:
        try:
            post = approve_one(db, request.app.state.settings, user, item.id, item.seen)
            db.commit()
            approved.append(post_view(post))
        except posting.PostError as exc:
            db.rollback()
            problems.append({"id": item.id, "error": str(exc)})
        except HTTPException:
            db.rollback()
            problems.append({"id": item.id, "error": "Not found."})
    return {"approved": approved, "problems": problems}


@router.post("/api/posts/{post_id}/cancel")
def cancel(post_id: str, user=Depends(current_user), db=Depends(get_db)):
    """Take back an approval before the upload starts. After that the video is on YouTube: change it in Studio."""
    post = own_post(db, user, post_id)
    if post.status not in ("approved", "failed"):
        raise HTTPException(409, "Only an approved post that hasn't uploaded yet can be cancelled."
                            if post.status in ("uploading", "scheduled", "posted") else "Nothing to cancel.")
    post.status, post.updated_at = "cancelled", utcnow()
    db.add(AuditEntry(user_id=user.id, action="post_cancelled", detail={"post": post.id}))
    db.commit()
    return post_view(post)


@router.delete("/api/posts/{post_id}")
def delete_post(post_id: str, user=Depends(current_user), db=Depends(get_db)):
    post = own_post(db, user, post_id)
    if post.status not in ("draft", "cancelled", "failed"):
        raise HTTPException(409, "Cancel it first.")
    db.delete(post)
    db.commit()
    return {"ok": True}


class StreamLink(BaseModel):
    link: str = Field("", max_length=300)


@router.put("/api/streams/{stream_id}/link")
def stream_link(stream_id: str, body: StreamLink, user=Depends(current_user), db=Depends(get_db)):
    """The stream on YouTube, put as "Full stream: <link>" at the top of new drafts from its clips."""
    stream = own_stream(db, user, stream_id)
    try:
        stream.link = posting.clean_link(body.link)
    except posting.PostError as exc:
        raise HTTPException(422, str(exc)) from exc
    # Drafts from this stream's clips get the link too (approved posts are frozen; teasers link the coming live).
    updated = 0
    if stream.link:
        for post in db.scalars(select(Post).join(Clip, Post.clip_id == Clip.id)
                               .where(Clip.stream_id == stream.id, Post.status == "draft", Post.teaser_for.is_(None))):
            if not posting.has_link(post.description):
                post.description, post.updated_at = posting.with_link(post.description, stream.link), utcnow()
                updated += 1
    db.commit()
    return {"link": stream.link, "drafts_updated": updated}


@router.get("/api/streams/{stream_id}/link-suggestions")
def link_suggestions(stream_id: str, user=Depends(current_user), db=Depends(get_db)):
    """Lives on the creator's channels that look like this stream: recorded the same day (or a day either side,
    for time zones and midnight streams) or about as long. From the calendar's copy of recent uploads: no units."""
    from datetime import date as date_
    from datetime import datetime as datetime_

    stream = own_stream(db, user, stream_id)
    day = date_.fromisoformat(stream.recorded_on) if stream.recorded_on else None
    found = []
    for channel in db.scalars(select(YouTubeChannel).where(YouTubeChannel.user_id == user.id)):
        for item in channel.recent or []:
            if not item.get("live") or not item.get("at"):
                continue
            at = datetime_.fromisoformat(item["at"].replace("Z", "+00:00"))
            same_day = day is not None and abs((at.date() - day).days) <= 1
            length = stream.duration_s or 0
            close = length > 0 and abs((item.get("seconds") or 0) - length) <= max(600, 0.15 * length)
            if same_day or close:
                found.append({"url": f"https://www.youtube.com/watch?v={item['id']}", "title": item.get("title") or "",
                              "at": item["at"], "seconds": item.get("seconds"), "channel": channel.title,
                              "score": 2 * same_day + close})
    found.sort(key=lambda f: (-f["score"], f["at"]))
    return [{k: v for k, v in f.items() if k != "score"} for f in found[:3]]


@router.post("/api/posts/{post_id}/cover")
def cover_again(post_id: str, user=Depends(current_user), db=Depends(get_db)):
    """Try the cover again (after the creator verified their channel, say): the worker sets it within a minute
    or two. 50 quota units."""
    post = own_post(db, user, post_id)
    if not post.video_id or post.status not in ("scheduled", "posted"):
        raise HTTPException(409, "The cover is set once the video is on YouTube.")
    if post.thumbnail == "set":
        raise HTTPException(409, "The cover is already set.")
    post.thumbnail, post.checked_at = None, None
    db.commit()
    return post_view(post)


class StudioDone(BaseModel):
    done: bool = True


@router.post("/api/posts/{post_id}/studio")
def studio_done(post_id: str, body: StudioDone, user=Depends(current_user), db=Depends(get_db)):
    """The creator finished the related video and pinned comment in YouTube Studio (or takes the tick back)."""
    post = own_post(db, user, post_id)
    if not post.video_id:
        raise HTTPException(409, "It isn't on YouTube yet.")
    post.studio_done = body.done
    db.commit()
    return post_view(post)
