"""The kill-match highlight (Highlights Stage 1, S1.4-S1.5): one match, or the best few in order, told the way
Goblin's and LoLzZz's editors tell it (reports/BGMI creators content A to Z.md, section 3), with the rules from
the viewer study (reports/What holds BGMI viewers.md, section 8; rule numbers below are that section's):

- a fast cold open of 12-20 s (rules 7-11): the best beats of the video (kill bursts, the best lines, moments
  the creator marked), never the Chicken Dinner itself (only the hook text promises it); the first beat matches
  the hook's promise and frame 0 is a shot or a word; hard cuts between beats and one whoosh into the match;
- every fight kept whole with its comms: from the call to the reaction, never ending before the first sentence
  after the last kill has finished (rules 14-15);
- talk scored like kills, with a laugh or shout lifting a moment (rules 2-3); moments marked live always in (5);
- looting, running and waiting cut; no more than about 40 s of footage between two payoffs (16, 19, 20);
- the face: full screen on sentences with no shooting, a short cutaway on the shout after a fight's last kill,
  black and white over the line after a death (25-27); nothing added on kills or on the Dinner banner (23, 28);
- the ending: the Chicken Dinner held to the end of the reaction sentence, or the death and the line after it,
  then 2 s of black (31-32);
- every cut falls on a quiet moment of the sound and never inside a word, with a short fade (22).

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
MERGE_GAP_S = 18.0           # pieces closer than this are joined: the editors studied never cut out less than about 19 s
SKIP_CARD_S = 150.0          # skipping more than this gets "A FEW MINUTES LATER"
CARD_S = 1.8
END_BLACK_S = 2.0
INTRO_S = (12.0, 20.0)       # the cold open's length (rule 8: skips spike when the story starts after 21-35 s)
TALK_MIN_SCORE = 8           # Gemini's talk rating, plus the reaction bonus, for a funny moment to go in
REACT_BONUS = 1.5            # a laugh or shout during or just after a line lifts its rating (rules 2-3)
REACT_MIN = 2.5              # how far above the stream's normal level a shout or laugh must be
REACT_WITHIN_S = 5.0
DINNER_AFTER_S = 8.0
BANNER_FROM_END_S = 6.0      # the Chicken Dinner banner is about this long before the match's end in the map
HOLD_AFTER_S = (3.0, 10.0)   # rule 31: after the banner, to the end of the reaction sentence + 1.5 s
DEATH_AFTER_S = (4.0, 12.0)  # rule 32: after a death, the result and the line said about it
REPLY_PAD_S = 1.5
REPLY_CAP_S = 20.0           # rule 15: a fight runs on to the first sentence after its last kill, at most this far
DROP_AT_S = 65.0             # a look at the drop only when something is said over it (rule 13)
DROP_S = 10.0
DROP_WORDS = 6
PUNCH_S = 2.6
PUNCH_EVERY_S = 30.0         # at most one face punch-in per this much of the video
PUNCH_GAP_S = 18.0
PUNCH_MIN = REACT_MIN
GUNFIRE_QUIET = 0.3          # no gunfire above this around a punch-in
CUTAWAY_S = (1.25, 2.5)      # rule 26: the face on the shout after a fight's last kill
MONO_S = (2.5, 8.0)          # rule 27: the face in black and white over the line after a death
JUMP_FACE_S = 3.0            # rule 17: a sentence starting this soon after a cut covers the jump with the face

# The cold open: beats from the whole video, the one that matches the hook first, then building up.
INTRO_BEATS = 4
BEAT_S = (3.0, 6.0)
BURST_GAP_S = 6.0            # kills this close together are one burst
KILL_ZOOM = 1.12             # a push-in (no longer used on the Dinner banner: rule 28)
KILL_ZOOM_HOLD_S = 2.0
ZOOM_IN_S, ZOOM_OUT_S, ZOOM_LEAD_S = 0.6, 0.4, 0.2
SFX_GAIN = {"whoosh": 0.55, "boom": 0.45}

# Pacing (rule 19): a payoff (kill, shooting, a reaction, a rated line, a marked moment) at least this often.
PACE_MAX_S = 40.0
PACE_AFTER_S = 12.0          # kept after the earlier payoff
PACE_BEFORE_S = 10.0         # and before the next
FINAL_KEEP_S = 60.0          # the last minute before a match's end is never trimmed (rule 20)
MARK_BEFORE_S, MARK_AFTER_S = 15.0, 8.0   # a moment marked live: markers point a little after the moment
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


def reaction_level(sounds):
    """(times, level): how far above the stream's normal the loudest shout or laugh is at each moment, in
    units of its usual spread (2.5 = a clear shout). None without the sound classes."""
    if not sounds or "t" not in sounds:
        return None
    level = None
    for group in ("scream", "laugh"):
        if group in sounds:
            values = sounds[group]
            base = float(np.median(values)) + 1e-3
            spread = float(np.percentile(values, 90) - np.median(values)) + 1e-3
            lv = (values - base) / spread
            level = lv if level is None else np.maximum(level, lv)
    return (sounds["t"], level) if level is not None else None


def reaction_at(level, a, b):
    """The strongest reaction in [a, b] as (time, level), or None."""
    if level is None:
        return None
    t, lv = level
    mask = (t >= a) & (t <= b)
    if not mask.any():
        return None
    i = int(np.argmax(np.where(mask, lv, -np.inf)))
    return float(t[i]), float(lv[i])


def reacted(level, a, b):
    found = reaction_at(level, a, b)
    return bool(found and found[1] >= REACT_MIN)


def sentence_after(t, words, within=6.0, gap=0.6, longest=8.0):
    """The first run of words starting in [t, t + within] (a sentence: pauses under `gap`), as (start, end)."""
    i = next((k for k, w in enumerate(words) if t <= w[0] <= t + within), None)
    if i is None:
        return None
    start, end = words[i]
    for a, b in words[i + 1:]:
        if a - end > gap or b - start > longest:
            break
        end = b
    return start, end


def first_sound(t, words, shots, within=2.5):
    """Frame 0 on a voice line or a shot (rule 9): the next word or shot at or after t, just before it."""
    found = [a for a, _ in words if t <= a <= t + within] + [float(x) for x in shots if t <= x <= t + within]
    inside = next((a for a, b in words if a < t < b), None)
    if inside is not None:
        return inside - 0.1
    return (min(found) - 0.1) if found else t


def _shots(sounds, at=0.5):
    """Times of the streamer's own shooting (louder, closer shots)."""
    return sounds["t"][sounds["gunfire"] >= at] if sounds and "gunfire" in sounds else np.array([])


