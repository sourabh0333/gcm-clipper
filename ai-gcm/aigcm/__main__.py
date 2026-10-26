"""Command line: run a job, check its status, grab frames for calibration, search YouTube, score results."""

import argparse
import csv
import re
import shutil
import sys
from pathlib import Path

from . import audio, captions, judge, moments, render, review, vision
from .config import Settings
from .jobs import STAGES, Job, log, read_json, write_json
from .media import download, extract_audio, extract_frame, is_url, parse_time, probe, search

# Folders and files each stage writes, removed when that stage is forced to run again.
OUTPUTS = {
    "ingest": ["source.mp4", "audio.wav", "info.json"],
    "audio": ["audio.npz"],
    "vision": ["vision.json"],
    "moments": ["moments.json"],
    "judge": ["judge", "ranked.json"],
    "captions": ["captions"],
    "render": ["clips", "clips.json"],
    "review": ["review.html"],
}


def job_name(source, section):
    if is_url(source):
        match = re.search(r"(?:v=|youtu\.be/|/live/|/shorts/)([\w-]{11})", source)
        base = match.group(1) if match else "video"
    else:
        base = re.sub(r"[^\w-]+", "-", Path(source).stem)[:40]
    if section:
        base += f"_{int(section[0])}-{int(section[1])}"
    return base


def clear_from(job, stage):
    for name in STAGES[STAGES.index(stage):]:
        for item in OUTPUTS[name]:
            path = job.path(item)
            if path.is_dir():
                shutil.rmtree(path)
            elif path.exists():
                path.unlink()
    job.invalidate_from(stage)


def pipeline(job, source, section, settings, use_judge, use_captions, until=None):
    def ingest(job):
        info = {"source": source}
        if is_url(source):
            path, meta = download(source, job.root, settings.download_height, section)
            info.update(meta)
        else:
            path = job.path("source" + Path(source).suffix.lower())
            shutil.copyfile(source, path)
            info["title"] = Path(source).stem
        info.update(probe(path), path=str(path), section=section)
        extract_audio(path, job.path("audio.wav"))
        write_json(job.path("info.json"), info)

    def audio_stage(job):
        audio.save(job.path("audio.npz"), audio.analyse(job.path("audio.wav"), settings.audio_hop_s))

    def vision_stage(job):
        info = read_json(job.path("info.json"))
        write_json(job.path("vision.json"), vision.scan(info["path"], info, settings))

    def moments_stage(job):
        info = read_json(job.path("info.json"))
        seen = read_json(job.path("vision.json"))
        events = seen["events"]
        found = moments.build(events, audio.load(job.path("audio.npz")), settings, info["duration"],
                              seen.get("remaining", []))
        write_json(job.path("moments.json"), found)
        log(f"moments: {len(found)} candidates from {len(events)} HUD events")

    def judge_stage(job):
        info = read_json(job.path("info.json"))
        found = read_json(job.path("moments.json"))
        if use_judge and settings.gemini_api_key:
            judge.judge_all(job, info["path"], found, settings)
        elif use_judge:
            log("judge: no GEMINI_API_KEY in .env, ranking with the detector score only")
        ranked = judge.merge(job, found, settings)[: settings.top_n]
        for n, clip in enumerate(ranked, 1):
            clip["rank"] = n
        write_json(job.path("ranked.json"), ranked)

    def captions_stage(job):
        if not use_captions:
            log("captions: skipped")
            return
        info = read_json(job.path("info.json"))
        captions.caption_clips(job, info["path"], read_json(job.path("ranked.json")), settings,
                               render.CAPTION_MARGIN.get(settings.layout, 380))

    def render_stage(job):
        info = read_json(job.path("info.json"))
        ranked = read_json(job.path("ranked.json"))
        out_dir = job.path("clips")
        out_dir.mkdir(exist_ok=True)
        done = read_json(job.path("clips.json"), {})
        for clip in ranked:
            if clip["id"] in done and (out_dir / done[clip["id"]]).exists():
                continue
            ass = job.path("captions", f"{clip['id']}.ass")
            done[clip["id"]] = render.render_clip(info["path"], clip, info, settings, out_dir, ass)
            write_json(job.path("clips.json"), done)

    def review_stage(job):
        info = read_json(job.path("info.json"))
        files = read_json(job.path("clips.json"), {})
        ranked = [dict(c, file=files[c["id"]]) for c in read_json(job.path("ranked.json")) if c["id"] in files]
        job.path("review.html").write_text(review.build(job.root.name, info, ranked), encoding="utf-8")
        log(f"review: open {job.path('review.html')}")

    stages = {"ingest": ingest, "audio": audio_stage, "vision": vision_stage, "moments": moments_stage,
              "judge": judge_stage, "captions": captions_stage, "render": render_stage, "review": review_stage}
    for name in STAGES:
        job.run(name, stages[name])
        if name == until:
            log(f"stopped after {until}; run again without --until to continue")
            break


