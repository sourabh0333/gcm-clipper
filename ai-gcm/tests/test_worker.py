"""The worker, with fake engine commands standing in for the real pipeline."""

import json
import sys
import threading
import time

import pytest
from fastapi.testclient import TestClient

from aigcm import db
from aigcm.api import create_app
from aigcm.api.settings import ApiSettings
from aigcm.db.models import Stream, User, new_id, utcnow
from aigcm.worker import Worker, claim_next, import_clips, requeue_interrupted

APP = {"x-kaatclip": "1"}

FINISH = r"""
import json, sys, pathlib
folder = pathlib.Path(sys.argv[1])
(folder / "clips").mkdir(exist_ok=True)
ranked = [{"id": "m01", "rank": 1, "start": 10.0, "end": 40.0, "type": "multi_kill", "final_score": 90,
           "title": "3 FINISHES 1 FIGHT", "why": "3 kills by the streamer at 0:00:20", "titles": ["a"],
           "labels": {"kills": 3}, "flags": [], "hashtags": ["#bgmi"], "mute_spans": [[12, 13]]},
          {"id": "m02", "rank": 2, "start": 100.0, "end": 130.0, "type": "funny", "final_score": 70,
           "title": "Yaar ye kya", "why": "laughing at 0:01:50"}]
files = {"m01": "01_multi_kill_m01.mp4", "m01_safe": "01_multi_kill_m01_safe.mp4", "m02": "02_funny_m02.mp4"}
for name in files.values():
    (folder / "clips" / name).write_bytes(b"mp4")
(folder / "ranked.json").write_text(json.dumps(ranked))
(folder / "clips.json").write_text(json.dumps(files))
(folder / "manifest.json").write_text(json.dumps({"stages": {s: {"status": "done"} for s in
    ["ingest", "vision", "audio", "sounds", "transcript", "moments", "judge", "captions", "render", "review"]}}))
print("review: done")
"""

FAIL = r"""
import json, sys, pathlib
folder = pathlib.Path(sys.argv[1])
(folder / "manifest.json").write_text(json.dumps({"stages": {"ingest": {"status": "done"},
    "vision": {"status": "failed", "error": "RuntimeError('ffmpeg failed (1)')"}}}))
sys.exit(1)
"""

SLOW = "import time\nprint('vision: 1 min scanned', flush=True)\ntime.sleep(120)\n"


def fake(script):
    return lambda stream, folder: [sys.executable, "-c", script, str(folder)]


@pytest.fixture
def settings(tmp_path):
    return ApiSettings(db_url=db.sqlite_url(tmp_path / "t.db"), jobs_dir=tmp_path / "jobs", dev_login=True,
                       invites=frozenset({"a@example.com"}))


def add_stream(worker, status="queued", source=True, email="a@example.com", queued_offset=0):
    with worker.sessions() as s:
        user = s.query(User).filter_by(email=email).first() or User(email=email)
        s.add(user)
        s.flush()
        stream_id = new_id("st")
        stream = Stream(id=stream_id, job_dir=stream_id, user_id=user.id, title="Stream", status=status,
                        queued_at=utcnow())
        s.add(stream)
        s.commit()
        folder = worker.settings.jobs_dir / stream.job_dir
        folder.mkdir(parents=True)
        if source:
            (folder / "source.mp4").write_bytes(b"video")
        return stream.id


def test_a_finished_job_brings_its_clips_into_the_database(settings):
    worker = Worker(settings, command=fake(FINISH))
    stream_id = add_stream(worker)
    assert worker.step() == stream_id
    with worker.sessions() as s:
        stream = s.get(Stream, stream_id)
        assert stream.status == "done" and stream.error is None and stream.finished_at
        clips = stream.clips
        assert [c.clip_key for c in clips] == ["m01", "m02"]
        assert clips[0].safe_file_name == "01_multi_kill_m01_safe.mp4" and clips[1].safe_file_name is None
        assert clips[0].details["labels"] == {"kills": 3} and clips[0].why.startswith("3 kills")
    log = (settings.jobs_dir / stream_id / "run.log").read_text(encoding="utf-8")
    assert "started by the worker" in log and "review: done" in log
    assert worker.step() is None   # queue empty


def test_a_failed_job_records_why(settings):
    worker = Worker(settings, command=fake(FAIL))
    stream_id = add_stream(worker)
    worker.step()
    with worker.sessions() as s:
        stream = s.get(Stream, stream_id)
        assert stream.status == "failed" and stream.error.startswith("vision: RuntimeError('ffmpeg failed")


def test_stop_kills_the_running_job_within_seconds(settings):
    worker = Worker(settings, command=fake(SLOW))
    stream_id = add_stream(worker)
    runner = threading.Thread(target=worker.step)
    runner.start()
    time.sleep(2.5)
    with worker.sessions() as s:
        assert s.get(Stream, stream_id).status == "running"
        s.get(Stream, stream_id).stop_requested = True
        s.commit()
    started = time.time()
    runner.join(timeout=30)
    assert not runner.is_alive() and time.time() - started < 15
    with worker.sessions() as s:
        stream = s.get(Stream, stream_id)
        assert stream.status == "stopped" and stream.stop_requested is False


