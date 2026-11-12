"""Public pages, accepting the policy, and deleting an account (M4.8; YouTube Developer Policies III.A.1, III.A.2,
III.D.2, III.E.4)."""

import shutil
from pathlib import Path

import httpx
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import func, select

from aigcm import db
from aigcm import youtube as yt
from aigcm.api import create_app
from aigcm.api.legal import TERMS_VERSION
from aigcm.api.settings import ApiSettings
from aigcm.db.models import AuditEntry, Clip, Session, Stream, User, YouTubeChannel
from aigcm.manage import import_jobs
from aigcm.studio import brand

DEMO = Path(__file__).resolve().parent.parent / "demo"
APP = {"x-kaatclip": "1"}
KEY = yt.new_key()


@pytest.fixture
def revoked():
    return []


@pytest.fixture
def app(tmp_path, revoked):
    def handler(request):
        if str(request.url) == yt.REVOKE_URL:
            revoked.append(request.content.decode())
            return httpx.Response(200)
        return httpx.Response(404)

    jobs = tmp_path / "jobs"
    shutil.copytree(DEMO, jobs, ignore=shutil.ignore_patterns("decisions.json", "run.log"))
    settings = ApiSettings(db_url=db.sqlite_url(tmp_path / "t.db"), jobs_dir=jobs, dev_login=True,
                           invites=frozenset({"owner@example.com", "b@example.com"}), admins=frozenset({"owner@example.com"}),
                           min_free_bytes=0, token_key=KEY, contact_email="hello@kaatclip.example")
    app = create_app(settings, http=httpx.Client(transport=httpx.MockTransport(handler)))
    with app.state.sessions() as s:
        import_jobs(s, settings, "owner@example.com")
        s.commit()
    return app


def client_for(app, email):
    client = TestClient(app, base_url="http://localhost", headers=APP)
    client.post("/auth/dev-login", json={"email": email})
    return client


def test_the_public_pages_say_what_the_policies_require(app):
    anyone = TestClient(app, base_url="http://localhost")
    for path in ("/about", "/guide", "/privacy", "/terms"):
        page = anyone.get(path)
        assert page.status_code == 200 and page.headers["content-type"].startswith("text/html"), path
        assert 'href="/privacy"' in page.text and 'href="/terms"' in page.text
    privacy = anyone.get("/privacy").text
    for needed in ("uses YouTube API Services", "https://policies.google.com/privacy",                  # III.A.2 b, c
                   "https://security.google.com/settings/security/permissions",                          # III.A.2 h
                   "hello@kaatclip.example", "cookie", "Gemini", "does not show advertisements",          # i, g, e, f
                   "Limited Use", "30 days", "Delete my account and data", TERMS_VERSION):
        assert needed in privacy, needed
    terms = anyone.get("/terms").text
    assert "you are agreeing to be bound by the" in terms and "https://www.youtube.com/t/terms" in terms   # III.A.1
    assert "YouTube API Services" in anyone.get("/about").text


def test_a_creator_accepts_before_connecting_youtube(app):
    client = client_for(app, "b@example.com")
    me = client.get("/api/me").json()
    assert me["accepted"] is False and me["terms_version"] == TERMS_VERSION
    assert client.get("/auth/youtube/start", follow_redirects=False).status_code in (403, 503)
    assert client.post("/api/me/accept", json={"version": "2020-01-01"}).status_code == 409
    assert client.post("/api/me/accept", json={"version": TERMS_VERSION}).json()["accepted"] is True
    assert client.get("/api/me").json()["accepted"] is True
    with app.state.sessions() as s:
        assert s.scalar(select(AuditEntry).where(AuditEntry.action == "terms_accepted")).detail == {"version": TERMS_VERSION}


def test_deleting_an_account_removes_everything_and_revokes(app, revoked):
    client = client_for(app, "owner@example.com")
    settings = app.state.settings
    with app.state.sessions() as s:
        user = s.scalar(select(User).where(User.email == "owner@example.com"))
        s.add(YouTubeChannel(user_id=user.id, channel_id="UC1", title="Test", refresh_token=yt.seal(KEY, "1//secret")))
        folders = [settings.jobs_dir / st.job_dir for st in s.scalars(select(Stream)).all()]
        s.commit()
        user_id = user.id
    kit = brand.folder(settings.jobs_dir, user_id)
    kit.mkdir(parents=True)
    (kit / "logo.png").write_bytes(b"x")
    assert all(f.is_dir() for f in folders)

    assert client.request("DELETE", "/api/me", json={"email": "someone@else.com"}).status_code == 422
    other = client_for(app, "b@example.com")
    gone = client.request("DELETE", "/api/me", json={"email": "Owner@Example.com "})
    assert gone.json() == {"ok": True} and "kc_session" in gone.headers["set-cookie"]
    assert revoked == ["token=1%2F%2Fsecret"]
    assert not any(f.exists() for f in folders) and not kit.exists()
    with app.state.sessions() as s:
        assert s.scalar(select(User).where(User.email == "owner@example.com")) is None
        for table in (Stream, Clip, YouTubeChannel):
            assert s.scalar(select(func.count()).select_from(table)) == 0
        assert s.scalar(select(func.count()).select_from(Session).where(Session.user_id == user_id)) == 0
        assert s.scalar(select(AuditEntry).where(AuditEntry.action == "account_deleted")).user_id is None
    assert client.get("/api/me").status_code == 401
    assert other.get("/api/me").status_code == 200          # nobody else is touched


def test_an_account_with_a_running_stream_waits(app):
    client = client_for(app, "owner@example.com")
    with app.state.sessions() as s:
        s.scalar(select(Stream)).status = "running"
        s.commit()
    refused = client.request("DELETE", "/api/me", json={"email": "owner@example.com"})
    assert refused.status_code == 409 and "Stop it first" in refused.json()["detail"]


def test_the_guide_walks_a_streamer_through(app):
    page = TestClient(app, base_url="http://localhost").get("/guide").text
    for needed in ("Continue with Google", "Connect YouTube", "Automatically record when streaming",
                   "Upload while I stream", "Approve", "Copy Reels caption", "youtube.com/verify", "hello@kaatclip.example"):
        assert needed in page, needed
