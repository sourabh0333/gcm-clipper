"""The hook: 1-2 lines of heavy caps with one emoji, drawn into a transparent PNG the size of its box
(M3 plan section 4.4, review S-R3). The same PNG is shown in the editor and laid over the export, so the
preview is exact.

ffmpeg's subtitle renderer (libass with HarfBuzz) shapes Hindi correctly but draws emoji only as flat
outlines. So the text is drawn by libass with a placeholder square where each emoji goes: first in pure
magenta, to find where libass put it, then fully transparent; the colour emoji image (Noto, bundled in
assets/emoji) is pasted into that spot. The text shrinks until it fits the box in at most two lines.

Fonts are bundled (assets/fonts, SIL Open Font License) so the result doesn't depend on Windows: Anton
for Latin hooks, Mukta ExtraBold when the hook has Hindi."""

import hashlib
import shutil
import tempfile
import unicodedata
from pathlib import Path

from ..config import ROOT
from ..jobs import log
from ..media import run, tool

FONTS = ROOT / "assets" / "fonts"
EMOJI = ROOT / "assets" / "emoji"
LATIN_FONT = "Anton"
DEVANAGARI_FONT = "Mukta ExtraBold"
COLOURS = {"yellow": "&H0000E6FF&", "white": "&H00FFFFFF&"}   # ASS is &HAABBGGRR
W = 1080
MARGIN_X = 50
MARGIN_Y = 24
START_SIZE = {"latin": 132, "devanagari": 124}
MAX_TRIES = 7
SHRINK = 0.88
VERSION = 2   # bump when the drawing changes, so cached PNGs are made again


def emoji_file(char):
    """The bundled image for one emoji character (variation selectors ignored), or None."""
    path = EMOJI / f"{ord(char):x}.png"
    return path if path.exists() else None


def tokens(text):
    """[(kind, value)]: runs of text and single emoji. Emoji without a bundled image are dropped, as are
    variation selectors and zero-width joiners, so nothing can turn into a box of tofu."""
    out = []
    for ch in text:
        if ch in ("️", "‍"):
            continue
        if emoji_file(ch):
            out.append(("emoji", ch))
        elif unicodedata.category(ch) == "So" and ord(ch) > 0x2000:
            continue
        elif out and out[-1][0] == "text":
            out[-1] = ("text", out[-1][1] + ch)
        else:
            out.append(("text", ch))
    return out


def has_devanagari(text):
    return any("ऀ" <= ch <= "ॿ" for ch in text)


def _escape(text):
    return text.replace("\\", "⧵").replace("{", "(").replace("}", ")").replace("\n", " ")


def placeholder_colour(k):
    """The k-th emoji's placeholder: magenta with a different blue, so emoji side by side stay apart."""
    return 255, 0, 255 - 28 * k     # R, G, B


def build_ass(parts, font, size, colour, box_h, placeholder, width=W):
    """An ASS script drawing the hook centred in a W x box_h box; each emoji is a square drawing in its
    own placeholder colour (to be found) or fully transparent (to be filled with the image)."""
    side = round(size * 0.92)
    body, k = "", 0
    for kind, value in parts:
        if kind == "emoji":
            r, g, b = placeholder_colour(k)
            bgr = f"&H{b:02X}{g:02X}{r:02X}&"
            fill = f"\\1c{bgr}\\3c{bgr}\\1a&H00&\\3a&H00&" if placeholder else "\\1a&HFF&\\3a&HFF&"
            body += f"{{\\bord0\\shad0{fill}\\p1}}m 0 0 l {side} 0 {side} {side} 0 {side}{{\\p0\\r}}"
            k += 1
        else:
            body += _escape(value.upper())
    # Letter spacing switches off complex shaping in libass, which breaks Hindi's vowel signs.
    spacing = 0 if has_devanagari("".join(v for kind, v in parts if kind == "text")) else 1
    return f"""[Script Info]
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {box_h}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Hook,{font},{size},{COLOURS[colour]},&H00FFFFFF&,&H00000000&,&H00000000&,0,0,0,0,100,100,{spacing},0,1,{max(4, round(size * 0.06))},0,5,{MARGIN_X},{MARGIN_X},0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:01.00,Hook,,0,0,0,,{body}
"""


def _draw(ass_text, box_h, folder, name, width=W):
    """Render an ASS script onto a transparent width x box_h image; returns it as an RGBA numpy array."""
    import cv2

    (folder / f"{name}.ass").write_text(ass_text, encoding="utf-8")
    fonts = shutil.copytree(FONTS, folder / "fonts", dirs_exist_ok=True)
    run([tool("ffmpeg"), "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=black@0.0:s={width}x{box_h}:d=1,format=rgba",
         "-vf", f"subtitles={name}.ass:fontsdir={Path(fonts).name}:alpha=1", "-frames:v", "1", f"{name}.png"],
        cwd=folder)
    image = cv2.imread(str(folder / f"{name}.png"), cv2.IMREAD_UNCHANGED)
    # ffmpeg's subtitle drawing squeezes colours into video range (255 -> 235, 0 -> 16) even on RGBA
    # frames (measured 10 Nov): stretch them back, so white is white and the placeholders are exact.
    import numpy as np

    rgb = (image[..., :3].astype(np.float32) - 16.0) * (255.0 / 219.0)
    image[..., :3] = np.clip(np.rint(rgb), 0, 255).astype(np.uint8)
    return image


