"""Connect YouTube (M4.1): a separate Google consent after sign-in for the three narrow scopes, the channel the
creator picked, disconnect with revoke, and the channel list for the app. See plans/M4 Plan and post plan.md.

The consent goes through the sign-in's registered callback (`/auth/google/callback`) with `purpose: youtube` in
the pending-login cookie, so no new redirect address has to be added in Google Cloud."""

import base64
import hashlib
import json
import secrets
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy import select

from .. import youtube as yt
from ..db.models import AuditEntry, YouTubeChannel, utcnow
from .auth import AUTH_URL, LOGIN_COOKIE, LOGIN_TTL_S, redirect_uri
from .deps import current_user, get_db, optional_user

router = APIRouter()
BACK = "/settings"


def ready(settings):
    return bool(settings.google_client_id and settings.google_client_secret and settings.token_key)


def view(row):
    return {"id": row.id, "channel_id": row.channel_id, "title": row.title, "thumbnail": row.thumbnail,
            "status": row.status, "connected_at": row.connected_at.isoformat() + "Z",
            "settings": {"made_for_kids": False, "synthetic": False, **(row.settings or {})}}


@router.get("/auth/youtube/start")
def youtube_start(request: Request, user=Depends(current_user)):
    settings = request.app.state.settings
    if not ready(settings):
        raise HTTPException(503, "YouTube isn't set up on the laptop yet.")
    state, verifier = secrets.token_urlsafe(32), secrets.token_urlsafe(48)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    query = urlencode({"client_id": settings.google_client_id, "redirect_uri": redirect_uri(settings),
                       "response_type": "code", "scope": " ".join(yt.SCOPES), "state": state,
                       "code_challenge": challenge, "code_challenge_method": "S256",
                       "access_type": "offline", "prompt": "consent", "include_granted_scopes": "true",
                       "login_hint": user.email})
    response = RedirectResponse(f"{AUTH_URL}?{query}", status_code=302)
    pending = base64.urlsafe_b64encode(json.dumps(
        {"state": state, "verifier": verifier, "purpose": "youtube", "user": user.id}).encode()).decode()
    response.set_cookie(LOGIN_COOKIE, pending, max_age=LOGIN_TTL_S, httponly=True, samesite="lax",
                        secure=request.url.scheme == "https", path="/auth/")
    return response


def _back(result):
    response = RedirectResponse(f"{BACK}?youtube={result}", status_code=302)
    response.delete_cookie(LOGIN_COOKIE, path="/auth/")
    return response


def finish_connect(request, db, pending, code):
    """The second half of the consent, called by the sign-in callback once state has been checked. Every
    outcome goes back to Settings with a short result code the page turns into words."""
    settings = request.app.state.settings
    user = optional_user(request, db)
    if user is None or user.id != pending.get("user"):
        return _back("signed-out")
    if not ready(settings):
        return _back("not-ready")
    http = request.app.state.http
    try:
        tokens = yt.exchange(http, settings, code, pending["verifier"], redirect_uri(settings))
    except yt.YouTubeError:
        return _back("refused")
    if yt.missing_scopes(tokens.get("scope")):
        # The creator unticked a box on Google's screen. Give the grant back rather than keep half of it.
        yt.revoke(http, tokens.get("refresh_token") or tokens.get("access_token", ""))
        return _back("scopes")
    if not tokens.get("refresh_token"):
        return _back("refused")
    try:
        channel = yt.my_channel(http, tokens["access_token"])
    except yt.YouTubeError:
        yt.revoke(http, tokens["refresh_token"])
        return _back("no-channel")
    row = db.scalar(select(YouTubeChannel).where(YouTubeChannel.user_id == user.id,
                                                 YouTubeChannel.channel_id == channel["id"]))
    if row is None:
        row = YouTubeChannel(user_id=user.id, channel_id=channel["id"], settings={})
        db.add(row)
    row.title, row.thumbnail, row.scopes = channel["title"][:200], channel["thumbnail"], tokens.get("scope", "")
    row.refresh_token = yt.seal(settings.token_key, tokens["refresh_token"])
    row.status, row.connected_at, row.checked_at = "ok", utcnow(), utcnow()
    db.add(AuditEntry(user_id=user.id, action="youtube_connect",
                      detail={"channel": channel["id"], "title": channel["title"][:200]}))
    db.commit()
    return _back("connected")


def own_channel(db, user, channel_id):
    row = db.get(YouTubeChannel, channel_id)
    if row is None or row.user_id != user.id:
        raise HTTPException(404, "Not found.")
    return row


@router.get("/api/youtube")
def channels(request: Request, user=Depends(current_user), db=Depends(get_db)):
    rows = db.scalars(select(YouTubeChannel).where(YouTubeChannel.user_id == user.id)
                      .order_by(YouTubeChannel.connected_at)).all()
    return {"available": ready(request.app.state.settings), "channels": [view(r) for r in rows]}


class ChannelSettings(BaseModel):
    made_for_kids: bool = False
    synthetic: bool = False


@router.put("/api/youtube/{channel_id}/settings")
def channel_settings(channel_id: str, body: ChannelSettings, user=Depends(current_user), db=Depends(get_db)):
    """The creator's own answers YouTube asks on every upload: made for kids, and altered or synthetic content."""
    row = own_channel(db, user, channel_id)
    row.settings = body.model_dump()
    db.commit()
    return view(row)


@router.post("/api/youtube/{channel_id}/check")
def check(channel_id: str, request: Request, user=Depends(current_user), db=Depends(get_db)):
    """Is the connection still alive? Marks it expired when Google says no (testing-mode tokens last 7 days)."""
    settings = request.app.state.settings
    row = own_channel(db, user, channel_id)
    try:
        token = yt.access_token(request.app.state.http, settings, yt.unseal(settings.token_key, row.refresh_token))
        channel = yt.my_channel(request.app.state.http, token)
        row.status, row.title, row.thumbnail = "ok", channel["title"][:200], channel["thumbnail"]
    except yt.Expired:
        row.status = "expired"
    except yt.YouTubeError as exc:
        raise HTTPException(502, str(exc)) from exc
    row.checked_at = utcnow()
    db.commit()
    return view(row)


@router.delete("/api/youtube/{channel_id}")
def disconnect(channel_id: str, request: Request, user=Depends(current_user), db=Depends(get_db)):
    """Revoke at Google and delete the token and everything kept about the channel, at once (Developer
    Policies III.D.2.3)."""
    settings = request.app.state.settings
    row = own_channel(db, user, channel_id)
    revoked = False
    try:
        revoked = yt.revoke(request.app.state.http, yt.unseal(settings.token_key, row.refresh_token))
    except yt.YouTubeError:
        pass
    db.add(AuditEntry(user_id=user.id, action="youtube_disconnect",
                      detail={"channel": row.channel_id, "revoked": revoked}))
    db.delete(row)
    db.commit()
    return {"ok": True, "revoked": revoked}
