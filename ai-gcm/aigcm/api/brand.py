"""The brand kit (M3.6): read and save it, upload a logo, intro or outro, and preview the lower-third strip.
Uploads are small (a logo up to 3 MB, an intro or outro up to 60 MB) and are re-encoded before use."""

from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse
from pydantic import ValidationError

from ..db.models import AuditEntry, BrandKitRow, utcnow
from ..studio import brand
from .deps import current_user, get_db

router = APIRouter()

MEDIA = {"logo": "image/png", "intro": "video/mp4", "outro": "video/mp4"}


def load_kit(db, user_id):
    row = db.get(BrandKitRow, user_id)
    try:
        return brand.BrandKit.model_validate(row.data) if row else brand.BrandKit()
    except ValidationError:
        return brand.BrandKit()


def kit_view(settings, user_id, kit):
    found = brand.files(settings.jobs_dir, user_id)
    return {"kit": kit.model_dump(mode="json"),
            "files": {kind: (f"/media/brand/{kind}" if found[kind] else None) for kind in MEDIA},
            "lengths": {"intro": found["intro_s"], "outro": found["outro_s"]},
            "music": {"intro": found["intro_music"], "outro": found["outro_music"]},
            "strip": "/media/brand/strip" if (kit.strip_text() or found["logo"]) else None}


@router.get("/api/brand")
def get_kit(request: Request, user=Depends(current_user), db=Depends(get_db)):
    return kit_view(request.app.state.settings, user.id, load_kit(db, user.id))


@router.put("/api/brand")
def save_kit(body: dict, request: Request, user=Depends(current_user), db=Depends(get_db)):
    try:
        kit = brand.BrandKit.model_validate(body)
    except ValidationError as exc:
        raise HTTPException(422, "; ".join(str(e.get("msg", "")).removeprefix("Value error, ") for e in exc.errors()[:3]))
    row = db.get(BrandKitRow, user.id) or BrandKitRow(user_id=user.id)
    row.data, row.updated_at = kit.model_dump(mode="json"), utcnow()
    db.add(row)
    db.add(AuditEntry(user_id=user.id, action="brand_kit", detail={}))
    db.commit()
    return kit_view(request.app.state.settings, user.id, kit)


async def _read(upload, limit):
    data = await upload.read(limit + 1)
    if len(data) > limit:
        raise HTTPException(413, "That file is too big.")
    return data


@router.post("/api/brand/{kind}")
async def upload(kind: Literal["logo", "intro", "outro"], file: UploadFile, request: Request,
                 user=Depends(current_user), db=Depends(get_db)):
    settings = request.app.state.settings
    user_id = user.id
    db.close()   # re-encoding takes a few seconds; no transaction may wait on it
    limit = brand.LOGO_BYTES if kind == "logo" else brand.CLIP_BYTES
    data = await _read(file, limit)
    import anyio

    try:
        if kind == "logo":
            await anyio.to_thread.run_sync(brand.save_logo, settings.jobs_dir, user_id, data)
        else:
            await anyio.to_thread.run_sync(brand.save_clip, settings.jobs_dir, user_id, kind, data)
    except ValueError as exc:
        raise HTTPException(422, str(exc))
    with request.app.state.sessions() as s:
        return kit_view(settings, user_id, load_kit(s, user_id))


@router.delete("/api/brand/{kind}")
def remove(kind: Literal["logo", "intro", "outro"], request: Request, user=Depends(current_user), db=Depends(get_db)):
    brand.remove(request.app.state.settings.jobs_dir, user.id, kind)
    return kit_view(request.app.state.settings, user.id, load_kit(db, user.id))


@router.get("/media/brand/{kind}")
def brand_file(kind: str, request: Request, user=Depends(current_user), db=Depends(get_db)):
    settings = request.app.state.settings
    if kind == "strip":
        kit = load_kit(db, user.id)
        db.close()
        path = brand.strip_for(settings.jobs_dir, user.id, kit)
        media = "image/png"
    elif kind in MEDIA:
        db.close()
        path, media = brand.files(settings.jobs_dir, user.id)[kind], MEDIA[kind]
    else:
        raise HTTPException(404, "Not found.")
    if not path or not path.is_file():
        raise HTTPException(404, "Not set.")
    return FileResponse(path, media_type=media, headers={"Cache-Control": "private, no-cache"})
