import os
import sys
import time
import types
import wave

import numpy as np
import pytest

from aigcm import transcript
from aigcm.__main__ import stale_sources
from aigcm.config import Settings
from aigcm.jobs import Job, read_json, write_json
from aigcm.vision import Counter


def test_counter_state_survives_a_restart():
    counter = Counter("elims")
    counter.update(0.0, 3)
    counter.update(0.5, 3)
    counter.update(1.0, 4)
    restored = Counter("elims").restore(counter.state())
    assert restored.update(1.5, 4) == (1.0, 3, 4)


class FakeWhisper:
    """Stands in for faster-whisper: one short line per chunk, and can crash on a chosen call."""
    calls = 0
    crash_on = None

    def __init__(self, *args, **kwargs):
        pass

    def transcribe(self, samples, **kwargs):
        FakeWhisper.calls += 1
        if FakeWhisper.calls == FakeWhisper.crash_on:
            raise RuntimeError("power cut")
        word = types.SimpleNamespace(start=1.0, end=1.4, word=f" line{FakeWhisper.calls}")
        seg = types.SimpleNamespace(compression_ratio=1.0, avg_logprob=-0.2, words=[word])
        return [seg], None


def silent_wav(path, seconds, rate=16000):
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(np.zeros(seconds * rate, dtype=np.int16).tobytes())


def test_transcript_resumes_after_a_crash_without_redoing_chunks(tmp_path, monkeypatch):
    monkeypatch.setitem(sys.modules, "faster_whisper", types.SimpleNamespace(WhisperModel=FakeWhisper))
    monkeypatch.setattr(transcript, "CHUNK_S", 10)
    wav, ckpt = tmp_path / "audio.wav", tmp_path / "transcript.partial.json"
    silent_wav(wav, 35)                                  # 4 chunks of 10 s
    settings = Settings(whisper_model="small")

    FakeWhisper.calls, FakeWhisper.crash_on = 0, 3
    with pytest.raises(RuntimeError):
        transcript.transcribe(wav, settings, ckpt)
    assert len(read_json(ckpt)["segments"]) == 2         # chunks 1 and 2 were saved

    FakeWhisper.crash_on = None
    result = transcript.transcribe(wav, settings, ckpt)
    assert FakeWhisper.calls == 3 + 2                    # 3 before the crash, then only chunks 3 and 4
    assert [s["start"] for s in result["segments"]] == [1.0, 11.0, 21.0, 31.0]
    assert not ckpt.exists()


def test_cleanup_deletes_only_old_sources_of_finished_jobs(tmp_path):
    def job(name, rendered, age_days):
        j = Job(tmp_path / name)
        for f in ("source.mp4", "audio.wav", "transcript.json"):
            j.path(f).write_bytes(b"x")
        if rendered:
            j.run("render", lambda _: None)
            write_json(j.path("clips.json"), {})
            old = time.time() - age_days * 86400
            os.utime(j.path("clips.json"), (old, old))
        return j

    job("old_done", True, 20)
    job("new_done", True, 2)
    job("old_unfinished", False, 20)
    names = sorted((p.parent.name, p.name) for p in stale_sources(tmp_path, 14))
    assert names == [("old_done", "audio.wav"), ("old_done", "source.mp4")]
