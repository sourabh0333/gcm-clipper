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
    # A fast cold open of 12-20 s: short beats under the hook, the kills the hook promises first, never the
    # Chicken Dinner or the kill that won it; hard cuts, and one whoosh into the match.
    assert 2 <= len(intro) <= highlight.INTRO_BEATS and intro[0]["why"] == "kills"
    assert not any(p["why"] == "dinner" or p["end"] >= 1180 for p in intro)
    assert sum(p["end"] - p["start"] for p in intro) <= highlight.INTRO_S[1] + 0.5
    assert all(p["text"] == "7 KILLS + CHICKEN DINNER 🏆" for p in intro)
    assert all(p["sfx"] == [] for p in intro)
    body = [p for p in pieces if p["kind"] not in ("card", "intro")]
    assert body[0]["sfx"] == [["whoosh", 0.0]]
    # Nothing is said over the drop, so the story starts on the first fight's call.
    assert not any(p["kind"] == "drop" for p in body)
    first = body[0]
    # The call before the first fight is in, both fights near each other joined, and the word at the end
    # isn't cut.
    assert first["start"] <= 285.0 - 0.05 and first["end"] >= 341.5
    for f in _map()["matches"][0]["fights"]:
        assert any(p["start"] <= f["start"] and p["end"] >= max(f["kill_times"] or [f["end"]]) for p in body), f
    # A long skip gets a card; the video ends a few seconds after the Dinner banner (at 1194), then black.
    assert any(p.get("text") == "A FEW MINUTES LATER" for p in pieces)
    assert 1197.0 <= body[-1]["end"] <= 1204.0
    assert pieces[-1] == {"kind": "card", "text": "", "length": highlight.END_BLACK_S}
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


def test_punch_ins_go_on_talk_or_reactions_held_for_the_sentence():
    t = np.arange(0, 3000, 1.0)
    scream, gun = np.zeros_like(t), np.zeros_like(t)
    scream[[315, 937, 2500]] = 1.0                    # 2500 is outside the highlight
    gun[(t >= 930) & (t <= 939)] = 0.8                # 937 is during shooting: no face then
    said = {"segments": [{"start": 314.0, "end": 317.5, "text": "bhai kya hua", "words": []},
                         {"start": 936.0, "end": 938.5, "text": "aaja", "words": []},
                         {"start": 2499.0, "end": 2501.0, "text": "outside", "words": []}]}
    plan = highlight.plan(_map(), [1], 3000.0, said, sounds={"t": t, "scream": scream, "laugh": np.zeros_like(t), "gunfire": gun},
                          facecam=(0.7, 0.6, 0.3, 0.4))
    spans = [s for p in plan["pieces"] for s in p.get("punch", [])]
    assert spans == [[313.9, 317.7]]                  # the whole sentence, not a fixed 2.6 s; never during shooting
    host = next(p for p in plan["pieces"] if p.get("punch"))
    assert host["captions"] and plan["facecam"] == [0.7, 0.6, 0.3, 0.4]


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
    # The last circles are kept, but a dead hold of 20 s or more ending over a minute before the end is cut.
    assert any(p["start"] <= 2000 - highlight.FINAL_KEEP_S and p["end"] >= 1997 for p in body)
    assert not any(p["start"] <= 1880 <= p["end"] for p in body)
    assert any(p["start"] <= 500 and p["end"] >= 530 for p in body)            # the gunfight with no kill
    assert not any(p["start"] <= 800 <= p["end"] for p in body)
    assert highlight.titles_for(stream_map, [1], plan)[0][0].startswith("CHICKEN DINNER WITH 1 FINISHES")


