# Highlights Stage 1: the stream map and the kill-match highlight

Written 12 November 2026, before any Stage 1 code. Built on the research in [reports/BGMI creators content A to Z.md](../reports/BGMI%20creators%20content%20A%20to%20Z.md), [reports/BGMI highlight channels deep study.md](../reports/BGMI%20highlight%20channels%20deep%20study.md) and [reports/BGMI highlight video structure.md](../reports/BGMI%20highlight%20video%20structure.md), the owner's decisions of 12 November (all recorded in [ai-gcm/BUILD_NOTES.md](../ai-gcm/BUILD_NOTES.md)), and a check of what the engine detects today on the test streams in `ai-gcm/jobs/`. **Nothing here is built until the owner approves this plan.**

**Stage 1 goal:** from one stream recording, Kaatclip makes a **map of the stream** (which parts are matches, lobby, chat and other things, and what happened in each match) and, from it, **a 16:9 highlight of the best kill match** (or the best few matches in order), told the way Goblin's and LoLzZz's editors tell it, plus **a few Shorts cut from that highlight and a teaser Short**, offered as one batch with suggested posting times. The creator watches, adjusts and approves on the phone; nothing posts by itself.

**Done when:**
1. On the three full test streams, the map finds every match and its kills, as checked against hand labels (section 4).
2. Each stream's highlight is a watchable story from drop to the ending, with no fight cut in half and no sentence cut mid-word.
3. The owner, watching them on the phone, says they are the kind of video he meant, which the 12 clips were not.

---

## 1. What the check of the engine found

| # | Finding | Effect on Stage 1 |
|---|---|---|
| H-R1 | **Most of the match map's raw signals already exist.** The HUD scan (`aigcm/vision.py`) reads the Eliminations counter (each rise is a kill; a drop to 0 in a fresh lobby is a new match, `match_start`) and the Remaining counter (players left, saved over time). It also reads the Chicken Dinner banner, "You knocked out" messages, kill-feed rows (when the layout allows it), and "Spectating". | The map is mostly assembly of what is already in `vision.json`, plus a few new reads (H-R3, H-R4). |
| H-R2 | **Match starts are found, but match ends are not stored.** "Spectating" is used inside the scan to ignore a teammate's counter, but the times are not saved. The end of a match (the streamer dies and spectates, wins, or leaves to the lobby) is never written down. | The scan saves spectating periods and the moment the counters disappear. The map then infers each match's end from: Chicken Dinner → death plus spectating → counters gone → the next match start. |
| H-R3 | **Placement is not read.** The result screen ("#4", "Chicken Dinner", the rank and kill summary) is not read, apart from the Chicken Dinner banner. | Add a result-screen read when the counters disappear at a match end. Best effort; the Remaining counter at the streamer's death is the fallback placement estimate. |
| H-R4 | **Chicken Dinners and knocks are rare in the test data.** Over about 7 hours of full test streams there is 1 Dinner and 0 knocks found. Knocks are read from the kill feed, which is unreadable in most layouts. | Fights are built from kills plus the gunfire detector (already in `moments.py`) rather than knocks. Whether Dinners are being missed or simply did not happen is checked against the hand labels (S1.1). |
| H-R5 | **The test set is thin.** There are only **three full streams**, all other streamers' and used only for testing, never posted. DIPENDU is 2 h 3 min (vertical), ANJI 2 h 9 min (vertical) and the Hindi "4.6 update" stream 3 h 8 min (landscape). Ten 30-minute sections cover other layouts: LoLzZz landscape, Bixi handcam, Shlok solo vs squad, Aashi and Beast vertical, and others. The owner does not stream, so there is none of his own. | Stage 1 is built and checked on these. **One full OBS recording from a beta creator** (their own footage, which they can post) is the real test before the beta (owner task, section 6). |
| H-R6 | **The compilation renderer already does most of the output work.** `studio/compile.py` renders pieces at 1920x1080 (vertical streams over a blurred copy), adds title cards and joins without re-encoding, at about 1.4x real time. The facecam finder, Studio Shorts layouts, covers, thumbnails and titles all exist. | The highlight is a new kind of piece list on the same renderer, not a new renderer. |
| H-R7 | **The source is deleted after 14 days** (`source_keep_days`), but decision 8 keeps leftover moments for three weeks. | Leftover fights are stream-copied into small working windows (as kept clips already are) before the source goes; those windows are removed after 21 days. |
| H-R8 | **The research overturns one earlier default.** None of the six channels adds a running kill counter, and none uses chapters. | No kill counter and no chapters on highlights. The "Full stream:" link stays in the description. |

---

## 2. Decisions for Stage 1

These come from the owner's choices and the research; they hold unless the owner changes them.