def test_streams_left_running_by_a_crash_go_back_to_the_queue(settings):
    worker = Worker(settings, command=fake(FINISH))
    stream_id = add_stream(worker, status="running")
    with worker.sessions() as s:
        assert requeue_interrupted(s) == [stream_id]
        assert s.get(Stream, stream_id).status == "queued"


def test_claims_take_the_oldest_and_never_the_same_stream_twice(settings):
    worker = Worker(settings, command=fake(FINISH))
    first, second = add_stream(worker), add_stream(worker)
    other = db.session_factory(db.make_engine(settings.db_url))
    with worker.sessions() as a, other() as b:
        assert claim_next(a) == first
        assert claim_next(b) == second
        assert claim_next(a) is None


def test_a_missing_recording_fails_cleanly(settings):
    worker = Worker(settings, command=fake(FINISH))
    stream_id = add_stream(worker, source=False)
    worker.step()
    with worker.sessions() as s:
        assert s.get(Stream, stream_id).status == "failed"


def test_reimporting_keeps_decisions_on_unchanged_clips(settings):
    worker = Worker(settings, command=fake(FINISH))
    stream_id = add_stream(worker)
    worker.step()
    folder = settings.jobs_dir / stream_id
    with worker.sessions() as s:
        stream = s.get(Stream, stream_id)
        stream.clips[0].decision = "keep"
        stream.clips[1].decision = "reject"
        s.commit()
    ranked = json.loads((folder / "ranked.json").read_text())
    ranked[1]["end"] = 135.0   # the second clip was re-cut: its old decision no longer applies
    (folder / "ranked.json").write_text(json.dumps(ranked))
    with worker.sessions() as s:
        stream = s.get(Stream, stream_id)
        import_clips(s, stream, folder)
        s.commit()
        assert [c.decision for c in stream.clips] == ["keep", None]


def test_the_api_stops_resumes_and_reports_the_worker(settings):
    app = create_app(settings)
    client = TestClient(app, base_url="http://localhost")
    client.post("/auth/dev-login", json={"email": "a@example.com"}, headers=APP)
    worker = Worker(settings, command=fake(FAIL))
    assert client.get("/api/worker").json() == {"online": False, "busy": False, "queue_waiting": False}
    stream_id = add_stream(worker)
    assert client.get("/api/worker").json()["queue_waiting"] is True
    assert client.post(f"/api/streams/{stream_id}/stop", headers=APP).json()["status"] == "stopped"
    assert client.post(f"/api/streams/{stream_id}/stop", headers=APP).status_code == 409
    assert client.post(f"/api/streams/{stream_id}/resume", headers=APP).json()["status"] == "queued"
    worker.start()
    worker.step()
    failed = client.get(f"/api/streams/{stream_id}").json()
    assert failed["status"] == "failed" and failed["progress"]["stages"][1]["status"] == "failed"
    assert client.get("/api/worker").json()["online"] is True
    assert client.post(f"/api/streams/{stream_id}/resume", headers=APP).json()["status"] == "queued"
    (settings.jobs_dir / stream_id / "source.mp4").unlink()
    with worker.sessions() as s:
        s.get(Stream, stream_id).status = "failed"
        s.commit()
    assert client.post(f"/api/streams/{stream_id}/resume", headers=APP).status_code == 409


def test_progress_reads_the_manifest_and_the_scan_lines(settings, tmp_path):
    from aigcm.jobview import progress
    folder = tmp_path / "job"
    folder.mkdir()
    (folder / "manifest.json").write_text(json.dumps({"stages": {"ingest": {"status": "done"},
                                                                 "vision": {"status": "running"}}}))
    (folder / "run.log").write_text("x" * 100000 + "\n[10:00:00] vision: 15 min scanned, 3 kills\nW0000 noise\n")
    p = progress(folder, duration_s=1800)
    assert p["fraction"] == pytest.approx(0.03 + 0.55 * 0.5) and p["last_log"].endswith("3 kills")


def test_a_second_worker_waits_while_the_first_is_alive(settings):
    import subprocess
    from aigcm.db.models import WorkerState
    first = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
    try:
        worker = Worker(settings, command=fake(FINISH))
        stream_id = add_stream(worker, status="running")
        with worker.sessions() as s:
            s.merge(WorkerState(id=1, heartbeat_at=utcnow(), stream_id=stream_id, pid=first.pid))
            s.commit()
        with pytest.raises(RuntimeError, match="Another worker"):
            worker.start(timeout=0)
        with worker.sessions() as s:
            assert s.get(Stream, stream_id).status == "running"   # not taken over
    finally:
        first.kill()
        first.wait()
    worker.start(timeout=0)   # the first one is dead now: its stream goes back to the queue
    with worker.sessions() as s:
        assert s.get(Stream, stream_id).status == "queued"
