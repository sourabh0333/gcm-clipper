"""Turns HUD events and audio signals into scored candidate clips.

Visual events close together form a fight. Each fight's clip starts where the shooting started and ends
after the reaction. Loud spikes with no HUD event become "reaction" candidates, which is where funny
moments usually hide."""

from collections import Counter

import numpy as np

WEIGHTS = {"self_kill": 12, "self_knock": 7, "accolade": 5, "dinner": 20}
EXCITEMENT_PEAK = 2.5
DENSITY_WINDOW_S = 20.0
BACKTRACK_S = 20.0
TAIL_S = 10.0
EDGE_S = 10.0
# YAMNet gunfire score that counts as a shot, and the longest pause that still belongs to one fight.
GUNFIRE_ON = 0.3
GUNFIRE_PAUSE_S = 4.0
# Talk moments (talk.py) score their rule score (about 3-12) or Gemini's 6-10 rating times these, so a good
# conversation ranks with a one- or two-kill fight.
TALK_WEIGHT_RULES = 3.0
TALK_WEIGHT_GEMINI = 5.0


def _index(t, value):
    return int(np.clip(np.searchsorted(t, value), 0, len(t) - 1)) if len(t) else 0


def _densest(events, window):
    times = sorted(e["t"] for e in events)
    best, j = 0, 0
    for i in range(len(times)):
        while times[i] - times[j] > window:
            j += 1
        best = max(best, i - j + 1)
    return best


def _cluster(events, gap):
    clusters, current = [], []
    for e in sorted(events, key=lambda e: e["t"]):
        if current and e["t"] - current[-1]["t"] > gap:
            clusters.append(current)
            current = []
        current.append(e)
    if current:
        clusters.append(current)
    return clusters


def _gunfire_start(first, sounds):
    """When the shooting that led up to `first` began: walk back while gunfire keeps coming, allowing short
    pauses, up to BACKTRACK_S. None if there was no gunfire just before."""
    t, gun = sounds["t"], sounds["gunfire"]
    shots = t[(gun >= GUNFIRE_ON) & (t <= first + 1) & (t >= first - BACKTRACK_S)]
    if not len(shots) or first - shots[-1] > GUNFIRE_PAUSE_S:
        return None
    begin = shots[-1]
    for shot in shots[::-1]:
        if begin - shot > GUNFIRE_PAUSE_S:
            break
        begin = shot
    return float(begin)


def _bounds(first, last, audio, settings, sounds=None):
    """Start where the shooting before the first event began; end once the reaction calms down."""
    t, action, excitement = audio["t"], audio["action"], audio["excitement"]
    start, end = first - settings.pre_roll_s, last + settings.post_roll_s
    began = _gunfire_start(first, sounds) if sounds else None
    if began is not None:
        start = min(start, began - 2.0)
    elif len(t):
        busy = float(np.percentile(action, 75))
        i = _index(t, first)
        while i > 0 and action[i - 1] > busy and first - t[i - 1] <= BACKTRACK_S:
            i -= 1
        start = min(start, float(t[i]) - 2.0)
    if len(t):
        k = _index(t, last)
        while k + 1 < len(t) and excitement[k + 1] > 1.0 and t[k + 1] - last <= TAIL_S:
            k += 1
        end = max(end, float(t[k]) + 1.0)
    return start, end


def _fit(start, end, anchor, settings, duration):
    """Clamp a window to the allowed clip length, keeping `anchor` inside it."""
    length = end - start
    if length < settings.min_clip_s:
        pad = (settings.min_clip_s - length) / 2
        start, end = start - pad, end + pad
    elif length > settings.max_clip_s:
        start = max(start, anchor - settings.max_clip_s / 2)
        end = start + settings.max_clip_s
    shift = max(0.0, -start) - max(0.0, end - duration)
    return round(max(0.0, start + shift), 2), round(min(duration, end + shift), 2)


def _players_left(remaining, t):
    """Players left at time t, from the Remaining counter's change log [(t, value)]."""
    left = None
    for when, value in remaining:
        if when > t:
            break
        left = value
    return left


