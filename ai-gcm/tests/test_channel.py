"""Your channel (M4.6): Analytics by Shorts, live and videos with "data through", recent uploads with views, and
the 30-day job that deletes old YouTube data and re-checks permission."""

import shutil
from datetime import date, timedelta

import httpx
import pytest
from sqlalchemy import select

from aigcm import channel_data, db
from aigcm import youtube as yt
from aigcm.api import create_app
from aigcm.api.settings import ApiSettings
from aigcm.db.models import Post, Render, YouTubeChannel, utcnow
from aigcm.manage import import_jobs

from test_calendar import FakeChannel
from test_posts import DEMO, client_for, setup_export

KEY = yt.new_key()


class FakeAnalytics(FakeChannel):
    def __init__(self):
        super().__init__()
        self.videos = [(v.ljust(11, "x"), at, length, live) for v, at, length, live in self.videos]
        self.analytics_calls, self.expired = 0, False
        self.through = (utcnow() - timedelta(days=3)).date()

    def handler(self, request):
        url = str(request.url)
        if url == yt.TOKEN_URL and self.expired:
            return httpx.Response(400, json={"error": "invalid_grant"})
        if url.startswith(yt.ANALYTICS):
            self.analytics_calls += 1
            p = request.url.params
            assert p["ids"] == "channel==MINE" and p["dimensions"] == "day,creatorContentType"
            day1, day2 = (self.through - timedelta(days=1)).isoformat(), self.through.isoformat()
            later = (self.through + timedelta(days=1)).isoformat()
            rows = [[day1, "SHORTS", 900, 60, 4], [day1, "LIVE_STREAM", 300, 900, 2], [day2, "SHORTS", 600, 40, 1],
                    [day2, "VIDEO_ON_DEMAND", 200, 50, 0], [day2, "STORY", 5, 0, 0], [later, "SHORTS", 0, 0, 0]]
            heads = [{"name": n} for n in ("day", "creatorContentType", "views", "estimatedMinutesWatched", "subscribersGained")]
            return httpx.Response(200, json={"columnHeaders": heads, "rows": rows})
        if url.startswith(f"{yt.API}/videos"):
            response = super().handler(request)
            data = response.json()
            for i, item in enumerate(data["items"]):
                item["statistics"] = {"viewCount": str(1000 * (i + 1))}
                item["status"] = {"privacyStatus": "public"}
            return httpx.Response(200, json=data)
        if url.startswith(f"{yt.API}/liveBroadcasts"):
            return httpx.Response(200, json={"items": []})
        return super().handler(request)


@pytest.fixture
def fake():
    return FakeAnalytics()


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
        s.commit()
    setup_export(app)
    with app.state.sessions() as s:
        s.scalar(select(YouTubeChannel)).refresh_token = yt.seal(KEY, "1//r")
        s.commit()
    return app


def test_your_channel_by_content_type_with_data_through(app, fake):
    client = client_for(app, "owner@example.com")
    [channel] = client.get("/api/channel").json()["channels"]
    stats = channel["stats"]
    assert stats["through"] == fake.through.isoformat()                 # the last day with numbers, not today
    assert stats["by_type"]["shorts"] == {"views": 1500, "minutes": 100, "subscribers": 5}
    assert stats["by_type"]["live"]["views"] == 300 and stats["by_type"]["videos"]["views"] == 200
    assert stats["by_type"]["other"]["views"] == 5
    kinds = {u["id"].rstrip("x"): u["kind"] for u in channel["uploads"]}
    assert kinds["live1"] == "live" and kinds["sh1"] == "shorts" and "old" not in kinds
    assert all(u["views"] for u in channel["uploads"])
    assert channel["uploads"][0]["at"] >= channel["uploads"][-1]["at"]          # newest first
    shorts_url = next(u["url"] for u in channel["uploads"] if u["kind"] == "shorts")
    assert shorts_url.startswith("https://youtube.com/shorts/")

    calls = fake.analytics_calls
    client.get("/api/channel")
    assert fake.analytics_calls == calls                                 # cached for 12 hours
    assert client_for(app, "b@example.com").get("/api/channel").json() == {"channels": []}


def test_kaatclip_posts_are_marked(app):
    client = client_for(app, "owner@example.com")
    with app.state.sessions() as s:
        user_id = s.scalar(select(YouTubeChannel)).user_id
        s.add(Post(user_id=user_id, status="posted", video_id="sh1xxxxxxxx", title="t"))
        s.commit()
    uploads = client.get("/api/channel").json()["channels"][0]["uploads"]
    assert [u["kaatclip"] for u in uploads if u["id"] == "sh1xxxxxxxx"] == [True]


def test_the_30_day_job_deletes_old_data_and_rechecks_permission(app, fake):
    client = client_for(app, "owner@example.com")
    client.get("/api/channel")
    settings, http = app.state.settings, app.state.http
    with app.state.sessions() as s:
        assert channel_data.retention(s, settings, http) == {"forgotten": 0, "checked": 0, "expired": 0}
        channel = s.scalar(select(YouTubeChannel))
        assert channel.recent and channel.stats
        later = utcnow() + timedelta(days=31)
        assert channel_data.retention(s, settings, http, now=later) == {"forgotten": 2, "checked": 1, "expired": 0}
        assert channel.recent is None and channel.stats is None and channel.status == "ok"

        fake.expired = True
        assert channel_data.retention(s, settings, http, now=later + timedelta(days=31))["expired"] == 1
        assert channel.status == "expired"


def test_an_expired_connection_on_refresh_deletes_the_copy(app, fake):
    client = client_for(app, "owner@example.com")
    client.get("/api/channel")
    fake.expired = True
    with app.state.sessions() as s:
        channel = s.scalar(select(YouTubeChannel))
        channel_data.refresh(s, app.state.settings, app.state.http, channel, utcnow() + timedelta(hours=13), stats=True)
        assert channel.status == "expired" and channel.recent is None and channel.stats is None
    [view] = client.get("/api/channel").json()["channels"]
    assert view["status"] == "expired" and view["stats"] is None and view["uploads"] == []


def test_report_parsing_without_rows():
    def handler(request):
        return httpx.Response(200, json={"columnHeaders": [{"name": "day"}], "rows": []})

    http = httpx.Client(transport=httpx.MockTransport(handler))
    report = yt.channel_report(http, "t", date(2026, 10, 14), date(2026, 11, 11))
    assert report["through"] is None and report["by_type"]["shorts"]["views"] == 0
    asked = []

    def picky(request):    # refuses day with creatorContentType, answers the totals
        asked.append(request.url.params["dimensions"])
        if "day" in request.url.params["dimensions"]:
            return httpx.Response(400, json={"error": {"message": "unsupported"}})
        return httpx.Response(200, json={"columnHeaders": [{"name": "creatorContentType"}, {"name": "views"}],
                                         "rows": [["SHORTS", 70], ["LIVE_STREAM", 30]]})

    report = yt.channel_report(httpx.Client(transport=httpx.MockTransport(picky)), "t", date(2026, 10, 14),
                               date(2026, 11, 11))
    assert asked == ["day,creatorContentType", "creatorContentType"]
    assert report["through"] is None and report["by_type"]["shorts"]["views"] == 70
    with pytest.raises(yt.YouTubeError):
        yt.channel_report(httpx.Client(transport=httpx.MockTransport(lambda r: httpx.Response(403))), "t",
                          date(2026, 10, 14), date(2026, 11, 11))
