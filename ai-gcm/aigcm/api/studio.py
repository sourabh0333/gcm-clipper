"""Studio (M3): a clip's editing project. Reading the edit and the state of its working window, saving
versions, asking for the window to be prepared and for exports, and serving the preview copy, filmstrip,
sound wave and exported videos to the clip's owner only. The work itself runs in the worker's render
lane; this API only queues it. See plans/M3 Studio plan.md."""

import re
from pathlib import Path
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel, ValidationError
from sqlalchemy import select

from ..db.models import AuditEntry, Render
from ..jobs import read_json
from ..studio import lane, project
from ..studio.edit import EditData, check_window, output_length
from .clips import clip_view, own_clip
from .deps import current_user, get_db, own_stream

router = APIRouter()


def render_view(render):
    done = render.status == "done" and render.kind == "export"
    return {"id": render.id, "kind": render.kind, "status": render.status, "error": render.error,
            "version": (render.params or {}).get("version"), "sponsor_safe": bool((render.params or {}).get("sponsor_safe")),
            "created_at": render.created_at.isoformat() + "Z" if render.created_at else None,
            "finished_at": render.finished_at.isoformat() + "Z" if render.finished_at else None,
            "video": f"/media/renders/{render.id}" if done else None,
            "cover": f"/media/renders/{render.id}/cover" if done else None}


def window_view(status, details, clip_id):
    view = {"status": status}
    if status == "ready":
        base = f"/media/studio/{clip_id}"
        view.update({k: details[k] for k in ("start", "end", "duration", "width", "height", "has_audio")},
                    strip=dict(details["strip"], url=f"{base}/strip.jpg"),
                    preview=f"{base}/preview.mp4", wave=f"{base}/wave.json")
    elif status == "failed":
        view["error"] = (details or {}).get("error")
    return view


@router.get("/api/clips/{clip_id}/studio")
def studio(clip_id: int, request: Request, user=Depends(current_user), db=Depends(get_db)):
    settings = request.app.state.settings
    clip = own_clip(db, user, clip_id)
    status, details = project.window_state(db, settings, clip)
    version, edit = project.current_edit(db, settings, clip, details if status == "ready" else None)
    exports = db.scalars(select(Render).where(Render.clip_id == clip.id, Render.kind == "export")
                         .order_by(Render.created_at.desc()).limit(10)).all()
    return {"clip": clip_view(clip), "window": window_view(status, details, clip.id),
            "edit": {"version": version, "data": edit.model_dump(mode="json"),
                     "length_s": round(output_length(edit.segments), 2)},
            "editor": project.editor_extras(settings, clip, details) if status == "ready" else None,
            "exports": [render_view(r) for r in exports]}


@router.post("/api/clips/{clip_id}/prepare")
def prepare(clip_id: int, request: Request, user=Depends(current_user), db=Depends(get_db)):
    """Ask the worker to save this clip's footage for editing (done automatically when a clip is kept)."""
    settings = request.app.state.settings
    clip = own_clip(db, user, clip_id)
    status, details = project.window_state(db, settings, clip)
    if status == "missing":
        raise HTTPException(409, "The recording is no longer on the laptop, so this clip can't be edited.")
    if status != "ready":
        project.queue_prepare(db, settings, clip)
        db.commit()
        status, details = project.window_state(db, settings, clip)
    return window_view(status, details, clip.id)


class EditBody(BaseModel):
    base_version: int
    data: dict


