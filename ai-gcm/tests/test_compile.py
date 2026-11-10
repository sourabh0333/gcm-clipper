"""The weekly compilation (M3.8): picking, ordering, chapters, both formats, and the API."""

import json
import shutil
import subprocess
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from aigcm import db
from aigcm.api import create_app
from aigcm.api.settings import ApiSettings
from aigcm.db.models import Render
from aigcm.manage import import_jobs
from aigcm.studio import compile as C
from aigcm.worker import Worker

DEMO = Path(__file__).resolve().parent.parent / "demo"
APP = {"x-kaatclip": "1"}


def ffmpeg():
    try:
        from aigcm.media import tool
        return tool("ffmpeg")
    except RuntimeError:
        return None


needs_ffmpeg = pytest.mark.skipif(ffmpeg() is None, reason="ffmpeg is not installed")


def piece(i, talk=False, length=60.0, job="a"):
    return C.Piece(i, f"P{i}", "v.mp4", 0.0, 100.0 * i, 100.0 * i + length, talk, "st", job, 0 if talk else 2)


def test_chapters_start_at_zero_and_follow_the_pieces():
    pieces = [piece(1), piece(2, talk=True, length=25), piece(3, length=3700)]
    assert C.chapters(pieces) == ["0:00 P1", "1:00 P2", "1:25 P3"]
    longer = [piece(1, length=3600), piece(2)]
    assert C.chapters(longer)[1] == "1:00:00 P2"


def test_the_best_fight_closes_and_untitled_clips_get_names():
    pieces = [piece(1), piece(2), piece(3, talk=True), piece(4)]
    assert [p.clip_id for p in C.finale(pieces)] == [2, 3, 4, 1]
    assert [p.clip_id for p in C.finale(pieces[:2])] == [1, 2]
    assert C.fallback_title("fight", 3, False) == "3 FINISHES" and C.fallback_title("fight", 1, False) == "1 FINISH"
    assert C.fallback_title("funny", 0, True, "haan bhai ye dekho kya hua yaar sach") == "haan bhai ye dekho kya hua"
    assert C.fallback_title("banter", 0, True) == "Banter"


@pytest.fixture
def app(tmp_path):
    jobs = tmp_path / "jobs"
    shutil.copytree(DEMO, jobs, ignore=shutil.ignore_patterns("decisions.json", "run.log"))
    folder = jobs / "demo-finished"
    (folder / "vision.json").write_text(json.dumps({"events": [
        {"t": 289.5, "kind": "self_kill"}, {"t": 293.0, "kind": "self_kill"}, {"t": 299.5, "kind": "self_kill"},
        {"t": 1158.0, "kind": "self_kill"}, {"t": 634.0, "kind": "self_kill"}]}))
    (folder / "transcript.json").write_text(json.dumps({"segments": [{"start": 900, "end": 1300, "words": [
        {"start": 1101.0, "end": 1101.5, "word": "bhai"}, {"start": 1101.6, "end": 1102.0, "word": "kya"}]}]}))
    settings = ApiSettings(db_url=db.sqlite_url(tmp_path / "t.db"), jobs_dir=jobs, dev_login=True,
                           invites=frozenset({"owner@example.com", "b@example.com"}), min_free_bytes=0)
    app = create_app(settings)
    with app.state.sessions() as s:
        import_jobs(s, settings, "owner@example.com")
        s.query(Render).filter_by(kind="posters").delete()
        s.commit()
    return app


def client_for(app, email):
    client = TestClient(app, base_url="http://localhost")
    client.post("/auth/dev-login", json={"email": email}, headers=APP)
    return client


def test_no_footage_no_suggestion(app):
    owner = client_for(app, "owner@example.com")
    got = owner.get("/api/compilations/suggest").json()
    assert got["pieces"] == [] and got["total_s"] == 0
    stream = next(s for s in owner.get("/api/streams").json() if s["status"] == "done")
    ids = [c["id"] for c in owner.get(f"/api/streams/{stream['id']}/clips").json()][:2]
    assert owner.post("/api/compilations", json={"clip_ids": ids}, headers=APP).status_code == 409
    assert client_for(app, "b@example.com").post("/api/compilations", json={"clip_ids": ids}, headers=APP).status_code == 404


def make_source(app, seconds=1400):
    folder = app.state.settings.jobs_dir / "demo-finished"
    subprocess.run([ffmpeg(), "-v", "error", "-y", "-f", "lavfi", "-i", f"testsrc2=s=640x360:r=10:d={seconds}",
                    "-f", "lavfi", "-i", f"sine=d={seconds}", "-c:v", "libx264", "-preset", "ultrafast", "-g", "20",
                    "-c:a", "aac", "-shortest", str(folder / "source.mp4")], check=True)
    info = json.loads((folder / "info.json").read_text())
    info["duration"] = seconds
    (folder / "info.json").write_text(json.dumps(info))


@needs_ffmpeg
@pytest.mark.parametrize("fmt", ["wide", "short"])
def test_a_compilation_end_to_end(app, fmt):
    from aigcm.media import probe

    make_source(app)
    owner = client_for(app, "owner@example.com")
    suggestion = owner.get("/api/compilations/suggest", params={"format": fmt}).json()
    chosen = [p for p in suggestion["pieces"] if p["chosen"]]
    assert len(chosen) == 4 and any(p["talk"] for p in chosen)          # the demo's reaction clip is talk
    assert chosen[-1]["kills"] == max(p["kills"] for p in chosen)        # the best fight closes it
    ids = [p["clip_id"] for p in chosen]
    if fmt == "short":
        assert all(p["length_s"] <= 30 for p in chosen) and suggestion["total_s"] <= C.SHORT_MAX_S
    job = owner.post("/api/compilations", json={"clip_ids": ids, "format": fmt}, headers=APP).json()
    assert job["status"] == "queued"
    Worker(app.state.settings).render_step()
    made = owner.get("/api/compilations").json()[0]
    assert made["status"] == "done", made
    assert len(made["titles"]) == 3 and len(made["thumbnails"]) == 3
    assert made["chapters"][0].startswith("0:00 ") and "Chapters:\n0:00" in made["description"]
    assert "KRAFTON" in made["description"]
    video = owner.get(made["video"])
    assert video.status_code == 200 and video.headers["content-type"] == "video/mp4"
    folder = app.state.settings.jobs_dir / "_compilations" / "1" / made["id"]
    info = probe(folder / "video.mp4")
    assert (info["width"], info["height"]) == ((1920, 1080) if fmt == "wide" else (1080, 1920))
    assert info["has_audio"] and info["duration"] == pytest.approx(made["length_s"], abs=1.0)
    assert not list(folder.glob("part_*.mp4"))                            # the pieces are cleaned up
    other = client_for(app, "b@example.com")
    assert other.get(made["video"]).status_code == 404
    assert other.delete(f"/api/compilations/{made['id']}", headers=APP).status_code == 404
    assert owner.delete(f"/api/compilations/{made['id']}", headers=APP).status_code == 204
    assert not folder.exists() and owner.get("/api/compilations").json() == []


def test_too_long_is_refused(app, monkeypatch):
    owner = client_for(app, "owner@example.com")
    stream = next(s for s in owner.get("/api/streams").json() if s["status"] == "done")
    ids = [c["id"] for c in owner.get(f"/api/streams/{stream['id']}/clips").json()][:2]
    monkeypatch.setattr(C, "piece_for", lambda settings, clip, short=False: piece(clip.id, length=200))
    assert owner.post("/api/compilations", json={"clip_ids": ids, "format": "short"}, headers=APP).status_code == 422
