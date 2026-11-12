"""The creator's brand kit (M3.6): set once, used on every export and on the engine's own clips.

What it holds: the hook and caption look, a lower-third strip (logo, name, UPI ID, Instagram) as mid-size
Indian channels use, an intro and outro, a standard description, hashtags, and the game line. Files live
in `<jobs>/_brand/<user id>/`: logo.png (re-encoded, at most 512 px), intro.mp4 and outro.mp4 (normalised
to 1080x1920, 30 fps, stereo AAC, at most 6 s, so they join any export). The lower-third is drawn once per
kit into a transparent strip, like the hook, so the preview and the export match.

No watermark on the clip itself (master plan 4.2): the logo appears only in the lower-third."""

import hashlib
import unicodedata
import tempfile
from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator

from ..jobs import log, read_json
from .edit import H, Strict

BRAND_DIR = "_brand"
LOGO_MAX = 512
LOGO_BYTES = 3 * 1024 * 1024
CLIP_BYTES = 60 * 1024 * 1024
CLIP_MAX_S = 6.0
STRIP_H = 140
STRIP_Y = H - STRIP_H - 30          # under the captions, above the phone's own buttons
STRIP_ALPHA = 0.68
LOGO_SIDE = 104
VERSION = 1


class BrandKit(Strict):
    hook_color: Literal["yellow", "white"] = "yellow"
    caption_color: Literal["white", "yellow"] = "white"
    caption_size: Literal["normal", "large"] = "normal"
    lower_third: bool = False
    name: str = Field("", max_length=40)
    upi: str = Field("", max_length=60)
    instagram: str = Field("", max_length=40)
    use_intro: bool = False
    use_outro: bool = False
    description: str = Field("", max_length=1500)
    hashtags: list[str] = Field(default_factory=list, max_length=10)
    disclaimer: str | None = Field(None, max_length=300)   # None: the game's standard line

    @field_validator("hashtags")
    @classmethod
    def _tags(cls, tags):
        out = []
        for tag in tags:
            # Letters, digits and vowel signs (Hindi's matras are marks, not letters) and underscores only.
            kept = "".join(ch for ch in tag.strip().lstrip("#")
                           if ch == "_" or unicodedata.category(ch)[0] in "LMN")
            tag = "#" + kept[:30]
            if len(tag) > 1 and tag.lower() not in [t.lower() for t in out]:
                out.append(tag)
        return out

    @field_validator("instagram")
    @classmethod
    def _insta(cls, value):
        value = value.strip()
        return ("@" + value.lstrip("@")) if value else ""

    def strip_text(self):
        parts = [self.name.strip()]
        if self.upi.strip():
            parts.append(f"UPI: {self.upi.strip()}")
        if self.instagram:
            parts.append(f"IG: {self.instagram}")
        return "  •  ".join(p for p in parts if p)


def folder(jobs_dir, user_id):
    return Path(jobs_dir) / BRAND_DIR / str(int(user_id))


def files(jobs_dir, user_id):
    """{logo, intro, outro}: paths that exist, else None, plus the intro and outro lengths."""
    base = folder(jobs_dir, user_id)
    out = {kind: (base / name if (base / name).exists() else None)
           for kind, name in (("logo", "logo.png"), ("intro", "intro.mp4"), ("outro", "outro.mp4"))}
    lengths = read_json(base / "lengths.json", {}) or {}
    out["intro_s"] = lengths.get("intro", 0.0) if out["intro"] else 0.0
    out["outro_s"] = lengths.get("outro", 0.0) if out["outro"] else 0.0
    out["intro_music"] = lengths.get("intro_music", 0.0) if out["intro"] else 0.0
    out["outro_music"] = lengths.get("outro_music", 0.0) if out["outro"] else 0.0
    return out


def defaults(kit, found):
    """What a new edit takes from the kit (edit.default_edit's `brand`)."""
    kit = kit or BrandKit()
    return {"hook_color": kit.hook_color, "caption_color": kit.caption_color, "caption_size": kit.caption_size,
            "lower_third": kit.lower_third and bool(kit.strip_text() or found.get("logo")),
            "intro": kit.use_intro and bool(found.get("intro")), "outro": kit.use_outro and bool(found.get("outro"))}


