"""Live !clip (M4.7) against a fake YouTube chat: finding the live, `!clip` from the owner or a moderator saved at
the second it was typed, viewers and look-alikes ignored, no duplicates across reads, the chat ending, and costs."""

from datetime import timedelta

import httpx
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select

from aigcm import db, livechat
from aigcm import youtube as yt
from aigcm.api import create_app
from aigcm.api.live import markers_file
from aigcm.api.settings import ApiSettings
from aigcm.db.models import LiveSession, Marker, QuotaDay, Stream, User, YouTubeChannel, utcnow
from aigcm.uploader import quota_day

KEY = yt.new_key()
APP = {"x-kaatclip": "1"}


def iso(moment):
    return moment.isoformat(timespec="milliseconds") + "Z"


def message(at, text, name="viewer", owner=False, mod=False):
    return {"snippet": {"displayMessage": text, "publishedAt": iso(at), "type": "textMessageEvent"},
            "authorDetails": {"displayName": name, "isChatOwner": owner, "isChatModerator": mod}}


class FakeChat:
    def __init__(self):
        self.live = False
        self.pages = []           # what each chat read returns, in turn
        self.reads, self.looks, self.tokens_seen = 0, 0, []
        self.ended = False
        self.expired = False

    def handler(self, request):
        url = str(request.url)
        if url == yt.TOKEN_URL:
            if self.expired:
                return httpx.Response(400, json={"error": "invalid_grant"})
            return httpx.Response(200, json={"access_token": "ya29.t"})
        if url.startswith(f"{yt.API}/liveBroadcasts"):
            self.looks += 1
            assert request.url.params["broadcastStatus"] == "active" and request.url.params["broadcastType"] == "all"
            items = [{"id": "BROADabcdef", "snippet": {"liveChatId": "CHAT123", "title": "Rank push"}}] if self.live else []
            return httpx.Response(200, json={"items": items})
        if url.startswith(f"{yt.API}/liveChat/messages"):
            self.reads += 1
            assert request.url.params["liveChatId"] == "CHAT123"
            self.tokens_seen.append(request.url.params.get("pageToken"))
            if self.ended:
                return httpx.Response(403, json={"error": {"errors": [{"reason": "liveChatEnded"}]}})
            items = self.pages.pop(0) if self.pages else []
            return httpx.Response(200, json={"items": items, "nextPageToken": f"tok{self.reads}",
                                             "pollingIntervalMillis": 5000})
        return httpx.Response(404)


@pytest.fixture
def chat():
    return FakeChat()


@pytest.fixture
def app(tmp_path, chat):
    settings = ApiSettings(db_url=db.sqlite_url(tmp_path / "t.db"), jobs_dir=tmp_path / "jobs", dev_login=True,
                           invites=frozenset({"owner@example.com"}), token_key=KEY, google_client_id="cid",
                           google_client_secret="sec")
    return create_app(settings, http=httpx.Client(transport=httpx.MockTransport(chat.handler)))


def live_session(app, with_channel=True):
    client = TestClient(app, base_url="http://localhost", headers=APP)
    client.post("/auth/dev-login", json={"email": "owner@example.com"})
    session = client.post("/api/live", json={"title": "Sunday"}).json()
    if with_channel:
        with app.state.sessions() as s:
            user = s.scalar(select(User))
            s.add(YouTubeChannel(user_id=user.id, channel_id="UC1", title="Test Gaming", refresh_token=yt.seal(KEY, "1//r")))
            s.commit()
    with app.state.sessions() as s:
        started = s.get(LiveSession, session["id"]).started_at
    return client, session["id"], started


def run(app, live_id, now=None):
    return livechat.step(app.state.settings, app.state.sessions, app.state.http, live_id, now=now)


def test_clip_from_the_owner_or_a_moderator_becomes_a_marker(app, chat):
    client, live_id, started = live_session(app)
    assert run(app, live_id) is None and chat.looks == 1                   # not live on YouTube yet
    assert "Waiting for your live" in client.get("/api/live").json()["open"]["chat"]

    chat.live = True
    chat.pages = [[message(started - timedelta(minutes=5), "!clip", "Owner", owner=True),       # before the session
                   message(started + timedelta(seconds=90), "!clip that 1v4", "Owner", owner=True),
                   message(started + timedelta(seconds=95), "!clip", "randomviewer"),            # not allowed
                   message(started + timedelta(seconds=100), "!clips", "Mod", mod=True),          # not the command
                   message(started + timedelta(seconds=120.5), "!CLIP", "Mod", mod=True)]]
    with app.state.sessions() as s:
        s.get(LiveSession, live_id).chat_at = None
        s.commit()
    assert run(app, live_id) == 2
    view = client.get("/api/live").json()["open"]
    assert [(m["t"], m["source"], m["by"]) for m in view["marks"]] == [(90.0, "chat", "Owner"), (120.5, "chat", "Mod")]
    assert "Listening to the chat on Test Gaming" in view["chat"]

    # The next read carries on from YouTube's page token; the same message read twice isn't saved twice.
    chat.pages = [[message(started + timedelta(seconds=120.5), "!CLIP", "Mod", mod=True),
                   message(started + timedelta(minutes=10), "!clip", "Owner", owner=True)]]
    with app.state.sessions() as s:
        live = s.get(LiveSession, live_id)
        assert live.chat_at >= utcnow() + timedelta(seconds=50)         # about a minute, not YouTube's 5 s hint
        live.chat_at = None
        s.commit()
    assert run(app, live_id) == 1 and chat.tokens_seen == [None, "tok1"]
    with app.state.sessions() as s:
        assert s.scalar(select(QuotaDay).where(QuotaDay.day == quota_day())).units == 1 + 1 + 5 + 5
        # The marks reach the job like button marks, counted from the session's start.
        stream = Stream(user_id=s.scalar(select(User)).id, title="x", job_dir="j1", live_session_id=live_id)
        assert [m["t"] for m in markers_file(s, stream)] == [90.0, 120.5, 600.0]


def test_the_chat_ending_and_an_expired_connection(app, chat):
    client, live_id, _ = live_session(app)
    chat.live = True
    run(app, live_id)
    chat.ended = True
    with app.state.sessions() as s:
        s.get(LiveSession, live_id).chat_at = None
        s.commit()
    run(app, live_id)
    assert "chat has ended" in client.get("/api/live").json()["open"]["chat"]
    with app.state.sessions() as s:
        assert livechat.due(s) == []                        # not read again for hours

    client2, live2, _ = live_session(app, with_channel=False)     # a new session ends the old one
    chat.expired = True
    run(app, live2)
    assert "expired" in client2.get("/api/live").json()["open"]["chat"]


def test_no_channel_means_no_chat_reading(app, chat):
    client, live_id, _ = live_session(app, with_channel=False)
    assert run(app, live_id) is None and chat.looks == 0 and chat.reads == 0
    assert "Connect YouTube" in client.get("/api/live").json()["open"]["chat"]
    client.post(f"/api/live/{live_id}/end")
    with app.state.sessions() as s:
        assert livechat.due(s) == []
        assert s.scalar(select(Marker)) is None


def test_the_command():
    assert livechat.is_clip("!clip") and livechat.is_clip("  !Clip  what a play") and livechat.is_clip("!CLIP")
    assert not livechat.is_clip("!clips") and not livechat.is_clip("nice !clip") and not livechat.is_clip("")
    assert livechat.allowed({"isChatModerator": True}) and livechat.allowed({"isChatOwner": True})
    assert not livechat.allowed({"isChatSponsor": True, "isVerified": True})
