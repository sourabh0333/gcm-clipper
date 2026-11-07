"""The Live screen's sessions and markers, and how they reach the engine."""

import base64
import json
from datetime import timedelta

import pytest
from fastapi.testclient import TestClient

from aigcm import db, media
from aigcm.api import create_app
from aigcm.api.settings import ApiSettings
from aigcm.db.models import LiveSession, Marker, Stream
from aigcm.worker import write_markers

APP = {"x-kaatclip": "1"}


@pytest.fixture
def app(tmp_path, monkeypatch):
    monkeypatch.setattr(media, "probe", lambda path: {"duration": 600.0})
    return create_app(ApiSettings(db_url=db.sqlite_url(tmp_path / "t.db"), jobs_dir=tmp_path / "jobs", dev_login=True,
                                  invites=frozenset({"a@example.com", "b@example.com"}), min_free_bytes=0))


def client_for(app, email):
    client = TestClient(app, base_url="http://localhost")
    client.post("/auth/dev-login", json={"email": email}, headers=APP)
    return client


def test_going_live_marking_undoing_and_ending(app):
    a = client_for(app, "a@example.com")
    assert a.get("/api/live").json() == {"open": None, "recent": []}
    live = a.post("/api/live", json={"title": "Rank push"}, headers=APP).json()
    for _ in range(3):
        a.post(f"/api/live/{live['id']}/markers", headers=APP)
    assert len(a.get("/api/live").json()["open"]["markers"]) == 3
    assert len(a.delete(f"/api/live/{live['id']}/markers/last", headers=APP).json()["markers"]) == 2
    ended = a.post(f"/api/live/{live['id']}/end", headers=APP).json()
    assert ended["ended_at"] and a.get("/api/live").json()["open"] is None
    assert a.post(f"/api/live/{live['id']}/markers", headers=APP).status_code == 409
    # Going live again closes any session left open.
    first = a.post("/api/live", json={}, headers=APP).json()
    second = a.post("/api/live", json={}, headers=APP).json()
    state = a.get("/api/live").json()
    assert state["open"]["id"] == second["id"] and first["id"] in [s["id"] for s in state["recent"]]


def test_someone_elses_live_session_is_out_of_reach(app):
    a, b = client_for(app, "a@example.com"), client_for(app, "b@example.com")
    live = a.post("/api/live", json={}, headers=APP).json()
    assert b.post(f"/api/live/{live['id']}/markers", headers=APP).status_code == 404
    assert b.post(f"/api/live/{live['id']}/end", headers=APP).status_code == 404


def test_an_upload_with_a_live_session_gives_the_engine_its_markers(app, tmp_path):
    a, b = client_for(app, "a@example.com"), client_for(app, "b@example.com")
    live = a.post("/api/live", json={}, headers=APP).json()
    with app.state.sessions() as s:
        session = s.get(LiveSession, live["id"])
        for minutes in (12, 47):
            s.add(Marker(user_id=session.user_id, live_session_id=session.id,
                         at=session.started_at + timedelta(minutes=minutes)))
        s.commit()
    meta = lambda sid: ",".join(f"{k} {base64.b64encode(v.encode()).decode()}" for k, v in
                                {"filename": "rec.mp4", "live_session": sid}.items())
    created = a.post("/api/uploads", headers={**APP, "upload-length": "3", "upload-metadata": meta(live["id"])})
    stolen = b.post("/api/uploads", headers={**APP, "upload-length": "3", "upload-metadata": meta(live["id"])})
    with app.state.sessions() as s:
        mine, theirs = s.get(Stream, created.headers["x-stream-id"]), s.get(Stream, stolen.headers["x-stream-id"])
        assert mine.live_session_id == live["id"] and theirs.live_session_id is None
        folder = app.state.settings.jobs_dir / mine.job_dir
        write_markers(s, mine, folder)
    markers = json.loads((folder / "markers.json").read_text())
    assert [m["t"] for m in markers] == [720.0, 2820.0] and markers[0]["source"] == "button"