def _emoji_boxes(image, count):
    """Where each emoji's placeholder landed: [(x, y, w, h)] in emoji order, or fewer if one is missing.
    Only the placeholders' solid insides are matched, so their soft edges don't blur into a neighbour."""
    import numpy as np

    b, g, r, a = (image[..., i].astype(int) for i in range(4))
    boxes = []
    for k in range(count):
        pr, pg, pb = placeholder_colour(k)
        ys, xs = np.where((abs(r - pr) < 10) & (g < 20) & (abs(b - pb) < 10) & (a > 245))
        if xs.size < 40:
            return boxes
        x0, x1, y0, y1 = int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())
        boxes.append((x0 - 1, y0 - 1, x1 - x0 + 3, y1 - y0 + 3))
    return boxes


def _ink_height(image):
    import numpy as np

    rows = np.where(image[..., 3].max(axis=1) > 0)[0]
    return int(rows[-1] - rows[0] + 1) if rows.size else 0


BACKING_ALPHA = 0.6
BACKING_PAD = 22


def over(top, bottom):
    """Straight-alpha "top over bottom" for float32 RGBA arrays in 0..255."""
    import numpy as np

    ta, ba = top[..., 3:4] / 255.0, bottom[..., 3:4] / 255.0
    out_a = ta + ba * (1 - ta)
    safe = np.where(out_a > 0, out_a, 1.0)
    rgb = (top[..., :3] * ta + bottom[..., :3] * ba * (1 - ta)) / safe
    return np.concatenate([rgb, out_a * 255.0], axis=-1)


def add_backing(image):
    """A dark, rounded box behind the hook's ink, so it reads over a busy picture (outside the black band)."""
    import cv2
    import numpy as np

    ys, xs = np.where(image[..., 3] > 0)
    if not xs.size:
        return image
    h, w = image.shape[:2]
    x0, y0 = max(0, xs.min() - BACKING_PAD), max(0, ys.min() - BACKING_PAD // 2)
    x1, y1 = min(w - 1, xs.max() + BACKING_PAD), min(h - 1, ys.max() + BACKING_PAD // 2)
    mask = np.zeros((h, w), np.uint8)
    r = 26
    cv2.rectangle(mask, (x0 + r, y0), (x1 - r, y1), 255, -1)
    cv2.rectangle(mask, (x0, y0 + r), (x1, y1 - r), 255, -1)
    for cx, cy in ((x0 + r, y0 + r), (x1 - r, y0 + r), (x0 + r, y1 - r), (x1 - r, y1 - r)):
        cv2.circle(mask, (cx, cy), r, 255, -1, lineType=cv2.LINE_AA)
    backing = np.zeros((h, w, 4), np.float32)
    backing[..., 3] = mask.astype(np.float32) * BACKING_ALPHA
    return np.clip(over(image.astype(np.float32), backing), 0, 255).astype(np.uint8)


def render(text, colour, box_h, out_path, backing=False, width=W, start_size=None):
    """Draw the hook into out_path (a width x box_h RGBA PNG; 1080 wide for Shorts, 1920 for a compilation's
    title cards), on a dark backing if asked. Returns out_path, or None for an empty hook."""
    import cv2
    import numpy as np

    parts = tokens(text.strip())
    if not any(kind == "emoji" or value.strip() for kind, value in parts):
        return None
    script = "devanagari" if has_devanagari(text) else "latin"
    font = DEVANAGARI_FONT if script == "devanagari" else LATIN_FONT
    emojis = [value for kind, value in parts if kind == "emoji"]
    size = start_size or START_SIZE[script]
    with tempfile.TemporaryDirectory(prefix="kaatclip_hook_") as tmp:
        folder = Path(tmp)
        for _ in range(MAX_TRIES):
            probe = _draw(build_ass(parts, font, size, colour, box_h, True, width), box_h, folder, "probe", width)
            boxes = _emoji_boxes(probe, len(emojis))
            lines = max(1, round(_ink_height(probe) / (size * 1.25)))
            if _ink_height(probe) <= box_h - 2 * MARGIN_Y and lines <= 2 and len(boxes) == len(emojis):
                break
            size = round(size * SHRINK)
        final = _draw(build_ass(parts, font, size, colour, box_h, False, width), box_h, folder, "final", width)
        for (x, y, w, h), ch in zip(boxes, emojis):
            pic = cv2.imread(str(emoji_file(ch)), cv2.IMREAD_UNCHANGED)
            side = max(w, h)
            pic = cv2.resize(pic, (side, side), interpolation=cv2.INTER_AREA)
            x0, y0 = max(0, x + (w - side) // 2), max(0, y + (h - side) // 2)
            x1, y1 = min(width, x0 + side), min(box_h, y0 + side)
            region = final[y0:y1, x0:x1].astype(np.float32)
            src = pic[: y1 - y0, : x1 - x0].astype(np.float32)
            final[y0:y1, x0:x1] = np.clip(over(src, region), 0, 255).astype(np.uint8)
        if backing:
            final = add_backing(final)
        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(out_path), final)
    log(f"hook: {out_path.name} ({size}px, {len(emojis)} emoji)")
    return out_path


def cache_name(text, colour, box_h, backing=False, width=W):
    key = f"{VERSION}|{text.strip()}|{colour}|{box_h}|{int(bool(backing))}|{width}".encode("utf-8")
    return hashlib.sha256(key).hexdigest()[:20] + ".png"


def cached(folder, text, colour, box_h, backing=False, width=W, start_size=None):
    """The hook PNG for these settings in `folder`, drawn once and kept; None for an empty hook."""
    path = Path(folder) / cache_name(text, colour, box_h, backing, width)
    if path.exists():
        return path
    return render(text, colour, box_h, path, backing, width, start_size)


def for_edit(folder, edit):
    """The hook image an edit shows, or None: on a dark backing unless it sits in the black band."""
    from .edit import hook_box

    if not edit.hook.on or not edit.hook.text.strip():
        return None
    return cached(folder, edit.hook.text, edit.hook.color, hook_box(edit.layout)[1], backing=not edit.layout.band_h)
