"""Reading an engine job folder for the platform: progress while it runs, and its clips once it is done.
Light on purpose (no engine imports), because both the API and the worker use it."""

import re
from pathlib import Path

from .jobs import STAGES, read_json

# Rough share of a job's time each stage takes (measured on uploaded sources, where ingest is only the
# ffprobe check and the audio track); only for the progress bar.
STAGE_WEIGHT = {"ingest": 0.03, "vision": 0.55, "audio": 0.01, "sounds": 0.02, "transcript": 0.17, "moments": 0.02,
                "judge": 0.08, "captions": 0.0, "render": 0.12, "review": 0.0}
SCANNED = re.compile(r"vision: (\d+) min scanned")
NOISE = ("W0000", "I0000", "absl", "XNNPACK", "WARNING")


def read_text(path, tail=64 * 1024):
    """The end of a text file: a long job's run.log runs to megabytes, and only its last lines matter."""
    path = Path(path)
    if not path.exists():
        return ""
    with open(path, "rb") as f:
        size = f.seek(0, 2)
        f.seek(max(0, size - tail))
        return f.read().decode("utf-8", errors="replace")


def last_line(text):
    lines = [line for line in text.splitlines()
             if line.strip() and not line.startswith("---") and not any(n in line for n in NOISE)]
    return lines[-1][:200] if lines else None


def progress(folder, duration_s=None):
    """{"stages": [{name, status, seconds}], "fraction": 0..1, "last_log": str} for a job folder."""
    folder = Path(folder)
    manifest = read_json(folder / "manifest.json", {"stages": {}})["stages"]
    stages = [{"name": s, "status": manifest.get(s, {}).get("status", "pending"),
               "seconds": manifest.get(s, {}).get("seconds")} for s in STAGES]
    fraction = sum(STAGE_WEIGHT[s["name"]] for s in stages if s["status"] == "done")
    log = read_text(folder / "run.log")
    scanned = SCANNED.findall(log)
    if manifest.get("vision", {}).get("status") == "running" and scanned and duration_s:
        fraction += STAGE_WEIGHT["vision"] * min(1.0, int(scanned[-1]) * 60 / duration_s)
    return {"stages": stages, "fraction": round(min(fraction, 1.0), 3), "last_log": last_line(log)}


def failure(folder):
    """Why a job failed, in a line: the failed stage's error, else the log's last line."""
    folder = Path(folder)
    for name, entry in read_json(folder / "manifest.json", {"stages": {}})["stages"].items():
        if entry.get("status") == "failed":
            return f"{name}: {entry.get('error') or 'failed'}"[:500]
    return (last_line(read_text(folder / "run.log")) or "The job stopped without a reason.")[:500]


def finished_clips(folder):
    """The job's rendered clips, best first, as plain dicts ready for the clips table."""
    folder = Path(folder)
    files = read_json(folder / "clips.json", {})
    out = []
    for clip in read_json(folder / "ranked.json", []):
        if clip["id"] not in files or not (folder / "clips" / files[clip["id"]]).exists():
            continue
        safe = files.get(clip["id"] + "_safe")
        details = {k: clip.get(k) for k in ("titles", "hashtags", "description", "labels", "flags", "reasons",
                                            "mute_spans", "players_left", "anchor")}
        out.append({"clip_key": clip["id"], "rank": clip.get("rank") or len(out) + 1, "start_s": clip["start"],
                    "end_s": clip["end"], "type": clip.get("type", "moment"),
                    "score": clip.get("final_score", clip.get("score")), "file_name": files[clip["id"]],
                    "safe_file_name": safe if safe and (folder / "clips" / safe).exists() else None,
                    "title": clip.get("title"), "why": clip.get("why"), "details": details})
    return out
