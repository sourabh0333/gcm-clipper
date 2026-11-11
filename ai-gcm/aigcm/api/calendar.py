"""The calendar (M4.4): posts by day, "fill empty evenings" with the creator's finished exports, moving a draft,
and the Shorts-share gauge. See plans/M4 Plan and post plan.md (M4.4) and the master plan (S8).

Times are kept in UTC; the phone sends its time zone so "7 pm" and "which day" mean the creator's own clock.
Filling only makes or moves drafts: nothing goes to YouTube until the creator approves, one by one or as the
listed week."""

from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy import select

from .. import posting
from .. import youtube as yt
from ..db.models import Clip, Post, Render, Stream, YouTubeChannel, utcnow
from ..studio import lane
from .deps import current_user, get_db
from .posts import draft_text, own_post, post_view, stamp, utc

router = APIRouter()

GAUGE_DAYS = 28
GAUGE_AHEAD = 7
GAUGE_WARN = 0.20     # the master plan: warn above about 20% Shorts (one correlational study; tracked in the beta)
REFRESH = timedelta(hours=6)
UTC = ZoneInfo("UTC")


def zone(name):
    try:
        return ZoneInfo(name or "Asia/Kolkata")
    except (ZoneInfoNotFoundError, ValueError):
        raise HTTPException(422, "Unknown time zone.")


def when(post):
    """The moment a post sits on the calendar: its publish time, or when it went (or will go) up for Post now."""
    if post.mode == "schedule" and post.publish_at:
        return post.publish_at
    return post.posted_at or post.approved_at if post.mode == "now" else None


def local_day(moment, tz):
    return moment.replace(tzinfo=UTC).astimezone(tz).date()


def to_utc(day, at, tz):
    return datetime.combine(day, at, tz).astimezone(UTC).replace(tzinfo=None)


# --- the Shorts-share gauge ----------------------------------------------------------------------------------

def refresh_recent(request, db, channel, now):
    """Re-read the channel's last 28 days of uploads if the copy is older than 6 hours. Problems leave the old copy."""
    if channel.status != "ok" or (channel.recent_at and now - channel.recent_at < REFRESH):
        return
    settings, http = request.app.state.settings, request.app.state.http
    try:
        token = yt.access_token(http, settings, yt.unseal(settings.token_key, channel.refresh_token))
        items, units = yt.recent_uploads(http, token, now - timedelta(days=GAUGE_DAYS))
        try:
            upcoming = yt.upcoming_streams(http, token)
            units += 1
        except yt.YouTubeError:
            upcoming = channel.upcoming
    except yt.Expired:
        channel.status = "expired"
        db.commit()
        return
    except (yt.YouTubeError, Exception):   # the gauge is a nice-to-have: never break the calendar over it
        return
    from ..uploader import spend

    spend(db, units=units)
    channel.recent, channel.recent_at, channel.upcoming = items, now, upcoming
    db.commit()


def gauge(db, channel, now):
    """Shorts as a share of the channel's uploads: the last 28 days on YouTube plus Kaatclip's planned posts for
    the next 7 days that aren't on YouTube yet."""
    if channel.recent is None:
        return None
    since = now - timedelta(days=GAUGE_DAYS)
    seen, shorts, total = set(), 0, 0
    for item in channel.recent:
        at = datetime.fromisoformat(item["at"].replace("Z", "+00:00")).replace(tzinfo=None) if item.get("at") else None
        if at is None or at < since or at > now + timedelta(days=GAUGE_AHEAD):
            continue
        seen.add(item["id"])
        total += 1
        shorts += bool(item["short"])
    planned = 0
    for post in db.scalars(select(Post).where(Post.channel_id == channel.id,
                                              Post.status.in_(("draft", "approved", "uploading", "scheduled")))):
        moment = when(post)
        if moment is None or not (now <= moment <= now + timedelta(days=GAUGE_AHEAD)) or post.video_id in seen:
            continue
        planned += 1
        total += 1
        shorts += 1
    share = shorts / total if total else 0.0
    return {"channel": channel.title, "shorts": shorts, "uploads": total, "planned": planned,
            "share": round(share, 3), "warn": total >= 5 and share > GAUGE_WARN, "limit": GAUGE_WARN,
            "days": GAUGE_DAYS, "ahead": GAUGE_AHEAD, "as_of": stamp(channel.recent_at)}


# --- the calendar --------------------------------------------------------------------------------------------

