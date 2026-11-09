"""Studio (M3.1): the edit list, working windows, the renderer and the render lane, end to end through the
API on a small generated source video."""

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
from aigcm.studio import edit as E
from aigcm.studio import window as W
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


# --- the edit list ---------------------------------------------------------------------------------------

def test_default_edit_keeps_vertical_streams_and_zooms_landscape_kills():
    events = [{"t": 20.0, "kind": "self_kill"}, {"t": 21.0, "kind": "self_kill"}, {"t": 30.0, "kind": "self_kill"},
              {"t": 25.0, "kind": "accolade"}, {"t": 90.0, "kind": "self_kill"}]
    vertical = E.default_edit(10, 40, 720, 1280, "3 FINISHES", events, captions=True)
    assert vertical.layout.template == "native" and vertical.zooms == []
    assert vertical.layout.panels[0].dst == (0, 0, 1080, 1920) and vertical.captions.on
    landscape = E.default_edit(10, 40, 1920, 1080, "3 FINISHES", events)
    assert landscape.layout.template == "blur"
    assert landscape.layout.panels[0].dst == (0, 656, 1080, 608)
    assert [z.t for z in landscape.zooms] == [20.0, 30.0]   # 21 s shares the first zoom; 90 s is outside
    assert landscape.hook.text == "3 FINISHES" and not landscape.hook.on
    clipped = E.default_edit(10, 40, 1920, 1080, window=(15.0, 35.0))
    assert (clipped.segments[0].start, clipped.segments[0].end) == (15.0, 35.0)


def test_split_layout_needs_a_facecam_box():
    assert E.template_layout("split", 1920, 1080).template == "blur"
    split = E.template_layout("split", 1920, 1080, facecam=(0.7, 0.05, 0.25, 0.3))
    assert [p.role for p in split.panels] == ["cam", "game"] and split.panels[0].dst == (0, 0, 1080, 760)


def test_edit_validation():
    layout = E.template_layout("blur", 1920, 1080).model_dump()
    good = {"segments": [{"start": 10, "end": 20}, {"start": 25, "end": 40, "speed": 2}], "layout": layout}
    assert E.output_length(E.EditData.model_validate(good).segments) == pytest.approx(17.5)
    bad = [
        {"segments": [{"start": 10, "end": 20}, {"start": 15, "end": 30}], "layout": layout},   # overlap
        {"segments": [{"start": 0, "end": 200}], "layout": layout},                              # too long
        {"segments": [{"start": 10, "end": 10.1}], "layout": layout},                            # too short
        {"segments": [{"start": 10, "end": 20, "speed": 8}], "layout": layout},                  # too fast
        {"segments": [{"start": 10, "end": 20}], "layout": dict(layout, panels=[
            {"role": "game", "src": [0.5, 0, 0.8, 1], "dst": [0, 0, 1080, 608]}])},              # crop outside
        {"segments": [{"start": 10, "end": 20}], "layout": dict(layout, panels=[
            {"role": "game", "src": [0, 0, 1, 1], "dst": [0, 1800, 1080, 608]}])},               # off the canvas
        dict(good, extra=1),
    ]
    for data in bad:
        with pytest.raises(ValueError):
            E.EditData.model_validate(data)
    edit = E.EditData.model_validate(good)
    with pytest.raises(ValueError):
        E.check_window(edit, 12, 60)
    E.check_window(edit, 10, 40)


def test_time_mapping_through_cuts_and_speed():
    segs = [E.Segment(start=10, end=20), E.Segment(start=30, end=40, speed=2)]
    assert E.to_output(segs, 15) == 5 and E.to_output(segs, 25) is None and E.to_output(segs, 34) == 12
    assert E.span_to_output(segs, 18, 32) == [(8.0, 10.0), (10.0, 11.0)]


# --- working windows -------------------------------------------------------------------------------------

