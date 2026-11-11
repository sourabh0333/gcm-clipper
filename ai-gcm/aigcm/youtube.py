"""Talking to YouTube for a creator (M4): the scopes, the creator's tokens (encrypted at rest), refreshing them,
finding the connected channel, and revoking. See plans/M4 Plan and post plan.md (P-R3, P-R4, P-R6).

Only three narrow scopes: upload, read, and analytics. Never `youtube`, `youtube.force-ssl` or
`youtubepartner`: the app never edits or deletes a creator's videos, and the consent screen says so."""

import re
import time
from datetime import datetime

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


DURATION = re.compile(r"^P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$")
SHORT_MAX_S = 180          # Shorts can be up to 3 minutes; the API has no Shorts flag, so length decides


def seconds(iso):
    m = DURATION.match(iso or "")
    if not m:
        return 0
    d, h, mi, s = (int(x or 0) for x in m.groups())
    return d * 86400 + h * 3600 + mi * 60 + s


def _get(http, token, path, **params):
    response = http.get(f"{API}/{path}", params=params, headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 401:
        raise Expired("The YouTube connection has expired. Reconnect the channel.")
    if response.status_code != 200:
        raise YouTubeError(f"YouTube didn't answer ({response.status_code}). Try again shortly.")
    return response.json()


def recent_uploads(http, token, since, pages=4):
    """The channel's uploads published since `since` (naive UTC), newest first: id, when, length, live or not,
    Short or not. Returns (items, units used). A few units: the uploads list, then 50 videos per call."""
    units = 1
    found = _get(http, token, "channels", part="contentDetails", mine="true").get("items") or []
    if not found:
        return [], units
    playlist = found[0]["contentDetails"]["relatedPlaylists"]["uploads"]
    ids, page = [], None
    for _ in range(pages):
        params = {"part": "contentDetails", "playlistId": playlist, "maxResults": 50}
        if page:
            params["pageToken"] = page
        data = _get(http, token, "playlistItems", **params)
        units += 1
        older = False
        for item in data.get("items") or []:
            at = (item.get("contentDetails") or {}).get("videoPublishedAt")
            if at and datetime.fromisoformat(at.replace("Z", "+00:00")).replace(tzinfo=None) < since:
                older = True
                continue
            ids.append(item["contentDetails"]["videoId"])
        page = data.get("nextPageToken")
        if older or not page:
            break
    items = []
    for start in range(0, len(ids), 50):
        data = _get(http, token, "videos", part="contentDetails,liveStreamingDetails,snippet,status,statistics",
                    id=",".join(ids[start:start + 50]))
        units += 1
        for v in data.get("items") or []:
            live = "liveStreamingDetails" in v
            length = seconds((v.get("contentDetails") or {}).get("duration"))
            at = (v.get("status") or {}).get("publishAt") or (v.get("snippet") or {}).get("publishedAt")
            views = (v.get("statistics") or {}).get("viewCount")
            items.append({"id": v["id"], "at": at, "seconds": length, "live": live,
                          "short": (not live) and 0 < length <= SHORT_MAX_S,
                          "title": ((v.get("snippet") or {}).get("title") or "")[:200],
                          "views": int(views) if views is not None else None,
                          "privacy": (v.get("status") or {}).get("privacyStatus")})
    return items, units


ANALYTICS = "https://youtubeanalytics.googleapis.com/v2/reports"
CONTENT_TYPES = {"SHORTS": "shorts", "LIVE_STREAM": "live", "VIDEO_ON_DEMAND": "videos"}


def channel_report(http, token, start, end):
    """Views, watch minutes and subscribers gained per content type (Shorts, live, videos; anything else counts as
    other) between two dates, and the last day YouTube had numbers for ("data through"; Analytics lags 2-3 days).
    Uses the YouTube Analytics API, which has its own quota."""
    params = {"ids": "channel==MINE", "startDate": start.isoformat(), "endDate": end.isoformat(),
              "metrics": "views,estimatedMinutesWatched,subscribersGained", "dimensions": "day,creatorContentType",
              "sort": "day"}
    response = http.get(ANALYTICS, params=params, headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 400:
        # Not every channel report takes day with creatorContentType: fall back to the totals (no "data through").
        params.update(dimensions="creatorContentType")
        params.pop("sort")
        response = http.get(ANALYTICS, params=params, headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 401:
        raise Expired("The YouTube connection has expired. Reconnect the channel.")
    if response.status_code == 403:
        raise YouTubeError("YouTube didn't allow reading the channel's stats. Reconnect and keep every box ticked.")
    if response.status_code != 200:
        raise YouTubeError(f"YouTube Analytics didn't answer ({response.status_code}). Try again later.")
    data = response.json()
    names = [h["name"] for h in data.get("columnHeaders") or []]
    totals = {kind: {"views": 0, "minutes": 0, "subscribers": 0} for kind in ("shorts", "live", "videos", "other")}
    through = None
    for row in data.get("rows") or []:
        cell = dict(zip(names, row))
        kind = CONTENT_TYPES.get(str(cell.get("creatorContentType", "")).upper(), "other")
        totals[kind]["views"] += int(cell.get("views") or 0)
        totals[kind]["minutes"] += int(cell.get("estimatedMinutesWatched") or 0)
        totals[kind]["subscribers"] += int(cell.get("subscribersGained") or 0)
        if cell.get("day") and any(cell.get(m) for m in ("views", "estimatedMinutesWatched")):
            through = max(through or cell["day"], cell["day"])
    return {"start": start.isoformat(), "end": end.isoformat(), "through": through, "by_type": totals}


def upcoming_streams(http, token):
    """The channel's scheduled lives: id, title, start (ISO, UTC). 1 unit."""
    data = _get(http, token, "liveBroadcasts", part="snippet", broadcastStatus="upcoming", maxResults=10)
    out = []
    for b in data.get("items") or []:
        snippet = b.get("snippet") or {}
        if snippet.get("scheduledStartTime"):
            out.append({"id": b["id"], "title": (snippet.get("title") or "")[:200], "start": snippet["scheduledStartTime"]})
    return out


def revoke(http, token):
    """Ask Google to end the grant. Best effort: the token is deleted on our side whatever Google says."""
    try:
        return http.post(REVOKE_URL, data={"token": token}, timeout=10).status_code == 200
    except Exception:
        return False


def now_s():
    return time.time()