def scored_talks(talks, level):
    """The rated talk moments with their value: Gemini's rating, lifted when a laugh or shout comes with the
    line or within 5 s of it (rules 2-3)."""
    out = []
    for c in talks or []:
        rating = c.get("talk_score") or 0
        if not rating:
            continue
        lifted = reacted(level, c["start"], c["end"] + REACT_WITHIN_S)
        out.append(dict(c, value=rating + (REACT_BONUS if lifted else 0.0), reacted=lifted))
    return out


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
    reply = sentence_after(last, words)
    if reply:
        # Rule 15: never before the first sentence after the last kill has finished, plus 1.5 s.
        end = max(end, min(reply[1] + REPLY_PAD_S, last + REPLY_CAP_S))
    return {"kind": "fight", "start": max(lo, start), "end": min(hi, end), "kills": fight.get("kills", 0)}


QUIET_CUT_S = 20.0           # inside a fight, a stretch this long with no shooting and no talk is cut out
QUIET_KEEP_S = 2.0           # with this much kept either side of it
SHOT_ON = 0.5                # gunfire score that counts as the streamer's fight (louder, closer shots)
SETTLE_S = 1.2               # a cut moves up to this far to a quiet moment of the sound
FADE_IN_S, FADE_OUT_S = 0.08, 0.15


def quiet_spans(a, b, words, sounds, least=QUIET_CUT_S, kills=()):
    """Stretches inside [a, b] at least `least` long with no shooting, no kill and nobody talking: the looting,
    running and waiting an editor cuts out of a fight. Everything else stays, so the game's movement is never
    chopped. Without the sound classes there is no evidence of quiet, so nothing is cut."""
    if not sounds or "gunfire" not in sounds:
        return []
    busy = [w for w in words if w[1] > a and w[0] < b] + [(k - 3.0, k + 3.0) for k in kills]
    if sounds and "gunfire" in sounds:
        t, gun = sounds["t"], sounds["gunfire"]
        busy += [(float(x) - 0.5, float(x) + 0.5) for x in t[(gun >= SHOT_ON) & (t >= a) & (t <= b)]]
    busy.sort()
    out, cursor = [], a
    for s0, s1 in busy:
        if s0 - cursor >= least:
            out.append((cursor, s0))
        cursor = max(cursor, s1)
    if b - cursor >= least:
        out.append((cursor, b))
    return out


def fight_pieces(fight, words, audio, lo, hi, sounds=None):
    """A fight whole, from the call or first shots to the reaction; long stretches inside it with no shooting
    and no talk are left out (Goblin's editor keeps a 162 s final fight in one piece)."""
    whole = fight_piece(fight, words, audio, lo, hi)
    spans = quiet_spans(whole["start"], whole["end"], words, sounds, kills=fight.get("kill_times") or ())
    pieces = cut_out(whole, spans)
    for p in pieces:
        p["kills"] = sum(1 for t in fight.get("kill_times", []) if p["start"] <= t <= p["end"])
    return pieces


def cut_out(piece, spans, keep=QUIET_KEEP_S):
    """The piece without the given stretches (keeping `keep` s either side of each). A piece after a cut is
    marked as a jump, so a face shot can cover it (rule 17)."""
    pieces, cursor = [], piece["start"]
    for q0, q1 in spans:
        if q0 + keep - cursor > 3:
            pieces.append(dict(piece, start=cursor, end=q0 + keep))
        cursor = q1 - keep
    pieces.append(dict(piece, start=cursor, end=piece["end"]))
    for p in pieces[1:]:
        p["jump"] = True
    return [p for p in pieces if p["end"] - p["start"] > 2]


def settle(t, side, words, audio):
    """Move a cut to the quietest moment of the sound within SETTLE_S that is not inside a word, so a cut
    never lands in the middle of a burst of gunfire or a shout; then out of any word."""
    if audio and "t" in audio and "loudness" in audio:
        times, loud = audio["t"], audio["loudness"]
        mask = (times >= t - SETTLE_S) & (times <= t + SETTLE_S)
        best = None
        for x, level in zip(times[mask], loud[mask]):
            if any(a - 0.05 <= x <= b + 0.05 for a, b in words):
                continue
            if best is None or level < best[1] - 1e-9 or (abs(level - best[1]) <= 1e-9 and abs(x - t) < abs(best[0] - t)):
                best = (float(x), float(level))
        if best is not None:
            t = best[0]
    return snap(t, words, side)


def _value(c):
    return c.get("value", c.get("talk_score") or 0)


def _talk_pieces(match, talks):
    out = []
    for c in talks or []:
        if _value(c) >= TALK_MIN_SCORE and match["start"] <= c["start"] and c["end"] <= match["end"] + 3:
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


def ending_span(match, words, duration):
    """The ending (rules 31-32) as (start, end, line): the Chicken Dinner banner held to the end of the first
    reaction sentence + 1.5 s (3-10 s), or the death and the line said about it (4-12 s). `line` is that
    sentence, or None."""
    hi = min(duration, match["end"])
    if match["ended"] == "dinner":
        at, (least, most) = hi - BANNER_FROM_END_S, HOLD_AFTER_S
        start = at - DINNER_AFTER_S + 2
    else:
        at, (least, most) = hi, DEATH_AFTER_S
        start = max(match["start"], hi - 6)
    line = sentence_after(at - 0.5, words, within=6.0)
    end = at + (min(most, max(least, line[1] + REPLY_PAD_S - at)) if line else least + 1.0)
    return start, min(duration, end), line