def _score(cand, audio, settings, remaining=()):
    counts = Counter(e["kind"] for e in cand["events"])
    score = float(sum(WEIGHTS.get(k, 0) * n for k, n in counts.items()))
    reasons = []
    left = _players_left(remaining, cand["end"])
    if left is not None and cand["events"]:
        cand["players_left"] = left
        if left <= 10:
            score += 12
            reasons.append(f"final circles ({left} players left)")
        elif left <= 25:
            score += 5
            reasons.append(f"late game ({left} players left)")
    own_kills, own_knocks = counts["self_kill"], counts["self_knock"]
    if own_kills or own_knocks:
        parts = [f"{n} {word}{'s' if n > 1 else ''}" for n, word in ((own_knocks, "knock"), (own_kills, "kill")) if n]
        reasons.append(f"{' and '.join(parts)} by the streamer")
    if counts["accolade"]:
        reasons.append("Ace Eliminator")
    dense = _densest([e for e in cand["events"] if e["kind"] in ("self_kill", "self_knock")], DENSITY_WINDOW_S)
    if dense >= 4:
        score += 25
        reasons.append(f"{dense} events within {DENSITY_WINDOW_S:.0f}s")
    elif dense == 3:
        score += 15
        reasons.append(f"3 events within {DENSITY_WINDOW_S:.0f}s")
    elif dense == 2:
        score += 6
    if counts["dinner"]:
        reasons.append("chicken dinner")

    t = audio["t"]
    if len(t):
        a, b = _index(t, cand["start"]), _index(t, cand["end"]) + 1
        peak = float(audio["excitement"][a:b].max())
        busy = float(audio["action"][a:b].mean()) / (float(audio["action"].mean()) + 1e-6)
        cand["audio_peak"], cand["action_ratio"] = round(peak, 2), round(busy, 2)
        score += min(max(peak, 0.0), 6.0) * 4
        score += min(busy, 3.0) * 3
        if peak >= EXCITEMENT_PEAK:
            reasons.append("loud reaction")
        if busy >= 2:
            reasons.append("heavy gunfire")
    talk = cand.get("talk_score")
    if talk is not None:
        score += talk * (TALK_WEIGHT_GEMINI if cand["source"] == "gemini" else TALK_WEIGHT_RULES)
        reasons = cand.get("reasons", []) + reasons
    length = cand["end"] - cand["start"]
    if length > 45:
        score -= (length - 45) * 0.3

    if counts["dinner"]:
        kind = "win"
    elif own_kills + own_knocks >= 3 or dense >= 3:
        kind = "multi_kill"
    elif cand["events"]:
        kind = "fight"
    elif talk is not None:
        kind = cand.get("talk_type", "talk")
    else:
        kind = "reaction"
    cand.update(score=round(score, 2), type=kind, reasons=list(dict.fromkeys(reasons)))
    return cand


def _overlap(a, b):
    inter = min(a["end"], b["end"]) - max(a["start"], b["start"])
    if inter <= 0:
        return 0.0
    return inter / min(a["end"] - a["start"], b["end"] - b["start"])


def build(events, audio, settings, duration, remaining=(), sounds=None, talks=()):
    candidates = [dict(t, events=[]) for t in talks]
    useful = [e for e in events if e["kind"] in WEIGHTS]
    for cluster in _cluster(useful, settings.merge_gap_s):
        first, last = cluster[0]["t"], cluster[-1]["t"]
        start, end = _bounds(first, last, audio, settings, sounds)
        anchor = float(np.median([e["t"] for e in cluster]))
        start, end = _fit(start, end, anchor, settings, duration)
        candidates.append({"start": start, "end": end, "events": cluster, "source": "hud"})

    t, excitement = audio["t"], audio["excitement"]
    if len(t):
        min_gap = int(30 / settings.audio_hop_s)
        order = np.argsort(excitement)[::-1]
        taken = []
        for i in order:
            if excitement[i] < EXCITEMENT_PEAK:
                break
            if any(abs(i - j) < min_gap for j in taken):
                continue
            taken.append(i)
            peak_t = float(t[i])
            if peak_t < EDGE_S or peak_t > duration - EDGE_S:
                continue  # a section's cut edge, not a reaction
            if any(c["start"] <= peak_t <= c["end"] for c in candidates):
                continue
            start, end = _fit(peak_t - 10, peak_t + 6, peak_t, settings, duration)
            candidates.append({"start": start, "end": end, "events": [], "source": "audio"})

    scored = sorted((_score(c, audio, settings, remaining) for c in candidates), key=lambda c: -c["score"])
    kept = []
    for cand in scored:
        if any(_overlap(cand, k) > 0.5 for k in kept):
            continue
        kept.append(cand)
        if len(kept) >= settings.max_candidates:
            break
    for n, cand in enumerate(kept, 1):
        cand["id"] = f"m{n:02d}"
        cand["heuristic_rank"] = n
    return kept