@router.put("/api/clips/{clip_id}/edit")
def save(clip_id: int, body: EditBody, request: Request, user=Depends(current_user), db=Depends(get_db)):
    settings = request.app.state.settings
    clip = own_clip(db, user, clip_id)
    status, details = project.window_state(db, settings, clip)
    if status != "ready":
        raise HTTPException(409, "This clip's footage isn't ready for editing yet.")
    try:
        edit = EditData.model_validate(body.data)
        check_window(edit, details["start"], details["end"])
    except (ValidationError, ValueError) as exc:
        errors = exc.errors() if isinstance(exc, ValidationError) else [{"msg": str(exc)}]
        raise HTTPException(422, "; ".join(str(e.get("msg", "")).removeprefix("Value error, ") for e in errors[:3]))
    latest = project.latest_edit(db, clip)
    if (latest.version if latest else 0) != body.base_version:
        raise HTTPException(409, "This clip was changed somewhere else. Reload it to see the newest version.")
    version = project.save_edit(db, clip, edit)
    db.commit()
    cam = next((p for p in edit.layout.panels if p.role == "cam"), None)
    if cam is not None and list(cam.src) != (project.stream_facecam(settings, clip) or []):
        from ..studio import facecam

        facecam.set_manual(project.job_folder(settings, clip), cam.src)
    return {"version": version, "data": edit.model_dump(mode="json"), "length_s": round(output_length(edit.segments), 2)}


class ExportBody(BaseModel):
    version: int | None = None     # default: the newest saved version (0 = the default edit)
    sponsor_safe: bool = False


@router.post("/api/clips/{clip_id}/export")
def export(clip_id: int, body: ExportBody, request: Request, user=Depends(current_user), db=Depends(get_db)):
    settings = request.app.state.settings
    clip = own_clip(db, user, clip_id)
    status, _ = project.window_state(db, settings, clip)
    if status != "ready":
        raise HTTPException(409, "This clip's footage isn't ready for editing yet.")
    latest = project.latest_edit(db, clip)
    version = (latest.version if latest else 0) if body.version is None else body.version
    if version and not any(e.version == version for e in clip.edits):
        raise HTTPException(404, "That version of the edit doesn't exist.")
    # The same version can look different later: the automatic edit (version 0) follows the brand kit and
    # the stream's camera box, and any version shows the kit's current strip, intro and outro. So an
    # earlier export is reused only when all of that is unchanged too.
    params = {"version": version, "sponsor_safe": body.sponsor_safe, "look": look(settings, db, clip, version)}
    for earlier in db.scalars(select(Render).where(Render.clip_id == clip.id, Render.kind == "export",
                                                   Render.status.in_(("queued", "running", "done")))).all():
        if earlier.params == params and (earlier.status != "done" or lane.export_path(settings, clip, earlier)):
            return render_view(earlier)   # the same export is already made or on its way
    render = Render(user_id=user.id, clip_id=clip.id, kind="export", params=params)
    db.add(render)
    db.add(AuditEntry(user_id=user.id, action="export", detail={"clip": clip.id, "version": version}))
    db.commit()
    return render_view(render)


def look(settings, db, clip, version):
    """A short fingerprint of everything an export of this version depends on besides its frames."""
    import hashlib
    import json

    from ..studio import brand

    if version:
        data = next(e.data for e in clip.edits if e.version == version)
    else:
        _, details = project.window_state(db, settings, clip)
        data = project.default_for(settings, clip, details).model_dump(mode="json")
    found = brand.files(settings.jobs_dir, clip.stream.user_id)
    kit = project.kit_for(clip)
    stamps = [brand.strip_name(kit, found["logo"])] + [
        str(found[k].stat().st_mtime_ns) if found[k] else "" for k in ("intro", "outro")]
    blob = json.dumps(data, sort_keys=True, ensure_ascii=False) + "|" + "|".join(stamps)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]


def own_render(db, user, render_id):
    render = db.get(Render, render_id)
    if render is None or render.user_id != user.id:
        raise HTTPException(404, "Not found.")
    return render


@router.get("/api/renders/{render_id}")
def render_status(render_id: str, user=Depends(current_user), db=Depends(get_db)):
    return render_view(own_render(db, user, render_id))


@router.get("/media/renders/{render_id}")
def render_video(render_id: str, request: Request, download: int = 0, user=Depends(current_user),
                 db=Depends(get_db)):
    render = own_render(db, user, render_id)
    clip = own_clip(db, user, render.clip_id) if render.clip_id else None
    path = lane.export_path(request.app.state.settings, clip, render) if clip else None
    db.close()  # the video may stream for minutes; no transaction may stay open that long
    if path is None:
        raise HTTPException(404, "This video is no longer on the laptop.")
    return FileResponse(path, media_type="video/mp4", filename=f"kaatclip_{path.name}" if download else None,
                        content_disposition_type="attachment" if download else "inline",
                        headers={"Cache-Control": "private, max-age=3600"})


