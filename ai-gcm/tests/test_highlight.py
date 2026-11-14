"""The kill-match highlight's cut (Highlights Stage 1, S1.4): fights whole, cuts out of words, cards on jumps,
the cold open first, the ending last; kill zooms, sounds and subtitles; short high-impact Shorts."""

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
    intro = [p for p in pieces if p["kind"] == "intro"]
    assert pieces[0] is intro[0] and intro[0]["label"] == "IN THIS VIDEO"
    # A fast cold open: a few short beats under the hook, the Chicken Dinner last, a whoosh between beats.
    assert 2 <= len(intro) <= highlight.INTRO_BEATS and intro[-1]["why"] == "dinner"
    assert all(p["end"] - p["start"] <= highlight.BEAT_S[1] + 2.6 for p in intro)
    assert all(p["text"] == "7 KILLS + CHICKEN DINNER 🏆" for p in intro)
    assert intro[0]["sfx"] == [] and all(["whoosh", 0.0] in p["sfx"] for p in intro[1:])
    body = [p for p in pieces if p["kind"] not in ("card", "intro")]
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
    matches = [p["match"] for p in plan["pieces"] if p["kind"] not in ("card", "intro")]
    assert matches == sorted(matches)
    assert plan["pieces"][0]["kind"] == "intro"     # the cold open takes beats from both matches


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


def test_no_kills_no_kill_beats():
    stream_map = {"matches": [{"n": 1, "start": 0.0, "end": 600.0, "ended": "death", "placement": None, "kills": 0,
                               "score": 1.0, "fights": [{"start": 200.0, "end": 210.0, "kills": 0, "kill_times": [],
                                                         "players_left": 50}]}]}
    plan = highlight.plan(stream_map, [1], 700.0)
    assert not any(p["kind"] == "intro" and p["why"] == "kills" for p in plan["pieces"])


def test_a_dinner_with_few_kills_keeps_its_last_circles_and_gunfights():
    t = np.arange(0, 3000, 1.0)
    gun = np.zeros_like(t)
    gun[(t >= 500) & (t <= 530)] = 0.9            # a gunfight with no kill
    gun[(t >= 800) & (t <= 803)] = 0.9            # too short to add
    stream_map = {"matches": [{"n": 1, "start": 100.0, "end": 2000.0, "ended": "dinner", "placement": 1, "kills": 1, "score": 20,
                               "fights": [{"start": 1200.0, "end": 1210.0, "kills": 1, "kill_times": [1205.0], "players_left": 30}]}]}
    plan = highlight.plan(stream_map, [1], 3000.0, sounds={"t": t, "gunfire": gun})
    body = [p for p in plan["pieces"] if p["kind"] not in ("card", "intro")]
    assert any(p["start"] <= 1820 and p["end"] >= 2000 for p in body)          # the last 3 minutes
    assert any(p["start"] <= 500 and p["end"] >= 530 for p in body)            # the gunfight with no kill
    assert not any(p["start"] <= 800 <= p["end"] for p in body)
    assert highlight.titles_for(stream_map, [1], plan)[0][0].startswith("CHICKEN DINNER WITH 1 FINISHES")


def test_the_editing_follows_the_action():
    plan = highlight.plan(_map(), [1], 3000.0, TRANSCRIPT,
                          talks=[{"start": 600.0, "end": 630.0, "peak": 615.0, "talk_score": 9, "title": "Bhai kya kar raha"}])
    fight = next(p for p in plan["pieces"] if p["kind"] == "fight" and p["start"] <= 910 <= p["end"])
    # A quick zoom on each kill (kills 5 s apart each get their own), a boom at the end of a burst.
    assert [round(t + fight["start"]) for t in fight["zooms"]] == [910, 915, 930, 938]
    assert any(name == "boom" for name, _ in fight["sfx"])
    talk = next(p for p in plan["pieces"] if p["kind"] == "talk")
    assert talk["captions"]                                                     # the funny line gets subtitles
    assert any(p["kind"] == "intro" and p["why"] == "funny" and p.get("captions") for p in plan["pieces"])


def test_shorts_are_short_high_impact_moments():
    stream_map = _map()
    plan = highlight.plan(stream_map, [1], 3000.0, TRANSCRIPT)
    shorts = highlight.short_moments(plan, stream_map, [{"start": 600.0, "end": 650.0, "talk_score": 9, "title": "Bhai"}])
    assert 1 <= len(shorts) <= highlight.SHORTS_MAX
    assert all(highlight.SHORT_S[0] - 0.01 <= s["end"] - s["start"] <= highlight.SHORT_S[1] + 0.01 for s in shorts)
    assert shorts[0]["kind"] == "dinner" and shorts[0]["role"] == "teaser" and "DINNER" in shorts[0]["title"]
    kinds = {s["kind"] for s in shorts}
    assert "clutch" in kinds or "fight" in kinds                                 # the 4-kill burst
    burst = next(s for s in shorts if s["kind"] in ("clutch", "fight"))
    assert burst["start"] <= 910 - highlight.SHORT_LEAD_S + 0.01 and burst["end"] >= 938 and burst["kills"] == 4
    for a in shorts:                                                            # no two Shorts overlap
        assert all(a is b or a["end"] <= b["start"] or a["start"] >= b["end"] for b in shorts)
    lone = {"matches": [{"n": 1, "start": 0.0, "end": 900.0, "ended": "death", "placement": 30, "kills": 1, "score": 3,
                         "fights": [{"start": 400.0, "end": 405.0, "kills": 1, "kill_times": [402.0], "players_left": 60}]}]}
    assert len(highlight.short_moments({"matches": [1]}, lone)) == 1             # a weak match: one Short, not three
