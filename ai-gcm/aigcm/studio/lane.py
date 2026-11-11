"""The worker's render lane: runs studio work (working windows, exports) beside stream jobs, so an export
never waits an hour behind a stream (M3 review S-R7).

Each render is planned in a short database transaction that reads everything it needs, run with no
transaction open (ffmpeg takes seconds to minutes, and an open write transaction would block the API;
the M2 lesson), then recorded in a second short transaction."""

import shutil
from pathlib import Path

from sqlalchemy import select

from ..db.models import Clip, Render, Stream, utcnow
from ..jobs import log, read_json, write_json
from . import project
from . import window as win
from .edit import EditData, check_window

EXPORTS = "exports"


def export_name(clip_key, version, render_id, safe):
    return f"{clip_key}_v{version}{'_safe' if safe else ''}_{render_id}.mp4"


def plan_prepare(settings, session, render):
    clip = session.get(Clip, render.clip_id)
    folder = project.job_folder(settings, clip)
    target = project.clip_folder(settings, clip)
    start_s, end_s = clip.start_s, clip.end_s

    def task(threads):
        source = project.source_file(folder)
        if source is None:
            raise RuntimeError("The recording is no longer on the laptop, so this clip can't be edited.")
        if shutil.disk_usage(settings.jobs_dir).free < settings.min_free_bytes:
            raise RuntimeError("The laptop is low on disk space; free some up and try again.")
        from ..media import probe

        duration = probe(source)["duration"]
        events = (read_json(folder / "vision.json", {}) or {}).get("events") or []
        start, end = win.plan_window(start_s, end_s, duration, events)
        win.prepare(source, target, start, end, threads=threads)
        from . import facecam

        facecam.for_stream(folder, source)   # once per stream, about 4 s
        return None
    return task


def cover_path(video):
    return Path(video).with_suffix(".jpg")


VIEW_W = 720
VIEW_CRF, VIEW_MAX = 26, "2M"


def view_path(video):
    """The light copy played in the app: 720 px wide, about 1.5-2 Mbps (the full clip is 1080p at 5-6 Mbps,
    too much for the phone's link through the relay). Downloads, shares and YouTube posts use the full file."""
    video = Path(video)
    return video.with_name(f"{video.stem}.view.mp4")


def make_view(video, threads=2):
    from ..media import run, tool

    out = view_path(video)
    partial = out.with_name(f"{video.stem}.view.part.mp4")
    try:
        run([tool("ffmpeg"), "-v", "error", "-y", "-i", str(video), "-vf", f"scale={VIEW_W}:-2", "-c:v", "libx264",
             "-preset", "veryfast", "-crf", str(VIEW_CRF), "-maxrate", VIEW_MAX, "-bufsize", "4M", "-pix_fmt", "yuv420p",
             "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", "-threads", str(threads), str(partial)])
        partial.replace(out)
        return out
    except RuntimeError as exc:   # one broken video must not stop the others
        log(f"studio: no light copy of {Path(video).name}: {exc}")
        partial.unlink(missing_ok=True)
        return None


def save_cover(video, at):
    """The Short's cover image: a full-size frame of the exported video (hook, captions and all), next to it."""
    from ..media import run, tool

    run([tool("ffmpeg"), "-v", "error", "-y", "-ss", f"{at:.3f}", "-i", str(video), "-frames:v", "1", "-q:v", "2",
         str(cover_path(video))])


def _hook(edit, folder):
    from . import hook

    return hook.for_edit(folder, edit)


