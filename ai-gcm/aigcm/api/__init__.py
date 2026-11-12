"""The platform API (FastAPI): accounts, uploads, streams, clips and decisions. It never runs the pipeline
itself; the worker does (aigcm.worker). See plans/M2 platform core plan.md."""

import httpx
from fastapi import FastAPI
from sqlalchemy import text

from .. import db
from ..telegram import Bot
from . import (account, admin, auth, brand, calendar, channel, clips, legal, compilations, highlights, library, live, notifications, posts, streams, studio,
               uploads, web, youtube)
from .deps import csrf_guard
from .settings import ApiSettings

VERSION = "0.2.0"


def create_app(settings: ApiSettings | None = None, http: httpx.Client | None = None) -> FastAPI:
    """`http` is the client used to talk to Google (tests pass one with a fake transport)."""
    settings = settings or ApiSettings.from_env()
    engine = db.make_engine(settings.db_url)
    db.migrate(engine)

    app = FastAPI(title="Kaatclip", version=VERSION, docs_url=None, redoc_url=None)
    app.state.settings = settings
    app.state.engine = engine
    app.state.sessions = db.session_factory(engine)
    app.state.http = http or httpx.Client(timeout=20)
    app.state.google_certs = auth.GoogleCerts(app.state.http.get)
    app.state.bot = Bot(settings.telegram_bot_token, http=http) if settings.telegram_bot_token else None
    app.middleware("http")(csrf_guard)
    for module in (auth, admin, streams, uploads, clips, library, studio, brand, compilations, highlights, live, notifications,
                   youtube, posts, calendar, channel, account, legal):
        app.include_router(module.router)
    app.include_router(streams.worker_router)

    @app.get("/api/health")
    def health():
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"ok": True, "version": VERSION}

    # Last: the web app answers every path the API doesn't.
    web.mount(app, settings.web_dir)
    return app
