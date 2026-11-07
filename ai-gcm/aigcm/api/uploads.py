"""Resumable uploads with tus 1.0 core semantics (https://tus.io/protocols/resumable-upload), so the browser
can use the maintained tus-js-client (M2 review R5):

    POST   /api/uploads          Upload-Length, Upload-Metadata  ->  201, Location: /api/uploads/<id>
    HEAD   /api/uploads/<id>                                     ->  Upload-Offset, Upload-Length
    PATCH  /api/uploads/<id>     Upload-Offset, body = next bytes ->  204, Upload-Offset
    DELETE /api/uploads/<id>                                     ->  204 (cancel)

Each upload belongs to a new stream. The bytes are written straight into the stream's job folder as
source.<ext> (review R6), so the engine uses the file in place. When the last byte arrives the file is
checked with ffprobe; a readable video queues the stream for the worker. Chunks are small (the browser
sends 8 MB) so each request stays well inside Cloudflare's 100 MB and 125 s limits later on."""

import asyncio
import base64
import shutil
from datetime import timedelta
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.concurrency import run_in_threadpool
from sqlalchemy import select

from ..db.models import AuditEntry, LiveSession, Stream, Upload, new_id, utcnow
from .deps import current_user, get_db

router = APIRouter(prefix="/api/uploads")

TUS = {"Tus-Resumable": "1.0.0"}
EXTENSIONS = {".mp4", ".mkv", ".mov"}
GAMES = {"bgmi"}
MAX_OPEN_UPLOADS = 3            # unfinished uploads one creator may have at a time
STALE_AFTER = timedelta(days=3)  # unfinished uploads untouched this long are removed
_locks: dict[str, asyncio.Lock] = {}


def parse_metadata(header):
    """tus metadata: 'key base64value,key2 base64value2'."""
    meta = {}
    for pair in (header or "").split(","):
        parts = pair.strip().split(" ")
        if parts and parts[0]:
            try:
                meta[parts[0]] = base64.b64decode(parts[1]).decode("utf-8") if len(parts) > 1 else ""
            except (ValueError, UnicodeDecodeError):
                raise HTTPException(400, "Upload-Metadata is not valid base64.") from None
    return meta


def source_path(settings, stream, upload):
    return settings.jobs_dir / stream.job_dir / ("source" + Path(upload.filename).suffix.lower())


def committed_bytes(db):
    """Bytes promised to unfinished uploads but not written yet: the disk must keep room for them."""
    return sum(u.length - u.offset for u in db.scalars(select(Upload).where(Upload.completed_at.is_(None))))


def own_upload(db, user, upload_id):
    upload = db.get(Upload, upload_id)
    if upload is None or upload.user_id != user.id:
        raise HTTPException(404, "Not found.")
    return upload


@router.post("", status_code=201)
def create_upload(request: Request, user=Depends(current_user), db=Depends(get_db)):
    settings = request.app.state.settings
    try:
        length = int(request.headers.get("upload-length", ""))
    except ValueError:
        raise HTTPException(400, "Upload-Length is missing.") from None
    meta = parse_metadata(request.headers.get("upload-metadata"))
    filename = Path(meta.get("filename", "")).name[:200]
    if Path(filename).suffix.lower() not in EXTENSIONS:
        raise HTTPException(415, "Upload an MP4, MKV or MOV recording.")
    if length <= 0 or length > settings.max_upload_bytes:
        raise HTTPException(413, f"Recordings up to {settings.max_upload_bytes // 1024**3} GB can be uploaded.")
    game = meta.get("game", "bgmi").lower()
    if game not in GAMES:
        raise HTTPException(400, "Only BGMI streams for now.")
    open_uploads = db.scalars(select(Upload).where(Upload.user_id == user.id, Upload.completed_at.is_(None))).all()
    if len(open_uploads) >= MAX_OPEN_UPLOADS:
        raise HTTPException(429, "Finish or cancel your other uploads first.")
    settings.jobs_dir.mkdir(parents=True, exist_ok=True)
    free = shutil.disk_usage(settings.jobs_dir).free
    if free - committed_bytes(db) - length < settings.min_free_bytes:
        raise HTTPException(507, "The laptop is short of disk space right now. Try again later.")

    title = (meta.get("title") or Path(filename).stem).strip()[:300] or "Stream"
    recorded_on = meta.get("recorded_on") or None
    if recorded_on and (len(recorded_on) != 10 or recorded_on[4] != "-" or recorded_on[7] != "-"):
        recorded_on = None
    live = db.get(LiveSession, meta["live_session"]) if meta.get("live_session") else None
    if live is not None and live.user_id != user.id:
        live = None
    stream_id = new_id("st")
    stream = Stream(id=stream_id, job_dir=stream_id, user_id=user.id, title=title, game=game,
                    recorded_on=recorded_on, source_name=filename, size_bytes=length, status="uploading",
                    live_session_id=live.id if live else None)
    upload = Upload(user_id=user.id, stream_id=stream.id, filename=filename, length=length)
    db.add_all([stream, upload])
    db.flush()
    path = source_path(settings, stream, upload)
    path.parent.mkdir(parents=True, exist_ok=False)
    path.touch()
    db.add(AuditEntry(user_id=user.id, action="upload_start", detail={"stream": stream.id, "bytes": length}))
    db.commit()
    return Response(status_code=201, headers={**TUS, "Location": f"/api/uploads/{upload.id}",
                                              "X-Stream-Id": stream.id})


