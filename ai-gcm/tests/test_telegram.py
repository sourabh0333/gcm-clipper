"""Telegram linking and messages, against a fake Telegram API."""

import json
import sys
import threading
from datetime import timedelta

import httpx
import pytest
from fastapi.testclient import TestClient

from aigcm import db, telegram
from aigcm.api import create_app
from aigcm.api.settings import ApiSettings
from aigcm.db.models import Stream, TelegramLink, User, WorkerState, utcnow
from aigcm.worker import Worker

APP = {"x-kaatclip": "1"}


class FakeTelegram:
    def __init__(self):
        self.sent, self.updates, self.stop = [], [], None

    def handler(self, request: httpx.Request):
        method = request.url.path.rsplit("/", 1)[1]
        body = json.loads(request.content or b"{}")
        if method == "getMe":
            return httpx.Response(200, json={"ok": True, "result": {"username": "kaatclip_bot"}})
        if method == "sendMessage":
            self.sent.append((body["chat_id"], body["text"]))
            return httpx.Response(200, json={"ok": True, "result": {}})
        if method == "getUpdates":
            batch, self.updates = self.updates, []
            if self.stop is not None:
                self.stop.set()
            return httpx.Response(200, json={"ok": True, "result": batch})
        return httpx.Response(404, json={"ok": False, "description": "no such method"})


@pytest.fixture
def tg():
    return FakeTelegram()


@pytest.fixture
def app(tmp_path, tg):
    settings = ApiSettings(db_url=db.sqlite_url(tmp_path / "t.db"), jobs_dir=tmp_path / "jobs", dev_login=True,
                           invites=frozenset({"a@example.com"}), admins=frozenset({"owner@example.com"}),
                           telegram_bot_token="123:abc", public_url="https://kc.example")
    return create_app(settings, http=httpx.Client(transport=httpx.MockTransport(tg.handler)))


def client_for(app, email):
    client = TestClient(app, base_url="http://localhost")
    client.post("/auth/dev-login", json={"email": email}, headers=APP)
    return client


def start_message(text, chat=555, kind="private", update_id=1):
    return {"update_id": update_id, "message": {"chat": {"id": chat, "type": kind}, "text": text}}


def link_chat(app, tg, client, chat=555):
    url = client.post("/api/telegram/link", headers=APP).json()["url"]
    token = url.split("start=")[1]
    with app.state.sessions() as s:
        telegram.handle_update(s, app.state.bot, start_message(f"/start {token}", chat=chat))
    return url


def test_linking_through_settings(app, tg):
    a = client_for(app, "a@example.com")
    assert a.get("/api/telegram").json() == {"available": True, "linked": False}
    url = link_chat(app, tg, a)
    assert url.startswith("https://t.me/kaatclip_bot?start=")
    token = url.split("start=")[1]
    assert 16 <= len(token) <= 64 and all(c.isalnum() or c in "-_" for c in token)
    assert a.get("/api/telegram").json()["linked"] is True
    assert tg.sent[-1][0] == 555 and "Connected" in tg.sent[-1][1]
    # The token works once.
    with app.state.sessions() as s:
        telegram.handle_update(s, app.state.bot, start_message(f"/start {token}", chat=999))
    assert "expired" in tg.sent[-1][1]
    assert a.delete("/api/telegram", headers=APP).json() == {"linked": False}
    assert a.get("/api/telegram").json()["linked"] is False


def test_expired_links_help_text_and_group_chats(app, tg):
    a = client_for(app, "a@example.com")
    token = a.post("/api/telegram/link", headers=APP).json()["url"].split("start=")[1]
    with app.state.sessions() as s:
        link = s.query(TelegramLink).one()
        link.token_expires_at = utcnow() - timedelta(minutes=1)
        s.commit()
        telegram.handle_update(s, app.state.bot, start_message(f"/start {token}"))
        assert "expired" in tg.sent[-1][1]
        telegram.handle_update(s, app.state.bot, start_message("hello"))
        assert "Settings" in tg.sent[-1][1]
        before = len(tg.sent)
        telegram.handle_update(s, app.state.bot, start_message(f"/start {token}", kind="group"))
        assert len(tg.sent) == before   # groups are ignored


def test_without_a_token_telegram_is_simply_unavailable(tmp_path):
    app = create_app(ApiSettings(db_url=db.sqlite_url(tmp_path / "t.db"), jobs_dir=tmp_path / "jobs", dev_login=True,
                                 invites=frozenset({"a@example.com"})))
    a = client_for(app, "a@example.com")
    assert a.get("/api/telegram").json() == {"available": False, "linked": False}
    assert a.post("/api/telegram/link", headers=APP).status_code == 503