def payoffs(match, sounds, level, talks, marks=()):
    """Times something pays off in a match: kills, the streamer's shooting, a shout or laugh, a rated line, a
    moment marked live, and the end."""
    lo, hi = match["start"], match["end"]
    out = [t for f in match.get("fights") or [] for t in f.get("kill_times") or []]
    out += [x for a, b, n in shooting_runs(sounds, lo, hi, threshold=SHOT_ON) if n >= 3 for x in np.arange(a, b + 0.1, 2.0)]
    if level is not None:
        t, lv = level
        out += [float(x) for x in t[(lv >= REACT_MIN) & (t >= lo) & (t <= hi)]]
    out += [x for c in talks or [] if _value(c) >= TALK_MIN_SCORE - 1 and lo <= c["start"] <= hi
            for x in np.arange(c["start"], c["end"] + 0.1, 2.0)]
    out += [t for t in marks if lo <= t <= hi] + [hi]
    return sorted(float(x) for x in out)


def pace(pieces, times, protect_from):
    """Rule 19: inside a piece, a stretch longer than PACE_MAX_S with no payoff keeps only PACE_AFTER_S after
    the earlier payoff and PACE_BEFORE_S before the next. Never after `protect_from` (the last minute)."""
    out = []
    for p in pieces:
        if p["kind"] in ("ending", "talk", "marked"):
            out.append(p)
            continue
        inside = [t for t in times if p["start"] <= t <= p["end"]]
        spans = []
        for a, b in zip(inside, inside[1:]):
            a2, b2 = a + PACE_AFTER_S, min(b, protect_from) - PACE_BEFORE_S
            if b - a > PACE_MAX_S and b2 - a2 > MERGE_GAP_S:
                spans.append((a2, b2))
        out += cut_out(p, spans, keep=0.0) if spans else [p]
    return out


def match_pieces(match, words, audio, talks, duration, sounds=None, marks=(), level=None):
    """The kept stretches of one match, in order, with their edges out of words."""
    lo, hi = match["start"], min(duration, match["end"])
    kills = [t for f in match.get("fights") or [] for t in f.get("kill_times") or []]
    end_start, end_end, _ = ending_span(match, words, duration)
    pieces = [p for f in match["fights"] for p in fight_pieces(f, words, audio, lo, hi + DINNER_AFTER_S, sounds)]
    pieces += _talk_pieces(match, talks)
    # Rule 5: a moment the creator marked live (chat !clip, the button, "clip that") always goes in.
    pieces += [{"kind": "marked", "start": max(lo, t - MARK_BEFORE_S), "end": min(hi, t + MARK_AFTER_S)}
               for t in marks if lo <= t <= hi]
    if match["ended"] == "dinner" or (match.get("placement") or 99) <= 3:
        # The last circles, kept, but without dead holds of 20 s or more ending over a minute before the end
        # (rule 20).
        final = {"kind": "fight", "start": max(lo, hi - FINAL_STRETCH_S), "end": min(hi, end_start + 1), "kills": 0,
                 "final": True}
        pieces += cut_out(final, quiet_spans(final["start"], hi - FINAL_KEEP_S, words, sounds, kills=kills))
    if _length(pieces) < MIN_BODY_S:
        # Few kills: the gunfights that had none tell the match too (a Dinner with 3 kills is still a fight).
        for first, last, n in sorted(shooting_runs(sounds, lo, hi), key=lambda r: -r[2]):
            if n < EXTRA_SHOTS or _length(pieces) >= MIN_BODY_S:
                break
            if any(p["start"] <= first and last <= p["end"] for p in pieces):
                continue
            # Rule 21: only a gunfight that carries talk or a reaction (when there is talk and sound to tell).
            if (words or level is not None) and not (reacted(level, first - 3, last + REACT_WITHIN_S)
                                                     or any(first - 3 <= a <= last + 5 for a, _ in words)):
                continue
            pieces.append({"kind": "fight", "start": max(lo, first - EXTRA_PAD[0]), "end": min(hi, last + EXTRA_PAD[1]),
                           "kills": 0})
    if not match["fights"] or match["fights"][0]["start"] - lo > 120:
        # Rule 13: the story starts on the first fight's call; the drop only when a plan is said over it.
        drop = lo + DROP_AT_S
        if drop + DROP_S < hi and sum(1 for a, _ in words if drop <= a <= drop + DROP_S) >= DROP_WORDS:
            pieces.append({"kind": "drop", "start": drop, "end": drop + DROP_S})
    pieces.append({"kind": "ending", "start": end_start, "end": end_end})
    pieces = _merge(pieces)
    if sounds is not None:
        pieces = pace(pieces, payoffs(match, sounds, level, talks, marks), hi - FINAL_KEEP_S)
    limit = min(duration, settle(end_end, "end", words, audio))
    for p in pieces:
        p["start"] = round(max(0.0, settle(p["start"], "start", words, audio)), 2)
        p["end"] = round(min(limit, settle(p["end"], "end", words, audio)), 2)
        p["match"] = match["n"]
    return [p for p in _merge(pieces) if p["end"] - p["start"] > 1]


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


