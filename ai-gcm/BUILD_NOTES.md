# Full app build notes

Progress on building the complete GCM Clipper app, milestone by milestone from [the master plan](../plans/GCM%20Clipper%20master%20plan.md), with the technical setup in [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md). Update before every push (see `CLAUDE.md`).

**Branch to merge first:** none

## Decisions (owner, 4 Nov 2026)

- Build the **full** app, all phases, before contacting streamers; money can come slowly.
- Own brand, not Cevrynt; the seller is the owner as a sole proprietor for now.
- YouTube first; Instagram optional after launch.
- Spend nothing until it earns; free tiers and the laptop.
- Prices ₹499 / ₹999, an editor tier about ₹2,499 after launch, ₹99 first month.

## Status by plan step

| Step | What | Status |
|---|---|---|
| 1 | Full-length streams: resume after crash, bounded disk | **In progress.** Vision and transcript resume from checkpoints (every 5 min of video / every 5-min chunk); `aigcm cleanup` deletes sources 14 days after clips are made. Not yet run on a full 3–5 hour stream |
| 2 | Speed | Not started |
| 3, 3a | Accuracy on 10 more streams; moment markers | Not started |
| 4 | File upload | Not started |
| 5 | Edit data model | Not started |
| 6 | Post-ready output and brand-safe check | Not started |
| 7 | Clip labels | Partly (clip type, game, score already saved in `ranked.json`) |
| 8 | Delivery (zip, share) | Partly (single-clip download and share in `app/`) |
| S1–S9 | Content studio | Not started |
| 9–17 | Service: domain, hosting, Google sign-in, queue, storage, payments, limits, notifications | Not started |
| 18–24 | YouTube posting after approval | Not started |
| 25–31 | Trust and launch | Not started |

## Done

- 4 Nov: architecture decided (`docs/ARCHITECTURE.md`): FastAPI API, a separate worker, SQLAlchemy with SQLite first, Google sign-in only at launch (phone OTP needs a paid SMS service), React + TypeScript web app, edit lists rendered by ffmpeg.
- 4 Nov: step 1, first part. `vision.scan(..., checkpoint)` saves counters, events and position to `vision.partial.json`; `transcript.transcribe(..., checkpoint)` saves finished chunks to `transcript.partial.json`; both are removed when the stage finishes. `python -m aigcm cleanup [--days N] [--dry-run]`.

## Next

1. Finish step 1: run one full 3–5 hour stream end to end, kill it once during vision and once during the transcript, and confirm it resumes.
2. Step 2 (speed): run vision, sounds and transcript in parallel; read the HUD less often during quiet stretches.

## Not tested yet

- Vision resume checked on a real 10-minute cut (4 Nov): the scan was killed at 5 min and resumed; same 3 kills, 130 s instead of 349 s.
- After `cleanup`, re-editing a clip needs the source again: the editor (step 5) must re-ingest or say the source is gone.