1. **The map comes first** (decision 1). Every stream is split into parts before anything is ranked:
   - **match**: the game HUD counters are on screen;
   - **between matches**: lobby, inventory, crates or menus, where the counters are gone but the stream keeps going;
   - **not BGMI**: no HUD for a long stretch, for example chat with the face full screen, another game or a watch party.

   Stage 1 tells these three apart. Telling chat from another game from a watch party comes in later stages; until then, every "not BGMI" part is simply not used, and the map says why (decision 6).
2. **What a highlight is.** One match, told in order:
   - a **15-25 s cold open** from the best fight or the ending, under an "IN THIS VIDEO" label;
   - the **drop** (a few seconds);
   - **every fight kept whole with its comms**, from the first call or shot to the reaction after the last kill;
   - looting, running and waiting **cut**, with an "A FEW MINUTES LATER" card only when a lot of time is skipped;
   - the **final circle**;
   - the **ending**: the Chicken Dinner or result screen, a few seconds of the streamer's face, then black.

   The length is whatever the match needs (decision of 12 Nov), usually 25-50% of the match.
3. **The session version.** When two or more matches in a stream are strong, a second version joins them in order with "MATCH 2", "MATCH 3" cards: LoLzZz's multi-match format and Goblin's day reel. The creator picks one version or both.
4. **Which match is "best".** Ranked on:
   - kills;
   - a Chicken Dinner or placement;
   - the number of fights and how close they were (players left, a knock on the streamer, a 1vN);
   - talk and laughter inside the match.

   The creator can pick any other match from the map.
5. **Keep the stream layout**, facecam and overlay included, in 16:9. **Facecam punch-ins** (the face full screen for 2-4 s) go on the biggest reactions, where the facecam finder found a face. This is the device all three creators use most, and it uses only the creator's own footage.
6. **No music under speech, no film or TV memes, no kill counter, no chapters.** Bleeps stay off unless the creator turns on sponsor-safe mode.
7. **Shorts come from the highlight** (decision of 12 Nov):
   - one **teaser Short** (the ending proof or best fight, 20-40 s), suggested for the same evening;
   - **2-3 best-moment Shorts** (30-60 s) in the stacked layout, suggested over the next days.

   The old 12 standalone clips stay available, but they are no longer the main product.
