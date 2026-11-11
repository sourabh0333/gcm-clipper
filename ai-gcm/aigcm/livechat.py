"""Live `!clip` (M4.7): while a creator has a Live session open in Kaatclip, read their YouTube live's chat and turn
`!clip` from the channel owner or a moderator into a marker at the moment it was typed. Nothing is posted in chat
(that needs the broad scope: M4 review P-R8); markers are saved silently.

YouTube's streaming chat method (liveChatMessages.streamList) is only offered over gRPC, which would need a new
package (the M4 decisions keep to none), so the listener polls `liveChatMessages.list` (5 units) about once a
minute. Each message carries the time it was typed, so a marker lands on the right second however late it is
read: about 300 units an hour of live, out of the app's 10,000 a day. Finding the live costs 1 unit, tried every
2 minutes until the creator is live."""

from datetime import datetime, timedelta, timezone

import httpx
from sqlalchemy import func, select

from . import youtube as yt
from .db.models import LiveSession, Marker, YouTubeChannel, utcnow
from .jobs import log

READ_EVERY = timedelta(seconds=60)
LOOK_EVERY = timedelta(minutes=2)
UNITS_READ, UNITS_LOOK = 5, 1
MAX_MARKERS = 300
COMMAND = "!clip"


def is_clip(text):
    """`!clip`, `!Clip`, `!clip that was insane`: yes. `!clips`, `lol !clip`: no."""
    words = (text or "").strip().split(maxsplit=1)
    return bool(words) and words[0].lower() == COMMAND


def allowed(author):
    return bool(author.get("isChatOwner") or author.get("isChatModerator"))


