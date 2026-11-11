"""Light copies for playing in the app: made in the background, served for playback, never for downloads,
shares or posts (the full file stays the one that goes to YouTube)."""

import shutil
import subprocess
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select

from aigcm import db
from aigcm.api import create_app
from aigcm.api.settings import ApiSettings
from aigcm.db.models import Clip, Render
from aigcm.manage import import_jobs
from aigcm.studio import lane

DEMO = Path(__file__).resolve().parent.parent / "demo"
APP = {"x-kaatclip": "1"}


def ffmpeg():
    try:
        from aigcm.media import tool
        return tool("ffmpeg")
    except RuntimeError:
        return None


@pytest.fixture
def app(tmp_path):
    jobs = tmp_path / "jobs"
    shutil.copytree(DEMO, jobs, ignore=shutil.ignore_patterns("decisions.json", "run.log"))
    settings = ApiSettings(db_url=db.sqlite_url(tmp_path / "t.db"), jobs_dir=jobs, dev_login=True,
                           invites=frozenset({"owner@example.com"}), min_free_bytes=0)
    app = create_app(settings)
    with app.state.sessions() as s:
        import_jobs(s, settings, "owner@example.com")
        s.query(Render).delete()
        s.commit()
    return app


def first_clip(app):
    with app.state.sessions() as s:
        clip = s.scalars(select(Clip).order_by(Clip.id)).first()
        return clip.id, app.state.settings.jobs_dir / clip.stream.job_dir / "clips" / clip.file_name


def test_playback_uses_the_light_copy_once_made(app):
    client = TestClient(app, base_url="http://localhost", headers=APP)
    client.post("/auth/dev-login", json={"email": "owner@example.com"})
    clip_id, full = first_clip(app)
    clip = next(c for c in client.get("/api/library").json()["items"] if c["id"] == clip_id)
    assert clip["play"] == f"/media/clips/{clip_id}?view=1"

    # No light copy yet: the full file plays, and the stream's posters job is queued to make it (once).
    assert client.get(clip["play"]).content == full.read_bytes()
    client.get(clip["play"])
    with app.state.sessions() as s:
        assert len(s.scalars(select(Render).where(Render.kind == "posters")).all()) == 1

    lane.view_path(full).write_bytes(b"light copy")
    assert client.get(clip["play"]).content == b"light copy"
    assert client.get(clip["play"], headers={"range": "bytes=0-4"}).content == b"light"     # phones ask in ranges
    # Downloads, shares and the sponsor-safe copy are always the full file.
    assert client.get(f"/media/clips/{clip_id}").content == full.read_bytes()
    assert client.get(f"/media/clips/{clip_id}?view=1&download=1").content == full.read_bytes()


@pytest.mark.skipif(ffmpeg() is None, reason="ffmpeg is not installed")
def test_a_light_copy_is_720_wide_and_much_smaller(tmp_path):
    from aigcm.media import probe

    src = tmp_path / "clip.mp4"
    subprocess.run([ffmpeg(), "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=s=1080x1920:r=30:d=4",
                    "-f", "lavfi", "-i", "sine=f=440:d=4", "-c:v", "libx264", "-b:v", "8M", "-c:a", "aac",
                    "-shortest", str(src)], check=True)
    out = lane.make_view(src, threads=2)
    assert out == tmp_path / "clip.view.mp4" and not (tmp_path / "clip.view.part.mp4").exists()
    info = probe(out)
    assert info["width"] == 720 and info["height"] == 1280
    assert out.stat().st_size < src.stat().st_size / 2
    assert lane.make_view(tmp_path / "missing.mp4") is None
