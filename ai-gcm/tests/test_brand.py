"""The brand kit (M3.6): saved once, applied to new edits, exports and the engine's clips."""

import shutil
import subprocess
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from aigcm import db
from aigcm.api import create_app
from aigcm.api.settings import ApiSettings
from aigcm.db.models import Render
from aigcm.manage import import_jobs
from aigcm.studio import brand
from aigcm.studio import edit as E

DEMO = Path(__file__).resolve().parent.parent / "demo"
APP = {"x-kaatclip": "1"}


def ffmpeg():
    try:
        from aigcm.media import tool
        return tool("ffmpeg")
    except RuntimeError:
        return None


needs_ffmpeg = pytest.mark.skipif(ffmpeg() is None, reason="ffmpeg is not installed")


def png_bytes():
    import cv2
    import numpy as np

    image = np.zeros((64, 64, 4), np.uint8)
    image[..., 2] = image[..., 3] = 255
    return cv2.imencode(".png", image)[1].tobytes()


def tiny_video(path, seconds=2, audio=True):
    cmd = [ffmpeg(), "-v", "error", "-y", "-f", "lavfi", "-i", f"testsrc2=s=320x240:r=15:d={seconds}"]
    if audio:
        cmd += ["-f", "lavfi", "-i", f"sine=d={seconds}", "-shortest"]
    subprocess.run(cmd + ["-c:v", "libx264", "-preset", "ultrafast", str(path)], check=True)
    return path


@pytest.fixture
def app(tmp_path):
    jobs = tmp_path / "jobs"
    shutil.copytree(DEMO, jobs, ignore=shutil.ignore_patterns("decisions.json", "run.log"))
    settings = ApiSettings(db_url=db.sqlite_url(tmp_path / "t.db"), jobs_dir=jobs, dev_login=True,
                           invites=frozenset({"owner@example.com", "b@example.com"}), min_free_bytes=0)
    app = create_app(settings)
    with app.state.sessions() as s:
        import_jobs(s, settings, "owner@example.com")
        s.query(Render).filter_by(kind="posters").delete()
        s.commit()
    return app


def client_for(app, email):
    client = TestClient(app, base_url="http://localhost")
    client.post("/auth/dev-login", json={"email": email}, headers=APP)
    return client


def test_kit_fields_are_checked_and_tidied():
    kit = brand.BrandKit(hashtags=["bgmi", "#BGMI", "shorts!", "#हिंदी", "  "], instagram="kaatclip", name="K")
    assert kit.hashtags == ["#bgmi", "#shorts", "#हिंदी"] and kit.instagram == "@kaatclip"
    assert kit.strip_text() == "K  •  IG: @kaatclip"
    with pytest.raises(ValueError):
        brand.BrandKit(name="x" * 41)
    with pytest.raises(ValueError):
        brand.BrandKit(colour="red")
    found = {"logo": None, "intro": Path("i.mp4"), "outro": None}
    assert brand.defaults(brand.BrandKit(use_intro=True, use_outro=True, lower_third=True), found) == {
        "hook_color": "yellow", "caption_color": "white", "caption_size": "normal",
        "lower_third": False, "intro": True, "outro": False}       # nothing to show in the strip, no outro file


def test_post_text_adds_the_kit_and_can_replace_the_game_line():
    engine = ("Full stream: https://youtu.be/x\n\nBGMI is a trademark of KRAFTON, Inc. This video is not endorsed by "
              "or affiliated with KRAFTON.\n\n#bgmi #shorts")
    out = brand.post_text("WIN 🏆", engine, ["#bgmi", "#shorts"], brand.BrandKit(description="Live daily 8 PM",
                                                                                 hashtags=["#kaatclip", "#BGMI"]))
    assert out["description"].split("\n\n") == ["Full stream: https://youtu.be/x", "Live daily 8 PM",
                                                 engine.split("\n\n")[1], "#kaatclip #BGMI #shorts"]
    assert out["text"].startswith("WIN 🏆\n\nFull stream")
    mine = brand.post_text("WIN", engine, [], brand.BrandKit(disclaimer="Not affiliated with Krafton."))
    assert "trademark" not in mine["description"] and "Not affiliated with Krafton." in mine["description"]
    assert "KRAFTON" not in brand.post_text("WIN", engine, [], brand.BrandKit(disclaimer=""))["description"]


def test_kit_api_saves_checks_and_keeps_kits_apart(app):
    owner = client_for(app, "owner@example.com")
    view = owner.get("/api/brand").json()
    assert view["kit"]["hook_color"] == "yellow" and view["files"] == {"logo": None, "intro": None, "outro": None}
    saved = owner.put("/api/brand", json={"name": "Kaatclip", "upi": "k@okaxis", "lower_third": True,
                                          "caption_color": "yellow", "hashtags": ["bgmi"]}, headers=APP).json()
    assert saved["kit"]["hashtags"] == ["#bgmi"] and saved["strip"] == "/media/brand/strip"
    assert owner.put("/api/brand", json={"name": "x" * 41}, headers=APP).status_code == 422
    assert owner.put("/api/brand", json={"surprise": 1}, headers=APP).status_code == 422
    other = client_for(app, "b@example.com")
    assert other.get("/api/brand").json()["kit"]["name"] == ""


