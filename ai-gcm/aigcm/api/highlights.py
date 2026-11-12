"""Highlights Stage 1 (plans/Highlights Stage 1 plan.md): the stream map, the kill-match highlight made from it
(the 16:9 video, thumbnails, titles, Shorts cut from it), and one stream's batch of posts with suggested times.

Nothing posts by itself: "Plan the posts" makes drafts in the calendar, which the creator approves as usual."""

import shutil
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from sqlalchemy import select

from ..db.models import AuditEntry, Clip, Post, Render, utcnow
from ..jobs import read_json
from ..studio import lane, project
from .deps import current_user, get_db, own_stream

router = APIRouter()

INDIA = ZoneInfo("Asia/Kolkata")
LONG_AT = time(12, 0)          # research: records and match cuts go up around noon the next day
SHORT_AT = time(21, 0)         # Shorts at 21:00-22:00
TEASER_AT = time(21, 30)


def _stamp(value):
    return value.isoformat() + "Z" if value else None


def map_view(stream_map):
    """What the phone needs from the map: the parts as a bar and each match's story."""
    if not stream_map:
        return None
    matches = [{k: m.get(k) for k in ("n", "start", "end", "ended", "placement", "kills", "score")}
               | {"fights": len(m.get("fights") or []), "map": ((m.get("mode") or {}).get("map")),
                  "mode": ((m.get("mode") or {}).get("mode"))}
               for m in stream_map.get("matches", [])]
    return {"duration": stream_map.get("duration"), "parts": stream_map.get("parts", []), "matches": matches,
            "best": stream_map.get("best"), "session": stream_map.get("session") or []}


def highlight_view(settings, db, render):
    params = render.params or {}
    out = {"id": render.id, "status": render.status, "error": render.error, "stream_id": params.get("stream_id"),
           "matches": params.get("matches"), "session": bool(params.get("session")), "auto": bool(params.get("auto")),
           "created_at": _stamp(render.created_at)}
    if render.status != "done":
        return out
    stream = own_stream_of(db, render)
    folder = lane.highlight_folder(settings, stream, render.id)
    result = read_json(folder / "result.json", {}) or {}
    plan = read_json(folder / "plan.json", {}) or {}
    names = read_json(folder / "titles.json", {}) or {}
    post = read_json(folder / "post.json", {}) or {}
    shorts = db.scalars(select(Clip).where(Clip.stream_id == stream.id)).all()
    shorts = [c for c in shorts if (c.details or {}).get("from_highlight") == render.id]
    pieces = []
    for i, p in enumerate(plan.get("pieces", [])):
        if p["kind"] == "card":
            pieces.append({"i": i, "kind": "card", "text": p.get("text") or "", "length": p.get("length")})
        else:
            pieces.append({"i": i, "kind": p["kind"], "start": p["start"], "end": p["end"],
                           "length": round(p["end"] - p["start"], 1), "kills": p.get("kills", 0),
                           "title": p.get("title"), "match": p.get("match"), "punch": len(p.get("punch") or [])})
    posts = db.scalars(select(Post).where(Post.render_id == render.id)).all()
    out.update(matches=result.get("matches"), length_s=result.get("length"), kept=result.get("kept"),
               kills=result.get("kills"), label=result.get("label"), titles=names.get("titles", []),
               description=post.get("description", ""), pieces=pieces, dropped=plan.get("dropped", []),
               video=f"/media/highlights/{render.id}/video", play=f"/media/highlights/{render.id}/video?view=1",
               thumbnails=[f"/media/highlights/{render.id}/thumb_{n}" for n in (1, 2, 3)
                           if (folder / f"thumb_{n}.jpg").exists()],
               shorts=[{"clip_id": c.id, "title": c.title, "role": (c.details or {}).get("role"),
                        "length_s": round(c.end_s - c.start_s, 1), "poster": f"/media/posters/{c.id}",
                        "decision": c.decision} for c in sorted(shorts, key=lambda c: c.rank)],
               posts=[{"id": p.id, "status": p.status, "publish_at": _stamp(p.publish_at)} for p in posts])
    return out


def own_stream_of(db, render):
    from ..db.models import Stream

    return db.get(Stream, (render.params or {}).get("stream_id"))


def own_highlight(db, user, render_id):
    render = db.get(Render, render_id)
    if render is None or render.user_id != user.id or render.kind != "highlight":
        raise HTTPException(404, "Not found.")
    return render


