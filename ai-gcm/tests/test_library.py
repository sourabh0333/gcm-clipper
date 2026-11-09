"""The library (M3.2): filters, search by what was said, paging, posters, and only the creator's own clips."""

import json
import shutil
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from aigcm import db
from aigcm.api import create_app
from aigcm.api.settings import ApiSettings
from aigcm.db.models import Clip, Edit, Render, Stream, User, new_id
from aigcm.manage import backfill_library, import_jobs
from aigcm.worker import Worker

DEMO = Path(__file__).resolve().parent.parent / "demo"
APP = {"x-kaatclip": "1"}

# Demo clips: 277.5-305.5 multi_kill, 1146-1165 fight, 622-640 fight, and a reaction.
TRANSCRIPT = {"segments": [
    {"start": 280.0, "end": 284.0, "text": " Bhai ek aur gaya, full rush!"},
    {"start": 1150.0, "end": 1152.0, "text": "Zone mein aao jaldi"},
    {"start": 5000.0, "end": 5001.0, "text": "elsewhere"},
]}


def ffmpeg_available():
    try:
        from aigcm.media import tool
        return bool(tool("ffmpeg"))
    except RuntimeError:
        return False


@pytest.fixture
def app(tmp_path):
    jobs = tmp_path / "jobs"
    shutil.copytree(DEMO, jobs, ignore=shutil.ignore_patterns("decisions.json", "run.log"))
    (jobs / "demo-finished" / "transcript.json").write_text(json.dumps(TRANSCRIPT))
    settings = ApiSettings(db_url=db.sqlite_url(tmp_path / "t.db"), jobs_dir=jobs, dev_login=True,
                           invites=frozenset({"owner@example.com", "b@example.com"}), min_free_bytes=0)
    app = create_app(settings)
    with app.state.sessions() as s:
        import_jobs(s, settings, "owner@example.com")
    return app


def client_for(app, email):
    client = TestClient(app, base_url="http://localhost")
    client.post("/auth/dev-login", json={"email": email}, headers=APP)
    return client


def test_import_stores_what_was_said_and_queues_posters(app):
    with app.state.sessions() as s:
        clips = {c.clip_key: c.spoken for c in s.query(Clip)}
        assert clips["m01"] == "Bhai ek aur gaya, full rush!" and clips["m02"] == "Zone mein aao jaldi"
        assert s.query(Render).filter_by(kind="posters").count() == 1


def test_filters_search_and_paging(app):
    owner = client_for(app, "owner@example.com")
    everything = owner.get("/api/library").json()
    assert everything["total"] == 4 and len(everything["items"]) == 4
    first = everything["items"][0]
    assert first["stream_title"] and first["edited"] is False and first["exported"] is False
    assert everything["facets"]["streams"][0]["count"] == 4
    assert {t["type"] for t in everything["facets"]["types"]} == {"multi_kill", "fight", "reaction"}

    def keys(**params):
        return [c["rank"] for c in owner.get("/api/library", params=params).json()["items"]]

    assert keys(q="RUSH bhai") == [1]               # every word, any case
    assert keys(q="zone") == [2]
    assert keys(q="nothing like this") == []
    assert keys(q="100%_") == []                    # wildcards are taken literally
    assert keys(type="fight") == [2, 3]
    assert keys(sort="score")[0] == 1
    page = owner.get("/api/library", params={"limit": 3, "offset": 3}).json()
    assert page["total"] == 4 and len(page["items"]) == 1

    clip_id = everything["items"][1]["id"]
    owner.post(f"/api/clips/{clip_id}/decision", json={"verdict": "keep"}, headers=APP)
    assert keys(decision="keep") == [2] and len(keys(decision="none")) == 3
    with app.state.sessions() as s:
        clip = s.get(Clip, clip_id)
        s.add(Edit(clip_id=clip.id, version=1, data={}))
        s.add(Render(user_id=clip.stream.user_id, clip_id=clip.id, kind="export", status="done"))
        clip.details = dict(clip.details, flags=[{"kind": "profanity"}])
        s.commit()
    assert keys(edited=True) == [2] and keys(exported=True) == [2] and keys(flag=True) == [2]


def test_only_your_own_clips(app):
    with app.state.sessions() as s:
        other = User(email="b@example.com")
        s.add(other)
        s.flush()
        stream = Stream(id=new_id("st"), job_dir="elsewhere", user_id=other.id, title="B's stream", status="done")
        s.add(stream)
        s.add(Clip(stream_id=stream.id, clip_key="m01", rank=1, start_s=0, end_s=10, type="fight",
                   file_name="x.mp4", spoken="bhai"))
        s.commit()
    b = client_for(app, "b@example.com")
    mine = b.get("/api/library").json()
    assert mine["total"] == 1 and mine["items"][0]["stream_title"] == "B's stream"
    assert [s["title"] for s in mine["facets"]["streams"]] == ["B's stream"]
    owner = client_for(app, "owner@example.com")
    assert owner.get("/api/library", params={"q": "bhai"}).json()["total"] == 1
    assert b.get(f"/media/posters/{owner.get('/api/library').json()['items'][0]['id']}").status_code == 404


@pytest.mark.skipif(not ffmpeg_available(), reason="ffmpeg is not installed")
def test_posters_are_made_by_the_worker_and_served(app):
    worker = Worker(app.state.settings)
    owner = client_for(app, "owner@example.com")
    assert all(c["poster"] is None for c in owner.get("/api/library").json()["items"])
    assert worker.render_step() and not worker.render_step()
    items = owner.get("/api/library").json()["items"]
    assert all(c["poster"] for c in items)
    image = owner.get(items[0]["poster"])
    assert image.status_code == 200 and image.headers["content-type"] == "image/jpeg"
    assert image.content[:2] == b"\xff\xd8" and len(image.content) < 60_000
    # The backfill only queues work again; posters that exist are skipped by the worker.
    with app.state.sessions() as s:
        assert backfill_library(s, app.state.settings) == (0, 1)
    worker.render_step()
    assert all(c["poster"] for c in owner.get("/api/library").json()["items"])
