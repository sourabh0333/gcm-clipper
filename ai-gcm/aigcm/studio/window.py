"""Working windows: the part of the source kept for editing a kept clip, so the 3-hour source can still be
deleted after 14 days (M3 review S-R1), and the small preview copy the phone plays (S-R2).

Each kept clip gets a folder `studio/<clip key>/` in its job folder:

    window.mkv    the source from a keyframe at or before the window start, stream-copied (no quality loss)
    preview.mp4   540p, a keyframe every second for quick seeking on a phone, about 1 Mbps
    strip.jpg     filmstrip for the timeline: one small frame every STRIP_EVERY_S seconds, in a grid
    wave.json     loudness peaks for the timeline, one per WAVE_STEP_S
    window.json   written last: start and end in source seconds, size, and the strip's grid

Window time 0 is source time `start`, in all three files."""

import json
import math
import os
import shutil
import wave
from pathlib import Path

from ..jobs import log, read_json, write_json
from ..media import probe, run, tool

CONTEXT_S = 60.0        # footage kept before and after the clip
FIGHT_GAP_S = 30.0      # kills closer than this belong to one fight
FIGHT_PAD_S = 15.0
MAX_WINDOW_S = 240.0
PREVIEW_SHORT_SIDE = 540
STRIP_EVERY_S = 2.0
STRIP_TILE_W = 96
STRIP_COLS = 10
WAVE_STEP_S = 0.1
FIGHT_KINDS = ("self_kill", "knock", "accolade", "chicken_dinner")


def studio_dir(job_folder, clip_key):
    return Path(job_folder) / "studio" / Path(clip_key).name


def ready(folder):
    """The window's details once it is complete, else None."""
    info = read_json(Path(folder) / "window.json")
    if info and (Path(folder) / "window.mkv").exists() and (Path(folder) / "preview.mp4").exists():
        return info
    return None


def fight_span(events, start, end):
    """The whole fight around the clip: its events chained with neighbours closer than FIGHT_GAP_S."""
    times = sorted(e["t"] for e in events or () if e.get("kind") in FIGHT_KINDS)
    inside = [t for t in times if start <= t <= end]
    if not inside:
        return None
    lo, hi = min(inside), max(inside)
    for t in reversed([t for t in times if t < lo]):
        if lo - t > FIGHT_GAP_S:
            break
        lo = t
    for t in [t for t in times if t > hi]:
        if t - hi > FIGHT_GAP_S:
            break
        hi = t
    return lo, hi


def plan_window(start, end, duration, events=()):
    """Source span to keep: the clip ±CONTEXT_S and its whole fight, at most MAX_WINDOW_S, clip inside."""
    a, b = start - CONTEXT_S, end + CONTEXT_S
    span = fight_span(events, start, end)
    if span:
        a, b = min(a, span[0] - FIGHT_PAD_S), max(b, span[1] + FIGHT_PAD_S)
    left, right = start - a, b - end
    budget = max(0.0, MAX_WINDOW_S - (end - start))
    if left + right > budget:
        k = budget / (left + right)
        left, right = left * k, right * k
    return max(0.0, start - left), min(duration, end + right)


def _start_time(source):
    out = run([tool("ffprobe"), "-v", "error", "-show_entries", "format=start_time", "-of", "csv=p=0", str(source)])
    try:
        return float(out.strip() or 0)
    except ValueError:
        return 0.0


def keyframes_before(source, t):
    """Video keyframe times (seconds from the file's start) shortly before source time t, oldest first."""
    if t <= 0.05:
        return [0.0]
    base = _start_time(source)
    for reach in (20.0, 120.0):
        out = run([tool("ffprobe"), "-v", "error", "-select_streams", "v:0", "-skip_frame", "nokey",
                   "-show_entries", "frame=pts_time", "-of", "csv=p=0",
                   "-read_intervals", f"{base + max(0.0, t - reach):.3f}%{base + t + 0.01:.3f}", str(source)])
        # One line per keyframe; side data can add trailing comma-separated fields.
        values = [line.split(",")[0].strip() for line in out.splitlines()]
        found = sorted(float(x) - base for x in values if x not in ("", "N/A"))
        found = [k for k in found if k <= t + 0.01]
        if found:
            return found
    return []


def _video_start(path):
    out = run([tool("ffprobe"), "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=start_time",
               "-of", "csv=p=0", str(path)])
    try:
        return float(out.strip().split(",")[0] or 0)
    except ValueError:
        return 0.0


