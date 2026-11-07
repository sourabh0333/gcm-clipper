"""Serves the built web app (web/dist) from the same address as the API, so cookies and the service worker
need no cross-site setup. Paths the app handles itself (/streams/x, /kept...) get index.html."""

from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

NOT_BUILT = """<!doctype html><meta name=viewport content="width=device-width"><title>Kaatclip</title>
<body style="font-family:system-ui;background:#0e0f13;color:#eee;padding:24px"><h1>Kaatclip</h1>
<p>The web app isn't built on this laptop yet. Run <code>npm install</code> and <code>npm run build</code> in
<code>ai-gcm/web</code>, then reload.</p></body>"""

RESERVED = ("api/", "auth/", "media/")


def mount(app, web_dir: Path):
    assets = web_dir / "assets"
    if assets.is_dir():
        # Hashed file names: safe to cache for a year.
        app.mount("/assets", StaticFiles(directory=assets), name="assets")
    router = APIRouter()

    @router.get("/{path:path}", include_in_schema=False)
    def page(path: str, request: Request):
        if path.startswith(RESERVED) or path in ("api", "auth", "media"):
            raise HTTPException(404, "Not found.")
        index = web_dir / "index.html"
        if not index.is_file():
            return HTMLResponse(NOT_BUILT, status_code=503)
        if path and "/" not in path:
            candidate = (web_dir / path).resolve()
            if candidate.parent == web_dir.resolve() and candidate.is_file():
                # The service worker and manifest must be re-checked on every visit.
                return FileResponse(candidate, headers={"Cache-Control": "no-cache"})
        return FileResponse(index, headers={"Cache-Control": "no-cache"})

    app.include_router(router)
