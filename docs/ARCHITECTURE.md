# GCM Clipper architecture

How the full app is put together. Decided 4 November 2026 for the full build in [the app plan](../plans/GCM%20Clipper%20sellable%20app%20plan.md). The goal is near-zero running cost at launch, the laptop as the first server, and a clean path to a cloud server later without rewriting.

## Parts

```
 creator's phone / laptop browser
        │  HTTPS (Cloudflare Tunnel to the laptop; static files from Cloudflare Pages later)
        ▼
 ┌──────────────┐   reads/writes   ┌───────────────┐
 │  API server   │ ───────────────▶ │   database     │  SQLite on the laptop, Postgres later
 │  (Python)     │                  └───────────────┘
 └──────┬───────┘                          ▲
        │ queues jobs                       │ job status, clips, posts
        ▼                                   │
 ┌──────────────┐  ffmpeg, OCR, Whisper,  ┌───────────────┐
 │  worker       │  YAMNet, Gemini ───────▶│  media storage │  local disk, Cloudflare R2 later
 │  (pipeline)   │                         └───────────────┘
 └──────────────┘
        │ scheduled uploads, analytics
        ▼
   YouTube Data API / Analytics API (creator's own channel, via Google sign-in)
```

| Part | Choice | Why |
|---|---|---|
| **Engine** | The existing `aigcm` Python package (stages: ingest, vision, audio, sounds, transcript, moments, judge, captions, render) | Already works on real streams; keep extending it |
| **API server** | Python, FastAPI | Same language as the engine; typed request/response models; easy to test |
| **Worker** | A separate Python process that takes jobs from the database queue one at a time | A crash in a 3-hour job can't take the website down; a second worker (cloud GPU) can be added later |
| **Database** | SQLAlchemy models with SQLite at first, Alembic migrations | Free and zero-setup on the laptop; the same models run on Postgres when moving to the cloud |
| **Sign-in** | **Google sign-in only** at launch (OpenID Connect), with the YouTube permission asked separately when the creator connects their channel | Every YouTuber has a Google account; phone OTP needs a paid SMS service, so it waits |
| **Sessions** | Secure, HTTP-only cookies holding a signed session id | No tokens in the browser's storage |
| **YouTube access** | OAuth refresh tokens, encrypted at rest, used only for approved uploads, scheduling and reading the channel's own analytics; deleted on disconnect | Google's user data rules |
| **Web app** | React + TypeScript + Vite, installable PWA, mobile-first | The studio (timeline, calendar, editor) needs real components; works from the phone session too (`npm` is available there) |
| **Editing** | Each clip is an **edit list** (cuts, layout, zoom, captions, text, brand kit) stored in the database. The browser previews it with the source video and CSS; the worker renders the final MP4 with ffmpeg | Edits are instant and undoable; only exports cost CPU |
| **Media** | Per-job folders on the laptop disk (`ai-gcm/jobs/`); sources kept for 14 days for re-editing, then deleted; finished clips kept 30 days | Disk stays bounded; cloud storage (R2) later behind the same interface |
| **Payments** | Razorpay Subscriptions (UPI AutoPay), webhook updates the plan in the database | Indian creators pay by UPI |
| **AI** | Gemini (paid tier with a spending cap for customer data), local models for speech, sounds and OCR | Cheap and private enough |

## Rules

- **The engine stays usable on its own** (`python -m aigcm run …`), and keeps its tests. The API and worker call into it; they don't copy its logic.
- **Every long step can resume** after a crash or power cut, from a checkpoint, not from the start.
- **No creator passwords, ever.** Only Google sign-in.
- **Nothing is posted without the creator's approval.**
- **Free tiers first**; anything that costs money is behind a setting and a cap.
- **Tests for every module**; a real-stream check before calling a pipeline change done.

## Folder layout (target)

```
ai-gcm/
  aigcm/            engine (pipeline stages) — exists
  aigcm/api/        FastAPI app: auth, jobs, clips, edits, calendar, posts, billing
  aigcm/worker.py   job runner
  aigcm/db/         SQLAlchemy models and migrations
  web/              React app (replaces app/ when it reaches the same features)
  tests/
docs/ARCHITECTURE.md
```

The current stdlib server (`aigcm/server.py`) and plain-JS PWA (`app/`) keep working until the new API and web app replace them.
