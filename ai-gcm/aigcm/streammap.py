"""The stream map (Highlights Stage 1): which parts of a stream are BGMI matches, which are lobby and menus
between them, and which are not BGMI at all (chat with the face full screen, another game, a video), and,
for each match, what happened in it: start and end, how it ended, placement, kills, the fights.

Research (reports/BGMI creators content A to Z.md): every creator's stream mixes these parts, and laughter or
loud talk ranks the wrong ones unless the stream is split first, so the map comes before any ranking.

Built from what the HUD scan saved (vision.py: counter changes, when the counters were on screen, when
"Spectating" was, the text on screen after a match), the sound classes (sounds.py) and the transcript. Gaps
between matches are told apart by reading a frame every so often: BGMI's lobby and menus have their own
words; a gap without them is not BGMI."""

import re

import numpy as np

from .jobs import log

# A match: the in-match HUD (Eliminations, Remaining) on screen. A new match starts where a fresh lobby fills
# (Remaining jumps to 80+ or the Eliminations counter resets to 0), or after a long stretch without the HUD.
NEW_MATCH_GAP_S = 150.0        # no HUD this long between two runs: the next run is another match
MIN_MATCH_S = 90.0             # shorter HUD runs are flickers (a menu showing the counters), not matches
FRESH_LOBBY = 80
END_AFTER_SPECTATE_S = 4.0     # the streamer's own match ends a little before Spectating shows
CUT_OFF_S = 15.0               # a match whose HUD runs this close to the end of the file was cut off
DINNER_TAIL_S = 6.0

# Fights inside a match: kills close together, and shooting heard on the stream.
FIGHT_GAP_S = 30.0
GUNFIRE_ON = 0.3
SHOT_PAUSE_S = 4.0
MIN_SHOTS = 4                  # sound samples (about 1 s each) with gunfire for shooting alone to be a fight

# Gaps between matches: a frame every GAP_SAMPLE_S seconds is read; BGMI's lobby and menus use these words.
GAP_SAMPLE_S = 30.0
NOT_BGMI_MIN_S = 60.0
LOBBY_WORDS = re.compile(
    r"\b(start|inventory|crate|crates|shop|events?|royale ?pass|clan|friends?|classic|erangel|livik|miramar|"
    r"sanhok|vikendi|nusa|rondo|squad|duo|solo|team ?up|ranked|unranked|matching|cancel|arena|tdm|loading|"
    r"mission|spectate|ready|lobby|bp|uc|ag|outfit|redeem|collection|lucky ?spin|treasure|premium|"
    r"rating|conqueror|ace|crown|diamond|platinum|tier|season|mode|map|chicken ?dinner|eliminations?|"
    r"assists?|damage|survived|rescue|rank|exit|continue|back to lobby|leave|squad ?wiped|"
    r"spawn ?island|plane|jump)\b", re.I)
MIN_LOBBY_WORDS = 2

PLACEMENT = [re.compile(r"#\s*(\d{1,3})\s*/\s*\d{2,3}"), re.compile(r"#\s*(\d{1,3})\b"),
             re.compile(r"\brank(?:ed)?\s*#?\s*(\d{1,3})\b", re.I)]
DINNER_TEXT = re.compile(r"winner ?winner|chicken ?dinner", re.I)


def _match_starts(vision):
    """Times a fresh match began: the Eliminations counter reset, or the Remaining counter jumping to a full
    lobby."""
    starts = [e["t"] for e in vision.get("events", []) if e["kind"] == "match_start"]
    previous = None
    for t, value in vision.get("remaining", []):
        # A full lobby (80+), or a jump of 20+ to 40+ players: Ultimate Royale lobbies hold 64, Livik 50.
        if (value >= FRESH_LOBBY and previous is None) or (previous is not None and value >= 40 and value - previous >= 20):
            starts.append(t)
        previous = value
    return sorted(starts)


# What the screen said just after the counters vanished (vision.py reads it): the match goes on (a respawn or
# recall since update 4.6, or the game is on and only the counters were unreadable), or it is over.
RESPAWN_TEXT = re.compile(r"respawn|returning to the battle|recall|don'?t give up|join the vampires", re.I)
END_TEXT = re.compile(r"winner ?winner|chicken ?dinner|better ?luck|luck ?next ?time|keep it up|you made the top|you'?re in the top|"
                      r"\bdefeat\b|\bvictory\b|finishes|promoting to|squad wiped", re.I)
