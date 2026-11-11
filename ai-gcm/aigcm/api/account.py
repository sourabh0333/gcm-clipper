"""A creator's account (M4.8): accepting the privacy policy and terms before using Kaatclip, and deleting the
account with everything in it (YouTube Developer Policies III.A.2 and III.E.4: deletion on request within 7 days;
Kaatclip does it at once)."""

import shutil

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import select

from .. import youtube as yt
from ..db.models import AuditEntry, Stream, User, YouTubeChannel, utcnow
from ..studio import brand, lane
from .deps import SESSION_COOKIE, current_user, get_db
from .legal import TERMS_VERSION
from .uploads import remove_stream_files

router = APIRouter()


class Accept(BaseModel):
    version: str


@router.post("/api/me/accept")
def accept(body: Accept, user=Depends(current_user), db=Depends(get_db)):
    """The creator read and accepted this version of the privacy policy and terms."""
    if body.version != TERMS_VERSION:
        raise HTTPException(409, "The privacy policy has changed. Reload the page and read the new version.")
    user.terms_version, user.terms_accepted_at = TERMS_VERSION, utcnow()
    db.add(AuditEntry(user_id=user.id, action="terms_accepted", detail={"version": TERMS_VERSION}))
    db.commit()
    return {"accepted": True, "version": TERMS_VERSION}


class Delete(BaseModel):
    email: str     # typed by the creator, so an account is never deleted by a slip


@router.delete("/api/me")
def delete_account(body: Delete, request: Request, user=Depends(current_user), db=Depends(get_db)):
    """Delete the account: YouTube access revoked at Google, then every recording, clip, export, post record, brand
    kit, compilation, connection and session removed. Videos already on YouTube stay there."""
    settings, http = request.app.state.settings, request.app.state.http
    if body.email.strip().lower() != user.email.lower():
        raise HTTPException(422, "Type your email address exactly to delete your account.")
    streams = db.scalars(select(Stream).where(Stream.user_id == user.id)).all()
    if any(s.status == "running" for s in streams):
        raise HTTPException(409, "A stream is being processed. Stop it first, then delete your account.")
    revoked = 0
    for channel in db.scalars(select(YouTubeChannel).where(YouTubeChannel.user_id == user.id)).all():
        try:
            revoked += yt.revoke(http, yt.unseal(settings.token_key, channel.refresh_token))
        except yt.YouTubeError:
            pass
    for stream in streams:
        remove_stream_files(settings, stream)
    jobs = settings.jobs_dir.resolve()
    for folder in (brand.folder(settings.jobs_dir, user.id), lane.compilation_folder(settings.jobs_dir, user.id, "x").parent):
        folder = folder.resolve()
        if folder.is_dir() and jobs in folder.parents:
            shutil.rmtree(folder, ignore_errors=True)
    db.add(AuditEntry(user_id=None, action="account_deleted", detail={"streams": len(streams), "revoked": revoked}))
    db.delete(db.get(User, user.id))
    db.commit()
    response = JSONResponse({"ok": True})
    response.delete_cookie(SESSION_COOKIE, path="/")
    return response
