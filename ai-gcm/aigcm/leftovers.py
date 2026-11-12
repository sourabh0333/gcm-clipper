"""Leftover fights (Highlights Stage 1, decision 8): fights with kills that no highlight used are kept for three
weeks after the stream, ready for a later "part 2" or a compilation. The recording itself is deleted after
14 days (source_keep_days), so just before that each leftover fight is copied out as a small window (stream
copy, no re-encode); the windows go after 21 days."""

import time
from pathlib import Path

from .jobs import log, read_json, write_json

KEEP_DAYS = 21
FOLDER = "leftovers"
PAD_S = 15.0


def used_spans(job_folder):
    """Source spans used by the stream's highlights (every piece of every highlight plan)."""
    spans = []
    for plan in Path(job_folder, "highlights").glob("*/plan.json"):
        spans += [(p["start"], p["end"]) for p in (read_json(plan, {}) or {}).get("pieces", []) if "start" in p]
    return spans


def unused_fights(stream_map, used):
    """Fights with kills that no highlight covers, in stream order."""
    out = []
    for m in (stream_map or {}).get("matches", []):
        for i, f in enumerate(m.get("fights") or []):
            if not f.get("kills"):
                continue
            if any(a <= f["start"] and f["end"] <= b for a, b in used):
                continue
            out.append({"match": m["n"], "fight": i, "start": f["start"], "end": f["end"], "kills": f["kills"]})
    return out


def finished_at(job_folder):
    clips = Path(job_folder, "clips.json")
    return clips.stat().st_mtime if clips.exists() else None


def keep(job_folder, source):
    """Copy the leftover fights out of the recording before it is deleted. Returns how many were saved."""
    from .studio.window import cut_window

    job_folder = Path(job_folder)
    stream_map = read_json(job_folder / "map.json")
    done = finished_at(job_folder)
    if not stream_map or done is None:
        return 0
    fights = unused_fights(stream_map, used_spans(job_folder))
    out = job_folder / FOLDER
    out.mkdir(exist_ok=True)
    saved = []
    for f in fights:
        name = f"m{f['match']}_f{f['fight']}.mkv"
        try:
            offset = cut_window(source, max(0.0, f["start"] - PAD_S), f["end"] + PAD_S, out / name)
        except Exception as exc:     # one bad cut must not stop the rest (or the cleanup)
            log(f"leftovers: {job_folder.name} {name}: {exc}")
            continue
        saved.append(dict(f, file=name, offset=round(offset, 3)))
    if saved:
        write_json(out / "leftovers.json", {"kept_until": done + KEEP_DAYS * 86400, "fights": saved})
        log(f"leftovers: {job_folder.name}: {len(saved)} fights kept for {KEEP_DAYS} days")
    return len(saved)


def expire(jobs_dir, now=None):
    """Remove leftover windows older than KEEP_DAYS. Returns the job folders cleared."""
    import shutil

    now = now or time.time()
    cleared = []
    for listing in Path(jobs_dir).glob(f"*/{FOLDER}/leftovers.json"):
        if (read_json(listing, {}) or {}).get("kept_until", 0) <= now:
            shutil.rmtree(listing.parent, ignore_errors=True)
            cleared.append(listing.parent.parent.name)
    return cleared


def summary(job_folder):
    """For the stream page: how many fights no highlight used yet, and until when they're kept."""
    job_folder = Path(job_folder)
    saved = read_json(job_folder / FOLDER / "leftovers.json")
    if saved:
        return {"count": len(saved["fights"]), "until": saved["kept_until"]}
    done = finished_at(job_folder)
    fights = unused_fights(read_json(job_folder / "map.json"), used_spans(job_folder))
    return {"count": len(fights), "until": done + KEEP_DAYS * 86400 if done else None}
