"""Reviewing clips: the clips of a stream, keep or reject (with an optional reason, and undo), every kept
clip across streams, and the clip videos themselves, streamed with Range support for phone players and
only ever to their owner."""

from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy import select

from ..db.models import AuditEntry, Clip, Stream, utcnow
from .deps import current_user, get_db, own_stream

router = APIRouter()

REASONS = {"bad_cut", "not_interesting", "wrong_moment", "duplicate", "other"}


def clip_view(clip):
    details = clip.details or {}
    return {
        "id": clip.id, "stream_id": clip.stream_id, "rank": clip.rank, "start_s": clip.start_s, "end_s": clip.end_s,
        "length_s": round(clip.end_s - clip.start_s, 1), "type": clip.type, "score": clip.score,
        "title": clip.title, "why": clip.why, "titles": details.get("titles") or [],
        "hashtags": details.get("hashtags") or [], "description": details.get("description"),
        "labels": details.get("labels") or {}, "flags": details.get("flags") or [],
        "decision": clip.decision, "reason": clip.decision_reason,
        "video": f"/media/clips/{clip.id}", "play": f"/media/clips/{clip.id}?view=1", "safe_video": f"/media/clips/{clip.id}?safe=1" if clip.safe_file_name else None,
    }


def own_clip(db, user, clip_id):
    clip = db.get(Clip, clip_id)
    if clip is None or clip.stream.user_id != user.id:
        raise HTTPException(404, "Not found.")
    return clip


@router.get("/api/streams/{stream_id}/clips")
def stream_clips(stream_id: str, user=Depends(current_user), db=Depends(get_db)):
    return [clip_view(c) for c in own_stream(db, user, stream_id).clips]


@router.get("/api/clips")
def all_clips(decision: str | None = None, user=Depends(current_user), db=Depends(get_db)):
    """Clips across all of the creator's streams, newest stream first; `decision=keep` for the kept list."""
    query = select(Clip).join(Stream).where(Stream.user_id == user.id)
    if decision in ("keep", "reject"):
        query = query.where(Clip.decision == decision)
    elif decision == "none":
        query = query.where(Clip.decision.is_(None))
    rows = db.scalars(query.order_by(Stream.created_at.desc(), Clip.rank)).all()
    return [dict(clip_view(c), stream_title=c.stream.title) for c in rows]


class Decision(BaseModel):
    verdict: str | None          # keep, reject, or null to undo
    reason: str | None = None    # one of REASONS, for rejects


@router.post("/api/clips/{clip_id}/decision")
def decide(clip_id: int, body: Decision, request: Request, user=Depends(current_user), db=Depends(get_db)):
    clip = own_clip(db, user, clip_id)
    if body.verdict not in ("keep", "reject", None):
        raise HTTPException(400, "verdict must be keep, reject or null.")
    reason = body.reason if body.verdict == "reject" and body.reason in REASONS else None
    clip.decision, clip.decision_reason = body.verdict, reason
    clip.decided_at = utcnow() if body.verdict else None
    db.add(AuditEntry(user_id=user.id, action="decision", detail={"clip": clip.id, "verdict": body.verdict,
                                                                   "reason": reason}))
    if body.verdict == "keep":
        # Save the clip's footage for the studio now, while the stream's recording is still on the laptop.
        from ..studio.project import queue_prepare

        queue_prepare(db, request.app.state.settings, clip)
    db.commit()
    return clip_view(clip)


def lighter(request, path, stream_id):
    """The light copy of a video for playing in the app, if made; otherwise the full file, and the stream's
    posters job is queued to make the missing light copies (once, in the background)."""
    from ..studio import lane, project

    light = lane.view_path(path)
    if light.is_file():
        return light
    with request.app.state.sessions() as writer:
        stream = writer.get(Stream, stream_id)
        if stream is not None:
            project.queue_posters(writer, stream)
            writer.commit()
    return path


@router.get("/media/clips/{clip_id}")
def clip_video(clip_id: int, request: Request, safe: int = 0, download: int = 0, view: int = 0,
               user=Depends(current_user), db=Depends(get_db)):
    clip = own_clip(db, user, clip_id)
    name = clip.safe_file_name if safe else clip.file_name
    if not name:
        raise HTTPException(404, "Not found.")
    folder = (request.app.state.settings.jobs_dir / clip.stream.job_dir / "clips").resolve()
    path = (folder / Path(name).name).resolve()
    stream_id = clip.stream_id
    db.close()  # the video may stream for minutes; no transaction may stay open that long
    if path.parent != folder or not path.is_file():
        raise HTTPException(404, "This clip's video is no longer on the laptop.")
    if view and not safe and not download:
        path = lighter(request, path, stream_id)
    return FileResponse(path, media_type="video/mp4", filename=path.name if download else None,
                        content_disposition_type="attachment" if download else "inline",
                        headers={"Cache-Control": "private, max-age=3600"})
