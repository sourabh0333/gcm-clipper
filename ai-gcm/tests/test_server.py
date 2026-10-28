import json
import shutil
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

import pytest

from aigcm import server
from aigcm.config import ROOT, Settings


@pytest.fixture
def app(tmp_path):
    shutil.copytree(ROOT / "demo", tmp_path / "jobs")
    server.Handler.jobs = server.Jobs(Settings(jobs_dir=tmp_path / "jobs"))
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{httpd.server_port}"
    httpd.shutdown()
    httpd.server_close()


def call(url, body=None, headers=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json", **(headers or {})})
    with urllib.request.urlopen(req) as res:
        return res.status, dict(res.headers), res.read()


def test_jobs_show_their_state(app):
    _, _, body = call(f"{app}/api/jobs")
    states = {j["name"]: j["state"] for j in json.loads(body)}
    assert states == {"demo-finished": "done", "demo-processing": "stopped", "demo-failed": "failed"}


def test_decisions_are_saved_and_undone(app):
    call(f"{app}/api/jobs/demo-finished/decisions", {"id": "m01", "verdict": "keep"})
    _, _, body = call(f"{app}/api/jobs/demo-finished/decisions", {"id": "m02", "verdict": "reject"})
    job = json.loads(body)
    assert (job["kept"], job["reviewed"]) == (1, 2)
    _, _, body = call(f"{app}/api/jobs/demo-finished/decisions", {"id": "m02", "verdict": None})
    assert list(json.loads(body)["decisions"]) == ["m01"]


def test_clips_stream_in_ranges(app):
    url = f"{app}/media/demo-finished/01_multi_kill_m01.mp4?download=1"
    status, headers, body = call(url, headers={"Range": "bytes=10-19"})
    assert status == 206 and len(body) == 10
    assert headers["Content-Range"].startswith("bytes 10-19/")
    assert "attachment" in headers["Content-Disposition"]


def test_bad_links_and_paths_are_refused(app):
    with pytest.raises(urllib.error.HTTPError) as err:
        call(f"{app}/api/jobs", {"url": "https://example.com/video"})
    assert err.value.code == 400
    for path in ["/api/jobs/..", "/media/demo-finished/..%2F..%2Fsettings.json", "/../aigcm/server.py"]:
        with pytest.raises(urllib.error.HTTPError) as err:
            call(app + path)
        assert err.value.code == 404


def test_app_files_are_served(app):
    status, headers, body = call(f"{app}/")
    assert status == 200 and b"GCM Clipper" in body
    assert call(f"{app}/manifest.webmanifest")[1]["Content-Type"] == "application/manifest+json"