@router.get("/api/streams/{stream_id}/highlights")
def stream_highlights(stream_id: str, request: Request, user=Depends(current_user), db=Depends(get_db)):
    """The stream's map (or whether it's being made) and its highlights, newest first."""
    settings = request.app.state.settings
    stream = own_stream(db, user, stream_id)
    folder = settings.jobs_dir / stream.job_dir
    mapping = db.scalars(select(Render).where(Render.kind == "map", Render.user_id == user.id)
                         .order_by(Render.created_at.desc())).all()
    mapping = next((r for r in mapping if (r.params or {}).get("stream_id") == stream.id), None)
    renders = db.scalars(select(Render).where(Render.kind == "highlight", Render.user_id == user.id)
                         .order_by(Render.created_at.desc())).all()
    renders = [r for r in renders if (r.params or {}).get("stream_id") == stream.id]
    from ..leftovers import summary

    left = summary(folder)
    return {"map": map_view(read_json(folder / "map.json")),
            "leftovers": {"count": left["count"],
                          "until": _stamp(datetime.utcfromtimestamp(left["until"])) if left["until"] else None},
            "map_status": mapping.status if mapping else None,
            "has_source": project.source_file(folder) is not None,
            "highlights": [highlight_view(settings, db, r) for r in renders]}


@router.post("/api/streams/{stream_id}/map")
def make_map(stream_id: str, user=Depends(current_user), db=Depends(get_db)):
    """Build (or rebuild) the stream's map."""
    stream = own_stream(db, user, stream_id)
    if stream.status != "done":
        raise HTTPException(409, "The stream is still being processed.")
    render = project.queue_map(db, stream)
    db.commit()
    return {"status": render.status}


class MakeBody(BaseModel):
    matches: list[int] | None = Field(default=None, max_length=8)
    session: bool = False
    drop: list[int] = Field(default_factory=list, max_length=200)


@router.post("/api/streams/{stream_id}/highlights")
def make(stream_id: str, body: MakeBody, request: Request, user=Depends(current_user), db=Depends(get_db)):
    """A highlight of the chosen matches (default: the best match; session: the strong matches in order),
    optionally without some of a previous plan's pieces (drop: their numbers)."""
    settings = request.app.state.settings
    stream = own_stream(db, user, stream_id)
    folder = settings.jobs_dir / stream.job_dir
    stream_map = read_json(folder / "map.json")
    if not stream_map:
        raise HTTPException(409, "The stream map isn't ready yet.")
    if project.source_file(folder) is None:
        raise HTTPException(409, "The recording is no longer on the laptop.")
    known = {m["n"] for m in stream_map["matches"]}
    if body.matches and not set(body.matches) <= known:
        raise HTTPException(422, "No such match in this stream.")
    if not body.matches and not stream_map.get("best"):
        raise HTTPException(409, "No match with kills was found in this stream.")
    render = Render(user_id=user.id, kind="highlight",
                    params={"stream_id": stream.id, "matches": sorted(body.matches) if body.matches else None,
                            "session": body.session, "drop": sorted(set(body.drop))})
    db.add(render)
    db.add(AuditEntry(user_id=user.id, action="highlight", detail={"stream": stream.id, "matches": body.matches,
                                                                     "session": body.session}))
    db.commit()
    return highlight_view(settings, db, render)


@router.get("/api/highlights/{render_id}")
def get(render_id: str, request: Request, user=Depends(current_user), db=Depends(get_db)):
    return highlight_view(request.app.state.settings, db, own_highlight(db, user, render_id))


@router.delete("/api/highlights/{render_id}", status_code=204)
def delete(render_id: str, request: Request, user=Depends(current_user), db=Depends(get_db)):
    """Delete a highlight (its video and thumbnails); its Shorts stay as clips of the stream."""
    render = own_highlight(db, user, render_id)
    if render.status in ("queued", "running"):
        raise HTTPException(409, "It's still being made.")
    if db.scalar(select(Post).where(Post.render_id == render.id, Post.status != "draft")):
        raise HTTPException(409, "It's approved for posting; cancel the post first.")
    for post in db.scalars(select(Post).where(Post.render_id == render.id)).all():
        db.delete(post)
    stream = own_stream_of(db, render)
    if stream is not None:
        shutil.rmtree(lane.highlight_folder(request.app.state.settings, stream, render.id), ignore_errors=True)
    db.delete(render)
    db.commit()


