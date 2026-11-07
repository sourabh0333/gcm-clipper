"""Request plumbing shared by every route: the database session, the signed-in user, admin checks, the
cross-site request guard, and the one way to fetch a creator's own rows."""

import hashlib
from datetime import timedelta

from fastapi import Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError

from ..db.models import Session as SessionRow
from ..db.models import Stream, User, utcnow

SESSION_COOKIE = "kc_session"
# Every state-changing API call carries this header. A page on another site can't add it without a CORS
# preflight, which this API never grants, so together with SameSite=Lax cookies it blocks cross-site forms.
CSRF_HEADER = "x-kaatclip"
UNSAFE = {"POST", "PUT", "PATCH", "DELETE"}
SLIDE_EVERY = timedelta(hours=1)


def token_hash(token):
    return hashlib.sha256(token.encode()).hexdigest()


def get_db(request: Request):
    """A database session for the request. GET and HEAD requests read in a plain transaction that never
    blocks a writer (the sign-in callback, a GET that writes, is the exception)."""
    readonly = request.method in ("GET", "HEAD") and not request.url.path.startswith("/auth/")
    with request.app.state.sessions() as session:
        if readonly:
            session.connection(execution_options={"readonly": True})
        yield session


def optional_user(request: Request, db=Depends(get_db)) -> User | None:
    token = request.cookies.get(SESSION_COOKIE)
    if not token:
        return None
    row = db.get(SessionRow, token_hash(token))
    now = utcnow()
    if row is None or row.expires_at <= now:
        return None
    if now - row.last_used_at >= SLIDE_EVERY:
        # Sliding expiry, written at most once an hour so reads don't all become writes. On a read-only
        # request another writer may get there first; the slide then simply waits for the next request.
        row.last_used_at = now
        row.expires_at = now + timedelta(days=request.app.state.settings.session_days)
        row.user.last_seen_at = now
        try:
            db.commit()
        except OperationalError:
            db.rollback()
            row = db.get(SessionRow, token_hash(token))
            if row is None:
                return None
    return row.user


def current_user(user: User | None = Depends(optional_user)) -> User:
    if user is None:
        raise HTTPException(401, "Sign in first.")
    return user


def admin_user(user: User = Depends(current_user)) -> User:
    if not user.is_admin:
        raise HTTPException(403, "Only the owner can do this.")
    return user


def own_stream(db, user: User, stream_id: str) -> Stream:
    """A stream the user owns. Someone else's stream answers exactly like a missing one (404), so ids can't
    be probed."""
    stream = db.get(Stream, stream_id)
    if stream is None or stream.user_id != user.id:
        raise HTTPException(404, "Not found.")
    return stream


def allowed_origins(settings):
    origins = {settings.public_url.rstrip("/")}
    if settings.dev_login:
        origins |= {"http://localhost:8770", "http://127.0.0.1:8770", "http://localhost:5173"}
    return origins


async def csrf_guard(request: Request, call_next):
    """Refuse state-changing calls that lack the app's header or come from another site's page."""
    if request.method in UNSAFE and (request.url.path.startswith("/api/") or request.url.path.startswith("/auth/")):
        origin = request.headers.get("origin")
        if request.headers.get(CSRF_HEADER) != "1" or (origin and origin not in allowed_origins(request.app.state.settings)):
            return JSONResponse({"detail": "Refused: this request did not come from the app."}, status_code=403)
    return await call_next(request)
