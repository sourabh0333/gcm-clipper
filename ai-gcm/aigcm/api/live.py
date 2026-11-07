"""The Live screen: a creator starts a live session when they go live and taps "Mark moment" during the
stream. Times are the server's clock (one clock for everyone, whatever the phone's is). When the
recording is uploaded with this session, the worker turns the markers into the job's markers.json,
counting from the session start (M2 review R8; a finer "shift markers" nudge comes with M2.8)."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select

from ..db.models import LiveSession, Marker, utcnow
from .deps import current_user, get_db

router = APIRouter(prefix="/api/live")
MAX_MARKERS = 300   # per session; a stuck button can't flood the job


class NewLive(BaseModel):
    title: str | None = None


def view(session, db):
    markers = db.scalars(select(Marker).where(Marker.live_session_id == session.id).order_by(Marker.at)).all()
    return {"id": session.id, "title": session.title, "started_at": session.started_at.isoformat() + "Z",
            "ended_at": session.ended_at.isoformat() + "Z" if session.ended_at else None,
            "markers": [round((m.at - session.started_at).total_seconds(), 1) for m in markers]}


def own_live(db, user, live_id):
    session = db.get(LiveSession, live_id)
    if session is None or session.user_id != user.id:
        raise HTTPException(404, "Not found.")
    return session


@router.get("")
def current(user=Depends(current_user), db=Depends(get_db)):
    """The open live session, and the last few ended ones to attach an upload to."""
    rows = db.scalars(select(LiveSession).where(LiveSession.user_id == user.id)
                      .order_by(LiveSession.started_at.desc()).limit(6)).all()
    open_one = next((s for s in rows if s.ended_at is None), None)
    return {"open": view(open_one, db) if open_one else None,
            "recent": [view(s, db) for s in rows if s.ended_at is not None][:5]}


@router.post("", status_code=201)
def go_live(body: NewLive, user=Depends(current_user), db=Depends(get_db)):
    for old in db.scalars(select(LiveSession).where(LiveSession.user_id == user.id, LiveSession.ended_at.is_(None))):
        old.ended_at = utcnow()
    session = LiveSession(user_id=user.id, title=(body.title or "").strip()[:300] or None)
    db.add(session)
    db.commit()
    return view(session, db)


@router.post("/{live_id}/markers")
def mark(live_id: str, user=Depends(current_user), db=Depends(get_db)):
    session = own_live(db, user, live_id)
    if session.ended_at is not None:
        raise HTTPException(409, "This live session has ended.")
    if db.query(Marker).filter_by(live_session_id=live_id).count() >= MAX_MARKERS:
        raise HTTPException(429, "That's a lot of marks for one stream.")
    db.add(Marker(user_id=user.id, live_session_id=live_id, source="button"))
    db.commit()
    return view(session, db)


@router.delete("/{live_id}/markers/last")
def unmark(live_id: str, user=Depends(current_user), db=Depends(get_db)):
    session = own_live(db, user, live_id)
    last = db.scalars(select(Marker).where(Marker.live_session_id == live_id).order_by(Marker.at.desc())).first()
    if last is not None:
        db.delete(last)
        db.commit()
    return view(session, db)


@router.post("/{live_id}/end")
def end(live_id: str, user=Depends(current_user), db=Depends(get_db)):
    session = own_live(db, user, live_id)
    session.ended_at = session.ended_at or utcnow()
    db.commit()
    return view(session, db)


def markers_file(db, stream):
    """The engine's markers.json content for a stream uploaded with a live session: seconds from the
    session's start, which is taken as the recording's start."""
    if not stream.live_session_id:
        return []
    session = db.get(LiveSession, stream.live_session_id)
    rows = db.scalars(select(Marker).where(Marker.live_session_id == session.id).order_by(Marker.at)).all()
    return [{"t": round((m.at - session.started_at).total_seconds(), 2), "source": m.source, "by": "creator"}
            for m in rows]
