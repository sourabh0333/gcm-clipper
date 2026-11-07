"""The worker: takes queued streams from the database one at a time and runs the engine on them.

    python -m aigcm.worker

The engine runs as a child process (`python -m aigcm run <source> --job <folder>`) writing to the job's
run.log, so a crash in a 3-hour job can't take the worker down and Stop can kill the whole process tree.
A stream left "running" by a crash, power cut or restart goes back to the queue at start, and the engine
resumes it from its checkpoints. When a job finishes, its clips are copied into the clips table once.
See plans/M2 platform core plan.md (M2.4, R10, R11)."""

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

from sqlalchemy import DateTime, bindparam, select, text

from . import db as database
from .config import ROOT
from .db.models import AuditEntry, Clip, Stream, WorkerState, utcnow
from .jobs import log
from .jobview import failure, finished_clips
from .procs import pid_alive

POLL_S = 3.0           # how often an idle worker looks for work
WATCH_S = 1.0          # how often a running job is checked for a Stop request
HOUSEKEEPING_S = 3600  # how often stale uploads are cleared
HEARTBEAT_S = 10.0
STALE_S = 45.0         # a heartbeat older than this means that worker is gone


def claim_next(session):
    """Atomically take the oldest queued stream: one statement, so two workers can never take the same one."""
    claim = text(
        "UPDATE streams SET status='running', started_at=:now, error=NULL, stop_requested=0 "
        "WHERE id=(SELECT id FROM streams WHERE status='queued' ORDER BY queued_at, created_at LIMIT 1) "
        "AND status='queued' RETURNING id").bindparams(bindparam("now", type_=DateTime))
    row = session.execute(claim, {"now": utcnow()}).first()
    session.commit()
    return row[0] if row else None


def requeue_interrupted(session):
    """Streams a crashed or stopped worker left running go back to the queue (they resume from checkpoints)."""
    stuck = session.scalars(select(Stream).where(Stream.status == "running")).all()
    for stream in stuck:
        stream.status, stream.queued_at = "queued", stream.queued_at or utcnow()
    session.commit()
    return [s.id for s in stuck]


def import_clips(session, stream, folder):
    """Copy the job's clips into the clips table. A clip that is unchanged from an earlier import (same id
    and same cut) keeps its keep or reject decision."""
    old = {c.clip_key: c for c in stream.clips}
    stream.clips.clear()
    session.flush()
    for item in finished_clips(folder):
        clip = Clip(stream_id=stream.id, **item)
        before = old.get(item["clip_key"])
        if before and before.start_s == clip.start_s and before.end_s == clip.end_s:
            clip.decision, clip.decision_reason, clip.decided_at = before.decision, before.decision_reason, before.decided_at
        stream.clips.append(clip)
    session.flush()
    return len(stream.clips)


def source_file(folder):
    found = sorted(Path(folder).glob("source.*"))
    return found[0] if found else None


def engine_command(stream, folder):
    return [sys.executable, "-m", "aigcm", "run", str(source_file(folder)), "--job", folder.name, "--game", stream.game]


def kill_tree(proc):
    if proc.poll() is not None:
        return
    if os.name == "nt":
        # terminate() would leave the engine's ffmpeg children running on Windows.
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)], capture_output=True)
    else:
        proc.terminate()
    try:
        proc.wait(timeout=30)
    except subprocess.TimeoutExpired:
        proc.kill()


