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
    assert any("?" in t or "🤣" in t for t in out)
    assert all(len(t) <= titles.MAX_LEN for t in out) and len(out) == 3


def test_judge_title_becomes_the_punchline():
    out = titles.suggest({"type": "rage", "talk": "rage", "kills": 0}, judge_title="Campers se pareshan")
    assert out[0] == "Campers se pareshan 🤣"


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
