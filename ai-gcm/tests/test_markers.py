import numpy as np

from aigcm import markers, moments
from aigcm.config import Settings
from aigcm.jobs import Job, write_json


def quiet_audio(duration, hop=0.5):
    n = int(duration / hop)
    return {"t": np.arange(n) * hop, "loudness": np.full(n, -30.0), "bursts": np.zeros(n),
            "action": np.zeros(n), "excitement": np.zeros(n)}


def ev(t, kind):
    return {"t": t, "kind": kind, "text": kind}


def test_markers_are_read_from_the_job_and_the_transcript(tmp_path):
    job = Job(tmp_path / "j")
    write_json(job.path("markers.json"), [{"t": 300, "source": "button"}, {"t": 120.5, "source": "chat", "by": "mod1"},
                                          {"source": "button"}])
    transcript = {"segments": [{"start": 400.0, "end": 402.0, "text": "bhai clip that wala moment"},
                               {"start": 500.0, "end": 501.0, "text": "loot karo"}]}
    found = markers.merge(markers.load(job), markers.from_transcript(transcript))
    assert [(m["t"], m["source"]) for m in found] == [(120.5, "chat"), (300, "button"), (398.0, "voice")]


def test_repeated_chat_marks_fold_into_one():
    found = markers.merge([{"t": 10, "source": "chat"}, {"t": 12, "source": "chat"}, {"t": 13, "source": "chat"}])
    assert len(found) == 1 and found[0]["count"] == 3


def test_a_marked_moment_always_becomes_a_clip_and_outranks_a_single_kill():
    s = Settings()
    found = moments.build([ev(100, "self_kill")], quiet_audio(600), s, 600, markers=[{"t": 400, "source": "button"}])
    marked = next(c for c in found if c["type"] == "marked")
    assert marked["start"] <= 400 - 15 and marked["end"] >= 400 + 5
    assert found[0] is marked and marked["why"].startswith("you marked this at 0:06:40")
    assert marked["labels"]["marked"] and marked["labels"]["game"] == "bgmi"


def test_a_marker_inside_a_fight_joins_that_fight():
    found = moments.build([ev(100, "self_kill"), ev(104, "self_kill")], quiet_audio(600), Settings(), 600,
                          markers=[{"t": 106, "source": "voice"}])
    assert len(found) == 1
    assert found[0]["labels"]["kills"] == 2 and found[0]["labels"]["marked"]
    assert found[0]["why"].startswith('you said "clip that", 2 kills by the streamer at 0:01:40')
