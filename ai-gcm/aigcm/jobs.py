"""Job folders and the stage runner. Every stage records its status in manifest.json, so a stopped or
failed run resumes from the first stage that is not done."""

import json
import os
import threading
import time
from pathlib import Path

# Vision is the slow stage and doesn't depend on audio, so it comes first: forcing a rerun of the (one
# second) audio analysis then doesn't redo vision.
STAGES = ["ingest", "vision", "audio", "sounds", "transcript", "moments", "judge", "captions", "render", "review"]


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def read_json(path, default=None):
    path = Path(path)
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, data):
    """Write through a temporary file so a crash never leaves half a file behind."""
    path = Path(path)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, path)


class Job:
    def __init__(self, root):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.manifest_path = self.root / "manifest.json"
        self.manifest = read_json(self.manifest_path, {"stages": {}})
        self._lock = threading.Lock()

    def path(self, *parts):
        return self.root.joinpath(*parts)

    def done(self, stage):
        return self.manifest["stages"].get(stage, {}).get("status") == "done"

    def _set(self, stage, **fields):
        # Stages that run side by side (vision with the audio stages) write the manifest from two threads.
        with self._lock:
            self.manifest["stages"].setdefault(stage, {}).update(fields)
            write_json(self.manifest_path, self.manifest)

    def invalidate_from(self, stage):
        """Mark a stage and everything after it as not done, so they run again."""
        for name in STAGES[STAGES.index(stage):]:
            if name in self.manifest["stages"]:
                self._set(name, status="stale")

    def run(self, stage, fn):
        if self.done(stage):
            log(f"{stage}: already done, skipping")
            return
        log(f"{stage}: starting")
        started = time.time()
        self._set(stage, status="running", error=None, started=round(started))
        try:
            fn(self)
        except BaseException as exc:
            self._set(stage, status="failed", error=repr(exc))
            raise
        self._set(stage, status="done", seconds=round(time.time() - started, 1))
        log(f"{stage}: done in {time.time() - started:.0f}s")

    def run_parallel(self, groups):
        """Run several stage lists at the same time, each list in order: [[("vision", fn)], [("audio", fn), ...]].
        Vision reads frames and the audio stages read the wav, so on a 4-core laptop they overlap well. The
        first error is raised after every group has stopped."""
        errors = []

        def worker(stages):
            try:
                for name, fn in stages:
                    self.run(name, fn)
            except BaseException as exc:
                errors.append(exc)

        threads = [threading.Thread(target=worker, args=(g,), daemon=True) for g in groups]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        if errors:
            raise errors[0]
