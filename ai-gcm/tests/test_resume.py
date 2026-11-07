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
    monkeypatch.setitem(sys.modules, "faster_whisper", types.SimpleNamespace(WhisperModel=FakeWhisper, BatchedInferencePipeline=lambda model: model))
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


def test_a_transcript_that_misses_detected_speech_looks_broken():
    t = np.arange(0.0, 600.0, 1.0)
    sounds = {"t": t, "speech": np.where(t < 300, 0.9, 0.0)}        # talking for the first 5 minutes
    full = {"segments": [{"words": [{"start": float(s), "end": s + 0.8, "word": "w"} for s in range(0, 300, 1)]}]}
    sparse = {"segments": [{"words": [{"start": float(s), "end": s + 0.8, "word": "w"} for s in range(0, 300, 10)]}]}
    assert transcript.coverage(full, sounds) > 0.95 and transcript.coverage(sparse, sounds) < 0.3
    assert not transcript.looks_broken(full, sounds) and transcript.looks_broken(sparse, sounds)
    quiet = {"t": t, "speech": np.zeros(len(t))}
    assert not transcript.looks_broken(sparse, quiet)              # too little speech to judge


def test_clip_windows_are_redone_and_spliced_into_the_transcript(tmp_path, monkeypatch):
    monkeypatch.setitem(sys.modules, "faster_whisper", types.SimpleNamespace(WhisperModel=FakeWhisper, BatchedInferencePipeline=lambda model: model))
    wav = tmp_path / "audio.wav"
    silent_wav(wav, 60)
    old = {"segments": [{"start": 5.0, "end": 6.0, "text": "old a", "words": [{"start": 5.0, "end": 6.0, "word": "old"}]},
                        {"start": 30.0, "end": 31.0, "text": "old b", "words": [{"start": 30.0, "end": 31.0, "word": "old"}]}]}
    FakeWhisper.calls, FakeWhisper.crash_on = 0, None
    new = transcript.retranscribe_windows(wav, [(20.0, 40.0)], Settings(whisper_model="small"), old)
    assert [s["text"] for s in new["segments"]] == ["old a", "line1"]     # "old b" was inside the window
    assert new["segments"][1]["start"] == 21.0 and new["windows"] == [[20.0, 40.0]]


def test_speech_spans_follow_the_sound_detector():
    t = np.arange(0.0, 100.0, 1.0)
    speech = np.zeros(100)
    speech[10:14] = 0.9          # 4 s of talk
    speech[15] = 0.9             # a 1 s gap, then more: merged into one span
    speech[50:95] = 0.9          # 45 s of talk: cut into 30 s + the rest
    spans = transcript.speech_spans({"t": t, "speech": speech}, 0.0, 100.0)
    assert spans[0] == {"start": 9.5, "end": 16.5}
    assert [s["end"] - s["start"] for s in spans[1:]] == [30.0, 16.0]
    assert transcript.speech_spans({"t": t, "speech": speech}, 20.0, 40.0) == []


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


def test_an_upload_in_the_job_folder_is_used_in_place_and_others_are_copied(tmp_path):
    from aigcm.__main__ import local_source
    from aigcm.jobs import Job
    job = Job(tmp_path / "st_1")
    upload = job.path("source.mkv")
    upload.write_bytes(b"video")
    assert local_source(upload, job) == upload and [p.name for p in job.root.iterdir()] == ["source.mkv"]
    elsewhere = tmp_path / "My Stream.MP4"
    elsewhere.write_bytes(b"other")
    copied = local_source(elsewhere, job)
    assert copied == job.path("source.mp4") and copied.read_bytes() == b"other" and elsewhere.exists()
