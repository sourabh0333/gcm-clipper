"""Uploading while streaming: a recording sent while OBS still writes it, whose start changes when recording stops,
is compared piece by piece, corrected, finished with its final size, and queued like any upload."""

import base64
import hashlib
import subprocess

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select

from aigcm import db
from aigcm.api import create_app, uploads
from aigcm.api.settings import ApiSettings
from aigcm.db.models import Stream, Upload

APP = {"x-kaatclip": "1"}
TUS = {**APP, "Tus-Resumable": "1.0.0"}
PIECE = 64 * 1024


def ffmpeg():
    try:
        from aigcm.media import tool
        return tool("ffmpeg")
    except RuntimeError:
        return None


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(uploads, "HASH_PIECE", PIECE)
    settings = ApiSettings(db_url=db.sqlite_url(tmp_path / "t.db"), jobs_dir=tmp_path / "jobs", dev_login=True,
                           invites=frozenset({"owner@example.com", "b@example.com"}), min_free_bytes=0)
    client = TestClient(create_app(settings), base_url="http://localhost")
    client.post("/auth/dev-login", json={"email": "owner@example.com"}, headers=APP)
    return client


def meta(name):
    return "filename " + base64.b64encode(name.encode()).decode() + ",title " + base64.b64encode(b"Sunday rank push").decode()


def start(client, name="2026-11-11 20-00-00.mkv"):
    made = client.post("/api/uploads", headers={**TUS, "Upload-Defer-Length": "1", "Upload-Metadata": meta(name)})
    assert made.status_code == 201
    return made.headers["location"], made.headers["x-stream-id"]


def patch(client, url, offset, body, final=None):
    headers = {**TUS, "Upload-Offset": str(offset), "Content-Type": "application/offset+octet-stream"}
    if final is not None:
        headers["Upload-Length"] = str(final)
    return client.patch(url, content=body, headers=headers)


@pytest.mark.skipif(ffmpeg() is None, reason="ffmpeg is not installed")
def test_a_recording_sent_while_growing_is_corrected_and_finished(client, tmp_path):
    final_file = tmp_path / "rec.mkv"
    subprocess.run([ffmpeg(), "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=s=640x360:r=30:d=6", "-f", "lavfi",
                    "-i", "sine=f=440:d=6", "-c:v", "libx264", "-preset", "ultrafast", "-b:v", "2M", "-c:a", "aac",
                    "-shortest", str(final_file)], check=True)
    final = final_file.read_bytes()
    # What the browser saw while OBS was still writing: the same bytes, except the header OBS rewrites at the end.
    early = bytearray(final)
    early[100:5000] = bytes(4900)
    sent = (len(final) * 2 // 3) // PIECE * PIECE

    url, stream_id = start(client)
    head = client.head(url, headers=TUS)
    assert head.headers["upload-defer-length"] == "1" and "upload-length" not in head.headers
    for at in range(0, sent, PIECE):
        assert patch(client, url, at, bytes(early[at:at + PIECE])).status_code == 204
    assert client.get(f"/api/streams/{stream_id}").json()["status"] == "uploading"

    # Recording stopped: compare, re-send what changed, then the rest with the final size.
    server = client.get(f"{url}/hashes", headers=APP).json()
    assert server["offset"] == sent and server["piece"] == PIECE
    changed = [i for i, h in enumerate(server["hashes"])
               if h != hashlib.sha256(final[i * PIECE:(i + 1) * PIECE]).hexdigest()]
    assert changed == [0]
    assert client.put(f"{url}/rewrite", params={"at": 0}, content=final[:PIECE], headers=APP).status_code == 204
    done = patch(client, url, sent, final[sent:], final=len(final))
    assert done.status_code == 204 and int(done.headers["upload-offset"]) == len(final)

    stream = client.get(f"/api/streams/{stream_id}").json()
    assert stream["status"] == "queued" and stream["duration_s"] == pytest.approx(6, abs=0.5)
    assert stream["size_bytes"] == len(final)
    on_laptop = (tmp_path / "jobs" / stream_id / "source.mkv").read_bytes()
    assert on_laptop == final


def test_the_rules_of_a_growing_upload(client, tmp_path):
    url, _ = start(client)
    assert patch(client, url, 0, b"x" * 1000).status_code == 204
    # Rewrites only inside what was received; the final size can't be smaller than what arrived.
    assert client.put(f"{url}/rewrite", params={"at": 900}, content=b"y" * 200, headers=APP).status_code == 416
    assert client.put(f"{url}/rewrite", params={"at": -1}, content=b"y", headers=APP).status_code == 416
    assert client.put(f"{url}/rewrite", params={"at": 10}, content=b"y" * 10, headers=APP).status_code == 204
    assert patch(client, url, 1000, b"", final=500).status_code == 413
    # A normal upload (known size) has no hashes or rewrites.
    normal = client.post("/api/uploads", headers={**TUS, "Upload-Length": "10", "Upload-Metadata": meta("a.mp4")})
    plain = normal.headers["location"]
    assert client.get(f"{plain}/hashes", headers=APP).status_code == 409
    assert client.put(f"{plain}/rewrite", params={"at": 0}, content=b"z", headers=APP).status_code == 409
    # Someone else's upload is invisible.
    other = TestClient(client.app, base_url="http://localhost")
    other.post("/auth/dev-login", json={"email": "b@example.com"}, headers=APP)
    assert other.get(f"{url}/hashes", headers=APP).status_code == 404
    # The disk check keeps room for a growing recording of unknown size.
    with client.app.state.sessions() as s:
        assert uploads.committed_bytes(s) >= uploads.GROWING_RESERVE - 1000
        assert s.scalar(select(Upload).where(Upload.growing.is_(True))).length == 0
        assert s.scalar(select(Stream).where(Stream.source_name.like("%.mkv"))).size_bytes is None
