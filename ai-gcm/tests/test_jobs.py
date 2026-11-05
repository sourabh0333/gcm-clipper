import pytest

from aigcm.__main__ import clear_from
from aigcm.jobs import Job, read_json, write_json


def test_failed_stage_reruns_and_done_stage_is_skipped(tmp_path):
    calls = []

    def ok(job):
        calls.append("ok")

    def boom(job):
        calls.append("boom")
        raise RuntimeError("crash")

    job = Job(tmp_path / "j")
    job.run("ingest", ok)
    with pytest.raises(RuntimeError):
        job.run("vision", boom)

    resumed = Job(tmp_path / "j")
    assert resumed.done("ingest") and not resumed.done("vision")
    resumed.run("ingest", ok)
    resumed.run("vision", ok)
    assert calls == ["ok", "boom", "ok"]


def test_rerunning_moments_keeps_earlier_decisions_aside(tmp_path):
    job = Job(tmp_path / "j")
    write_json(job.path("ranked.json"), [{"id": "m01"}])
    write_json(job.path("decisions.json"), {"m01": {"verdict": "keep"}})
    clear_from(job, "moments")
    assert not job.path("decisions.json").exists() and not job.path("ranked.json").exists()
    (archive,) = job.path("history").iterdir()
    assert read_json(archive / "decisions.json") == {"m01": {"verdict": "keep"}}
    assert read_json(archive / "ranked.json") == [{"id": "m01"}]


def test_parallel_groups_run_together_and_report_the_first_error(tmp_path):
    import threading
    import time

    job = Job(tmp_path / "j")
    seen = []
    gate = threading.Event()

    def vision(j):
        gate.wait(5)          # finishes only once the audio group has started: proves they overlap
        seen.append("vision")

    def audio_(j):
        gate.set()
        seen.append("audio")

    def boom(j):
        raise RuntimeError("whisper died")

    job.run_parallel([[("vision", vision)], [("audio", audio_)]])
    assert sorted(seen) == ["audio", "vision"] and job.done("vision") and job.done("audio")
    with pytest.raises(RuntimeError, match="whisper died"):
        job.run_parallel([[("sounds", lambda j: time.sleep(0.1))], [("transcript", boom)]])
    assert job.done("sounds") and not job.done("transcript")


def test_invalidate_marks_later_stages_stale(tmp_path):
    job = Job(tmp_path / "j")
    for stage in ("ingest", "vision", "audio", "moments"):
        job.run(stage, lambda j: None)
    job.invalidate_from("audio")
    assert job.done("ingest") and job.done("vision")
    assert not job.done("audio") and not job.done("moments")
