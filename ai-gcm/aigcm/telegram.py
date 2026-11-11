"""Telegram messages (plan D8): "clips ready", "job failed", and alerts to the owner.

A creator links their Telegram from Settings: the app makes a one-time token and opens
t.me/<bot>?start=<token>; Telegram sends the bot "/start <token>", and the worker's poller (getUpdates long
polling, so the laptop needs no public address) ties that chat to the account. Messages are plain text,
a handful a day, far under Telegram's limits (about one a second per chat). Telegram is free for bots.
"""

import re
import secrets
import threading
import time
from datetime import timedelta

import httpx
from sqlalchemy import select

from .db.models import Stream, TelegramLink, User, utcnow
from .jobs import log

API = "https://api.telegram.org"
TOKEN_TTL = timedelta(minutes=30)
START = re.compile(r"^/start(?:@\w+)?\s+([A-Za-z0-9_-]{16,64})$")


class Bot:
    def __init__(self, token, http=None):
        self.token = token
        self.http = http or httpx.Client(timeout=40)
        self._username = None

    def call(self, method, **params):
        response = self.http.post(f"{API}/bot{self.token}/{method}", json=params)
        data = response.json()
        if not data.get("ok"):
            raise RuntimeError(f"Telegram {method}: {data.get('description', response.status_code)}")
        return data["result"]

    def username(self):
        if self._username is None:
            self._username = self.call("getMe")["username"]
        return self._username

    def send(self, chat_id, text):
        return self.call("sendMessage", chat_id=chat_id, text=text[:4000], disable_web_page_preview=True)


def new_link_token(db, user):
    """A one-time token for t.me/<bot>?start=<token>: letters, digits, _ and - only, under 64 characters."""
    link = db.get(TelegramLink, user.id) or TelegramLink(user_id=user.id)
    link.link_token = secrets.token_urlsafe(24)
    link.token_expires_at = utcnow() + TOKEN_TTL
    db.merge(link)
    db.commit()
    return link.link_token


def handle_update(db, bot, update):
    """One update from getUpdates: a /start <token> links the chat; anything else gets a short help."""
    message = update.get("message") or {}
    chat = (message.get("chat") or {}).get("id")
    text = (message.get("text") or "").strip()
    if not chat or (message.get("chat") or {}).get("type") != "private":
        return
    match = START.match(text)
    if not match:
        bot.send(chat, "Hi! This is Kaatclip. Open Kaatclip → Settings → Connect Telegram to get a message here "
                       "when your clips are ready.")
        return
    link = db.scalar(select(TelegramLink).where(TelegramLink.link_token == match[1]))
    if link is None or link.token_expires_at is None or link.token_expires_at < utcnow():
        bot.send(chat, "That link has expired. Open Kaatclip → Settings → Connect Telegram to get a new one.")
        return
    link.chat_id, link.linked_at, link.link_token, link.token_expires_at = chat, utcnow(), None, None
    db.commit()
    bot.send(chat, "Connected ✅ You'll get a message here when your clips are ready.")


def poll(sessions, bot, stop: threading.Event, timeout=25):
    """Long-poll Telegram for /start messages until `stop` is set. Runs in a thread in the worker."""
    offset = None
    while not stop.is_set():
        try:
            params = {"timeout": timeout, "allowed_updates": ["message"]}
            if offset is not None:
                params["offset"] = offset
            for update in bot.call("getUpdates", **params):
                offset = update["update_id"] + 1
                with sessions() as db:
                    handle_update(db, bot, update)
        except Exception as exc:  # network down, Telegram busy: try again shortly
            log(f"telegram: {exc}")
            stop.wait(15)


def stream_message(stream, event, public_url):
    link = f"{public_url}/streams/{stream.id}"
    if event == "done":
        count = len(stream.clips)
        return f"✅ {stream.title}: {count} clip{'s' if count != 1 else ''} ready.\nReview them: {link}/review"
    if event == "failed":
        return f"⚠️ {stream.title} stopped with an error: {stream.error or 'unknown'}\nOpen it: {link}"
    return None


def post_message(post, event, public_url):
    from .uploader import when_india

    title = f"“{post.title}”"
    channel = post.channel.title if post.channel else "YouTube"
    finish = "" if post.studio_done else f"\nFinish in Studio (related video, pinned comment): {public_url}/posts/{post.id}"
    if event == "scheduled":
        return (f"📅 {title} is on {channel}, private until {when_india(post.publish_at)} (India time). "
                f"YouTube makes it public then.{finish}")
    if event in ("posted", "live"):
        return f"✅ {title} is live on {channel}: https://youtube.com/shorts/{post.video_id}{finish}"
    if event == "failed":
        return f"⚠️ {title} didn't post: {post.error or 'unknown error'}\nOpen it: {public_url}/posts/{post.id}"
    return None


def post_notifier(sessions, bot, public_url):
    """An uploader hook: message the post's owner when it is uploaded, goes live or fails."""
    from .db.models import Post

    def hook(post_id, event):
        with sessions() as db:
            post = db.get(Post, post_id)
            text = post_message(post, event, public_url) if post else None
            link = db.get(TelegramLink, post.user_id) if post else None
            if text and link and link.chat_id:
                bot.send(link.chat_id, text)
    return hook


def notifier(sessions, bot, public_url):
    """A worker hook: message the stream's owner when their job is done or failed."""
    def hook(stream, event):
        text = stream_message(stream, event, public_url)
        if not text:
            return
        with sessions() as db:
            link = db.get(TelegramLink, stream.user_id)
            if link and link.chat_id:
                bot.send(link.chat_id, text)
    return hook


def alert_owners(db, bot, settings, text):
    """Send an alert to every admin who linked Telegram."""
    for user in db.scalars(select(User).where(User.is_admin.is_(True))):
        link = db.get(TelegramLink, user.id)
        if link and link.chat_id:
            bot.send(link.chat_id, f"🔔 Kaatclip: {text}")


def worker_offline(db, now=None, stale=timedelta(minutes=5)):
    """True when streams are waiting and the worker hasn't beaten for `stale`."""
    from .db.models import WorkerState

    now = now or utcnow()
    waiting = db.scalar(select(Stream.id).where(Stream.status == "queued").limit(1)) is not None
    state = db.get(WorkerState, 1)
    beat = state.heartbeat_at if state else None
    return waiting and (beat is None or now - beat > stale)


def watchdog(sessions, bot, settings, stop: threading.Event, every=300, repeat_after=3600):
    """Runs in the API: tells the owner when uploaded streams wait and the worker isn't running."""
    last_alert = 0.0
    while not stop.wait(every):
        try:
            with sessions() as db:
                if worker_offline(db) and time.time() - last_alert > repeat_after:
                    alert_owners(db, bot, settings, "streams are waiting but the worker isn't running. Start it with "
                                                    "python -m aigcm.worker on the laptop.")
                    last_alert = time.time()
        except Exception as exc:
            log(f"telegram watchdog: {exc}")
