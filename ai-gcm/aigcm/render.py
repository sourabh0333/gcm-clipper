"""Cuts the final 1080x1920 clips.

"blur" layout: the whole gameplay frame, full width, over a blurred, zoomed copy of itself, so the kill
feed and HUD stay visible. "split" layout: the facecam on top and the full gameplay frame below it.
Captions are burned in from the clip's .ass file."""

import shutil

from .jobs import log
from .media import run, tool

W, H = 1080, 1920
FACECAM_H = 760

# Where captions sit, measured up from the bottom edge, for each layout.
CAPTION_MARGIN = {"blur": 380, "split": 260}


def _filter(layout, info, facecam, captions):
    gameplay_h = int(round(W * info["height"] / info["width"] / 2) * 2)
    if layout == "split" and facecam:
        fx, fy, fw, fh = facecam
        crop = (f"crop=iw*{fw}:ih*{fh}:iw*{fx}:ih*{fy},"
                f"scale={W}:{FACECAM_H}:force_original_aspect_ratio=increase,crop={W}:{FACECAM_H}")
        graph = (f"[0:v]split=3[a][b][c];"
                 f"[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=24:2[bg];"
                 f"[b]{crop}[cam];"
                 f"[c]scale={W}:{gameplay_h}[game];"
                 f"[bg][cam]overlay=0:0[t];[t][game]overlay=0:{FACECAM_H}")
    else:
        graph = (f"[0:v]split=2[a][b];"
                 f"[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=24:2[bg];"
                 f"[b]scale={W}:{gameplay_h}[game];"
                 f"[bg][game]overlay=0:(H-h)/2")
    if captions:
        # Relative name: the command runs inside the clips folder, which avoids ffmpeg's Windows path escaping.
        graph += f",subtitles={captions.name}"
    return graph + ",format=yuv420p[v]"


def render_clip(source, clip, info, settings, out_dir, captions=None):
    out = out_dir / f"{clip['rank']:02d}_{clip['type']}_{clip['id']}.mp4"
    local_captions = None
    if captions and captions.exists():
        local_captions = out_dir / captions.name
        shutil.copyfile(captions, local_captions)
    graph = _filter(settings.layout, info, settings.facecam, local_captions)
    cmd = [tool("ffmpeg"), "-v", "error", "-y", "-ss", f"{clip['start']:.3f}", "-i", str(source),
           "-t", f"{clip['end'] - clip['start']:.3f}", "-filter_complex", graph, "-map", "[v]", "-map", "0:a?",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-r", "30",
           "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", out.name]
    run(cmd, cwd=out_dir)
    if local_captions:
        local_captions.unlink(missing_ok=True)
    log(f"render: {out.name}")
    return out.name
