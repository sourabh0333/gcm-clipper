import pytest

from aigcm.jobs import Job


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


def test_invalidate_marks_later_stages_stale(tmp_path):
    job = Job(tmp_path / "j")
    for stage in ("ingest", "vision", "audio", "moments"):
        job.run(stage, lambda j: None)
    job.invalidate_from("audio")
    assert job.done("ingest") and job.done("vision")
    assert not job.done("audio") and not job.done("moments")