class Worker:
    def __init__(self, settings, command=engine_command, notify=()):
        self.settings = settings
        self.engine = database.make_engine(settings.db_url)
        database.migrate(self.engine)
        self.sessions = database.session_factory(self.engine)
        self.command = command
        self.notify = list(notify)   # callables (stream, event) -> None; Telegram joins in M2.7
        self.last_beat = self.last_housekeeping = 0.0

    def heartbeat(self, stream_id=None, force=False):
        if not force and time.time() - self.last_beat < HEARTBEAT_S:
            return
        with self.sessions() as s:
            state = s.get(WorkerState, 1) or WorkerState(id=1)
            state.heartbeat_at, state.stream_id, state.pid = utcnow(), stream_id, os.getpid()
            s.merge(state)
            s.commit()
        self.last_beat = time.time()

    def housekeeping(self):
        if time.time() - self.last_housekeeping < HOUSEKEEPING_S:
            return
        from .api.uploads import expire_uploads

        with self.sessions() as s:
            removed = expire_uploads(s, self.settings)
        if removed:
            log(f"worker: removed {len(removed)} unfinished uploads untouched for days")
        self.last_housekeeping = time.time()

    def other_worker(self):
        """The pid of another worker that is alive and beating, or None. Only one worker may run: a second
        one would take over streams the first is still processing (M2.4 check, 7 Nov)."""
        with self.sessions() as s:
            state = s.get(WorkerState, 1)
        if state is None or not state.heartbeat_at or state.pid in (None, os.getpid()):
            return None
        fresh = (utcnow() - state.heartbeat_at).total_seconds() < STALE_S
        return state.pid if fresh and pid_alive(state.pid) else None

    def start(self, timeout=None):
        """Wait until no other worker is alive (or raise after `timeout` seconds), then re-queue the streams
        a dead worker left running."""
        waited, told = 0.0, False
        while (other := self.other_worker()) is not None:
            if timeout is not None and waited >= timeout:
                raise RuntimeError(f"Another worker is running (process {other}).")
            if not told:
                log(f"worker: another worker is running (process {other}); waiting for it to stop")
                told = True
            time.sleep(POLL_S)
            waited += POLL_S
        with self.sessions() as s:
            requeued = requeue_interrupted(s)
        if requeued:
            log(f"worker: back in the queue after a restart: {', '.join(requeued)}")
        self.heartbeat(force=True)

    def step(self):
        """Run at most one job. Returns the stream id it ran, or None if the queue was empty."""
        self.heartbeat()
        self.housekeeping()
        with self.sessions() as s:
            stream_id = claim_next(s)
        if stream_id:
            self.run(stream_id)
        return stream_id

    def run(self, stream_id):
        with self.sessions() as s:
            stream = s.get(Stream, stream_id)
            folder = self.settings.jobs_dir / stream.job_dir
            if source_file(folder) is None:
                stream.status, stream.error = "failed", "The recording is missing from the laptop."
                s.commit()
                return
            cmd = self.command(stream, folder)
        log(f"worker: starting {stream_id}")
        self.heartbeat(stream_id, force=True)
        env = dict(os.environ, AIGCM_JOBS_DIR=str(self.settings.jobs_dir.resolve()), PYTHONIOENCODING="utf-8")
        with open(folder / "run.log", "a", encoding="utf-8") as out:
            out.write(f"\n--- started by the worker at {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n")
            out.flush()
            proc = subprocess.Popen(cmd, cwd=ROOT, stdout=out, stderr=subprocess.STDOUT, env=env)
        stopped = False
        while proc.poll() is None:
            time.sleep(WATCH_S)
            self.heartbeat(stream_id)
            with self.sessions() as s:
                if s.get(Stream, stream_id).stop_requested:
                    kill_tree(proc)
                    stopped = True
        self.finish(stream_id, folder, proc.returncode, stopped)

    def finish(self, stream_id, folder, returncode, stopped):
        with self.sessions() as s:
            stream = s.get(Stream, stream_id)
            if stopped:
                stream.status, stream.stop_requested = "stopped", False
                event = "stopped"
            elif returncode == 0:
                count = import_clips(s, stream, folder)
                stream.status, stream.error = "done", None
                event = "done"
                log(f"worker: {stream_id} done, {count} clips")
            else:
                stream.status, stream.error = "failed", failure(folder)
                event = "failed"
                log(f"worker: {stream_id} failed: {stream.error}")
            stream.finished_at = utcnow()
            s.add(AuditEntry(user_id=stream.user_id, action=f"job_{event}", detail={"stream": stream_id}))
            s.commit()
            for hook in self.notify:
                try:
                    hook(stream, event)
                except Exception as exc:  # a failed message must never stop the worker
                    log(f"worker: notification failed: {exc!r}")
        self.heartbeat(None, force=True)

    def forever(self):
        self.start()
        log(f"worker: waiting for streams (jobs in {self.settings.jobs_dir})")
        while True:
            if not self.step():
                time.sleep(POLL_S)


def main(argv=None):
    from .api.settings import ApiSettings

    parser = argparse.ArgumentParser(prog="aigcm.worker", description=__doc__.split("\n\n")[0])
    parser.add_argument("--once", action="store_true", help="run at most one queued stream, then exit")
    args = parser.parse_args(argv)
    worker = Worker(ApiSettings.from_env())
    if args.once:
        worker.start()
        worker.step()
    else:
        worker.forever()


if __name__ == "__main__":
    main()