# TDM's score goal ("Goal: 40"); a stream overlay's donation goal ("GOAL:2225/6000") is not it.
TDM_TEXT = re.compile(r"\bgoal\s?:\s?(?:20|30|40|50|60|80)(?![\d/])", re.I)
COMPASS = {"15", "30", "60", "75", "105", "120", "150", "165", "195", "210", "240", "255", "285", "300", "330", "345"}


def compass_marks(text):
    """How many of the in-game compass's bearings are on screen. OCR runs them together ("150165", "330345"),
    so each run of digits counts when it splits wholly into bearings."""
    count = 0
    for run in re.findall(r"\d{2,12}", text):
        best = [0] + [None] * len(run)       # best[i]: bearings in a split of run[:i]
        for i in range(1, len(run) + 1):
            for k in (2, 3):
                if i >= k and best[i - k] is not None and run[i - k:i] in COMPASS:
                    best[i] = max(best[i] or 0, best[i - k] + 1)
        count += best[-1] or 0
    return count
MIN_LOBBY_GAP_S = 40.0     # a new match needs at least this long without the HUD before it (the lobby)
SPAWN_S = 58.0             # the spawn island and plane before the counters show (measured on 5 labelled matches)
SPAWN_GAP_S = 75.0


def reads_after(results, t):
    return [line for r in results if abs(r.get("after", -1e9) - t) <= 1 for line in r["lines"]]


def what_next(lines):
    """"on" (a respawn, or the game still on screen), "end" (a result screen) or None (nothing read)."""
    text = " ".join(lines)
    if END_TEXT.search(text):
        return "end"
    if RESPAWN_TEXT.search(text):
        return "on"
    if in_lobby(lines):
        return "end"
    if compass_marks(text) >= 3:
        return "on"
    return None


def in_lobby(lines):
    """True for BGMI's lobby or menus, False for a match on screen, None when the frame doesn't say."""
    text = " ".join(lines)
    if compass_marks(text) >= 3:
        return False
    words = sum(len(LOBBY_WORDS.findall(line)) for line in lines)
    return True if words >= MIN_LOBBY_WORDS + 1 else None


def _group_runs(hud, starts, results=(), read_text=None):
    """HUD runs → matches. After a run ends, the screen read says whether the match went on (respawn, game
    still on) or ended (result screen). Without a read, a fresh-lobby signal after a lobby-length gap, or a
    long gap, starts a new match, unless a frame from the middle of the gap shows the game still on (a
    vertical stream's tiny counters can go unread for minutes, and a teammate's 0 looks like a reset)."""
    groups = []
    for start, end in hud:
        if not groups:
            groups.append([[start, end]])
            continue
        prev_end = groups[-1][-1][1]
        gap = start - prev_end
        said = what_next(reads_after(results, prev_end))
        fresh = any(prev_end - 1 < s <= end for s in starts)
        if said is None and read_text and gap >= MIN_LOBBY_GAP_S:
            # Look early in the gap: its last minute or so is the next match's spawn island and plane.
            last = start - (SPAWN_S + 20) if gap > SPAWN_S + 50 else prev_end + gap * 0.4
            looks = [in_lobby(read_text(t)) for t in sorted({round(prev_end + 12, 1), round(max(prev_end + 12, last), 1)})]
            if True in looks:
                said = "end"
            elif False in looks:
                said = "on"
        if said == "end" or (said is None and ((fresh and gap >= MIN_LOBBY_GAP_S) or gap >= NEW_MATCH_GAP_S)):
            groups.append([[start, end]])
        else:
            groups[-1].append([start, end])
    return [g for g in groups if g[-1][1] - g[0][0] >= MIN_MATCH_S]


def placement_from(lines):
    """Placement from the text read after a match: "#4/98", "#4", "Rank 4"; a Chicken Dinner is 1."""
    text = " ".join(lines)
    if DINNER_TEXT.search(text):
        return 1
    for pattern in PLACEMENT:
        for found in pattern.finditer(text):
            value = int(found.group(1))
            if 1 <= value <= 100:
                return value
    return None


MAPS = ("erangel", "livik", "miramar", "sanhok", "vikendi", "nusa", "rondo", "karakin")
MODE_TEXT = re.compile(r"(ranked|unranked)?\s*(classic|arena|tdm|team ?deathmatch|ultimate ?royale)", re.I)