def test_window_covers_context_and_the_whole_fight_within_the_cap():
    assert W.plan_window(100, 130, 1000) == (40, 190)
    assert W.plan_window(20, 40, 70) == (0, 70)
    events = [{"t": t, "kind": "self_kill"} for t in (30, 55, 80, 110, 120, 170, 400)]
    assert W.fight_span(events, 100, 130) == (30, 120)     # 170 is 50 s later: another fight
    assert W.plan_window(100, 130, 1000, events) == (15, 190)
    long = [{"t": t, "kind": "self_kill"} for t in range(0, 600, 20)]
    a, b = W.plan_window(300, 330, 1000, long)
    assert b - a == pytest.approx(W.MAX_WINDOW_S) and a < 300 and b > 330


# --- end to end ------------------------------------------------------------------------------------------

def make_source(path, seconds=400):
    """A vertical test video with keyframes every 2 s and a tone, like a phone stream but tiny."""
    subprocess.run([ffmpeg(), "-v", "error", "-y", "-f", "lavfi", "-i", f"testsrc2=s=360x640:r=15:d={seconds}",
                    "-f", "lavfi", "-i", f"sine=f=440:d={seconds}", "-c:v", "libx264", "-preset", "ultrafast",
                    "-g", "30", "-c:a", "aac", "-shortest", str(path)], check=True)


@pytest.fixture
def studio_app(tmp_path):
    jobs = tmp_path / "jobs"
    shutil.copytree(DEMO, jobs, ignore=shutil.ignore_patterns("decisions.json", "run.log"))
    settings = ApiSettings(db_url=db.sqlite_url(tmp_path / "t.db"), jobs_dir=jobs, dev_login=True,
                           invites=frozenset({"owner@example.com", "b@example.com"}), min_free_bytes=0)
    app = create_app(settings)
    with app.state.sessions() as s:
        import_jobs(s, settings, "owner@example.com")
        s.query(Render).filter_by(kind="posters").delete()   # library posters are tested in test_library
        s.commit()
    return app


def client_for(app, email):
    client = TestClient(app, base_url="http://localhost")
    client.post("/auth/dev-login", json={"email": email}, headers=APP)
    return client


def first_clip(client):
    stream = next(s for s in client.get("/api/streams").json() if s["status"] == "done")
    return client.get(f"/api/streams/{stream['id']}/clips").json()[0]


def test_without_a_recording_a_clip_cannot_be_edited(studio_app):
    owner = client_for(studio_app, "owner@example.com")
    clip = first_clip(owner)
    view = owner.get(f"/api/clips/{clip['id']}/studio").json()
    assert view["window"]["status"] == "missing" and view["edit"]["version"] == 0
    assert view["edit"]["data"]["layout"]["template"] == "native"    # the demo stream is vertical
    assert owner.post(f"/api/clips/{clip['id']}/prepare", headers=APP).status_code == 409
    assert owner.post(f"/api/clips/{clip['id']}/export", json={}, headers=APP).status_code == 409
    other = client_for(studio_app, "b@example.com")
    assert other.get(f"/api/clips/{clip['id']}/studio").status_code == 404


