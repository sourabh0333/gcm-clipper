"""The kill-match highlight (Highlights Stage 1, S1.4-S1.5): one match, or the best few in order, told the way
Goblin's and LoLzZz's editors tell it (reports/BGMI creators content A to Z.md, section 3):

- a 15-25 s cold open from the best fight, under an "IN THIS VIDEO" label;
- every fight kept whole with its comms: from the call or first shot to the reaction after the last kill;
- the funniest talk inside the match;
- looting, running and waiting cut, with "A FEW MINUTES LATER" only where a lot is skipped;
- "MATCH 2", "MATCH 3" cards in the session version;
- the ending: the Chicken Dinner or the last fight, a few seconds of the face, then black;
- the face full screen for a moment on the biggest reactions (when the stream has a face cam).

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
PUNCH_EVERY_S = 75.0         # at most one face punch-in per this much of the video
PUNCH_GAP_S = 40.0
PUNCH_MIN = 2.5              # how far above the stream's normal level a shout or laugh must be

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


def match_pieces(match, words, audio, talks, duration):
    """The kept stretches of one match, in order, with their edges out of words."""
    lo, hi = match["start"], min(duration, match["end"])
    pieces = [fight_piece(f, words, audio, lo, hi + DINNER_AFTER_S) for f in match["fights"]]
    pieces += _talk_pieces(match, talks)
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


def teaser(match, pieces, words):
    """The cold open: the best fight's last kills, or the Chicken Dinner, 15-25 s."""
    fights = [f for f in match["fights"] if f.get("kills")]
    if not fights:
        return None
    best = max(fights, key=lambda f: (f["kills"] + (3 if f.get("dinner") else 0), f["start"]))
    peak = max(best.get("kill_times") or [best["end"]])
    if match["ended"] == "dinner" and best is fights[-1]:
        peak = match["end"] - DINNER_AFTER_S + 3
    start, end = peak - (TEASER_S[1] - 7), peak + 7
    inside = next((p for p in pieces if p["start"] <= peak <= p["end"]), None)
    if inside:
        start, end = max(start, inside["start"]), min(end, inside["end"])
    if end - start < TEASER_S[0]:
        start = end - TEASER_S[0]
    return {"kind": "teaser", "start": round(snap(start, words, "start"), 2), "end": round(snap(end, words, "end"), 2),
            "label": "IN THIS VIDEO", "match": match["n"]}


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
                                              if p["kind"] not in ("card", "teaser"))]
    chosen = []
    for v, t in sorted(inside, reverse=True):
        if all(abs(t - c) >= PUNCH_GAP_S for c in chosen):
            chosen.append(t)
        if len(chosen) >= limit:
            break
    out = {}
    for t in sorted(chosen):
        i = next(i for i, p in enumerate(pieces) if p["kind"] not in ("card", "teaser")
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
        pieces = match_pieces(m, words, audio, talks, duration)
        if len(matches) > 1:
            body.append({"kind": "card", "text": f"MATCH {k + 1}", "length": CARD_S, "match": m["n"]})
        for i, p in enumerate(pieces):
            if i and p["start"] - pieces[i - 1]["end"] >= SKIP_CARD_S:
                body.append({"kind": "card", "text": "A FEW MINUTES LATER", "length": CARD_S, "match": m["n"]})
            body.append(p)
            kept += p["end"] - p["start"]
    best = max(matches, key=lambda m: m["score"])
    cold = teaser(best, [p for p in body if p.get("match") == best["n"] and p["kind"] != "card"], words)
    pieces = ([cold] if cold else []) + body + [{"kind": "card", "text": "", "length": END_BLACK_S}]
    total = sum(p.get("length") or (p["end"] - p["start"]) for p in pieces)
    if facecam:
        for i, spans in punch_ins(pieces, sounds, audio, int(total // PUNCH_EVERY_S)).items():
            pieces[i]["punch"] = spans
    span = sum(m["end"] - m["start"] for m in matches)
    return {"matches": [m["n"] for m in matches], "pieces": pieces, "length": round(total, 1),
            "kept": round(kept / span, 3) if span else 0, "kills": sum(m["kills"] for m in matches),
            "facecam": list(facecam) if facecam else None}


# --- what goes with the video: Shorts, titles, the channel label ----------------------------------------------

SHORT_S = (20.0, 58.0)
TEASER_SHORT_S = (25.0, 40.0)
SHORTS_BEST = 2
RECORD_KILLS = 15


def short_moments(the_plan):
    """The Shorts cut from the highlight (owner's decision of 12 Nov): the teaser (the same peak as the cold
    open, a little longer) and the best other fights, each ending just after its last kill."""
    pieces = [p for p in the_plan["pieces"] if p["kind"] not in ("card",)]
    out = []
    teaser = next((p for p in pieces if p["kind"] == "teaser"), None)
    if teaser:
        end = teaser["end"]
        start = min(teaser["start"], end - TEASER_SHORT_S[0])
        out.append({"role": "teaser", "start": round(max(0.0, start), 2), "end": round(end, 2),
                    "kills": teaser.get("kills", 0), "match": teaser.get("match")})
    fights = [p for p in pieces if p["kind"] in ("fight", "ending") and p.get("kills")]
    for p in sorted(fights, key=lambda p: (-p["kills"], p["start"])):
        if len([o for o in out if o["role"] == "best"]) >= SHORTS_BEST:
            break
        if teaser and p["start"] <= teaser["end"] and teaser["start"] <= p["end"]:
            continue     # the teaser already covers this fight
        end = p["end"]
        start = max(p["start"], end - SHORT_S[1])
        if end - start < SHORT_S[0]:
            start = end - SHORT_S[0]
        out.append({"role": "best", "start": round(max(0.0, start), 2), "end": round(end, 2), "kills": p["kills"],
                    "match": p.get("match")})
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


def render_piece(piece, source, info, out, folder, facecam=None, threads=3):
    """One stretch of the stream at 1920x1080: the layout as streamed (vertical over a blurred copy), the
    "IN THIS VIDEO" label on the cold open, and the face full screen during its punch-ins."""
    from ..media import run, tool

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
    if punch and facecam:
        x, y, cw, ch = facecam
        when = "+".join(f"between(t,{a - piece['start']:.2f},{b - piece['start']:.2f})" for a, b in punch)
        lines += [f"{cam_in}crop=iw*{cw:.4f}:ih*{ch:.4f}:iw*{x:.4f}:ih*{y:.4f},"
                  f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1[cam]",
                  f"{base}[cam]overlay=0:0:enable='{when}'[punched]"]
        base = "[punched]"
    if label:
        lines.append(f"{base}[{label_in}:v]overlay=0:40[labelled]")
        base = "[labelled]"
    lines.append(f"{base}fps={FPS},format=yuv420p[v]")
    audio = "[0:a:0]" if info.get("has_audio", True) else f"[{silent_in}:a]"
    lines.append(f"{audio}aresample=48000,aformat=channel_layouts=stereo[a]")
    cmd += ["-filter_complex", ";".join(lines), "-map", "[v]", "-map", "[a]", *ENCODE, "-threads", str(threads),
            str(Path(out).resolve())]
    run(cmd)


def render(the_plan, source, info, out, threads=3, progress=None):
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
                render_piece(piece, source, info, part, work, the_plan.get("facecam"), threads)
            parts.append(part)
            if progress:
                progress(i + 1, len(the_plan["pieces"]))
        join(parts, out)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    log(f"highlight: {out.name} made from {len(the_plan['pieces'])} pieces, {the_plan['length'] / 60:.1f} min")
    return out


def render_short(moment, source, info, out, title, facecam, transcript, kit_defaults=None, threads=3):
    """One Short from the highlight, through the Studio renderer with a clip's default edit (layout, camera,
    hook title, zoom on kills, captions), so it can be opened in the editor like any clip."""
    from . import hook
    from .edit import default_edit
    from .render import render as render_edit

    edit = default_edit(moment["start"], moment["end"], info["width"], info["height"], title,
                        moment.get("events") or (), captions=False, facecam=facecam, brand=kit_defaults)
    picture = hook.for_edit(Path(out).parent / "hooks", edit)
    render_edit(edit, source, 0.0, info.get("has_audio", True), out, transcript=transcript, threads=threads,
                hook_png=picture)
    return edit
