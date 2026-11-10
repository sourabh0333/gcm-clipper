"""Sign-in with Google only (plan D7, M2 review R1, R2, R9).

Authorization-code flow with PKCE, `state` and `nonce`. The pending login (state, PKCE verifier, nonce,
where to go after) lives in a short-lived HttpOnly cookie; Google's ID token is verified against Google's
certificates (cached for as long as Google says). Only `openid email profile` is asked for, so the app
needs no tester list and Google's 7-day expiry doesn't apply. Sign-in is by invitation during the beta.
"""

import base64
import hashlib
import json
import secrets
import time
from datetime import timedelta
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from google.auth import exceptions as google_exceptions
from google.auth import jwt as google_jwt
from pydantic import BaseModel
from sqlalchemy import select

from ..db.models import AuditEntry, Invite, User, utcnow
from ..db.models import Session as SessionRow
from .deps import SESSION_COOKIE, current_user, get_db, optional_user, token_hash

AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
CERTS_URL = "https://www.googleapis.com/oauth2/v1/certs"
ISSUERS = {"accounts.google.com", "https://accounts.google.com"}
LOGIN_COOKIE = "kc_login"
LOGIN_TTL_S = 600

router = APIRouter()


class GoogleCerts:
    """Google's signing certificates, re-fetched when the max-age Google sends runs out."""

    def __init__(self, fetch):
        self.fetch = fetch
        self.certs, self.until = None, 0.0

    def get(self):
        if self.certs is None or time.time() >= self.until:
            response = self.fetch(CERTS_URL)
            response.raise_for_status()
            max_age = 3600
            for part in response.headers.get("cache-control", "").split(","):
                if part.strip().startswith("max-age="):
                    max_age = int(part.strip()[8:])
            self.certs, self.until = response.json(), time.time() + max_age
        return self.certs


def redirect_uri(settings):
    return f"{settings.public_url}/auth/google/callback"


def safe_next(path):
    """Only paths on this site: '/streams/x' yes; '//evil.com', '/\\evil.com' (browsers read a backslash as
    a slash), control characters or 'https://evil.com' no."""
    ok = (isinstance(path, str) and path.startswith("/") and not path.startswith("//") and "\\" not in path
          and len(path) <= 300 and not any(ord(c) < 32 for c in path))
    return path if ok else "/"


def may_sign_in(db, settings, email):
    email = email.lower()
    return (email in settings.invites or email in settings.admins
            or db.get(Invite, email) is not None)


def start_session(request, response, db, user):
    token = secrets.token_urlsafe(32)
    days = request.app.state.settings.session_days
    db.add(SessionRow(id=token_hash(token), user_id=user.id, expires_at=utcnow() + timedelta(days=days),
                      user_agent=(request.headers.get("user-agent") or "")[:300]))
    user.last_seen_at = utcnow()
    db.add(AuditEntry(user_id=user.id, action="sign_in", detail={"via": "google" if user.google_sub else "dev"}))
    db.commit()
    # Secure when the request came over HTTPS (through the tunnel: uvicorn trusts its X-Forwarded-Proto).
    secure = request.url.scheme == "https"
    response.set_cookie(SESSION_COOKIE, token, max_age=days * 86400, httponly=True, secure=secure,
                        samesite="lax", path="/")


def find_or_create_user(db, settings, email, sub=None, name=None, picture=None):
    email = email.lower()
    user = db.scalar(select(User).where(User.google_sub == sub)) if sub else None
    user = user or db.scalar(select(User).where(User.email == email))
    if user is None:
        user = User(email=email)
        db.add(user)
    user.email, user.google_sub = email, sub or user.google_sub
    user.name, user.picture = name or user.name, picture or user.picture
    user.is_admin = email in settings.admins
    db.flush()
    return user


@router.get("/auth/google/start")
def google_start(request: Request, next: str = "/"):
    settings = request.app.state.settings
    if not settings.google_client_id:
        raise HTTPException(503, "Google sign-in is not set up yet (GOOGLE_CLIENT_ID is missing).")
    state, verifier, nonce = (secrets.token_urlsafe(32) for _ in range(3))
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    query = urlencode({"client_id": settings.google_client_id, "redirect_uri": redirect_uri(settings),
                       "response_type": "code", "scope": "openid email profile", "state": state,
                       "nonce": nonce, "code_challenge": challenge, "code_challenge_method": "S256",
                       "prompt": "select_account"})
    response = RedirectResponse(f"{AUTH_URL}?{query}", status_code=302)
    pending = base64.urlsafe_b64encode(json.dumps(
        {"state": state, "verifier": verifier, "nonce": nonce, "next": safe_next(next)}).encode()).decode()
    response.set_cookie(LOGIN_COOKIE, pending, max_age=LOGIN_TTL_S, httponly=True, samesite="lax",
                        secure=request.url.scheme == "https", path="/auth/")
    return response


