"""The stream funnel (M4.5): the stream link found and added to drafts, the approval warning's data, the
"Finish in Studio" checklist, and teaser Shorts before upcoming lives."""

import shutil
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import httpx
import pytest
from sqlalchemy import select

from aigcm import db
from aigcm import youtube as yt
from aigcm.api import create_app
from aigcm.api.settings import ApiSettings
from aigcm.db.models import Clip, Post, Render, Stream, YouTubeChannel, utcnow
from aigcm.manage import import_jobs
from aigcm.telegram import post_message

from test_calendar import FakeChannel, iso
from test_posts import DEMO, client_for, setup_export

KEY = yt.new_key()
IST = ZoneInfo("Asia/Kolkata")


class FakeWithLives(FakeChannel):
    def __init__(self):
        super().__init__()
        self.videos = [(v.ljust(11, "x"), at, length, live) for v, at, length, live in self.videos]   # real-length ids
        self.live_at = utcnow().replace(microsecond=0) + timedelta(days=1, hours=1)

    def handler(self, request):
        if str(request.url).startswith(f"{yt.API}/liveBroadcasts"):
            assert request.url.params["broadcastStatus"] == "upcoming"
            return httpx.Response(200, json={"items": [
                {"id": "LIVEabcdefg", "snippet": {"title": "BGMI rank push", "scheduledStartTime": iso(self.live_at)}}]})
        return super().handler(request)


@pytest.fixture
def fake():
    return FakeWithLives()


@pytest.fixture
def app(tmp_path, fake):
    jobs = tmp_path / "jobs"
    shutil.copytree(DEMO, jobs, ignore=shutil.ignore_patterns("decisions.json", "run.log"))
    settings = ApiSettings(db_url=db.sqlite_url(tmp_path / "t.db"), jobs_dir=jobs, dev_login=True,
                           invites=frozenset({"owner@example.com", "b@example.com"}), min_free_bytes=0,
                           token_key=KEY, google_client_id="cid", google_client_secret="sec")
    app = create_app(settings, http=httpx.Client(transport=httpx.MockTransport(fake.handler)))
    with app.state.sessions() as s:
        import_jobs(s, settings, "owner@example.com")
        s.query(Render).delete()
        for clip in s.scalars(select(Clip)).all():
            clip.decision = "keep"
        s.commit()
    return app


def ready(app, n=1):
    out = [setup_export(app, clip_n=i) for i in range(n)]
    with app.state.sessions() as s:
        s.scalar(select(YouTubeChannel)).refresh_token = yt.seal(KEY, "1//r")
        s.commit()
    return out


def stream_of(app, clip_id):
    with app.state.sessions() as s:
        return s.get(Clip, clip_id).stream_id


def test_the_stream_link_is_suggested_and_added_to_drafts(app, fake):
    (render_id, clip_id, _), = ready(app)
    client = client_for(app, "owner@example.com")
    stream_id = stream_of(app, clip_id)
    draft = client.post("/api/posts", json={"render_id": render_id}).json()
    assert draft["has_link"] is False and draft["stream_link"] is None

    client.get("/api/calendar", params={"start": datetime.now(IST).date().isoformat()})    # reads recent uploads
    with app.state.sessions() as s:
        stream = s.get(Stream, stream_id)
        stream.recorded_on = (utcnow() - timedelta(days=3)).date().isoformat()            # the day of "live2"
        stream.duration_s = 2 * 3600 + 120
        s.commit()
    found = client.get(f"/api/streams/{stream_id}/link-suggestions").json()
    assert found[0]["url"] == "https://www.youtube.com/watch?v=live2xxxxxx"

    saved = client.put(f"/api/streams/{stream_id}/link", json={"link": found[0]["url"]}).json()
    assert saved == {"link": found[0]["url"], "drafts_updated": 1}
    draft = client.get(f"/api/posts/{draft['id']}").json()
    assert draft["description"].startswith(f"Full stream: {found[0]['url']}") and draft["has_link"] is True
    # Saving again doesn't add it twice.
    assert client.put(f"/api/streams/{stream_id}/link", json={"link": found[0]["url"]}).json()["drafts_updated"] == 0


