"""The uploader (M4.3) against a fake YouTube: only the approved text goes up, private with publishAt; pieces,
resuming after a dropped connection, the read-back, the thumbnail, going live, the daily limit, and the cases
that must fail loudly."""

import json
import shutil
from datetime import datetime, timedelta
from urllib.parse import parse_qs

import httpx
import pytest
from sqlalchemy import select

from aigcm import db, uploader
from aigcm import youtube as yt
from aigcm.api import create_app
from aigcm.api.settings import ApiSettings
from aigcm.db.models import AuditEntry, Clip, Post, QuotaDay, Render, YouTubeChannel, utcnow
from aigcm.manage import import_jobs
from aigcm.studio import lane, project
from aigcm.telegram import post_message

from test_posts import DEMO, client_for, draft, later, setup_export

KEY = yt.new_key()
SIZE = 2500          # the fake export's size; pieces of 1,000 bytes make three PUTs


class FakeYouTube:
    def __init__(self):
        self.metadata, self.sessions_started, self.puts, self.thumbs = [], 0, [], []
        self.received = b""
        self.fail_put = set()       # PUT numbers that answer 503
        self.privacy = None         # what the read-back says; None = what was asked for
        self.processing = "succeeded"
        self.refresh_error = None
        self.gone = False

    def handler(self, request: httpx.Request):
        url = str(request.url)
        if url == yt.TOKEN_URL:
            if self.refresh_error:
                return httpx.Response(400, json={"error": self.refresh_error})
            return httpx.Response(200, json={"access_token": "ya29.t", "expires_in": 3600})
        if url.startswith(uploader.UPLOAD_URL) and request.method == "POST":
            assert parse_qs(request.url.query.decode())["uploadType"] == ["resumable"]
            assert request.headers["x-upload-content-length"] == str(SIZE)
            self.metadata.append(json.loads(request.content))
            self.sessions_started += 1
            self.received = b""
            return httpx.Response(200, headers={"location": f"https://upload.fake/s{self.sessions_started}"})
        if url.startswith("https://upload.fake/") and request.method == "PUT":
            self.puts.append(request.headers["content-range"])
            if len(self.puts) in self.fail_put:
                return httpx.Response(503)
            spec, total = request.headers["content-range"][6:].split("/")
            if spec != "*":
                start = int(spec.split("-")[0])
                assert start == len(self.received), "a piece must start where YouTube's copy ends"
                self.received += request.content
            if len(self.received) == int(total):
                return httpx.Response(200, json={"id": "vid12345678"})
            headers = {"range": f"bytes=0-{len(self.received) - 1}"} if self.received else {}
            return httpx.Response(308, headers=headers)
        if url.startswith(f"{yt.API}/videos"):
            if self.gone:
                return httpx.Response(200, json={"items": []})
            meta = self.metadata[-1]["status"]
            status = {"uploadStatus": "processed" if self.processing == "succeeded" else "uploaded",
                      "privacyStatus": self.privacy or meta["privacyStatus"]}
            if "publishAt" in meta:
                status["publishAt"] = meta["publishAt"]
            return httpx.Response(200, json={"items": [{"id": "vid12345678", "status": status,
                                                        "processingDetails": {"processingStatus": self.processing}}]})
        if url.startswith(uploader.THUMB_URL):
            self.thumbs.append(len(request.content))
            return httpx.Response(200, json={"items": []})
        return httpx.Response(404)


@pytest.fixture
def app(tmp_path):
    jobs = tmp_path / "jobs"
    shutil.copytree(DEMO, jobs, ignore=shutil.ignore_patterns("decisions.json", "run.log"))
    settings = ApiSettings(db_url=db.sqlite_url(tmp_path / "t.db"), jobs_dir=jobs, dev_login=True,
                           invites=frozenset({"b@example.com"}), admins=frozenset({"owner@example.com"}),
                           min_free_bytes=0, token_key=KEY, google_client_id="cid", google_client_secret="sec")
    app = create_app(settings)
    with app.state.sessions() as s:
        import_jobs(s, settings, "owner@example.com")
        s.query(Render).delete()
        s.commit()
    return app


