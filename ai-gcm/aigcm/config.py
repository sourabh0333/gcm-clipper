"""Run settings. Defaults suit a 16:9 BGMI recording; override them in .env or on the command line."""

import os
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Screen regions where BGMI shows messages worth reading, as (x, y, width, height) fractions of the frame.
# Kills come from the Eliminations counter (located automatically); "banner" catches chicken dinner, knock
# and accolade messages. Check regions against real footage with `aigcm frames`.
DEFAULT_REGIONS = {
    "banner": (0.15, 0.05, 0.70, 0.30),
}


def load_dotenv(path):
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


@dataclass
class Settings:
    jobs_dir: Path = ROOT / "jobs"
    download_height: int = 720

    # Vision: frames sampled per second, the height they are scaled to, and how often the HUD is read
    # even when nothing seems to change.
    vision_fps: float = 2.0
    vision_height: int = 720
    ocr_every_s: float = 10.0
    regions: dict = field(default_factory=lambda: dict(DEFAULT_REGIONS))
    player_names: tuple = ()

    # Moments: events closer than merge_gap_s belong to one fight; clips get a lead-in and a reaction tail.
    # The Eliminations counter changes at the moment of the kill, so the lead-in has to cover the fight
    # before it (a 4 s lead-in on the first test stream cut straight to the aftermath).
    audio_hop_s: float = 0.5
    merge_gap_s: float = 25.0
    pre_roll_s: float = 12.0
    post_roll_s: float = 6.0
    min_clip_s: float = 15.0
    max_clip_s: float = 60.0
    max_candidates: int = 25
    top_n: int = 12

    # Rendering: "auto" keeps a vertical stream as it is ("native") and puts a landscape one over a
    # blurred fill ("blur"); "split" puts a given facecam box on top.
    layout: str = "auto"
    facecam: tuple | None = None

    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash-lite"
    gemini_rpm: int = 10
    whisper_model: str = "small"
    # Auto-detect mistook Hinglish clips for Spanish and Portuguese; set AIGCM_CAPTION_LANGUAGE to change it.
    caption_language: str | None = "hi"

    @classmethod
    def from_env(cls):
        load_dotenv(ROOT / ".env")
        s = cls()
        # AIGCM_JOBS_DIR=demo points the app at the demo jobs made by make_demo.py.
        s.jobs_dir = ROOT / os.environ.get("AIGCM_JOBS_DIR", "jobs")
        s.gemini_api_key = os.environ.get("GEMINI_API_KEY", "").strip()
        s.gemini_model = os.environ.get("AIGCM_GEMINI_MODEL", s.gemini_model)
        s.gemini_rpm = int(os.environ.get("AIGCM_GEMINI_RPM", s.gemini_rpm))
        s.whisper_model = os.environ.get("AIGCM_WHISPER_MODEL", s.whisper_model)
        s.caption_language = os.environ.get("AIGCM_CAPTION_LANGUAGE", s.caption_language) or None
        names = os.environ.get("AIGCM_PLAYER_NAMES", "")
        s.player_names = tuple(n.strip().lower() for n in names.split(",") if n.strip())
        return s
