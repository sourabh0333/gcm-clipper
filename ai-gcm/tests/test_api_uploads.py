"""Resumable uploads (tus semantics), their guards, and what they leave on disk."""

import base64
import subprocess
from datetime import timedelta

import pytest
from fastapi.testclient import TestClient

from aigcm import db, media
from aigcm.api import create_app
from aigcm.api import uploads as uploads_module
from aigcm.api.settings import ApiSettings
from aigcm.db.models import Upload, utcnow

APP = {"x-kaatclip": "1"}
CHUNK = {"content-type": "application/offset+octet-stream", **APP}


def meta(**fields):
    return ",".join(f"{k} {base64.b64encode(v.encode()).decode()}" for k, v in fields.items())


@pytest.fixture
def app(tmp_path, monkeypatch):
    settings = ApiSettings(db_url=db.sqlite_url(tmp_path / "t.db"), jobs_dir=tmp_path / "jobs", dev_login=True,
                           invites=frozenset({"a@example.com", "b@example.com"}), min_free_bytes=0)
    monkeypatch.setattr(media, "probe", lambda path: {"duration": 1800.0, "width": 1280, "height": 720})
    return create_app(settings)


def client_for(app, email):
    client = TestClient(app, base_url="http://localhost")
    assert client.post("/auth/dev-login", json={"email": email}, headers=APP).status_code == 200
    return client


def start(client, length, filename="Rank push day 3.mp4", **extra):
    return client.post("/api/uploads", headers={**APP, "tus-resumable": "1.0.0", "upload-length": str(length),
                                                 "upload-metadata": meta(filename=filename, **extra)})


def test_a_chunked_upload_resumes_after_a_lost_answer_and_queues_the_stream(app):
    a = client_for(app, "a@example.com")
    data = bytes(range(256)) * 400   # 102,400 bytes
    created = start(a, len(data), title="Conqueror push", recorded_on="2026-11-05")
    assert created.status_code == 201 and created.headers["tus-resumable"] == "1.0.0"
    url, stream_id = created.headers["location"], created.headers["x-stream-id"]
    assert a.head(url).headers["upload-offset"] == "0"

    first = a.patch(url, content=data[:40000], headers={**CHUNK, "upload-offset": "0"})
    assert first.status_code == 204 and first.headers["upload-offset"] == "40000"
    # The browser never saw that answer and sends the same chunk again: refused, it asks, it resumes.
    assert a.patch(url, content=data[:40000], headers={**CHUNK, "upload-offset": "0"}).status_code == 409
    offset = int(a.head(url).headers["upload-offset"])
    assert offset == 40000
    stream = a.get(f"/api/streams/{stream_id}").json()
    assert stream["status"] == "uploading" and stream["upload"]["offset"] == 40000
    last = a.patch(url, content=data[offset:], headers={**CHUNK, "upload-offset": str(offset)})
    assert last.status_code == 204 and last.headers["upload-offset"] == str(len(data))

    stream = a.get(f"/api/streams/{stream_id}").json()
    assert stream["status"] == "queued" and stream["title"] == "Conqueror push" and stream["duration_s"] == 1800.0
    assert stream["recorded_on"] == "2026-11-05" and "upload" not in stream
    source = app.state.settings.jobs_dir / stream_id / "source.mp4"
    assert source.read_bytes() == data
    assert a.patch(url, content=b"x", headers={**CHUNK, "upload-offset": str(len(data))}).status_code == 409


def test_someone_else_cannot_see_or_touch_an_upload(app):
    a, b = client_for(app, "a@example.com"), client_for(app, "b@example.com")
    url = start(a, 10).headers["location"]
    assert b.head(url).status_code == 404
    assert b.patch(url, content=b"0123456789", headers={**CHUNK, "upload-offset": "0"}).status_code == 404
    assert b.delete(url, headers=APP).status_code == 404
    assert TestClient(app).head(url).status_code == 401


@pytest.mark.parametrize("filename, length, status", [
    ("stream.avi", 100, 415),           # not MP4, MKV or MOV
    ("stream.mp4", 0, 413),             # empty
    ("stream.mp4", 11 * 1024**3, 413),  # over 10 GB
])
def test_wrong_files_are_refused_up_front(app, filename, length, status):
    a = client_for(app, "a@example.com")
    assert start(a, length, filename=filename).status_code == status


def test_mkv_and_mov_are_accepted_and_kept_with_their_extension(app):
    a = client_for(app, "a@example.com")
    for name in ("obs 2026-11-05.mkv", "phone.MOV"):
        response = start(a, 5, filename=name)
        assert response.status_code == 201
        stream_id = response.headers["x-stream-id"]
        folder = app.state.settings.jobs_dir / stream_id
        assert [p.name for p in folder.iterdir()] == ["source" + name[-4:].lower()]


