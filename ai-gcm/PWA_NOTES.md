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

## What the app can read from a job folder

| File | What it holds |
|---|---|
| `manifest.json` | `stages.<name>.status`: `done`, `running`, `failed` or `stale` (missing means pending), plus `seconds` or `error` |
| `settings.json` | Source URL, section, layout, number of clips |
| `info.json` | Video title, channel, duration, size (written after `ingest`) |
| `ranked.json` | Chosen clips, best first: `id`, `rank`, `start`, `end`, `type`, `final_score`, `reasons`, `players_left`, `events` |
| `clips.json` | Clip id to file name in `clips/` |

Stage order is in `aigcm.jobs.STAGES`. A job starts with `python -m aigcm run <url> --section <from>-<to>`; running the same command again resumes it.

## Demo jobs (`ai-gcm/demo/`)

| Job | State |
|---|---|
| `demo-finished` | All stages done, 4 placeholder clips (coloured cards, 18–28 s, with sound) |
| `demo-processing` | Ingest done, vision running |
| `demo-failed` | Ingest failed with a download error |

## Done

- 28 Oct: demo jobs, `AIGCM_JOBS_DIR` setting, these notes and `CLAUDE.md`.

## Next

1. Choose the server approach (keep dependencies small; the laptop already has Python 3.12).
2. Job list and "new job" screen.
3. Progress screen that polls `manifest.json`.
4. Swipe review with keep or reject, saved on the server so both devices see it.
5. Download and share (Web Share API on the phone).
6. Manifest and service worker so it installs on the phone's home screen.

## Not tested yet

- Nothing in the PWA exists yet.