FINISH = r"""
import json, sys, pathlib
folder = pathlib.Path(sys.argv[1]); (folder / "clips").mkdir(exist_ok=True)
(folder / "clips" / "a.mp4").write_bytes(b"x"); (folder / "clips" / "b.mp4").write_bytes(b"x")
(folder / "ranked.json").write_text(json.dumps([{"id": "m01", "start": 1, "end": 20}, {"id": "m02", "start": 30, "end": 50}]))
(folder / "clips.json").write_text(json.dumps({"m01": "a.mp4", "m02": "b.mp4"}))
"""


def test_the_worker_messages_the_creator_when_clips_are_ready(app, tg):
    a = client_for(app, "a@example.com")
    link_chat(app, tg, a, chat=777)
    settings = app.state.settings
    worker = Worker(settings, command=lambda stream, folder: [sys.executable, "-c", FINISH, str(folder)],
                    notify=[telegram.notifier(app.state.sessions, app.state.bot, settings.public_url)])
    with worker.sessions() as s:
        user = s.query(User).filter_by(email="a@example.com").one()
        stream = Stream(id="st_t1", job_dir="st_t1", user_id=user.id, title="Rank push", status="queued", queued_at=utcnow())
        s.add(stream)
        s.commit()
    (settings.jobs_dir / "st_t1").mkdir(parents=True)
    (settings.jobs_dir / "st_t1" / "source.mp4").write_bytes(b"v")
    worker.step()
    chat, text = tg.sent[-1]
    assert chat == 777 and text.startswith("✅ Rank push: 2 clips ready.")
    assert "https://kc.example/streams/st_t1/review" in text


def test_failed_jobs_say_why_and_unlinked_creators_get_nothing(app, tg):
    hook = telegram.notifier(app.state.sessions, app.state.bot, "https://kc.example")
    with app.state.sessions() as s:
        user = User(email="nolink@example.com")
        s.add(user)
        s.flush()
        stream = Stream(id="st_f", job_dir="st_f", user_id=user.id, title="Scrims", status="failed", error="vision: ffmpeg failed")
        s.add(stream)
        s.commit()
        hook(stream, "failed")
        assert tg.sent == []
        s.add(TelegramLink(user_id=user.id, chat_id=42))
        s.commit()
        hook(stream, "failed")
        hook(stream, "stopped")   # a creator's own Stop needs no message
    assert tg.sent == [(42, "⚠️ Scrims stopped with an error: vision: ffmpeg failed\nOpen it: https://kc.example/streams/st_f")]


def test_the_poller_links_chats_from_updates(app, tg):
    a = client_for(app, "a@example.com")
    token = a.post("/api/telegram/link", headers=APP).json()["url"].split("start=")[1]
    tg.updates = [start_message(f"/start {token}", chat=31337, update_id=10)]
    tg.stop = threading.Event()
    telegram.poll(app.state.sessions, app.state.bot, tg.stop, timeout=0)
    assert a.get("/api/telegram").json()["linked"] is True and tg.sent[-1][0] == 31337


def test_owner_alerts_when_the_worker_is_down_or_the_disk_is_low(app, tg, monkeypatch):
    owner = client_for(app, "owner@example.com")
    link_chat(app, tg, owner, chat=1)
    with app.state.sessions() as s:
        assert telegram.worker_offline(s) is False                 # nothing waiting
        user = s.query(User).filter_by(email="owner@example.com").one()
        s.add(Stream(id="st_q", job_dir="st_q", user_id=user.id, title="x", status="queued"))
        s.merge(WorkerState(id=1, heartbeat_at=utcnow()))
        s.commit()
        assert telegram.worker_offline(s) is False                 # worker alive
        assert telegram.worker_offline(s, now=utcnow() + timedelta(minutes=10)) is True
    import shutil
    worker = Worker(app.state.settings, bot=app.state.bot)
    monkeypatch.setattr(shutil, "disk_usage", lambda p: shutil._ntuple_diskusage(100, 99, 1))
    app.state.settings.min_free_bytes = 10
    assert worker.check_disk() is True and "GB free" in tg.sent[-1][1] and tg.sent[-1][0] == 1
    assert worker.check_disk() is False                            # once a day