def mode_from(lines):
    """Mode and map from the result screen's line ("Ranked Classic Mode (TPP) - Squad - Erangel"); OCR drops
    spaces and letters, so the map is matched loosely."""
    import difflib

    text = " ".join(lines).lower()
    found = MODE_TEXT.search(text)
    mode = found.group(2).replace(" ", "") if found else None
    if mode is None and TDM_TEXT.search(text):
        mode = "tdm"
    words = re.findall(r"[a-z]{4,}", text)
    game_map = next((m for m in MAPS for w in words if difflib.SequenceMatcher(None, w, m).ratio() >= 0.8), None)
    return {"mode": mode, "ranked": bool(found and found.group(1) == "ranked"), "map": game_map} if (mode or game_map) else None


def _players_left(remaining, t):
    left = None
    for when, value in remaining:
        if when > t:
            break
        left = value
    return left


LEAD_BACK_S = 25.0             # how far back the shooting before a fight's first kill is followed
TAIL_ON_S = 10.0               # and forward after its last kill
FINAL_FIGHT_S = 30.0           # shooting that ends this close to the streamer's end is the fight they lost


def _shots(sounds, start, end):
    if not sounds or "gunfire" not in sounds:
        return np.array([])
    t, gun = sounds["t"], sounds["gunfire"]
    return t[(gun >= GUNFIRE_ON) & (t >= start) & (t <= end)]


def _follow(shots, t, direction, limit):
    """From t, follow gunfire with pauses of at most SHOT_PAUSE_S, up to `limit` seconds away."""
    edge = t
    ordered = shots[shots <= t][::-1] if direction < 0 else shots[shots >= t]
    for shot in ordered:
        if abs(shot - edge) > SHOT_PAUSE_S or abs(shot - t) > limit:
            break
        edge = float(shot)
    return edge


CLOSE_S = 12.0


def _connected(shots, a, b):
    """True when gunfire keeps coming between a and b with no pause longer than SHOT_PAUSE_S."""
    inside = shots[(shots >= a) & (shots <= b)] if len(shots) else shots
    edges = np.concatenate([[a], inside, [b]])
    return bool(len(edges) and np.max(np.diff(edges)) <= SHOT_PAUSE_S)


def fights(match, events, sounds, remaining, kill_times=None):
    """The fights of one match, in order. A fight is a cluster of the streamer's kills (and knocks), from the
    shooting that led up to it to the shooting that followed; shooting with no kill counts only as the
    match's last fight, the one the streamer lost. (Joining all gunfire made one 12-minute "fight" out of a
    busy 28-kill match: other squads' fights are heard all the time.)"""
    lo, hi = match["start"], match["end"] + DINNER_TAIL_S
    if kill_times is None:
        kill_times = [e["t"] for e in events if e["kind"] == "self_kill" and lo <= e["t"] <= hi]
    points = sorted([(t, "self_kill") for t in kill_times]
                    + [(e["t"], e["kind"]) for e in events
                       if e["kind"] in ("self_down", "dinner") and lo <= e["t"] <= hi])
    # Knocks read from the kill feed are not trusted to shape fights: on some layouts the feed reader logs a
    # "knock" every read (LoLzZz's vampire-event feed: one every 4 s for 6 minutes). They are counted only.
    knocks = [e["t"] for e in events if e["kind"] == "self_knock" and lo <= e["t"] <= hi]
    shots = _shots(sounds, lo, hi)
    clusters = []
    for t, kind in points:
        prev = clusters[-1][-1][0] if clusters else None
        # Same fight: close together, or the shooting between them never stops for long (a busy match has a
        # kill every 20-30 s, but the looting and running between fights is cut, as editors do).
        if prev is not None and (t - prev <= CLOSE_S or (t - prev <= FIGHT_GAP_S and _connected(shots, prev, t))):
            clusters[-1].append((t, kind))
        else:
            clusters.append([(t, kind)])
    out = []
    for c in clusters:
        first, last = c[0][0], c[-1][0]
        begin = max(lo, _follow(shots, first, -1, LEAD_BACK_S)) if len(shots) else first
        finish = min(hi, _follow(shots, last, +1, TAIL_ON_S)) if len(shots) else last
        kinds = [k for _, k in c]
        out.append({"start": round(begin, 2), "end": round(finish, 2), "kills": kinds.count("self_kill"),
                    "knocks": sum(1 for k in knocks if begin <= k <= finish), "down": "self_down" in kinds, "dinner": "dinner" in kinds,
                    "shots": int(((shots >= begin) & (shots <= finish)).sum()) if len(shots) else 0,
                    "players_left": _players_left(remaining, first),
                    "kill_times": [t for t, k in c if k == "self_kill"],
                    "points": [round(t, 2) for t, k in c if k in ("self_kill", "self_knock", "dinner")]})
    if match.get("ended") in ("death", "unknown") and len(shots):
        last_shot = float(shots[-1])
        if match["end"] - last_shot <= FINAL_FIGHT_S and not any(f["start"] <= last_shot <= f["end"] for f in out):
            begin = _follow(shots, last_shot, -1, 60.0)
            n = int(((shots >= begin) & (shots <= last_shot)).sum())
            if n >= MIN_SHOTS:
                out.append({"start": round(begin, 2), "end": round(min(hi, last_shot + 3), 2), "kills": 0, "knocks": 0,
                            "down": True, "dinner": False, "shots": n, "players_left": _players_left(remaining, begin),
                            "kill_times": [], "final": True})
    return sorted(out, key=lambda f: f["start"])