def plan_export(settings, session, render):
    clip = session.get(Clip, render.clip_id)
    target = project.clip_folder(settings, clip)
    details = win.ready(target)
    if not details:
        raise RuntimeError("This clip's footage isn't ready for editing yet.")
    version = render.params.get("version") or 0
    if version:
        saved = next((e for e in clip.edits if e.version == version), None)
        if saved is None:
            raise RuntimeError(f"Version {version} of this edit no longer exists.")
        edit = EditData.model_validate(saved.data)
    else:
        edit = project.default_for(settings, clip, details)
    check_window(edit, details["start"], details["end"])
    folder = project.job_folder(settings, clip)
    safe = bool(render.params.get("sponsor_safe") or edit.sponsor_safe)
    spans = (clip.details or {}).get("mute_spans") if safe else None
    name = export_name(clip.clip_key, version, render.id, safe)
    clip_start = clip.start_s
    hooks_folder = target / "hooks"   # worked out now: the task runs after this session has closed
    from . import brand
    from .edit import MAX_LENGTH_S, cover_time, output_length

    owner = clip.stream.user_id
    kit = project.kit_for(clip)
    found = brand.files(settings.jobs_dir, owner)
    intro = found["intro"] if edit.intro else None
    outro = found["outro"] if edit.outro else None
    total = output_length(edit.segments) + (found["intro_s"] if intro else 0) + (found["outro_s"] if outro else 0)
    if total > MAX_LENGTH_S + 0.01:
        raise RuntimeError(f"With the intro and outro the Short would be {total:.0f} s; Shorts can be at most 3 minutes.")

    def task(threads):
        from .render import output_mute, render as render_edit

        transcript = read_json(folder / "transcript.json") if edit.captions.on else None
        out_dir = folder / EXPORTS
        out_dir.mkdir(exist_ok=True)
        render_edit(edit, target / "window.mkv", details["start"], details["has_audio"], out_dir / name,
                    transcript=transcript, mute_spans=output_mute(edit, clip_start, spans), threads=threads,
                    hook_png=_hook(edit, hooks_folder),
                    strip_png=brand.strip_for(settings.jobs_dir, owner, kit) if edit.lower_third else None,
                    intro=intro, outro=outro)
        save_cover(out_dir / name, cover_time(edit, found["intro_s"] if intro else 0.0))
        make_view(out_dir / name, threads)
        return name
    return task


def plan_posters(settings, session, render):
    stream = session.get(Stream, (render.params or {}).get("stream_id"))
    if stream is None:
        raise RuntimeError("That stream no longer exists.")
    folder = Path(settings.jobs_dir) / stream.job_dir
    todo = [(folder / "clips" / Path(c.file_name).name, project.poster_path(settings, c), project.poster_time(c))
            for c in stream.clips if not project.poster_path(settings, c).exists()]
    # The light copies played in the app, for clips and finished exports that have none yet.
    videos = [folder / "clips" / Path(c.file_name).name for c in stream.clips]
    clip_ids = [c.id for c in stream.clips]
    if clip_ids:
        for done in session.scalars(select(Render).where(Render.clip_id.in_(clip_ids), Render.kind == "export",
                                                         Render.status == "done")).all():
            if done.output:
                videos.append(folder / EXPORTS / Path(done.output).name)
    light = [v for v in videos if v.exists() and not view_path(v).exists()]

    def task(threads):
        from ..media import run, tool

        made = 0
        for video, poster, at in todo:
            if not video.exists():
                continue
            poster.parent.mkdir(exist_ok=True)
            partial = poster.with_suffix(".part.jpg")
            try:
                run([tool("ffmpeg"), "-v", "error", "-y", "-ss", f"{at:.2f}", "-i", str(video), "-frames:v", "1",
                     "-vf", f"scale={project.POSTER_W}:-2", "-q:v", "6", "-threads", str(threads), str(partial)])
                partial.replace(poster)
                made += 1
            except RuntimeError as exc:   # one broken clip must not stop the others
                log(f"studio: no poster for {video.name}: {exc}")
                partial.unlink(missing_ok=True)
        log(f"studio: {made} posters for {folder.name}")
        views = sum(make_view(v, threads) is not None for v in light if v.exists())
        if views:
            log(f"studio: {views} light copies for {folder.name}")
        return None
    return task


REACTION_S = 4.0    # the streamer's reaction is the loudest moment this soon after a kill


