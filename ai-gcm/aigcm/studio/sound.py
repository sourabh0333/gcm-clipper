"""Sound safety (M3.9). A Short over one minute with any active Content ID claim is blocked worldwide; under
a minute it is not (YouTube Help, "three-minute Shorts"). Streamers often play music under the game, so:

- music is found with the sound detector's "Music" score (YAMNet, about once a second, in each job's
  sounds.npz). Under loud game sound YAMNet scores music low, while Content ID still matches quiet music,
  so a few seconds above a modest score count (measured 10 Nov on the 17 test streams: music above 0.3 in
  1-3% of each stream, up to 29% of a clip);
- a clip with music gets a flag, and an edit over 60 s with music gets a strong warning and "cut to 59 s";
- nothing is ever added that someone else owns: the studio's sound effects are synthesised (make_sfx.py)."""

from pathlib import Path

MUSIC_SCORE = 0.3
MUSIC_FLAG_S = 3.0       # this much music in a clip earns the flag
MERGE_GAP_S = 2.0
SFX_DIR = Path(__file__).resolve().parents[2] / "assets" / "sfx"
SFX = ("whoosh", "boom", "ding", "pop")


def music_spans(sounds, lo=0.0, hi=float("inf")):
    """[(start, end)] source spans where music plays, from a job's sound scores (sounds.load), merged
    across gaps under MERGE_GAP_S, within [lo, hi]."""
    if not sounds or "music" not in sounds:
        return []
    times, scores = sounds["t"], sounds["music"]
    step = float(times[1] - times[0]) if len(times) > 1 else 1.0
    spans = []
    for t, score in zip(times, scores):
        if score <= MUSIC_SCORE or t < lo - step or t > hi:
            continue
        a, b = max(lo, float(t)), min(hi, float(t) + step)
        if spans and a - spans[-1][1] <= MERGE_GAP_S:
            spans[-1][1] = b
        else:
            spans.append([a, b])
    return [(round(a, 2), round(b, 2)) for a, b in spans if b > a]


def seconds_in(spans, segments):
    """How many seconds of music survive the edit's parts."""
    total = 0.0
    for a, b in spans:
        for s in segments:
            total += max(0.0, min(b, s.end) - max(a, s.start))
    return total


def job_sounds(folder):
    path = Path(folder) / "sounds.npz"
    if not path.exists():
        return None
    try:
        from ..sounds import load
    except ImportError:   # the light API install (requirements-api.txt) has no numpy: no music check there
        return None
    return load(path)


def music_flag(seconds):
    return {"kind": "music", "text": f"Background music for about {round(seconds)} s: over 1 minute, a claim blocks the Short"}


def clip_music(folder, start, end, sounds=None):
    """Seconds of music in a clip [start, end], or 0 when the job has no sound scores."""
    sounds = sounds if sounds is not None else job_sounds(folder)
    spans = music_spans(sounds, start, end)
    return round(sum(b - a for a, b in spans), 1)


def sfx_file(name):
    path = SFX_DIR / f"{name}.wav"
    return path if name in SFX and path.exists() else None
