from aigcm import package, safety, titles
from aigcm.config import Settings


def words(text, start=1.0):
    out, t = [], start
    for w in text.split():
        out.append({"start": round(t, 2), "end": round(t + 0.4, 2), "word": w})
        t += 0.5
    return out


def test_titles_cover_the_three_families_and_stay_short():
    labels = {"type": "multi_kill", "kills": 3, "players_left": 8, "win": False, "marked": False}
    out = titles.suggest(labels, said="Are bhai ye kya tha? Camper ka bachcha.", series=7)
    assert out[0] == "3 FINISHES 1 FIGHT LAST ZONE #7 🔥"
    assert out[1] == "Bhai ye kya tha? 😎"          # the question the streamer asked, with the last-zone emoji
    assert all(len(t) <= titles.MAX_LEN for t in out) and len(out) == 3


def test_judge_title_becomes_the_punchline_with_an_emoji_for_the_kind():
    out = titles.suggest({"type": "rage", "talk": "rage", "kills": 0}, judge_title="Campers se pareshan")
    assert out[0] == "Campers se pareshan 😡"
    # A kill clip leads with its stat; the judge's line comes second with a kill emoji, not the laughing one.
    out = titles.suggest({"type": "fight", "kills": 2, "players_left": 40}, judge_title="Clean Clutches in BGMI!")
    assert out[0] == "DOUBLE FINISH 💀" and out[1] == "Clean Clutches in BGMI! 💀"
    assert titles.clip_emoji({"win": True, "kills": 3}) == "🏆" and titles.clip_emoji({"kills": 1, "players_left": 4}) == "😎"


def test_hashtags_depend_on_channel_size_and_description_carries_the_krafton_line():
    assert len(titles.hashtags("bgmi", 4_000)) == 5 and titles.hashtags("bgmi", 900_000) == ["#bgmi", "#shorts"]
    text = titles.description("https://youtu.be/x", "bgmi", ["#bgmi"], "A clutch.")
    assert text.startswith("Full stream: https://youtu.be/x") and "KRAFTON" in text and text.endswith("#bgmi")


def test_series_counter_continues_from_history():
    assert titles.series_counter(["1v4 LAST ZONE #3 🔥", "DOUBLE FINISH 💀", "1v4 #5"], "1v4") == 6
    assert titles.series_counter([], "1v4") is None


def test_safety_flags_title_gaali_betting_other_games_and_overclaims():
    flags = safety.check("Chutiya camper 1v4 😱", "Use code on 1xbet, also play Free Fire",
                         words("abe bhen ke lode ye kya tha"), {"kills": 1, "win": False})
    kinds = {(f["kind"], f["where"]) for f in flags}
    assert ("profanity", "title") in kinds and ("betting", "description") in kinds
    assert ("other_game", "description") in kinds and ("profanity", "audio") in kinds
    assert ("overclaim", "title") in kinds
    assert not safety.sponsor_safe(flags)


def test_clean_clip_has_no_flags_and_assault_is_not_a_swear():
    assert safety.check("PATT SE HEADSHOT 💀", "Full stream: x", words("assault rifle se finish kiya"), {"kills": 1}) == []


def test_mute_spans_merge_touching_words_and_make_an_ffmpeg_filter():
    spans = safety.mute_spans(words("abe bhen ke lode chal"))     # "bhen ke lode" is one gaali across 3 words
    assert spans == [(1.42, 2.98)]
    assert safety.mute_filter([(1.0, 1.5)]) == "volume=enable='between(t,1.0,1.5)':volume=0"


def test_decorate_fills_every_post_field():
    transcript = {"segments": [{"start": 12.0, "end": 14.0, "text": "ye kya tha bhai", "words": words("ye kya tha bhai", 12.0)}]}
    info = {"source": "https://www.youtube.com/watch?v=abc", "webpage_url": "https://www.youtube.com/watch?v=abc",
            "channel_follower_count": 1200}
    clip = {"start": 10.0, "end": 30.0, "labels": {"type": "fight", "kills": 1, "win": False}, "judge": None}
    package.decorate([clip], info, transcript, Settings())
    assert clip["title"] and len(clip["titles"]) >= 2 and clip["hashtags"][0] == "#bgmi"
    assert "watch?v=abc" in clip["description"] and clip["flags"] == [] and clip["sponsor_safe"]


def test_judge_kind_does_not_relabel_a_kill_clip(tmp_path):
    from aigcm import judge
    from aigcm.jobs import Job, write_json
    job = Job(tmp_path / "j")
    job.path("judge").mkdir()
    write_json(job.path("judge", "m01.json"), {"worth": 7, "type": "rage", "start_trim_s": 0, "end_trim_s": 0})
    write_json(job.path("judge", "m02.json"), {"worth": 6, "type": "banter", "start_trim_s": 0, "end_trim_s": 0})
    fight = {"id": "m01", "start": 0.0, "end": 30.0, "score": 40, "type": "multi_kill", "events": [{"t": 10, "kind": "self_kill"}],
             "labels": {"type": "multi_kill"}}
    talk = {"id": "m02", "start": 100.0, "end": 130.0, "score": 20, "type": "talk", "events": [], "labels": {"type": "talk"}}
    ranked = judge.merge(job, [fight, talk], Settings())
    by_id = {c["id"]: c for c in ranked}
    assert by_id["m01"]["type"] == "multi_kill" and by_id["m01"]["judge_type"] == "rage"
    assert by_id["m02"]["type"] == "banter" and by_id["m02"]["labels"]["type"] == "banter"
