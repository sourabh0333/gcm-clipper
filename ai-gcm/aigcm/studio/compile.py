"""The weekly compilation (M3.8): "best of this week", 8-13 minutes in 16:9 for the channel's main feed, or a
9:16 version up to 3 minutes. Master plan 4.4: never a silent kill montage (YouTube's inauthentic-content
rule): the creator's own talk clips sit between the fights, each piece opens with a title card, talk pieces
keep their captions, and the description carries chapters.

Pieces come from the source while it is on the laptop, else from a kept clip's working window. Kill clips
run as their whole fight (60-120 s), talk clips as a moment (20-45 s). Each piece is rendered to the same
format, then the pieces are joined without re-encoding."""

import shutil
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path

from ..jobs import log, read_json, write_json
from . import project
from . import window as win
from .edit import is_talk

TARGET_S = (8 * 60, 13 * 60)      # the 16:9 compilation's length
SHORT_MAX_S = 175.0               # the 9:16 version stays under YouTube's 3 minutes
MAX_PIECES = 16
TALK_EVERY = 2                    # a talk clip after every two fights
CARD_S = 4.0                      # each piece opens with its title card this long
WIDE = (1920, 1080)
FPS = 30


@dataclass
class Piece:
    clip_id: int
    title: str
    video: str          # the file the footage is in
    offset: float       # source time of that file's time 0
    start: float        # source seconds
    end: float
    talk: bool
    stream_id: str
    job_dir: str
    kills: int = 0

    @property
    def length(self):
        return self.end - self.start


def footage(settings, clip):
    """(file, offset, lo, hi) for a clip's footage: the stream's source (whole stream) or the clip's working
    window; None when neither is on the laptop."""
    folder = project.job_folder(settings, clip)
    source = project.source_file(folder)
    if source is not None:
        info = read_json(folder / "info.json", {}) or {}
        return str(source), 0.0, 0.0, float(info.get("duration") or 1e9)
    details = win.ready(project.clip_folder(settings, clip))
    if details:
        return str(project.clip_folder(settings, clip) / "window.mkv"), details["start"], details["start"], details["end"]
    return None


def piece_for(settings, clip, short=False):
    found = footage(settings, clip)
    if found is None:
        return None
    video, offset, lo, hi = found
    folder = project.job_folder(settings, clip)
    events = (read_json(folder / "vision.json", {}) or {}).get("events") or []
    talk = is_talk(clip.type, (clip.details or {}).get("labels"))
    presets = win.length_presets(clip.start_s, clip.end_s, (clip.details or {}).get("anchor"), events, lo, hi)
    a, b = presets["moment"] if (talk or short) else presets["full_fight"]
    if short:
        b = min(b, a + 30.0)
    kills = sum(1 for e in events if e.get("kind") == "self_kill" and a <= e["t"] <= b)
    return Piece(clip.id, clip.title or fallback_title(clip.type, kills, talk, clip.spoken), video, offset, a, b,
                 talk, clip.stream_id, clip.stream.job_dir, kills)


def fallback_title(kind, kills, talk, spoken=None):
    """A chapter name for a clip the engine gave no title (clips made before titles existed): its kills, or
    the first words said in it."""
    if not talk and kills:
        return f"{kills} FINISH{'ES' if kills > 1 else ''}"
    said = " ".join((spoken or "").split()[:6]).strip(" ,.")
    if talk and said:
        return said[:40]
    return {"funny": "Funny moment", "banter": "Banter", "rage": "Rage", "reaction": "Reaction", "win": "Chicken dinner",
            "clutch": "Clutch"}.get(kind, "Fight" if not talk else "Talk")


