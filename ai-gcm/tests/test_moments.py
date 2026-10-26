import numpy as np

from aigcm import moments
from aigcm.captions import chunk_words, to_ass
from aigcm.config import Settings
from aigcm.vision import classify


def quiet_audio(duration, hop=0.5):
    n = int(duration / hop)
    return {"t": np.arange(n) * hop, "loudness": np.full(n, -30.0), "bursts": np.zeros(n),
            "action": np.zeros(n), "excitement": np.zeros(n)}


def ev(t, kind):
    return {"t": t, "kind": kind, "text": kind}


def test_events_close_together_form_one_fight():
    s = Settings()
    found = moments.build([ev(100, "self_knock"), ev(108, "self_kill"), ev(300, "self_kill")],
                          quiet_audio(600), s, 600)
    assert len(found) == 2
    fight = next(c for c in found if c["start"] < 100)
    assert fight["start"] <= 100 - s.pre_roll_s and fight["end"] >= 108 + s.post_roll_s
    assert len(fight["events"]) == 2


def test_multi_kill_outranks_single_kill():
    found = moments.build([ev(50, "self_kill"), ev(200, "self_knock"), ev(205, "self_kill"), ev(210, "self_kill"),
                           ev(214, "self_kill")], quiet_audio(600), Settings(), 600)
    assert found[0]["type"] == "multi_kill"
    assert found[0]["score"] > found[1]["score"]


def test_clip_lengths_stay_within_limits_and_inside_the_video():
    s = Settings()
    events = [ev(t, "self_knock") for t in range(5, 200, 10)] + [ev(598, "self_kill")]
    for c in moments.build(events, quiet_audio(600), s, 600):
        assert s.min_clip_s - 0.01 <= c["end"] - c["start"] <= s.max_clip_s + 0.01
        assert 0 <= c["start"] and c["end"] <= 600


def test_late_game_fight_outranks_early_one():
    found = moments.build([ev(100, "self_kill"), ev(400, "self_kill")], quiet_audio(600), Settings(), 600,
                          remaining=[(0, 90), (300, 8)])
    assert found[0]["start"] > 300 and found[0]["players_left"] == 8


def test_loud_spike_without_hud_event_becomes_reaction():
    audio = quiet_audio(600)
    audio["excitement"][800] = 5.0
    found = moments.build([], audio, Settings(), 600)
    assert len(found) == 1 and found[0]["type"] == "reaction"
    assert found[0]["start"] < 400 < found[0]["end"]


def test_hud_text_classification():
    assert classify("YOU KNOCKED OUT Rider_99 with M416") == "self_knock"
    assert classify("You finally killed Ghost") == "self_kill"
    assert classify("WINNER WINNER CHICKEN DINNER!") == "dinner"
    assert classify("You've become the new Ace Eliminator!") == "accolade"
    assert classify("Alpha knocked out Bravo with AKM") is None
    assert classify("alpha knocked out bravo", player_names=("alpha",)) == "self_knock"
    # Text seen on a real stream that must not count as kills.
    assert classify("Picked up Painkillers.") is None
    assert classify("Eliminate3players withaPistol.") is None
    assert classify("Zone is shrinking") is None


def test_captions_split_into_short_timed_chunks():
    words = [{"start": i * 0.3, "end": i * 0.3 + 0.25, "word": f" w{i}"} for i in range(7)]
    chunks = chunk_words(words)
    assert [c["text"] for c in chunks] == ["w0 w1 w2", "w3 w4 w5", "w6"]
    assert "Dialogue: 0,0:00:00.00,0:00:00.85,Caption,,0,0,0,,W0 W1 W2" in to_ass(chunks, 300)