@router.get("/media/renders/{render_id}/cover")
def render_cover(render_id: str, request: Request, download: int = 0, user=Depends(current_user), db=Depends(get_db)):
    """The Short's cover frame (a JPEG of the export at its cover time)."""
    render = own_render(db, user, render_id)
    clip = own_clip(db, user, render.clip_id) if render.clip_id else None
    path = lane.export_path(request.app.state.settings, clip, render) if clip else None
    db.close()
    cover = lane.cover_path(path) if path else None
    if cover is None or not cover.is_file():
        raise HTTPException(404, "No cover for this export.")
    return FileResponse(cover, media_type="image/jpeg", filename=f"kaatclip_{cover.name}" if download else None,
                        content_disposition_type="attachment" if download else "inline",
                        headers={"Cache-Control": "private, max-age=3600"})


def thumbs_view(render, settings, stream):
    view = {"id": render.id, "status": render.status, "error": render.error, "images": [], "titles": []}
    if render.status == "done":
        folder = Path(settings.jobs_dir) / stream.job_dir / "thumbs" / render.id
        view["images"] = [f"/media/thumbs/{render.id}/{n}" for n in (1, 2, 3) if (folder / f"thumb_{n}.jpg").exists()]
        view["titles"] = (read_json(folder / "titles.json", {}) or {}).get("titles", [])
    return view


def stream_thumbs(db, stream):
    renders = db.scalars(select(Render).where(Render.kind == "thumbs", Render.user_id == stream.user_id)
                         .order_by(Render.created_at.desc())).all()
    return [r for r in renders if (r.params or {}).get("stream_id") == stream.id]


@router.get("/api/streams/{stream_id}/thumbnails")
def get_thumbnails(stream_id: str, request: Request, user=Depends(current_user), db=Depends(get_db)):
    """Three thumbnails and three titles for a long video of this stream (highlights, or the compilation)."""
    stream = own_stream(db, user, stream_id)
    made = stream_thumbs(db, stream)
    return thumbs_view(made[0], request.app.state.settings, stream) if made else {"status": "none"}


@router.post("/api/streams/{stream_id}/thumbnails")
def make_thumbnails(stream_id: str, request: Request, user=Depends(current_user), db=Depends(get_db)):
    stream = own_stream(db, user, stream_id)
    if stream.status != "done":
        raise HTTPException(409, "Thumbnails come once the stream's clips are ready.")
    active = next((r for r in stream_thumbs(db, stream) if r.status in ("queued", "running")), None)
    render = active or Render(user_id=user.id, kind="thumbs", params={"stream_id": stream.id})
    if not active:
        db.add(render)
        db.commit()
    return thumbs_view(render, request.app.state.settings, stream)


@router.get("/media/thumbs/{render_id}/{n}")
def thumb_image(render_id: str, n: int, request: Request, download: int = 0, user=Depends(current_user),
                db=Depends(get_db)):
    render = own_render(db, user, render_id)
    if render.kind != "thumbs" or n not in (1, 2, 3):
        raise HTTPException(404, "Not found.")
    stream = own_stream(db, user, (render.params or {}).get("stream_id", ""))
    path = Path(request.app.state.settings.jobs_dir) / stream.job_dir / "thumbs" / render.id / f"thumb_{n}.jpg"
    db.close()
    if not path.is_file():
        raise HTTPException(404, "Not found.")
    return FileResponse(path, media_type="image/jpeg", filename=f"thumbnail_{n}.jpg" if download else None,
                        content_disposition_type="attachment" if download else "inline",
                        headers={"Cache-Control": "private, max-age=86400"})


class HookBody(BaseModel):
    text: str
    color: Literal["yellow", "white"] = "yellow"
    box_h: int = 420
    backing: bool = False   # outside the black band the hook sits on a dark box