FINAL_SPECTATE_S = 90.0        # Spectating seen this close to the end of the HUD: the streamer was out for good


def final_spectate(spans, start, hud_end):
    """When the streamer was out for good: the start of the Spectating that runs on to the end of the match.
    Since update 4.6 a dead player can be recalled and fly back in, so Spectating earlier in a match, followed
    by minutes of play, is not the end. Spectating is only noticed now and then (when the counter shows a
    teammate's number), so sightings up to FINAL_SPECTATE_S apart count as one stretch."""
    seen = [s for s in spans if start + 60 <= s[0] <= hud_end]
    if not seen or hud_end - seen[-1][1] > FINAL_SPECTATE_S:
        return None
    first = seen[-1][0]
    for a, b in reversed(seen[:-1]):
        if first - b > FINAL_SPECTATE_S:
            break
        first = a
    return first


def _match(group, vision, sounds, duration):
    events = vision.get("events", [])
    start, hud_end = group[0][0], group[-1][1]
    end, ended = hud_end, "unknown"
    dinner = next((e["t"] for e in events if e["kind"] == "dinner" and start <= e["t"] <= hud_end + 30), None)
    spectate = final_spectate(vision.get("spectating", []), start, hud_end)
    downs = [e["t"] for e in events if e["kind"] == "self_down" and start <= e["t"] <= hud_end]
    down = downs[-1] if downs else None
    if dinner is not None and (spectate is None or spectate > dinner):
        end, ended = dinner + DINNER_TAIL_S, "dinner"
    elif spectate is not None:
        end, ended = max(start, spectate - END_AFTER_SPECTATE_S), "death"
        if down is not None and down < end:
            end = down + 3.0
    elif down is not None:
        end, ended = down + 3.0, "death"
    elif duration - hud_end <= CUT_OFF_S:
        ended = "cut_off"
    reads = [r for r in vision.get("results", []) if hud_end - 1 <= r.get("after", -1) <= hud_end + 1]
    lines = [line for r in reads for line in r["lines"]]
    ranks = [r["rank"][0] for r in reads if r.get("rank")]
    place = max(set(ranks), key=ranks.count) if ranks else placement_from(lines)
    if dinner is not None:
        place = 1
    elif place is not None and ended == "unknown":
        ended = "death" if place > 1 else "dinner"
    kills = [e["t"] for e in events if e["kind"] == "self_kill" and start <= e["t"] <= end + 2
             and not any(a - 2 <= e["t"] <= b + 6 for a, b in vision.get("spectating", []))]
    kills = drop_teammate_jumps(kills, hud_end, ended)
    match = {"start": round(start, 2), "end": round(min(end, duration), 2), "ended": ended,
             "placement": place, "kills": len(kills), "kill_times": kills,
             "players_left_at_end": _players_left(vision.get("remaining", []), end),
             "mode": mode_from([line for r in vision.get("results", []) if start <= r.get("after", -1) <= hud_end + 1
                                for line in r["lines"]]),
             "result_text": lines[:20]}
    match["fights"] = fights(match, events, sounds, vision.get("remaining", []), kills)
    return match


TEAMMATE_JUMP = 3          # this many "kills" in the same second, just before the counters go, is a teammate's count
TEAMMATE_WINDOW_S = 45.0


def drop_teammate_jumps(kills, hud_end, ended):
    """After the streamer is out for good the counter shows a teammate's eliminations (DIPENDU: "5 -> 9" a few
    seconds before the result screen). Three or more at once in the last seconds before the counters go is
    that, not a squad wipe read in one second."""
    if ended == "dinner":
        return kills
    out = []
    for t in kills:
        same = sum(1 for k in kills if abs(k - t) < 0.5)
        if same >= TEAMMATE_JUMP and hud_end - TEAMMATE_WINDOW_S <= t <= hud_end:
            continue
        out.append(t)
    return out


