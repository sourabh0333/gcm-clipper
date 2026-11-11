"""The calendar (M4.4): posts by day in the creator's time zone, filling free evenings with drafts (never approving
them), moving drafts, and the Shorts-share gauge from the channel's recent uploads."""

import shutil
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

import httpx
import pytest
from sqlalchemy import select

from aigcm import db
from aigcm import youtube as yt
from aigcm.api import create_app
from aigcm.api.settings import ApiSettings
from aigcm.db.models import Clip, Post, Render, YouTubeChannel, utcnow
from aigcm.manage import import_jobs

from test_posts import DEMO, client_for, later, setup_export

KEY = yt.new_key()
IST = ZoneInfo("Asia/Kolkata")


def iso(moment):
    return moment.replace(microsecond=0).isoformat() + "Z"


class FakeChannel:
    """The channel's uploads: 3 lives and 2 Shorts in the last 28 days, and an old Short that doesn't count."""

    def __init__(self):
        now = utcnow()
        self.videos = [("live1", now - timedelta(days=1), "PT3H2M", True), ("live2", now - timedelta(days=3), "PT2H", True),
                       ("live3", now - timedelta(days=9), "PT4H", True), ("sh1", now - timedelta(days=2), "PT45S", False),
                       ("sh2", now - timedelta(days=5), "PT1M10S", False), ("old", now - timedelta(days=40), "PT30S", False)]
        self.calls = 0

    def handler(self, request):
        url = str(request.url)
        self.calls += 1
        if url == yt.TOKEN_URL:
            return httpx.Response(200, json={"access_token": "ya29.t"})
        if url.startswith(f"{yt.API}/channels"):
            return httpx.Response(200, json={"items": [{"contentDetails": {"relatedPlaylists": {"uploads": "UU1"}}}]})
        if url.startswith(f"{yt.API}/playlistItems"):
            return httpx.Response(200, json={"items": [{"contentDetails": {"videoId": v, "videoPublishedAt": iso(at)}}
                                                       for v, at, _, _ in self.videos]})
        if url.startswith(f"{yt.API}/videos"):
            items = []
            wanted = request.url.params["id"].split(",")
            for v, at, length, live in self.videos:
                if v not in wanted:
                    continue
                item = {"id": v, "contentDetails": {"duration": length}, "snippet": {"publishedAt": iso(at)}, "status": {}}
                if live:
                    item["liveStreamingDetails"] = {"actualStartTime": iso(at)}
                items.append(item)
            return httpx.Response(200, json={"items": items})
        return httpx.Response(404)


@pytest.fixture
def fake():
    return FakeChannel()


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


def exports(app, n):
    out = [setup_export(app, clip_n=i) for i in range(n)]
    with app.state.sessions() as s:
        s.scalar(select(YouTubeChannel)).refresh_token = yt.seal(KEY, "1//r")
        s.commit()
    return out


def today_ist():
    return datetime.now(IST).date()


def test_fill_puts_drafts_on_free_evenings_and_approves_nothing(app):
    exports(app, 3)
    client = client_for(app, "owner@example.com")
    start = today_ist() + timedelta(days=1)
    assert client.post("/api/posts", json={"render_id": "rn_nope"}).status_code == 404
    result = client.post("/api/calendar/fill", json={"tz": "Asia/Kolkata", "start": start.isoformat(), "days": 5}).json()
    assert len(result["placed"]) == 3 and result["free_left"] == 2 and result["exports_left"] == 0
    times = [datetime.fromisoformat(p["publish_at"].replace("Z", "+00:00")).astimezone(IST) for p in result["placed"]]
    assert [t.date() for t in times] == [start + timedelta(days=i) for i in range(3)]
    assert all((t.hour, t.minute) == (19, 0) for t in times)
    assert all(p["status"] == "draft" for p in result["placed"])           # nothing approved by filling

    # Filling again finds no free evening it can use and makes no duplicates.
    again = client.post("/api/calendar/fill", json={"start": start.isoformat(), "days": 3}).json()
    assert again["placed"] == [] and len(client.get("/api/posts").json()) == 3

    week = client.get("/api/calendar", params={"start": start.isoformat(), "days": 7}).json()
    assert [p["day"] for p in week["posts"]] == [(start + timedelta(days=i)).isoformat() for i in range(3)]
    assert week["unscheduled"] == []


