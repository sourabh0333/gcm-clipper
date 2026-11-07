"""A creator's streams. M2.2 has the read side, so access rules are tested from the start; uploads add
streams in M2.3 and the worker fills in their progress in M2.4."""

from fastapi import APIRouter, Depends
from sqlalchemy import select

from ..db.models import Stream
from .deps import current_user, get_db, own_stream

router = APIRouter(prefix="/api/streams")


def stream_summary(stream):
    return {"id": stream.id, "title": stream.title, "game": stream.game, "status": stream.status,
            "recorded_on": stream.recorded_on, "duration_s": stream.duration_s, "error": stream.error,
            "created_at": stream.created_at.isoformat()}


@router.get("")
def list_streams(user=Depends(current_user), db=Depends(get_db)):
    rows = db.scalars(select(Stream).where(Stream.user_id == user.id).order_by(Stream.created_at.desc()))
    return [stream_summary(s) for s in rows]


@router.get("/{stream_id}")
def get_stream(stream_id: str, user=Depends(current_user), db=Depends(get_db)):
    return stream_summary(own_stream(db, user, stream_id))
