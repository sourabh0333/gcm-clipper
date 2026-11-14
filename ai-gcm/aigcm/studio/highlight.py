"""The kill-match highlight (Highlights Stage 1, S1.4-S1.5): one match, or the best few in order, told the way
Goblin's and LoLzZz's editors tell it (reports/BGMI creators content A to Z.md, section 3):

- a fast cold open (owner, 14 Nov: "the intro is the most crucial part"): the 3-4 best beats of the video
  (kill bursts, the funniest line, the Chicken Dinner last), 3-6 s each, building up, under a big hook title,
  with a whoosh between beats;
- every fight kept whole with its comms: from the call or first shot to the reaction after the last kill;
- the funniest talk inside the match;
- looting, running and waiting cut, with "A FEW MINUTES LATER" only where a lot is skipped;
- "MATCH 2", "MATCH 3" cards in the session version;
- the ending: the Chicken Dinner or the last fight, a few seconds of the face, then black;
- the editing follows the action (owner, 14 Nov): a quick zoom on every kill, a punchy sound on a burst of
  kills, the face full screen on big reactions, and subtitles on the funny lines.

The stream layout stays as it is (16:9, vertical streams over a blurred copy). No music under speech, no kill
counter, no chapters, no film or TV memes. Length is whatever the match needs.

plan() works on the stream map and the job's saved signals only, so it is quick and testable; render() makes
the video with ffmpeg."""

import shutil
import tempfile
from pathlib import Path

import numpy as np

from ..jobs import log

LEAD_S = 8.0                 # before a fight's first shot or kill
CALL_BACK_S = 16.0           # at most this far back to catch the call that starts a fight
TAIL_S = 6.0                 # after a fight's last kill
REACTION_MAX_S = 10.0        # the reaction after it, while the excitement lasts
EXCITED = 1.0
MERGE_GAP_S = 6.0            # pieces closer than this are joined (no jump cut for a few seconds)
SKIP_CARD_S = 150.0          # skipping more than this gets "A FEW MINUTES LATER"
CARD_S = 1.8
END_BLACK_S = 2.0
TEASER_S = (15.0, 25.0)
TALK_MIN_SCORE = 8           # Gemini's talk rating (or the rules' score) for a funny moment to go in
DINNER_AFTER_S = 8.0
ENDING_FACE_S = 4.0
DROP_AT_S = 65.0             # without a fight early on, a short look at the drop: about when the plane leaves
DROP_S = 10.0
PUNCH_S = 2.6
PUNCH_EVERY_S = 30.0         # at most one face punch-in per this much of the video
PUNCH_GAP_S = 18.0
PUNCH_MIN = 2.5              # how far above the stream's normal level a shout or laugh must be

# The cold open: beats from the whole video, built up to the biggest one.
INTRO_BEATS = 4
BEAT_S = (3.0, 6.0)
BURST_GAP_S = 6.0            # kills this close together are one burst
KILL_ZOOM = 1.18             # the quick zoom on a kill (the frame grows this much, centred on the crosshair)
KILL_ZOOM_HOLD_S = 0.9
ZOOM_IN_S, ZOOM_OUT_S, ZOOM_LEAD_S = 0.18, 0.3, 0.25
BOOM_KILLS = 2               # a burst of this many kills gets a punchy sound
SFX_GAIN = {"whoosh": 0.55, "boom": 0.45}
CAPTION_SIZE = 84            # subtitles: big and bold, like JokerClips'
CAPTION_MARGIN = 250         # above the streamer's own overlay bar at the foot of the frame
HOOK_Y = 170                 # the cold open's hook, under the "IN THIS VIDEO" label

WIDE = (1920, 1080)
FPS = 30


def _words(transcript):
    if not transcript:
        return []
    return sorted(((w["start"], w["end"]) for seg in transcript.get("segments", []) for w in seg.get("words", [])
                   if w.get("end", 0) > w.get("start", 0)), key=lambda w: w[0])


def snap(t, words, side):
    """Move a cut out of the middle of a word: a start goes to before the word, an end to after it. Also
    lets a sentence that is still going finish (up to 3 s) at an end, and catches its start at a start."""
    for a, b in words:
        if a - 0.05 <= t <= b + 0.05:
            return a - 0.1 if side == "start" else b + 0.15
    if side == "end":
        nxt = [(a, b) for a, b in words if t < a <= t + 0.6]
        if nxt:
            # Speech continues right after the cut: run on to the end of that run of words, up to 3 s.
            end = nxt[0][1]
            for a, b in words:
                if end < a <= end + 0.4 and b <= t + 3.0:
                    end = b
            return end + 0.15
    return t


