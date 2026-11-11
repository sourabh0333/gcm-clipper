"""Your channel (M4.6): for each connected channel, the last 28 days split into Shorts, live and videos (views,
watch time, subscribers; YouTube Analytics, "data through" its last day of numbers) and the recent uploads with
their views. Shown on the streams page. See plans/M4 Plan and post plan.md (M4.6)."""

from fastapi import APIRouter, Depends, Request
from sqlalchemy import select

from ..channel_data import refresh
from ..db.models import Post, YouTubeChannel, utcnow
from .deps import current_user, get_db
from .posts import stamp

router = APIRouter()
RECENT_SHOWN = 8


def kind_of(item):
    return "live" if item.get("live") else "shorts" if item.get("short") else "videos"


@router.get("/api/channel")
def your_channel(request: Request, user=Depends(current_user), db=Depends(get_db)):
    now = utcnow()
    out = []
    channels = db.scalars(select(YouTubeChannel).where(YouTubeChannel.user_id == user.id)
                          .order_by(YouTubeChannel.connected_at)).all()
    ours = {p.video_id for p in db.scalars(select(Post).where(Post.user_id == user.id, Post.video_id.is_not(None)))}
    for channel in channels:
        refresh(db, request.app.state.settings, request.app.state.http, channel, now, stats=True)
        uploads = sorted((i for i in channel.recent or [] if i.get("privacy") != "private" or i.get("id") in ours),
                         key=lambda i: i.get("at") or "", reverse=True)
        out.append({"id": channel.id, "title": channel.title, "thumbnail": channel.thumbnail, "status": channel.status,
                    "stats": channel.stats, "stats_at": stamp(channel.stats_at), "recent_at": stamp(channel.recent_at),
                    "uploads": [{"id": i["id"], "title": i.get("title") or "", "at": i.get("at"), "kind": kind_of(i),
                                 "views": i.get("views"), "kaatclip": i["id"] in ours,
                                 "url": f"https://youtube.com/{'shorts/' + i['id'] if i.get('short') else 'watch?v=' + i['id']}"}
                                for i in uploads[:RECENT_SHOWN]]})
    return {"channels": out}