def _fail(message, status=400):
    response = JSONResponse({"detail": message}, status_code=status)
    response.delete_cookie(LOGIN_COOKIE, path="/auth/")
    return response


@router.get("/auth/google/callback")
def google_callback(request: Request, code: str = "", state: str = "", error: str = "", db=Depends(get_db)):
    settings = request.app.state.settings
    try:
        pending = json.loads(base64.urlsafe_b64decode(request.cookies.get(LOGIN_COOKIE, "")))
    except (ValueError, TypeError):
        pending = None
    if error:
        if pending and pending.get("purpose") == "youtube":
            from .youtube import _back
            return _back("cancelled")
        return _fail(f"Google sign-in was cancelled ({error}).")
    if not pending or not code or not secrets.compare_digest(state, pending.get("state", "")):
        return _fail("This sign-in link has expired. Start again.")
    if pending.get("purpose") == "youtube":
        from .youtube import finish_connect
        return finish_connect(request, db, pending, code)
    http = request.app.state.http
    response = http.post(TOKEN_URL, data={
        "client_id": settings.google_client_id, "client_secret": settings.google_client_secret,
        "code": code, "code_verifier": pending["verifier"], "grant_type": "authorization_code",
        "redirect_uri": redirect_uri(settings)})
    if response.status_code != 200 or "id_token" not in response.json():
        return _fail("Google did not accept the sign-in. Try again.", 502)
    try:
        claims = google_jwt.decode(response.json()["id_token"], certs=request.app.state.google_certs.get(),
                                   audience=settings.google_client_id, clock_skew_in_seconds=10)
    except (ValueError, google_exceptions.GoogleAuthError):
        return _fail("Google's answer could not be verified.", 502)
    if claims.get("iss") not in ISSUERS or claims.get("nonce") != pending["nonce"]:
        return _fail("Google's answer could not be verified.", 502)
    if not claims.get("email") or not claims.get("email_verified"):
        return _fail("This Google account has no verified email address.", 403)
    if not may_sign_in(db, settings, claims["email"]):
        return _fail("Kaatclip is invite-only during the beta, and this Google account is not invited yet.", 403)
    user = find_or_create_user(db, settings, claims["email"], claims["sub"], claims.get("name"),
                               claims.get("picture"))
    redirect = RedirectResponse(pending["next"], status_code=302)
    redirect.delete_cookie(LOGIN_COOKIE, path="/auth/")
    start_session(request, redirect, db, user)
    return redirect


def dev_login_allowed(request):
    """Dev sign-in: only when switched on, only on this laptop's own address, and never through a tunnel or
    proxy (which add forwarding headers)."""
    forwarded = [h for h in request.headers if h.startswith(("x-forwarded-", "cf-", "tailscale-")) or h == "forwarded"]
    return (request.app.state.settings.dev_login and request.url.hostname in ("localhost", "127.0.0.1")
            and not forwarded)


class DevLogin(BaseModel):
    email: str
    name: str | None = None


@router.post("/auth/dev-login")
def dev_login(body: DevLogin, request: Request, db=Depends(get_db)):
    if not dev_login_allowed(request):
        raise HTTPException(404, "Not found.")
    settings = request.app.state.settings
    if not may_sign_in(db, settings, body.email):
        raise HTTPException(403, "Not invited.")
    user = find_or_create_user(db, settings, body.email, name=body.name)
    response = JSONResponse({"ok": True})
    start_session(request, response, db, user)
    return response


@router.post("/auth/logout")
def logout(request: Request, user=Depends(optional_user), db=Depends(get_db)):
    token = request.cookies.get(SESSION_COOKIE)
    if token:
        row = db.get(SessionRow, token_hash(token))
        if row is not None:
            db.delete(row)
        if user is not None:
            db.add(AuditEntry(user_id=user.id, action="sign_out", detail={}))
        db.commit()
    response = JSONResponse({"ok": True})
    response.delete_cookie(SESSION_COOKIE, path="/")
    return response


@router.get("/api/me")
def me(user=Depends(current_user)):
    return {"email": user.email, "name": user.name, "picture": user.picture, "admin": user.is_admin}


@router.get("/api/auth-config")
def auth_config(request: Request):
    """What the sign-in screen offers."""
    settings = request.app.state.settings
    return {"google": bool(settings.google_client_id), "dev": dev_login_allowed(request)}