CALL_GAP_S = 12.0            # talk that ended this close before a fight is its call ("enemy aage hai")


def _speech_before(t, words, limit):
    """Where the call before a fight began: the run of talk that ended at most CALL_GAP_S before t (or is still
    going), not earlier than limit."""
    before = [w for w in words if w[0] < t and w[0] >= limit]
    near = [w for w in before if w[1] >= t - CALL_GAP_S]
    if not near:
        return t
    start = near[0][0]
    for a, b in reversed([w for w in before if w[0] < start]):
        if b < start - 1.2:
            break
        start = a
    return start


def _excited_until(t, audio, limit):
    if not audio or "t" not in audio:
        return t
    times, ex = audio["t"], audio["excitement"]
    i = int(np.searchsorted(times, t))
    while i < len(times) and times[i] <= limit and ex[i] > EXCITED:
        i += 1
    return float(times[min(i, len(times) - 1)]) if len(times) else t


def fight_piece(fight, words, audio, lo, hi):
    """One fight, whole: the call before it, every shot and kill, and the reaction after."""
    first = fight["start"]
    last = max([fight["end"]] + fight.get("kill_times", []))
    start = min(first - LEAD_S, _speech_before(first, words, first - CALL_BACK_S))
    end = max(last + TAIL_S, _excited_until(last, audio, last + REACTION_MAX_S))
    return {"kind": "fight", "start": max(lo, start), "end": min(hi, end), "kills": fight.get("kills", 0)}


LONG_FIGHT_S = 90.0          # a fight longer than this is cut down to its kills (the walking between goes)
POINT_BEFORE_S, POINT_AFTER_S = 15.0, 8.0


def fight_pieces(fight, words, audio, lo, hi):
    """A short fight whole; a long one (a busy match where the kills never stop) as a window around each kill
    and knock, joined where they touch, with the run-up before the first and the reaction after the last."""
    points = sorted(fight.get("points") or fight.get("kill_times") or [])
    if fight["end"] - fight["start"] <= LONG_FIGHT_S or len(points) < 2:
        return [fight_piece(fight, words, audio, lo, hi)]
    windows = []
    for t in points:
        a, b = t - POINT_BEFORE_S, t + POINT_AFTER_S
        if windows and a - windows[-1][1] <= MERGE_GAP_S:
            windows[-1][1] = b
        else:
            windows.append([a, b])
    windows[0][0] = min(windows[0][0], fight["start"] - LEAD_S)
    last = points[-1]
    windows[-1][1] = max(windows[-1][1], _excited_until(last, audio, last + REACTION_MAX_S))
    out = []
    for a, b in windows:
        kills = sum(1 for t in fight.get("kill_times", []) if a <= t <= b)
        out.append({"kind": "fight", "start": max(lo, a), "end": min(hi, b), "kills": kills})
    return out


def _talk_pieces(match, talks):
    out = []
    for c in talks or []:
        score = c.get("talk_score") or 0
        if score >= TALK_MIN_SCORE and match["start"] <= c["start"] and c["end"] <= match["end"] + 3:
            out.append({"kind": "talk", "start": c["start"], "end": c["end"], "title": c.get("title") or ""})
    return out


def _merge(pieces):
    pieces = sorted(pieces, key=lambda p: p["start"])
    out = []
    for p in pieces:
        if out and p["start"] - out[-1]["end"] <= MERGE_GAP_S:
            last = out[-1]
            last["end"] = max(last["end"], p["end"])
            last["kills"] = last.get("kills", 0) + p.get("kills", 0)
            if p["kind"] in ("ending",) or last["kind"] != p["kind"]:
                last["kind"] = p["kind"] if p["kind"] == "ending" else last["kind"]
        else:
            out.append(dict(p))
    return out


FINAL_STRETCH_S = 180.0      # a Dinner or a top-3 finish: the last circles are the story, kept whole
MIN_BODY_S = 240.0           # a match cut shorter than this gets the heaviest shooting that had no kill
EXTRA_SHOTS = 6              # gunfire samples (about 1 s each) a no-kill gunfight needs to be added
EXTRA_PAD = (6.0, 5.0)


def shooting_runs(sounds, lo, hi, pause=4.0, threshold=0.3):
    """Gunfire heard between lo and hi as [(first, last, samples)], pauses up to `pause` s joined."""
    if not sounds or "gunfire" not in sounds:
        return []
    t, gun = sounds["t"], sounds["gunfire"]
    shots = t[(gun >= threshold) & (t >= lo) & (t <= hi)]
    runs = []
    for x in shots:
        if runs and x - runs[-1][1] <= pause:
            runs[-1][1] = float(x)
            runs[-1][2] += 1
        else:
            runs.append([float(x), float(x), 1])
    return [tuple(r) for r in runs]