@router.get("/api/calendar")
def calendar(request: Request, start: date, days: int = 7, tz: str = "Asia/Kolkata", channel: str | None = None,
             user=Depends(current_user), db=Depends(get_db)):
    if not 1 <= days <= 42:
        raise HTTPException(422, "Ask for 1 to 42 days.")
    zone_ = zone(tz)
    lo, hi = to_utc(start, time(0), zone_), to_utc(start + timedelta(days=days), time(0), zone_)
    rows = db.scalars(select(Post).where(Post.user_id == user.id, Post.status != "cancelled")).all()
    placed, unscheduled = [], []
    for post in rows:
        moment = when(post)
        if moment is None or (post.status == "draft" and moment < utcnow()):
            if post.status == "draft":
                unscheduled.append(post_view(post))
            continue
        if lo <= moment < hi:
            view = post_view(post)
            view["day"] = local_day(moment, zone_).isoformat()
            view["at"] = stamp(moment)
            placed.append(view)
    placed.sort(key=lambda v: v["at"])
    channels = db.scalars(select(YouTubeChannel).where(YouTubeChannel.user_id == user.id)
                          .order_by(YouTubeChannel.connected_at)).all()
    target = next((c for c in channels if c.id == channel), channels[0] if channels else None)
    meter = None
    if target is not None:
        now = utcnow()
        refresh_recent(request, db, target, now)
        meter = gauge(db, target, now)
    lives = []
    for channel_row in channels:
        teased = {p.teaser_for for p in rows if p.teaser_for}
        for live in channel_row.upcoming or []:
            begins = parse_iso(live["start"])
            if lo <= begins < hi and begins > utcnow():
                lives.append({**live, "channel_id": channel_row.id, "channel": channel_row.title,
                              "day": local_day(begins, zone_).isoformat(), "teased": live["id"] in teased,
                              "can_tease": begins - TEASER_BEFORE >= utcnow() + timedelta(minutes=20)})
    lives.sort(key=lambda live: live["start"])
    return {"start": start.isoformat(), "days": days, "posts": placed, "unscheduled": unscheduled, "gauge": meter,
            "lives": lives,
            "channels": [{"id": c.id, "title": c.title} for c in channels]}


class Fill(BaseModel):
    tz: str = "Asia/Kolkata"
    start: date | None = None          # the first day to fill (default: today, if the hour is still ahead)
    days: int = Field(7, ge=1, le=14)
    hour: int = Field(19, ge=0, le=23)
    minute: int = Field(0, ge=0, le=59)
    channel_id: str | None = None


def ready_exports(db, settings, user):
    """Each kept clip's newest finished export that has no post yet (the clips worth posting, made by the creator)."""
    taken = {p.clip_id for p in db.scalars(select(Post).where(Post.user_id == user.id,
                                                             Post.status != "cancelled")).all()}
    out = []
    rows = db.scalars(select(Render).join(Clip, Render.clip_id == Clip.id).join(Stream, Clip.stream_id == Stream.id)
                      .where(Render.user_id == user.id, Render.kind == "export", Render.status == "done",
                             Clip.decision == "keep")
                      .order_by(Render.finished_at.desc())).all()
    for render in rows:
        clip = db.get(Clip, render.clip_id)
        if clip.id in taken or lane.export_path(settings, clip, render) is None:
            continue
        taken.add(clip.id)
        out.append((clip, render))
    out.sort(key=lambda pair: -(pair[0].score or 0))       # the best clips get the nearest evenings
    return out


