"""Build the demo jobs in demo/: a finished job with placeholder clips, one still processing and one that
failed. They let the app's screens be built and checked without downloading or processing a stream.

    python make_demo.py

Point the app at them with AIGCM_JOBS_DIR=demo. The clips are coloured cards with text, not real footage.
"""

import shutil
from pathlib import Path

from aigcm import review
from aigcm.jobs import write_json
from aigcm.media import run, tool

DEMO = Path(__file__).resolve().parent / "demo"
FONT = Path("C:/Windows/Fonts/arial.ttf")

INFO = {
    "source": "https://www.youtube.com/watch?v=demo0000001",
    "id": "demo0000001",
    "title": "Demo stream: rush gameplay | BGMI",
    "uploader": "Demo Streamer",
    "channel": "Demo Streamer",
    "duration": 1800.0,
    "webpage_url": "https://www.youtube.com/watch?v=demo0000001",
    "was_live": True,
    "width": 720,
    "height": 1280,
    "fps": 30.0,
    "has_audio": True,
    "path": None,
    "section": [1800.0, 3600.0],
}

# (start, end, type, kill times, players left, score, colour) for each placeholder clip, best first.
CLIPS = [
    (277.5, 305.5, "multi_kill", [289.5, 293.0, 299.5], 9, 100.0, "0x1d3557"),
    (1146.0, 1165.0, "fight", [1158.0, 1159.0], 41, 94.0, "0x6a040f"),
    (622.0, 640.0, "fight", [634.0], 72, 71.5, "0x2d6a4f"),
    (1502.0, 1520.0, "reaction", [], 23, 52.0, "0x7b2cbf"),
]


def event(t, n):
    return {"t": t, "kind": "self_kill", "text": f"eliminations {n} -> {n + 1}", "region": "counter"}


def clip_record(rank, start, end, kind, kills, players_left, score):
    reasons = []
    if players_left <= 10:
        reasons.append(f"final circles ({players_left} players left)")
    reasons.append(f"{len(kills)} kill{'s' if len(kills) > 1 else ''} by the streamer" if kills else "loud reaction")
    return {
        "start": start, "end": end, "events": [event(t, n) for n, t in enumerate(kills)],
        "source": "hud" if kills else "audio", "players_left": players_left, "audio_peak": 1.5,
        "action_ratio": 1.0, "score": round(score * 0.4, 2), "type": kind, "reasons": reasons,
        "id": f"m{rank:02d}", "heuristic_rank": rank, "detector_score": score, "judge": None,
        "final_score": score, "rank": rank,
    }


def placeholder(dst, rank, kind, kills, colour, seconds):
    """A 540x960 card with the clip's rank and type, a running clock and a quiet tone."""
    font = "fontfile=arial.ttf:" if FONT.exists() else ""
    label = f"{kind.replace('_', ' ')}, {len(kills)} kills" if kills else kind
    text = [f"drawtext={font}text='DEMO CLIP {rank}':fontsize=64:fontcolor=white:x=(w-tw)/2:y=h*0.30",
            f"drawtext={font}text='{label}':fontsize=44:fontcolor=white:x=(w-tw)/2:y=h*0.42",
            f"drawtext={font}text='%{{pts\\:hms}}':fontsize=36:fontcolor=white@0.8:x=(w-tw)/2:y=h*0.80"]
    run([tool("ffmpeg"), "-v", "error", "-y",
         "-f", "lavfi", "-i", f"color=c={colour}:s=540x960:d={seconds}:r=30",
         "-f", "lavfi", "-i", f"sine=frequency=330:duration={seconds}",
         "-vf", ",".join(text), "-af", "volume=0.1",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "30", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "48k", "-shortest", "-movflags", "+faststart", str(dst)],
        cwd=FONT.parent if FONT.exists() else None)


def manifest(done, current=None, status=None, error=None):
    stages = {name: {"status": "done", "error": None, "seconds": seconds} for name, seconds in done}
    if current:
        stages[current] = {"status": status, "error": error}
    return {"stages": stages}


def settings_file(job):
    write_json(job / "settings.json", {"source": INFO["source"], "section": INFO["section"], "layout": "auto",
                                       "facecam": None, "top_n": 12})


def finished():
    job = DEMO / "demo-finished"
    (job / "clips").mkdir(parents=True)
    ranked, files = [], {}
    for rank, (start, end, kind, kills, players_left, score, colour) in enumerate(CLIPS, 1):
        clip = clip_record(rank, start, end, kind, kills, players_left, score)
        name = f"{rank:02d}_{kind}_{clip['id']}.mp4"
        placeholder(job / "clips" / name, rank, kind, kills, colour, end - start)
        ranked.append(clip)
        files[clip["id"]] = name
    write_json(job / "info.json", INFO)
    write_json(job / "ranked.json", ranked)
    write_json(job / "clips.json", files)
    settings_file(job)
    write_json(job / "manifest.json", manifest([("ingest", 1057.6), ("vision", 1240.1), ("audio", 0.3),
                                                ("moments", 0.1), ("judge", 0.0), ("captions", 61.8),
                                                ("render", 120.8), ("review", 0.0)]))
    ranked = [dict(c, file=files[c["id"]]) for c in ranked]
    (job / "review.html").write_text(review.build(job.name, INFO, ranked), encoding="utf-8")


def processing():
    job = DEMO / "demo-processing"
    job.mkdir(parents=True)
    write_json(job / "info.json", INFO)
    settings_file(job)
    write_json(job / "manifest.json", manifest([("ingest", 1057.6)], "vision", "running"))


def failed():
    job = DEMO / "demo-failed"
    job.mkdir(parents=True)
    settings_file(job)
    write_json(job / "manifest.json", manifest([], "ingest", "failed",
                                               "DownloadError('ERROR: [youtube] demo0000001: Video unavailable')"))


if __name__ == "__main__":
    shutil.rmtree(DEMO, ignore_errors=True)
    finished()
    processing()
    failed()
    print(f"demo jobs written to {DEMO}")
