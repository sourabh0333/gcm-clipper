"""Makes each ranked clip post-ready: titles, hashtags, description, safety flags and bleep spans."""

from . import safety, titles
from .transcript import text_between, words_between


def decorate(ranked, info, transcript, settings, history=()):
    game = settings.game
    tags = titles.hashtags(game, info.get("channel_follower_count"))
    stream_url = info.get("webpage_url") if str(info.get("source", "")).startswith("http") else ""
    for clip in ranked:
        labels = clip.get("labels", {})
        words = words_between(transcript, clip["start"], clip["end"])
        said = text_between(transcript, clip["start"], clip["end"])
        verdict = clip.get("judge") or {}
        series = titles.series_counter(history, "1v4") if (labels.get("kills") or 0) >= 3 else None
        clip["titles"] = titles.suggest(labels, said, verdict.get("title") or None, series)
        clip["title"] = clip["titles"][0] if clip["titles"] else clip.get("title", "")
        clip["hashtags"] = tags
        clip["description"] = titles.description(stream_url, game, tags, verdict.get("summary", ""))
        clip["flags"] = safety.check(clip["title"], clip["description"], words, labels)
        clip["mute_spans"] = safety.mute_spans(words)
        clip["sponsor_safe"] = safety.sponsor_safe(clip["flags"])
    return ranked