def test_the_editing_follows_the_game_and_the_talk():
    t = np.arange(0, 3000, 1.0)
    gun = np.zeros_like(t)
    gun[(t >= 905) & (t <= 940)] = 0.9                # the fight around kills 910-938
    plan = highlight.plan(_map(), [1], 3000.0, TRANSCRIPT, sounds={"t": t, "gunfire": gun},
                          talks=[{"start": 600.0, "end": 630.0, "peak": 615.0, "talk_score": 9, "title": "Bhai kya kar raha"}])
    fight = next(p for p in plan["pieces"] if p["kind"] == "fight" and p["start"] <= 910 <= p["end"])
    # The fight is one piece from the shots to the reaction, with nothing added on its kills.
    assert fight["start"] <= 905 and fight["end"] >= 938 and fight["zooms"] == [] and fight["sfx"] == []
    # Nothing on the Chicken Dinner banner either: it would crop the face at the frame's edge.
    assert not any(p.get("zooms") for p in plan["pieces"])
    talk = next(p for p in plan["pieces"] if p["kind"] == "talk")
    assert talk["captions"] is True                    # the funny line gets subtitles
    assert any(p["kind"] == "intro" and p["why"] == "funny" and p.get("captions") for p in plan["pieces"])


def test_dead_stretches_inside_a_fight_are_cut_but_action_never_is():
    t = np.arange(0, 2000, 1.0)
    gun = np.zeros_like(t)
    gun[(t >= 100) & (t <= 130)] = 0.9
    gun[(t >= 200) & (t <= 230)] = 0.9                # 70 s of looting between two bursts of shooting
    fight = {"start": 100.0, "end": 230.0, "kills": 2, "kill_times": [128.0, 228.0], "players_left": 40}
    pieces = highlight.fight_pieces(fight, [], None, 0.0, 2000.0, {"t": t, "gunfire": gun})
    assert len(pieces) == 2 and pieces[0]["end"] <= 140 and pieces[1]["start"] >= 190
    assert highlight.fight_pieces(fight, [], None, 0.0, 2000.0, None)[0]["end"] >= 230   # no sound data: kept whole


def test_shorts_are_short_high_impact_moments():
    stream_map = _map()
    plan = highlight.plan(stream_map, [1], 3000.0, TRANSCRIPT)
    shorts = highlight.short_moments(plan, stream_map, [{"start": 600.0, "end": 650.0, "talk_score": 9, "title": "Bhai"}])
    assert 1 <= len(shorts) <= highlight.SHORTS_MAX
    assert all(highlight.SHORT_S[0] - 0.01 <= s["end"] - s["start"] <= highlight.SHORT_S[1] + 0.01 for s in shorts)
    # A person moment ranks first and is the teaser; the Dinner Short is never the teaser (the video keeps it).
    assert shorts[0]["kind"] == "funny" and shorts[0]["role"] == "teaser" and shorts[0]["title"] == "Bhai 😂"
    assert any(s["kind"] == "dinner" and s["role"] == "dinner" for s in shorts)
    kinds = {s["kind"] for s in shorts}
    assert "clutch" in kinds or "fight" in kinds                                 # the 4-kill burst
    burst = next(s for s in shorts if s["kind"] in ("clutch", "fight") and s["kills"] == 4)
    # From the run-up to the reaction: never ending on the kill frame, the face after a little game.
    assert burst["start"] <= 910 - highlight.SHORT_LEAD_S + 0.01
    assert 938 + highlight.SHORT_GAME_AFTER_S + highlight.SHORT_FACE_S[0] - 0.01 <= burst["end"] <= 938 + 5.01
    assert burst["face"][0] == 938 + highlight.SHORT_GAME_AFTER_S
    # Searched across the whole stream: match 2's 3-kill burst can be a Short too.
    assert any(s["match"] == 2 for s in shorts) or len(shorts) == highlight.SHORTS_MAX
    for a in shorts:                                                            # no two Shorts overlap
        assert all(a is b or a["end"] <= b["start"] or a["start"] >= b["end"] for b in shorts)
    lone = {"matches": [{"n": 1, "start": 0.0, "end": 900.0, "ended": "death", "placement": 30, "kills": 1, "score": 3,
                         "fights": [{"start": 400.0, "end": 405.0, "kills": 1, "kill_times": [402.0], "players_left": 60}]}]}
    assert len(highlight.short_moments({"matches": [1]}, lone)) == 1             # a weak match: one Short, not three


