"""The weekly compilation (M3.8): a suggested set of the week's clips the creator can change and reorder,
then the render lane makes the video, three thumbnails, three titles and a description with chapters."""

import shutil
from datetime import timedelta
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from sqlalchemy import select

from ..db.models import AuditEntry, Clip, Render, Stream, utcnow
from ..jobs import read_json
from ..studio import compile, lane
from .deps import current_user, get_db

router = APIRouter()

MAX_WIDE_S = 20 * 60


def week_clips(db, user, days):
    since = utcnow() - timedelta(days=days)
    return db.scalars(select(Clip).join(Stream).where(Stream.user_id == user.id, Stream.status == "done",
                                                     Stream.created_at >= since)).all()


def piece_view(piece, clip, chosen):
    return {"clip_id": clip.id, "title": piece.title, "stream_title": clip.stream.title, "type": clip.type,
            "talk": piece.talk, "length_s": round(piece.length, 1), "kills": piece.kills, "kept": clip.decision == "keep",
            "chosen": chosen, "poster": f"/media/posters/{clip.id}"}


@router.get("/api/compilations/suggest")
def suggest(request: Request, days: int = 7, format: Literal["wide", "short"] = "wide", user=Depends(current_user),
            db=Depends(get_db)):
    """The suggested pieces in order, then every other usable clip of the period to add."""
    settings = request.app.state.settings
    clips = [c for c in week_clips(db, user, max(1, min(days, 31))) if c.decision != "reject"]
    short = format == "short"
    chosen = compile.suggest(clips, settings, short)
    by_id = {c.id: c for c in clips}
    picked = {p.clip_id for p in chosen}
    others = []
    for clip in sorted(clips, key=lambda c: (c.decision != "keep", -(c.score or 0))):
        if clip.id in picked:
            continue
        piece = compile.piece_for(settings, clip, short)
        if piece:
            others.append(piece_view(piece, clip, False))
    return {"format": format, "days": days, "total_s": round(sum(p.length for p in chosen), 1),
            "limit_s": compile.SHORT_MAX_S if short else compile.TARGET_S[1], "target_s": list(compile.TARGET_S),
            "pieces": [piece_view(p, by_id[p.clip_id], True) for p in chosen] + others[:40]}


class MakeBody(BaseModel):
    clip_ids: list[int] = Field(min_length=2, max_length=compile.MAX_PIECES)
    format: Literal["wide", "short"] = "wide"


@router.post("/api/compilations")
def make(body: MakeBody, request: Request, user=Depends(current_user), db=Depends(get_db)):
    settings = request.app.state.settings
    clips = {c.id: c for c in db.scalars(select(Clip).join(Stream).where(Clip.id.in_(body.clip_ids),
                                                                         Stream.user_id == user.id)).all()}
    if len(clips) != len(set(body.clip_ids)):
        raise HTTPException(404, "Some of those clips aren't yours.")
    short = body.format == "short"
    pieces = [compile.piece_for(settings, clips[i], short) for i in body.clip_ids]
    if any(p is None for p in pieces):
        raise HTTPException(409, "Some of those clips have no footage left on the laptop.")
    total = sum(p.length for p in pieces)
    limit = compile.SHORT_MAX_S if short else MAX_WIDE_S
    if total > limit + 0.5:
        raise HTTPException(422, f"That's {total / 60:.1f} minutes; the most is {limit / 60:.1f}.")
    render = Render(user_id=user.id, kind="compilation", params={"clip_ids": body.clip_ids, "format": body.format})
    db.add(render)
    db.add(AuditEntry(user_id=user.id, action="compilation", detail={"clips": body.clip_ids, "format": body.format}))
    db.commit()
    return view(settings, render)


def view(settings, render):
    out = {"id": render.id, "status": render.status, "error": render.error,
           "format": (render.params or {}).get("format", "wide"), "pieces": len((render.params or {}).get("clip_ids") or []),
           "created_at": render.created_at.isoformat() + "Z" if render.created_at else None}
    if render.status == "done":
        folder = lane.compilation_folder(settings.jobs_dir, render.user_id, render.id)
        plan, post = compile.load_plan(folder), read_json(folder / "post.json", {}) or {}
        out.update(video=f"/media/compilations/{render.id}/video", titles=plan.get("titles", []),
                   chapters=plan.get("chapters", []), description=post.get("description", ""),
                   length_s=round(sum(p["end"] - p["start"] for p in plan.get("pieces", [])), 1),
                   thumbnails=[f"/media/compilations/{render.id}/thumb_{n}" for n in (1, 2, 3)
                               if (folder / f"thumb_{n}.jpg").exists()])
    return out


def own(db, user, render_id):
    render = db.get(Render, render_id)
    if render is None or render.user_id != user.id or render.kind != "compilation":
        raise HTTPException(404, "Not found.")
    return render


@router.get("/api/compilations")
def listing(request: Request, user=Depends(current_user), db=Depends(get_db)):
    renders = db.scalars(select(Render).where(Render.user_id == user.id, Render.kind == "compilation")
                         .order_by(Render.created_at.desc()).limit(20)).all()
    return [view(request.app.state.settings, r) for r in renders]


@router.delete("/api/compilations/{render_id}", status_code=204)
def delete(render_id: str, request: Request, user=Depends(current_user), db=Depends(get_db)):
    render = own(db, user, render_id)
    if render.status in ("queued", "running"):
        raise HTTPException(409, "It's still being made.")
    shutil.rmtree(lane.compilation_folder(request.app.state.settings.jobs_dir, user.id, render.id), ignore_errors=True)
    db.delete(render)
    db.commit()


FILES = {"video": ("video.mp4", "video/mp4"), "thumb_1": ("thumb_1.jpg", "image/jpeg"),
         "thumb_2": ("thumb_2.jpg", "image/jpeg"), "thumb_3": ("thumb_3.jpg", "image/jpeg")}


@router.get("/media/compilations/{render_id}/{name}")
def media(render_id: str, name: str, request: Request, download: int = 0, user=Depends(current_user),
          db=Depends(get_db)):
    if name not in FILES:
        raise HTTPException(404, "Not found.")
    render = own(db, user, render_id)
    filename, media_type = FILES[name]
    path = lane.compilation_folder(request.app.state.settings.jobs_dir, user.id, render.id) / filename
    db.close()
    if not path.is_file():
        raise HTTPException(404, "Not ready.")
    return FileResponse(path, media_type=media_type, filename=f"kaatclip_week_{filename}" if download else None,
                        content_disposition_type="attachment" if download else "inline",
                        headers={"Cache-Control": "private, max-age=3600"})
