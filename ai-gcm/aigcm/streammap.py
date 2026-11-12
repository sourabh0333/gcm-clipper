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
SHOT_PAUSE_S = 6.0
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


def _group_runs(hud, starts):
    """HUD runs → matches: a run begins a new match when a fresh-match signal falls inside it or just before,
    or when the HUD was gone long enough for a new lobby."""
    groups = []
    for start, end in hud:
        fresh = any(start - NEW_MATCH_GAP_S <= s <= end for s in starts
                    if not groups or s > groups[-1][-1][1] - 1)
        if groups and not fresh and start - groups[-1][-1][1] < NEW_MATCH_GAP_S:
            groups[-1].append([start, end])
        else:
            groups.append([[start, end]])
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
    words = re.findall(r"[a-z]{4,}", text)
    game_map = next((m for m in MAPS for w in words if difflib.SequenceMatcher(None, w, m).ratio() >= 0.8), None)
    return {"mode": mode, "ranked": bool(found and found.group(1) == "ranked"), "map": game_map} if (mode or game_map) else None


def _shooting(sounds, start, end):
    """Spans of gunfire heard between start and end: [(first, last, samples)]."""
    if not sounds or "gunfire" not in sounds:
        return []
    t, gun = sounds["t"], sounds["gunfire"]
    shots = t[(gun >= GUNFIRE_ON) & (t >= start) & (t <= end)]
    spans = []
    for s in shots:
        if spans and s - spans[-1][1] <= SHOT_PAUSE_S:
            spans[-1][1] = float(s)
            spans[-1][2] += 1
        else:
            spans.append([float(s), float(s), 1])
    return [tuple(s) for s in spans]


def _players_left(remaining, t):
    left = None
    for when, value in remaining:
        if when > t:
            break
        left = value
    return left


def fights(match, events, sounds, remaining):
    """The fights of one match, in order: kill and knock clusters joined with the shooting around them, plus
    shooting with no kill (a fight lost, a near miss) when it lasted a few seconds."""
    own = [e for e in events if e["kind"] in ("self_kill", "self_knock", "self_down", "dinner")
           and match["start"] <= e["t"] <= match["end"] + DINNER_TAIL_S]
    spans = []
    for first, last, n in _shooting(sounds, match["start"], match["end"]):
        spans.append({"start": first, "end": last, "shots": n, "events": []})
    for e in own:
        spans.append({"start": e["t"], "end": e["t"], "shots": 0, "events": [e]})
    spans.sort(key=lambda s: s["start"])
    merged = []
    for s in spans:
        if merged and s["start"] - merged[-1]["end"] <= FIGHT_GAP_S:
            m = merged[-1]
            m["end"] = max(m["end"], s["end"])
            m["shots"] += s["shots"]
            m["events"].extend(s["events"])
        else:
            merged.append(dict(s, events=list(s["events"])))
    out = []
    for m in merged:
        kinds = [e["kind"] for e in m["events"]]
        if not kinds and m["shots"] < MIN_SHOTS:
            continue
        out.append({"start": round(m["start"], 2), "end": round(m["end"], 2),
                    "kills": kinds.count("self_kill"), "knocks": kinds.count("self_knock"),
                    "down": "self_down" in kinds, "dinner": "dinner" in kinds, "shots": m["shots"],
                    "players_left": _players_left(remaining, m["start"]),
                    "kill_times": [e["t"] for e in m["events"] if e["kind"] == "self_kill"]})
    return out


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
    kills = [e["t"] for e in events if e["kind"] == "self_kill" and start <= e["t"] <= end + 2]
    match = {"start": round(start, 2), "end": round(min(end, duration), 2), "ended": ended,
             "placement": place, "kills": len(kills), "kill_times": kills,
             "players_left_at_end": _players_left(vision.get("remaining", []), end),
             "mode": mode_from(lines),
             "result_text": lines[:20]}
    match["fights"] = fights(match, events, sounds, vision.get("remaining", []))
    return match


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
    groups = _group_runs([tuple(s) for s in vision.get("hud", [])], _match_starts(vision))
    matches = [_match(g, vision, sounds, duration) for g in groups]
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