def cmd_run(args, settings):
    section = None
    if args.section:
        start, end = args.section.split("-")
        section = (parse_time(start), parse_time(end))
    if args.layout:
        settings.layout = args.layout
    if args.facecam:
        settings.facecam = tuple(float(v) for v in args.facecam.split(","))
        settings.layout = "split"
    if args.top:
        settings.top_n = args.top
    job = Job(settings.jobs_dir / (args.job or job_name(args.source, section)))
    saved = read_json(job.path("settings.json"))
    if saved:
        # A resumed job keeps the layout it started with unless the command line changes it.
        settings.layout = args.layout or ("split" if args.facecam else saved.get("layout", settings.layout))
        settings.facecam = settings.facecam or (tuple(saved["facecam"]) if saved.get("facecam") else None)
    write_json(job.path("settings.json"), {"source": args.source, "section": section, "layout": settings.layout,
                                          "facecam": settings.facecam, "top_n": settings.top_n})
    if args.force:
        clear_from(job, args.force)
    log(f"job folder: {job.root}")
    pipeline(job, args.source, section, settings, not args.no_judge, not args.no_captions, args.until)


def cmd_status(args, settings):
    job = Job(args.job)
    for name in STAGES:
        entry = job.manifest["stages"].get(name, {})
        extra = entry.get("error") or (f"{entry['seconds']}s" if entry.get("seconds") else "")
        print(f"{name:9} {entry.get('status', 'pending'):8} {extra}")


def cmd_frames(args, settings):
    job = Job(args.job)
    info = read_json(job.path("info.json"))
    out = job.path("frames")
    out.mkdir(exist_ok=True)
    for value in args.at.split(","):
        t = parse_time(value)
        dst = out / f"t{int(t):06d}.jpg"
        extract_frame(info["path"], t, dst)
        print(dst)


def cmd_find(args, settings):
    for item in search(args.query, args.limit):
        minutes = (item["duration"] or 0) / 60
        print(f"{minutes:6.0f} min  {item['channel']}  |  {item['title']}\n         {item['url']}")


def cmd_eval(args, settings):
    """Compare chosen clips with hand-labelled moments (CSV: start,end,type,rating in seconds)."""
    job = Job(args.job)
    clips = read_json(job.path("ranked.json"), [])
    with open(args.labels, newline="", encoding="utf-8") as f:
        labels = [{"start": parse_time(r["start"]), "end": parse_time(r["end"]), "type": r.get("type", ""),
                   "rating": int(r.get("rating") or 3)} for r in csv.DictReader(f)]

    def covers(clip, label):
        inter = min(clip["end"], label["end"]) - max(clip["start"], label["start"])
        return inter >= 0.5 * (label["end"] - label["start"])

    top = [l for l in labels if l["rating"] >= 4]
    found = [l for l in top if any(covers(c, l) for c in clips)]
    matched = [c for c in clips if any(covers(c, l) for l in labels)]
    print(f"top moments found: {len(found)}/{len(top)} ({100 * len(found) / max(1, len(top)):.0f}%)")
    print(f"clips that match a labelled moment: {len(matched)}/{len(clips)} "
          f"({100 * len(matched) / max(1, len(clips)):.0f}%)")
    missed = [l for l in top if l not in found]
    for l in missed:
        print(f"  missed {l['type'] or 'moment'} at {l['start']:.0f}-{l['end']:.0f}s (rating {l['rating']})")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="aigcm", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("run", help="process a YouTube URL or a local video")
    p.add_argument("source")
    p.add_argument("--section", help="only this part of a YouTube video, e.g. 0:30:00-1:30:00")
    p.add_argument("--job", help="job folder name (default: from the video id or file name)")
    p.add_argument("--top", type=int, help="number of clips to make (default 12)")
    p.add_argument("--layout", choices=["blur", "split"])
    p.add_argument("--facecam", help="facecam box as x,y,w,h fractions of the frame; implies --layout split")
    p.add_argument("--force", choices=STAGES, help="rerun this stage and everything after it")
    p.add_argument("--until", choices=STAGES, help="stop after this stage")
    p.add_argument("--no-judge", action="store_true", help="skip Gemini even if a key is set")
    p.add_argument("--no-captions", action="store_true")
    p.set_defaults(fn=cmd_run)

    p = sub.add_parser("status", help="show which stages of a job are done")
    p.add_argument("job")
    p.set_defaults(fn=cmd_status)

    p = sub.add_parser("frames", help="save still frames from a job's video, for calibrating screen regions")
    p.add_argument("job")
    p.add_argument("--at", required=True, help="comma-separated times, e.g. 600,0:15:00")
    p.set_defaults(fn=cmd_frames)

    p = sub.add_parser("find", help="search YouTube without downloading")
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=10)
    p.set_defaults(fn=cmd_find)

    p = sub.add_parser("eval", help="score a job's clips against hand-labelled moments")
    p.add_argument("job")
    p.add_argument("labels")
    p.set_defaults(fn=cmd_eval)

    args = parser.parse_args(argv)
    try:
        args.fn(args, Settings.from_env())
    except KeyboardInterrupt:
        log("stopped; run the same command again to continue")
        sys.exit(130)


if __name__ == "__main__":
    main()