def stream_moments(folder, clips, windows):
    """Kill and reaction moments of a stream's best clips, each located in a file that still has it: the
    source if it's on the laptop, else a kept clip's working window. Returns (moments, kills, dinners)."""
    import numpy as np

    from .thumbs import Moment

    source = project.source_file(folder)
    events = (read_json(folder / "vision.json", {}) or {}).get("events") or []
    kills_all = [e["t"] for e in events if e.get("kind") == "self_kill"]
    dinners = sum(1 for e in events if e.get("kind") == "dinner")   # the HUD scan's name for a chicken dinner

    def locate(t):
        if source is not None:
            return source, t
        for path, (a, b) in windows.items():
            if a <= t <= b:
                return path, t - a
        return None

    loud = None
    if (folder / "audio.npz").exists():
        data = np.load(folder / "audio.npz")
        loud = (data["t"], data["excitement"])
    moments = []
    for clip in sorted(clips, key=lambda c: c.rank):
        for t in [k for k in kills_all if clip.start_s <= k <= clip.end_s]:
            spot = locate(t + 0.3)
            if spot:
                moments.append(Moment(spot[0], spot[1], "kill", score=(clip.score or 0) - clip.rank))
            if loud is not None:
                times, excitement = loud
                near = (times > t) & (times <= t + REACTION_S)
                if near.any():
                    i = int(np.argmax(np.where(near, excitement, -1e9)))
                    spot = locate(float(times[i]))
                    if spot:
                        moments.append(Moment(spot[0], spot[1], "reaction", score=float(excitement[i])))
    if not any(m.kind == "kill" for m in moments):   # talk streams: the clips' key moments instead
        for clip in sorted(clips, key=lambda c: c.rank)[:6]:
            at = (clip.details or {}).get("anchor") or (clip.start_s + clip.end_s) / 2
            spot = locate(at)
            if spot:
                moments.append(Moment(spot[0], spot[1], "kill", score=-clip.rank))
    return moments, len(kills_all), dinners


def plan_thumbs(settings, session, render):
    from .. import titles
    from . import facecam
    from .thumbs import make_set

    stream = session.get(Stream, (render.params or {}).get("stream_id"))
    if stream is None:
        raise RuntimeError("That stream no longer exists.")
    folder = Path(settings.jobs_dir) / stream.job_dir
    clips = list(stream.clips)
    windows = {}
    for clip in clips:
        details = win.ready(project.clip_folder(settings, clip))
        if details:
            windows[project.clip_folder(settings, clip) / "window.mkv"] = (details["start"], details["end"])
    moments, kills, dinners = stream_moments(folder, clips, windows)
    if not moments:
        raise RuntimeError("The stream's recording is no longer on the laptop and no kept clip has footage saved.")
    talk = next((c.title for c in sorted(clips, key=lambda c: c.rank)
                 if c.title and (c.type in ("funny", "banter", "rage", "hype", "story", "talk", "reaction"))), None)
    texts = titles.thumb_words(kills, dinners, [c.type for c in sorted(clips, key=lambda c: c.rank)])
    names = titles.long_titles(kills, dinners, titles.stream_context(stream.title), talk, stream.game or "bgmi")
    cam = (facecam.for_stream(folder) or {}).get("box")
    out_dir = folder / "thumbs" / render.id

    def task(threads):
        from ..jobs import write_json

        make_set(moments, cam, texts, out_dir)
        write_json(out_dir / "titles.json", {"titles": names, "words": texts})
        return render.id
    return task


COMPILATIONS = "_compilations"


def compilation_folder(jobs_dir, user_id, render_id):
    return Path(jobs_dir) / COMPILATIONS / str(int(user_id)) / Path(render_id).name