def _length(pieces):
    return sum(p["end"] - p["start"] for p in _merge([dict(p) for p in pieces]))


def match_pieces(match, words, audio, talks, duration, sounds=None):
    """The kept stretches of one match, in order, with their edges out of words."""
    lo, hi = match["start"], min(duration, match["end"])
    pieces = [p for f in match["fights"] for p in fight_pieces(f, words, audio, lo, hi + DINNER_AFTER_S)]
    pieces += _talk_pieces(match, talks)
    if match["ended"] == "dinner" or (match.get("placement") or 99) <= 3:
        pieces.append({"kind": "fight", "start": max(lo, hi - FINAL_STRETCH_S), "end": hi, "kills": 0, "final": True})
    if _length(pieces) < MIN_BODY_S:
        # Few kills: the gunfights that had none tell the match too (a Dinner with 3 kills is still a fight).
        for first, last, n in sorted(shooting_runs(sounds, lo, hi), key=lambda r: -r[2]):
            if n < EXTRA_SHOTS or _length(pieces) >= MIN_BODY_S:
                break
            if any(p["start"] <= first and last <= p["end"] for p in pieces):
                continue
            pieces.append({"kind": "fight", "start": max(lo, first - EXTRA_PAD[0]), "end": min(hi, last + EXTRA_PAD[1]),
                           "kills": 0})
    if not match["fights"] or match["fights"][0]["start"] - lo > 120:
        drop = lo + DROP_AT_S
        if drop + DROP_S < hi:
            pieces.append({"kind": "drop", "start": drop, "end": drop + DROP_S})
    # The ending: the Dinner banner and the face after it, or the last moments before the match ended.
    if match["ended"] == "dinner":
        pieces.append({"kind": "ending", "start": hi - DINNER_AFTER_S - 4, "end": min(duration, hi + ENDING_FACE_S)})
    else:
        pieces.append({"kind": "ending", "start": max(lo, hi - 6), "end": min(duration, hi + ENDING_FACE_S)})
    pieces = _merge(pieces)
    for p in pieces:
        p["start"] = round(max(0.0, snap(p["start"], words, "start")), 2)
        p["end"] = round(min(duration, snap(p["end"], words, "end")), 2)
        p["match"] = match["n"]
    return _merge(pieces)


def bursts(kill_times, gap=BURST_GAP_S):
    """Kills close together, as [(first, last, count)]."""
    out = []
    for t in sorted(kill_times):
        if out and t - out[-1][1] <= gap:
            out[-1] = (out[-1][0], t, out[-1][2] + 1)
        else:
            out.append((t, t, 1))
    return out


def intro_text(matches):
    """The hook over the cold open: the result in a few words."""
    kills = sum(m["kills"] for m in matches)
    dinner = any(m["ended"] == "dinner" or m.get("placement") == 1 for m in matches)
    if dinner and kills:
        return f"{kills} KILLS + CHICKEN DINNER 🏆"
    if dinner:
        return "CHICKEN DINNER 🏆"
    if kills >= 3:
        return f"{kills} KILLS 🔥"
    return "WATCH TILL THE END 😱"


