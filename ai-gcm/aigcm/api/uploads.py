"""Resumable uploads with tus 1.0 core semantics (https://tus.io/protocols/resumable-upload), so the browser
can use the maintained tus-js-client (M2 review R5):

    POST   /api/uploads          Upload-Length, Upload-Metadata  ->  201, Location: /api/uploads/<id>
    HEAD   /api/uploads/<id>                                     ->  Upload-Offset, Upload-Length
    PATCH  /api/uploads/<id>     Upload-Offset, body = next bytes ->  204, Upload-Offset
    DELETE /api/uploads/<id>                                     ->  204 (cancel)

Each upload belongs to a new stream. The bytes are written straight into the stream's job folder as
source.<ext> (review R6), so the engine uses the file in place. When the last byte arrives the file is
checked with ffprobe; a readable video queues the stream for the worker. Chunks are small (the browser
sends 8 MB) so each request stays well inside Cloudflare's 100 MB and 125 s limits later on.

Uploading while streaming: the browser creates the upload with `Upload-Defer-Length: 1` (tus
creation-defer-length) because OBS is still writing the recording, sends the file as it grows, and gives the
final size with the last PATCH. When recording stops, OBS rewrites the start of an MKV or MP4 (measured 11 Nov:
the first 64 KB), so before the last bytes the browser compares piece hashes (`GET .../hashes`) and re-sends any
piece that changed (`PUT .../rewrite?at=`)."""

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
GROWING_RESERVE = 12 * 1024**3   # disk kept free for a recording of unknown size (a long 1080p OBS stream)
HASH_PIECE = 8 * 1024 * 1024     # the piece size for comparing the laptop's copy with the finished recording
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
    return sum(max(0, (u.length or (GROWING_RESERVE if u.growing else 0)) - u.offset)
               for u in db.scalars(select(Upload).where(Upload.completed_at.is_(None))))


def own_upload(db, user, upload_id):
    upload = db.get(Upload, upload_id)
    if upload is None or upload.user_id != user.id:
        raise HTTPException(404, "Not found.")
    return upload


@router.post("", status_code=201)
def create_upload(request: Request, user=Depends(current_user), db=Depends(get_db)):
    settings = request.app.state.settings
    growing = request.headers.get("upload-defer-length") == "1"
    try:
        length = 0 if growing else int(request.headers.get("upload-length", ""))
    except ValueError:
        raise HTTPException(400, "Upload-Length is missing.") from None
    meta = parse_metadata(request.headers.get("upload-metadata"))
    filename = Path(meta.get("filename", "")).name[:200]
    if Path(filename).suffix.lower() not in EXTENSIONS:
        raise HTTPException(415, "Upload an MP4, MKV or MOV recording.")
    if not growing and (length <= 0 or length > settings.max_upload_bytes):
        raise HTTPException(413, f"Recordings up to {settings.max_upload_bytes // 1024**3} GB can be uploaded.")
    game = meta.get("game", "bgmi").lower()
    if game not in GAMES:
        raise HTTPException(400, "Only BGMI streams for now.")
    open_uploads = db.scalars(select(Upload).where(Upload.user_id == user.id, Upload.completed_at.is_(None))).all()
    if len(open_uploads) >= MAX_OPEN_UPLOADS:
        raise HTTPException(429, "Finish or cancel your other uploads first.")
    settings.jobs_dir.mkdir(parents=True, exist_ok=True)
    free = shutil.disk_usage(settings.jobs_dir).free
    if free - committed_bytes(db) - (GROWING_RESERVE if growing else length) < settings.min_free_bytes:
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
                    recorded_on=recorded_on, source_name=filename, size_bytes=length or None, status="uploading",
                    live_session_id=live.id if live else None)
    upload = Upload(user_id=user.id, stream_id=stream.id, filename=filename, length=length, growing=growing)
    db.add_all([stream, upload])
    db.flush()
    path = source_path(settings, stream, upload)
    path.parent.mkdir(parents=True, exist_ok=False)
    path.touch()
    db.add(AuditEntry(user_id=user.id, action="upload_start",
                      detail={"stream": stream.id, "bytes": length, "growing": growing}))
    db.commit()
    return Response(status_code=201, headers={**TUS, "Location": f"/api/uploads/{upload.id}",
                                              "X-Stream-Id": stream.id})


@router.head("/{upload_id}")
def upload_offset(upload_id: str, user=Depends(current_user), db=Depends(get_db)):
    upload = own_upload(db, user, upload_id)
    size = {"Upload-Length": str(upload.length)} if upload.length else {"Upload-Defer-Length": "1"}
    return Response(status_code=200, headers={**TUS, "Upload-Offset": str(upload.offset), **size,
                                              "Cache-Control": "no-store", "X-Stream-Id": upload.stream_id})