def test_finish_in_studio_has_the_comment_and_the_related_stream(app):
    (render_id, clip_id, _), = ready(app)
    client = client_for(app, "owner@example.com")
    client.put(f"/api/streams/{stream_of(app, clip_id)}/link", json={"link": "https://youtu.be/abcdefghijk"})
    post = client.post("/api/posts", json={"render_id": render_id}).json()
    assert post["studio"] is None                                      # not on YouTube yet
    assert client.post(f"/api/posts/{post['id']}/studio", json={"done": True}).status_code == 409
    with app.state.sessions() as s:
        row = s.get(Post, post["id"])
        row.video_id, row.status = "vid12345678", "scheduled"
        s.commit()
    studio = client.get(f"/api/posts/{post['id']}").json()["studio"]
    assert studio["url"] == "https://studio.youtube.com/video/vid12345678/edit"
    assert studio["comment"] == "Full stream 👉 https://youtu.be/abcdefghijk" and studio["related"] and studio["done"] is False
    with app.state.sessions() as s:
        assert "Finish in Studio" in post_message(s.get(Post, post["id"]), "scheduled", "https://x")
    assert client.post(f"/api/posts/{post['id']}/studio", json={"done": True}).json()["studio"]["done"] is True
    with app.state.sessions() as s:
        assert "Finish in Studio" not in post_message(s.get(Post, post["id"]), "live", "https://x")
    assert client_for(app, "b@example.com").post(f"/api/posts/{post['id']}/studio", json={}).status_code == 404


def test_a_teaser_for_an_upcoming_live(app, fake):
    ready(app, 2)
    client = client_for(app, "owner@example.com")
    start = datetime.now(IST).date()
    week = client.get("/api/calendar", params={"start": start.isoformat(), "days": 7}).json()
    [live] = week["lives"]
    assert live["id"] == "LIVEabcdefg" and live["teased"] is False and live["can_tease"] is True
    assert live["day"] == fake.live_at.replace(tzinfo=ZoneInfo("UTC")).astimezone(IST).date().isoformat()

    teaser = client.post("/api/calendar/teaser", json={"live_id": "LIVEabcdefg"}).json()
    assert teaser["status"] == "draft" and teaser["teaser_for"] == "LIVEabcdefg"
    assert teaser["title"].startswith("LIVE at ") and len(teaser["title"]) <= 100
    assert teaser["description"].startswith("🔴 Live at ") and "https://www.youtube.com/watch?v=LIVEabcdefg" in teaser["description"]
    assert teaser["has_link"] is True and teaser["stream_link"] == "https://www.youtube.com/watch?v=LIVEabcdefg"
    publish = datetime.fromisoformat(teaser["publish_at"].replace("Z", "+00:00")).replace(tzinfo=None)
    assert publish == fake.live_at - timedelta(hours=2)

    assert client.post("/api/calendar/teaser", json={"live_id": "LIVEabcdefg"}).status_code == 409   # one per live
    assert client.get("/api/calendar", params={"start": start.isoformat()}).json()["lives"][0]["teased"] is True
    assert client.post("/api/calendar/teaser", json={"live_id": "nope"}).status_code == 404
    assert client_for(app, "b@example.com").post("/api/calendar/teaser", json={"live_id": "LIVEabcdefg"}).status_code == 404


def test_a_teaser_needs_time_and_an_export(app, fake):
    client = client_for(app, "owner@example.com")
    ready(app, 1)
    with app.state.sessions() as s:
        s.query(Render).delete()
        s.commit()
    client.get("/api/calendar", params={"start": datetime.now(IST).date().isoformat()})
    refused = client.post("/api/calendar/teaser", json={"live_id": "LIVEabcdefg"})
    assert refused.status_code == 409 and "Export a kept clip" in refused.json()["detail"]
    with app.state.sessions() as s:
        channel = s.scalar(select(YouTubeChannel))
        channel.upcoming = [{"id": "SOONabcdefg", "title": "soon", "start": iso(utcnow() + timedelta(minutes=90))}]
        s.commit()
    refused = client.post("/api/calendar/teaser", json={"live_id": "SOONabcdefg"})
    assert refused.status_code == 409 and "too soon" in refused.json()["detail"]
