"""A creator's streams. M2.2 has the read side, so access rules are tested from the start; uploads add
streams in M2.3 and the worker fills in their progress in M2.4."""

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy import select

from ..db.models import AuditEntry, Stream, Upload
from .deps import current_user, get_db, own_stream

router = APIRouter(prefix="/api/streams")


def stream_summary(stream, db=None):
    out = {"id": stream.id, "title": stream.title, "game": stream.game, "status": stream.status,
           "recorded_on": stream.recorded_on, "duration_s": stream.duration_s, "size_bytes": stream.size_bytes,
           "error": stream.error, "created_at": stream.created_at.isoformat()}
    if stream.status == "uploading" and db is not None:
        upload = db.scalar(select(Upload).where(Upload.stream_id == stream.id))
        if upload is not None:
            out["upload"] = {"id": upload.id, "offset": upload.offset, "length": upload.length}
    return out


@router.get("")
def list_streams(user=Depends(current_user), db=Depends(get_db)):
    rows = db.scalars(select(Stream).where(Stream.user_id == user.id).order_by(Stream.created_at.desc()))
    return [stream_summary(s, db) for s in rows]


@router.get("/{stream_id}")
def get_stream(stream_id: str, user=Depends(current_user), db=Depends(get_db)):
    return stream_summary(own_stream(db, user, stream_id), db)


@router.delete("/{stream_id}", status_code=204)
def delete_stream(stream_id: str, request: Request, user=Depends(current_user), db=Depends(get_db)):
    """Delete a stream with its recording, analysis and clips. A stream being processed must be stopped
    first, so the worker never works on a folder that is going away."""
    from .uploads import remove_stream_files

    stream = own_stream(db, user, stream_id)
    if stream.status == "running":
        raise HTTPException(409, "This stream is being processed. Stop it first.")
    remove_stream_files(request.app.state.settings, stream)
    db.delete(stream)
    db.add(AuditEntry(user_id=user.id, action="stream_delete", detail={"stream": stream_id}))
    db.commit()
    return Response(status_code=204)