def cold_open(matches, talks, words):
    """The intro: the best beats of the video, 3-6 s each, the biggest last. Beats are kill bursts (the more
    kills and the later in the match, the bigger), the funniest talk moments, and the Chicken Dinner."""
    beats = []
    for m in matches:
        left = {f["start"]: f.get("players_left") for f in m.get("fights") or []}
        for first, last, n in bursts([t for f in m.get("fights") or [] for t in f.get("kill_times") or []]):
            late = any(f["start"] <= first <= f["end"] and (f.get("players_left") or 99) <= 15
                       for f in m.get("fights") or [])
            a = first - 2.5
            b = min(last + 2.0, a + BEAT_S[1])
            beats.append({"score": 3.0 * n + (3 if late else 0), "start": a, "end": max(b, a + BEAT_S[0]),
                          "kills": n, "match": m["n"], "why": "kills"})
        if m["ended"] == "dinner":
            banner = m["end"] - DINNER_AFTER_S + 2
            beats.append({"score": 100.0, "start": banner - 3.0, "end": banner + 2.5, "kills": 0, "match": m["n"],
                          "why": "dinner"})
        del left
    for c in talks or []:
        rating = c.get("talk_score") or 0
        peak = c.get("peak") or (c["start"] + c["end"]) / 2
        if rating >= TALK_MIN_SCORE and any(m["start"] <= peak <= m["end"] for m in matches):
            beats.append({"score": 2.0 * rating - 6, "start": peak - 3.0, "end": peak + 2.5, "kills": 0,
                          "match": next(m["n"] for m in matches if m["start"] <= peak <= m["end"]), "why": "funny",
                          "captions": True})
    chosen = []
    for b in sorted(beats, key=lambda b: -b["score"]):
        if all(b["end"] <= c["start"] - 1 or b["start"] >= c["end"] + 1 for c in chosen):
            chosen.append(b)
        if len(chosen) >= INTRO_BEATS:
            break
    if not chosen:
        return []
    chosen.sort(key=lambda b: (b["why"] == "dinner", b["score"]))     # build up; the Dinner closes it
    text = intro_text(matches)
    out = []
    for i, b in enumerate(chosen):
        piece = {"kind": "intro", "start": round(max(0.0, snap(b["start"], words, "start")), 2),
                 "end": round(snap(b["end"], words, "end"), 2), "match": b["match"], "kills": b["kills"],
                 "text": text, "sfx": [["whoosh", 0.0]] if i else [], "why": b["why"]}
        if piece["end"] - piece["start"] > BEAT_S[1] + 2.5:     # a word ran long: keep the beat short
            piece["end"] = round(piece["start"] + BEAT_S[1] + 2.5, 2)
        if b.get("captions"):
            piece["captions"] = True
        out.append(piece)
    out[0]["label"] = "IN THIS VIDEO"
    return out


def effects(pieces, kill_times, talks):
    """What each kept piece shows on top of the footage: a quick zoom on every kill, a punchy sound at the
    end of a burst of kills, and subtitles on the funny lines (talk pieces and funny moments inside fights)."""
    funny = [(c["start"], c["end"]) for c in talks or [] if (c.get("talk_score") or 0) >= TALK_MIN_SCORE]
    for p in pieces:
        if p["kind"] == "card":
            continue
        inside = [t for t in kill_times if p["start"] + 0.3 <= t <= p["end"] - 0.3]
        zooms = []
        for t in inside:
            if not zooms or t - zooms[-1] > KILL_ZOOM_HOLD_S + ZOOM_OUT_S:
                zooms.append(t)
        p["zooms"] = [round(t - p["start"], 2) for t in zooms]
        sfx = list(p.get("sfx") or [])
        for first, last, n in bursts(inside):
            if n >= BOOM_KILLS:
                sfx.append(["boom", round(last - p["start"], 2)])
        p["sfx"] = sfx
        if p["kind"] == "talk":
            p["captions"] = True
        else:
            # Only the funny lines inside a fight get subtitles, not the whole stretch.
            spans = [[round(max(a, p["start"]) - p["start"], 2), round(min(b, p["end"]) - p["start"], 2)]
                     for a, b in funny if a < p["end"] and b > p["start"]]
            if spans:
                p["captions"] = spans
    return pieces


def punch_ins(pieces, sounds, audio, limit):
    """Face full screen for a moment on the biggest shouts and laughs inside the kept footage."""
    if limit <= 0:
        return {}
    peaks = []
    if sounds and "t" in sounds:
        t = sounds["t"]
        for group in ("scream", "laugh"):
            if group not in sounds:
                continue
            values = sounds[group]
            base = float(np.median(values)) + 1e-3
            spread = float(np.percentile(values, 90) - np.median(values)) + 1e-3
            level = (values - base) / spread
            peaks += [(float(level[i]), float(t[i])) for i in range(len(t)) if level[i] >= PUNCH_MIN]
    if audio and "t" in audio:
        peaks += [(float(v) / 2, float(t)) for t, v in zip(audio["t"], audio["excitement"]) if v >= 2 * PUNCH_MIN]
    inside = [(v, t) for v, t in peaks if any(p["start"] + 1 <= t <= p["end"] - PUNCH_S for p in pieces
                                              if p["kind"] not in ("card", "teaser", "intro"))]
    # Every funny talk piece gets the face at its loudest moment (or its middle), the reaction being the joke.
    for p in pieces:
        if p["kind"] == "talk" and p["end"] - p["start"] > PUNCH_S + 2:
            near = [(v, t) for v, t in peaks if p["start"] + 1 <= t <= p["end"] - PUNCH_S]
            inside.append((99.0, max(near)[1] if near else (p["start"] + p["end"] - PUNCH_S) / 2))
    chosen = []
    for v, t in sorted(inside, reverse=True):
        if all(abs(t - c) >= PUNCH_GAP_S for c in chosen):
            chosen.append(t)
        if len(chosen) >= limit:
            break
    out = {}
    for t in sorted(chosen):
        i = next(i for i, p in enumerate(pieces) if p["kind"] not in ("card", "teaser", "intro")
                 and p["start"] + 1 <= t <= p["end"] - PUNCH_S)
        out.setdefault(i, []).append([round(t - 0.3, 2), round(t - 0.3 + PUNCH_S, 2)])
    return out