# --- saving the creator's files ---------------------------------------------------------------------------

def save_logo(jobs_dir, user_id, data):
    """Re-encode an uploaded image as a PNG of at most LOGO_MAX px (anything that isn't a real image is
    refused; nothing uploaded is ever served as it came)."""
    from io import BytesIO

    from PIL import Image

    if len(data) > LOGO_BYTES:
        raise ValueError("The logo can be at most 3 MB.")
    try:
        image = Image.open(BytesIO(data))
        image.load()
    except Exception as exc:
        raise ValueError("That file isn't an image.") from exc
    image = image.convert("RGBA")
    image.thumbnail((LOGO_MAX, LOGO_MAX))
    target = folder(jobs_dir, user_id)
    target.mkdir(parents=True, exist_ok=True)
    image.save(target / "logo.png", "PNG")
    return target / "logo.png"


def save_clip(jobs_dir, user_id, kind, data):
    """Normalise an uploaded intro or outro: checked with ffprobe, cut to CLIP_MAX_S, 1080x1920 (fitted,
    black bars), 30 fps, stereo AAC (silence added if it has none)."""
    from ..jobs import write_json
    from ..media import probe, run, tool

    if kind not in ("intro", "outro"):
        raise ValueError("kind must be intro or outro")
    if len(data) > CLIP_BYTES:
        raise ValueError("The intro or outro can be at most 60 MB.")
    target = folder(jobs_dir, user_id)
    target.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="kaatclip_brand_") as tmp:
        raw = Path(tmp) / "upload"
        raw.write_bytes(data)
        try:
            info = probe(raw)
        except Exception as exc:
            raise ValueError("That file isn't a video ffmpeg can read.") from exc
        length = min(CLIP_MAX_S, info["duration"])
        cmd = [tool("ffmpeg"), "-v", "error", "-y", "-i", str(raw)]
        if not info["has_audio"]:
            cmd += ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
        cmd += ["-t", f"{length:.3f}", "-map", "0:v:0", "-map", "0:a:0" if info["has_audio"] else "1:a:0",
                "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black,"
                       "setsar=1,fps=30,format=yuv420p",
                "-af", "aresample=48000", "-ac", "2", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(Path(tmp) / "out.mp4")]
        run(cmd)
        (Path(tmp) / "out.mp4").replace(target / f"{kind}.mp4")
    lengths = read_json(target / "lengths.json", {}) or {}
    lengths[kind] = round(length, 3)
    lengths[f"{kind}_music"] = music_in(target / f"{kind}.mp4")
    write_json(target / "lengths.json", lengths)
    return target / f"{kind}.mp4"


def music_in(video):
    """Seconds of music the sound detector hears in an intro or outro (M3.9): music the creator doesn't own
    would get every Short that uses it claimed. 0 when the detector isn't installed here."""
    try:
        from .. import sounds
        from ..media import extract_audio
        from . import sound
    except ImportError:
        return 0.0
    with tempfile.TemporaryDirectory(prefix="kaatclip_music_") as tmp:
        wav = Path(tmp) / "a.wav"
        try:
            extract_audio(video, wav)
            found = sounds.analyse(wav)
        except Exception as exc:   # no model, no network: the upload still works, just unchecked
            log(f"brand: music check skipped ({exc!r})")
            return 0.0
    return round(sum(b - a for a, b in sound.music_spans(found)), 1)


def remove(jobs_dir, user_id, kind):
    name = {"logo": "logo.png", "intro": "intro.mp4", "outro": "outro.mp4"}[kind]
    (folder(jobs_dir, user_id) / name).unlink(missing_ok=True)


# --- the lower-third strip ----------------------------------------------------------------------------------

def strip_name(kit, logo):
    stamp = logo.stat().st_mtime_ns if logo else 0
    key = f"{VERSION}|{kit.strip_text()}|{stamp}".encode("utf-8")
    return "lt-" + hashlib.sha256(key).hexdigest()[:16] + ".png"


