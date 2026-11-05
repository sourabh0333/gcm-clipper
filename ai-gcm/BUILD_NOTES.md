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
| 1 | Full-length streams: resume after crash, bounded disk | **Done.** The full 3.1-hour GtxPreet stream (`jobs/vHLz6WDqJkk_full`, 2.7 GB) ran end to end on 5 Nov with no manual fixes: 59 kills, 1 chicken dinner, 8 accolades, 12 clips. The run was stopped once mid-way (to change thread limits) and resumed from the checkpoints. Two more full streams still to run for the "three streams" gate |
| 2 | Speed: 3-hour stream in about 1 hour | **Close.** Measured on the 3.1-hour stream: download 8 min; HUD scan about 36 min (1 fps, 0.19× realtime); transcript 77 min; sounds 3 min; judge 7 min (Gemini busy-retries); render 4 min. Vision and the transcript run side by side with half the threads each, so analysis took about 70 min and the whole job about 85 min. **The transcript is the bottleneck**: 0.2× realtime alone, 0.5–0.75× while vision runs. Next idea: skip transcription of stretches the sound detector marks as no speech |
| 3 | Accuracy on 10 more streams, knock detection, bigger speech model fallback | **Bigger model dropped.** The Apex (large-v3-turbo) conversion ran at 19× realtime on the laptop and produced garbage ("nan nan nan"), so it was removed. The code path stays: a transcript covering under half of the detected speech (ANJI 0.14; good streams 0.83–0.84) is marked `broken`, and the chosen clips' windows are redone with a bigger model if one is ever installed in `models/` (`transcript.retranscribe_windows`). For ANJI-type noisy streams the realistic fix later is a paid API (Sarvam, about ₹30 per hour of speech). 10-stream test and knock detection not started |
| 3a | Moment markers | **Done (file-based).** `markers.json` in the job folder (`{"t", "source": button/chat/voice, "by"}`); spoken "clip that / clip karo" found in the transcript; repeats within 5 s fold into one; a marked moment is always a clip and outranks a two-kill fight |
| 6 | Post-ready output and brand-safe check | **Done.** `titles.py` (stat / Hinglish punchline / suspense, ≤45 chars, one emoji, series counter, hashtags by channel size, description with stream link and Krafton line), `safety.py` (gaali in Latin and Devanagari across word boundaries, slurs, betting, other games, title overclaims), bleeped "sponsor-safe" export with `--sponsor-safe`. `package.decorate` fills `titles`, `title`, `hashtags`, `description`, `flags`, `mute_spans`, `sponsor_safe` on every ranked clip |
| 7 | Clip labels and "why this clip" | **Done.** Every clip has `labels` (type, game, kills, knocks, win, marked, talk, players_left, length) and `why` ("2 kills by the streamer at 1:12:40") |
| 4, 5, 8 | Upload, edit model, delivery | M2/M3 |

## Done

- 4 Nov: architecture (`docs/ARCHITECTURE.md`). Vision and transcript checkpoints; cleanup command.
- 5 Nov: markers, labels, why, titles, safety and bleep, parallel analysis stages, 1 fps HUD reads. 50 tests pass.

## Measurements

- 10-min landscape cut, 2 fps HUD: 349 s (0.58× realtime), 3 kills. **At 1 fps: 185 s (0.31×), same 3 kills** (first kill timestamp moved by 3 s, well inside the 12 s lead-in).
- Full 3.1-hour stream, 5 Nov: see step 2 above. Titles on the 12 clips read like the top Shorts style after the fix (stat first for fights: "DOUBLE FINISH 💀", "4 FINISHES 1 FIGHT 🔥", "CHICKEN DINNER 1 FINISH LAST ZONE 🏆"; the judge's Hinglish line second). Gaali detector found 18 spoken gaali in the 3.1 h (gand, kutte, randi, saala); none fell inside the 12 clips, so 0 flags.
- Gemini's free tier returned 503 "high demand" repeatedly during the judge; the talk scan now retries like the judge does. Change-detection on the counter crop was tried and dropped: the box sits over moving gameplay, so the pixels change every frame and OCR still ran on 1,133 of 1,200 frames.
- Digit recognition: about 27 ms per crop at the padded 320-wide input. A narrower input is 15 ms but misreads some digits ("2" → "28"), so it was not adopted.
- Full stream download (3.1 h, 720p): 8 min.

## Next

1. Transcript speed: skip stretches with no detected speech (the sound detector already knows), and measure Apex on ANJI (running).
2. Two more full streams end to end (different streamers) for the step 1 gate.
3. Step 3: download 10 more streams, label 5 by hand, measure recall, add knock detection from the kill feed.
4. Then M2: database, API, worker, Google sign-in, upload, new web app.

## Not tested yet

- `--sponsor-safe` export on a real clip with gaali (no clip in the full run had any; the filter is unit-tested).
- After `cleanup`, re-editing a clip needs the source again: the editor (step 5) must re-ingest or say the source is gone.