def plan_compilation(settings, session, render):
    """A weekly compilation from the creator's chosen clips, in their order: the video, three thumbnails, three
    titles and a description with chapters (M3.8)."""
    from .. import titles
    from . import brand, compile, facecam, hook
    from .thumbs import Moment, make_set

    params = render.params or {}
    short = params.get("format") == "short"
    clips = {c.id: c for c in session.query(Clip).filter(Clip.id.in_(params.get("clip_ids") or [])).all()
             if c.stream.user_id == render.user_id}
    pieces, edits, cams, events_by_job = [], {}, {}, {}
    for clip_id in params.get("clip_ids") or []:
        clip = clips.get(clip_id)
        piece = compile.piece_for(settings, clip, short) if clip else None
        if piece is None:
            continue
        pieces.append(piece)
        folder = project.job_folder(settings, clip)
        events_by_job[piece.job_dir] = (read_json(folder / "vision.json", {}) or {}).get("events") or []
        cams[piece.job_dir] = (facecam.for_stream(folder) or {}).get("box")
        if short:
            edit = project.default_for(settings, clip)
            edits[clip.id] = (edit, None if not edit.hook.on else (folder, edit))
    if len(pieces) < 2:
        raise RuntimeError("At least two of the chosen clips need footage on the laptop.")
    out_dir = compilation_folder(settings.jobs_dir, render.user_id, render.id)
    kills = sum(p.kills for p in pieces)
    dinners = sum(1 for p in pieces for e in events_by_job[p.job_dir]
                  if e.get("kind") == "dinner" and p.start <= e["t"] <= p.end)
    talk = next((clips[p.clip_id].title for p in pieces if p.talk and clips[p.clip_id].title), None)   # a real title only
    names = titles.long_titles(kills, dinners, "BEST OF THE WEEK", talk)
    words = titles.thumb_words(kills, dinners, [clips[p.clip_id].type for p in pieces])
    chapter_lines = compile.chapters(pieces)
    kit = project.kit_for(next(iter(clips.values())))
    engine_text = "Chapters:\n" + "\n".join(chapter_lines) + "\n\n" + titles.KRAFTON_LINE
    post = brand.post_text(names[0], engine_text, ["#bgmi"], kit)
    best = next((p for p in reversed(pieces) if not p.talk), pieces[0])
    moments = []
    for p in pieces:
        for e in events_by_job[p.job_dir]:
            if e.get("kind") == "self_kill" and p.start <= e["t"] <= p.end:
                moments.append(Moment(Path(p.video), e["t"] + 0.3 - p.offset, "kill", score=p.kills))
                moments.append(Moment(Path(p.video), min(p.end, e["t"] + 2.0) - p.offset, "reaction", score=p.kills))
    if not moments:
        moments = [Moment(Path(p.video), (p.start + p.end) / 2 - p.offset, "kill") for p in pieces]
    transcripts = {p.job_dir: read_json(Path(settings.jobs_dir) / p.job_dir / "transcript.json") for p in pieces}

    def task(threads):
        out_dir.mkdir(parents=True, exist_ok=True)
        if short:
            ready = {}
            for clip_id, (edit, hook_job) in edits.items():
                picture = hook.for_edit(out_dir / "hooks", edit) if hook_job else None
                ready[clip_id] = (edit, picture)
            compile.render_short(pieces, out_dir, ready, transcripts, threads)
        else:
            compile.render_wide(pieces, out_dir, transcripts, threads)
        make_set(moments, cams.get(best.job_dir), words, out_dir)
        compile.save_plan(out_dir, pieces, "short" if short else "wide", names, chapter_lines)
        write_json(out_dir / "post.json", post)
        return render.id
    return task


PLANNERS = {"prepare": plan_prepare, "export": plan_export, "posters": plan_posters, "thumbs": plan_thumbs,
            "compilation": plan_compilation}


def run(settings, sessions, render_id, threads):
    """Run one claimed render and record how it ended. Never raises: a failed render is recorded."""
    task, error, output = None, None, None
    with sessions() as s:
        render = s.get(Render, render_id)
        kind = render.kind
        try:
            task = PLANNERS[kind](settings, s, render)
        except Exception as exc:
            error = exc
        s.commit()   # ends the read transaction before any slow work
    if task is not None:
        try:
            output = task(threads)
        except Exception as exc:
            error = exc
    with sessions() as s:
        render = s.get(Render, render_id)
        if error is None:
            render.status, render.output, render.error = "done", output, None
        else:
            log(f"studio: {kind} {render_id} failed: {error!r}")
            render.status, render.error = "failed", str(error)[:500]
        render.finished_at = utcnow()
        s.commit()
        return render.status


def export_path(settings, clip, render):
    if not render.output:
        return None
    folder = (project.job_folder(settings, clip) / EXPORTS).resolve()
    path = (folder / Path(render.output).name).resolve()
    return path if path.parent == folder and path.is_file() else None