8. **One stream, one batch** (decision 4). The stream page offers the highlight and its Shorts together, with suggested times taken from the research: the teaser the same night at 21:00-22:00, the highlight the next day at about 12:00, and the other Shorts at 21:00 on the following days. They go into the existing calendar as drafts. Each one is approved one by one, or in a batch, with the existing approval flow.
9. **Titles** (decision 3). Every highlight gets a kill title ("14 KILLS CHICKEN DINNER") and, when the kill feed or the talk gives a name with confidence, a people title ("vs NAME"). The people title comes first when there is one. The creator picks.
10. **Channel label** (decision 5). Highlights cut from the stream are labelled "second channel" as a suggestion; a record match (the stream's best kill count by far) is labelled "main". There is still one connected channel.
11. **Leftovers** (decision 8). Fights not used in any video stay listed on the map for 21 days, kept as small windows, ready for a later "part 2" or a compilation.

---

## 3. Steps

Each step ends with its own check, and BUILD_NOTES is updated after each.

| Step | What | How | Checked by |
|---|---|---|---|
| **S1.1 Hand labels** | The truth to measure against | Claude labels the three full streams and four of the 30-minute sections from frames (one every 10 s, closer near counter changes): each match's start and end, kills, placement, Chicken Dinner, and the not-BGMI parts. Saved as `tests/data/labels/*.json` (numbers only, no footage). | The labels themselves are spot-checked against the frames a second time |
| **S1.2 Scan additions** | The match-end signals | `vision.py` saves the spectating periods, when the counters vanish and reappear, and reads the result screen (placement, and kills when shown) once a match ends. Only these three streams' vision stage is re-run. | A unit test with frames from the test streams; the new fields appear in `vision.json` |
| **S1.3 The stream map** | `aigcm/streammap.py`, a new stage `map` after `moments` | Builds the parts (match / between matches / not BGMI) and, for each match: start, end, how it ended (Dinner, death, unknown), placement, kills over time, the fights (kills plus gunfire, with players left), and the talk and laughter inside it. Writes `map.json`. | Scored against the labels: every match found, start and end within 20 s, kills exact in at least 9 of 10 matches, Dinners all found. The results go in BUILD_NOTES. |
| **S1.4 Highlight cut** | `aigcm/studio/highlight.py` | Turns one match (or several) into a piece list using the rules in decision 2. Fight edges follow the gunfire start and the transcript, so setup calls and the reaction stay in and no word is cut. Cuts are stretched to sentence ends. The cold open comes from the best fight's peak. Cards appear where time is skipped or a match changes. The ending is the result screen plus face. Punch-ins come from laughter and shout peaks inside the facecam box. | Unit tests on the rules; for each test stream, a written cut list Claude checks against the frames (no fight cut short, nothing silent and long) |
| **S1.5 Render** | Highlight video and light copy | On the compilation renderer: pieces at 1920x1080, cards and the "IN THIS VIDEO" label drawn like the hook titles, the punch-in as a crop of the facecam box scaled up, then joined. A render-lane job `highlight`. Also makes the light play copy, three thumbnails and the titles. | The three test highlights rendered; Claude watches them through frames and checks the sound; render time recorded |
| **S1.6 Shorts from the highlight** | Teaser and 2-3 Shorts | Picks the moments from the highlight's own pieces and makes each one a normal Studio clip with the stacked layout and a hook title. Each one can then be opened in the existing editor. | The Shorts exist, play and open in the editor |
| **S1.7 Phone screens** | The map and the highlight on the stream page | A **Highlights** section on the stream page: the map as a bar (matches numbered, with kills and Dinner; not-BGMI parts greyed with the reason); the suggested highlight playing; the fights listed, each with an on/off switch and a play button; another match or the session version; **Make again**; titles to choose from; the label (main/second). | Web tests; the screens checked at phone size on a copy of the database |
| **S1.8 Batch and schedule** | One stream, one batch (decision 4) | **Plan the posts** turns the highlight and its Shorts into calendar drafts at the suggested times, with the existing approve and batch-approve flow. Never auto-posted. | API test; a batch appears in Posts → Week at the right times |
| **S1.9 Leftovers** | Decision 8 | Fights not used are stream-copied as windows before the source is deleted and removed after 21 days by housekeeping. They are listed on the map as "not used yet". | Test with a fake clock: the windows exist on day 15 and are gone on day 22 |
| **S1.10 Owner check** | The real test | The owner watches the three highlights and their Shorts on the phone and says what is wrong. The fixes are made, then the next stage is planned. | The owner's verdict, written in BUILD_NOTES |

The order is S1.1 → S1.3 first (the map must be right before anything is cut from it), then S1.4 → S1.6, then the screens and the batch.

---

## 4. How "good" is measured

- **The map**, against the hand labels:
  - matches found: all of them;
  - start and end within 20 s;
  - kills per match exact in at least 9 of 10;
  - Chicken Dinners: all of them;
  - placement: right or within 2 places in most matches (best effort);
  - not-BGMI parts: no BGMI match marked as not BGMI.
- **The highlight**, checked by Claude on every test stream:
  - every labelled kill in the chosen match appears;
  - no cut inside a word;
  - no stretch over 20 s with nothing happening and nobody talking;
  - the ending shows the result.
- **The owner's verdict**, the one that decides: are these the videos you meant, would a streamer post them? Each highlight gets yes or no plus what is wrong.

---

## 5. Not in Stage 1 (later stages, in the order the owner chose)

- **Stage 2, comedy:** the funny-session highlight (laughter read only inside the BGMI part, units from setup to punchline, facecam zooms, "THE NEXT DAY" cards), from the JokerClips recipe.
- **Stage 3, the other session types**, in the order of decision 2:
  - custom room / TDM (mode detection, round cards);
  - crate opening (crate-screen detection, ending on the total);
  - talk cut (a "chat" part type, topic edges).
- **Later:** telling chat, other games and watch parties apart; compilations and "part 2" from leftovers; a second connected channel; the milestone cut; a second player's recording (decision 7: not now).

---

## 6. Risks and what the owner needs to do

| Risk | What we do |
|---|---|
| Three full test streams is a small set, and none is a beta creator's own | Check on them, then on **one full OBS recording from a beta creator** before the beta. *Owner task:* when a creator agrees to try Kaatclip, ask for one whole stream recording. Their own footage, so their highlight can be posted. |
| Chicken Dinner and placement may be missed in some layouts | The map shows "ending: unknown", and the highlight ends on the last fight and the face. The hand labels will show how often this happens. |
| Kill feed unreadable means no names, so no people titles | The kill title is used. Names said in the talk are a second source, best effort. |
| Rendering a 10-minute highlight takes about 14 min on the laptop and uses disk | It runs in the render lane in the background, and Telegram says when it is ready. Leftover windows are small (stream copies of single fights). |
| Test streams are other streamers' footage | Never posted, as now. Only the creator's own recordings are posted. |
| The owner may find the first highlights still not right | S1.10 is the checkpoint: fix, then decide, before Stage 2. |

**Owner tasks in Stage 1:** approve this plan; at S1.10, watch the three highlights on the phone and say what is wrong; ask a beta creator for one full recording.
