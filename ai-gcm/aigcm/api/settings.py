"""Platform settings, read from ai-gcm/.env. Kept apart from the engine's Settings so the API and worker
start without importing any engine code."""

import os
from dataclasses import dataclass, field
from pathlib import Path

from ..config import ROOT, load_dotenv


def _emails(text):
    return frozenset(e.strip().lower() for e in (text or "").split(",") if e.strip())


@dataclass
class ApiSettings:
    db_url: str = ""
    jobs_dir: Path = ROOT / "jobs"
    web_dir: Path = ROOT / "web" / "dist"
    # Where the browser reaches the app: the Google redirect URI and Telegram links are built from it.
    public_url: str = "http://localhost:8770"
    google_client_id: str = ""
    google_client_secret: str = ""
    # Beta sign-in is by invitation: these addresses (plus rows in the invites table) may sign in, and the
    # admins may also invite others.
    invites: frozenset = field(default_factory=frozenset)
    admins: frozenset = field(default_factory=frozenset)
    # A sign-in without Google, for tests and development on the laptop only (see auth.dev_login_allowed).
    dev_login: bool = False
    telegram_bot_token: str = ""
    # Encrypts creators' YouTube tokens at rest (M4). Made once by `python -m aigcm.manage token-key`, kept in .env.
    token_key: str = ""
    session_days: int = 30
    max_upload_bytes: int = 10 * 1024**3
    max_chunk_bytes: int = 16 * 1024**2
    # Uploads are refused when they would leave less than this free on the jobs disk.
    min_free_bytes: int = 20 * 1024**3

    @classmethod
    def from_env(cls, **overrides):
        load_dotenv(ROOT / ".env")
        data_dir = ROOT / "data"
        s = cls(
            db_url=os.environ.get("AIGCM_DB_URL") or f"sqlite:///{(data_dir / 'kaatclip.db').as_posix()}",
            jobs_dir=ROOT / os.environ.get("AIGCM_JOBS_DIR", "jobs"),
            public_url=os.environ.get("AIGCM_PUBLIC_URL", cls.public_url).rstrip("/"),
            google_client_id=os.environ.get("GOOGLE_CLIENT_ID", "").strip(),
            google_client_secret=os.environ.get("GOOGLE_CLIENT_SECRET", "").strip(),
            invites=_emails(os.environ.get("AIGCM_INVITES")),
            admins=_emails(os.environ.get("AIGCM_ADMINS")),
            dev_login=os.environ.get("AIGCM_DEV_LOGIN", "") == "1",
            telegram_bot_token=os.environ.get("TELEGRAM_BOT_TOKEN", "").strip(),
            token_key=os.environ.get("KAATCLIP_TOKEN_KEY", "").strip(),
        )
        for key, value in overrides.items():
            setattr(s, key, value)
        return s
