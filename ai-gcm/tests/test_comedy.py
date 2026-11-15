"""The comedy highlight's units (Highlights Stage 2, S2.2-S2.4): lines, Gemini's units, the rules, tidying,
the window and the selection, and the score against an editor."""

import json

import numpy as np

from aigcm import comedy

VTT = """WEBVTT

00:00:01.000 --> 00:00:03.000 align:start position:0%

bhai<00:00:01.500><c> ye</c><00:00:02.000><c> kya</c>

00:00:03.000 --> 00:00:03.010 align:start position:0%
bhai ye kya

00:00:03.010 --> 00:00:05.000 align:start position:0%
bhai ye kya
हा<00:00:03.500><c> हा</c><00:00:04.000><c> हा</c><00:00:04.500><c> [हंसी]</c>
"""


def test_lines_from_captions_and_transcripts():
    lines = comedy.lines_from_vtt(VTT)
    assert [(a, b) for a, b, _ in lines] == [(1.0, 3.0), (3.01, 5.0)]
    assert comedy.LAUGH_TEXT.search(lines[1][2])
    said = {"segments": [{"start": 10.0, "end": 12.0, "text": " kya scene hai "}, {"start": 5.0, "end": 5.0, "text": "x"}]}
    assert comedy.lines_from_transcript(said) == [(10.0, 12.0, "kya scene hai")]


def test_gemini_units_are_parsed_cached_and_offset():
    lines = [(1250.0, 1253.0, "tu noob hai"), (1260.0, 1262.0, "haha")]
    calls = []

    def ask(prompt):
        calls.append(prompt)
        return json.dumps([{"start": "00:45", "end": "01:05", "type": "roast", "funny": 8, "line": "tu noob hai",
                            "label": "noob"},
                           {"start": "02:00", "end": "02:10", "type": "banter", "funny": 3},    # too weak
                           {"start": "bad", "end": "02:10", "funny": 9}])                       # unreadable

    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmp:
        cache = Path(tmp) / "comedy.json"
        units = comedy.gemini_units(lines, [(1200.0, 1500.0)], cache, ask)
        assert units == [{"start": 1245.0, "end": 1265.0, "funny": 8, "type": "roast", "line": "tu noob hai",
                          "label": "NOOB", "source": "gemini"}]
        assert "tu noob hai" in calls[0] and "00:50" in calls[0]
        assert comedy.gemini_units(lines, [(1200.0, 1500.0)], cache, ask) == units and len(calls) == 1   # cached


def test_rule_units_come_from_laughs_marks_and_rated_talk():
    lines = [(100.0, 103.0, "tera kya hoga"), (104.0, 106.0, "hahaha"), (300.0, 302.0, "clip that")]
    t = np.arange(0, 600, 1.0)
    laugh = np.zeros_like(t)
    laugh[200] = 1.0
    units = comedy.rule_units(lines, 0, 600, {"t": t, "laugh": laugh}, marks=[301.0],
                              talks=[{"start": 400.0, "end": 420.0, "talk_score": 8, "talk_type": "rage", "title": "Gussa"}])
    by = {u["source"]: u for u in units}
    said = next(u for u in units if u["source"] == "laugh" and u["start"] < 150)
    assert said["start"] <= 100.0 and said["end"] >= 106.0                     # from the setup to the laugh
    assert by["marked"]["funny"] == 9 and by["talk"]["type"] == "rage"
    assert any(u["start"] <= 200 <= u["end"] for u in units)                   # the laugh that was heard


def test_tidy_snaps_to_lines_bounds_lengths_and_joins_overlaps():
    lines = [(10.0, 14.0, "a"), (15.0, 19.0, "b"), (60.0, 61.0, "c")]
    units = [{"start": 11.0, "end": 18.0, "funny": 6, "type": "banter", "line": "", "label": "", "source": "gemini"},
             {"start": 16.0, "end": 18.5, "funny": 9, "type": "roast", "line": "b!", "label": "X", "source": "laugh"},
             {"start": 25.0, "end": 80.5, "funny": 7, "type": "story", "line": "", "label": "", "source": "gemini"}]
    out = comedy.tidy(units, lines)
    first = next(u for u in out if u["start"] < 15)
    assert first["start"] == 9.9 and first["end"] >= 19.0 and first["funny"] == 9 and first["line"] == "b!"
    assert "gemini" in first["source"] and "laugh" in first["source"]
    assert all(u["end"] - u["start"] <= comedy.UNIT_S[1] + 0.01 for u in out)


