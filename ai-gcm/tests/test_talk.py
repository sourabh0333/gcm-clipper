import numpy as np

from aigcm import moments, talk
from aigcm.config import Settings


def line(start, text, gap=0.4):
    words = [{"start": round(start + i * gap, 2), "end": round(start + i * gap + 0.3, 2), "word": w}
             for i, w in enumerate(text.split())]
    return {"start": words[0]["start"], "end": words[-1]["end"], "text": text, "words": words}


def calm(duration):
    t = np.arange(0.0, duration, 1.0)
    sounds = {"t": t, "laugh": np.zeros(len(t)), "scream": np.zeros(len(t)), "gunfire": np.zeros(len(t))}
    audio = {"t": t, "loudness": np.full(len(t), -30.0), "bursts": np.zeros(len(t)), "action": np.zeros(len(t)),
             "excitement": np.zeros(len(t))}
    return sounds, audio


def test_laughing_banter_becomes_a_talk_clip_with_its_setup():
    sounds, audio = calm(600)
    sounds["laugh"][300:304] = 0.08
    segments = [line(t, "loot karo idhar aao") for t in range(20, 580, 40)]
    segments += [line(286, "bhai tu pagal hai kya kar raha hai"), line(294, "abe sorry sorry"),
                 line(299, "hahaha noob")]
    transcript = {"segments": sorted(segments, key=lambda s: s["start"])}
    found = talk.from_rules(transcript, sounds, audio, Settings(), 600)
    assert found, "no talk moment found"
    best = found[0]
    assert best["start"] <= 286 and best["end"] >= 300
    assert "laughing" in best["reasons"] and "laughs in the transcript" in best["reasons"]


def test_quiet_routine_talk_makes_no_clip():
    sounds, audio = calm(600)
    transcript = {"segments": [line(t, "loot karo idhar aao") for t in range(20, 580, 40)]}
    assert talk.from_rules(transcript, sounds, audio, Settings(), 600) == []


def test_talk_moment_is_ranked_and_typed():
    sounds, audio = calm(600)
    found = moments.build([], audio, Settings(), 600, sounds=sounds,
                          talks=[{"start": 280.0, "end": 310.0, "peak": 300.0, "talk_score": 8, "source": "gemini",
                                  "talk_type": "banter", "title": "Teammate ko roast", "reasons": ["roasts a teammate"]}])
    assert found[0]["type"] == "banter" and found[0]["title"] == "Teammate ko roast"
    assert found[0]["reasons"][0] == "roasts a teammate"


def test_gemini_answer_is_turned_into_clip_times():
    assert talk._seconds("01:05") == 65 and talk._seconds("12:30") == 750
