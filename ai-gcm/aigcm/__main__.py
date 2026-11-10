"""Command line: run a job, check its status, grab frames for calibration, search YouTube, score results."""

import argparse
import csv
from dataclasses import replace
import re
import shutil
import sys
import time
from pathlib import Path

from . import audio, captions, judge, markers, moments, package, render, review, sounds, talk, transcript, vision
from .config import Settings
from .jobs import STAGES, Job, log, read_json, stages_from, write_json
from .media import download, extract_audio, extract_frame, is_url, parse_time, probe, search
from .procs import Busy, FolderLock

# Folders and files each stage writes, removed when that stage is forced to run again.
OUTPUTS = {
    "ingest": ["source.mp4", "audio.wav", "info.json"],
    "vision": ["vision.json", "vision.partial.json"],
    "audio": ["audio.npz"],
    "sounds": ["sounds.npz"],
    "transcript": ["transcript.json", "transcript.partial.json"],
    "moments": ["moments.json", "talk.json"],
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
    # Keep or reject decisions belong to the clips they were made on. Clip ids are reused when moments run
    # again, so move the decisions aside with the clip list they refer to; they are labelled data.
    decisions = job.path("decisions.json")
    if STAGES.index(stage) <= STAGES.index("moments") and decisions.exists():
        archive = job.path("history", time.strftime("%Y%m%d-%H%M%S"))
        archive.mkdir(parents=True)
        shutil.move(str(decisions), archive / "decisions.json")
        if job.path("ranked.json").exists():
            shutil.copyfile(job.path("ranked.json"), archive / "ranked.json")
        log(f"earlier keep/reject decisions moved to {archive}")
    for name in stages_from(stage):
        for item in OUTPUTS[name]:
            path = job.path(item)
            if path.is_dir():
                shutil.rmtree(path)
            elif path.exists():
                path.unlink()
    job.invalidate_from(stage)


def local_source(source, job):
    """The job's copy of a local video. An upload is written straight into the job folder (M2 review R6),
    so it is used where it is; copying an 8 GB recording would double the disk it takes."""
    source = Path(source)
    if source.parent.resolve() == job.root.resolve() and source.stem == "source":
        return source
    path = job.path("source" + source.suffix.lower())
    shutil.copyfile(source, path)
    return path


def pipeline(job, source, section, settings, use_judge, use_captions, until=None):
    def ingest(job):
        info = {"source": source}
        if is_url(source):
            path, meta = download(source, job.root, settings.download_height, section)
            info.update(meta)
        else:
            path = local_source(source, job)
            info["title"] = Path(source).stem
        info.update(probe(path), path=str(path), section=section)
        extract_audio(path, job.path("audio.wav"))
        write_json(job.path("info.json"), info)

    def audio_stage(job):
        audio.save(job.path("audio.npz"), audio.analyse(job.path("audio.wav"), settings.audio_hop_s))

    def sounds_stage(job):
        sounds.save(job.path("sounds.npz"), sounds.analyse(job.path("audio.wav")))

    def transcript_stage(job):
        heard_path = job.path("sounds.npz")
        heard = sounds.load(heard_path) if heard_path.exists() else None
        said = transcript.transcribe(job.path("audio.wav"), settings, job.path("transcript.partial.json"), heard)
        # A noisy stream can defeat the small Hinglish model (ANJI: speech half the time, 309 words). The
        # coverage is recorded here; the chosen clips are redone with the bigger model in the judge stage,
        # because that model is too slow for a whole stream.
        if heard is not None:
            said["coverage"] = transcript.coverage(said, heard)
            said["broken"] = transcript.looks_broken(said, heard)
            if said["broken"]:
                log(f"transcript: covers only {said['coverage']:.0%} of the detected speech; clips will be redone "
                    f"with the bigger model if one is installed")
        write_json(job.path("transcript.json"), said)

    def vision_stage(job):
        info = read_json(job.path("info.json"))
        write_json(job.path("vision.json"), vision.scan(info["path"], info, settings, job.path("vision.partial.json")))

    def moments_stage(job):
        info = read_json(job.path("info.json"))
        seen = read_json(job.path("vision.json"))
        events = seen["events"]
        heard, said = sounds.load(job.path("sounds.npz")), read_json(job.path("transcript.json"))
        loudness = audio.load(job.path("audio.npz"))
        talks = talk.find(job, said, heard, loudness, settings, info["duration"])
        marks = markers.merge(markers.load(job), markers.from_transcript(said))
        found = moments.build(events, loudness, settings, info["duration"], seen.get("remaining", []), heard, talks,
                              marks)
        write_json(job.path("moments.json"), found)
        log(f"moments: {len(found)} candidates from {len(events)} HUD events, {len(marks)} markers")

    def judge_stage(job):
        info = read_json(job.path("info.json"))
        found = read_json(job.path("moments.json"))
        if use_judge and settings.gemini_api_key:
            judge.judge_all(job, info["path"], found, settings, read_json(job.path("transcript.json")))
        elif use_judge:
            log("judge: no GEMINI_API_KEY in .env, ranking with the detector score only")
        ranked = judge.merge(job, found, settings)[: settings.top_n]
        for n, clip in enumerate(ranked, 1):
            clip["rank"] = n
        said = read_json(job.path("transcript.json"))
        # The whole-stream transcript is the fast batched one; the chosen clips get the fuller plain read
        # (and a bigger model, if one is installed, when the transcript looks broken).
        windows = [(c["start"], c["end"]) for c in ranked]
        if windows and said.get("windows") != [[round(s, 2), round(e, 2)] for s, e in windows]:
            bigger = transcript.fallback_model(settings) if said.get("broken") else None
            said = transcript.retranscribe_windows(job.path("audio.wav"), windows,
                                                   replace(settings, whisper_model=bigger) if bigger else settings, said)
            write_json(job.path("transcript.json"), said)
        package.decorate(ranked, info, said, settings)
        flagged = sum(1 for c in ranked if c["flags"])
        log(f"judge: {len(ranked)} clips packaged with titles; {flagged} carry safety flags")
        write_json(job.path("ranked.json"), ranked)

    def captions_stage(job):
        if not use_captions:
            log("captions: skipped")
            return
        info = read_json(job.path("info.json"))
        layout = render.resolve_layout(settings.layout, info)
        captions.caption_clips(job, read_json(job.path("ranked.json")), read_json(job.path("transcript.json")),
                               render.CAPTION_MARGIN.get(layout, 380))

    def render_stage(job):
        """Each clip is cut by the studio renderer from its default edit (M3 review S-R8): the swipe video
        is already the Short the creator would post (layout, camera, zoom on kills, hook, captions), and
        the studio and the engine can't drift apart."""
        from .studio import facecam, hook
        from .studio import render as studio_render
        from .studio.edit import default_edit, is_talk, template_layout

        info = read_json(job.path("info.json"))
        ranked = read_json(job.path("ranked.json"))
        out_dir = job.path("clips")
        out_dir.mkdir(exist_ok=True)
        done = read_json(job.path("clips.json"), {})
        said = read_json(job.path("transcript.json")) if use_captions else None
        cam = list(settings.facecam) if settings.facecam else (facecam.for_stream(job.root, info["path"]) or {}).get("box")
        for clip in ranked:
            if clip["id"] in done and (out_dir / done[clip["id"]]).exists():
                continue
            edit = default_edit(clip["start"], clip["end"], info["width"], info["height"], clip.get("title"),
                                clip.get("events") or (), captions=bool(said) and is_talk(clip.get("type"), clip.get("labels")),
                                facecam=cam)
            if settings.layout in ("blur", "split", "native"):
                edit = edit.model_copy(update={"layout": template_layout(settings.layout, info["width"], info["height"], cam)})
            picture = hook.for_edit(job.path("studio", "hooks"), edit)
            name = f"{clip['rank']:02d}_{clip['type']}_{clip['id']}.mp4"
            studio_render.render(edit, info["path"], 0.0, info.get("has_audio", True), out_dir / name, transcript=said,
                                 threads=8, hook_png=picture)
            done[clip["id"]] = name
            if settings.sponsor_safe and clip.get("mute_spans"):
                safe = f"{clip['rank']:02d}_{clip['type']}_{clip['id']}_safe.mp4"
                studio_render.render(edit, info["path"], 0.0, info.get("has_audio", True), out_dir / safe,
                                     transcript=said, threads=8, hook_png=picture,
                                     mute_spans=studio_render.output_mute(edit, clip["start"], clip["mute_spans"]))
                done[clip["id"] + "_safe"] = safe
            write_json(job.path("clips.json"), done)

    def review_stage(job):
        info = read_json(job.path("info.json"))
        files = read_json(job.path("clips.json"), {})
        ranked = [dict(c, file=files[c["id"]]) for c in read_json(job.path("ranked.json")) if c["id"] in files]
        job.path("review.html").write_text(review.build(job.root.name, info, ranked), encoding="utf-8")
        log(f"review: open {job.path('review.html')}")

    stages = {"ingest": ingest, "audio": audio_stage, "sounds": sounds_stage, "transcript": transcript_stage,
              "vision": vision_stage, "moments": moments_stage,
              "judge": judge_stage, "captions": captions_stage, "render": render_stage, "review": review_stage}
    # Vision (frames, OCR) runs alongside the audio stages (wav, YAMNet, Whisper); the rest is sequential.
    side_by_side = ["vision", "audio", "sounds", "transcript"]
    name_iter = iter(STAGES)
    for name in name_iter:
        if name == "vision":
            analysis = [s for s in side_by_side if not job.done(s)]
            if analysis:
                log(f"running side by side: {', '.join(analysis)}")
                job.run_parallel([[(s, stages[s])] for s in analysis if s == "vision"]
                                 + [[(s, stages[s]) for s in analysis if s != "vision"]])
            for s in side_by_side[1:]:
                next(name_iter)
            if until in side_by_side:
                log(f"stopped after {until}; run again without --until to continue")
                break
            continue
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
    settings.sponsor_safe = bool(getattr(args, "sponsor_safe", False))
    if getattr(args, "game", None):
        settings.game = args.game
    job = Job(settings.jobs_dir / (args.job or job_name(args.source, section)))
    saved = read_json(job.path("settings.json"))
    if saved:
        # A resumed job keeps its time range too; the downloaded video only covers that range.
        section = section or (tuple(saved["section"]) if saved.get("section") else None)
        # A resumed job keeps the layout it started with unless the command line changes it.
        settings.layout = args.layout or ("split" if args.facecam else saved.get("layout", settings.layout))
        settings.facecam = settings.facecam or (tuple(saved["facecam"]) if saved.get("facecam") else None)
    write_json(job.path("settings.json"), {"source": args.source, "section": section, "layout": settings.layout,
                                          "facecam": settings.facecam, "top_n": settings.top_n})
    if args.force:
        clear_from(job, args.force)
    log(f"job folder: {job.root}")
    try:
        with FolderLock(job.root):
            pipeline(job, args.source, section, settings, not args.no_judge, not args.no_captions, args.until)
    except Busy as exc:
        log(f"refused: {exc}")
        sys.exit(3)


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


def stale_sources(jobs_dir, keep_days, now=None):
    """Source video and audio files of finished jobs whose clips were made more than keep_days ago. Clips,
    transcripts and analysis stay; only the large inputs go (re-editing needs the source, hence the wait)."""
    now = now or time.time()
    found = []
    for root in sorted(p for p in Path(jobs_dir).iterdir() if p.is_dir()):
        job = Job(root)
        clips = job.path("clips.json")
        if not job.done("render") or not clips.exists() or now - clips.stat().st_mtime < keep_days * 86400:
            continue
        found += [p for p in root.iterdir() if p.is_file() and (p.name.startswith("source.") or p.name == "audio.wav")]
    return found


def cmd_cleanup(args, settings):
    days = args.days if args.days is not None else settings.source_keep_days
    files = stale_sources(settings.jobs_dir, days)
    size = sum(p.stat().st_size for p in files) / 1e9
    for p in files:
        print(f"{'would delete' if args.dry_run else 'deleting'} {p}")
        if not args.dry_run:
            p.unlink()
    print(f"{len(files)} files, {size:.1f} GB{' (dry run)' if args.dry_run else ' freed'}")


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


def cmd_serve(args, settings):
    """The old stdlib app was retired on 7 Nov 2026 (M2.9); `serve` now starts the platform API and web app.
    The worker runs separately: python -m aigcm.worker (or double-click Start Kaatclip.cmd for both)."""
    from .api.__main__ import main as api_main

    log("serve: starting the Kaatclip API and web app; start the worker too (python -m aigcm.worker)")
    api_main(["--host", args.host, "--port", str(args.port)])


def main(argv=None):
    parser = argparse.ArgumentParser(prog="aigcm", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("run", help="process a YouTube URL or a local video")
    p.add_argument("source")
    p.add_argument("--section", help="only this part of a YouTube video, e.g. 0:30:00-1:30:00")
    p.add_argument("--job", help="job folder name (default: from the video id or file name)")
    p.add_argument("--top", type=int, help="number of clips to make (default 12)")
    p.add_argument("--layout", choices=["auto", "blur", "split", "native"])
    p.add_argument("--facecam", help="facecam box as x,y,w,h fractions of the frame; implies --layout split")
    p.add_argument("--force", choices=STAGES, help="rerun this stage and everything after it")
    p.add_argument("--until", choices=STAGES, help="stop after this stage")
    p.add_argument("--no-judge", action="store_true", help="skip Gemini even if a key is set")
    p.add_argument("--no-captions", action="store_true")
    p.add_argument("--sponsor-safe", action="store_true", help="also render a bleeped copy of clips with gaali")
    p.add_argument("--game", choices=["bgmi"], help="which game's HUD to read (default bgmi)")
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

    p = sub.add_parser("cleanup", help="delete source videos of finished jobs to free disk space")
    p.add_argument("--days", type=int, help="keep sources this many days after clips are made (default 14)")
    p.add_argument("--dry-run", action="store_true", help="only list what would be deleted")
    p.set_defaults(fn=cmd_cleanup)

    p = sub.add_parser("serve", help="run the Kaatclip API and web app (same as python -m aigcm.api)")
    p.add_argument("--host", default="127.0.0.1", help="127.0.0.1: this laptop and the Tailscale Funnel address")
    p.add_argument("--port", type=int, default=8770)
    p.set_defaults(fn=cmd_serve)

    args = parser.parse_args(argv)
    # Stream titles carry emoji; the Windows console's default code page can't print them.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    try:
        args.fn(args, Settings.from_env())
    except KeyboardInterrupt:
        log("stopped; run the same command again to continue")
        sys.exit(130)


if __name__ == "__main__":
    main()