def test_the_window_is_the_first_two_hours_of_bgmi():
    parts = [{"kind": "not_bgmi", "start": 0, "end": 1000}, {"kind": "match", "start": 1000, "end": 4000},
             {"kind": "between", "start": 4000, "end": 4300}, {"kind": "not_bgmi", "start": 4300, "end": 5000},
             {"kind": "match", "start": 5000, "end": 12000}]
    assert comedy.window(parts) == [(1000, 4300), (5000, 8900.0)]


def test_selection_fills_about_eight_minutes_in_stream_order():
    units = [{"start": 100.0 * i, "end": 100.0 * i + 20, "funny": 5 + i % 5} for i in range(60)]
    chosen = comedy.select(units)
    total = sum(u["end"] - u["start"] for u in chosen)
    assert comedy.TARGET_S[0] <= total <= comedy.TARGET_S[1] + 20
    assert [u["start"] for u in chosen] == sorted(u["start"] for u in chosen)
    assert min(u["funny"] for u in chosen) >= 8                        # the best first
    joined = comedy.blocks([{"start": 0.0, "end": 10.0}, {"start": 25.0, "end": 40.0}, {"start": 100.0, "end": 110.0}])
    assert [(b["start"], b["end"], len(b["units"])) for b in joined] == [(0.0, 40.0, 2), (100.0, 110.0, 1)]


def test_overlap_scores():
    kept = [(10.0, 20.0), (100.0, 110.0)]
    assert comedy.overlap_scores([{"start": 22.0, "end": 30.0}], kept) == (0.5, 1.0)     # within 3 s of slack
    assert comedy.overlap_scores([{"start": 50.0, "end": 60.0}], kept) == (0.0, 0.0)


def test_the_comedy_cut_has_a_teaser_face_zooms_clean_text_and_a_black_end():
    from aigcm.studio import comedycut

    segs, units = [], []
    for i in range(30):
        a = 100.0 + 120 * i
        text = "tera lulla dekh" if i == 3 else f"bhai ye line {i} hai"
        segs.append({"start": a + 10, "end": a + 13, "text": text,
                     "words": [{"start": a + 10, "end": a + 13, "word": text}]})
        units.append({"start": a, "end": a + 14, "funny": 9 if i % 3 == 0 else 7, "type": "roast",
                      "line": text, "label": "LOLO" if i % 2 else "", "source": "gemini"})
    stream_map = {"matches": [{"n": 1, "start": 0, "end": 5000}], "parts": []}
    plan = comedycut.plan(units, stream_map, 5000.0, {"segments": segs}, facecam=(0.7, 0.6, 0.3, 0.4))
    pieces = plan["pieces"]
    intro = [p for p in pieces if p["kind"] == "intro"]
    assert 3 <= len(intro) <= 5 and intro[0]["label"] == "IN THIS VIDEO"
    body = [p for p in pieces if p["kind"] == "unit"]
    assert [p["start"] for p in body] == sorted(p["start"] for p in body)          # stream order
    assert all(p.get("punch") for p in body)                                       # the face on every punchline
    words = [o["text"] for p in body for o in p.get("overlays") or []] + [p["title"] for p in body]
    assert not any("LULLA" in w.upper() for w in words)                            # rude words never written
    rude = next((p for p in body if p["start"] <= 460 <= p["end"]), None)
    assert rude is None or rude["captions"] == []
    assert pieces[-1] == {"kind": "card", "text": "", "length": 2.0}
    assert comedy.TARGET_S[0] - 60 <= plan["length"] <= comedy.TARGET_S[1] + 60
    titles, _ = comedycut.titles_for(plan, "Gtx")
    assert titles[0].startswith("GTX & LOLO") and all("LULLA" not in t for t in titles)
    shorts = comedycut.short_moments([u for p in body for u in p["units"]], {"segments": segs})
    assert shorts and shorts[0]["role"] == "teaser"
    assert all(comedycut.hl.SHORT_S[0] <= s["end"] - s["start"] <= comedycut.hl.SHORT_S[1] for s in shorts)
