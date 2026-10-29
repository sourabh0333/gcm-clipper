"""The app's server: serves the PWA in app/, lists jobs, starts, stops and resumes them, streams clips and
saves keep or reject decisions. Standard library only, so it runs wherever the pipeline does.

Jobs run one at a time, as `python -m aigcm run` child processes writing to the job's run.log. Only jobs
started by this server count as running; a job left "running" in its manifest by a crash or a stopped
server shows as stopped and can be resumed.
"""

import json
import mimetypes
import os
import re
import socket
import subprocess
import sys
import threading
import time
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from .__main__ import job_name
from .config import ROOT
from .jobs import STAGES, log, read_json, write_json
from .media import is_url, parse_time

APP_DIR = ROOT / "app"
TYPES = {".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".png": "image/png",
         ".svg": "image/svg+xml", ".webmanifest": "application/manifest+json", ".json": "application/json",
         ".mp4": "video/mp4"}
NAME = re.compile(r"^[\w-]{1,80}$")

# Rough share of a job's time each stage takes, from the three test streams; only for the progress bar.
STAGE_WEIGHT = {"ingest": 0.33, "vision": 0.42, "audio": 0.01, "sounds": 0.02, "transcript": 0.12, "moments": 0.01,
                "judge": 0.02, "captions": 0.0, "render": 0.07, "review": 0.0}
SCANNED = re.compile(r"vision: (\d+) min scanned")


class Jobs:
    def __init__(self, settings):
        self.settings = settings
        self.root = settings.jobs_dir
        self.root.mkdir(parents=True, exist_ok=True)
        self.procs = {}
        self.lock = threading.Lock()

    def folder(self, name):
        if not NAME.match(name or "") or not (self.root / name).is_dir():
            raise LookupError(name)
        return self.root / name

    def running(self):
        return [name for name, proc in self.procs.items() if proc.poll() is None]

    def summary(self, name):
        job = self.folder(name)
        manifest = read_json(job / "manifest.json", {"stages": {}})["stages"]
        settings = read_json(job / "settings.json", {})
        info = read_json(job / "info.json", {})
        stages = [dict(manifest.get(s, {}), name=s, status=manifest.get(s, {}).get("status", "pending"))
                  for s in STAGES]
        last = last_line(job / "run.log")
        live = name in self.running()
        if all(s["status"] == "done" for s in stages):
            state = "done"
        elif any(s["status"] == "failed" for s in stages) and not live:
            state = "failed"
        else:
            state = "running" if live else "stopped"
        progress = sum(STAGE_WEIGHT[s["name"]] for s in stages if s["status"] == "done")
        scanned = SCANNED.findall(read_text(job / "run.log"))
        if live and manifest.get("vision", {}).get("status") == "running" and scanned and info.get("duration"):
            progress += STAGE_WEIGHT["vision"] * min(1.0, int(scanned[-1]) * 60 / info["duration"])
        files = read_json(job / "clips.json", {})
        decisions = read_json(job / "decisions.json", {})
        return {
            "name": name, "state": state, "progress": round(min(progress, 1.0), 3), "stages": stages,
            "title": info.get("title") or settings.get("source") or name, "channel": info.get("channel"),
            "source": settings.get("source"), "section": settings.get("section"),
            "duration": info.get("duration"), "created": round((job / "settings.json").stat().st_mtime)
            if (job / "settings.json").exists() else None,
            "clips": len(files), "kept": sum(d.get("verdict") == "keep" for d in decisions.values()),
            "reviewed": len(decisions), "last_log": last,
        }

    def detail(self, name):
        job = self.folder(name)
        files = read_json(job / "clips.json", {})
        clips = [dict(c, file=files[c["id"]]) for c in read_json(job / "ranked.json", []) if c["id"] in files]
        return dict(self.summary(name), items=clips, decisions=read_json(job / "decisions.json", {}))

    def all(self):
        names = [p.name for p in self.root.iterdir() if p.is_dir() and NAME.match(p.name)]
        jobs = [self.summary(n) for n in names]
        return sorted(jobs, key=lambda j: j["created"] or 0, reverse=True)

    def start(self, url, section_text=""):
        if not is_url(url) or not re.search(r"(youtube\.com|youtu\.be)/", url):
            raise ValueError("Paste a YouTube link (youtube.com or youtu.be).")
        section = None
        if section_text.strip():
            try:
                start, end = (parse_time(v.strip()) for v in section_text.split("-"))
            except ValueError:
                raise ValueError("Write the time range like 0:30:00-1:30:00.") from None
            if end <= start:
                raise ValueError("The end time must be after the start time.")
            section = (start, end)
        name = job_name(url, section)
        args = ["run", url, "--job", name] + (["--section", f"{int(section[0])}-{int(section[1])}"] if section else [])
        self._launch(name, args)
        return name

    def resume(self, name):
        settings = read_json(self.folder(name) / "settings.json", {})
        if not settings.get("source"):
            raise ValueError("This job has no saved source to resume from.")
        section = settings.get("section")
        args = ["run", settings["source"], "--job", name]
        if section:
            args += ["--section", f"{int(section[0])}-{int(section[1])}"]
        self._launch(name, args)

    def _launch(self, name, args):
        with self.lock:
            busy = self.running()
            if busy:
                raise RuntimeError(f"Another job is still running ({busy[0]}). Wait for it or stop it first.")
            job = self.root / name
            job.mkdir(parents=True, exist_ok=True)
            out = open(job / "run.log", "a", encoding="utf-8")
            out.write(f"\n--- started from the app at {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n")
            out.flush()
            self.procs[name] = subprocess.Popen([sys.executable, "-m", "aigcm"] + args, cwd=ROOT, stdout=out,
                                                stderr=subprocess.STDOUT)
            out.close()
            log(f"app: started {name}")

    def stop(self, name):
        proc = self.procs.get(name)
        if proc is None or proc.poll() is not None:
            raise ValueError("This job is not running.")
        if os.name == "nt":
            # terminate() would leave the run's ffmpeg and yt-dlp children behind on Windows.
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)], capture_output=True)
        else:
            proc.terminate()
        proc.wait(timeout=30)
        log(f"app: stopped {name}")

    def decide(self, name, clip_id, verdict, reason=""):
        if verdict not in ("keep", "reject", None):
            raise ValueError("verdict must be keep, reject or null")
        job = self.folder(name)
        with self.lock:
            decisions = read_json(job / "decisions.json", {})
            if verdict is None:
                decisions.pop(clip_id, None)
            else:
                decisions[clip_id] = {"verdict": verdict, "reason": reason[:300],
                                      "at": time.strftime("%Y-%m-%dT%H:%M:%S")}
            write_json(job / "decisions.json", decisions)
        return decisions


