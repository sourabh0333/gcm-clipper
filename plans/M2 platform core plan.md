# M2 platform core: reviewed plan

Written 7 November 2026 before any M2 code, after reviewing the [master plan](GCM%20Clipper%20master%20plan.md) section M2, [the architecture](../docs/ARCHITECTURE.md), the old server and app, and the engine, with two research passes on the outside facts. Progress is tracked in [ai-gcm/BUILD_NOTES.md](../ai-gcm/BUILD_NOTES.md).

**M2 goal (from the master plan):** database and models, API, worker queue, Google sign-in, resumable and marker-window upload, Telegram bot, a new web app with jobs, progress and review, replacing the current server and PWA. **Done when** two creators can sign in, upload from a phone, and review their own streams, and the old app is retired.

---

## 1. What the review found

| # | Finding | Effect on M2 |
|---|---|---|
| R1 | **Google sign-in cannot work on the Wi-Fi address.** Redirect URIs must be HTTPS and may not be raw IP addresses; only localhost is exempt. | Phone tests need a stable public HTTPS address. Free choice: **Tailscale Funnel** (`https://<laptop>.<tailnet>.ts.net`, stable, no data cap, no warning page; free plan is "non-commercial", fine before the first sale; throughput unknown, so test a large upload early). Cloudflare quick tunnels change address every run; named tunnels need the domain; ngrok's free plan caps data at 1 GB a month. The Cloudflare named tunnel replaces Funnel when the domain is bought (M5). |
| R2 | **Sign-in-only scopes skip the tester list.** An app in "Testing" that asks only for `openid`, `email` and `profile` has no 100-user list, no warning screen and no 7-day expiry. | M2 asks for those three only. YouTube scopes come in M4 and bring the 100 testers and 7-day re-consent until Google's check passes (already planned). |
| R3 | **The old app imports YouTube links**, which the product must never do (D4, Developer Policies III.E.1). | The new API accepts uploads only. The command line keeps link import for the owner's engine tests on public streams; it is never exposed in the app. |
| R4 | **Most phone streaming apps keep no local recording.** Only PRISM Live probably saves a copy; Streamlabs mobile, Turnip and YouTube's own "Go live" were not shown to. PC and OBS streamers do record locally (OBS 30.2+ defaults to Hybrid MP4; older setups use MKV). | **Full upload from a PC is the main path.** Marker-window upload stays, but it cuts windows in the browser on a PC or phone that has the file, and is the last M2 step behind a go/no-go spike. Creators with no local file can download their own stream from YouTube Studio and upload it (to check: Studio's download for long streams). |
| R5 | **Uploads must fit the later Cloudflare limits**: 100 MB per request on the free plan and a 125 s timeout per request. | Resumable upload in **8 MB chunks** (a slow 1 Mbps uplink still finishes a chunk in about 64 s). tus protocol semantics on the server (create, HEAD for offset, PATCH with `Upload-Offset`), the maintained `tus-js-client` in the browser. |
| R6 | **Ingest copies the input into the job folder**, which would double an 8 GB upload on disk. | Uploads are written straight into the stream's job folder as `source.<ext>`; ingest skips the copy when the file is already there. Upload refused when free disk would fall under 20 GB. |
| R7 | **A stream made of marker pieces breaks the engine's assumptions**: a counter read across a join would invent kills, and clips must report stream time, not file time. | Pieces are joined with a stream copy plus a `pieces.json` map; the HUD scan resets its counters at each join; fight clusters never cross a join; all times are mapped back to the stream. |
| R8 | **Live markers need the recording's clock.** The Live screen records phone time; the recording starts a few seconds after "Go live". | A live session stores its start time; on upload the markers are placed relative to it, with a "shift markers" nudge. Windows are ±60–75 s, so a few seconds of drift is harmless. |
| R9 | **Anyone with the link could sign in and use the laptop.** | An **invite list** (`AIGCM_INVITES`, emails) during M2–M7; the owner's email is admin. |
| R10 | **Two processes write one SQLite file** (API and worker). | WAL mode, `synchronous=NORMAL`, 15 s busy timeout, write transactions started with `BEGIN IMMEDIATE`; the worker claims a job with one `UPDATE … WHERE id=(SELECT …) AND status='queued' RETURNING`. Python's SQLite here is 3.49.1, so `RETURNING` works. |
| R11 | **Two sources of truth.** The engine writes `manifest.json`, `ranked.json`, `decisions.json`. | The engine stays file-based and usable alone. The database owns accounts, ownership, the queue, clips and decisions; stage progress is read from the manifest. On success the worker copies `ranked.json` and `clips.json` into the clips table once. Decisions live only in the database (the old `decisions.json` is imported once). |
| R12 | **Tooling versions.** React Router 8 needs Node 22.22+ (the laptop has 22.17.1); TypeScript 7 is the new Go compiler with no stable API yet. | Pin **react-router 7.18.4** and **TypeScript 6.0.3**. Everything else at the newest release that is at least two weeks old (section 4). |
| R13 | **The phone session can't install the engine's heavy models.** | API and worker code must not import the engine's heavy modules at import time; API dependencies go in their own `requirements-api.txt`, so the phone session can run the API tests and the web app against the demo jobs. |

