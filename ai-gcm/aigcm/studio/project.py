"""A clip as a studio project: its files, its default edit, its saved versions and its render queue.
Used by the API (light: no heavy imports) and by the worker's render lane."""

from pathlib import Path

from sqlalchemy import DateTime, bindparam, select, text

from ..db.models import Edit, Render, utcnow
from ..jobs import read_json
from . import window as win
from .edit import EditData, default_edit

KEEP_VERSIONS = 20
POSTER_W = 270          # library posters: 270x480 JPEGs of about 15 KB, two to a row on a phone
STUDIO_FILES = {"preview.mp4": "video/mp4", "strip.jpg": "image/jpeg", "wave.json": "application/json"}


def job_folder(settings, clip):
    return Path(settings.jobs_dir) / clip.stream.job_dir


def clip_folder(settings, clip):
    return win.studio_dir(job_folder(settings, clip), clip.clip_key)


def poster_path(settings, clip):
    return job_folder(settings, clip) / "posters" / f"{Path(clip.clip_key).name}.jpg"


def poster_time(clip):
    """Seconds into the engine's clip for its poster: the clip's key moment, else 40% in."""
    length = max(0.1, clip.end_s - clip.start_s)
    anchor = (clip.details or {}).get("anchor")
    at = anchor - clip.start_s if isinstance(anchor, (int, float)) else length * 0.4
    return min(max(at, 0.0), max(0.0, length - 0.1))


def source_file(folder):
    found = sorted(Path(folder).glob("source.*"))
    return found[0] if found else None


def engine_clip(folder, clip_key):
    """The clip as the engine wrote it in ranked.json (events, title, ...), or {}."""
    return next((c for c in read_json(Path(folder) / "ranked.json", []) if c.get("id") == clip_key), {})


def has_captions(folder, clip_key):
    chunks = read_json(Path(folder) / "captions" / f"{clip_key}.json", {}) or {}
    return bool(chunks.get("chunks")) and (Path(folder) / "transcript.json").exists()


def stream_facecam(settings, clip):
    """The stream's camera box (frame fractions) if it has been worked out and one was found."""
    from . import facecam

    return ((facecam.for_stream(job_folder(settings, clip)) or {}).get("box")) or None


def default_for(settings, clip, window=None):
    folder = job_folder(settings, clip)
    info = window or read_json(folder / "info.json", {}) or {}
    width, height = info.get("width") or 1920, info.get("height") or 1080
    span = (window["start"], window["end"]) if window else None
    return default_edit(clip.start_s, clip.end_s, width, height, clip.title,
                        engine_clip(folder, clip.clip_key).get("events") or (),
                        captions=has_captions(folder, clip.clip_key), window=span,
                        facecam=stream_facecam(settings, clip))


MARKER_KINDS = ("self_kill", "knock", "accolade", "chicken_dinner")


def editor_extras(settings, clip, details):
    """What the editor shows besides the edit: the kills and other events inside the saved footage (for
    the timeline) and the two length presets."""
    folder = job_folder(settings, clip)
    events = (read_json(folder / "vision.json", {}) or {}).get("events") or []
    lo, hi = details["start"], details["end"]
    shown = [{"t": e["t"], "kind": e["kind"]} for e in events
             if e.get("kind") in MARKER_KINDS and lo <= e.get("t", -1) <= hi]
    anchor = (clip.details or {}).get("anchor")
    from . import facecam

    cam = facecam.for_stream(folder) or {}
    return {"events": shown, "anchor": anchor, "facecam": cam.get("box"), "facecam_source": cam.get("source"),
            "presets": win.length_presets(clip.start_s, clip.end_s, anchor, events, lo, hi)}


def latest_edit(db, clip):
    return db.scalars(select(Edit).where(Edit.clip_id == clip.id).order_by(Edit.version.desc()).limit(1)).first()


def current_edit(db, settings, clip, window=None):
    """(version, EditData): the newest saved version, or version 0 with the default edit."""
    saved = latest_edit(db, clip)
    if saved:
        return saved.version, EditData.model_validate(saved.data)
    return 0, default_for(settings, clip, window)


def save_edit(db, clip, data):
    """Store `data` (a validated EditData) as the clip's next version; older versions beyond the last
    KEEP_VERSIONS are dropped."""
    saved = latest_edit(db, clip)
    version = (saved.version if saved else 0) + 1
    db.add(Edit(clip_id=clip.id, version=version, data=data.model_dump(mode="json")))
    db.flush()
    old = db.scalars(select(Edit).where(Edit.clip_id == clip.id, Edit.version <= version - KEEP_VERSIONS)).all()
    for row in old:
        db.delete(row)
    return version


# --- the render queue -----------------------------------------------------------------------------------

def active_render(db, clip, kind):
    return db.scalars(select(Render).where(Render.clip_id == clip.id, Render.kind == kind,
                                           Render.status.in_(("queued", "running")))
                      .order_by(Render.created_at.desc()).limit(1)).first()


def last_render(db, clip, kind):
    return db.scalars(select(Render).where(Render.clip_id == clip.id, Render.kind == kind)
                      .order_by(Render.created_at.desc()).limit(1)).first()


def window_state(db, settings, clip):
    """(status, details): ready, preparing, failed, none (can be prepared) or missing (no source left)."""
    folder = clip_folder(settings, clip)
    details = win.ready(folder)
    if details:
        return "ready", details
    if active_render(db, clip, "prepare"):
        return "preparing", None
    if source_file(job_folder(settings, clip)) is None:
        return "missing", None
    last = last_render(db, clip, "prepare")
    if last and last.status == "failed":
        return "failed", {"error": last.error}
    return "none", None


def queue_prepare(db, settings, clip):
    """Queue saving the clip's working window, unless it is ready, queued, or impossible. Returns the
    render (new or already queued) or None."""
    status, _ = window_state(db, settings, clip)
    if status == "preparing":
        return active_render(db, clip, "prepare")
    if status not in ("none", "failed"):
        return None
    render = Render(user_id=clip.stream.user_id, clip_id=clip.id, kind="prepare")
    db.add(render)
    return render


def queue_posters(db, stream):
    """Queue posters for a stream's clips (the worker skips clips that already have one)."""
    for render in db.scalars(select(Render).where(Render.kind == "posters",
                                                  Render.status.in_(("queued", "running")))).all():
        if (render.params or {}).get("stream_id") == stream.id:
            return render
    render = Render(user_id=stream.user_id, kind="posters", params={"stream_id": stream.id})
    db.add(render)
    return render


def claim_render(session):
    """Atomically take the oldest queued render (the same pattern as the stream queue)."""
    claim = text(
        "UPDATE renders SET status='running', started_at=:now, error=NULL "
        "WHERE id=(SELECT id FROM renders WHERE status='queued' ORDER BY created_at LIMIT 1) "
        "AND status='queued' RETURNING id").bindparams(bindparam("now", type_=DateTime))
    row = session.execute(claim, {"now": utcnow()}).first()
    session.commit()
    return row[0] if row else None


def requeue_renders(session):
    stuck = session.scalars(select(Render).where(Render.status == "running")).all()
    for render in stuck:
        render.status = "queued"
    session.commit()
    return [r.id for r in stuck]