def active_broadcast(http, token):
    """The live the channel is broadcasting now (any kind: scheduled event or Go Live), or None. 1 unit."""
    response = http.get(f"{yt.API}/liveBroadcasts", params={"part": "snippet", "broadcastStatus": "active",
                                                            "broadcastType": "all", "maxResults": 5},
                        headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 401:
        raise yt.Expired("The YouTube connection has expired. Reconnect the channel.")
    if response.status_code != 200:
        raise yt.YouTubeError(f"YouTube didn't answer ({response.status_code}).")
    for item in response.json().get("items") or []:
        snippet = item.get("snippet") or {}
        if snippet.get("liveChatId"):
            return {"id": item["id"], "chat_id": snippet["liveChatId"], "title": snippet.get("title") or ""}
    return None


class ChatOver(Exception):
    """The live's chat has ended or is turned off."""


def read_chat(http, token, chat_id, page_token=None):
    """One page of chat since `page_token`: (messages, next token, YouTube's polling hint in seconds). 5 units."""
    params = {"liveChatId": chat_id, "part": "snippet,authorDetails", "maxResults": 2000}
    if page_token:
        params["pageToken"] = page_token
    response = http.get(f"{yt.API}/liveChat/messages", params=params, headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 401:
        raise yt.Expired("The YouTube connection has expired. Reconnect the channel.")
    if response.status_code in (403, 404):
        try:
            reason = ((response.json().get("error") or {}).get("errors") or [{}])[0].get("reason")
        except ValueError:
            reason = None
        if reason in ("liveChatEnded", "liveChatDisabled", "liveChatNotFound") or response.status_code == 404:
            raise ChatOver(reason or "liveChatNotFound")
        raise yt.YouTubeError(f"YouTube refused reading the chat ({reason or response.status_code}).")
    if response.status_code != 200:
        raise yt.YouTubeError(f"YouTube didn't answer ({response.status_code}).")
    data = response.json()
    if data.get("offlineAt"):
        raise ChatOver("offline")
    return data.get("items") or [], data.get("nextPageToken"), (data.get("pollingIntervalMillis") or 0) / 1000


def _when(iso):
    """YouTube's time (with any offset) as naive UTC, like every time Kaatclip stores."""
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(timezone.utc).replace(tzinfo=None)


def clip_markers(items, since):
    """(time, who) for each `!clip` by the owner or a moderator typed at or after `since` (naive UTC)."""
    out = []
    for item in items:
        snippet, author = item.get("snippet") or {}, item.get("authorDetails") or {}
        text = snippet.get("displayMessage") or (snippet.get("textMessageDetails") or {}).get("messageText")
        if not is_clip(text) or not allowed(author) or not snippet.get("publishedAt"):
            continue
        at = _when(snippet["publishedAt"])
        if at >= since:
            out.append((at, (author.get("displayName") or "")[:100]))
    return out


def due(db, now=None):
    """Open Live sessions whose chat should be looked at now."""
    now = now or utcnow()
    return [s.id for s in db.scalars(select(LiveSession).where(LiveSession.ended_at.is_(None))).all()
            if s.chat_at is None or s.chat_at <= now]


def step(settings, sessions, http, live_id, now=None):
    """Look at one open session's chat once: find the live if not yet found, else read new messages and save
    `!clip` markers. Returns the number of markers added (None when it only looked for the live)."""
    from .uploader import spend

    now = now or utcnow()
    with sessions() as db:
        live = db.get(LiveSession, live_id)
        channels = db.scalars(select(YouTubeChannel).where(YouTubeChannel.user_id == live.user_id,
                                                           YouTubeChannel.status == "ok")
                              .order_by(YouTubeChannel.connected_at)).all()
        if live.channel_id:
            channels = [c for c in channels if c.id == live.channel_id]
        if not channels or not settings.token_key:
            live.chat_note, live.chat_at = "Connect YouTube in Settings to mark moments with !clip in chat.", now + LOOK_EVERY
            db.commit()
            return None
        tokens = {c.id: c.refresh_token for c in channels}
        titles = {c.id: c.title for c in channels}
        chat_id, page_token, started = live.chat_id, live.chat_token, live.started_at
    added, note, units = None, None, 0
    next_at = now + READ_EVERY
    found = None
    try:
        if chat_id is None:
            for channel_id, sealed in tokens.items():
                token = yt.access_token(http, settings, yt.unseal(settings.token_key, sealed))
                units += UNITS_LOOK
                broadcast = active_broadcast(http, token)
                if broadcast:
                    found = (channel_id, broadcast)
                    break
            if found is None:
                note, next_at = "Waiting for your live on YouTube…", now + LOOK_EVERY
            else:
                channel_id, broadcast = found
                chat_id = broadcast["chat_id"]
                note = f"Listening to the chat on {titles[channel_id]}: !clip from you or a moderator marks a moment."
        if chat_id is not None:
            channel_id = found[0] if found else next(iter(tokens))
            token = yt.access_token(http, settings, yt.unseal(settings.token_key, tokens[channel_id]))
            items, page_token, hint = read_chat(http, token, chat_id, page_token)
            units += UNITS_READ
            marks = clip_markers(items, started)
            with sessions() as db:
                live = db.get(LiveSession, live_id)
                have = db.scalar(select(func.count()).select_from(Marker).where(Marker.live_session_id == live_id))
                existing = {(m.at, m.by) for m in db.scalars(select(Marker).where(Marker.live_session_id == live_id,
                                                                               Marker.source == "chat"))}
                added = 0
                for at, who in marks:
                    if (at, who) in existing or have + added >= MAX_MARKERS:
                        continue
                    db.add(Marker(user_id=live.user_id, live_session_id=live_id, at=at, source="chat", by=who))
                    added += 1
                db.commit()
            next_at = now + max(READ_EVERY, timedelta(seconds=hint))
            note = note or f"Listening to the chat on {titles[channel_id]}: !clip from you or a moderator marks a moment."
    except ChatOver:
        note, next_at, page_token = "The live's chat has ended. Tap End when you're done.", now + timedelta(hours=12), None
    except yt.Expired:
        note, next_at = "The YouTube connection has expired. Reconnect in Settings.", now + LOOK_EVERY
    except (yt.YouTubeError, httpx.TransportError) as exc:
        log(f"live chat {live_id}: {exc}")
        note, next_at = "Couldn't reach YouTube's chat; trying again.", now + READ_EVERY
    with sessions() as db:
        live = db.get(LiveSession, live_id)
        if found:
            live.channel_id, live.broadcast_id = found[0], found[1]["id"]
        live.chat_id, live.chat_token, live.chat_at, live.chat_note = chat_id, page_token, next_at, note
        if units:
            spend(db, units=units, now=now)
        db.commit()
    if added:
        log(f"live chat {live_id}: {added} !clip marker{'s' if added > 1 else ''}")
    return added