def score(match):
    """How good a match is for a kill-match highlight: kills first, then winning or a high place, then how
    many fights there were and how close the last ones were."""
    s = 3.0 * match["kills"]
    if match["ended"] == "dinner" or match["placement"] == 1:
        s += 15
    elif match["placement"] and match["placement"] <= 5:
        s += 6 - match["placement"]
    s += 1.0 * len(match["fights"])
    late = [f for f in match["fights"] if f["players_left"] and f["players_left"] <= 20 and f["kills"]]
    s += 2.0 * len(late)
    return round(s, 1)


def classify_gaps(gaps, read_text, step=GAP_SAMPLE_S):
    """Split the time between matches into "between" (BGMI lobby, menus, result screens) and "not_bgmi".
    `read_text(t)` returns the lines of text on the frame at t."""
    parts = []
    for start, end in gaps:
        samples = []
        t = start + min(10.0, (end - start) / 2)
        while t < end:
            lines = read_text(t)
            words = sum(len(LOBBY_WORDS.findall(line)) for line in lines)
            samples.append((t, words >= MIN_LOBBY_WORDS))
            t += step
        runs = []
        for t, bgmi in samples:
            kind = "between" if bgmi else "not_bgmi"
            if runs and runs[-1]["kind"] == kind:
                runs[-1]["last"] = t
            else:
                runs.append({"kind": kind, "first": t, "last": t})
        # Short not-BGMI stretches inside the lobby are menus OCR couldn't read: fold them in.
        for r in runs:
            if r["kind"] == "not_bgmi" and r["last"] - r["first"] + step < NOT_BGMI_MIN_S and len(runs) > 1:
                r["kind"] = "between"
        edges = [start] + [(a["last"] + b["first"]) / 2 for a, b in zip(runs, runs[1:])] + [end]
        piece = []
        for r, a, b in zip(runs, edges, edges[1:]):
            if piece and piece[-1]["kind"] == r["kind"]:
                piece[-1]["end"] = round(b, 2)
            else:
                piece.append({"start": round(a, 2), "end": round(b, 2), "kind": r["kind"]})
        if not runs:
            piece = [{"start": round(start, 2), "end": round(end, 2), "kind": "between"}]
        for p in piece:
            if p["kind"] == "not_bgmi":
                p["why"] = "no BGMI on screen (chat, another game or a video)"
        parts.extend(piece)
    return parts


def build(vision, duration, sounds=None, read_text=None):
    """The map of one stream. `read_text(t)` reads a frame's text, for telling the lobby from not-BGMI."""
    groups = _group_runs([tuple(s) for s in vision.get("hud", [])], _match_starts(vision), vision.get("results", []),
                         read_text)
    matches, previous_end = [], 0.0
    for g in groups:
        m = _match(g, vision, sounds, duration)
        # The counters show only once the match is under way; the spawn island and the plane come first.
        if m["start"] - previous_end >= SPAWN_GAP_S and m["start"] > 5 and (m.get("mode") or {}).get("mode") != "tdm":
            m["start"] = round(max(previous_end + 10.0, m["start"] - SPAWN_S), 2)
        previous_end = m["end"]
        matches.append(m)
    for n, m in enumerate(matches, 1):
        m["n"] = n
        m["score"] = score(m)
    gaps, cursor = [], 0.0
    for m in matches:
        if m["start"] - cursor > 1:
            gaps.append((cursor, m["start"]))
        cursor = m["end"]
    if duration - cursor > 1:
        gaps.append((cursor, duration))
    between = classify_gaps(gaps, read_text) if read_text else [
        {"start": round(a, 2), "end": round(b, 2), "kind": "between"} for a, b in gaps]
    parts = sorted(between + [{"start": m["start"], "end": m["end"], "kind": "match", "match": m["n"]}
                              for m in matches], key=lambda p: p["start"])
    ranked = sorted(matches, key=lambda m: -m["score"])
    best = ranked[0]["n"] if ranked and ranked[0]["kills"] else None
    session = sorted(m["n"] for m in ranked if best and m["kills"] >= max(5, 0.6 * ranked[0]["kills"]))
    log(f"map: {len(matches)} matches, kills {[m['kills'] for m in matches]}, best {best}, "
        f"{sum(p['kind'] == 'not_bgmi' for p in parts)} not-BGMI parts")
    return {"version": 1, "duration": round(duration, 2), "parts": parts, "matches": matches, "best": best,
            "session": session if len(session) >= 2 else []}