@needs_ffmpeg
def test_keep_prepare_edit_and_export(studio_app):
    settings = studio_app.state.settings
    make_source(settings.jobs_dir / "demo-finished" / "source.mp4")
    worker = Worker(settings)
    owner = client_for(studio_app, "owner@example.com")
    clip = first_clip(owner)   # 277.5-305.5 s, kills at 289.5, 293 and 299.5
    url = f"/api/clips/{clip['id']}"

    # Keeping the clip queues its working window; the render lane makes it.
    assert owner.get(f"{url}/studio").json()["window"]["status"] == "none"
    owner.post(f"{url}/decision", json={"verdict": "keep"}, headers=APP)
    assert owner.get(f"{url}/studio").json()["window"]["status"] == "preparing"
    owner.post(f"{url}/decision", json={"verdict": "keep"}, headers=APP)    # no second prepare queued
    with studio_app.state.sessions() as s:
        assert s.query(Render).filter_by(kind="prepare").count() == 1
    assert worker.render_step() and not worker.render_step()
    view = owner.get(f"{url}/studio").json()
    win = view["window"]
    assert win["status"] == "ready" and win["start"] <= 277.5 - 55 and win["end"] >= 305.5 + 55
    assert win["width"] == 360 and win["height"] == 640 and win["has_audio"]
    for name in ("preview", "wave"):
        assert owner.get(win[name]).status_code == 200
    assert owner.get(win["strip"]["url"]).headers["content-type"] == "image/jpeg"
    assert client_for(studio_app, "b@example.com").get(win["preview"]).status_code == 404

    # Save an edit: two parts, the second sped up.
    data = view["edit"]["data"]
    data["segments"] = [{"start": 280, "end": 290, "speed": 1}, {"start": 295, "end": 305, "speed": 2}]
    saved = owner.put(f"{url}/edit", json={"base_version": 0, "data": data}, headers=APP)
    assert saved.status_code == 200 and saved.json()["version"] == 1 and saved.json()["length_s"] == 15
    stale = owner.put(f"{url}/edit", json={"base_version": 0, "data": data}, headers=APP)
    assert stale.status_code == 409
    outside = dict(data, segments=[{"start": 1, "end": 20, "speed": 1}])
    assert owner.put(f"{url}/edit", json={"base_version": 1, "data": outside}, headers=APP).status_code == 422
    assert owner.get(f"{url}/studio").json()["edit"]["version"] == 1

    # Export it; asking again returns the same export.
    queued = owner.post(f"{url}/export", json={}, headers=APP).json()
    assert queued["status"] == "queued" and queued["version"] == 1
    assert owner.post(f"{url}/export", json={}, headers=APP).json()["id"] == queued["id"]
    assert worker.render_step() == queued["id"]
    done = owner.get(f"/api/renders/{queued['id']}").json()
    assert done["status"] == "done" and done["video"]
    video = owner.get(done["video"])
    assert video.status_code == 200 and video.headers["content-type"] == "video/mp4"
    assert client_for(studio_app, "b@example.com").get(done["video"]).status_code == 404
    out = next((settings.jobs_dir / "demo-finished" / "exports").glob("*.mp4"))
    from aigcm.media import probe
    info = probe(out)
    assert (info["width"], info["height"]) == (1080, 1920)
    assert info["duration"] == pytest.approx(15, abs=0.15)

    # The default edit exports too (version 0), and a re-run of the job keeps the clip's edits.
    default = owner.post(f"{url}/export", json={"version": 0}, headers=APP).json()
    worker.render_step()
    assert owner.get(f"/api/renders/{default['id']}").json()["status"] == "done"
    from aigcm.worker import import_clips
    from aigcm.db.models import Stream
    with studio_app.state.sessions() as s:
        stream = s.get(Stream, clip["stream_id"])
        import_clips(s, stream, settings.jobs_dir / stream.job_dir)
        s.commit()
    assert owner.get(f"{url}/studio").json()["edit"]["version"] == 1


@needs_ffmpeg
def test_a_failed_render_is_recorded_and_the_lane_goes_on(studio_app):
    settings = studio_app.state.settings
    worker = Worker(settings)
    owner = client_for(studio_app, "owner@example.com")
    clip = first_clip(owner)
    source = settings.jobs_dir / "demo-finished" / "source.mp4"
    source.write_bytes(b"not a video")
    owner.post(f"/api/clips/{clip['id']}/decision", json={"verdict": "keep"}, headers=APP)
    assert worker.render_step()
    view = owner.get(f"/api/clips/{clip['id']}/studio").json()["window"]
    assert view["status"] == "failed" and view["error"]
    # Asking again queues a new attempt.
    assert owner.post(f"/api/clips/{clip['id']}/prepare", headers=APP).json()["status"] == "preparing"


def test_prepare_kept_queues_only_clips_that_need_footage(studio_app):
    from aigcm.manage import prepare_kept

    settings = studio_app.state.settings
    with studio_app.state.sessions() as s:
        assert prepare_kept(s, settings) == 0          # the demo stream has no recording on disk
    (settings.jobs_dir / "demo-finished" / "source.mp4").write_bytes(b"x")
    owner = client_for(studio_app, "owner@example.com")
    kept = first_clip(owner)
    owner.post(f"/api/clips/{kept['id']}/decision", json={"verdict": "keep"}, headers=APP)   # queues one
    with studio_app.state.sessions() as s:
        assert prepare_kept(s, settings) == 1          # the same clip, already queued: no second render
        assert s.query(Render).filter_by(kind="prepare").count() == 1