def test_a_short_shows_the_face_alone_while_talking_with_no_shooting():
    t = np.arange(0, 100, 1.0)
    gun = np.zeros_like(t)
    gun[(t >= 40) & (t <= 48)] = 0.9
    said = {"segments": [{"start": 12.0, "end": 15.0}, {"start": 16.5, "end": 19.0},     # joined: 1.5 s apart
                         {"start": 42.0, "end": 45.0},                                    # during shooting: no
                         {"start": 60.0, "end": 60.5}]}                                   # too short to switch for
    assert highlight.talk_spans(10.0, 70.0, said, {"t": t, "gunfire": gun}) == [(11.9, 19.2)]
    from aigcm.studio.edit import FaceSpan, default_edit
    from aigcm.studio.render import build_graph

    edit = default_edit(10.0, 40.0, 1280, 720, "X", facecam=(0.7, 0.6, 0.3, 0.4))
    edit = edit.model_copy(update={"face": [FaceSpan(start=11.9, end=19.2)]})
    graph = build_graph(edit, 10.0, True)
    assert "between(t,1.900,9.200)" in graph and "[faced]" in graph
    plain = build_graph(default_edit(10.0, 40.0, 1280, 720, "X"), 10.0, True)
    assert "[faced]" not in plain                                  # no camera, no face moments


def _sounds(n=3000):
    t = np.arange(0, n, 1.0)
    return t, {"t": t, "scream": np.zeros_like(t), "laugh": np.zeros_like(t), "gunfire": np.zeros_like(t)}


def test_talk_is_rated_like_kills_and_a_reaction_lifts_it():
    t, sounds = _sounds()
    sounds["laugh"][[620]] = 1.0                       # a laugh right after the line
    talks = [{"start": 600.0, "end": 618.0, "talk_score": 7, "title": "A"},
             {"start": 700.0, "end": 718.0, "talk_score": 7, "title": "B"}]
    scored = highlight.scored_talks(talks, highlight.reaction_level(sounds))
    assert [c["reacted"] for c in scored] == [True, False]
    plan = highlight.plan(_map(), [1], 3000.0, sounds=sounds, talks=talks)
    titles = [p.get("title") for p in plan["pieces"] if p["kind"] == "talk"]
    assert titles == ["A"]                             # the 7 with a laugh goes in, the flat 7 doesn't


def test_a_fight_runs_on_to_the_line_after_the_last_kill():
    words = [(1003.0, 1004.0), (1004.2, 1006.0)]       # said 3 s after the last kill, ending at 1006
    fight = {"start": 980.0, "end": 1000.0, "kills": 1, "kill_times": [1000.0], "players_left": 30}
    piece = highlight.fight_piece(fight, words, None, 0.0, 3000.0)
    assert piece["end"] >= 1006.0 + highlight.REPLY_PAD_S - 0.01


def test_the_ending_holds_for_the_reaction_and_a_death_shows_the_line_after_it():
    dinner = {"n": 1, "start": 0.0, "end": 1000.0, "ended": "dinner", "placement": 1, "kills": 1, "fights": []}
    words = [(995.0, 996.0), (996.1, 998.5)]           # "winner winner" said after the banner at 994
    a, b, line = highlight.ending_span(dinner, words, 2000.0)
    assert line == (995.0, 998.5) and b == 998.5 + highlight.REPLY_PAD_S
    a, b, line = highlight.ending_span(dinner, [], 2000.0)
    assert 994 + highlight.HOLD_AFTER_S[0] <= b <= 994 + highlight.HOLD_AFTER_S[1]
    death = {"n": 2, "start": 0.0, "end": 500.0, "ended": "death", "placement": 20, "kills": 2,
             "fights": [{"start": 300.0, "end": 310.0, "kills": 2, "kill_times": [302.0, 309.0], "players_left": 50}]}
    said = {"segments": [{"start": 501.0, "end": 504.0, "text": "nahi yaar", "words": [
        {"start": 501.0, "end": 502.0, "word": "nahi"}, {"start": 502.2, "end": 504.0, "word": "yaar"}]}]}
    plan = highlight.plan({"matches": [death]}, [2], 2000.0, said, facecam=(0.7, 0.6, 0.3, 0.4))
    last = [p for p in plan["pieces"] if p["kind"] != "card"][-1]
    assert last["end"] >= 504.0 + highlight.REPLY_PAD_S - 0.01
    assert last["mono"] == [[500.9, 503.5]] or last["mono"][0][0] == 500.9   # black and white over the line
    assert last["mono"][0][1] - last["mono"][0][0] >= highlight.MONO_S[0] - 0.01