@pytest.fixture
def yt_fake():
    return FakeYouTube()


def approved_post(app, mode="schedule", minutes=120, clip_n=0):
    render_id, clip_id, _ = setup_export(app, clip_n=clip_n)
    with app.state.sessions() as s:
        channel = s.scalar(select(YouTubeChannel))
        channel.refresh_token = yt.seal(KEY, "1//refresh")
        clip = s.get(Clip, clip_id)
        video = project.job_folder(app.state.settings, clip) / "exports" / f"e{clip_id}.mp4"
        video.write_bytes(bytes(range(256)) * (SIZE // 256) + b"x" * (SIZE % 256))
        lane.cover_path(video).write_bytes(b"\xff\xd8 fake jpeg")
        s.commit()
    client = client_for(app, "owner@example.com")
    post = draft(client, render_id, title="1v4 clutch", description="Full stream: https://youtu.be/abcdefghijk",
                 tags=["bgmi"], mode=mode, publish_at=later(minutes) if mode == "schedule" else None)
    done = client.post(f"/api/posts/{post['id']}/approve", json={"seen": post["updated_at"]})
    assert done.status_code == 200, done.json()
    return post["id"], client


def run(app, fake, events=None, chunk=1000, **kw):
    http = httpx.Client(transport=httpx.MockTransport(fake.handler))
    notify = (lambda post_id, event: events.append(event)) if events is not None else None
    with app.state.sessions() as s:
        post_id = uploader.claim(s)
    if post_id is None:
        return None
    return uploader.upload(app.state.settings, app.state.sessions, http, post_id, notify, chunk=chunk, **kw)


def post_row(app, post_id):
    with app.state.sessions() as s:
        post = s.get(Post, post_id)
        s.expunge(post)
        return post


def test_a_scheduled_post_goes_up_private_with_exactly_the_approved_text(app, yt_fake):
    post_id, client = approved_post(app)
    events = []
    assert run(app, yt_fake, events) == "scheduled" and events == ["scheduled"]
    [meta] = yt_fake.metadata
    approval = post_row(app, post_id).approval
    assert meta["snippet"] == {"title": "1v4 clutch", "description": "Full stream: https://youtu.be/abcdefghijk",
                               "tags": ["bgmi"], "categoryId": "20"}
    assert meta["status"]["privacyStatus"] == "private" and meta["status"]["publishAt"] == approval["publish_at"]
    assert meta["status"]["selfDeclaredMadeForKids"] is False and meta["status"]["containsSyntheticMedia"] is False
    assert len([p for p in yt_fake.puts if "*" not in p]) == 3         # three pieces of 1,000 bytes or less
    row = post_row(app, post_id)
    assert row.status == "scheduled" and row.video_id == "vid12345678" and row.upload_url is None
    assert client.get("/api/posts/quota").json() == {"uploads": 1, "uploads_limit": 100, "units": 1, "units_limit": 10000}
    with app.state.sessions() as s:
        assert s.scalar(select(AuditEntry).where(AuditEntry.action == "post_uploaded")).detail["video"] == "vid12345678"
    assert client.post(f"/api/posts/{post_id}/cancel").status_code == 409      # on YouTube now: Studio only


def test_post_now_is_public_and_the_thumbnail_follows_processing(app, yt_fake):
    post_id, _ = approved_post(app, mode="now")
    events = []
    assert run(app, yt_fake, events) == "posted" and events == ["posted"]
    assert yt_fake.metadata[0]["status"]["privacyStatus"] == "public" and "publishAt" not in yt_fake.metadata[0]["status"]
    http = httpx.Client(transport=httpx.MockTransport(yt_fake.handler))
    settings, sessions = app.state.settings, app.state.sessions
    with sessions() as s:
        assert uploader.due_check(s, utcnow() + timedelta(minutes=2)) == post_id
    yt_fake.processing = "processing"
    assert uploader.check(settings, sessions, http, post_id, now=utcnow() + timedelta(minutes=2)) is None
    assert post_row(app, post_id).thumbnail is None and yt_fake.thumbs == []
    yt_fake.processing = "succeeded"
    assert uploader.check(settings, sessions, http, post_id, now=utcnow() + timedelta(minutes=4)) == "thumbnail"
    assert post_row(app, post_id).thumbnail == "set" and yt_fake.thumbs == [len(b"\xff\xd8 fake jpeg")]
    with sessions() as s:
        assert uploader.due_check(s, utcnow() + timedelta(minutes=10)) is None     # nothing left to look at
        assert uploader.usage(s)["units"] == 1 + 1 + 1 + 50


def test_a_scheduled_post_is_confirmed_live_after_its_time(app, yt_fake):
    post_id, _ = approved_post(app, minutes=60)
    run(app, yt_fake)
    http = httpx.Client(transport=httpx.MockTransport(yt_fake.handler))
    publish_at = post_row(app, post_id).publish_at
    events = []
    notify = lambda pid, event: events.append(event)    # noqa: E731
    yt_fake.privacy = "public"
    assert uploader.check(app.state.settings, app.state.sessions, http, post_id, notify,
                          now=publish_at + timedelta(minutes=1)) == "posted"
    row = post_row(app, post_id)
    assert row.status == "posted" and row.posted_at and events == ["live"]


def test_still_private_long_after_its_time_fails_loudly(app, yt_fake):
    post_id, _ = approved_post(app, minutes=60)
    run(app, yt_fake)
    http = httpx.Client(transport=httpx.MockTransport(yt_fake.handler))
    publish_at = post_row(app, post_id).publish_at
    yt_fake.privacy = "private"
    assert uploader.check(app.state.settings, app.state.sessions, http, post_id,
                          now=publish_at + timedelta(hours=3)) == "failed"
    assert "didn't make it public" in post_row(app, post_id).error


def test_a_dropped_connection_resumes_where_it_stopped(app, yt_fake):
    post_id, _ = approved_post(app)
    yt_fake.fail_put = {2}
    assert run(app, yt_fake) == "retrying"
    row = post_row(app, post_id)
    assert row.status == "approved" and row.upload_url == "https://upload.fake/s1" and row.next_try_at and row.attempts == 1
    with app.state.sessions() as s:
        assert uploader.claim(s) is None              # not before its time
        s.get(Post, post_id).next_try_at = utcnow() - timedelta(seconds=1)
        s.commit()
    assert run(app, yt_fake) == "scheduled"
    assert yt_fake.sessions_started == 1             # the same session carried on
    assert "bytes */2500" in yt_fake.puts            # asked YouTube how far it had got
    with app.state.sessions() as s:
        assert s.get(QuotaDay, uploader.quota_day()).uploads == 1


def test_a_restart_carries_on_uploading(app, yt_fake):
    post_id, _ = approved_post(app)
    with app.state.sessions() as s:
        assert uploader.claim(s) == post_id
        assert uploader.requeue(s) == 1
        assert s.get(Post, post_id).status == "approved"


@pytest.mark.parametrize("privacy", ["public", "unlisted"])
def test_youtube_changing_the_privacy_fails_loudly(app, yt_fake, privacy):
    post_id, _ = approved_post(app)
    yt_fake.privacy = privacy
    events = []
    assert run(app, yt_fake, events) == "failed" and events == ["failed"]
    row = post_row(app, post_id)
    assert f"set it to {privacy} instead of private" in row.error and row.video_id == "vid12345678"


def test_a_missed_time_is_not_posted_late(app, yt_fake):
    post_id, _ = approved_post(app, minutes=30)
    publish_at = post_row(app, post_id).publish_at
    assert run(app, yt_fake, now=publish_at - timedelta(minutes=1)) == "failed"
    assert "missed its time" in post_row(app, post_id).error and yt_fake.metadata == []


def test_the_daily_upload_limit_waits_for_the_next_day(app, yt_fake):
    post_id, _ = approved_post(app)
    with app.state.sessions() as s:
        uploader.spend(s, uploads=100)
        s.commit()
    assert run(app, yt_fake) == "waiting" and yt_fake.metadata == []
    row = post_row(app, post_id)
    assert row.status == "approved" and row.next_try_at == uploader.next_quota_day() and row.attempts == 0


def test_an_expired_connection_fails_and_marks_the_channel(app, yt_fake):
    post_id, _ = approved_post(app)
    yt_fake.refresh_error = "invalid_grant"
    assert run(app, yt_fake) == "failed"
    assert "Reconnect" in post_row(app, post_id).error
    with app.state.sessions() as s:
        assert s.scalar(select(YouTubeChannel)).status == "expired"


def test_nothing_unapproved_or_changed_is_uploaded(app, yt_fake):
    post_id, _ = approved_post(app)
    with app.state.sessions() as s:
        s.get(Post, post_id).description = "something else"      # changed behind the approval's back
        s.commit()
    assert run(app, yt_fake) is None and yt_fake.metadata == []
    assert "Approve it again" in post_row(app, post_id).error

    post_id, _ = approved_post(app, clip_n=1)
    with app.state.sessions() as s:
        post = s.get(Post, post_id)
        video = lane.export_path(app.state.settings, post.clip, s.get(Render, post.render_id))
        video.write_bytes(b"a different video")
    assert run(app, yt_fake) == "failed" and yt_fake.metadata == []
    assert "changed after it was approved" in post_row(app, post_id).error


def test_youtube_refusals_are_sorted():
    def answer(status, reason=None):
        body = {"error": {"message": "nope", "errors": [{"reason": reason}]}} if reason else {}
        return httpx.Response(status, json=body)

    with pytest.raises(uploader.Retry):
        uploader.refuse(answer(503), "upload")
    with pytest.raises(uploader.Wait):
        uploader.refuse(answer(403, "quotaExceeded"), "upload")
    with pytest.raises(uploader.Wait):
        uploader.refuse(answer(400, "uploadLimitExceeded"), "upload")
    with pytest.raises(uploader.Retry):
        uploader.refuse(answer(403, "rateLimitExceeded"), "upload")
    with pytest.raises(yt.Expired):
        uploader.refuse(answer(401), "upload")
    with pytest.raises(uploader.Fail, match="nope"):
        uploader.refuse(answer(400, "invalidTitle"), "upload")


def test_google_quota_day_is_pacific():
    # 07:00 UTC on 10 Nov is 23:00 on 9 Nov in California (PST, UTC-8).
    assert uploader.quota_day(datetime(2026, 11, 10, 7, 0)) == "2026-11-09"
    assert uploader.quota_day(datetime(2026, 11, 10, 8, 30)) == "2026-11-10"
    assert uploader.next_quota_day(datetime(2026, 11, 10, 7, 0)) == datetime(2026, 11, 10, 8, 5)
    assert uploader.next_quota_day(datetime(2026, 7, 10, 12, 0)) == datetime(2026, 7, 11, 7, 5)   # summer: UTC-7


def test_messages_and_the_owner_only_quota(app):
    post = Post(id="po_1", title="1v4 clutch", video_id="vid12345678", publish_at=datetime(2026, 11, 11, 13, 30),
                error="It missed its time.")
    assert "Wed 11 Nov, 7:00 pm" in post_message(post, "scheduled", "https://x")
    assert "https://youtube.com/shorts/vid12345678" in post_message(post, "live", "https://x")
    assert "https://x/posts/po_1" in post_message(post, "failed", "https://x")
    other = client_for(app, "b@example.com")
    assert other.get("/api/posts/quota").status_code == 403