def suggested_times(now, shorts):
    """The batch's times in India (decision 4): the teaser tonight at 21:30 (tomorrow if that's under two
    hours away), the highlight at noon the next day, the other Shorts at 21:00 on the days after."""
    local = now.replace(tzinfo=ZoneInfo("UTC")).astimezone(INDIA)
    teaser_day = local.date() if local.time() <= time(19, 30) else local.date() + timedelta(days=1)

    def at(day, clock):
        moment = datetime.combine(day, clock, INDIA).astimezone(ZoneInfo("UTC")).replace(tzinfo=None)
        return moment

    long_day = teaser_day + timedelta(days=1)
    times = {"video": at(long_day, LONG_AT)}
    n = 0
    for short in shorts:
        if short["role"] == "teaser":
            times[short["clip_id"]] = at(teaser_day, TEASER_AT)
        else:
            n += 1
            times[short["clip_id"]] = at(long_day + timedelta(days=n), SHORT_AT)
    return times


@router.post("/api/highlights/{render_id}/plan-posts")
def plan_posts(render_id: str, request: Request, user=Depends(current_user), db=Depends(get_db)):
    """One stream, one batch (decision 4): drafts for the highlight and its Shorts at suggested times. Shorts
    need a finished export first; those without one are listed so the creator can export them. Never approved
    here: the creator approves in Posts."""
    from .posts import draft_text, highlight_draft, post_view

    settings = request.app.state.settings
    render = own_highlight(db, user, render_id)
    view = highlight_view(settings, db, render)
    if render.status != "done":
        raise HTTPException(409, "This highlight isn't finished yet.")
    times = suggested_times(utcnow(), view["shorts"])
    made, waiting = [], []
    long_post = highlight_draft(db, settings, user, render, publish_at=times["video"])
    if long_post.publish_at is None:
        long_post.publish_at = times["video"]
    made.append(long_post)
    for short in view["shorts"]:
        clip = db.get(Clip, short["clip_id"])
        export = db.scalar(select(Render).where(Render.clip_id == clip.id, Render.kind == "export",
                                                Render.status == "done").order_by(Render.created_at.desc()))
        if export is None or lane.export_path(settings, clip, export) is None:
            waiting.append(short["clip_id"])
            if not db.scalar(select(Render).where(Render.clip_id == clip.id, Render.kind.in_(("prepare", "export")),
                                                  Render.status.in_(("queued", "running")))):
                project.queue_prepare_and_export(db, settings, clip)
            continue
        post = db.scalar(select(Post).where(Post.render_id == export.id, Post.status == "draft"))
        if post is None:
            channel = long_post.channel_id
            title, description, tags = draft_text(db, clip)
            post = Post(user_id=user.id, clip_id=clip.id, render_id=export.id, channel_id=channel, title=title,
                        description=description, tags=tags)
            db.add(post)
        post.publish_at = post.publish_at or times[short["clip_id"]]
        made.append(post)
    db.commit()
    return {"posts": [post_view(p) for p in made], "waiting": waiting}


FILES = {"video": ("video.mp4", "video/mp4"), "thumb_1": ("thumb_1.jpg", "image/jpeg"),
         "thumb_2": ("thumb_2.jpg", "image/jpeg"), "thumb_3": ("thumb_3.jpg", "image/jpeg")}


@router.get("/media/highlights/{render_id}/{name}")
def media(render_id: str, name: str, request: Request, download: int = 0, view: int = 0, user=Depends(current_user),
          db=Depends(get_db)):
    if name not in FILES:
        raise HTTPException(404, "Not found.")
    render = own_highlight(db, user, render_id)
    stream = own_stream_of(db, render)
    db.close()
    if stream is None:
        raise HTTPException(404, "Not found.")
    filename, media_type = FILES[name]
    path = lane.highlight_folder(request.app.state.settings, stream, render.id) / filename
    if name == "video" and view and not download and lane.view_path(path).is_file():
        path = lane.view_path(path)
    if not path.is_file():
        raise HTTPException(404, "Not ready.")
    return FileResponse(path, media_type=media_type, filename=f"kaatclip_highlight_{filename}" if download else None,
                        content_disposition_type="attachment" if download else "inline",
                        headers={"Cache-Control": "private, max-age=3600"})