def test_a_shout_after_the_last_kill_gets_a_face_cutaway():
    t, sounds = _sounds()
    sounds["scream"][[940]] = 1.0                      # right after the last kill at 938
    sounds["gunfire"][(t >= 905) & (t <= 938)] = 0.9
    plan = highlight.plan(_map(), [1], 3000.0, {"segments": []}, sounds=sounds, facecam=(0.7, 0.6, 0.3, 0.4))
    spans = [s for p in plan["pieces"] if p["kind"] != "intro" for s in p.get("punch", [])]
    cut = next(s for s in spans if 938 < s[0] < 942)
    assert highlight.CUTAWAY_S[0] - 0.01 <= cut[1] - cut[0] <= highlight.CUTAWAY_S[1] + 0.01


def test_long_stretches_with_no_payoff_are_trimmed_but_not_the_last_minute():
    t, sounds = _sounds()
    match = {"n": 1, "start": 0.0, "end": 900.0, "ended": "death", "placement": 30, "kills": 2,
             "fights": [{"start": 100.0, "end": 200.0, "kills": 2, "kill_times": [110.0, 195.0], "players_left": 60}]}
    words = [(x, x + 0.5) for x in np.arange(100.0, 200.0, 1.0)]   # talk all the way through: never "quiet"
    pieces = highlight.match_pieces(match, words, None, [], 1000.0, sounds)
    covered = [(p["start"], p["end"]) for p in pieces if p["start"] < 200]
    assert len(covered) == 2                                          # the 85 s between the kills is trimmed
    assert covered[0][1] <= 110 + highlight.PACE_AFTER_S + 3.5 and covered[1][0] >= 195 - highlight.PACE_BEFORE_S - 3.5


def test_shorts_rank_reactions_and_the_hook_band_is_short():
    assert highlight.band("BP Badhane Wala Teammate Ka Asli Chehra Dekho") == "BP Badhane Wala Teammate Ka Asli 😂"
    assert highlight.band("Paani Me Kya Ho Raha 😱") == "Paani Me Kya Ho Raha 😱"
    t, sounds = _sounds()
    sounds["scream"][2021] = 1.0                       # match 2's burst has a shout after it, match 1's don't
    shorts = highlight.short_moments({"matches": [1]}, _map(), (), (), sounds)
    fights = [s for s in shorts if s["kind"] in ("fight", "clutch")]
    assert any(s["match"] == 2 for s in fights)       # from another match of the stream, for its shout
    assert not any(s["start"] <= 310 <= s["end"] for s in shorts)   # 2 kills, no shout, no clutch: not a Short


def test_a_low_stakes_match_leads_with_its_line_and_a_catchphrase_is_a_title():
    stream_map = {"matches": [{"n": 1, "start": 0.0, "end": 900.0, "ended": "death", "placement": 30, "kills": 2,
                               "fights": [{"start": 100.0, "end": 130.0, "kills": 2, "kill_times": [110.0, 125.0],
                                           "players_left": 60}]}]}
    said = {"segments": [{"start": 100.0 + 5 * i, "end": 102.0 + 5 * i, "text": "bilkul badhiya scene", "words": [
        {"start": 100.0 + 5 * i, "end": 100.6 + 5 * i, "word": "bilkul"},
        {"start": 100.7 + 5 * i, "end": 101.3 + 5 * i, "word": "badhiya"},
        {"start": 101.4 + 5 * i, "end": 102.0 + 5 * i, "word": "scene"}]} for i in range(4)]}
    plan = highlight.plan(stream_map, [1], 1000.0, said)
    titles, _ = highlight.titles_for(stream_map, [1], plan, transcript=said)
    assert titles[0].startswith('"BILKUL BADHIYA SCENE" 😂')
