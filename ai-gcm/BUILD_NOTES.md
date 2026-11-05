# Full app build notes

Progress on building the complete GCM Clipper app, milestone by milestone from [the master plan](../plans/GCM%20Clipper%20master%20plan.md), with the technical setup in [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md). Update before every push (see `CLAUDE.md`).

**Branch to merge first:** none

## Decisions (owner, 4–5 Nov 2026)

- Build the **full** app, all phases, before contacting streamers; money can come slowly.
- Own brand, not Cevrynt; the seller is the owner as a sole proprietor for now. Product name still open (D0).
- YouTube first; Instagram optional after launch. **Upload only**, no YouTube link import (YouTube's developer policies).
- Spend nothing until it earns; free tiers and the laptop.
- Prices ₹99 first month, ₹499 / ₹999, ₹49–99 per stream, editor tier about ₹2,499 after launch.

## Milestone M1: engine product-grade (in progress)

| Step | What | Status |
|---|---|---|
| 1 | Full-length streams: resume after crash, bounded disk | Resume done and checked on a real cut. `aigcm cleanup` done. Full 3.1-hour stream (`jobs/vHLz6WDqJkk_full`, GtxPreet, 2.7 GB) downloaded in 8 min; the end-to-end run is next |
| 2 | Speed: 3-hour stream in about 1 hour | **In progress.** Vision now runs alongside audio, sounds and transcript (`Job.run_parallel`). HUD reads at 1 fps instead of 2 (the reset hold is time-based, 10 s); banner text is read at most every 3 s. Being timed on the 10-minute cut (baseline 349 s = 0.58× realtime at 2 fps) |
| 3 | Accuracy on 10 more streams, knock detection, bigger speech model fallback | Not started |
| 3a | Moment markers | **Done (file-based).** `markers.json` in the job folder (`{"t", "source": button/chat/voice, "by"}`); spoken "clip that / clip karo" found in the transcript; repeats within 5 s fold into one; a marked moment is always a clip and outranks a two-kill fight |
| 6 | Post-ready output and brand-safe check | **Done.** `titles.py` (stat / Hinglish punchline / suspense, ≤45 chars, one emoji, series counter, hashtags by channel size, description with stream link and Krafton line), `safety.py` (gaali in Latin and Devanagari across word boundaries, slurs, betting, other games, title overclaims), bleeped "sponsor-safe" export with `--sponsor-safe`. `package.decorate` fills `titles`, `title`, `hashtags`, `description`, `flags`, `mute_spans`, `sponsor_safe` on every ranked clip |
| 7 | Clip labels and "why this clip" | **Done.** Every clip has `labels` (type, game, kills, knocks, win, marked, talk, players_left, length) and `why` ("2 kills by the streamer at 1:12:40") |
| 4, 5, 8 | Upload, edit model, delivery | M2/M3 |

## Done

- 4 Nov: architecture (`docs/ARCHITECTURE.md`). Vision and transcript checkpoints; cleanup command.
- 5 Nov: markers, labels, why, titles, safety and bleep, parallel analysis stages, 1 fps HUD reads. 50 tests pass.

## Measurements

- 10-min landscape cut, 2 fps HUD: 349 s (0.58× realtime), 3 kills. Change-detection on the counter crop was tried and dropped: the box sits over moving gameplay, so the pixels change every frame and OCR still ran on 1,133 of 1,200 frames.
- Digit recognition: about 27 ms per crop at the padded 320-wide input. A narrower input is 15 ms but misreads some digits ("2" → "28"), so it was not adopted.
- Full stream download (3.1 h, 720p): 8 min.

## Next

1. Read the 1 fps timing on the cut; then run the full 3.1-hour stream end to end with the parallel stages and record the total time per stage.
2. Kill the full run once during vision and once during the transcript and confirm both resume.
3. Step 3: download 10 more streams (mix of layouts and games later), label 5 by hand, measure recall, add knock detection from the kill feed, and the Apex speech model fallback when a transcript looks broken.
4. Then M2: database, API, worker, Google sign-in, upload, new web app.

## Not tested yet

- The parallel stages on a real job (unit-tested only); CPU contention between OCR and Whisper may cut the gain.
- `--sponsor-safe` export on a real clip with gaali (unit-tested filter only).
- After `cleanup`, re-editing a clip needs the source again: the editor (step 5) must re-ingest or say the source is gone.
