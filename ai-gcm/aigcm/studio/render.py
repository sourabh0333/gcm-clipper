"""Renders an edit list into the final 1080x1920 video from the clip's working window.

The filter graph: each part is trimmed from the window and sped up if asked (video `setpts`, audio
`atempo`, which keeps the pitch), the parts are joined, then the layout draws the background and each
panel (a crop of the frame, scaled into its canvas rectangle). A zoom on the kill grows the game panel's
picture with `scale` evaluated per frame and crops it back to the panel size, centred, so the crosshair
stays in place (tested in the M3 review, S-R6). Captions are burned from an ASS file and the sponsor-safe
version silences the flagged words. No user text ever enters the filter graph (S-R11)."""

import os
import tempfile
from pathlib import Path

from ..jobs import log
from ..media import run, tool
from ..safety import mute_filter
from .edit import H, W, span_to_output, to_output

FPS = 30
ZOOM_IN_S = 0.25
ZOOM_OUT_S = 0.35
ZOOM_LEAD_S = 0.4      # the zoom starts this long before the kill
CAPTION_MARGIN = {"native": 560, "blur": 380, "band": 380, "split": 260}


def zoom_expr(edit):
    """The game panel's zoom factor as an ffmpeg expression of output time t, or None without zooms."""
    terms = []
    for z in edit.zooms:
        at = to_output(edit.segments, z.t)
        if at is None or z.scale <= 1.0:
            continue
        a, b = max(0.0, at - ZOOM_LEAD_S), at + z.dur
        terms.append(f"{z.scale - 1:.3f}*clip((t-{a:.3f})/{ZOOM_IN_S},0,1)*clip(({b:.3f}-t)/{ZOOM_OUT_S},0,1)")
    return "1+" + "+".join(terms) if terms else None


def _panel_chain(panel, zoom):
    x, y, w, h = panel.src
    dw, dh = panel.dst[2] // 2 * 2, panel.dst[3] // 2 * 2
    chain = (f"crop=iw*{w:.5f}:ih*{h:.5f}:iw*{x:.5f}:ih*{y:.5f},"
             f"scale={dw}:{dh}:force_original_aspect_ratio=increase,crop={dw}:{dh},setsar=1")
    if zoom and panel.role == "game":
        chain += (f",scale=w='2*trunc({dw}*({zoom})/2)':h='2*trunc({dh}*({zoom})/2)':eval=frame,"
                  f"crop={dw}:{dh}")
    return chain


def build_graph(edit, input_start, has_audio, captions_name=None, mute=()):
    """The -filter_complex text. `input_start` is the source time of the input's first frame (after any
    `-ss`), so the parts are trimmed relative to it; zooms stay in source time. `mute` is output-time spans
    to silence."""
    segs = edit.segments
    n = len(segs)
    lines = []
    vlabels = [f"[vs{i}]" for i in range(n)]
    lines.append(f"[0:v]split={n}" + "".join(vlabels) if n > 1 else "[0:v]null[vs0]")
    if has_audio:
        alabels = [f"[as{i}]" for i in range(n)]
        lines.append(f"[0:a]asplit={n}" + "".join(alabels) if n > 1 else "[0:a]anull[as0]")
    joined = ""
    for i, s in enumerate(segs):
        a, b = s.start - input_start, s.end - input_start
        lines.append(f"[vs{i}]trim=start={a:.3f}:end={b:.3f},setpts=(PTS-STARTPTS)/{s.speed:g}[v{i}]")
        joined += f"[v{i}]"
        if has_audio:
            tempo = f",atempo={s.speed:g}" if s.speed != 1 else ""
            lines.append(f"[as{i}]atrim=start={a:.3f}:end={b:.3f},asetpts=PTS-STARTPTS{tempo}[a{i}]")
            joined += f"[a{i}]"
    lines.append(f"{joined}concat=n={n}:v=1:a={1 if has_audio else 0}[cv]" + ("[ca]" if has_audio else ""))

    layout = edit.layout
    k = 1 + len(layout.panels)
    lines.append(f"[cv]fps={FPS},split={k}[bgsrc]" + "".join(f"[ps{i}]" for i in range(len(layout.panels))))
    if layout.background == "blur":
        lines.append(f"[bgsrc]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=24:2,"
                     f"setsar=1[bg]")
    else:
        lines.append(f"[bgsrc]scale={W}:{H},setsar=1,drawbox=x=0:y=0:w=iw:h=ih:color=black:t=fill[bg]")
    zoom = zoom_expr(edit)
    base = "[bg]"
    for i, panel in enumerate(layout.panels):
        lines.append(f"[ps{i}]{_panel_chain(panel, zoom)}[p{i}]")
        lines.append(f"{base}[p{i}]overlay={panel.dst[0]}:{panel.dst[1]}[o{i}]")
        base = f"[o{i}]"
    tail = f",subtitles={captions_name}" if captions_name else ""
    lines.append(f"{base}null{tail},format=yuv420p[v]")
    if has_audio:
        silence = f"{mute_filter(mute)}," if mute else ""
        lines.append(f"[ca]{silence}aresample=48000[a]")
    return ";".join(lines)


def caption_chunks(edit, transcript):
    """Caption chunks in output time: the words spoken inside each part, timed through the cuts."""
    from ..captions import chunk_words

    words = []
    for seg in transcript.get("segments", []) if transcript else []:
        for w in seg.get("words", []):
            start, end = to_output(edit.segments, w["start"]), to_output(edit.segments, w["end"])
            if start is not None and end is not None and end > start:
                words.append(dict(w, start=start, end=end))
    words.sort(key=lambda w: w["start"])
    return chunk_words(words)


def output_mute(edit, clip_start, spans):
    """The clip's flagged-word spans (seconds from the engine clip's start) in output time."""
    out = []
    for a, b in spans or ():
        out += span_to_output(edit.segments, clip_start + a, clip_start + b)
    return out


def render(edit, window_file, window_start, has_audio, out_path, transcript=None, mute_spans=(), threads=3):
    """Render `edit` from the window file (time 0 = source time `window_start`) into out_path."""
    from ..captions import to_ass

    out_path = Path(out_path)
    first = min(s.start for s in edit.segments) - window_start
    seek = max(0.0, first - 1.0)
    with tempfile.TemporaryDirectory(prefix="kaatclip_render_") as tmp:
        captions_name = None
        if edit.captions.on and transcript:
            chunks = caption_chunks(edit, transcript)
            if chunks:
                captions_name = "captions.ass"
                margin = CAPTION_MARGIN.get(edit.layout.template, 380)
                (Path(tmp) / captions_name).write_text(to_ass(chunks, margin), encoding="utf-8")
        graph = build_graph(edit, window_start + seek, has_audio, captions_name, mute_spans)
        partial = out_path.with_name(out_path.stem + ".part.mp4")
        cmd = [tool("ffmpeg"), "-v", "error", "-y", "-ss", f"{seek:.3f}", "-i", str(Path(window_file).resolve()),
               "-filter_complex", graph, "-filter_complex_threads", str(threads), "-map", "[v]"]
        if has_audio:
            cmd += ["-map", "[a]", "-c:a", "aac", "-b:a", "128k"]
        cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-r", str(FPS), "-threads", str(threads),
                "-movflags", "+faststart", str(partial.resolve())]
        # The ASS file is named relative to the working folder: it avoids ffmpeg's Windows path escaping.
        try:
            run(cmd, cwd=tmp)
        except BaseException:
            partial.unlink(missing_ok=True)
            raise
    os.replace(partial, out_path)
    log(f"studio: rendered {out_path.name}")
    return out_path