def plan(stream_map, match_numbers, duration, transcript=None, sounds=None, audio=None, talks=(), facecam=None):
    """The piece list for a highlight of the given matches (one: a match highlight; several: the session
    version with MATCH cards). Each piece is {"kind", "start", "end"} in source seconds, or a card
    {"kind": "card", "text", "length"}."""
    words = _words(transcript)
    matches = [m for m in stream_map["matches"] if m["n"] in match_numbers]
    matches.sort(key=lambda m: m["start"])
    if not matches:
        raise ValueError("no such match in the map")
    body, kept = [], 0.0
    for k, m in enumerate(matches):
        pieces = match_pieces(m, words, audio, talks, duration, sounds)
        if len(matches) > 1:
            body.append({"kind": "card", "text": f"MATCH {k + 1}", "length": CARD_S, "match": m["n"]})
        for i, p in enumerate(pieces):
            if i and p["start"] - pieces[i - 1]["end"] >= SKIP_CARD_S:
                body.append({"kind": "card", "text": "A FEW MINUTES LATER", "length": CARD_S, "match": m["n"]})
            body.append(p)
            kept += p["end"] - p["start"]
    kill_times = [t for m in matches for f in m.get("fights") or [] for t in f.get("kill_times") or []]
    effects(body, kill_times, talks)
    intro = effects(cold_open(matches, talks, words), kill_times, talks)
    pieces = intro + body + [{"kind": "card", "text": "", "length": END_BLACK_S}]
    total = sum(p.get("length") or (p["end"] - p["start"]) for p in pieces)
    if facecam:
        for i, spans in punch_ins(pieces, sounds, audio, int(total // PUNCH_EVERY_S)).items():
            pieces[i]["punch"] = spans
    span = sum(m["end"] - m["start"] for m in matches)
    return {"matches": [m["n"] for m in matches], "pieces": pieces, "length": round(total, 1),
            "kept": round(kept / span, 3) if span else 0, "kills": sum(m["kills"] for m in matches),
            "facecam": list(facecam) if facecam else None}


# --- what goes with the video: Shorts, titles, the channel label ----------------------------------------------

SHORT_S = (15.0, 40.0)       # owner, 14 Nov: Shorts and Reels are for one high-impact moment, kept short
SHORTS_MAX = 3
SHORT_LEAD_S = 7.0           # the run-up before the first kill of a burst
SHORT_TAIL_S = 4.0           # and the reaction after the last
SHORT_MIN_SCORE = 6.0
SHORT_BURST_GAP_S = 15.0     # a Short takes a whole fight's kills, as long as it fits in SHORT_S
RECORD_KILLS = 15


def short_moments(the_plan, stream_map=None, talks=(), words=()):
    """The Shorts cut from a highlight: only high-impact moments, each 15-40 s, from the run-up to the
    reaction. Kill bursts (more kills, faster, later in the match = bigger), the Chicken Dinner (the last kill
    and the banner), and the funniest talk. Fewer Shorts rather than weak ones."""
    numbers = the_plan.get("matches") or []
    matches = [m for m in (stream_map or {}).get("matches", []) if m["n"] in numbers]
    candidates = []
    for m in matches:
        fights = m.get("fights") or []
        for first, last, n in bursts([t for f in fights for t in f.get("kill_times") or []], SHORT_BURST_GAP_S):
            late = any(f["start"] <= first <= f["end"] and (f.get("players_left") or 99) <= 15 for f in fights)
            quick = n >= 2 and last - first <= 10
            score = 4.0 * n + (4 if late else 0) + (2 if quick else 0)
            a, b = first - SHORT_LEAD_S, last + SHORT_TAIL_S
            role = "clutch" if late and n >= 2 else "fight"
            title = (f"{n} KILLS IN {max(1, round(last - first))} SECONDS 🔥" if quick and n >= 3
                     else "LAST CIRCLE CLUTCH 😱" if role == "clutch" else f"{n} KILLS 🔥" if n >= 2 else "ONE TAP 🎯")
            candidates.append({"score": score, "start": a, "end": b, "kills": n, "match": m["n"], "role": role,
                               "title": title})
        if m["ended"] == "dinner":
            banner = m["end"] - DINNER_AFTER_S + 2
            last_kill = max([t for t in m.get("kill_times") or [] if t <= banner] or [banner - 15])
            a = max(last_kill - SHORT_LEAD_S, banner - SHORT_S[1] + SHORT_TAIL_S)
            candidates.append({"score": 50.0, "start": a, "end": banner + SHORT_TAIL_S, "kills": 0, "match": m["n"],
                               "role": "dinner", "title": "CHICKEN DINNER 🏆"})
    for c in talks or []:
        rating = c.get("talk_score") or 0
        if rating >= TALK_MIN_SCORE and any(m["start"] <= c["start"] <= m["end"] for m in matches):
            candidates.append({"score": 1.5 * rating, "start": c["start"], "end": c["end"], "kills": 0, "role": "funny",
                               "title": (c.get("title") or "FUNNY MOMENT 😂")[:60], "match": None})
    chosen = []
    for c in sorted(candidates, key=lambda c: -c["score"]):
        if c["score"] < SHORT_MIN_SCORE and chosen:
            break
        length = c["end"] - c["start"]
        if length < SHORT_S[0]:
            c["start"] = c["end"] - SHORT_S[0]
        elif length > SHORT_S[1]:
            c["start"] = c["end"] - SHORT_S[1]
        if words:
            c["start"], c["end"] = snap(c["start"], words, "start"), min(c["start"] + SHORT_S[1] + 2, snap(c["end"], words, "end"))
        if all(c["end"] <= o["start"] or c["start"] >= o["end"] for o in chosen):
            chosen.append(c)
        if len(chosen) >= SHORTS_MAX:
            break
    out = []
    for i, c in enumerate(chosen):
        out.append({"role": "teaser" if i == 0 else c["role"], "kind": c["role"], "start": round(max(0.0, c["start"]), 2),
                    "end": round(c["end"], 2), "kills": c["kills"], "match": c["match"], "title": c["title"]})
    return out


def channel_label(stream_map, numbers):
    """Where the highlight fits (decision 5, a suggestion): a record match goes on the main channel, like
    LoLzZz's records; a normal match cut on the second channel, like GoBLiN shorts and LoLzZz Plays."""
    kills = [m["kills"] for m in stream_map["matches"] if m["n"] in numbers]
    others = sorted(m["kills"] for m in stream_map["matches"])
    usual = others[len(others) // 2] if others else 0
    if len(numbers) == 1 and kills and kills[0] >= max(RECORD_KILLS, 2 * usual):
        return "main"
    return "second"


def titles_for(stream_map, numbers, the_plan, names=()):
    """Titles for the highlight: the kill title, a people title when a name is known (decision 3: people
    first), and the talk or suspense title."""
    from .. import titles

    matches = [m for m in stream_map["matches"] if m["n"] in numbers]
    kills = sum(m["kills"] for m in matches)
    dinners = sum(1 for m in matches if m["ended"] == "dinner" or m.get("placement") == 1)
    maps = [((m.get("mode") or {}).get("map") or "").upper() for m in matches]
    context = f"{len(matches)} MATCHES" if len(matches) > 1 else (maps[0] if maps and maps[0] else "FULL MATCH")
    talk = next((p.get("title") for p in the_plan["pieces"] if p["kind"] == "talk" and p.get("title")), None)
    out = titles.long_titles(kills, dinners, context, talk)
    if len(matches) == 1 and dinners:
        # One match: "CHICKEN DINNER WITH 15 FINISHES", not "1 CHICKEN DINNER + 15 FINISHES".
        out[0] = titles._cut(f"CHICKEN DINNER WITH {kills} FINISHES | {context} | BGMI" if kills
                             else f"CHICKEN DINNER | {context} | BGMI", titles.LONG_MAX)
    for name in names:
        out.insert(0, titles._cut(f"{name.upper()} vs ME 😱 | {kills} FINISHES | BGMI", titles.LONG_MAX))
    words = titles.thumb_words(kills, dinners)
    return out, words


# --- rendering --------------------------------------------------------------------------------------------

def _card_png(folder, text, box_h=360):
    from . import hook
    return hook.cached(folder, text, "yellow", box_h, backing=False, width=WIDE[0], start_size=190) if text else None


def _label_png(folder, text):
    from . import hook
    return hook.cached(folder, text, "yellow", 230, backing=True, width=WIDE[0], start_size=130)


ENCODE = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-r", str(FPS), "-c:a", "aac", "-b:a", "160k",
          "-ar", "48000", "-ac", "2"]


def render_card(text, out, folder, length):
    from ..media import run, tool

    png = _card_png(folder, text)
    w, h = WIDE
    cmd = [tool("ffmpeg"), "-v", "error", "-y", "-f", "lavfi", "-t", f"{length:.2f}", "-i", f"color=c=black:s={w}x{h}:r={FPS}",
           "-f", "lavfi", "-t", f"{length:.2f}", "-i", "anullsrc=r=48000:cl=stereo"]
    if png:
        cmd += ["-i", str(png), "-filter_complex", f"[0:v][2:v]overlay=0:(H-h)/2,format=yuv420p[v]", "-map", "[v]",
                "-map", "1:a"]
    else:
        cmd += ["-map", "0:v", "-map", "1:a", "-pix_fmt", "yuv420p"]
    run(cmd + ENCODE + ["-shortest", str(Path(out).resolve())])


def zoom_factor(times):
    """The kill zooms as an ffmpeg expression of the piece's time t (1 = no zoom)."""
    terms = []
    for at in times:
        a, b = max(0.0, at - ZOOM_LEAD_S), at + KILL_ZOOM_HOLD_S
        terms.append(f"{KILL_ZOOM - 1:.3f}*clip((t-{a:.3f})/{ZOOM_IN_S},0,1)*clip(({b:.3f}-t)/{ZOOM_OUT_S},0,1)")
    return "1+" + "+".join(terms) if terms else None


def _hook_png(folder, text):
    from . import hook
    return hook.cached(folder, text, "yellow", 260, backing=True, width=WIDE[0], start_size=150)


def render_piece(piece, source, info, out, folder, facecam=None, threads=3, transcript=None):
    """One stretch of the stream at 1920x1080: the layout as streamed (vertical over a blurred copy), with
    what the plan put on it: the hook title and label over the cold open, a quick zoom on each kill, the face
    full screen during punch-ins, subtitles on funny lines, and sounds (a whoosh between intro beats, a boom
    on a burst of kills)."""
    from ..media import run, tool
    from .sound import sfx_file

    w, h = WIDE
    length = piece["end"] - piece["start"]
    vertical = info["height"] > info["width"]
    cmd = [tool("ffmpeg"), "-v", "error", "-y", "-ss", f"{piece['start']:.3f}", "-t", f"{length:.3f}",
           "-i", str(Path(source).resolve())]
    inputs = 1
    label = _label_png(folder, piece["label"]) if piece.get("label") else None
    if label:
        cmd += ["-i", str(label)]
        label_in = inputs
        inputs += 1
    hook_text = _hook_png(folder, piece["text"]) if piece.get("text") and piece["kind"] == "intro" else None
    if hook_text:
        cmd += ["-i", str(hook_text)]
        hook_in = inputs
        inputs += 1
    sounds = []
    for name, at in piece.get("sfx") or []:
        path = sfx_file(name) if info.get("has_audio", True) else None
        if path and 0 <= at < length:
            cmd += ["-i", str(path)]
            sounds.append((inputs, at, SFX_GAIN.get(name, 0.5)))
            inputs += 1
    if not info.get("has_audio", True):
        cmd += ["-f", "lavfi", "-t", f"{length:.3f}", "-i", "anullsrc=r=48000:cl=stereo"]
        silent_in = inputs
        inputs += 1
    punch = piece.get("punch") or []
    split = 2 if punch and facecam else 1
    lines = [f"[0:v]split={split + (1 if vertical else 0)}" + "".join(f"[s{i}]" for i in range(split + (1 if vertical else 0)))]
    if vertical:
        lines += [f"[s0]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},boxblur=24:2[bg]",
                  f"[s1]scale=-2:{h}[fg]", "[bg][fg]overlay=(W-w)/2:0,setsar=1[base]"]
        cam_in = "[s2]"
    else:
        lines.append(f"[s0]scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,setsar=1[base]")
        cam_in = "[s1]"
    base = "[base]"
    zoom = zoom_factor(piece.get("zooms") or [])
    if zoom:
        lines.append(f"{base}scale=w='2*trunc({w}*({zoom})/2)':h='2*trunc({h}*({zoom})/2)':eval=frame,"
                     f"crop={w}:{h}[zoomed]")
        base = "[zoomed]"
    if punch and facecam:
        x, y, cw, ch = facecam
        when = "+".join(f"between(t,{a - piece['start']:.2f},{b - piece['start']:.2f})" for a, b in punch)
        lines += [f"{cam_in}crop=iw*{cw:.4f}:ih*{ch:.4f}:iw*{x:.4f}:ih*{y:.4f},"
                  f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1[cam]",
                  f"{base}[cam]overlay=0:0:enable='{when}'[punched]"]
        base = "[punched]"
    if hook_text:
        lines.append(f"{base}[{hook_in}:v]overlay=0:{HOOK_Y}[hooked]")
        base = "[hooked]"
    if label:
        lines.append(f"{base}[{label_in}:v]overlay=0:40[labelled]")
        base = "[labelled]"
    tail = ""
    work = None
    words = _piece_words(piece, transcript) if piece.get("captions") else []
    if words:
        from .compile import _captions_ass
        from .render import FONTS

        work = Path(tempfile.mkdtemp(prefix="kaatclip_cap_", dir=folder))
        (work / "captions.ass").write_text(_captions_ass(words, size=CAPTION_SIZE, margin=CAPTION_MARGIN),
                                           encoding="utf-8")
        shutil.copytree(FONTS, work / "fonts")
        tail = ",subtitles=captions.ass:fontsdir=fonts"
    lines.append(f"{base}fps={FPS}{tail},format=yuv420p[v]")
    audio = "[0:a:0]" if info.get("has_audio", True) else f"[{silent_in}:a]"
    if sounds:
        lines.append(f"{audio}aresample=48000,aformat=channel_layouts=stereo[main]")
        for k, (index, at, gain) in enumerate(sounds):
            ms = int(at * 1000)
            lines.append(f"[{index}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms},volume={gain}[fx{k}]")
        lines.append("[main]" + "".join(f"[fx{k}]" for k in range(len(sounds)))
                     + f"amix=inputs={1 + len(sounds)}:duration=first:normalize=0[a]")
    else:
        lines.append(f"{audio}aresample=48000,aformat=channel_layouts=stereo[a]")
    cmd += ["-filter_complex", ";".join(lines), "-map", "[v]", "-map", "[a]", *ENCODE, "-threads", str(threads),
            str(Path(out).resolve())]
    try:
        run(cmd, cwd=work) if work else run(cmd)
    finally:
        if work:
            shutil.rmtree(work, ignore_errors=True)


def _piece_words(piece, transcript):
    """The transcript's words inside a piece (or inside its caption spans), in the piece's own time."""
    if not transcript:
        return []
    spans = piece.get("captions")
    spans = spans if isinstance(spans, list) else [[0.0, piece["end"] - piece["start"]]]
    out = []
    for seg in transcript.get("segments", []):
        for w in seg.get("words", []):
            a, b = w.get("start", -1) - piece["start"], w.get("end", 1e9) - piece["start"]
            if any(lo <= a and b <= hi for lo, hi in spans):
                out.append(dict(w, start=a, end=b))
    return out


def render(the_plan, source, info, out, threads=3, progress=None, transcript=None):
    """The highlight video at `out`, from the plan's pieces joined without re-encoding."""
    from .compile import join

    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="kaatclip_hl_", dir=out.parent))
    try:
        parts = []
        for i, piece in enumerate(the_plan["pieces"]):
            part = work / f"part_{i:03d}.mp4"
            if piece["kind"] == "card":
                render_card(piece["text"], part, work, piece["length"])
            else:
                render_piece(piece, source, info, part, work, the_plan.get("facecam"), threads, transcript)
            parts.append(part)
            if progress:
                progress(i + 1, len(the_plan["pieces"]))
        join(parts, out)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    log(f"highlight: {out.name} made from {len(the_plan['pieces'])} pieces, {the_plan['length'] / 60:.1f} min")
    return out


def render_short(moment, source, info, out, title, facecam, transcript, kit_defaults=None, threads=3, game=None):
    """One Short from the highlight, through the Studio renderer with a clip's default edit (layout, camera,
    hook title, zoom on kills, captions), so it can be opened in the editor like any clip."""
    from . import hook
    from .edit import default_edit
    from .render import render as render_edit

    edit = default_edit(moment["start"], moment["end"], info["width"], info["height"], title,
                        moment.get("events") or (), captions=bool(transcript), facecam=facecam, brand=kit_defaults,
                        game=game)
    picture = hook.for_edit(Path(out).parent / "hooks", edit)
    render_edit(edit, source, 0.0, info.get("has_audio", True), out, transcript=transcript, threads=threads,
                hook_png=picture)
    return edit