def _finish(db, upload_id, path):
    """Last byte in: check the file is a video the engine can read, then queue it. ffprobe runs before any
    transaction opens, so the database isn't held while it reads the file."""
    from ..media import probe

    try:
        info = probe(path)
        if info["duration"] <= 0:
            raise ValueError("no duration")
    except Exception:  # ffprobe missing, unreadable file, no video stream...
        info = None
        path.unlink(missing_ok=True)
    upload = db.get(Upload, upload_id)
    stream = db.get(Stream, upload.stream_id)
    upload.completed_at = utcnow()
    stream.size_bytes = upload.length
    if info is None:
        stream.status, stream.error = "failed", "This file isn't a video we can read. Upload an MP4, MKV or MOV recording."
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
        if upload.growing and not upload.length and request.headers.get("upload-length"):
            # The recording has stopped: this is its final size (tus creation-defer-length).
            try:
                final = int(request.headers["upload-length"])
            except ValueError:
                raise HTTPException(400, "Upload-Length is not a number.") from None
            if final < upload.offset or final > settings.max_upload_bytes:
                raise HTTPException(413, "That final size doesn't fit this upload.")
            upload.length = final
        stream = db.get(Stream, upload.stream_id)
        path = source_path(settings, stream, upload)
        start, length, stream_id = upload.offset, upload.length, upload.stream_id
        room = (length or settings.max_upload_bytes) - start   # a growing recording's size is unknown yet
        # Receiving a chunk can take a minute on mobile data: no transaction stays open meanwhile.
        db.commit()
        written = 0
        with open(path, "r+b") as f:
            f.seek(start)
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
                # Bytes that made it to the file count, even if the request failed half way. The lock above
                # keeps this the only writer of this upload's offset.
                upload = db.get(Upload, upload_id)
                upload.offset = start + written
                upload.updated_at = utcnow()
                db.commit()
        offset = start + written
        if length and offset == length:
            await run_in_threadpool(_finish, db, upload_id, path)
            _locks.pop(upload_id, None)
    return Response(status_code=204, headers={**TUS, "Upload-Offset": str(offset), "X-Stream-Id": stream_id})


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


def _piece_hashes(path, end, piece):
    import hashlib

    out = []
    with open(path, "rb") as f:
        for start in range(0, end, piece):
            f.seek(start)
            out.append(hashlib.sha256(f.read(min(piece, end - start))).hexdigest())
    return out


@router.get("/{upload_id}/hashes")
async def piece_hashes(upload_id: str, request: Request, user=Depends(current_user), db=Depends(get_db)):
    """SHA-256 of each 8 MB piece the laptop has so far, for the browser to find pieces OBS changed when the
    recording stopped. Reading a long recording takes a little while, so it runs off the event loop."""
    upload = own_upload(db, user, upload_id)
    if not upload.growing or upload.completed_at is not None:
        raise HTTPException(409, "Only an unfinished upload of a growing recording is compared.")
    stream = db.get(Stream, upload.stream_id)
    path, end = source_path(request.app.state.settings, stream, upload), upload.offset
    db.commit()
    hashes = await run_in_threadpool(_piece_hashes, path, end, HASH_PIECE)
    return {"piece": HASH_PIECE, "offset": end, "hashes": hashes}


@router.put("/{upload_id}/rewrite", status_code=204)
async def rewrite_piece(upload_id: str, at: int, request: Request, user=Depends(current_user), db=Depends(get_db)):
    """Replace bytes the laptop already has with what the finished recording holds there (a piece OBS rewrote
    when recording stopped). Only inside what was already received; the end still grows by PATCH."""
    settings = request.app.state.settings
    body = await request.body()
    lock = _locks.setdefault(upload_id, asyncio.Lock())
    async with lock:
        upload = own_upload(db, user, upload_id)
        if not upload.growing or upload.completed_at is not None:
            raise HTTPException(409, "Only an unfinished upload of a growing recording can be corrected.")
        if at < 0 or not body or len(body) > settings.max_chunk_bytes or at + len(body) > upload.offset:
            raise HTTPException(416, "That piece isn't inside what was uploaded.")
        stream = db.get(Stream, upload.stream_id)
        path = source_path(settings, stream, upload)
        upload.updated_at = utcnow()
        db.commit()

        def write():
            with open(path, "r+b") as f:
                f.seek(at)
                f.write(body)

        await run_in_threadpool(write)
    return Response(status_code=204)