def suggest(clips, settings, short=False):
    """Pieces for the week: kept clips first, then unreviewed ones by score (never rejected), with footage on
    the laptop; a talk clip after every two fights; in stream order, filling up to the target length."""
    usable = [c for c in clips if c.decision != "reject"]
    usable.sort(key=lambda c: (c.decision != "keep", -(c.score or 0)))
    fights, talks = [], []
    for clip in usable:
        piece = piece_for(settings, clip, short)
        if piece is None:
            continue
        (talks if piece.talk else fights).append(piece)
    limit = SHORT_MAX_S if short else TARGET_S[1]
    chosen, total, since_talk = [], 0.0, 0
    while (fights or talks) and len(chosen) < MAX_PIECES:
        take_talk = bool(talks) and (since_talk >= TALK_EVERY or not fights)
        piece = talks.pop(0) if take_talk else fights.pop(0)
        if total + piece.length > limit:
            continue
        chosen.append(piece)
        total += piece.length
        since_talk = 0 if piece.talk else since_talk + 1
    return finale(chosen)


def finale(pieces):
    """Keep the picked rhythm (two fights, then the creator talking) but save the best fight for the end."""
    best = next((p for p in pieces if not p.talk), None)
    if best is None or len(pieces) < 3:
        return pieces
    return [p for p in pieces if p is not best] + [best]


def chapters(pieces, intro_s=0.0):
    """YouTube chapters: the first at 0:00, one per piece, each at least 10 s (pieces are 20 s or more)."""
    lines, at = [], intro_s
    for i, piece in enumerate(pieces):
        stamp = 0 if i == 0 else at
        m, s = divmod(int(stamp), 60)
        h, m = divmod(m, 60)
        lines.append(f"{h}:{m:02d}:{s:02d} {piece.title}" if h else f"{m}:{s:02d} {piece.title}")
        at += piece.length
    return lines


# --- rendering --------------------------------------------------------------------------------------------

def _captions_ass(words, size=58, margin=70):
    from ..captions import chunk_words
    from .render import CAPTION_FONT

    chunks = chunk_words(words)

    def stamp(t):
        cs = int(round(max(0.0, t) * 100))
        return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"

    lines = [f"""[Script Info]
ScriptType: v4.00+
PlayResX: {WIDE[0]}
PlayResY: {WIDE[1]}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,{CAPTION_FONT},{size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,5,2,2,80,80,{margin},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"""]
    for c in chunks:
        text = c["text"].replace("{", "(").replace("}", ")").upper()
        lines.append(f"Dialogue: 0,{stamp(c['start'])},{stamp(c['end'])},Caption,,0,0,0,,{text}")
    return "\n".join(lines) + "\n"


def piece_words(piece, transcript):
    if not transcript:
        return []
    return [dict(w, start=w["start"] - piece.start, end=w["end"] - piece.start)
            for seg in transcript.get("segments", []) for w in seg.get("words", [])
            if piece.start <= w["start"] and w["end"] <= piece.end]


def render_wide_piece(piece, out, card_png, transcript, threads):
    """One piece in 1920x1080 at 30 fps with stereo sound: the title card for its first seconds, captions on
    talk pieces. Vertical footage sits over a blurred copy of itself."""
    from ..media import probe, run, tool
    from .render import FONTS

    info = probe(piece.video)
    vertical = info["height"] > info["width"]
    w, h = WIDE
    with tempfile.TemporaryDirectory(prefix="kaatclip_comp_") as tmp:
        cmd = [tool("ffmpeg"), "-v", "error", "-y", "-ss", f"{piece.start - piece.offset:.3f}",
               "-t", f"{piece.length:.3f}", "-i", str(Path(piece.video).resolve())]
        if card_png:
            cmd += ["-i", str(Path(card_png).resolve())]
        if not info["has_audio"]:
            cmd += ["-f", "lavfi", "-t", f"{piece.length:.3f}", "-i", "anullsrc=r=48000:cl=stereo"]
        if vertical:
            lines = [f"[0:v]split=2[a][b]", f"[a]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},boxblur=24:2[bg]",
                     f"[b]scale=-2:{h}[fg]", "[bg][fg]overlay=(W-w)/2:0,setsar=1[base]"]
        else:
            lines = [f"[0:v]scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,setsar=1[base]"]
        base = "[base]"
        if card_png:
            lines.append(f"{base}[1:v]overlay=0:36:enable='lte(t,{CARD_S})'[carded]")
            base = "[carded]"
        tail = ""
        words = piece_words(piece, transcript) if piece.talk else []
        if words:
            (Path(tmp) / "captions.ass").write_text(_captions_ass(words), encoding="utf-8")
            shutil.copytree(FONTS, Path(tmp) / "fonts")
            tail = ",subtitles=captions.ass:fontsdir=fonts"
        lines.append(f"{base}fps={FPS}{tail},format=yuv420p[v]")
        audio = "[0:a:0]" if info["has_audio"] else f"[{2 if card_png else 1}:a]"
        lines.append(f"{audio}aresample=48000,aformat=channel_layouts=stereo[a]")
        cmd += ["-filter_complex", ";".join(lines), "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast",
                "-crf", "21", "-r", str(FPS), "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2",
                "-threads", str(threads), str(Path(out).resolve())]
        run(cmd, cwd=tmp)