def cut_window(source, start, end, out_path):
    """Copy source [start, end] into out_path without re-encoding and return the source time of the
    window's time 0.

    A stream copy has to begin on a keyframe. Asked to start exactly on one, ffmpeg's seek lands a whole
    keyframe earlier (measured 9 Nov: -ss 1039.101 began at 1034.1 on the Aashi stream), so the cut is asked
    to start a little after the keyframe, and the start it really got is confirmed by snapping the
    measured start to the known keyframe list. If that doesn't line up, the window is cut exactly by
    re-encoding instead."""
    end = min(end, probe(source)["duration"])
    keys = keyframes_before(source, start)
    if keys:
        key = keys[-1]
        seek = key + 0.3
        run([tool("ffmpeg"), "-v", "error", "-y", "-ss", f"{seek:.3f}", "-i", str(source),
             "-t", f"{end - seek:.3f}", "-map", "0:v:0", "-map", "0:a:0?", "-c", "copy",
             "-avoid_negative_ts", "make_zero", str(out_path)])
        video_at = _video_start(out_path)          # the first video frame, in window time
        measured = end - probe(out_path)["duration"] + video_at
        nearest = min(keys, key=lambda k: abs(k - measured))
        if abs(nearest - measured) < 0.5:
            return nearest - video_at
        log(f"studio: copy cut started at {measured:.2f}s, not on a known keyframe; re-encoding the window")
    run([tool("ffmpeg"), "-v", "error", "-y", "-ss", f"{start:.3f}", "-i", str(source), "-t", f"{end - start:.3f}",
         "-map", "0:v:0", "-map", "0:a:0?", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
         "-c:a", "aac", "-b:a", "192k", str(out_path)])
    return start


def make_preview(window, out_path, width, height, threads=3):
    scale = f"-2:{PREVIEW_SHORT_SIDE}" if width >= height else f"{PREVIEW_SHORT_SIDE}:-2"
    run([tool("ffmpeg"), "-v", "error", "-y", "-i", str(window), "-vf", f"scale={scale}",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "30", "-maxrate", "1200k", "-bufsize", "2400k",
         "-force_key_frames", "expr:gte(t,n_forced*1)", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "96k", "-ac", "2", "-movflags", "+faststart", "-threads", str(threads),
         str(out_path)])


def make_strip(window, out_path, duration, width, height):
    frames = max(1, math.ceil(duration / STRIP_EVERY_S))
    rows = math.ceil(frames / STRIP_COLS)
    tile_h = int(round(STRIP_TILE_W * height / width / 2)) * 2
    run([tool("ffmpeg"), "-v", "error", "-y", "-i", str(window), "-vf",
         f"fps=1/{STRIP_EVERY_S},scale={STRIP_TILE_W}:{tile_h},tile={STRIP_COLS}x{rows}",
         "-frames:v", "1", "-q:v", "5", str(out_path)])
    return {"every_s": STRIP_EVERY_S, "cols": STRIP_COLS, "rows": rows, "frames": frames,
            "tile_w": STRIP_TILE_W, "tile_h": tile_h}


def make_wave(window, out_path, duration, has_audio):
    peaks = []
    if has_audio:
        import numpy as np

        wav = Path(out_path).with_suffix(".wav")
        run([tool("ffmpeg"), "-v", "error", "-y", "-i", str(window), "-vn", "-ac", "1", "-ar", "8000",
             "-c:a", "pcm_s16le", str(wav)])
        with wave.open(str(wav), "rb") as f:
            samples = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32)
        wav.unlink(missing_ok=True)
        step = int(8000 * WAVE_STEP_S)
        if samples.size:
            n = math.ceil(samples.size / step)
            padded = np.zeros(n * step, dtype=np.float32)
            padded[:samples.size] = np.abs(samples)
            level = padded.reshape(n, step).max(axis=1)
            top = max(float(np.percentile(level, 99)), 1.0)
            peaks = [int(min(100, round(100 * v / top))) for v in level]
    Path(out_path).write_text(json.dumps({"step_s": WAVE_STEP_S, "peaks": peaks}), encoding="utf-8")


def prepare(source, folder, start, end, threads=3):
    """Make the window, preview copy, filmstrip and wave for source span [start, end]. Idempotent: a
    complete window is returned as it is."""
    folder = Path(folder)
    done = ready(folder)
    if done:
        return done
    folder.mkdir(parents=True, exist_ok=True)
    window = folder / "window.mkv"
    real_start = cut_window(source, start, end, window)
    info = probe(window)
    preview_tmp = folder / "preview.tmp.mp4"
    make_preview(window, preview_tmp, info["width"], info["height"], threads)
    os.replace(preview_tmp, folder / "preview.mp4")
    strip = make_strip(window, folder / "strip.jpg", info["duration"], info["width"], info["height"])
    make_wave(window, folder / "wave.json", info["duration"], info["has_audio"])
    details = {"start": round(real_start, 3), "end": round(real_start + info["duration"], 3),
               "duration": round(info["duration"], 3), "width": info["width"], "height": info["height"],
               "fps": info["fps"], "has_audio": info["has_audio"], "strip": strip}
    write_json(folder / "window.json", details)
    log(f"studio: window {folder.name} {details['start']:.1f}-{details['end']:.1f}s ready")
    return details


def remove(folder):
    shutil.rmtree(folder, ignore_errors=True)