---

## 2. Decisions taken in this review

- **Sign-in:** Google authorization-code flow with PKCE, `state` and `nonce`, written with `httpx`; the ID token verified with `google-auth` (certificates cached). No Authlib, no signed-cookie sessions: a random session id in an HttpOnly, Secure, SameSite=Lax cookie, looked up in a `sessions` table, 30 days sliding. A "dev sign-in" exists only when `AIGCM_DEV_LOGIN=1` and the request comes to `localhost` with no tunnel headers, for tests and laptop development.
- **Upload:** tus semantics, own server code (about 150 lines), `tus-js-client` 4.3.1, 8 MB chunks, up to 10 GB, MP4, MKV or MOV, checked with ffprobe when complete.
- **Worker:** `python -m aigcm worker`, one job at a time, runs the pipeline as a child process (as the old server does, so a crash or Stop can't take the worker down), heartbeat in the database, re-queues jobs left running after a crash (they resume from checkpoints).
- **Web app:** React 19 + TypeScript + Vite in `ai-gcm/web/`, React Router 7, Vitest; a hand-written service worker (no PWA plugin); the built files served by FastAPI, later by Cloudflare Pages.
- **Marker windows in the browser:** Mediabunny's low-level packet copy (reads only the needed bytes, MP4/MOV/MKV, no re-encode). ffmpeg.wasm is the fallback (30 MB download, 2 GB limit without WORKERFS); mp4box.js is out (no writer, keeps media in memory when the index is at the end).
- **Telegram:** long polling (`getUpdates`) from the worker, no public webhook needed; linking by `t.me/<bot>?start=<one-time token>` (up to 64 characters of `A–Z a–z 0–9 _ -`); about one message a second per chat is the limit, far above our needs.

---

## 3. Steps

Each step ends with tests green, notes updated, and a commit to `main`.

| Step | What | Done when |
|---|---|---|
| **M2.1 Foundation** | `requirements-api.txt`; settings from `.env`; SQLAlchemy models (`users`, `sessions`, `invites`, `streams`, `uploads`, `clips`, `live_sessions`, `markers`, `telegram_links`, `audit_log`); Alembic migration; SQLite pragmas; FastAPI app in `aigcm/api/` with `/api/health`; `python -m aigcm api` | A fresh database is created by the migration; the API answers on localhost; tests pass without the engine's models installed |
| **M2.2 Sign-in** | Google code flow with PKCE, invite list, sessions, sign-out, `/api/me`, dev sign-in for localhost; owner-only admin flag; per-user data access helper used by every query | Mocked Google flow test passes; a second user gets 404 on the first user's streams and media; real Google sign-in tested on localhost once the OAuth client exists |
| **M2.3 Upload and streams** | tus create/HEAD/PATCH/DELETE, 8 MB chunks, size and disk guard, ffprobe check; stream rows with title, game, recorded date; upload lands in the job folder; engine ingest skips the copy | An upload interrupted halfway resumes and queues the stream; the engine ingests the file without copying it |
| **M2.4 Worker** | Claim, child-process run, Stop, crash re-queue, heartbeat, progress from the manifest, clip import on success, error on failure | A real uploaded section runs end to end through the worker; killing the worker mid-scan and restarting it resumes from the checkpoint |
| **M2.5 Review API and migration** | Clips with reason, labels, titles, flags; media by clip id with access check and Range; decisions with reason and undo; kept list and downloads; `aigcm import-jobs --owner <email>` for the existing jobs and their `decisions.json` | The owner's existing jobs and swipes appear under their account; another account sees none |
| **M2.6 Web app** | Sign-in, streams list, new stream with upload progress and resume, progress screen, swipe review (keep, reject, undo, reasons, sound, keys), kept clips (download, share), Live marker screen, settings (Telegram, sign out); installable PWA | Every old-app feature works in the new app in Chrome on Android over the Funnel address; it installs to the home screen |
| **M2.7 Telegram** | Bot link, "clips ready" with a link, "job failed", owner alerts for worker offline and low disk | A real message reaches the owner's phone for a finished job |
| **M2.8 Marker-window upload** | Spike first: on a mid-range Android phone with a 4 GB OBS file, cut 3 windows in under a minute. Then live sessions and markers, browser cutting with Mediabunny, pieces uploaded into one stream, engine support for pieces (R7). If the phone part fails the gate, windows are cut on the PC page only and phones use full upload | A 15-marker stream uploads about an hour of pieces and its clips land on the markers |
| **M2.9 Go live and retire the old app** | Funnel address, Google OAuth client, two real accounts on two phones; delete `server.py` and `app/`; `serve` starts the new API; `PWA_NOTES.md` archived | The master plan's M2 "done when" is met |

**Order and risk:** the large-upload throughput over Funnel is tested as soon as M2.3 works (a 2 GB file), because it decides whether Funnel is good enough for the beta. M2.8 is last because it has the most unknowns and the least evidence of need (R4).

---

## 4. Versions (newest release at least two weeks old, checked 7 Nov 2026)

| Python | Version | npm | Version |
|---|---|---|---|
| fastapi | 0.162.0 | react, react-dom | 19.3.1 |
| uvicorn | 0.54.0 | vite | 8.3.5 |
| sqlalchemy | 2.1.6 | @vitejs/plugin-react | 6.1.2 |
| alembic | 1.20.1 | typescript | 6.0.3 (not 7: no stable API yet) |
| python-multipart | 0.0.32 | react-router | 7.18.4 (8 needs Node 22.22+) |
| httpx | 0.28.1 | vitest | 5.0.5 |
| google-auth | 2.62.0 | @testing-library/react | 16.3.3 |
| cryptography | 50.0.2 (installed) | tus-js-client | 4.3.1 |
| | | mediabunny | 1.62.1 (M2.8 only) |

---

## 5. What the owner does for M2 (all free, only when the step needs it)

| Step | Task | Claude prepares |
|---|---|---|
| M2.2 | Create a Google Cloud project "Kaatclip" and a web OAuth client; consent screen with app name, support email, scopes `openid email profile` only; add `http://localhost:8765/auth/google/callback` and later the Funnel address as redirect URIs; paste the client id and secret into `ai-gcm/.env` | Exact click path and every field's text; can be done together in the browser with your OK |
| M2.6 | Install Tailscale on the laptop, sign in, and turn on Funnel for port 8765 | The commands and a check script |
| M2.7 | Create the bot with @BotFather (name "Kaatclip", username like `kaatclip_bot`) and paste the token into `.env` | The bot's description and commands |
| M2.9 | One more person (or a second Google account) signs in from another phone for the two-creator test | The test checklist |

---

## 6. Changes to the master plan from this review

- Marker-window upload is no longer the main mobile-data path (R4); full upload from the PC is. The M2 "done when" keeps "upload from a phone", which full upload over Funnel covers.
- Phone testing during M2 uses Tailscale Funnel; the domain and Cloudflare named tunnel stay in M5.
- M2 sign-in asks for name and email only; YouTube scopes stay in M4.
- Pinned tool versions as above; Node upgrade to 22.22+ only if React Router 8 is ever needed.
