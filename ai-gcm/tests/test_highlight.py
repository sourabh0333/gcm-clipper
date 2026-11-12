"""The kill-match highlight's cut (Highlights Stage 1, S1.4): fights whole, cuts out of words, cards on jumps,
the teaser first, the ending last."""

import numpy as np

from aigcm.studio import highlight


def _map():
    fights = [
        {"start": 300.0, "end": 320.0, "kills": 2, "kill_times": [310.0, 318.0], "players_left": 80, "dinner": False},
        {"start": 330.0, "end": 335.0, "kills": 0, "kill_times": [], "players_left": 78, "dinner": False},
        {"start": 900.0, "end": 940.0, "kills": 4, "kill_times": [910.0, 915.0, 930.0, 938.0], "players_left": 12,
         "dinner": False},
        {"start": 1180.0, "end": 1195.0, "kills": 1, "kill_times": [1190.0], "players_left": 2, "dinner": True},
    ]
    one = {"n": 1, "start": 100.0, "end": 1200.0, "ended": "dinner", "placement": 1, "kills": 7, "fights": fights,
           "score": 40.0}
    two = {"n": 2, "start": 1500.0, "end": 2400.0, "ended": "death", "placement": 9, "kills": 3, "score": 12.0,
           "fights": [{"start": 2000.0, "end": 2020.0, "kills": 3, "kill_times": [2005.0, 2010.0, 2019.0],
                       "players_left": 40, "dinner": False}]}
    return {"matches": [one, two]}


TRANSCRIPT = {"segments": [{"words": [
    {"start": 285.0, "end": 286.0, "word": "enemy"}, {"start": 286.2, "end": 287.0, "word": "aage"},
    {"start": 287.2, "end": 289.0, "word": "hai"},          # the call, a few seconds before the first shot
    {"start": 340.0, "end": 341.5, "word": "bhai"},         # still talking when the fight ends
]}]}


def test_a_match_highlight_keeps_fights_whole_and_cuts_the_rest():
    plan = highlight.plan(_map(), [1], 3000.0, TRANSCRIPT)
    pieces = plan["pieces"]
    assert pieces[0]["kind"] == "teaser" and pieces[0]["label"] == "IN THIS VIDEO"
    assert highlight.TEASER_S[0] <= pieces[0]["end"] - pieces[0]["start"] <= highlight.TEASER_S[1] + 3
    body = [p for p in pieces[1:] if p["kind"] != "card"]
    assert body[0]["kind"] == "drop"                # the first fight is minutes in: a look at the drop first
    first = body[1]
    # The call before the first fight is in, both fights near each other joined, and the word at the end
    # isn't cut.
    assert first["start"] <= 285.0 - 0.05 and first["end"] >= 341.5
    for f in _map()["matches"][0]["fights"]:
        assert any(p["start"] <= f["start"] and p["end"] >= max(f["kill_times"] or [f["end"]]) for p in body), f
    # A long skip gets a card; the video ends on the Dinner and then black.
    assert any(p.get("text") == "A FEW MINUTES LATER" for p in pieces)
    assert body[-1]["end"] >= 1200.0 and pieces[-1] == {"kind": "card", "text": "", "length": highlight.END_BLACK_S}
    assert 0.1 < plan["kept"] < 0.5 and plan["kills"] == 7


def test_the_session_version_has_match_cards_in_order():
    plan = highlight.plan(_map(), [2, 1], 3000.0)
    cards = [p["text"] for p in plan["pieces"] if p["kind"] == "card" and p["text"].startswith("MATCH")]
    assert cards == ["MATCH 1", "MATCH 2"]
    matches = [p["match"] for p in plan["pieces"] if p["kind"] not in ("card", "teaser")]
    assert matches == sorted(matches)
    assert plan["pieces"][0]["match"] == 1          # the teaser comes from the better match


def test_cuts_never_land_inside_a_word():
    words = [(10.0, 11.0), (11.2, 12.0)]
    assert highlight.snap(10.5, words, "start") < 10.0
    assert highlight.snap(10.5, words, "end") > 11.0
    assert highlight.snap(9.0, [(9.3, 10.0), (10.2, 11.0)], "end") > 11.0   # a sentence going on finishes
    assert highlight.snap(30.0, words, "end") == 30.0


def test_punch_ins_go_on_the_loudest_reactions_inside_kept_footage():
    t = np.arange(0, 3000, 1.0)
    scream = np.zeros_like(t)
    scream[[315, 935, 2500]] = 1.0              # 2500 is outside the highlight
    plan = highlight.plan(_map(), [1], 3000.0, TRANSCRIPT, sounds={"t": t, "scream": scream, "laugh": np.zeros_like(t)},
                          facecam=(0.7, 0.6, 0.3, 0.4))
    spans = [s for p in plan["pieces"] for s in p.get("punch", [])]
    assert 1 <= len(spans) <= 2 and all(300 < a < 1200 for a, _ in spans)
    assert plan["facecam"] == [0.7, 0.6, 0.3, 0.4]


def test_no_kills_no_teaser():
    stream_map = {"matches": [{"n": 1, "start": 0.0, "end": 600.0, "ended": "death", "placement": None, "kills": 0,
                               "score": 1.0, "fights": [{"start": 200.0, "end": 210.0, "kills": 0, "kill_times": [],
                                                         "players_left": 50}]}]}
    plan = highlight.plan(stream_map, [1], 700.0)
    assert plan["pieces"][0]["kind"] != "teaser"
