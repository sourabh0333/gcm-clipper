"""Thumbnails and cover frames (M3.7)."""

import json
import shutil
import subprocess
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from aigcm import db, titles
from aigcm.api import create_app
from aigcm.api.settings import ApiSettings
from aigcm.db.models import Render
from aigcm.manage import import_jobs
from aigcm.studio import edit as E
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


def test_cover_time_follows_the_choice_then_the_first_kill():
    edit = E.default_edit(10, 40, 1280, 720, events=[{"t": 25, "kind": "self_kill"}, {"t": 30, "kind": "self_kill"}])
    assert E.cover_time(edit) == pytest.approx(15.3)                     # the first zoomed kill, 15 s in
    assert E.cover_time(edit, intro_s=4) == pytest.approx(19.3)          # after an intro
    chosen = edit.model_copy(update={"cover_t": 12.0})
    assert E.cover_time(chosen) == pytest.approx(2.0)
    calm = E.default_edit(10, 40, 720, 1280)                              # vertical: no zooms
    assert E.cover_time(calm) == pytest.approx(12.0)                     # 40% in
    cut_out = chosen.model_copy(update={"cover_t": 99.0})                 # a frame no longer in the clip
    assert E.cover_time(cut_out) == pytest.approx(15.3)                  # back to the first kill


def test_long_titles_and_thumbnail_words():
    assert titles.stream_context("🔴 BGMI LIVE🔥SOLO VS SQUAD") == "SOLO VS SQUAD"
    assert titles.stream_context("Just chatting") == "RUSH GAMEPLAY"
    names = titles.long_titles(59, 1, "RANK PUSH", "Lulla Chhaap Likes! 😂")
    assert names[0] == "1 CHICKEN DINNER + 59 FINISHES | RANK PUSH | BGMI"
    assert names[1].startswith("Lulla Chhaap Likes!") and len(names) == 3
    assert all(len(n) <= titles.LONG_MAX for n in titles.long_titles(9, 0, "X" * 120, "y " * 80))
    assert titles.thumb_words(12, 0, ["fight", "squad_wipe"]) == ["12 FINISHES", "SQUAD WIPE"]
    assert titles.thumb_words(0, 0, []) == ["BEST MOMENTS"]


@needs_ffmpeg
def test_three_thumbnails_without_a_camera(tmp_path):
    import cv2
    from aigcm.studio import thumbs

    video = tmp_path / "v.mp4"
    subprocess.run([ffmpeg(), "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=s=640x360:r=15:d=6",
                    "-c:v", "libx264", "-preset", "ultrafast", str(video)], check=True)
    moments = [thumbs.Moment(video, 1.0, "kill", 3), thumbs.Moment(video, 4.0, "kill", 2)]
    paths = thumbs.make_set(moments, None, ["12 FINISHES", "SQUAD WIPE"], tmp_path / "out")
    assert [p.name for p in paths] == ["thumb_1.jpg", "thumb_2.jpg", "thumb_3.jpg"]
    images = [cv2.imread(str(p)) for p in paths]
    assert all(i.shape == (720, 1280, 3) for i in images)
    assert abs(images[0].astype(int) - images[2].astype(int)).mean() > 5     # words and zoom make them differ
    with pytest.raises(RuntimeError):
        thumbs.make_set([thumbs.Moment(tmp_path / "missing.mp4", 1, "kill")], None, ["X"], tmp_path / "none")


@pytest.fixture
def app(tmp_path):
    jobs = tmp_path / "jobs"
    shutil.copytree(DEMO, jobs, ignore=shutil.ignore_patterns("decisions.json", "run.log"))
    folder = jobs / "demo-finished"
    (folder / "vision.json").write_text(json.dumps({"events": [
        {"t": 289.5, "kind": "self_kill"}, {"t": 293.0, "kind": "self_kill"}, {"t": 1158.0, "kind": "self_kill"},
        {"t": 1300.0, "kind": "dinner"}]}))     # vision.py's name for a chicken dinner
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


@needs_ffmpeg
def test_stream_thumbnails_through_the_api(app):
    folder = app.state.settings.jobs_dir / "demo-finished"
    subprocess.run([ffmpeg(), "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=s=640x360:r=10:d=1400",
                    "-c:v", "libx264", "-preset", "ultrafast", "-g", "20", str(folder / "source.mp4")], check=True)
    owner = client_for(app, "owner@example.com")
    stream = next(s for s in owner.get("/api/streams").json() if s["status"] == "done")
    url = f"/api/streams/{stream['id']}/thumbnails"
    assert owner.get(url).json() == {"status": "none"}
    queued = owner.post(url, headers=APP).json()
    assert queued["status"] == "queued" and owner.post(url, headers=APP).json()["id"] == queued["id"]
    Worker(app.state.settings).render_step()
    done = owner.get(url).json()
    assert done["status"] == "done", done
    assert len(done["images"]) == 3 and len(done["titles"]) == 3
    assert done["titles"][0].startswith("1 CHICKEN DINNER + 3 FINISHES")
    image = owner.get(done["images"][0])
    assert image.status_code == 200 and image.headers["content-type"] == "image/jpeg"
    other = client_for(app, "b@example.com")
    assert other.get(url).status_code == 404 and other.get(done["images"][0]).status_code == 404


def test_thumbnails_wait_for_the_clips(app):
    owner = client_for(app, "owner@example.com")
    failed = next(s for s in owner.get("/api/streams").json() if s["status"] == "failed")
    assert owner.post(f"/api/streams/{failed['id']}/thumbnails", headers=APP).status_code == 409