def frame_reader(src, info, ocr=None):
    """read_text(t) for build(): OCR of the whole frame at t (vertical streams enlarged, their text is small)."""
    from . import vision as v
    ocr = ocr or v.Ocr()
    vertical = info["height"] > info["width"]
    size = v.frame_size(info, 1080 if vertical else 720)

    def read_text(t):
        frame = v.grab_frame(src, t, size)
        if frame is None:
            return []
        found = ocr.lines_hires(frame, 1.0) if vertical else ocr.lines(frame)
        return [text for text, conf, _ in found if conf >= 0.5]
    return read_text


def summary(stream_map):
    return [{k: m[k] for k in ("n", "start", "end", "ended", "placement", "kills", "score")} | {"fights": len(m["fights"])}
            for m in stream_map["matches"]]


def hud_from_events(vision):
    """For a vision.json made before the scan saved HUD runs: approximate them from counter changes, so old jobs
    still get a rough map (each match from its first to its last counter change)."""
    times = sorted([e["t"] for e in vision.get("events", []) if e["kind"] in ("self_kill", "match_start")]
                   + [t for t, _ in vision.get("remaining", [])])
    spans = []
    for t in times:
        if spans and t - spans[-1][1] <= NEW_MATCH_GAP_S:
            spans[-1][1] = t
        else:
            spans.append([t, t])
    return spans


def make(job, read_frames=True):
    """Build and save the job's map.json from its saved scan; returns the map."""
    from . import sounds as sound_classes
    from .jobs import read_json, write_json

    info = read_json(job.path("info.json"))
    seen = read_json(job.path("vision.json")) or {}
    if "hud" not in seen:
        log("map: this scan predates HUD runs; matches are approximated from counter changes")
        seen = dict(seen, hud=hud_from_events(seen))
    heard_path = job.path("sounds.npz")
    heard = sound_classes.load(heard_path) if heard_path.exists() else None
    reader = frame_reader(info["path"], info) if read_frames and info.get("path") and _exists(info["path"]) else None
    stream_map = np_free(build(seen, info["duration"], heard, reader))
    write_json(job.path("map.json"), stream_map)
    return stream_map


def _exists(path):
    from pathlib import Path
    return Path(path).exists()


def compare(stream_map, labels, tolerance_s=20.0):
    """Score a map against hand labels (tests/data/labels): which labelled matches were found, how far their
    edges are off, and whether kills, endings and placements agree."""
    rows, used = [], set()
    for want in labels["matches"]:
        best, overlap = None, 0.0
        for m in stream_map["matches"]:
            o = min(m["end"], want["end"]) - max(m["start"], want["start"])
            if o > overlap and m["n"] not in used:
                best, overlap = m, o
        if best is None:
            rows.append({"label": want["n"], "found": False})
            continue
        used.add(best["n"])
        tol = max(tolerance_s, want.get("tolerance_s") or 0)
        rows.append({"label": want["n"], "found": True, "map": best["n"],
                     "start_off": round(best["start"] - want["start"], 1), "end_off": round(best["end"] - want["end"], 1),
                     "edges_ok": abs(best["start"] - want["start"]) <= tol and abs(best["end"] - want["end"]) <= tol,
                     "kills": [best["kills"], want["kills"]], "kills_ok": best["kills"] == want["kills"],
                     "ended": [best["ended"], want["ended"]], "placement": [best["placement"], want.get("placement")]})
    extra = [m["n"] for m in stream_map["matches"] if m["n"] not in used]
    found = [r for r in rows if r["found"]]
    return {"matches": rows, "extra": extra,
            "found": f"{len(found)}/{len(rows)}",
            "edges_ok": f"{sum(r['edges_ok'] for r in found)}/{len(found)}",
            "kills_ok": f"{sum(r['kills_ok'] for r in found)}/{len(found)}",
            "dinners": f"{sum(r['ended'] == ['dinner', 'dinner'] for r in found)}/"
                       f"{sum(w['ended'] == 'dinner' for w in labels['matches'])}"}


def np_free(obj):
    """JSON-safe copy (numpy numbers to Python)."""
    if isinstance(obj, dict):
        return {k: np_free(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [np_free(v) for v in obj]
    if isinstance(obj, np.generic):
        return obj.item()
    return obj
