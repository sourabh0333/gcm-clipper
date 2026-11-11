"""Connect YouTube (M4.1) against a fake Google: the narrow scopes, the channel picked, tokens sealed at rest,
expiry, disconnect with revoke, and one creator never seeing another's channel."""

import json

from urllib.parse import parse_qs, urlparse

import httpx
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select

from aigcm import youtube as yt
from aigcm.db.models import AuditEntry, YouTubeChannel
from aigcm.manage import token_key

from test_api_auth import APP, FakeGoogle, build, sign_in

KEY = yt.new_key()


class FakeYouTube(FakeGoogle):
    """Google sign-in plus the YouTube consent's token exchange, refresh, channels.list and revoke."""

    def __init__(self):
        super().__init__()
        self.youtube_mode = False
        self.scope = " ".join(yt.SCOPES)
        self.refresh = "1//refresh-secret"
        self.channel = {"id": "UC123", "snippet": {"title": "Test Gaming",
                                                   "thumbnails": {"default": {"url": "https://yt3.example/p.jpg"}}}}
        self.expired = False
        self.revoked = []

    def handler(self, request):
        url = str(request.url)
        if url == yt.REVOKE_URL:
            self.revoked.append(parse_qs(request.content.decode())["token"][0])
            return httpx.Response(200)
        if url.startswith(f"{yt.API}/channels"):
            assert request.headers["authorization"] == "Bearer ya29.access"
            return httpx.Response(200, json={"items": [self.channel] if self.channel else []})
        if url == yt.TOKEN_URL and self.youtube_mode:
            form = parse_qs(request.content.decode())
            self.exchanges.append(form)
            if form["grant_type"] == ["refresh_token"]:
                if self.expired:
                    return httpx.Response(400, json={"error": "invalid_grant"})
                return httpx.Response(200, json={"access_token": "ya29.access", "expires_in": 3599})
            body = {"access_token": "ya29.access", "scope": self.scope, "expires_in": 3599}
            if self.refresh:
                body["refresh_token"] = self.refresh
            return httpx.Response(200, json=body)
        return super().handler(request)


@pytest.fixture
def google():
    return FakeYouTube()


def app_with_key(tmp_path, google, **settings):
    return build(tmp_path, google, token_key=KEY, **settings)


def connect(client, google):
    google.youtube_mode = True
    start = client.get("/auth/youtube/start", follow_redirects=False)
    assert start.status_code == 302
    query = parse_qs(urlparse(start.headers["location"]).query)
    done = client.get("/auth/google/callback", params={"code": "yt-code", "state": query["state"][0]},
                      follow_redirects=False)
    google.youtube_mode = False
    return done, query


def accept(client):
    from aigcm.api.legal import TERMS_VERSION

    assert client.post("/api/me/accept", json={"version": TERMS_VERSION}).status_code == 200


def signed_in(tmp_path, google, **settings):
    client = TestClient(app_with_key(tmp_path, google, **settings), headers=APP)
    sign_in(client, google)
    accept(client)
    return client


def test_connect_asks_only_the_narrow_scopes_and_stores_the_channel(tmp_path, google):
    client = signed_in(tmp_path, google)
    done, query = connect(client, google)
    assert query["scope"] == [" ".join(yt.SCOPES)]
    assert "youtube.force-ssl" not in query["scope"][0] and not query["scope"][0].endswith("/youtube")
    assert query["access_type"] == ["offline"] and query["prompt"] == ["consent"]
    assert query["code_challenge_method"] == ["S256"] and query["redirect_uri"][0].endswith("/auth/google/callback")
    assert done.status_code == 302 and done.headers["location"] == "/settings?youtube=connected"
    assert google.exchanges[-1]["code"] == ["yt-code"] and google.exchanges[-1]["code_verifier"][0]

    state = client.get("/api/youtube").json()
    assert state["available"] is True
    [c] = state["channels"]
    assert (c["channel_id"], c["title"], c["status"]) == ("UC123", "Test Gaming", "ok")
    assert c["thumbnail"] == "https://yt3.example/p.jpg" and c["settings"] == {"made_for_kids": False, "synthetic": False}
    assert "refresh" not in json.dumps(state)          # the token never leaves the server

    with client.app.state.sessions() as s:
        row = s.scalar(select(YouTubeChannel))
        assert google.refresh not in row.refresh_token        # sealed at rest
        assert yt.unseal(KEY, row.refresh_token) == google.refresh
        assert s.scalar(select(AuditEntry).where(AuditEntry.action == "youtube_connect")) is not None


def test_connecting_again_updates_the_same_channel(tmp_path, google):
    client = signed_in(tmp_path, google)
    connect(client, google)
    google.refresh, google.channel["snippet"]["title"] = "1//newer", "Renamed"
    connect(client, google)
    [c] = client.get("/api/youtube").json()["channels"]
    assert c["title"] == "Renamed"
    with client.app.state.sessions() as s:
        assert yt.unseal(KEY, s.scalar(select(YouTubeChannel)).refresh_token) == "1//newer"