def test_logo_upload_is_checked_and_re_encoded(app):
    owner = client_for(app, "owner@example.com")
    bad = owner.post("/api/brand/logo", files={"file": ("x.png", b"<script>alert(1)</script>", "image/png")}, headers=APP)
    assert bad.status_code == 422
    good = owner.post("/api/brand/logo", files={"file": ("logo.png", png_bytes(), "image/png")}, headers=APP).json()
    assert good["files"]["logo"] == "/media/brand/logo"
    image = owner.get("/media/brand/logo")
    assert image.headers["content-type"] == "image/png" and image.content[:4] == b"\x89PNG"
    assert client_for(app, "b@example.com").get("/media/brand/logo").status_code == 404
    if ffmpeg():
        strip = owner.get("/media/brand/strip")
        assert strip.status_code == 200 and strip.headers["content-type"] == "image/png"
    assert owner.delete("/api/brand/logo", headers=APP).json()["files"]["logo"] is None


@needs_ffmpeg
def test_intro_upload_is_normalised(app, tmp_path):
    from aigcm.media import probe

    owner = client_for(app, "owner@example.com")
    raw = tiny_video(tmp_path / "intro.mp4", seconds=9, audio=False).read_bytes()
    view = owner.post("/api/brand/intro", files={"file": ("intro.mp4", raw, "video/mp4")}, headers=APP).json()
    assert view["files"]["intro"] == "/media/brand/intro" and view["lengths"]["intro"] == brand.CLIP_MAX_S
    info = probe(brand.files(app.state.settings.jobs_dir, 1)["intro"])
    assert (info["width"], info["height"], info["has_audio"]) == (1080, 1920, True)   # silence added
    assert info["duration"] == pytest.approx(brand.CLIP_MAX_S, abs=0.1)
    bad = owner.post("/api/brand/outro", files={"file": ("o.mp4", b"not a video", "video/mp4")}, headers=APP)
    assert bad.status_code == 422


def test_new_edits_take_the_kit(app):
    owner = client_for(app, "owner@example.com")
    owner.put("/api/brand", json={"hook_color": "white", "caption_color": "yellow", "caption_size": "large",
                                  "name": "Kaatclip", "lower_third": True}, headers=APP)
    stream = next(s for s in owner.get("/api/streams").json() if s["status"] == "done")
    clip = owner.get(f"/api/streams/{stream['id']}/clips").json()[0]
    data = owner.get(f"/api/clips/{clip['id']}/studio").json()["edit"]["data"]
    assert data["hook"]["color"] == "white" and data["captions"]["color"] == "yellow"
    assert data["captions"]["size"] == "large" and data["lower_third"] is True and data["intro"] is False
    text = owner.get(f"/api/clips/{clip['id']}/post-text").json()
    assert set(text) == {"title", "description", "hashtags", "text"}
    assert client_for(app, "b@example.com").get(f"/api/clips/{clip['id']}/post-text").status_code == 404


@needs_ffmpeg
def test_render_with_strip_intro_and_outro(tmp_path):
    from aigcm.media import probe
    from aigcm.studio import render as R

    src = tmp_path / "land.mp4"
    subprocess.run([ffmpeg(), "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=s=640x360:r=15:d=6",
                    "-c:v", "libx264", "-preset", "ultrafast", "-g", "15", str(src)], check=True)   # no sound
    jobs = tmp_path / "jobs"
    intro = brand.save_clip(jobs, 1, "intro", tiny_video(tmp_path / "i.mp4", 2).read_bytes())
    outro = brand.save_clip(jobs, 1, "outro", tiny_video(tmp_path / "o.mp4", 1).read_bytes())
    strip = brand.strip_for(jobs, 1, brand.BrandKit(name="Kaatclip", lower_third=True))
    edit = E.default_edit(1, 5, 640, 360, brand={"lower_third": True, "intro": True, "outro": True})
    out = R.render(edit, src, 0.0, False, tmp_path / "out.mp4", threads=2, strip_png=strip, intro=intro, outro=outro)
    info = probe(out)
    assert (info["width"], info["height"], info["has_audio"]) == (1080, 1920, True)
    assert info["duration"] == pytest.approx(2 + 4 + 1, abs=0.2)
    plain = R.render(edit.model_copy(update={"intro": False, "outro": False}), src, 0.0, False, tmp_path / "p.mp4",
                     threads=2, strip_png=strip, intro=intro, outro=outro)
    assert probe(plain)["duration"] == pytest.approx(4, abs=0.1)


def test_the_worker_hands_the_kit_to_the_engine(app):
    from aigcm.db.models import Stream
    from aigcm.jobs import read_json
    from aigcm.worker import write_brand

    owner = client_for(app, "owner@example.com")
    owner.put("/api/brand", json={"hook_color": "white", "use_intro": True}, headers=APP)
    with app.state.sessions() as s:
        stream = s.query(Stream).filter_by(status="done").first()
        folder = app.state.settings.jobs_dir / stream.job_dir
        write_brand(s, stream, folder, app.state.settings)
    saved = read_json(folder / "brand.json")
    assert saved["defaults"]["hook_color"] == "white" and saved["defaults"]["intro"] is False   # no intro file yet
    assert saved["intro"] == "" and saved["kit"]["use_intro"] is True


def test_an_export_is_reused_only_while_its_look_is_unchanged(app):
    from aigcm.api.studio import look
    from aigcm.db.models import Clip

    owner = client_for(app, "owner@example.com")
    with app.state.sessions() as s:
        clip = s.query(Clip).first()
        before = look(app.state.settings, s, clip, 0)
    owner.put("/api/brand", json={"hook_color": "white"}, headers=APP)      # the automatic edit changes
    with app.state.sessions() as s:
        clip = s.query(Clip).first()
        after = look(app.state.settings, s, clip, 0)
        assert after != before and look(app.state.settings, s, clip, 0) == after