def cold_open(matches, talks, words, sounds=None, audio=None, marks=(), level=None):
    """The intro (rules 7-12): the best beats of the video, 3-6 s each and 12-20 s in all. Beats are kill
    bursts (more kills, later in the match, with a shout after = bigger), the best lines (rated like kills) and
    moments marked live; never the Chicken Dinner banner or the kill that won it, which the viewer waits for.
    The first beat is the one the hook promises (kills, or the best line), starting on a shot or a word; the
    rest build up. Hard cuts between beats; the one whoosh is on the way into the match (see plan)."""
    shots = _shots(sounds, SHOT_ON)
    beats = []
    for m in matches:
        fights = m.get("fights") or []
        banner = m["end"] - BANNER_FROM_END_S if m["ended"] == "dinner" else None
        for first, last, n in bursts([t for f in fights for t in f.get("kill_times") or []]):
            if banner is not None and last >= banner - 30:
                continue                     # the winning kill stays for the end
            late = any(f["start"] <= first <= f["end"] and (f.get("players_left") or 99) <= 15 for f in fights)
            # From the shots that lead to the kill (or 2.5 s before it) to when the shooting stops.
            onset = first - 2.5
            before = shots[(shots >= first - 4.0) & (shots <= first)] if len(shots) else shots
            if len(before):
                onset = float(before.min()) - 0.6
            after = shots[(shots >= last) & (shots <= last + 3.0)] if len(shots) else shots
            settle_at = (float(after.max()) if len(after) else last) + 0.8
            b = min(settle_at, onset + BEAT_S[1] + 2)
            react = reacted(level, last, last + REACT_WITHIN_S)
            beats.append({"score": 3.0 * n + (3 if late else 0) + (3 if react else 0), "start": onset,
                          "end": max(b, onset + BEAT_S[0]), "kills": n, "match": m["n"], "why": "kills"})
        for t in marks:
            if m["start"] <= t <= m["end"] and (banner is None or t < banner - 30):
                beats.append({"score": 14.0, "start": t - 4.0, "end": t + 1.5, "kills": 0, "match": m["n"],
                              "why": "marked"})
    for c in talks or []:
        value = _value(c)
        peak = c.get("peak") or (c["start"] + c["end"]) / 2
        home = next((m for m in matches if m["start"] <= peak <= m["end"]), None)
        if value >= TALK_MIN_SCORE and home is not None:
            start = c["start"] if peak - c["start"] <= 4.0 else peak - 3.0
            beats.append({"score": 3.0 * value - 12, "start": start, "end": max(peak + 2.5, start + BEAT_S[0]),
                          "kills": 0, "match": home["n"], "why": "funny", "captions": True})
    promise = "kills" if sum(m["kills"] for m in matches) >= 3 else "funny"
    # The beat the hook promises leads (rule 9); the others are capped so the hook isn't left unshown.
    ranked = sorted(beats, key=lambda b: -b["score"])
    lead = next((b for b in ranked if b["why"] == promise), None)
    if lead is not None:
        ranked = [lead] + [b for b in ranked if b is not lead]
    chosen, total = [], 0.0
    for b in ranked:
        if len(chosen) >= INTRO_BEATS:
            break
        if lead is not None and b["why"] != promise and sum(1 for c in chosen if c["why"] != promise) >= 2:
            continue
        if not all(b["end"] <= c["start"] - 1 or b["start"] >= c["end"] + 1 for c in chosen):
            continue
        room = INTRO_S[1] - total
        if room < BEAT_S[0]:
            break
        b = dict(b, end=min(b["end"], b["start"] + room))
        chosen.append(b)
        total += b["end"] - b["start"]
    if not chosen:
        return []
    text = intro_text(matches)
    lead = chosen[0] if lead is not None else max(chosen, key=lambda b: b["score"])   # ranked put it first
    chosen = [lead] + sorted((b for b in chosen if b is not lead), key=lambda b: b["score"])
    out = []
    for i, b in enumerate(chosen):
        # Frame 0 is a shot or a word (rule 9); later beats start on the quietest moment, out of words.
        start = first_sound(b["start"], words, shots) if i == 0 else settle(b["start"], "start", words, audio)
        piece = {"kind": "intro", "start": round(max(0.0, start), 2),
                 "end": round(settle(b["end"], "end", words, audio), 2), "match": b["match"], "kills": b["kills"],
                 "text": text, "sfx": [], "why": b["why"]}
        if piece["end"] - piece["start"] > BEAT_S[1] + 2.5:     # a word ran long: keep the beat short
            piece["end"] = round(piece["start"] + BEAT_S[1] + 2.5, 2)
        if b.get("captions"):
            piece["captions"] = True
        out.append(piece)
    while len(out) > 1 and sum(p["end"] - p["start"] for p in out) > INTRO_S[1] + 0.5:
        over = sum(p["end"] - p["start"] for p in out) - INTRO_S[1]
        last = out[-1]
        if last["end"] - last["start"] - over >= BEAT_S[0]:
            last["end"] = round(last["end"] - over, 2)
        else:
            out.pop()
    out[0]["label"] = "IN THIS VIDEO"
    return out


def effects(pieces, kill_times, talks):
    """What a piece shows on top of the footage. Nothing on kills and nothing on the Chicken Dinner banner
    (rules 23, 28: none of the 18 videos measured adds zooms or sounds there; the game's own kill feed and
    recoil carry them). The rated lines get subtitles."""
    funny = [(c["start"], c["end"]) for c in talks or [] if _value(c) >= TALK_MIN_SCORE]
    for p in pieces:
        if p["kind"] == "card":
            continue
        p["zooms"] = []
        p["sfx"] = list(p.get("sfx") or [])
        if p["kind"] == "talk":
            p["captions"] = True
        else:
            spans = [[round(max(a, p["start"]) - p["start"], 2), round(min(b, p["end"]) - p["start"], 2)]
                     for a, b in funny if a < p["end"] and b > p["start"]]
            if spans:
                p["captions"] = spans
    return pieces


PUNCH_SENTENCE_S = (1.2, 6.0)   # a punch-in lasts the sentence, within these bounds