@router.post("/api/clips/{clip_id}/hook")
def draw_hook(clip_id: int, body: HookBody, request: Request, user=Depends(current_user), db=Depends(get_db)):
    """Draw the hook for the editor's preview (the export uses the very same image). About 0.3-0.6 s the
    first time; cached after that."""
    from ..studio import hook

    if len(body.text) > 80 or not 120 <= body.box_h <= 900:
        raise HTTPException(422, "The hook can be at most 80 characters.")
    folder = project.clip_folder(request.app.state.settings, own_clip(db, user, clip_id)) / "hooks"
    db.close()   # drawing takes a moment; no transaction may wait on it
    path = hook.cached(folder, body.text, body.color, body.box_h, body.backing)
    return {"url": f"/media/studio/{clip_id}/hooks/{path.name}" if path else None}


HOOK_NAME = re.compile(r"^[0-9a-f]{20}\.png$")


@router.get("/media/studio/{clip_id}/hooks/{name}")
def hook_image(clip_id: int, name: str, request: Request, user=Depends(current_user), db=Depends(get_db)):
    if not HOOK_NAME.match(name):
        raise HTTPException(404, "Not found.")
    path = project.clip_folder(request.app.state.settings, own_clip(db, user, clip_id)) / "hooks" / name
    db.close()
    if not path.is_file():
        raise HTTPException(404, "Not found.")
    return FileResponse(path, media_type="image/png", headers={"Cache-Control": "private, max-age=86400"})


class ConvertBody(BaseModel):
    script: Literal["latin", "devanagari"]
    words: list[dict]   # [{"t": start, "w": word}] as the editor shows them


@router.post("/api/clips/{clip_id}/captions/convert")
def convert_script(clip_id: int, body: ConvertBody, user=Depends(current_user), db=Depends(get_db)):
    """Caption words in the other script, each keeping its start time; the editor applies them as word
    fixes (nothing is saved here)."""
    from ..studio import script

    own_clip(db, user, clip_id)
    db.close()
    try:
        times = [round(float(w["t"]), 2) for w in body.words]
        converted = script.convert([str(w.get("w", ""))[:40] for w in body.words], body.script)
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(422, str(exc))
    except script.Unavailable as exc:
        raise HTTPException(503, str(exc))
    return {"script": body.script, "words": [{"t": t, "w": w} for t, w in zip(times, converted)]}


@router.get("/api/clips/{clip_id}/post-text")
def post_text(clip_id: int, user=Depends(current_user), db=Depends(get_db)):
    """Title, description and hashtags to post with: the engine's (stream link, game line) and the brand kit's
    (standard description, hashtags, own game line)."""
    from ..studio import brand

    clip = own_clip(db, user, clip_id)
    saved = project.latest_edit(db, clip)
    title = (saved.data.get("hook") or {}).get("text") if saved else None
    details = clip.details or {}
    return brand.post_text(title or clip.title, details.get("description"), details.get("hashtags"),
                           project.kit_for(clip))


FONT_FILES = {"Anton-Regular.ttf", "Mukta-ExtraBold.ttf"}


@router.get("/fonts/{name}")
def font(name: str):
    """The bundled fonts, for the editor's preview of captions (open fonts; no sign-in needed)."""
    from ..studio.render import FONTS

    if name not in FONT_FILES:
        raise HTTPException(404, "Not found.")
    return FileResponse(FONTS / name, media_type="font/ttf", headers={"Cache-Control": "public, max-age=604800"})


@router.get("/media/studio/{clip_id}/{name}")
def studio_file(clip_id: int, name: str, request: Request, user=Depends(current_user), db=Depends(get_db)):
    if name not in project.STUDIO_FILES:
        raise HTTPException(404, "Not found.")
    clip = own_clip(db, user, clip_id)
    folder = project.clip_folder(request.app.state.settings, clip)
    path = folder / name
    db.close()
    if not path.is_file():
        raise HTTPException(404, "Not ready yet.")
    return FileResponse(path, media_type=project.STUDIO_FILES[name], headers={"Cache-Control": "private, max-age=600"})