@router.head("/{upload_id}")
def upload_offset(upload_id: str, user=Depends(current_user), db=Depends(get_db)):
    upload = own_upload(db, user, upload_id)
    return Response(status_code=200, headers={**TUS, "Upload-Offset": str(upload.offset),
                                              "Upload-Length": str(upload.length), "Cache-Control": "no-store"})


def _finish(request, db, upload, stream):
    """Last byte in: check the file is a video the engine can read, then queue it."""
    from ..media import probe

    path = source_path(request.app.state.settings, stream, upload)
    upload.completed_at = utcnow()
    try:
        info = probe(path)
        if info["duration"] <= 0:
            raise ValueError("no duration")
    except Exception:  # ffprobe missing, unreadable file, no video stream...
        stream.status, stream.error = "failed", "This file isn't a video we can read. Upload an MP4, MKV or MOV recording."
        path.unlink(missing_ok=True)
    else:
        stream.status, stream.duration_s, stream.queued_at = "queued", round(info["duration"], 1), utcnow()
    db.add(AuditEntry(user_id=upload.user_id, action="upload_done", detail={"stream": stream.id, "status": stream.status}))
    db.commit()


@router.patch("/{upload_id}", status_code=204)
async def append_chunk(upload_id: str, request: Request, user=Depends(current_user), db=Depends(get_db)):
    settings = request.app.state.settings
    if request.headers.get("content-type") != "application/offset+octet-stream":
        raise HTTPException(415, "Content-Type must be application/offset+octet-stream.")
    lock = _locks.setdefault(upload_id, asyncio.Lock())
    async with lock:
        upload = own_upload(db, user, upload_id)
        if upload.completed_at is not None:
            raise HTTPException(409, "This upload is already complete.")
        try:
            claimed = int(request.headers.get("upload-offset", ""))
        except ValueError:
            raise HTTPException(400, "Upload-Offset is missing.") from None
        if claimed != upload.offset:
            # The browser lost track (e.g. a chunk landed but the answer didn't); it asks HEAD and resumes.
            raise HTTPException(409, "Upload-Offset doesn't match; ask for the current offset.")
        stream = db.get(Stream, upload.stream_id)
        path = source_path(settings, stream, upload)
        room = upload.length - upload.offset
        written = 0
        with open(path, "r+b") as f:
            f.seek(upload.offset)
            try:
                async for piece in request.stream():
                    if written + len(piece) > min(room, settings.max_chunk_bytes):
                        raise HTTPException(413, "Too many bytes in this request.")
                    await run_in_threadpool(f.write, piece)
                    written += len(piece)
            except HTTPException:
                raise
            except Exception:
                pass  # The connection dropped: keep what arrived; the browser resumes from the new offset.
            finally:
                f.flush()
                # Bytes that made it to the file count, even if the request failed half way.
                upload.offset += written
                upload.updated_at = utcnow()
                db.commit()
        if upload.offset == upload.length:
            await run_in_threadpool(_finish, request, db, upload, stream)
    return Response(status_code=204, headers={**TUS, "Upload-Offset": str(upload.offset)})


def remove_stream_files(settings, stream):
    folder = settings.jobs_dir / stream.job_dir
    if folder.is_dir() and folder.resolve().parent == settings.jobs_dir.resolve():
        shutil.rmtree(folder, ignore_errors=True)


@router.delete("/{upload_id}", status_code=204)
def cancel_upload(upload_id: str, request: Request, user=Depends(current_user), db=Depends(get_db)):
    upload = own_upload(db, user, upload_id)
    if upload.completed_at is not None:
        raise HTTPException(409, "This upload is complete; delete the stream instead.")
    stream = db.get(Stream, upload.stream_id)
    remove_stream_files(request.app.state.settings, stream)
    db.delete(stream)
    db.add(AuditEntry(user_id=user.id, action="upload_cancel", detail={"stream": stream.id}))
    db.commit()
    return Response(status_code=204, headers=TUS)


def expire_uploads(db, settings, now=None):
    """Remove unfinished uploads nobody touched for STALE_AFTER, with their half-written files. The worker
    calls this now and then. Returns the stream ids removed."""
    cutoff = (now or utcnow()) - STALE_AFTER
    stale = db.scalars(select(Upload).where(Upload.completed_at.is_(None), Upload.updated_at < cutoff)).all()
    removed = []
    for upload in stale:
        stream = db.get(Stream, upload.stream_id)
        if stream is not None:
            remove_stream_files(settings, stream)
            removed.append(stream.id)
            db.delete(stream)
    db.commit()
    return removed