def test_fill_uses_waiting_drafts_first_and_skips_busy_days(app):
    (r1, _, _), (r2, _, _) = exports(app, 2)
    client = client_for(app, "owner@example.com")
    waiting = client.post("/api/posts", json={"render_id": r1}).json()
    start = today_ist() + timedelta(days=1)
    busy_at = datetime.combine(start, datetime.min.time(), IST).replace(hour=21)
    planned = client.post("/api/posts", json={"render_id": r2}).json()
    client.put(f"/api/posts/{planned['id']}/time", json={"publish_at": busy_at.isoformat()})
    result = client.post("/api/calendar/fill", json={"start": start.isoformat(), "days": 2}).json()
    assert [p["id"] for p in result["placed"]] == [waiting["id"]]
    placed_day = datetime.fromisoformat(result["placed"][0]["publish_at"].replace("Z", "+00:00")).astimezone(IST).date()
    assert placed_day == start + timedelta(days=1)                             # the first evening was busy


def test_fill_needs_a_channel_and_only_uses_kept_clips(app):
    client = client_for(app, "owner@example.com")
    assert client.post("/api/calendar/fill", json={}).status_code == 409
    exports(app, 2)
    with app.state.sessions() as s:
        for clip in s.scalars(select(Clip)).all():
            clip.decision = "reject"
        s.commit()
    assert client.post("/api/calendar/fill", json={"start": (today_ist() + timedelta(days=1)).isoformat()}).json()["placed"] == []


def test_moving_a_draft_and_not_an_approved_post(app):
    (r1, _, _), = exports(app, 1)
    client = client_for(app, "owner@example.com")
    post = client.post("/api/posts", json={"render_id": r1}).json()
    target = (datetime.now(IST) + timedelta(days=2)).replace(hour=20, minute=30, second=0, microsecond=0)
    moved = client.put(f"/api/posts/{post['id']}/time", json={"publish_at": target.isoformat()}).json()
    assert moved["publish_at"].startswith(target.astimezone(ZoneInfo("UTC")).strftime("%Y-%m-%dT%H:%M"))
    soon = datetime.now(IST) + timedelta(minutes=5)
    assert client.put(f"/api/posts/{post['id']}/time", json={"publish_at": soon.isoformat()}).status_code == 422
    approved = client.post(f"/api/posts/{post['id']}/approve", json={"seen": moved["updated_at"]})
    assert approved.status_code == 200, approved.json()
    refused = client.put(f"/api/posts/{post['id']}/time", json={"publish_at": target.isoformat()})
    assert refused.status_code == 409 and "YouTube Studio" in refused.json()["detail"]


def test_gauge_counts_recent_uploads_and_planned_shorts(app, fake):
    exports(app, 2)
    client = client_for(app, "owner@example.com")
    client.post("/api/calendar/fill", json={"start": (today_ist() + timedelta(days=1)).isoformat(), "days": 2})
    g = client.get("/api/calendar", params={"start": today_ist().isoformat()}).json()["gauge"]
    # 5 uploads in 28 days (3 lives, 2 Shorts) + 2 planned Shorts = 4 Shorts of 7.
    assert (g["shorts"], g["uploads"], g["planned"]) == (4, 7, 2) and g["warn"] is True and g["channel"] == "Test Gaming"
    calls = fake.calls
    client.get("/api/calendar", params={"start": today_ist().isoformat()})
    assert fake.calls == calls                                                  # cached for a few hours
    with app.state.sessions() as s:
        channel = s.scalar(select(YouTubeChannel))
        assert len(channel.recent) == 5 and {v["id"] for v in channel.recent if v["short"]} == {"sh1", "sh2"}


def test_calendar_rules(app):
    client = client_for(app, "owner@example.com")
    assert client.get("/api/calendar", params={"start": "2026-11-09", "days": 60}).status_code == 422
    assert client.get("/api/calendar", params={"start": "2026-11-09", "tz": "Mars/Base"}).status_code == 422
    other = client_for(app, "b@example.com")
    (r1, _, _), = exports(app, 1)
    post = client.post("/api/posts", json={"render_id": r1}).json()
    assert other.put(f"/api/posts/{post['id']}/time", json={"publish_at": later()}).status_code == 404
    assert other.get("/api/calendar", params={"start": date.today().isoformat()}).json()["posts"] == []
    assert yt.seconds("PT1H2M3S") == 3723 and yt.seconds("P1D") == 86400 and yt.seconds("bad") == 0
    with app.state.sessions() as s:
        assert s.scalar(select(Post)) is not None
