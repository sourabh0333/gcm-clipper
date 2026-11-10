"""A creator's streams. M2.2 has the read side, so access rules are tested from the start; uploads add
streams in M2.3 and the worker fills in their progress in M2.4."""

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy import select

from datetime import timedelta

from .. import jobview
from ..db.models import AuditEntry, Stream, Upload, WorkerState, utcnow
from .deps import current_user, get_db, own_stream

router = APIRouter(prefix="/api/streams")


def stream_summary(stream, db=None, jobs_dir=None):
    out = {"id": stream.id, "title": stream.title, "game": stream.game, "status": stream.status,
           "recorded_on": stream.recorded_on, "link": stream.link, "duration_s": stream.duration_s, "size_bytes": stream.size_bytes,
           "error": stream.error, "stopping": stream.stop_requested, "created_at": stream.created_at.isoformat(),
           "clips": len(stream.clips), "kept": sum(c.decision == "keep" for c in stream.clips),
           "reviewed": sum(c.decision is not None for c in stream.clips)}
    if stream.status == "uploading" and db is not None:
        upload = db.scalar(select(Upload).where(Upload.stream_id == stream.id))
        if upload is not None:
            out["upload"] = {"id": upload.id, "offset": upload.offset, "length": upload.length}
    if stream.status in ("running", "stopped", "failed") and jobs_dir is not None:
        out["progress"] = jobview.progress(jobs_dir / stream.job_dir, stream.duration_s)
    return out


@router.get("")
def list_streams(request: Request, user=Depends(current_user), db=Depends(get_db)):
    rows = db.scalars(select(Stream).where(Stream.user_id == user.id).order_by(Stream.created_at.desc()))
    return [stream_summary(s, db, request.app.state.settings.jobs_dir) for s in rows]


@router.get("/{stream_id}")
def get_stream(stream_id: str, request: Request, user=Depends(current_user), db=Depends(get_db)):
    return stream_summary(own_stream(db, user, stream_id), db, request.app.state.settings.jobs_dir)


@router.post("/{stream_id}/stop")
def stop_stream(stream_id: str, request: Request, user=Depends(current_user), db=Depends(get_db)):
    """A queued stream stops at once; a running one is stopped by the worker within a few seconds."""
    stream = own_stream(db, user, stream_id)
    if stream.status == "queued":
        stream.status = "stopped"
    elif stream.status == "running":
        stream.stop_requested = True
    else:
        raise HTTPException(409, "This stream is not being processed.")
    db.add(AuditEntry(user_id=user.id, action="stream_stop", detail={"stream": stream_id}))
    db.commit()
    return stream_summary(stream, db, request.app.state.settings.jobs_dir)


@router.post("/{stream_id}/resume")
def resume_stream(stream_id: str, request: Request, user=Depends(current_user), db=Depends(get_db)):
    """Put a stopped or failed stream back in the queue; the engine carries on from its checkpoints."""
    from ..worker import source_file

    stream = own_stream(db, user, stream_id)
    if stream.status not in ("stopped", "failed"):
        raise HTTPException(409, "Only a stopped or failed stream can be resumed.")
    if source_file(request.app.state.settings.jobs_dir / stream.job_dir) is None:
        raise HTTPException(409, "The recording is no longer on the laptop. Upload it again.")
    stream.status, stream.error, stream.stop_requested, stream.queued_at = "queued", None, False, utcnow()
    db.add(AuditEntry(user_id=user.id, action="stream_resume", detail={"stream": stream_id}))
    db.commit()
    return stream_summary(stream, db, request.app.state.settings.jobs_dir)


worker_router = APIRouter()


@worker_router.get("/api/worker")
def worker_status(user=Depends(current_user), db=Depends(get_db)):
    """Whether the laptop's worker is running (it writes a heartbeat every few seconds)."""
    state = db.get(WorkerState, 1)
    online = bool(state and state.heartbeat_at and utcnow() - state.heartbeat_at < timedelta(seconds=60))
    queued = db.scalar(select(Stream.id).where(Stream.status == "queued").limit(1)) is not None
    return {"online": online, "busy": bool(online and state.stream_id), "queue_waiting": queued}


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
