"""The worker's render lane: runs studio work (working windows, exports) beside stream jobs, so an export
never waits an hour behind a stream (M3 review S-R7).

Each render is planned in a short database transaction that reads everything it needs, run with no
transaction open (ffmpeg takes seconds to minutes, and an open write transaction would block the API;
the M2 lesson), then recorded in a second short transaction."""

import shutil
from pathlib import Path

from ..db.models import Clip, Render, Stream, utcnow
from ..jobs import log, read_json
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
    from .edit import MAX_LENGTH_S, output_length

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
        return name
    return task


def plan_posters(settings, session, render):
    stream = session.get(Stream, (render.params or {}).get("stream_id"))
    if stream is None:
        raise RuntimeError("That stream no longer exists.")
    folder = Path(settings.jobs_dir) / stream.job_dir
    todo = [(folder / "clips" / Path(c.file_name).name, project.poster_path(settings, c), project.poster_time(c))
            for c in stream.clips if not project.poster_path(settings, c).exists()]

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
        return None
    return task


PLANNERS = {"prepare": plan_prepare, "export": plan_export, "posters": plan_posters}


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
