"""The library (M3.2): every clip across the creator's streams, with filters (stream, type, decision, flag,
edited, exported), search by what was said or the title, and a poster per clip, a page at a time so
hundreds of clips stay quick on a phone.

Search is a plain case-insensitive match of every word typed against the clip's spoken text, title and
reason. A creator has hundreds or a few thousand clips, where this takes milliseconds; SQLite's full-text
index (FTS5) can replace it if libraries grow far beyond that (M3 plan, decision 6)."""

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse
from sqlalchemy import and_, exists, func, or_, select

from ..db.models import Clip, Edit, Render, Stream
from ..studio import project
from .clips import clip_view, own_clip
from .deps import current_user, get_db

router = APIRouter()

PAGE = 40
MAX_PAGE = 60
MAX_TERMS = 6


def _like(term):
    return "%" + term.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_") + "%"


def matches(term):
    pattern = _like(term)
    return or_(Clip.spoken.ilike(pattern, escape="\\"), Clip.title.ilike(pattern, escape="\\"),
               Clip.why.ilike(pattern, escape="\\"))


EDITED = exists(select(Edit.id).where(Edit.clip_id == Clip.id))
EXPORTED = exists(select(Render.id).where(Render.clip_id == Clip.id, Render.kind == "export",
                                          Render.status == "done"))
FLAGGED = func.coalesce(func.json_array_length(Clip.details, "$.flags"), 0) > 0


@router.get("/api/library")
def library(request: Request, q: str = "", stream: str | None = None, type: str | None = None,
            decision: str | None = None, flag: bool = False, edited: bool = False, exported: bool = False,
            sort: str = "new", offset: int = 0, limit: int = PAGE, user=Depends(current_user), db=Depends(get_db)):
    settings = request.app.state.settings
    mine = Stream.user_id == user.id
    where = [mine]
    if stream:
        where.append(Clip.stream_id == stream)
    if type:
        where.append(Clip.type == type)
    if decision in ("keep", "reject"):
        where.append(Clip.decision == decision)
    elif decision == "none":
        where.append(Clip.decision.is_(None))
    if flag:
        where.append(FLAGGED)
    if edited:
        where.append(EDITED)
    if exported:
        where.append(EXPORTED)
    for term in q.split()[:MAX_TERMS]:
        where.append(matches(term[:60]))
    condition = and_(*where)

    total = db.scalar(select(func.count(Clip.id)).join(Stream).where(condition))
    order = [Clip.score.desc().nulls_last(), Clip.id] if sort == "score" else [Stream.created_at.desc(), Clip.rank]
    limit = max(1, min(limit, MAX_PAGE))
    rows = db.scalars(select(Clip).join(Stream).where(condition).order_by(*order)
                      .offset(max(0, offset)).limit(limit)).all()
    ids = [c.id for c in rows]
    edited_ids = set(db.scalars(select(Edit.clip_id).where(Edit.clip_id.in_(ids)))) if ids else set()
    exported_ids = set(db.scalars(select(Render.clip_id).where(Render.clip_id.in_(ids), Render.kind == "export",
                                                               Render.status == "done"))) if ids else set()
    items = [dict(clip_view(c), stream_title=c.stream.title, edited=c.id in edited_ids, exported=c.id in exported_ids,
                  poster=f"/media/posters/{c.id}" if project.poster_path(settings, c).exists() else None)
             for c in rows]

    streams = db.execute(select(Stream.id, Stream.title, func.count(Clip.id)).join(Clip).where(mine)
                         .group_by(Stream.id).order_by(Stream.created_at.desc())).all()
    types = db.execute(select(Clip.type, func.count(Clip.id)).join(Stream).where(mine)
                       .group_by(Clip.type).order_by(func.count(Clip.id).desc())).all()
    return {"items": items, "total": total, "offset": offset, "limit": limit,
            "facets": {"streams": [{"id": i, "title": t, "count": n} for i, t, n in streams],
                       "types": [{"type": t, "count": n} for t, n in types]}}


@router.get("/media/posters/{clip_id}")
def poster(clip_id: int, request: Request, user=Depends(current_user), db=Depends(get_db)):
    clip = own_clip(db, user, clip_id)
    path = project.poster_path(request.app.state.settings, clip)
    db.close()
    if not path.is_file():
        raise HTTPException(404, "No poster yet.")
    return FileResponse(path, media_type="image/jpeg", headers={"Cache-Control": "private, max-age=86400"})