def read_text(path):
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def last_line(path):
    lines = [line for line in read_text(path).splitlines() if line.strip() and not line.startswith("---")]
    return lines[-1][:200] if lines else None


class Handler(BaseHTTPRequestHandler):
    jobs: Jobs = None

    def log_message(self, fmt, *args):
        pass

    def do_GET(self):
        url = urlparse(self.path)
        parts = [p for p in url.path.split("/") if p]
        try:
            if parts[:2] == ["api", "jobs"] and len(parts) == 2:
                return self.send_json(self.jobs.all())
            if parts[:2] == ["api", "jobs"] and len(parts) == 3:
                return self.send_json(self.jobs.detail(parts[2]))
            if parts[:1] == ["media"] and len(parts) == 3:
                path = self.jobs.folder(parts[1]) / "clips" / parts[2]
                if not NAME.match(path.stem) or not path.is_file():
                    raise LookupError(parts[2])
                return self.send_file(path, download="download" in parse_qs(url.query))
            path = (APP_DIR / "/".join(parts or ["index.html"])).resolve()
            if APP_DIR.resolve() not in path.parents or not path.is_file():
                raise LookupError(url.path)
            return self.send_file(path, cache="no-cache")
        except LookupError:
            self.send_json({"error": "Not found"}, HTTPStatus.NOT_FOUND)

    def do_POST(self):
        parts = [p for p in urlparse(self.path).path.split("/") if p]
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
            if parts == ["api", "jobs"]:
                name = self.jobs.start(str(body.get("url", "")).strip(), str(body.get("section", "")))
                return self.send_json(self.jobs.summary(name), HTTPStatus.CREATED)
            if parts[:2] == ["api", "jobs"] and len(parts) == 4:
                name, action = parts[2], parts[3]
                if action == "resume":
                    self.jobs.resume(name)
                elif action == "stop":
                    self.jobs.stop(name)
                elif action == "decisions":
                    self.jobs.decide(name, str(body.get("id")), body.get("verdict"), str(body.get("reason", "")))
                else:
                    raise LookupError(action)
                return self.send_json(self.jobs.detail(name))
            raise LookupError(self.path)
        except LookupError:
            self.send_json({"error": "Not found"}, HTTPStatus.NOT_FOUND)
        except RuntimeError as exc:
            self.send_json({"error": str(exc)}, HTTPStatus.CONFLICT)
        except (ValueError, json.JSONDecodeError) as exc:
            self.send_json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)

    def send_json(self, data, status=HTTPStatus.OK):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            pass  # The page was closed or reloaded before the answer arrived.

    def send_file(self, path, download=False, cache="private, max-age=3600"):
        """Send a file, honouring Range requests: phone browsers need them to play and seek video."""
        size = path.stat().st_size
        start, end = 0, size - 1
        match = re.fullmatch(r"bytes=(\d*)-(\d*)", self.headers.get("Range", ""))
        if match and (match[1] or match[2]):
            if match[1]:
                start, end = int(match[1]), min(int(match[2]) if match[2] else size - 1, size - 1)
            else:
                start = max(0, size - int(match[2]))
            if start > end:
                self.send_response(HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE)
                self.send_header("Content-Range", f"bytes */{size}")
                self.end_headers()
                return
            self.send_response(HTTPStatus.PARTIAL_CONTENT)
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        else:
            self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", TYPES.get(path.suffix) or mimetypes.guess_type(path.name)[0]
                         or "application/octet-stream")
        self.send_header("Content-Length", str(end - start + 1))
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Cache-Control", cache)
        if download:
            self.send_header("Content-Disposition", f'attachment; filename="{path.name}"')
        self.end_headers()
        try:
            with open(path, "rb") as f:
                f.seek(start)
                left = end - start + 1
                while left > 0:
                    chunk = f.read(min(256 * 1024, left))
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    left -= len(chunk)
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            pass  # The browser stopped reading, e.g. when the viewer seeks or swipes to the next clip.


def lan_address():
    """This laptop's address on the home network (connecting a UDP socket sends nothing)."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("10.255.255.255", 1))
            return s.getsockname()[0]
    except OSError:
        return None


def serve(settings, host="0.0.0.0", port=8765):
    Handler.jobs = Jobs(settings)
    server = ThreadingHTTPServer((host, port), Handler)
    log(f"app: open http://localhost:{port} on this laptop (jobs in {settings.jobs_dir})")
    if host == "0.0.0.0" and lan_address():
        log(f"app: on a phone on the same Wi-Fi, open http://{lan_address()}:{port}")
    try:
        server.serve_forever()
    finally:
        for name in Handler.jobs.running():
            Handler.jobs.stop(name)
        server.server_close()