def add_silence(video):
    from ..media import run, tool

    tmp = Path(video).with_name(Path(video).stem + ".sound.mp4")
    run([tool("ffmpeg"), "-v", "error", "-y", "-i", str(video), "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
         "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-shortest", str(tmp)])
    tmp.replace(video)


def join(parts, out):
    """Join same-format pieces without re-encoding."""
    from ..media import run, tool

    with tempfile.TemporaryDirectory(prefix="kaatclip_join_") as tmp:
        listing = Path(tmp) / "list.txt"
        listing.write_text("".join(f"file '{Path(p).resolve().as_posix()}'\n" for p in parts), encoding="utf-8")
        run([tool("ffmpeg"), "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(listing), "-c", "copy",
             "-movflags", "+faststart", str(out)])


def render_wide(pieces, out_dir, transcripts, threads=3):
    from . import hook

    out_dir = Path(out_dir)
    parts = []
    for i, piece in enumerate(pieces):
        card = hook.cached(out_dir / "cards", piece.title, "yellow", 200, backing=True, width=WIDE[0], start_size=96)
        part = out_dir / f"part_{i:02d}.mp4"
        render_wide_piece(piece, part, card, transcripts.get(piece.job_dir), threads)
        parts.append(part)
        log(f"compilation: piece {i + 1}/{len(pieces)} done")
    join(parts, out_dir / "video.mp4")
    for part in parts:
        part.unlink(missing_ok=True)
    shutil.rmtree(out_dir / "cards", ignore_errors=True)
    return out_dir / "video.mp4"


def render_short(pieces, out_dir, edits, transcripts, threads=3):
    """The 9:16 version: each piece through the studio renderer with the clip's default edit (layout, camera,
    hook, captions, zoom), cut to the piece, then joined."""
    from ..media import probe
    from .edit import Segment
    from .render import render as render_edit

    out_dir = Path(out_dir)
    parts = []
    for i, piece in enumerate(pieces):
        edit, hook_png = edits[piece.clip_id]
        edit = edit.model_copy(update={"segments": [Segment(start=piece.start, end=piece.end)], "intro": False,
                                       "outro": False})
        part = out_dir / f"part_{i:02d}.mp4"
        has_audio = probe(piece.video)["has_audio"]
        render_edit(edit, piece.video, piece.offset, has_audio, part, threads=threads, hook_png=hook_png,
                    transcript=transcripts.get(piece.job_dir) if edit.captions.on else None)
        if not has_audio:
            add_silence(part)   # every part needs a sound track to be joined without re-encoding
        parts.append(part)
    join(parts, out_dir / "video.mp4")
    for part in parts:
        part.unlink(missing_ok=True)
    return out_dir / "video.mp4"


def save_plan(out_dir, pieces, fmt, titles, description_lines):
    write_json(Path(out_dir) / "plan.json", {"format": fmt, "pieces": [asdict(p) for p in pieces], "titles": titles,
                                             "chapters": description_lines})


def load_plan(out_dir):
    return read_json(Path(out_dir) / "plan.json", {}) or {}
