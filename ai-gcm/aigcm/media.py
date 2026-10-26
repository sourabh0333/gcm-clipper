"""ffmpeg, ffprobe and yt-dlp wrappers."""

import json
import os
import shutil
import subprocess
from pathlib import Path

# Checked when ffmpeg is not on PATH, e.g. a build unzipped to C:\ffmpeg.
FFMPEG_DIRS = [os.environ.get("AIGCM_FFMPEG_DIR", ""), r"C:\ffmpeg\bin"]


def tool(name):
    path = shutil.which(name)
    for folder in FFMPEG_DIRS:
        if not path and folder:
            path = shutil.which(name, path=folder)
    if not path:
        raise RuntimeError(f"{name} not found. Install ffmpeg (see README) or set AIGCM_FFMPEG_DIR in .env.")
    return path


def run(cmd, cwd=None):
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        tail = "\n".join(proc.stderr.strip().splitlines()[-15:])
        raise RuntimeError(f"{Path(cmd[0]).name} failed ({proc.returncode}):\n{tail}")
    return proc.stdout


def parse_time(text):
    """'1:30:00', '90:00' or '5400' -> seconds."""
    seconds = 0.0
    for part in text.strip().split(":"):
        seconds = seconds * 60 + float(part)
    return seconds


def is_url(source):
    return str(source).startswith(("http://", "https://"))


def download(url, out_dir, height=720, section=None):
    """Download a YouTube video (optionally only a time range) as out_dir/source.mp4."""
    import yt_dlp
    from yt_dlp.utils import download_range_func

    # yt-dlp's partial-download check ignores ffmpeg_location, so make sure ffmpeg is on PATH too.
    ffmpeg_dir = str(Path(tool("ffmpeg")).parent)
    if ffmpeg_dir not in os.environ.get("PATH", ""):
        os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")
    # Sorting by "res" limits the shorter side, so vertical streams also come down at 720x1280 rather than
    # 405x720. 30 fps is enough for clips and about half the download of 60 fps; H.264 decodes fastest.
    opts = {
        "format": "bv*+ba/b",
        "format_sort": [f"res:{height}", "fps:30", "vcodec:h264", "acodec:aac"],
        "outtmpl": str(Path(out_dir) / "source.%(ext)s"),
        "merge_output_format": "mp4",
        "ffmpeg_location": ffmpeg_dir,
        # YouTube now needs a JavaScript runtime to unlock full-speed downloads; Node is the one installed here.
        "js_runtimes": {"node": {"path": shutil.which("node")}},
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,
    }
    if section:
        opts["download_ranges"] = download_range_func(None, [section])
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
    path = Path(out_dir) / "source.mp4"
    if not path.exists():
        raise RuntimeError("Download finished but source.mp4 is missing.")
    keep = ("id", "title", "uploader", "channel", "channel_follower_count", "duration", "upload_date",
            "webpage_url", "was_live", "language")
    return path, {k: info.get(k) for k in keep}


def search(query, limit=10):
    """List YouTube search results without downloading anything."""
    import yt_dlp

    opts = {"quiet": True, "no_warnings": True, "extract_flat": True}
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(f"ytsearch{limit}:{query}", download=False)
    return [{k: e.get(k) for k in ("title", "channel", "duration", "url", "view_count")}
            for e in info.get("entries", [])]


def probe(path):
    out = run([tool("ffprobe"), "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)])
    data = json.loads(out)
    video = next(s for s in data["streams"] if s["codec_type"] == "video")
    num, den = video.get("avg_frame_rate", "0/1").split("/")
    return {
        "duration": float(data["format"]["duration"]),
        "width": int(video["width"]),
        "height": int(video["height"]),
        "fps": float(num) / float(den) if float(den) else 0.0,
        "has_audio": any(s["codec_type"] == "audio" for s in data["streams"]),
    }


def extract_audio(src, dst, start=None, duration=None):
    """Mono 16 kHz WAV, the format the audio analysis and Whisper both use."""
    cmd = [tool("ffmpeg"), "-v", "error", "-y"]
    if start is not None:
        cmd += ["-ss", f"{start:.3f}"]
    cmd += ["-i", str(src)]
    if duration is not None:
        cmd += ["-t", f"{duration:.3f}"]
    cmd += ["-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(dst)]
    run(cmd)


def extract_frame(src, t, dst):
    run([tool("ffmpeg"), "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", str(src), "-frames:v", "1", "-q:v", "2", str(dst)])


def cut_preview(src, start, end, dst, height=360):
    """Small, low-bitrate cut used only for the Gemini judge."""
    run([tool("ffmpeg"), "-v", "error", "-y", "-ss", f"{start:.3f}", "-i", str(src), "-t", f"{end - start:.3f}",
         "-vf", f"scale=-2:{height},fps=15", "-c:v", "libx264", "-preset", "veryfast", "-crf", "32",
         "-c:a", "aac", "-b:a", "64k", "-ac", "1", str(dst)])