@pytest.mark.parametrize("change, result", [
    (lambda g: setattr(g, "scope", " ".join(yt.SCOPES[:1])), "scopes"),     # a box unticked on Google's screen
    (lambda g: setattr(g, "channel", None), "no-channel"),                   # an account with no channel
    (lambda g: setattr(g, "refresh", None), "refused"),                      # no offline access granted
])
def test_a_partial_grant_is_given_back_and_nothing_stored(tmp_path, google, change, result):
    client = signed_in(tmp_path, google)
    change(google)
    done, _ = connect(client, google)
    assert done.headers["location"] == f"/settings?youtube={result}"
    assert client.get("/api/youtube").json()["channels"] == []
    if result != "refused":
        assert google.revoked                              # the half-grant was handed back to Google


def test_cancel_and_strangers_go_back_to_settings(tmp_path, google):
    client = signed_in(tmp_path, google)
    google.youtube_mode = True
    start = client.get("/auth/youtube/start", follow_redirects=False)
    state = parse_qs(urlparse(start.headers["location"]).query)["state"][0]
    cancelled = client.get("/auth/google/callback", params={"error": "access_denied", "state": state},
                           follow_redirects=False)
    assert cancelled.headers["location"] == "/settings?youtube=cancelled"

    # The consent finishing in a browser where someone else is signed in stores nothing for either.
    start = client.get("/auth/youtube/start", follow_redirects=False)
    state = parse_qs(urlparse(start.headers["location"]).query)["state"][0]
    client.post("/auth/logout")
    done = client.get("/auth/google/callback", params={"code": "c", "state": state}, follow_redirects=False)
    assert done.headers["location"] == "/settings?youtube=signed-out"


def test_connect_needs_sign_in_and_the_key(tmp_path, google):
    client = TestClient(app_with_key(tmp_path, google), headers=APP)
    assert client.get("/auth/youtube/start", follow_redirects=False).status_code == 401
    no_key = TestClient(build(tmp_path / "b", google), headers=APP)
    sign_in(no_key, google)
    accept(no_key)
    assert no_key.get("/api/youtube").json() == {"available": False, "channels": []}
    assert no_key.get("/auth/youtube/start", follow_redirects=False).status_code == 503


def test_an_expired_connection_is_marked_and_disconnect_revokes_and_deletes(tmp_path, google):
    client = signed_in(tmp_path, google)
    connect(client, google)
    [c] = client.get("/api/youtube").json()["channels"]
    google.youtube_mode = True
    assert client.post(f"/api/youtube/{c['id']}/check").json()["status"] == "ok"
    google.expired = True
    assert client.post(f"/api/youtube/{c['id']}/check").json()["status"] == "expired"

    answers = client.put(f"/api/youtube/{c['id']}/settings", json={"made_for_kids": False, "synthetic": True})
    assert answers.json()["settings"] == {"made_for_kids": False, "synthetic": True}

    gone = client.delete(f"/api/youtube/{c['id']}")
    assert gone.json() == {"ok": True, "revoked": True} and google.revoked[-1] == google.refresh
    assert client.get("/api/youtube").json()["channels"] == []
    with client.app.state.sessions() as s:
        assert s.scalar(select(YouTubeChannel)) is None
        assert s.scalar(select(AuditEntry).where(AuditEntry.action == "youtube_disconnect")).detail["revoked"] is True


def test_another_creator_cannot_see_or_touch_the_channel(tmp_path, google):
    client = signed_in(tmp_path, google)
    connect(client, google)
    [c] = client.get("/api/youtube").json()["channels"]
    other = TestClient(client.app, headers=APP)
    google.claims = {"email": "second@example.com", "sub": "g-2"}
    sign_in(other, google)
    assert other.get("/api/youtube").json()["channels"] == []
    assert other.delete(f"/api/youtube/{c['id']}").status_code == 404
    assert other.post(f"/api/youtube/{c['id']}/check").status_code == 404
    assert other.put(f"/api/youtube/{c['id']}/settings", json={}).status_code == 404
    assert len(client.get("/api/youtube").json()["channels"]) == 1


def test_sealing_and_the_key_command(tmp_path):
    sealed = yt.seal(KEY, "1//abc")
    assert yt.unseal(KEY, sealed) == "1//abc"
    with pytest.raises(yt.YouTubeError):
        yt.unseal(yt.new_key(), sealed)
    with pytest.raises(yt.YouTubeError):
        yt.seal("", "x")
    assert yt.missing_scopes(" ".join(reversed(yt.SCOPES))) == [] and yt.missing_scopes(None) == yt.SCOPES

    env = tmp_path / ".env"
    env.write_text("GEMINI_API_KEY=x", encoding="utf-8")
    assert token_key(env) is True and token_key(env) is False      # made once, never replaced
    lines = env.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "GEMINI_API_KEY=x"
    [key_line] = [line for line in lines if line.startswith("KAATCLIP_TOKEN_KEY=")]
    assert yt.unseal(key_line.split("=", 1)[1], yt.seal(key_line.split("=", 1)[1], "t")) == "t"


def test_sign_in_still_works_alongside(tmp_path, google):
    client = TestClient(app_with_key(tmp_path, google), headers=APP)
    done, query = sign_in(client, google)
    assert query["scope"] == ["openid email profile"] and done.headers["location"] == "/"
    assert client.get("/api/me").status_code == 200

