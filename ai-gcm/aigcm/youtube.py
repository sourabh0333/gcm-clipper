"""Talking to YouTube for a creator (M4): the scopes, the creator's tokens (encrypted at rest), refreshing them,
finding the connected channel, and revoking. See plans/M4 Plan and post plan.md (P-R3, P-R4, P-R6).

Only three narrow scopes: upload, read, and analytics. Never `youtube`, `youtube.force-ssl` or
`youtubepartner`: the app never edits or deletes a creator's videos, and the consent screen says so."""

import time

from cryptography.fernet import Fernet, InvalidToken

SCOPES = ["https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube.readonly",
          "https://www.googleapis.com/auth/yt-analytics.readonly"]
TOKEN_URL = "https://oauth2.googleapis.com/token"
REVOKE_URL = "https://oauth2.googleapis.com/revoke"
API = "https://www.googleapis.com/youtube/v3"


class YouTubeError(RuntimeError):
    """Something a creator should be told about, in plain words."""


class Expired(YouTubeError):
    """The connection no longer works (revoked, or a testing-mode token past its 7 days): reconnect."""


# --- tokens at rest ------------------------------------------------------------------------------------------

def new_key():
    return Fernet.generate_key().decode()


def _fernet(key):
    if not key:
        raise YouTubeError("YouTube isn't set up on the laptop yet (the token key is missing).")
    return Fernet(key.encode() if isinstance(key, str) else key)


def seal(key, token):
    return _fernet(key).encrypt(token.encode()).decode()


def unseal(key, sealed):
    try:
        return _fernet(key).decrypt(sealed.encode()).decode()
    except InvalidToken as exc:
        raise YouTubeError("The saved YouTube connection can't be read; connect the channel again.") from exc


def missing_scopes(granted):
    """The scopes Google didn't grant (the consent screen lets a creator untick boxes)."""
    have = set((granted or "").split())
    return [s for s in SCOPES if s not in have]


# --- calls ---------------------------------------------------------------------------------------------------

def exchange(http, settings, code, verifier, redirect_uri):
    response = http.post(TOKEN_URL, data={
        "client_id": settings.google_client_id, "client_secret": settings.google_client_secret,
        "code": code, "code_verifier": verifier, "grant_type": "authorization_code", "redirect_uri": redirect_uri})
    if response.status_code != 200:
        raise YouTubeError("Google did not accept the connection. Try again.")
    return response.json()


def _error(response):
    try:
        return response.json().get("error")
    except ValueError:
        return None


def access_token(http, settings, refresh_token):
    """A fresh access token from the refresh token. Raises Expired when Google says it no longer works."""
    response = http.post(TOKEN_URL, data={
        "client_id": settings.google_client_id, "client_secret": settings.google_client_secret,
        "refresh_token": refresh_token, "grant_type": "refresh_token"})
    if response.status_code == 400 and _error(response) in ("invalid_grant", "unauthorized_client"):
        raise Expired("The YouTube connection has expired. Reconnect the channel.")
    if response.status_code != 200:
        raise YouTubeError(f"Google didn't answer ({response.status_code}). Try again shortly.")
    return response.json()["access_token"]


def my_channel(http, token):
    """The channel the creator chose on Google's consent screen: id, title, thumbnail. 1 quota unit."""
    response = http.get(f"{API}/channels", params={"part": "snippet", "mine": "true"},
                        headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 401:
        raise Expired("The YouTube connection has expired. Reconnect the channel.")
    if response.status_code != 200:
        raise YouTubeError(f"YouTube didn't answer ({response.status_code}). Try again shortly.")
    items = response.json().get("items") or []
    if not items:
        raise YouTubeError("This Google account has no YouTube channel yet.")
    item = items[0]
    thumbs = item["snippet"].get("thumbnails") or {}
    picture = (thumbs.get("default") or thumbs.get("medium") or {}).get("url")
    return {"id": item["id"], "title": item["snippet"].get("title") or item["id"], "thumbnail": picture}


def revoke(http, token):
    """Ask Google to end the grant. Best effort: the token is deleted on our side whatever Google says."""
    try:
        return http.post(REVOKE_URL, data={"token": token}, timeout=10).status_code == 200
    except Exception:
        return False


def now_s():
    return time.time()
