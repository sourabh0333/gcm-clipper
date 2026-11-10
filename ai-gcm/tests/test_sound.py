"""Sound safety (M3.9): music found and flagged, effects that can't be claimed, and the intro check."""

import shutil
import subprocess
from pathlib import Path

import numpy as np
import pytest

from aigcm.studio import edit as E
from aigcm.studio import sound

DEMO = Path(__file__).resolve().parent.parent / "demo"


def ffmpeg():
    try:
        from aigcm.media import tool
        return tool("ffmpeg")
    except RuntimeError:
        return None


needs_ffmpeg = pytest.mark.skipif(ffmpeg() is None, reason="ffmpeg is not installed")


def fake_sounds(music_at):
    t = np.arange(0, 400, 0.96, dtype=np.float32)
    music = np.zeros_like(t)
    for a, b in music_at:
        music[(t >= a) & (t < b)] = 0.6
    return {"t": t, "music": music}


def test_music_spans_merge_and_count_inside_the_parts():
    snd = fake_sounds([(100, 110), (111.5, 115), (300, 302)])
    spans = sound.music_spans(snd)
    assert len(spans) == 2 and spans[0][0] == pytest.approx(100, abs=1) and spans[0][1] == pytest.approx(115, abs=1)
    assert sound.music_spans(snd, 105, 108) == [(105.0, 108.0)]
    segs = [E.Segment(start=90, end=105), E.Segment(start=113, end=130)]
    assert sound.seconds_in([(100, 115)], segs) == pytest.approx(7)
    assert sound.clip_music(None, 100, 200, snd) == pytest.approx(15, abs=1.5)
    assert sound.music_spans(None) == [] and sound.music_spans({"t": np.array([])}) == []


def test_clips_with_music_are_flagged_at_import(tmp_path):
    from aigcm.jobview import finished_clips

    folder = tmp_path / "job"
    shutil.copytree(DEMO / "demo-finished", folder)
    np.savez_compressed(folder / "sounds.npz", **fake_sounds([(280, 300)]))      # under clip m01 (277.5-305.5)
    clips = {c["clip_key"]: c for c in finished_clips(folder)}
    flags = clips["m01"]["details"]["flags"]
    assert [f["kind"] for f in flags] == ["music"] and "1 minute" in flags[0]["text"]
    assert not any(f["kind"] == "music" for f in clips["m02"]["details"]["flags"] or [])


def test_sound_effects_are_ours_and_checked():
    for name in sound.SFX:
        assert sound.sfx_file(name) is not None
    assert sound.sfx_file("../../.env") is None and sound.sfx_file("music") is None
    with pytest.raises(ValueError):
        E.SoundFx(t=1, name="airhorn")
    with pytest.raises(ValueError):
        E.SoundFx(t=1, name="boom", gain=3)


@needs_ffmpeg
def test_effects_mix_over_the_clip_sound(tmp_path):
    from aigcm.media import probe
    from aigcm.studio import render as R

    src = tmp_path / "s.mp4"
    subprocess.run([ffmpeg(), "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=s=640x360:r=15:d=6",
                    "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", "6", "-c:v", "libx264", "-preset",
                    "ultrafast", "-c:a", "aac", str(src)], check=True)
    edit = E.default_edit(1, 5, 640, 360).model_copy(update={"sfx": [E.SoundFx(t=3, name="boom", gain=1.0)]})
    out = R.render(edit, src, 0.0, True, tmp_path / "o.mp4", threads=2)
    assert probe(out)["duration"] == pytest.approx(4, abs=0.1)

    def loudness(start):
        r = subprocess.run([ffmpeg(), "-hide_banner", "-ss", str(start), "-t", "0.4", "-i", str(out), "-af", "volumedetect",
                            "-f", "null", "-"], capture_output=True, text=True)
        return float(r.stderr.split("max_volume:")[1].split("dB")[0])

    assert loudness(2.0) > -20 > loudness(0.2)        # the boom at the kill (2 s in), silence before it


@pytest.mark.skipif(not (Path(__file__).resolve().parent.parent / "models" / "yamnet.tflite").exists(),
                    reason="the sound detector's model isn't downloaded here")
@needs_ffmpeg
def test_music_in_an_intro_is_heard(tmp_path):
    from aigcm.studio.brand import music_in

    melody = tmp_path / "m.mp4"
    subprocess.run([ffmpeg(), "-v", "error", "-y", "-f", "lavfi", "-i",
                    "aevalsrc='0.3*sin(2*PI*(440+220*floor(mod(t*4,4)))*t)':s=48000:d=5", "-c:a", "aac", str(melody)],
                   check=True)
    noise = tmp_path / "n.mp4"
    subprocess.run([ffmpeg(), "-v", "error", "-y", "-f", "lavfi", "-i", "anoisesrc=d=5:amplitude=0.3", "-c:a", "aac",
                    str(noise)], check=True)
    assert music_in(melody) >= 2 and music_in(noise) == 0