def render_strip(kit, logo, out_path):
    """A 1080 x STRIP_H transparent PNG: a dark bar, the logo on the left, the kit's line of text. None if the
    kit has neither text nor logo."""
    import cv2
    import numpy as np

    from . import hook

    text = kit.strip_text()
    if not text and not logo:
        return None
    width = hook.W
    bar = np.zeros((STRIP_H, width, 4), np.float32)
    bar[..., 3] = 255 * STRIP_ALPHA
    left = 36
    if logo:
        pic = cv2.imread(str(logo), cv2.IMREAD_UNCHANGED)
        if pic is not None:
            if pic.shape[2] == 3:
                pic = np.dstack([pic, np.full(pic.shape[:2], 255, np.uint8)])
            scale = LOGO_SIDE / max(pic.shape[:2])
            pic = cv2.resize(pic, (max(1, round(pic.shape[1] * scale)), max(1, round(pic.shape[0] * scale))),
                             interpolation=cv2.INTER_AREA).astype(np.float32)
            y0 = (STRIP_H - pic.shape[0]) // 2
            region = bar[y0:y0 + pic.shape[0], left:left + pic.shape[1]]
            bar[y0:y0 + pic.shape[0], left:left + pic.shape[1]] = hook.over(pic, region)
            left += pic.shape[1] + 24
    if text:
        font = hook.DEVANAGARI_FONT
        size = 50
        with tempfile.TemporaryDirectory(prefix="kaatclip_strip_") as tmp:
            for _ in range(6):
                ass = _strip_ass(text, font, size, left)
                drawn = hook._draw(ass, STRIP_H, Path(tmp), "strip")
                cols = np.where(drawn[..., 3].max(axis=0) > 0)[0]
                if not cols.size or cols[-1] < width - 24:
                    break
                size = round(size * 0.88)
        bar = hook.over(drawn.astype(np.float32), bar)
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out_path), np.clip(bar, 0, 255).astype(np.uint8))
    log(f"brand: lower-third {out_path.name}")
    return out_path


def _strip_ass(text, font, size, left):
    from . import hook

    return f"""[Script Info]
ScriptType: v4.00+
PlayResX: {hook.W}
PlayResY: {STRIP_H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Strip,{font},{size},&H00FFFFFF&,&H00FFFFFF&,&H00000000&,&H00000000&,0,0,0,0,100,100,0,0,1,2,0,4,{left},24,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:01.00,Strip,,0,0,0,,{hook._escape(text)}
"""


def strip_for(jobs_dir, user_id, kit):
    """The kit's lower-third strip, drawn once and kept in the brand folder; None if there's nothing to show."""
    found = files(jobs_dir, user_id)
    path = folder(jobs_dir, user_id) / strip_name(kit, found["logo"])
    if path.exists():
        return path
    return render_strip(kit, found["logo"], path)


# --- the post text --------------------------------------------------------------------------------------------

def post_text(title, engine_description, engine_tags, kit):
    """Title, description and hashtags for posting: the engine's description (stream link, game line), with
    the kit's standard description added and its game line and hashtags used."""
    from ..titles import KRAFTON_LINE

    kit = kit or BrandKit()
    tags = []
    for tag in list(kit.hashtags) + list(engine_tags or []):
        if tag.lower() not in [t.lower() for t in tags]:
            tags.append(tag)
    tags = tags[:8]
    parts = [p for p in (engine_description or "").split("\n\n") if p.strip()]
    had_game_line = KRAFTON_LINE in parts
    # Only the stream link is kept from the engine's text: anything else there is the AI judge's private note
    # about the clip ("The screen is black..."), which must never reach a public description (found 12 Nov).
    parts = [p for p in parts if p.strip().startswith("Full stream:")]
    if kit.description.strip():
        parts.append(kit.description.strip())
    game_line = KRAFTON_LINE if kit.disclaimer is None and had_game_line else (kit.disclaimer or "").strip()
    if game_line:
        parts.append(game_line)
    if tags:
        parts.append(" ".join(tags))
    description = "\n\n".join(parts)
    return {"title": title or "", "description": description, "hashtags": tags,
            "text": "\n\n".join(p for p in (title, description) if p)}