@router.post("/api/calendar/fill")
def fill(body: Fill, request: Request, user=Depends(current_user), db=Depends(get_db)):
    """Put a draft on every free evening: first the creator's drafts without a time, then new drafts from kept
    clips' finished exports. Returns the drafts it placed; the creator approves them afterwards."""
    settings = request.app.state.settings
    zone_ = zone(body.tz)
    now = utcnow()
    at = time(body.hour, body.minute)
    first = body.start or local_day(now, zone_)
    days = [first + timedelta(days=i) for i in range(body.days)]
    days = [d for d in days if to_utc(d, at, zone_) >= now + timedelta(hours=1)]
    if body.channel_id:
        channel = db.get(YouTubeChannel, body.channel_id)
        if channel is None or channel.user_id != user.id:
            raise HTTPException(404, "Not found.")
    else:
        channel = db.scalar(select(YouTubeChannel).where(YouTubeChannel.user_id == user.id, YouTubeChannel.status == "ok")
                            .order_by(YouTubeChannel.connected_at))
    if channel is None:
        raise HTTPException(409, "Connect a YouTube channel in Settings first.")
    busy = set()
    for post in db.scalars(select(Post).where(Post.user_id == user.id, Post.channel_id == channel.id,
                                              Post.status != "cancelled", Post.status != "failed")).all():
        moment = when(post)
        if moment is not None and moment >= now:
            busy.add(local_day(moment, zone_))
    free = [d for d in days if d not in busy]
    waiting = db.scalars(select(Post).where(Post.user_id == user.id, Post.status == "draft")
                         .order_by(Post.created_at)).all()
    waiting = [p for p in waiting if when(p) is None or when(p) < now]
    exports = ready_exports(db, settings, user)
    placed = []
    for day in free:
        if waiting:
            post = waiting.pop(0)
        elif exports:
            clip, render = exports.pop(0)
            title, description, tags = draft_text(db, clip)
            post = Post(user_id=user.id, clip_id=clip.id, render_id=render.id, title=title, description=description,
                        tags=tags)
            db.add(post)
        else:
            break
        post.channel_id, post.mode, post.publish_at, post.updated_at = channel.id, "schedule", to_utc(day, at, zone_), now
        placed.append(post)
    db.commit()
    return {"placed": [post_view(p) for p in placed], "free_left": len(free) - len(placed),
            "exports_left": len(exports), "drafts_left": len(waiting)}


TEASER_BEFORE = timedelta(hours=2)


def parse_iso(text):
    return datetime.fromisoformat(text.replace("Z", "+00:00")).astimezone(UTC).replace(tzinfo=None)


class Teaser(BaseModel):
    live_id: str = Field(max_length=32)
    tz: str = "Asia/Kolkata"


@router.post("/api/calendar/teaser")
def teaser(body: Teaser, request: Request, user=Depends(current_user), db=Depends(get_db)):
    """A draft teaser Short for an upcoming live: the best kept clip with a finished export and no post yet, going
    public two hours before the live, titled "LIVE at 8 pm" and linking the live. The creator checks and approves it."""
    channels = db.scalars(select(YouTubeChannel).where(YouTubeChannel.user_id == user.id)).all()
    found = next(((c, live) for c in channels for live in c.upcoming or [] if live["id"] == body.live_id), None)
    if found is None:
        raise HTTPException(404, "Not found.")
    channel, live = found
    if db.scalar(select(Post).where(Post.teaser_for == live["id"], Post.status != "cancelled")) is not None:
        raise HTTPException(409, "This live already has a teaser.")
    begins = parse_iso(live["start"])
    publish_at = begins - TEASER_BEFORE
    if publish_at < utcnow() + timedelta(minutes=20):
        raise HTTPException(409, "The live starts too soon for a teaser.")
    ready = ready_exports(db, request.app.state.settings, user)
    if not ready:
        raise HTTPException(409, "No finished export to use. Export a kept clip in the Library first.")
    clip, render = ready[0]
    title, description, tags = draft_text(db, clip)
    if clip.stream.link:     # a teaser points at the coming live, not at the old stream the clip came from
        description = description.replace(f"Full stream: {clip.stream.link}", "").strip()
    local = begins.replace(tzinfo=UTC).astimezone(zone(body.tz))
    hour = local.strftime("%I:%M %p").lstrip("0").replace(":00", "").lower()
    lead = f"LIVE at {hour} today! "
    link = f"https://www.youtube.com/watch?v={live['id']}"
    post = Post(user_id=user.id, clip_id=clip.id, render_id=render.id, channel_id=channel.id, mode="schedule",
                publish_at=publish_at, teaser_for=live["id"], tags=tags,
                title=(lead + title)[:posting.TITLE_MAX],
                description=f"🔴 Live at {hour} today: {link}" + ("\n\n" + description if description else ""))
    db.add(post)
    db.commit()
    return post_view(post)


class Move(BaseModel):
    publish_at: datetime


@router.put("/api/posts/{post_id}/time")
def move(post_id: str, body: Move, user=Depends(current_user), db=Depends(get_db)):
    """Move a draft to another time. An approved post is on its way to YouTube: change it in YouTube Studio."""
    post = own_post(db, user, post_id)
    if post.status != "draft":
        raise HTTPException(409, "Only drafts can be moved here. An approved post is changed in YouTube Studio.")
    moment = utc(body.publish_at)
    try:
        posting.check_time("schedule", moment)
    except posting.PostError as exc:
        raise HTTPException(422, str(exc)) from exc
    post.mode, post.publish_at, post.updated_at = "schedule", moment, utcnow()
    db.commit()
    return post_view(post)