def test_the_disk_guard_counts_unfinished_uploads(app, monkeypatch):
    a = client_for(app, "a@example.com")
    total, free = 500 * 1024**3, 30 * 1024**3
    usage = uploads_module.shutil._ntuple_diskusage(total, total - free, free)
    monkeypatch.setattr(uploads_module.shutil, "disk_usage", lambda p: usage)
    app.state.settings.min_free_bytes = 20 * 1024**3
    assert start(a, 6 * 1024**3).status_code == 201       # 30 - 6 = 24 GB left: fine
    assert start(a, 6 * 1024**3).status_code == 507       # the first one's 6 GB still counts: 18 GB left


def test_one_creator_can_have_three_unfinished_uploads(app):
    a = client_for(app, "a@example.com")
    assert [start(a, 10).status_code for _ in range(4)] == [201, 201, 201, 429]


def test_a_chunk_cannot_run_past_the_declared_length(app):
    a = client_for(app, "a@example.com")
    url = start(a, 10).headers["location"]
    assert a.patch(url, content=b"x" * 11, headers={**CHUNK, "upload-offset": "0"}).status_code == 413
    assert a.head(url).headers["upload-offset"] == "0"
    assert a.patch(url, content=b"x" * 10, headers={**APP, "upload-offset": "0",
                                                    "content-type": "text/plain"}).status_code == 415


def test_a_file_that_isnt_a_video_fails_and_is_removed(app, monkeypatch):
    def broken(path):
        raise RuntimeError("ffprobe: Invalid data found")
    monkeypatch.setattr(media, "probe", broken)
    a = client_for(app, "a@example.com")
    created = start(a, 4)
    a.patch(created.headers["location"], content=b"junk", headers={**CHUNK, "upload-offset": "0"})
    stream = a.get(f"/api/streams/{created.headers['x-stream-id']}").json()
    assert stream["status"] == "failed" and "isn't a video" in stream["error"]
    assert list((app.state.settings.jobs_dir / stream["id"]).iterdir()) == []


def test_cancel_and_delete_remove_the_files(app):
    a = client_for(app, "a@example.com")
    created = start(a, 10)
    folder = app.state.settings.jobs_dir / created.headers["x-stream-id"]
    assert a.delete(created.headers["location"], headers=APP).status_code == 204
    assert not folder.exists() and a.get("/api/streams").json() == []

    done = start(a, 3)
    a.patch(done.headers["location"], content=b"abc", headers={**CHUNK, "upload-offset": "0"})
    stream_id = done.headers["x-stream-id"]
    assert a.delete(done.headers["location"], headers=APP).status_code == 409   # complete: delete the stream
    assert a.delete(f"/api/streams/{stream_id}", headers=APP).status_code == 204
    assert not (app.state.settings.jobs_dir / stream_id).exists()


def test_running_streams_cannot_be_deleted(app):
    a = client_for(app, "a@example.com")
    created = start(a, 3)
    a.patch(created.headers["location"], content=b"abc", headers={**CHUNK, "upload-offset": "0"})
    from aigcm.db.models import Stream
    with app.state.sessions() as s:
        s.get(Stream, created.headers["x-stream-id"]).status = "running"
        s.commit()
    assert a.delete(f"/api/streams/{created.headers['x-stream-id']}", headers=APP).status_code == 409


def test_stale_unfinished_uploads_expire(app):
    a = client_for(app, "a@example.com")
    old, fresh = start(a, 10), start(a, 10)
    with app.state.sessions() as s:
        row = s.get(Upload, old.headers["location"].rsplit("/", 1)[1])
        row.updated_at = utcnow() - timedelta(days=4)
        s.commit()
        removed = uploads_module.expire_uploads(s, app.state.settings)
    assert removed == [old.headers["x-stream-id"]]
    assert not (app.state.settings.jobs_dir / old.headers["x-stream-id"]).exists()
    assert [x["id"] for x in a.get("/api/streams").json()] == [fresh.headers["x-stream-id"]]


def test_a_real_recording_passes_the_ffprobe_check(tmp_path, monkeypatch):
    try:
        ffmpeg = media.tool("ffmpeg")
    except RuntimeError:
        pytest.skip("ffmpeg is not installed here")
    video = tmp_path / "clip.mp4"
    subprocess.run([ffmpeg, "-v", "error", "-f", "lavfi", "-i", "testsrc=duration=2:size=320x180:rate=30",
                    "-f", "lavfi", "-i", "sine=duration=2", "-shortest", "-c:v", "libx264", "-c:a", "aac",
                    str(video)], check=True)
    settings = ApiSettings(db_url=db.sqlite_url(tmp_path / "t.db"), jobs_dir=tmp_path / "jobs", dev_login=True,
                           invites=frozenset({"a@example.com"}), min_free_bytes=0)
    a = client_for(create_app(settings), "a@example.com")
    data = video.read_bytes()
    created = start(a, len(data))
    url, offset = created.headers["location"], 0
    while offset < len(data):   # 8 KB chunks, as the browser sends 8 MB ones
        piece = data[offset:offset + 8192]
        offset = int(a.patch(url, content=piece, headers={**CHUNK, "upload-offset": str(offset)}).headers["upload-offset"])
    stream = a.get(f"/api/streams/{created.headers['x-stream-id']}").json()
    assert stream["status"] == "queued" and 1.9 <= stream["duration_s"] <= 2.2