def punch_ins(pieces, sounds, audio, limit, transcript=None):
    """The face full screen while the streamer talks or reacts and nobody is shooting, held for the whole
    sentence (JokerClips: a hard cut in on the line, a hard cut back after it). Sentences in talk pieces come
    first, and a sentence just after a cut, where the face covers the jump in position (rule 17); then the ones
    with the biggest laugh or shout."""
    if limit <= 0 or not transcript:
        return {}
    shots = _shots(sounds, GUNFIRE_QUIET)
    level = reaction_level(sounds)
    candidates = []
    for seg in transcript.get("segments", []):
        a, b = seg.get("start"), seg.get("end")
        if a is None or b is None or not (PUNCH_SENTENCE_S[0] <= b - a <= PUNCH_SENTENCE_S[1] + 2):
            continue
        b = min(b, a + PUNCH_SENTENCE_S[1])
        if len(shots) and ((shots >= a - 1.0) & (shots <= b + 0.5)).any():
            continue                     # shooting: the game is the story, the face stays small
        host = next((i for i, p in enumerate(pieces) if p["kind"] not in ("card", "intro")
                     and p["start"] <= a and b <= p["end"] - 0.3), None)
        if host is None:
            continue
        p = pieces[host]
        jump = bool(p.get("jump")) and a - p["start"] <= JUMP_FACE_S
        if jump:
            a = p["start"] + 0.1         # from the cut itself, so the face hides the jump
            b = min(b, a + PUNCH_SENTENCE_S[1])
        elif a < p["start"] + 0.5:
            continue
        found = reaction_at(level, a, b)
        score = (found[1] if found else 0.0) + (5.0 if p["kind"] == "talk" or jump else 0.0)
        if score >= PUNCH_MIN or p["kind"] == "talk":
            candidates.append((score, a, b, host))
    chosen = []
    for score, a, b, host in sorted(candidates, reverse=True):
        if all(abs(a - c[0]) >= PUNCH_GAP_S for c in chosen):
            chosen.append((a, b, host))
        if len(chosen) >= limit:
            break
    out = {}
    for a, b, host in sorted(chosen):
        out.setdefault(host, []).append([round(a - 0.1, 2), round(b + 0.2, 2)])
    return out


def cutaways(pieces, matches, level, words, taken):
    """Rule 26: the face for 1.25-2.5 s on a shout or laugh right after a fight's last kill, from 0.5 s after
    the kill, as {piece index: [[start, end]]}."""
    out = {}
    for m in matches:
        for f in m.get("fights") or []:
            if not f.get("kill_times"):
                continue
            last = max(f["kill_times"])
            found = reaction_at(level, last + 0.5, last + 4.0)
            if not found or found[1] < REACT_MIN:
                continue
            a = max(last + 0.5, found[0] - 0.5)
            line = sentence_after(a - 0.3, words, within=1.0, longest=CUTAWAY_S[1])
            b = a + (min(CUTAWAY_S[1], max(CUTAWAY_S[0], line[1] + 0.1 - a)) if line else 2.0)
            host = next((i for i, p in enumerate(pieces) if p["kind"] not in ("card", "intro")
                         and p["start"] <= a and b <= p["end"] - 0.3), None)
            if host is None or any(not (b <= x0 or a >= x1) for x0, x1 in taken.get(host, [])):
                continue
            out.setdefault(host, []).append([round(a, 2), round(b, 2)])
    return out


def mono_faces(pieces, matches, words, duration):
    """Rule 27: after a death, the face in black and white over the line said about it (2.5-8 s)."""
    out = {}
    for m in matches:
        if m["ended"] == "dinner" or (m.get("placement") or 99) <= 3:
            continue
        _, _, line = ending_span(m, words, duration)
        if not line:
            continue
        a = line[0] - 0.1
        b = min(line[0] + MONO_S[1], max(line[1] + 0.3, a + MONO_S[0]))
        host = next((i for i, p in enumerate(pieces) if p["kind"] not in ("card", "intro")
                     and p["start"] <= a and b <= p["end"] + 0.01), None)
        if host is not None:
            out.setdefault(host, []).append([round(a, 2), round(min(b, pieces[host]["end"]), 2)])
    return out


