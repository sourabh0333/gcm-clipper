# PWA progress notes

Shared notes between the laptop and phone sessions. Update before every push (see `CLAUDE.md`).

**Branch to merge first:** none

## Goal

A mobile-first web app over the existing pipeline, installable on a phone as a PWA:

1. Paste a YouTube link (and optionally a time range) to start a job.
2. Watch the job's progress, stage by stage.
3. Swipe through the finished clips to keep or reject each one.
4. Download or share the kept clips.

## Decisions so far

- PWA, not a native app (28 Oct). Costs ₹0.
- The server runs on the laptop, because the pipeline needs its CPU, ffmpeg and models. The phone reaches it on home Wi-Fi first; a free Cloudflare Tunnel can come later for use outside home.
- Build on the job folders the pipeline already writes. The app reads them; it does not change how the pipeline stores things.
- Server: Python standard library only (`aigcm/server.py`, started with `python -m aigcm serve`). App: plain HTML, CSS and JS modules in `app/`, no build step, so the phone session can edit it too.
- One job runs at a time, as a `python -m aigcm run` child process logging to the job's `run.log`. Only jobs started by the running server count as "running"; anything else left half done shows as "stopped" with a Resume button.
- Keep or reject decisions are saved on the laptop in the job's `decisions.json`, so the phone and laptop see the same review.

## How it fits together

| Piece | Where |
|---|---|
| Server, API, clip streaming (Range requests) | `aigcm/server.py` |
| Screens: job list and new job, progress, swipe review, kept clips | `app/app.js`, `app/style.css`, `app/index.html` |
| Install and offline shell | `app/manifest.webmanifest`, `app/sw.js`, `app/icon-*.png` |
| Tests | `tests/test_server.py` (runs against a copy of the demo jobs) |

API: `GET /api/jobs`, `GET /api/jobs/<job>`, `POST /api/jobs {url, section}`, `POST /api/jobs/<job>/resume`, `POST /api/jobs/<job>/stop`, `POST /api/jobs/<job>/decisions {id, verdict: keep|reject|null}`, `GET /media/<job>/<clip file>[?download=1]`.

## What the app reads from a job folder

| File | What it holds |
|---|---|
| `manifest.json` | `stages.<name>.status`: `done`, `running`, `failed` or `stale` (missing means pending), plus `seconds`, `started` or `error` |
| `settings.json` | Source URL, section, layout, number of clips |
| `info.json` | Video title, channel, duration, size (written after `ingest`) |
| `ranked.json` | Chosen clips, best first: `id`, `rank`, `start`, `end` (from the start of the section), `type`, `final_score`, `reasons`, `players_left`, `events` |
| `clips.json` | Clip id to file name in `clips/` |
| `decisions.json` | Written by the app: clip id to `{verdict, reason, at}` |
| `run.log` | Written by the app: the pipeline's output; the last line shows on the progress screen, and "N min scanned" lines drive the bar during vision |

## Demo jobs (`ai-gcm/demo/`)

| Job | State |
|---|---|
| `demo-finished` | All stages done, 4 placeholder clips (coloured cards, 18–28 s, with sound) |
| `demo-processing` | Ingest done, vision left "running" (shows as stopped) |
| `demo-failed` | Ingest failed with a download error |

Run against them with `AIGCM_JOBS_DIR=demo`. To avoid writing decisions into the committed demo folder while testing, copy it somewhere and point `AIGCM_JOBS_DIR` at the copy (an absolute path works).

## Done

- 28 Oct: demo jobs, `AIGCM_JOBS_DIR` setting, these notes and `CLAUDE.md`.
- 28 Oct: first working app. Job list and new-job form, progress screen with stage list, rough percentage, last log line, Stop and Resume, failed-step errors; swipe review with keep, reject, undo, tap to pause, sound toggle and arrow keys; kept clips with Download (and Share where the browser allows it); manifest, service worker and icons. Clip reasons now read "2 kills by the streamer" instead of "0 knocks and 2 kills".

## Tested

- In the desktop app's browser against copies of the demo jobs: all screens, swipe left, keep and undo buttons, finish screen, kept clips, a Range request with download, the service worker installing.
- Starting a job through the app: it launched the real pipeline, YouTube rejected the made-up demo video, and the progress screen showed the real error. Bad links get a clear message; a second job is refused while one runs.
- 28 Oct: the owner opened it on their phone over home Wi-Fi (`http://192.168.1.100:8765`) and it worked with the 3 real test jobs. The laptop's firewall already allows Python 3.12 on private networks.
- `tests/test_server.py`: states, decisions and undo, Range streaming, refusing bad links and path tricks, app files.

## Not tested yet

- A full real stream through the app, including the progress bar during vision and the Stop button (`taskkill` on Windows).
- Share: needs HTTPS (or localhost), so it won't show over the plain Wi-Fi address.
- Installing to the home screen: also needs HTTPS.

## Next

1. Run one real stream through the app on the laptop and fix what shows up.
2. HTTPS for use outside home and for install and share: Cloudflare quick tunnel (`cloudflared tunnel --url http://localhost:8765`, free, no account), plus a simple PIN on the server first, because anyone with the tunnel address could start jobs.
3. Show an estimated time left, using the stage times from earlier jobs.
4. Better titles for jobs that failed before download (now the raw link).
