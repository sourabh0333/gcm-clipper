"""Reviewing clips through the API, and importing the job folders made before the platform."""

import json
import shutil
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from aigcm import db
from aigcm.api import create_app
from aigcm.api.settings import ApiSettings
from aigcm.db.models import Stream
from aigcm.manage import import_jobs

DEMO = Path(__file__).resolve().parent.parent / "demo"
APP = {"x-kaatclip": "1"}


@pytest.fixture
def app(tmp_path):
    jobs = tmp_path / "jobs"
    shutil.copytree(DEMO, jobs, ignore=shutil.ignore_patterns("decisions.json", "run.log"))
    (jobs / "demo-finished" / "decisions.json").write_text(json.dumps(
        {"m01": {"verdict": "keep", "reason": "", "at": "2026-11-05T10:00:00"},
         "m03": {"verdict": "reject", "reason": "bad cut", "at": "2026-11-05T10:01:00"}}))
    settings = ApiSettings(db_url=db.sqlite_url(tmp_path / "t.db"), jobs_dir=jobs, dev_login=True,
                           invites=frozenset({"owner@example.com", "b@example.com"}),
                           admins=frozenset({"owner@example.com"}))
    app = create_app(settings)
    with app.state.sessions() as s:
        assert sorted(import_jobs(s, settings, "Owner@Example.com")) == ["demo-failed", "demo-finished", "demo-processing"]
    return app


def client_for(app, email):
    client = TestClient(app, base_url="http://localhost")
    client.post("/auth/dev-login", json={"email": email}, headers=APP)
    return client


def finished(client):
    return next(s for s in client.get("/api/streams").json() if s["status"] == "done")


def test_import_brings_folders_clips_and_swipes_and_runs_once(app):
    owner = client_for(app, "owner@example.com")
    streams = {s["status"] for s in owner.get("/api/streams").json()}
    assert streams == {"done", "stopped", "failed"}
    done = finished(owner)
    assert done["clips"] == 4 and done["kept"] == 1 and done["reviewed"] == 2
    clips = owner.get(f"/api/streams/{done['id']}/clips").json()
    assert [c["decision"] for c in clips] == ["keep", None, "reject", None]
    assert clips[0]["video"] == f"/media/clips/{clips[0]['id']}" and clips[0]["length_s"] > 0
    failed = next(s for s in owner.get("/api/streams").json() if s["status"] == "failed")
    assert failed["error"]
    with app.state.sessions() as s:
        assert import_jobs(s, app.state.settings, "owner@example.com") == []
        assert s.query(Stream).count() == 3


def test_keep_reject_with_a_reason_and_undo(app):
    owner = client_for(app, "owner@example.com")
    clip = owner.get(f"/api/streams/{finished(owner)['id']}/clips").json()[1]
    url = f"/api/clips/{clip['id']}/decision"
    rejected = owner.post(url, json={"verdict": "reject", "reason": "not_interesting"}, headers=APP).json()
    assert rejected["decision"] == "reject" and rejected["reason"] == "not_interesting"
    kept = owner.post(url, json={"verdict": "keep", "reason": "not_interesting"}, headers=APP).json()
    assert kept["decision"] == "keep" and kept["reason"] is None
    assert owner.post(url, json={"verdict": None}, headers=APP).json()["decision"] is None
    assert owner.post(url, json={"verdict": "maybe"}, headers=APP).status_code == 400
    weird = owner.post(url, json={"verdict": "reject", "reason": "<script>"}, headers=APP).json()
    assert weird["reason"] is None


def test_the_kept_list_spans_streams(app):
    owner = client_for(app, "owner@example.com")
    kept = owner.get("/api/clips", params={"decision": "keep"}).json()
    assert len(kept) == 1 and kept[0]["decision"] == "keep" and kept[0]["stream_title"]
    assert len(owner.get("/api/clips").json()) == 4
    assert len(owner.get("/api/clips", params={"decision": "none"}).json()) == 2


def test_videos_stream_in_ranges_and_download(app):
    owner = client_for(app, "owner@example.com")
    clip = owner.get(f"/api/streams/{finished(owner)['id']}/clips").json()[0]
    full = owner.get(clip["video"])
    assert full.status_code == 200 and full.headers["content-type"] == "video/mp4" and len(full.content) > 1000
    part = owner.get(clip["video"], headers={"range": "bytes=0-99"})
    assert part.status_code == 206 and len(part.content) == 100
    assert part.headers["content-range"].startswith("bytes 0-99/")
    download = owner.get(clip["video"], params={"download": 1})
    assert download.headers["content-disposition"].startswith("attachment")
    assert owner.get(clip["video"], params={"safe": 1}).status_code == 404   # no sponsor-safe copy


def test_nobody_else_sees_clips_or_videos(app):
    owner, other = client_for(app, "owner@example.com"), client_for(app, "b@example.com")
    done = finished(owner)
    clip = owner.get(f"/api/streams/{done['id']}/clips").json()[0]
    assert other.get(f"/api/streams/{done['id']}/clips").status_code == 404
    assert other.get(clip["video"]).status_code == 404
    assert other.post(f"/api/clips/{clip['id']}/decision", json={"verdict": "reject"}, headers=APP).status_code == 404
    assert other.get("/api/clips").json() == []
    assert TestClient(app).get(clip["video"]).status_code == 401


def test_a_missing_video_file_says_so(app):
    owner = client_for(app, "owner@example.com")
    done = finished(owner)
    clip = owner.get(f"/api/streams/{done['id']}/clips").json()[0]
    with app.state.sessions() as s:
        folder = app.state.settings.jobs_dir / s.get(Stream, done["id"]).job_dir / "clips"
    for f in folder.iterdir():
        f.unlink()
    response = owner.get(clip["video"])
    assert response.status_code == 404 and "no longer on the laptop" in response.json()["detail"]