def plan(stream_map, match_numbers, duration, transcript=None, sounds=None, audio=None, talks=(), facecam=None,
         marks=()):
    """The piece list for a highlight of the given matches (one: a match highlight; several: the session
    version with MATCH cards). Each piece is {"kind", "start", "end"} in source seconds, or a card
    {"kind": "card", "text", "length"}. `marks` are times the creator marked live."""
    words = _words(transcript)
    matches = [m for m in stream_map["matches"] if m["n"] in match_numbers]
    matches.sort(key=lambda m: m["start"])
    if not matches:
        raise ValueError("no such match in the map")
    level = reaction_level(sounds)
    talks = scored_talks(talks, level)
    body, kept = [], 0.0
    for k, m in enumerate(matches):
        pieces = match_pieces(m, words, audio, talks, duration, sounds, marks, level)
        if len(matches) > 1:
            body.append({"kind": "card", "text": f"MATCH {k + 1}", "length": CARD_S, "match": m["n"]})
        for i, p in enumerate(pieces):
            if i and p["start"] - pieces[i - 1]["end"] >= SKIP_CARD_S:
                body.append({"kind": "card", "text": "A FEW MINUTES LATER", "length": CARD_S, "match": m["n"]})
            body.append(p)
            kept += p["end"] - p["start"]
    kill_times = [t for m in matches for f in m.get("fights") or [] for t in f.get("kill_times") or []]
    effects(body, kill_times, talks)
    intro = effects(cold_open(matches, talks, words, sounds, audio, marks, level), kill_times, talks)
    if intro:
        # Rule 11: hard cuts inside the cold open; one whoosh on the way into the match.
        first = next((p for p in body if p["kind"] != "card"), None)
        if first is not None:
            first["sfx"] = [["whoosh", 0.0]] + first["sfx"]
    pieces = intro + body + [{"kind": "card", "text": "", "length": END_BLACK_S}]
    total = sum(p.get("length") or (p["end"] - p["start"]) for p in pieces)
    if facecam:
        for i, spans in punch_ins(pieces, sounds, audio, int(total // PUNCH_EVERY_S), transcript).items():
            pieces[i]["punch"] = spans
            # What is said while the face fills the screen gets subtitles.
            p = pieces[i]
            extra = [[round(a - p["start"], 2), round(b - p["start"], 2)] for a, b in spans]
            if p.get("captions") is not True:
                p["captions"] = (p.get("captions") or []) + extra
        taken = {i: [tuple(s) for s in p.get("punch") or []] for i, p in enumerate(pieces)}
        for i, spans in cutaways(pieces, matches, level, words, taken).items():
            pieces[i]["punch"] = sorted((pieces[i].get("punch") or []) + spans)
        for i, spans in mono_faces(pieces, matches, words, duration).items():
            pieces[i]["mono"] = spans
            # The black-and-white face covers its own stretch; no colour punch-in under it.
            pieces[i]["punch"] = [s for s in pieces[i].get("punch") or []
                                  if all(s[1] <= a or s[0] >= b for a, b in spans)]
            p = pieces[i]
            if p.get("captions") is not True:
                p["captions"] = (p.get("captions") or []) + [[round(a - p["start"], 2), round(b - p["start"], 2)]
                                                             for a, b in spans]
        for p in pieces:
            if "punch" in p and not p["punch"]:
                del p["punch"]
    span = sum(m["end"] - m["start"] for m in matches)
    return {"matches": [m["n"] for m in matches], "pieces": pieces, "length": round(total, 1),
            "kept": round(kept / span, 3) if span else 0, "kills": sum(m["kills"] for m in matches),
            "facecam": list(facecam) if facecam else None}


# --- what goes with the video: Shorts, titles, the channel label ----------------------------------------------

SHORT_S = (15.0, 60.0)       # rule 37: hits run 19-60 s (owner, 14 Nov: one high-impact moment each)
SHORT_AIM_S = (20.0, 45.0)   # and most sit here
SHORTS_MAX = 4               # rule 36: offer 3-5
SHORT_LEAD_S = 7.0           # the run-up before the first kill of a burst
SHORT_GAME_AFTER_S = 1.5     # rule 39: after the last kill, a little game...
SHORT_FACE_S = (1.25, 3.5)   # ...then the face reacting; never ending on the kill frame
SHORT_MIN_SCORE = 6.0
SHORT_BURST_GAP_S = 15.0     # a Short takes a whole fight's kills, as long as it fits in SHORT_S
RECORD_KILLS = 15
BAND_WORDS = 6               # rule 42: the hook band names the person or situation in 2-6 words and one emoji


def band(text, emoji="😂"):
    """The Short's hook band: at most BAND_WORDS words and exactly one emoji."""
    words = [w for w in (text or "").split() if any(ch.isalnum() for ch in w)]
    has = next((ch for ch in (text or "") if ord(ch) > 0x2600 and not ch.isalnum()), None)
    return " ".join(words[:BAND_WORDS]) + " " + (has or emoji) if words else emoji


def _reaction_end(last, words, level):
    """Rule 39: where a kill Short ends: 1.5 s of game after the last kill, then the face while the streamer
    reacts (the sentence said, 1.25-3.5 s), so it never ends on the kill frame. Returns (end, face span)."""
    line = sentence_after(last, words, within=3.0)
    if line:
        face_end = min(line[1] + 0.3, last + SHORT_GAME_AFTER_S + SHORT_FACE_S[1])
    else:
        found = reaction_at(level, last, last + 4.0)
        face_end = (found[0] + 1.0) if found and found[1] >= REACT_MIN else last + SHORT_GAME_AFTER_S + 1.5
    face_end = max(face_end, last + SHORT_GAME_AFTER_S + SHORT_FACE_S[0])
    face_end = min(face_end, last + SHORT_GAME_AFTER_S + SHORT_FACE_S[1])
    return face_end, (last + SHORT_GAME_AFTER_S, face_end)


def quote(transcript, a, b):
    """A line said in [a, b] for a Short's hook band when the moment has no title: the longest sentence of
    3-8 words, else None."""
    lines = [seg.get("text", "").strip() for seg in (transcript or {}).get("segments", [])
             if seg.get("start") is not None and a <= seg["start"] and seg.get("end", 1e9) <= b]
    from ..safety import GAALI, SLURS

    lines = [t for t in lines if 3 <= len(t.split()) <= 8 and not GAALI.search(t) and not SLURS.search(t)]
    return max(lines, key=lambda t: len(t.split()), default=None)


def short_moments(the_plan, stream_map=None, talks=(), words=(), sounds=None, marks=(), transcript=None):
    """The Shorts (rules 35-43): person moments first, from anywhere in the stream (rule 36), 15-60 s each.
    Rated lines and banter (a laugh or shout lifts them), moments marked live, then kill bursts and the Chicken
    Dinner, which need a reaction or a clutch to rank high (rule 35). Each starts on a shot or a word (38) and
    ends on the reaction, never on the kill frame (39). The teaser (posted before the video) is never the
    Dinner, which the video keeps for its end (43). Fewer Shorts rather than weak ones."""
    matches = list((stream_map or {}).get("matches", []))
    level = reaction_level(sounds)
    shots = _shots(sounds, SHOT_ON)
    talks = scored_talks(talks, level)
    candidates = []
    for m in matches:
        fights = m.get("fights") or []
        for first, last, n in bursts([t for f in fights for t in f.get("kill_times") or []], SHORT_BURST_GAP_S):
            late = any(f["start"] <= first <= f["end"] and (f.get("players_left") or 99) <= 15 for f in fights)
            quick = n >= 2 and last - first <= 10
            react = reacted(level, last, last + REACT_WITHIN_S)
            role = "clutch" if late and n >= 2 else "fight"
            score = 4.0 * n + (4 if late else 0) + (2 if quick else 0) + (8 if react else 0)
            if level is not None and not react and role != "clutch":
                score *= 0.5                 # a kill with no reaction ranks below one with it (rule 3)
            end, face = _reaction_end(last, words, level)
            secs = max(1, round(last - first))
            title = (f"{n} KILLS IN {secs} SECOND{'S' if secs > 1 else ''} 🔥" if quick and n >= 3
                     else "LAST CIRCLE CLUTCH 😱" if role == "clutch" else f"{n} KILLS 🔥" if n >= 2 else "ONE TAP 🎯")
            candidates.append({"score": score, "start": first - SHORT_LEAD_S, "end": end, "kills": n, "match": m["n"],
                               "role": role, "title": title, "face": face})
        if m["ended"] == "dinner":
            banner = m["end"] - BANNER_FROM_END_S
            kills = [t for f in fights for t in f.get("kill_times") or []] + list(m.get("kill_times") or [])
            last_kill = max([t for t in kills if t <= banner] or [banner - 15])
            react = reacted(level, banner - 10, banner + REACT_WITHIN_S)     # the shout at the win, or after
            end, face = _reaction_end(banner, words, level)
            candidates.append({"score": 25.0 + (15 if react else 0), "start": last_kill - SHORT_LEAD_S, "end": end,
                               "kills": 0, "match": m["n"], "role": "dinner", "title": "CHICKEN DINNER 🏆", "face": face})
    for c in talks:
        if _value(c) >= TALK_MIN_SCORE:
            home = next((m["n"] for m in matches if m["start"] <= c["start"] <= m["end"]), None)
            candidates.append({"score": 6.0 * _value(c) - 20, "start": c["start"], "end": c["end"], "kills": 0,
                               "role": "funny", "match": home,
                               "title": band(c.get("title") or quote(transcript, c["start"], c["end"]) or "FUNNY MOMENT")})
    for t in marks:
        home = next((m["n"] for m in matches if m["start"] <= t <= m["end"]), None)
        candidates.append({"score": 30.0, "start": t - 20.0, "end": t + 6.0, "kills": 0, "role": "marked",
                           "title": "WATCH THIS 😱", "match": home})
    numbers = set(the_plan.get("matches") or [])
    for c in candidates:
        if c["match"] in numbers:   # the highlight's own Dinner first (posted after it); on a tie, its matches
            c["score"] += 10.0 if c["role"] == "dinner" else 0.5
    chosen = []
    for c in sorted(candidates, key=lambda c: -c["score"]):
        if c["score"] < SHORT_MIN_SCORE and chosen:
            break
        if c["role"] == "dinner" and any(o["role"] == "dinner" for o in chosen):
            continue                 # one Dinner Short is enough
        if words:
            c["end"] = snap(c["end"], words, "end")
        longest = SHORT_AIM_S[1] if c["role"] == "dinner" else SHORT_S[1]
        length = c["end"] - c["start"]
        if length < SHORT_AIM_S[0]:
            c["start"] = c["end"] - SHORT_AIM_S[0]     # more of the setup
        elif length > longest:
            c["start"] = c["end"] - longest
        # Frame 0 on a shot or the first word of the setup (rule 38).
        c["start"] = first_sound(c["start"], words, shots, within=3.0)
        if c["end"] - c["start"] < SHORT_S[0]:
            c["start"] = c["end"] - SHORT_S[0]
        if all(c["end"] <= o["start"] or c["start"] >= o["end"] for o in chosen):
            chosen.append(c)
        if len(chosen) >= SHORTS_MAX:
            break
    teaser = next((c for c in chosen if c["role"] != "dinner"), None)
    if teaser is not None:
        chosen = [teaser] + [c for c in chosen if c is not teaser]
    out = []
    for c in chosen:
        item = {"role": "teaser" if c is teaser else c["role"], "kind": c["role"], "start": round(max(0.0, c["start"]), 2),
                "end": round(c["end"], 2), "kills": c["kills"], "match": c["match"], "title": c["title"]}
        if c.get("face") and c["start"] < c["face"][0] < c["end"] - 0.5:
            item["face"] = [round(c["face"][0], 2), round(min(c["face"][1], c["end"]), 2)]
        out.append(item)
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


def reaction_peaks(the_plan, sounds, most=8, apart=10.0):
    """The loudest shouts and laughs inside the video, as [(time, level)]: where the thumbnail's face comes from
    (rule 48: 83 of 93 thumbnails show an expressive face)."""
    level = reaction_level(sounds)
    if level is None:
        return []
    t, lv = level
    inside = np.zeros_like(t, dtype=bool)
    for p in the_plan["pieces"]:
        if p["kind"] != "card":
            inside |= (t >= p["start"]) & (t <= p["end"])
    out = []
    for i in np.argsort(-np.where(inside, lv, -np.inf)):
        if not inside[i] or lv[i] < REACT_MIN or len(out) >= most:
            break
        if all(abs(float(t[i]) - x) >= apart for x, _ in out):
            out.append((float(t[i]), round(float(lv[i]), 2)))
    return out


CATCH_MIN = 3               # a phrase said this often in the video is its catchphrase
CATCH_SKIP = set("""bhai bhaiya haan han nahi nahin kya kyu kyun hai hain hoon hun tha thi the ho hota hoti hote raha rahe
    rahi gaya gaye gayi gya kar karo karna karke kiya kiye mein main mai mera meri mere tera teri tere apna apni
    aur bhi toh to abhi yaar yeh woh wo vo aaja aaja chal chalo dekh dekho bol bolo sun suno kuch koi kaise kaisa
    kahan jaa ja jao aa aaya aayi aao wala wali wale liye unko usko isko iska uska uske iske hamare hum tum aap
    ab phir fir sab bas acha accha achha theek thik matlab karte karta karti raho rakho dena dedo diya liya
    like subscribe share comment channel stream live the and you what yes yeah okay ok bro hello guys this
    that there here they for with not but are was its it's like just go come get one""".split())


def catchphrase(the_plan, transcript):
    """The phrase (2-3 words) said most often inside the video, at least CATCH_MIN times, with at least two
    words that aren't filler: what viewers quote and retitle videos after (rule 46)."""
    from collections import Counter

    from ..safety import GAALI, SLURS

    if not transcript:
        return None
    spans = [(p["start"], p["end"]) for p in the_plan["pieces"] if p["kind"] not in ("card", "intro")]
    said = [w.get("word", "").strip(" .,!?\"'").lower() for seg in transcript.get("segments", [])
            for w in seg.get("words", []) if any(a <= w.get("start", -1) <= b for a, b in spans)]
    said = [w for w in said if w]
    counts = Counter()
    for n in (3, 2):
        for i in range(len(said) - n + 1):
            gram = said[i:i + n]
            text = " ".join(gram)
            if (sum(1 for w in gram if len(w) >= 3 and w not in CATCH_SKIP) >= 2 and len(set(gram)) == n
                    and not GAALI.search(text) and not SLURS.search(text)):
                counts[text] += 1
    best = max(counts.items(), key=lambda kv: (kv[1], len(kv[0])), default=None)
    return best[0].upper() if best and best[1] >= CATCH_MIN else None


def titles_for(stream_map, numbers, the_plan, names=(), transcript=None):
    """Titles for the highlight (rules 45-47): people first when a name is known, then the result title
    ("CHICKEN DINNER WITH 15 FINISHES", its number the final screen's), the catchphrase and the talk title. A
    match with little at stake (no Dinner, few kills) leads with its best line instead of the result alone."""
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
    phrase = catchphrase(the_plan, transcript)
    if phrase:
        out.insert(1, titles._cut(f"\"{phrase}\" 😂 | {kills} FINISHES | BGMI", titles.LONG_MAX))
    if not dinners and kills < 5 and (talk or phrase):
        out.append(out.pop(0))       # rule 47: a low-stakes match isn't titled on its result alone
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
    what the plan put on it: the hook title and label over the cold open, the face full screen during punch-ins
    and cutaways (black and white over a line after a death), subtitles on rated lines, and the one whoosh into
    the match."""
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
    mono = piece.get("mono") or []
    split = 2 if (punch or mono) and facecam else 1
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
    if (punch or mono) and facecam:
        x, y, cw, ch = facecam
        lines.append(f"{cam_in}crop=iw*{cw:.4f}:ih*{ch:.4f}:iw*{x:.4f}:ih*{y:.4f},"
                     f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1"
                     + ("[cam]" if not (punch and mono) else ",split=2[cam][cam2]"))
        for spans, name, look in ((punch, "punched", ""), (mono, "mono", "hue=s=0,")):
            if not spans:
                continue
            src = "[cam2]" if (name == "mono" and punch) else "[cam]"
            when = "+".join(f"between(t,{a - piece['start']:.2f},{b - piece['start']:.2f})" for a, b in spans)
            if look:
                lines.append(f"{src}{look}null[{name}cam]")
                src = f"[{name}cam]"
            lines.append(f"{base}{src}overlay=0:0:enable='{when}'[{name}]")
            base = f"[{name}]"
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
    fade = f"afade=t=in:d={FADE_IN_S},afade=t=out:st={max(0.0, length - FADE_OUT_S):.3f}:d={FADE_OUT_S}"
    if sounds:
        lines.append(f"{audio}aresample=48000,aformat=channel_layouts=stereo,{fade}[main]")
        for k, (index, at, gain) in enumerate(sounds):
            ms = int(at * 1000)
            lines.append(f"[{index}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms},volume={gain}[fx{k}]")
        lines.append("[main]" + "".join(f"[fx{k}]" for k in range(len(sounds)))
                     + f"amix=inputs={1 + len(sounds)}:duration=first:normalize=0[a]")
    else:
        lines.append(f"{audio}aresample=48000,aformat=channel_layouts=stereo,{fade}[a]")
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


def talk_spans(a, b, transcript, sounds):
    """Sentences inside [a, b] spoken with no shooting around them: when a Short shows the face alone."""
    if not transcript:
        return []
    shots = sounds["t"][sounds["gunfire"] >= GUNFIRE_QUIET] if sounds and "gunfire" in sounds else np.array([])
    out = []
    for seg in transcript.get("segments", []):
        s0, s1 = seg.get("start"), seg.get("end")
        if s0 is None or s1 is None or s0 < a + 1.0 or s1 > b - 0.5 or not (PUNCH_SENTENCE_S[0] <= s1 - s0 <= 8.0):
            continue
        if len(shots) and ((shots >= s0 - 1.0) & (shots <= s1 + 0.5)).any():
            continue
        if out and s0 - out[-1][1] < 2.5:
            out[-1][1] = s1 + 0.2                     # back-to-back sentences: one face moment
        else:
            out.append([s0 - 0.1, s1 + 0.2])
    return [tuple(round(x, 2) for x in span) for span in out]


def join_spans(spans, gap=0.8):
    out = []
    for a, b in sorted(spans):
        if out and a - out[-1][1] < gap:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return out


DARK_MEAN, DARK_SPREAD = 28.0, 8.0   # a camera this dark or this flat (blank, covered) is no face to show


def face_lit(source, box, times):
    """Whether the camera box shows something: most sampled frames neither dark nor blank."""
    from .thumbs import grab

    lit = seen = 0
    for t in times:
        frame = grab(source, t)
        if frame is None:
            continue
        h, w = frame.shape[:2]
        x, y, bw, bh = box
        crop = frame[int(y * h):int((y + bh) * h), int(x * w):int((x + bw) * w)]
        if crop.size == 0:
            continue
        gray = crop.mean(axis=2)
        seen += 1
        lit += float(gray.mean()) >= DARK_MEAN and float(gray.std()) >= DARK_SPREAD
    return seen == 0 or lit * 2 >= seen


def render_short(moment, source, info, out, title, facecam, transcript, kit_defaults=None, threads=3, game=None,
                 sounds=None, said=None):
    """One Short from the highlight, through the Studio renderer with a clip's default edit (layout, camera,
    hook title, captions), so it can be opened in the editor like any clip. The face goes big while the streamer
    talks with no shooting and on the reaction after the last kill; a dark or blank camera is left out and the
    Short shows the game alone (rule 41)."""
    from . import hook
    from .edit import default_edit
    from .render import render as render_edit

    if facecam and not face_lit(source, facecam, [moment["start"] + 2, (moment["start"] + moment["end"]) / 2,
                                                  moment["end"] - 2]):
        log(f"highlight: the camera is dark in {Path(out).name}; game only")
        facecam = None
    edit = default_edit(moment["start"], moment["end"], info["width"], info["height"], title,
                        moment.get("events") or (), captions=bool(transcript), facecam=facecam, brand=kit_defaults,
                        game=game)
    if any(p.role == "cam" for p in edit.layout.panels):
        from .edit import FaceSpan

        spans = talk_spans(moment["start"], moment["end"], said or transcript, sounds)
        if moment.get("face"):
            spans = join_spans(list(spans) + [tuple(moment["face"])])
        edit = edit.model_copy(update={"face": [FaceSpan(start=a, end=b) for a, b in spans][:20]})
    picture = hook.for_edit(Path(out).parent / "hooks", edit)
    render_edit(edit, source, 0.0, info.get("has_audio", True), out, transcript=transcript, threads=threads,
                hook_png=picture)
    return edit
