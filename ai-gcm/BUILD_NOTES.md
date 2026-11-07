# Full app build notes

Progress on building the complete GCM Clipper app, milestone by milestone from [the master plan](../plans/GCM%20Clipper%20master%20plan.md), with the technical setup in [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md). Update before every push (see `CLAUDE.md`).

**Branch to merge first:** none

## Decisions (owner, 4–5 Nov 2026)

- Build the **full** app, all phases, before contacting streamers; money can come slowly.
- Own brand, not Cevrynt; the seller is the owner as a sole proprietor for now. **Product name: Kaatclip** (D0, chosen 6 Nov after the naming study in `reports/Product name research.md`; domains and YouTube handle were free, to be registered by the owner).
- YouTube first; Instagram optional after launch. **Upload only**, no YouTube link import (YouTube's developer policies).
- Spend nothing until it earns; free tiers and the laptop.
- Prices ₹99 first month, ₹499 / ₹999, ₹49–99 per stream, editor tier about ₹2,499 after launch.

## Milestone M1: engine product-grade (in progress)

| Step | What | Status |
|---|---|---|
| 1 | Full-length streams: resume after crash, bounded disk | **Done: 3 of 3 streams.** GtxPreet 3.1 h (`jobs/vHLz6WDqJkk_full`, landscape): 59 kills, 1 chicken dinner, 12 clips, about 55 min with the final code. DIPENDU 2.06 h (`jobs/Pylusnav-1Q_full`, vertical): 21 kills over 3 matches, **78 min** (vision 47 min = 0.38× realtime: vertical layouts do a whole-frame "Spectating" read). ANJI 2.15 h (`jobs/utvX-jHSFi8_full`, vertical, noisy): 20 kills over 6 matches, **67 min** (vision 21 min, transcript 15 min with coverage 0.23 flagged as broken, judge 22 min of mostly Gemini busy-retries). All three with no manual fixes |
| 2 | Speed: 3-hour stream in about 1 hour | **Done for the transcript; the whole job is now bounded by the 36-min HUD scan.** On the 3.1-hour stream: download 8 min; HUD scan about 36 min (1 fps, 0.19× realtime); sounds 3 min; **transcript 18 min** (was 77: faster-whisper's batched pipeline driven by the sound detector's speech spans); judge 7 min (Gemini busy-retries); render 4 min. Vision and the transcript run side by side with half the threads each. Expected whole job: about 55 min |
| 3 | Accuracy on 10 more streams, knock detection, bigger speech model fallback | **10-stream set done (see below): all layouts handled, kills plausible, recall awaits the owner's swipes. Knock detection built from the kill feed (6 Nov evening, see below), best-effort by layout.** Bigger model dropped. The Apex (large-v3-turbo) conversion ran at 19× realtime on the laptop and produced garbage ("nan nan nan"), so it was removed. The code path stays: a transcript covering under half of the detected speech (ANJI 0.14; good streams 0.83–0.84) is marked `broken`, and the chosen clips' windows are redone with a bigger model if one is ever installed in `models/` (`transcript.retranscribe_windows`). For ANJI-type noisy streams the realistic fix later is a paid API (Sarvam, about ₹30 per hour of speech). Knock detection: see "Kill feed and knocks" |
| 3a | Moment markers | **Done (file-based).** `markers.json` in the job folder (`{"t", "source": button/chat/voice, "by"}`); spoken "clip that / clip karo" found in the transcript; repeats within 5 s fold into one; a marked moment is always a clip and outranks a two-kill fight |
| 6 | Post-ready output and brand-safe check | **Done.** `titles.py` (stat / Hinglish punchline / suspense, ≤45 chars, one emoji, series counter, hashtags by channel size, description with stream link and Krafton line), `safety.py` (gaali in Latin and Devanagari across word boundaries, slurs, betting, other games, title overclaims), bleeped "sponsor-safe" export with `--sponsor-safe`. `package.decorate` fills `titles`, `title`, `hashtags`, `description`, `flags`, `mute_spans`, `sponsor_safe` on every ranked clip |
| 7 | Clip labels and "why this clip" | **Done.** Every clip has `labels` (type, game, kills, knocks, win, marked, talk, players_left, length) and `why` ("2 kills by the streamer at 1:12:40") |
| 4, 5, 8 | Upload, edit model, delivery | M2/M3 |

## Milestone M2: platform core (started 7 Nov)

Reviewed before any code: [plans/M2 platform core plan.md](../plans/M2%20platform%20core%20plan.md) (13 findings, decisions, steps M2.1–M2.9, owner tasks). M1 stays open only for what the owner's swipes decide (recall figure, transcript threshold).

| Step | Status |
|---|---|
| M2.1 Foundation | In progress |
| M2.2 Sign-in | — |
| M2.3 Upload and streams | — |
| M2.4 Worker | — |
| M2.5 Review API and migration | — |
| M2.6 Web app | — |
| M2.7 Telegram | — |
| M2.8 Marker-window upload | — |
| M2.9 Go live, retire old app | — |

## Done

- 4 Nov: architecture (`docs/ARCHITECTURE.md`). Vision and transcript checkpoints; cleanup command.
- 5 Nov: markers, labels, why, titles, safety and bleep, parallel analysis stages, 1 fps HUD reads. 50 tests pass.
- 6 Nov: accuracy set of ten 30-min sections complete (icon HUD, 1080 vertical sources, 24-frame search). Vertical Spectating check rebuilt (stroke template match, undo window, overlapping-box guard, 40-player lobbies), counter boxes anchored on digits, four-read rule for big kill jumps. 62 tests pass.

## Measurements

- 10-min landscape cut, 2 fps HUD: 349 s (0.58× realtime), 3 kills. **At 1 fps: 185 s (0.31×), same 3 kills** (first kill timestamp moved by 3 s, well inside the 12 s lead-in).
- Full 3.1-hour stream, 5 Nov: see step 2 above. Titles on the 12 clips read like the top Shorts style after the fix (stat first for fights: "DOUBLE FINISH 💀", "4 FINISHES 1 FIGHT 🔥", "CHICKEN DINNER 1 FINISH LAST ZONE 🏆"; the judge's Hinglish line second). Gaali detector found 18 spoken gaali in the 3.1 h (gand, kutte, randi, saala); none fell inside the 12 clips, so 0 flags.
- Gemini's free tier returned 503 "high demand" repeatedly during the judge; the talk scan now retries like the judge does.
- **Transcript methods on the full 3.1-hour stream** (coverage = share of detected-speech seconds that have a transcribed word): plain pipeline 69 min, 21,573 words, 0.86; batched pipeline with its own speech detector 12 min, 17,561 words, 0.70; **batched driven by YAMNet speech spans 18 min, 17,753 words, 0.73 (adopted)**. The quality filter (compression, log-probability) is not the cause of the gap; the batched pipeline simply finds fewer words. So the chosen clips (about 6 minutes of audio) are re-read with the plain pipeline after judging, for captions and the safety check.
- **Apex (large-v3-turbo Hinglish) on the laptop:** 19× realtime and garbage output ("nan nan nan") after int8 conversion. Removed. For noisy streams like ANJI, the realistic later fix is a paid API. Change-detection on the counter crop was tried and dropped: the box sits over moving gameplay, so the pixels change every frame and OCR still ran on 1,133 of 1,200 frames.
- Digit recognition: about 27 ms per crop at the padded 320-wide input. A narrower input is 15 ms but misreads some digits ("2" → "28"), so it was not adopted.
- Full stream download (3.1 h, 720p): 8 min.

- **Full job rebuilt on the new transcript (5 Nov, 14:22):** moments 7.5 min (Gemini read the whole transcript this time; the first run had hit a 503), judge 11 min including the 12-clip plain re-read, render 6 min. With Gemini's talk scan working, 8 of the top 12 are talk clips (funny, banter, rage) and the 4-kill fight sits at #6, the chicken dinner at #9. Whether that balance is right is for the owner's swipes to decide (talk weight is `TALK_WEIGHT_GEMINI`). Two clips carried spoken gaali ("saala") and got sponsor-safe copies (`*_safe.mp4`) with the word muted.

## Accuracy set (step 3)

Ten 30-minute sections chosen for variety (`jobs/acc_*`): LoLzZz (big creator, landscape, compact icon HUD), YouTube SULTHAN (facecam, vertical), im_Trex (small, facecam, vertical), Aashi (vertical), Bixi OP (handcam, pro, landscape), Beast (vertical), SHLOK (solo vs squad, landscape), PABLO (Telugu and Hindi, vertical), Zx_Rajput (small, Hindi, vertical), NesaMani (Tamil). GoDsBrOtHeR and ESWAR were dropped: both streams had just ended (`post_live`) and YouTube only serves DASH segments then, so the section download fails; the pipeline now refuses those with a clear message. Processed on 5 Nov without the Gemini judge (its busy-retries were most of the time).

**What the set found, and what was fixed:**

- **7 of 10 worked first time:** counters found, 11–16 kills per 30 min, plausible clip mixes. Landscape sections scan in 5–6 min, vertical ones in 11–21 min (the whole-frame "Spectating" read).
- **Compact icon HUD (LoLzZz):** BGMI's newer HUD shows person 36 · crosshair 20 · wings 2 with no text labels, so the label search found nothing and 0 kills. Fixed: the row is read as one OCR line and the numbers placed from its three fixed cells (`icon_row`); reads were right on all six checked frames (92/79/50/36/32/18 players, 9→26 kills). Two earlier attempts anchored on the OCR box edges and failed because OCR merges the icons into the number boxes unpredictably.
- **Vertical streams with a small gameplay window (SULTHAN, Rajput):** at 720×1280 the HUD text is about 8 px tall; SULTHAN's "Remaining 52" read as "2" and Rajput's labels were never found although he had 3–4 kills a match. Fixed: vertical sources are downloaded and analysed at 1080×1920 (`VERTICAL_HEIGHT`, `VERTICAL_ANALYSIS`). SULTHAN's remaining counter then read correctly (52 → 15, new lobby 52); his section has 1 kill, which looks genuine (early deaths).
- **Transcript coverage** is 0.84–0.86 on landscape streams and 0.38–0.54 on vertical ones; six of ten were flagged "broken" by the 0.5 rule. Either the rule is too strict for noisy phone streams or the batched spans miss speech under loud game audio; to be looked at with the owner's swipes.
- **Gemini free tier** failed two jobs outright with 503 before the judge was made to leave a clip unrated instead of failing.

Recall against hand-picked moments still needs the owner's strict swipes on five of these sections (their keeps are the "top moments").

**Final per-stream results (6 Nov, all ten complete, no Gemini judge):**

| Section | Layout | Counters | Kills / 30 min | Transcript coverage | Clip mix | Minutes (HUD + transcript + render) |
|---|---|---|---|---|---|---|
| LoLzZz (big creator) | landscape 720 | icon HUD, kills only | 28 (3 accolades) | 0.60 | 3 multi-kill, 6 fight, 2 rage, 1 funny | 12 + 14 + 10 |
| Bixi OP (handcam, pro) | landscape 720 | both | 12 | 0.84 | 1 multi-kill, 7 fight, 2 talk, 2 reaction | 6 + 2 + 4 |
| SHLOK (solo vs squad) | landscape 720 | both | 11 | 0.86 | 7 fight, 1 funny, 1 talk, 3 reaction | 6 + 3 + 4 |
| NesaMani (Tamil) | landscape 720 | both | 5 (1 chicken dinner) | 0.32 | 1 win, 4 fight, 1 talk, 3 reaction | 5 + 3 + 4 |
| Aashi | vertical 720 | both | 16 (same after the rebuild) | 0.51 | 3 multi-kill, 4 fight, 5 talk | 18 + 12 + 6 |
| Beast | vertical 720 | both | 12 (same) | 0.48 | 1 multi-kill, 8 fight, 1 talk, 2 reaction | 19 + 9 + 5 |
| PABLO (Telugu, Hindi) | vertical 720 | both (digit-anchored) | 13 → **8** (the 13 had a stuck counter and a teammate's 5) | 0.41 | 2 multi-kill, 4 fight | 21 → **8** + 8 + 1 |
| im_Trex (small, facecam) | vertical 720 | both | 14 (same) | 0.40 | 1 multi-kill, 6 fight, 1 funny, 4 reaction | 17 + 11 + 2 |
| SULTHAN (facecam) | vertical 1080 | both | 1 → **6** after the Spectating fix | 0.38 | 4 talk, 1 fight, 7 reaction | 18 → **13** + 4 + 1 |
| Zx_Rajput (small, Hindi) | vertical 1080 | elims only (24-frame search) | 6 → **12** after the Spectating fix | 0.54 | 1 multi-kill, 7 fight, 1 talk, 3 reaction | 55 → **9** + 4 + 1 |

- **10 of 10 layouts handled** after the three fixes (icon HUD, 1080 for vertical sources, 24 calibration frames for the whole-frame search). Rajput's counters were found on 3 and 6 of the 24 frames; with 12 frames they were missed because most of his section is lobby time.
- **The vertical "Spectating" check was rebuilt (6 Nov)** after Rajput's scan took 55 min for 30 min of video and his count was wrong in both directions. What was found and fixed, in `vision.py`:
  - His tiny HUD made OCR's "Remaining" box swallow its own number, so both counters sat on the Eliminations number: no lobby was ever seen, a new match's reset was refused and his later matches' kills were lost. Overlapping counter boxes now keep only Eliminations (`drop_overlapping`).
  - Every misread of the tiny digits triggered a whole-frame Spectating read (about 3 s each, 914 times). The check now waits for two agreeing reads, and on vertical frames looks for the text only in a band below the counters.
  - OCR reads the tiny in-game "Spectating: Teammate" on only about a quarter of the frames (the text is on screen every second; the busy background defeats OCR), so the first find is a repeated enlarged search every second while a counter change looks possible, and from then on a **pixel template** of the text is matched on every frame at no cost (`spectate_template`, `spectate_match`). Only thin strokes go into the template and the match (orange mask, else bright mask): PABLO's first template included a character's skin, so every frame looked like spectating and his kills vanished. The results screen's "Spectating: 0/10" is skipped.
  - A teammate's counter can still be accepted in the seconds before the text is seen, so a change is **undone** if the text appears within 12 s of it (`SPECTATE_RETRACT_S`; longer would undo a real kill made just before dying).
  - A rise of 20 to at least 40 players now counts as a new lobby (SULTHAN's lobbies fill to about 52).
  - **Counter boxes are anchored on the digits** OCR finds next to the label (`number_box`): the enlarged whole-frame search pads the label box, which on PABLO cut off the first digit of "Remaining" (players read as 1–19, no lobby ever seen, resets refused, 1 kill found). With no digits on a calibration frame the old label-edge estimate is used.
  - **A kill jump of 3 or more must hold for four reads** (two for 1–2): PABLO's HUD flashed a teammate's "5" for two seconds, which had become five kills at a wrong time.
  - Result: Rajput 55 → 9 min and 6 → 12 kills (6 + 2 + 4 over three matches, teammate changes undone); SULTHAN 18 → 13 min and 1 → 6 kills (his early kills had been suppressed by false "Spectating" matches from his facecam overlay text, and his second match was never reset); PABLO 21 → 8 min and a clean 8 kills at the right seconds. Aashi, Beast and im_Trex re-ran with the same counts as before. All six vertical sections now have fresh clips. Landscape streams went through the same code paths only for the counter calibration (`number_box`) and the jump rule; they were not re-run and should be spot-checked once (GtxPreet's full job is the reference: 59 kills).
- Kill counts: 11–16 per 30 min on most streams; LoLzZz 28 (big creator, aggressive); NesaMani 5 with a dinner.
- The owner's strict swipes on five of these sections are still needed for the recall figure; the clips are in the app.

## Kill feed and knocks (6–7 Nov)

BGMI's kill feed sits under the teammate list at the left edge of the gameplay window, one row per event: "killer, weapon icon, kneeling icon for a knock, victim" (no words; the own rows are highlighted). Built in `vision.py`:

- `feed_region` places the feed from the counter row (left edge of the frame to 18 label-heights past the Remaining number, 4–12 label-heights below the row). Read every 4 s while any text shows there; each OCR read costs about 0.3 s whatever the crop size, so it roughly doubles a landscape scan (Bixi 5.7 → 11 min). `feed_worth_reading` gives the feed up after 120 reads if fewer than 8% produced a full "killer > victim" row.
- `feed_rows` pairs the two names per row (OCR returns them as separate boxes split by the icons).
- `knocks_from_feed` learns the streamer's in-game name from the rows at the counter's kill times (fuzzy, since OCR mangles names), then: own row with no counter rise within −2..+4 s = `self_knock`; row ending with the name = `self_down`. `AIGCM_PLAYER_NAMES` still overrides.
- Results so far: **Bixi** learned "Sutli Bomb" by itself and found 2 knocks and 1 down beside his 12 kills. **GtxPreet**: the feed rows are half-transparent over a bright map and OCR reads none of them at any zoom (name None, 0 knocks). **Aashi** (vertical): 22 junk rows. **DIPENDU**: an overlay covers the feed. So knocks are a bonus signal on layouts with a readable feed, not a guarantee. The moments already weight `self_knock` (7) and label knocks; `self_down` is stored but not scored yet.
- **Confirmed 7 Nov:** GtxPreet's section gives the feed up after 120 reads (1 full row) at 3 min of video and scans in 10.9 min for 40 min; Bixi keeps it and scans in 9.0 min for 30 min (5.7 without the feed, 11.3 with 3 s reads), learning "sutli bamb" and finding 1 knock and 1 down (a second knock seen with 3 s reads is missed at 4 s; accepted). Knocks and downs are a bonus on readable layouts.
- Downs are used in moments (7 Nov): a `self_down` within 15 s after a fight's last event is attached to it, the clip runs on to it, the reason says "then the streamer goes down" and the label `down` is set; a down alone is never a clip. Knock-only clips get stat titles ("2 KNOCKS NO FINISH", "KNOCK DIYA PHIR").

Also fixed 6 Nov: `--force vision` used to mark the audio chain stale too, so Whisper re-ran beside every scan and halved its CPU (`jobs.stages_from`); forcing vision now leaves audio/sounds/transcript alone, and vice versa.

## Next

1. Owner: strict swipes on five accuracy sections and the rebuilt GtxPreet job (recall figure, talk-vs-fight balance).
1a. (Done 6 Nov) Bixi re-scanned after the calibration and jump-rule changes: same 12 kills, 2 matches, 1 accolade, 5.7 min. Landscape is unaffected.
2. Decide the transcript "broken" threshold from the owner's swipes; then M2 (database, API, worker, Google sign-in, upload, new web app).
3. Then M2: database, API, worker, Google sign-in, upload, new web app.

## Known slow spots

- Gemini free tier: the judge spends most of its time in 503 "busy" retries (7–22 min per job). The paid tier at launch (M6) should remove that.
- Vertical layouts now scan at 0.25–0.65× realtime (8–19 min per 30 min) after the Spectating rebuild; the enlarged search for the text costs about 1 s per try until it is found, so streams where it is found late (Aashi, Beast: never found in 30 min) are the slower ones. Landscape 720 is 0.2×.

## Not tested yet

- The ranking balance between talk clips and fights (needs the owner's swipes on the rebuilt GtxPreet job).
- After `cleanup`, re-editing a clip needs the source again: the editor (step 5) must re-ingest or say the source is gone.
