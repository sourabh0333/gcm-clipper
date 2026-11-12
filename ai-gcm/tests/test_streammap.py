"""The stream map (Highlights Stage 1, S1.3): matches, their endings and fights, and the parts between them."""

import numpy as np

from aigcm import streammap, vision


def _vision(**extra):
    base = {
        "events": [
            {"t": 400.0, "kind": "match_start"},
            {"t": 700.0, "kind": "self_kill"}, {"t": 705.0, "kind": "self_kill"},
            {"t": 1500.0, "kind": "self_kill"},
            {"t": 2400.0, "kind": "match_start"},
            {"t": 2600.0, "kind": "self_kill"},
            {"t": 3500.0, "kind": "dinner"},
        ],
        "remaining": [[400.0, 99], [1500.0, 12], [2400.0, 98], [3400.0, 3]],
        # Match 1: HUD 390-1800 with a short gap; match 2: 2390-3510.
        "hud": [[390.0, 1100.0], [1104.0, 1800.0], [2390.0, 3510.0]],
        "spectating": [[1700.0, 1790.0]],
        "results": [{"t": 1830.0, "after": 1800.0, "lines": ["#7/99", "Eliminations 3"]}],
    }
    base.update(extra)
    return base


def _sounds():
    t = np.arange(0, 4000, 1.0, dtype=np.float32)
    gun = np.zeros_like(t)
    gun[(t >= 690) & (t <= 708)] = 0.8        # the fight around the first two kills
    gun[(t >= 1200) & (t <= 1210)] = 0.8      # shooting without a kill
    return {"t": t, "gunfire": gun}


def test_matches_their_endings_and_kills():
    found = streammap.build(_vision(), 4000.0, _sounds())
    first, second = found["matches"]
    assert (first["start"], first["kills"], first["ended"], first["placement"]) == (390.0, 3, "death", 7)
    assert first["end"] == 1700.0 - streammap.END_AFTER_SPECTATE_S        # ends when Spectating shows
    assert (second["ended"], second["placement"], second["kills"]) == ("dinner", 1, 1)
    assert found["best"] == 2 and found["session"] == []                     # a Dinner beats 3 kills here
    kinds = [p["kind"] for p in found["parts"]]
    assert kinds == ["between", "match", "between", "match", "between"]


def test_fights_join_kills_with_the_shooting_around_them():
    first = streammap.build(_vision(), 4000.0, _sounds())["matches"][0]
    fights = first["fights"]
    assert fights[0]["start"] == 690.0 and fights[0]["kills"] == 2 and fights[0]["players_left"] == 99
    assert any(f["kills"] == 0 and f["shots"] >= streammap.MIN_SHOTS for f in fights)   # a fight with no kill
    assert sum(f["kills"] for f in fights) == first["kills"]


def test_a_new_lobby_splits_runs_that_are_close_together():
    v = _vision(hud=[[390.0, 1800.0], [1900.0, 3510.0]], events=[
        {"t": 400.0, "kind": "match_start"}, {"t": 1910.0, "kind": "match_start"}], spectating=[], results=[])
    assert len(streammap.build(v, 4000.0)["matches"]) == 2
    v["events"] = [{"t": 400.0, "kind": "match_start"}]
    v["remaining"] = [[400.0, 99]]
    assert len(streammap.build(v, 4000.0)["matches"]) == 1        # no new-lobby signal and a short gap: one match


def test_placement_from_result_text():
    assert streammap.placement_from(["#12/98", "Eliminations 4"]) == 12
    assert streammap.placement_from(["WINNER WINNER CHICKEN DINNER"]) == 1
    assert streammap.placement_from(["Rank 3"]) == 3
    assert streammap.placement_from(["Remaining 40"]) is None


def test_gaps_split_into_lobby_and_not_bgmi():
    def read_text(t):
        if t < 600:
            return ["Thanks for the support guys"]               # chat, face full screen
        return ["START", "Classic - Erangel", "Inventory"]
    parts = streammap.classify_gaps([(0.0, 900.0)], read_text)
    assert [p["kind"] for p in parts] == ["not_bgmi", "between"]
    assert parts[0]["why"] and 580 <= parts[0]["end"] <= 640


def test_a_cut_off_match_and_the_comparison_with_labels():
    v = _vision(hud=[[390.0, 3995.0]], spectating=[], results=[], events=[{"t": 700.0, "kind": "self_kill"}])
    found = streammap.build(v, 4000.0)
    assert found["matches"][0]["ended"] == "cut_off"
    labels = {"matches": [{"n": 1, "start": 395, "end": 4000, "ended": "cut_off", "kills": 1},
                          {"n": 2, "start": 5000, "end": 5100, "ended": "death", "kills": 0}]}
    report = streammap.compare(found, labels)
    assert report["found"] == "1/2" and report["kills_ok"] == "1/1" and report["edges_ok"] == "1/1"


def test_hud_visible_needs_plausible_counters():
    assert vision.hud_visible({"elims": (3, 0.9), "remaining": (54, 0.9)})
    assert not vision.hud_visible({"elims": (3, 0.9), "remaining": (None, 0.0)})
    assert not vision.hud_visible({"elims": (250, 0.9)})        # a lobby number, not Eliminations
    runs = vision.Runs(8.0)
    for t in (1, 2, 3, 20, 21):
        runs.see(t)
    assert runs.spans == [[1, 3], [20, 21]]


def test_a_recall_mid_match_is_not_the_end():
    # Since update 4.6 a dead streamer can be recalled: Spectating at 900 then minutes of play.
    v = _vision(spectating=[[900.0, 960.0], [1750.0, 1760.0], [1790.0, 1795.0]], results=[])
    first = streammap.build(v, 4000.0)["matches"][0]
    assert first["end"] == 1750.0 - streammap.END_AFTER_SPECTATE_S and first["ended"] == "death"
    assert streammap.final_spectate([[900.0, 960.0]], 390.0, 1800.0) is None


def test_leftover_fights_are_the_ones_no_highlight_used(tmp_path):
    import time

    from aigcm import leftovers
    from aigcm.jobs import write_json

    stream_map = {"matches": [{"n": 1, "fights": [{"start": 100, "end": 130, "kills": 2}, {"start": 400, "end": 420, "kills": 0},
                                                  {"start": 600, "end": 640, "kills": 1}]}]}
    write_json(tmp_path / "map.json", stream_map)
    (tmp_path / "highlights" / "r1").mkdir(parents=True)
    (tmp_path / "leftovers").mkdir()
    write_json(tmp_path / "highlights" / "r1" / "plan.json", {"pieces": [{"kind": "fight", "start": 90, "end": 140},
                                                                          {"kind": "card", "text": ""}]})
    write_json(tmp_path / "clips.json", {})
    left = leftovers.unused_fights(stream_map, leftovers.used_spans(tmp_path))
    assert [(f["match"], f["fight"]) for f in left] == [(1, 2)]       # used and kill-less fights are not leftovers
    assert leftovers.summary(tmp_path)["count"] == 1
    write_json(tmp_path / "leftovers" / "leftovers.json", {"kept_until": time.time() - 1, "fights": []})
    assert leftovers.expire(tmp_path.parent) == [tmp_path.name] and not (tmp_path / "leftovers").exists()
