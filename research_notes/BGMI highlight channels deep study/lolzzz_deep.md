# LoLzZz Gaming and LoLzZz Plays: how the challenge highlights are made, cut and uploaded (deep study)

Measured 12 Nov 2026 with yt-dlp: flat playlists of every tab, per-video metadata, Hindi auto-captions (`hi-orig`), YouTube storyboard mosaics (`sb0`, one 320x180 frame about every 5 s for 10-15 min videos) and thumbnails. No video or audio was downloaded. This extends `research_notes/BGMI highlight video structure/lolzzz_challenge.md`; facts already there are not repeated unless a number changed.

Method notes (apply to every section):
- **Source mapping** was done by matching word 3-grams of a highlight's auto-captions against the auto-captions of candidate streams, then taking the longest chain of anchors that runs forward in both videos. A jump in the offset (stream time minus highlight time) is a cut. A highlight's music-covered or speechless stretches produce no anchors, so the cut lists below are a lower bound on the number of cuts and the "kept" pieces are the speech-anchored parts. A visual frame-matching check (storyboard to storyboard) was tried for the 72-kill video and gave too little margin at 10 s stream sampling to be used.
- Storyboard frame times are accurate to about ±5 s. Anything shorter than about 5 s on screen (a 2-3 s card, a quick flash) can be missed.
- Raw data, scripts and contact sheets are in `C:\Users\soura\AppData\Local\Temp\claude\21027423ba80eb72\ab9e7281-b606-4050-82cb-606e6c8ce9f9\scratchpad\yt_research\lolzzz_deep\` (`main_*.jsonl`, `plays_*.jsonl`, `stream_dates.txt`, `short_meta.txt`, `subs\`, `sb\`, `chain.py`, `phase.py`).
- All times IST. "HL" means the highlight video.

## 1. What the two channels upload, and how the work is split

### Takeaway
The main channel is a daily 5-7 hour live stream plus a rare edited highlight. In 2026 the edited highlight is almost always one record match ("N SOLO KILLS WORLD RECORD"). LoLzZz Plays carries the rest of the edited output: the second-best record matches, cash-per-kill challenges, "vs streamer" fights, esports watch-party reactions and nearly all Shorts. The same editor style, thumbnail template and stream recordings feed both channels. In one case two different 50+ kill matches from the **same** stream went one to each channel.

### Cited Findings
- **Inventory sizes (flat playlists, 12 Nov 2026):**
  - Main channel [@LoLzZzGaming](https://www.youtube.com/@LoLzZzGaming): 418 items on /videos (Nov 2019 to Oct 2026), at least 600 on /streams (600 is the fetch limit; all within roughly the last 1-1.5 years), 107 on /shorts.
  - [LoLzZz Plays](https://www.youtube.com/@lolzzzplays): at least 600 on /videos (limit hit; back to 2022), 390 on /shorts, 62 on /streams (mostly 2023 and 2025 restreams such as "ULTIMATE ROYALE RANK PUSH WITH JONATHAN GAMING", 29,812 s, [sABphn5ZHQA](https://www.youtube.com/watch?v=sABphn5ZHQA)).
- **Main-channel streams (600 newest):** median 21,709 s (6.0 h), interquartile range 18,609-24,442 s (5.2-6.8 h), median 537K views, maximum 2.1M (BMSD 2026 Grand Finals Day 1 watch party, [hNCb6AT6dwc](https://www.youtube.com/watch?v=hNCb6AT6dwc)) — [streams tab](https://www.youtube.com/@LoLzZzGaming/streams)
- **Stream cadence from exact start times** (101 streams, 7 Jun to 21 Oct 2026, plus the Oct-Nov ones already fetched):
  - 22 streams in 7-30 Jun (138 h), 24 in Jul (150 h), 28 in Aug (170 h, 6 of them PMWC watch parties), 15 in Sep (80 h), about 19 in Oct, 7 in 1-11 Nov.
  - Gameplay streams start at 21:05-21:52 IST almost every time (for example [wq2fjFmms1U](https://www.youtube.com/watch?v=wq2fjFmms1U) 24 Oct 21:32, [KsDcjdMrBzw](https://www.youtube.com/watch?v=KsDcjdMrBzw) 4 Jul 21:17). Watch parties start at about 13:00-16:00.
  - Source: per-video `release_timestamp` via yt-dlp.
- **Main /videos by type** (title-keyword classification, items of 61 s or more):

  | Type | All 398 | Newest 52 (about Nov 2024-Oct 2026) | Median length (newest) | Median views (newest) |
  |---|---|---|---|---|
  | Kill record ("N SOLO/SQUAD KILLS/FINISHES") | 153 | 26 | 760 s | 264K |
  | Tournament / scrims POV (BGIS, PMGC) | 13 | 5 | 1,180 s | 285K |
  | Other challenge (non-cash) | 10 | 4 | 656 s | 220K |
  | Clutch compilations | 25 | 4 | 572 s | 210K |
  | Cash challenge (₹/$/€, per kill) | 12 | 3 | 622 s | 272K |
  | Rank journey (Conqueror/#1/Legend) | 41 | 2 | 1,278 s | 404K |
  | 1v1/TDM collab with Jonathan | 10 | 1 | 481 s | 847K |
  | Vlog, story, sponsor, other | 98 | 6 | 905 s | 236K |

  Source: [main videos tab](https://www.youtube.com/@LoLzZzGaming/videos)
- **LoLzZz Plays /videos by type** (448 items of 61 s or more; newest 199 in brackets):
  - "vs streamer" encounter fights ("LoLzZz GAMING vs PIHU IS LIVE…", "THIS STREAMER STREAM SNIPED ME AND THIS HAPPENED"): 140 (91), median 604 s, 98K views.
  - Kill records / dominations: 70 (38), 576 s, 111K.
  - Esports reactions ("LoLzZz REACTION ON TAG…"): 24 (19), 524 s, 155K; top "REACTION ON JONATHAN'S LAMBORGHINI" 1.2M.
  - Crate openings: 16 (10).
  - Cash challenges: 10 (9), 639 s, 198K.
  - TDM/2v2 with Jonathan: 8 (7), 206K.
  - Source: [Plays videos tab](https://www.youtube.com/@lolzzzplays/videos)
- **Cadence of edited videos in 2026:**
  - Main channel: 16 long uploads (Jan 1, Feb 4, Mar 1, May 1, Jul 4, Sep 4, Oct 1). In July, 24 streams produced 2 main-channel records (61 and 64 kills) plus 1 cash challenge and 1 scrims video.
  - Plays: about 65 videos by YouTube's approximate dates. From exact dates: 10 uploads from 9 Sep to 10 Oct 2026, then none until 12 Nov, while its Shorts continued.
  - Sources: per-video `upload_date`; [Plays videos tab](https://www.youtube.com/@lolzzzplays/videos)
- **Same stream, two channels:** the 8 Sep 2026 stream "50 SOLO KILLS KAB HONGE" ([-vMIYNYkLAA](https://www.youtube.com/watch?v=-vMIYNYkLAA), 18,028 s) produced:
  - Plays' "I MADE A WORLD RECORD OF 51 SOLO KILLS IN BGMI" ([EJTupVtHuY8](https://www.youtube.com/watch?v=EJTupVtHuY8)), from the stream's **first** match at 0:16:28-0:42:07, uploaded 9 Sep 10:00.
  - The main channel's "55 SOLO KILLS IN NARUTO MODE" ([fbVXWfefL8c](https://www.youtube.com/watch?v=fbVXWfefL8c)), from the match at 4:05:20-4:29:25, uploaded 10 Sep 12:10.
  - The stream's captions also have him announcing other 50+ matches that got no highlight: "50 ho gaya" at 2:32:30; "50 kill ho gaye… isme hi 51 maare hain" at 3:34-3:36.
  - Source: caption alignment (section 3).
- Plays also took a record that fit the main channel's format: "TAG LoLzZz 50 SOLO FINISHES IN 4.4 UPDATE" ([ckdrrSD2Y0w](https://www.youtube.com/watch?v=ckdrrSD2Y0w)), cut from the 30 Jun stream [zpbonbp_tyw](https://www.youtube.com/watch?v=zpbonbp_tyw). Four days later the main channel posted the 61-kill record.
- **Some highlights come from a teammate's stream.** "WE GOT ₹1,000 PER KILL CHALLENGE IN SCRIMS" ([3i83F-jSotA](https://www.youtube.com/watch?v=3i83F-jSotA)) and the main channel's "THIS IS HOW I REACHED LEGEND IN ULTIMATE ROYALE" ([69AEExuBZfU](https://www.youtube.com/watch?v=69AEExuBZfU)) both show a stream overlay labelled "JONATHAN" with a 7.4-7.9M subscriber counter, and a different facecam. The 3i83F thumbnail shows Jonathan holding cash next to LoLzZz — storyboards and [thumbnail](https://i.ytimg.com/vi/3i83F-jSotA/hqdefault.jpg)

### Inferences
- The split looks like this:
  - **Main** = the session's single best "trophy" match (a new personal best, or a first in a new update or mode) or a big collab.
  - **Plays** = a second strong match from the same run, cash challenges, streamer encounters and reactions.
  - For Kaatclip this maps to "one headline highlight per session, plus a secondary cut" rather than one video per match.
- Highlights are rare relative to streaming. About one main-channel highlight per 6-12 streams, and the multi-day stream titles ("60 SOLO KILLS KAB HONGE?" → "70 SOLO KILLS TODAY?") show the edit waits for the goal to be reached.

### Gaps
- Dates for streams older than June 2026, and for Plays items older than September 2026, are YouTube's coarse "N months/years ago", so long-run cadence is approximate.
- The exact rule for which record goes to which channel is not stated anywhere; the "best to main, other to Plays" reading rests on one fully mapped stream plus the timing of the 50/61/64 uploads.

## 2. Anatomy and editing grammar of the highlights (15 videos)

### Takeaway
Every challenge highlight from both channels uses the same edit grammar:
1. A cold open of about 30-60 s (median about 0:39): a black frame, a full-screen facecam stating the goal (lifted from the stream's first minutes), 2-3 teaser kill shots, then the final number said over music, and a black frame before the match.
2. The match plays in order on the unchanged stream layout (small facecam, live subscriber counter, sponsor bar).
3. The match is spiced every 1-3 minutes with meme cutaways that carry name labels ("ENEMY :", "IGL", "LoLzZz"), full-screen facecam punch-ins on reactions, and the occasional TV-colour-bars or whip transition.
4. It ends on proof: the Winner Winner Chicken Dinner and/or MVP screen, a full-screen facecam celebration with his catchphrase ("mode koi bhi ho, record tere bhai ka rahega"), and a 5-10 s black end screen.

No editor-made kill counter or "Match 2" card was seen in any storyboard.

### Cited Findings
**Per-video measurements.** "Open" is when the match's first gameplay starts after the cold open (from storyboards). Heatmap peaks are "most replayed" local maxima as time (% of length, value). "End" is what is on screen after the final kill.

| Video (channel) | Dur | Views | Open ends | Heatmap peaks | End sequence |
|---|---|---|---|---|---|
| [72 SOLO KILLS](https://www.youtube.com/watch?v=-qpx-ejuq9Q) (main) | 11:49 | 990,648 | 0:48 | none yet | WWCD 11:14, facecam, lobby, black 11:44 |
| [62 SOLO KILLS ZOMBIE](https://www.youtube.com/watch?v=Car5bJ_yP-E) (main) | 13:32 | 595,971 | 0:29 | 5:24 (40%, 1.00), 9:20 (69%), 11:54 (88%) | ~70 s full-screen facecam cake celebration 12:12-13:22 |
| [61 SOLO KILLS](https://www.youtube.com/watch?v=Gn1AvcFXl-Y) (main) | 13:17 | 751,570 | 0:38 lobby, 0:54 drop | 6:06 (46%, 1.00), 1:59 (15%, 0.96) | facecam, WWCD 12:42, MVP 12:57, black 13:07 |
| [64 SOLO KILLS](https://www.youtube.com/watch?v=0inNw0cj1p0) (main) | 15:11 | 484,187 | 0:42 | 6:22 (42%, 1.00), 11:59 (79%), 13:49 (91%) | facecam, WWCD 14:22, lobby, MVP 14:41, black 15:01 |
| [55 NARUTO MODE](https://www.youtube.com/watch?v=fbVXWfefL8c) (main) | 12:16 | 360,625 | 0:44 | 11:17 (92%, 1.00), 5:23 (44%) | WWCD 11:11, facecam, WWCD medals, MVP 11:41-11:56, facecam, black 12:11 |
| [50 FINISHES 4.3](https://www.youtube.com/watch?v=4UDz_mbdTtM) (main) | 12:59 | 238,624 | 1:04 (parachute) | 12:27 (96%, 1.00), 7:08 (55%) | facecam 12:29-12:39, lobby, MVP 12:49 |
| [200€ FOR 40 SOLO KILLS](https://www.youtube.com/watch?v=KQofJQWmP4Y) (main) | 10:22 | 187,315 | 0:34 | 9:26 (91%, 1.00), 4:46 (46%, 1.00) | WWCD 10:12, end 10:17 |
| [PER KILL 1000](https://www.youtube.com/watch?v=KzSEzZBOpns) (main) | 10:19 | 272,277 | 0:39 | 6:36 (64%, 1.00), 9:54 (96%) | death and "55 dekh, chal yaar" (no win) |
| [LEGEND IN ULTIMATE ROYALE](https://www.youtube.com/watch?v=69AEExuBZfU) (main, Jonathan POV) | 10:14 | 191,553 | 0:39 | 7:34 (74%, 1.00), 9:49 (96%) | team results table 9:59, facecam, black |
| [100 KILLS IN 3 MATCHES](https://www.youtube.com/watch?v=-9A2Hyty0Lg) (main) | 24:11 | 370,148 | ~1:09 | 20:05 (83%, 1.00), 2:25 (10%, 0.95) | team results table 23:41, facecam, black 24:01 |
| [51 SOLO KILLS](https://www.youtube.com/watch?v=EJTupVtHuY8) (Plays) | 12:11 | 265,859 | 0:34 | 5:22 (44%, 1.00) = a labelled meme | facecam, WWCD 11:56-12:06 |
| [50 SOLO FINISHES 4.4](https://www.youtube.com/watch?v=ckdrrSD2Y0w) (Plays) | 11:57 | 184,882 | 0:59 | 5:08 (43%, 1.00), 6:27, 9:20 | facecam 11:17-11:32, MVP 11:47 |
| [₹5000 PER KILL SNIPER](https://www.youtube.com/watch?v=7bmUiiUuAdE) (Plays) | 9:37 | 365,038 | 0:34 | 6:20 (66%, 1.00) = sniper kills | WWCD 9:12, facecam, MVP 9:22 |
| [₹1000 PER KILL IN SCRIMS](https://www.youtube.com/watch?v=3i83F-jSotA) (Plays, Jonathan POV) | 9:09 | 198,250 | ~0:39 | 5:12 (57%, 1.00) | placement banner 8:44, MVP 8:49-8:54, facecam |
| [PLATINUM TO #1 CONQUEROR](https://www.youtube.com/watch?v=gPonigAeizQ) (main) | 31:13 | 486,183 | ~1:00 (from earlier notes) | 27:10 (87%) | celebration |

Sources: storyboards and yt-dlp `heatmap` for each linked video.

- **The cold open is built from stream lines said hours apart from the match.** Caption alignment shows:
  - The 72-kill cold open uses 0:00-0:04 from the **previous day's** stream ([IsBYwffTPHE](https://www.youtube.com/watch?v=IsBYwffTPHE) at 10:26: "aaj se le teen din tak … every game 30 40 50 60 70 80 90"), and 0:21 from minute 5:26 of the source stream ("mera target 70 hai").
  - The 61-kill open uses stream 2:45-2:58 ("aaj apan 55 kills pahunch payenge… challenge hai mere ko 56 solo kill ₹1 lakh").
  - The 64-kill open uses 3:44-3:49 and 5:18, plus a line from an **earlier match** at 1:08:44 ("ye saare kill lene hain, to ye game confirm").
  - The 55-kill open uses 14:27 ("bhai log are you ready … Spiderman").
  - Each open then plays the record catchphrase with the number ("…record tere bhai ka 64", "…let's go 55") taken from the end of the match.
  - Sources: [-qpx-ejuq9Q](https://www.youtube.com/watch?v=-qpx-ejuq9Q), [Gn1AvcFXl-Y](https://www.youtube.com/watch?v=Gn1AvcFXl-Y), [0inNw0cj1p0](https://www.youtube.com/watch?v=0inNw0cj1p0), [fbVXWfefL8c](https://www.youtube.com/watch?v=fbVXWfefL8c)
- **The cold open's visual order** repeats, with small variations, across all 14 storyboards checked (the 62 and 64 open on teaser gameplay before the first facecam shot): frame 0:00 black → full-screen facecam (a crop of the stream's facecam, sometimes black-and-white: 72, 50-in-4.3, per-kill-1000) → 2-3 teaser shots (scope kills, multi-kills) → facecam reaction → black frame at about 0:24-0:34 → match. The 61 open ends on the MVP screen (0:34) as a spoiler of the result; the 72 open ends on music under "72" — storyboards of the videos above.
- **Meme cutaways with name labels** are part of the house style:
  - 72 kills: "BRO IS LIVING IN 2019" meme 1:58, a CID meme 2:03, another 2:23, another streamer's cam labelled "THUNDER:" 3:13, a sticker 5:17.
  - 61 kills: a meme labelled "LoLzZz" 1:58; a group shot labelled "LoLzZz / MOR / RyLoZ / WOLF / T2" (his squad) 2:13; "ENEMY WITH AKM:" 2:48; a crowd meme 5:36; "ENEMY" 6:26.
  - 55 kills: 0:39 and an "ENEMY" meme 6:05.
  - Per-kill 1000: "ENEMY :" 1:04 and "RyLoZ :" 3:42.
  - Plays 51: a meme labelled "IGL / LOLZZZ" at 5:21-5:25, which is also that video's most-replayed point (5:22).
  - 100-in-3: an Oggy meme with a Hinglish caption 1:38.
  - Source: storyboards of the linked videos.
- **Other effects:**
  - Full-screen facecam punch-ins on big moments: 72 at 7:11 and 10:19; 55 at 3:47, 4:46, 10:42; per-kill 1000 at 6:36, right after the fight at its heatmap peak.
  - TV colour-bar "glitch" transitions: 61 at 2:18; 100-in-3 at 0:59.
  - Whip/motion-blur transitions: 55 at 6:15; Plays 51 at 2:13.
  - Black-and-white for a low moment: per-kill 1000 at 2:33.
  - A zoom into the HUD and facecam at the record kill: 72 at 11:04.
  - Source: storyboards.
- **The stream layout is kept unchanged in gameplay:** small facecam bottom-left, live subscriber counter (2,798,802 → 2,798,848 across the 72-kill match), and a sponsor bar (KICK, iQOO 15R, AMD Ryzen). The counter climbs steadily through each video, consistent with a single continuous session — [72-kill storyboard](https://www.youtube.com/watch?v=-qpx-ejuq9Q)
- **Multi-match challenge transitions are the in-game results screens, not cards.** In "100 SOLO KILLS IN 3 MATCHES":
  - Match 1 runs about 1:09-6:34, ends on the WWCD screen at 6:34, then a cutaway of another streamer reacting at 6:44, then match 2 lands at 6:54.
  - Match 2 ends on WWCD "#1/25" at 15:17, and match 3 (snow map) starts at 15:27.
  - The spoken checkpoints are "32 kill hue to 68 aur" (6:40) and "aakhri mukabla, maha mukabla" (15:30).
  - No "Match 2/3" text card is visible at 10 s storyboard spacing.
  - Source: [-9A2Hyty0Lg](https://www.youtube.com/watch?v=-9A2Hyty0Lg)
- **Event modes with recall (respawn) put parachutes mid-match:** 64 kills at 6:22, Plays 50 at 5:16, 61 at 5:26. The captions say "recall". Dying is therefore not the end of the match in these modes — storyboards and captions of [0inNw0cj1p0](https://www.youtube.com/watch?v=0inNw0cj1p0), [ckdrrSD2Y0w](https://www.youtube.com/watch?v=ckdrrSD2Y0w)
- **The ending tail after the record kill** runs about 43 s on the 72 video (final kill about 11:06 → end 11:49, about 5 s of it black), about 75 s on the 61 video (12:02 → 13:17) and about 70 s on the 55 video (about 11:06 → 12:16). The 62 video adds a 70 s facecam cake celebration — storyboards
- **Heatmap shape over 13 videos with heatmaps:**
  - The global maximum is in the middle third (40-66%) in 8 of them: a squad wipe, a sniper streak or a labelled meme.
  - It is in the last 10% in 3 (55 Naruto at 92%, 50-in-4.3 at 96%, 200€ at 91%).
  - The opening bin is above the mean in all 13 (1.03-4.55 times the mean).
  - Source: yt-dlp `heatmap`.
- **Minute-by-minute, 72 SOLO KILLS** ([-qpx-ejuq9Q](https://www.youtube.com/watch?v=-qpx-ejuq9Q); storyboard plus captions plus alignment):
  - 0:00-0:48 cold open: black; black-and-white facecam; black-and-white gameplay 0:09-0:14; "mera target 70 hai" at 0:21; colour facecam 0:24; teaser gameplay with effects 0:29-0:34; facecam 0:39-0:44.
  - 0:48-3:10 the drop and landing fights in a red-foliage zone (stream 1:49:10-1:54:44), fast cuts, four meme cutaways.
  - 3:16-3:49 a single 33 s piece standing in for 8 min of mid-game (stream 1:58:59-1:59:32).
  - 3:51-11:13 late game almost continuous (stream 2:02:47-2:14:08): driving and fighting from an orange car, facecam punch-ins at 7:11 and 10:19, "let's go bro 72 kills" at about 11:00.
  - 11:14 WWCD screen; 11:19-11:24 full-screen facecam scream; 11:29-11:34 Halloween lobby; 11:39 facecam; 11:44-11:49 black.
- **Minute-by-minute, 55 SOLO KILLS IN NARUTO MODE** ([fbVXWfefL8c](https://www.youtube.com/watch?v=fbVXWfefL8c)):
  - 0:00-0:44 cold open: black; facecam "are you ready for Spiderman" (stream 0:14:27); teasers 0:09-0:14; facecam 0:19-0:24 with "…tumhare bhai ka rahega, let's go 55"; black 0:29; teaser 0:34; meme 0:39.
  - 0:44-2:40 landing fights in town (stream 4:05:20-4:10:04).
  - 2:58-4:13 rotation pieces (stream 4:13:34-4:16:46).
  - 4:14-6:01 a 107 s continuous fight block (stream 4:17:07-4:18:54), "ENEMY" meme 6:05, whip 6:15.
  - 6:21-11:30 late game in pieces of 37-73 s, sniper scope shots, facecam 10:42.
  - 11:11 WWCD plus an in-game "Gameplay Management System" warning pop-up; 11:16-11:21 facecam; 11:31-11:36 WWCD medals; 11:41-11:56 MVP; 12:01-12:06 facecam ("57 tha ye… self-knock maar diya", "let's go 55"); 12:11 black.
- **Minute-by-minute, 61 SOLO KILLS** ([Gn1AvcFXl-Y](https://www.youtube.com/watch?v=Gn1AvcFXl-Y)):
  - 0:00-0:34 facecam goal talk (stream 0:02:45-0:02:58) cut against teasers at 0:14 and 0:24; "61" at 0:30; MVP screen 0:34 (spoiler).
  - 0:38-0:48 lobby donation read kept as setup ("a token for you to make 51 kills in next match", stream 2:41:40-2:42:08); plane path 0:39; facecam with subscriber counter 0:44; drop map "Ferry Pier" 0:49; parachute 0:54; landing 0:59.
  - 1:58-2:48 three labelled memes plus colour bars; 5:26 recall parachute; 6:06 most-replayed fight.
  - 12:02 final kill through a scope; 12:07-12:52 facecam alternating with "VICTORY TIME" gameplay, "61 mark kiya, world record is once again… always on top"; WWCD 12:42; MVP 12:57; black 13:07-13:17.
- **Minute-by-minute, 100 SOLO KILLS IN 3 MATCHES** ([-9A2Hyty0Lg](https://www.youtube.com/watch?v=-9A2Hyty0Lg)):
  - 0:00-1:09 cold open: facecam goal 0:09-0:19, teasers 0:29-0:39, facecam 0:49, colour bars 0:59.
  - Match 1 1:09-6:34 (memes 1:18 and 1:38, another streamer's reaction 4:46), WWCD 6:34.
  - Reaction cutaway 6:44 and match 2 6:54-15:17 (checkpoint 6:40; facecam 12:00), WWCD 15:17.
  - Match 3 15:27-23:21 ("aakhri mukabla" 15:30; most-replayed 20:05); dark frame 23:21; facecam head-in-hands 23:31; results table 23:41; facecam 23:51; black 24:01-24:11.
  - So about 5.4, 8.4 and 7.9 min per match.

### Inferences
- The edit is not a pure "every fight" compression. It is the match told in order with a fixed garnish: about one meme or facecam insert every 1-2 minutes in the first half, and facecam punch-ins at the biggest kills. The labelled memes give the viewer a running cast ("ENEMY", "IGL", squad names) without any narration.
- Proof screens (WWCD, MVP showing the kill number, results table) do the job a kill counter would do, which is why no counter overlay is needed.
- The heatmap points to the mid-match squad wipe or sniper streak as the most rewatched moment more often than the record kill. Kaatclip should place its best fight around 40-65% of the runtime and not save everything for the end.

### Gaps
- Overlays shorter than about 5 s (a "Match 2" flash, a sound-effect caption) cannot be ruled out at storyboard resolution.
- Music identity and levels cannot be measured without audio. The `[संगीत]` (music) tags in the auto-captions appear 9 times in the 72-kill video's captions, mostly in the cold open and the fight montages.

## 3. Source mapping: which stream segments each highlight uses

### Takeaway
Six highlights were mapped to their source streams with confidence (hundreds of unique caption 3-gram anchors each, against about 30-60 for unrelated streams). Each is **one match** of 24-30 stream minutes, cut to 10.6-14.4 minutes (keep ratio **0.41-0.52, median about 0.45**), always in chronological order apart from the cold open. The cut is uneven: the first 6 minutes (landing fights) keep about 40-50%, the middle quarter (rotation, bots, driving, chat) is cut hardest (often under 30%, once 9%), and the last quarter (final zones) keeps 57-70%. The highlight goes up about 11.5-12.5 hours after the match ends, at 10:00-12:10 the next day. The one exception waited 34 h because Plays had taken the stream's other match the morning before.

### Cited Findings
**Summary of the six mappings** (match span = first to last speech anchor inside the match; HL span = the matching highlight time):

| Highlight | Source stream (start, length) | Match in stream | Match length | HL span | Keep ratio | Kept speech pieces / cuts >60 s | Upload delay after match end |
|---|---|---|---|---|---|---|---|
| [72 SOLO KILLS](https://www.youtube.com/watch?v=-qpx-ejuq9Q) (main) | [wq2fjFmms1U](https://www.youtube.com/watch?v=wq2fjFmms1U), 24 Oct 21:32, 5.5 h | 1:49:10-2:14:44 | 25.6 min | 0:49-11:45 (10.9 min) | 0.43 | 23 / 4 | about 12.2 h (match ended about 23:47; up 25 Oct 12:00) |
| [55 NARUTO](https://www.youtube.com/watch?v=fbVXWfefL8c) (main) | [-vMIYNYkLAA](https://www.youtube.com/watch?v=-vMIYNYkLAA), 8 Sep 21:22, 5.0 h | 4:05:20-4:29:25 | 24.1 min | 0:51-12:06 (11.3 min) | 0.47 | 15 / 6 | about 34 h (01:51 → 10 Sep 12:10) |
| [51 SOLO KILLS](https://www.youtube.com/watch?v=EJTupVtHuY8) (Plays) | same stream | 0:16:28-0:42:07 | 25.6 min | 0:01-12:07 (12.1 min) | 0.47 | 21 / 3 | about 11.9 h (22:04 → 9 Sep 10:00) |
| [61 SOLO KILLS](https://www.youtube.com/watch?v=Gn1AvcFXl-Y) (main) | [KsDcjdMrBzw](https://www.youtube.com/watch?v=KsDcjdMrBzw), 4 Jul 21:17, 5.1 h | 2:41:53-3:11:37 (lobby from 2:41:40) | 29.7 min | 0:38-13:06 (12.5 min) | 0.42 | 26 / 6 | about 11.7 h (00:29 → 5 Jul 12:08) |
| [64 SOLO KILLS](https://www.youtube.com/watch?v=0inNw0cj1p0) (main) | [YwfDaz6eDrI](https://www.youtube.com/watch?v=YwfDaz6eDrI), 7 Jul 21:18, 5.3 h | 2:46:52-3:14:37 | 27.8 min | 0:42-15:04 (14.4 min) | 0.52 | 26 / 5 | about 11.5 h (00:33 → 8 Jul 12:00) |
| [50 SOLO FINISHES 4.4](https://www.youtube.com/watch?v=ckdrrSD2Y0w) (Plays) | [zpbonbp_tyw](https://www.youtube.com/watch?v=zpbonbp_tyw), 30 Jun 21:13, 6.4 h | 2:14:44-2:43:11 | 28.4 min | 0:17-11:52 (11.6 min) | 0.41 | 24 / 5 | about 11.6 h (23:56 → 1 Jul 11:32) |

**Keep ratio by quarter of match time** (highlight seconds per stream second):

| Highlight | Q1 (landing) | Q2 | Q3 | Q4 (end zones) |
|---|---|---|---|---|
| 72 | 0.38 | **0.09** | 0.54 | 0.70 |
| 55 | 0.32 | 0.29 | 0.58 | 0.68 |
| 51 (Plays) | 0.48 | **0.26** | 0.57 | 0.58 |
| 61 | 0.41 | **0.28** | 0.41 | 0.57 |
| 64 | 0.45 | 0.50 | 0.52 | 0.59 |
| 50 (Plays) | 0.52 | **0.29** | 0.42 | 0.40 |

Source: caption alignment; the 55 row was recomputed by hand after dropping a single stray anchor at 4:55:29.

**Segment table, 72 SOLO KILLS ← wq2fjFmms1U** (highlight order = stream order; "cut before" = stream seconds removed before this piece):

| HL | Stream | Length | Cut before |
|---|---|---|---|
| 0:00-0:04 | other stream IsBYwffTPHE 0:10:26 (cold open) | 4 s | — |
| 0:21-0:22 | 0:05:26 (cold open, "target 70") | 1 s | — |
| 0:49-0:59 | 1:49:10-1:49:20 (landing) | 10 s | lobby, plane and drop (1:47-1:49) removed |
| 1:12-1:31 | 1:49:45-1:50:04 | 19 s | 11 s |
| 1:36 | 1:50:18 | ~5 s | 10 s |
| 1:49-1:51 | 1:51:04-1:51:06 | ~10 s | 33 s |
| 2:39-2:45 | 1:53:32-1:53:38 | 6 s | 108 s |
| 2:49-3:02 | 1:54:16-1:54:29 | 13 s | 34 s |
| 3:10 | 1:54:43 | ~5 s | 6 s |
| 3:16-3:49 | 1:58:59-1:59:32 | 33 s | **250 s** (bot kills, driving, chat with a visitor, choosing Pochinki or the farm) |
| 3:51-3:58 | 2:02:47-2:02:53 | 7 s | **192 s** (recall, vehicles, "30 hue" at 2:00:00, "35 kill aur chahiye" at 2:02:30) |
| 4:09-4:32 | 2:03:22-2:03:48 | 26 s | 18 s |
| 4:38-5:29 | 2:04:12-2:05:04 | 52 s | 18 s |
| 5:33-5:38 | 2:05:19-2:05:25 | 6 s | 12 s |
| 5:45-6:17 | 2:06:33-2:07:05 | 32 s | 61 s |
| 6:26-7:06 | 2:07:26-2:08:07 | 41 s | 13 s |
| 7:17-7:31 | 2:08:55-2:09:26 | ~25 s | 37 s / 16 s |
| 7:40-8:04 | 2:10:01-2:10:25 | 24 s | 27 s |
| 8:06-8:54 | 2:10:36-2:11:24 | 48 s | 8 s |
| 9:02-10:25 | 2:11:46-2:13:09 | 83 s | 14 s |
| 10:30-11:13 | 2:13:25-2:14:08 | 43 s | 11 s ("let's go bro 72 kills" at 2:14:00) |
| 11:22-11:45 | 2:14:20-2:14:44 | 24 s | 4 s; celebration audio continues under WWCD/lobby/facecam visuals |

After 2:14:44 the stream's 2.5 minutes of membership plugs, thanks and replay talk ("72 ka ulta 27…", "80 maar dunga") were all cut — [wq2fjFmms1U captions](https://www.youtube.com/watch?v=wq2fjFmms1U)

**Segment table, 55 NARUTO ← -vMIYNYkLAA** (cold-open lines from 0:14:27 and 2:17:23, then):
- HL 0:51 ← 4:05:20
- 1:08-1:29 ← 4:07:14-34 (cut 96 s)
- 1:43-2:02 ← 4:08:00-19 (12 s)
- 2:09-2:40 ← 4:09:33-4:10:04 (66 s)
- 2:58-3:15 ← 4:13:34-50 (192 s)
- 3:19-3:50 ← 4:15:49-4:16:19 (114 s)
- 3:52-4:13 ← 4:16:26-46 (4 s)
- 4:14-6:01 ← 4:17:07-4:18:54 (20 s)
- 6:21-7:30 ← 4:20:40-4:21:48 (90 s)
- 7:46-8:59 ← 4:23:11-4:24:24 (67 s)
- 9:08-10:01 ← 4:24:57-4:25:50 (23 s)
- 10:05-10:49 ← 4:26:20-4:27:05 (27 s)
- 10:53-11:30 ← 4:27:57-4:28:33 (48 s)
- 11:33-12:06 ← 4:28:52-4:29:25 (16 s)

**Segment table, 61 SOLO KILLS ← KsDcjdMrBzw** (cold open from 0:02:45-0:02:58, then):
- HL 0:38-0:50 ← 2:41:53-2:42:08 (lobby donation read)
- 1:14-1:47 ← 2:43:01-2:44:20 in three pieces (cuts 30, 39, 6 s)
- 2:21-2:46 ← 2:46:35-2:47:00 (102 s)
- 3:08-4:47 ← 2:48:28-2:51:10 in five pieces (cuts 65, 15, 22, 15, 11 s)
- 4:52-5:21 ← 2:52:38-2:53:16 (84 s)
- 5:45-6:12 ← 2:56:46-2:57:14 (187 s)
- 6:38-7:59 ← 2:59:47-3:01:52 (128, 44 s)
- 8:08-8:34 ← 3:02:29-3:02:54 (28 s)
- 8:50-10:17 ← 3:04:13-3:06:28 (63, 49 s)
- 10:26-11:38 ← 3:07:19-3:09:11 (42, 22, 18 s)
- 11:50-13:06 ← 3:09:32-3:11:37 (9, 31, 10, 8 s)

**Condensed, 64 SOLO KILLS ← YwfDaz6eDrI:**
- Cold open from 0:03:44, 0:05:18 and 1:08:44 (an earlier match).
- Match 2:46:52 → 3:14:37 in 26 anchored pieces of 2-111 s, with cuts of 4-112 s (median 19 s).
- The longest pieces: HL 7:47-9:38 ← 3:01:21-3:03:12 (111 s); HL 12:11-13:12 ← 3:09:38-3:10:39 (61 s).
- The last piece, HL 14:39-15:04 ← 3:14:07-3:14:37, is post-match talk ("64 kills… ye screenshot le lo, legendary screenshot hai").

**Condensed, 51 (Plays) ← -vMIYNYkLAA:**
- HL 0:01-0:03 ← 0:16:28 ("ye bhai dekho pehla game chicken hai…", the pre-match lobby talk), then the match in 21 pieces to HL 12:07 ← 0:42:07.
- Cuts of 5-215 s; the largest, 215 s, is at HL 3:06 (stream 22:29 → 26:07).

**Condensed, 50 FINISHES (Plays) ← zpbonbp_tyw:**
- Cold open from 0:03:40-0:03:58 ("aaj thok de… aaj 50 kill to aa hi hai").
- Then HL 0:17 ← 2:14:44 (match start) to HL 11:52 ← 2:43:11, in 24 pieces; cuts of 3-153 s, including 127 s and 131 s gaps in the last third.

- **What was cut, from reading the stream captions in the removed spans** (72-kill match, [wq2fjFmms1U](https://www.youtube.com/watch?v=wq2fjFmms1U)):
  - lobby and plane (1:47-1:49: membership plugs, "best plane");
  - bot kills and looting ("saare bot maar liye", 1:54:40-1:55:30);
  - driving and route choice ("Pochinki loo kya?… farm le raha hoon", 1:57:30-1:58:00);
  - talking with a visiting creator ("kya haal hai bhai, kab aa rahe vapas", 1:57:00);
  - recalls and waiting (1:59:30-2:00:30);
  - post-match plugs and thanks (2:14:44 onward).
  - Some kills were cut too: he announces "30 hue" at 2:00:00 inside a removed span.
- **The match is entered at the landing, not the lobby.** In the 72-kill video the plane and drop are absent apart from one parachute frame; in the 61-kill video the lobby donation read, the plane path and the drop map are kept for about 20 s as setup; in the 64-kill video the drop map appears at 0:39 — storyboards and alignment above.
- **A rough lead-in/lead-out measure.** Kill-call words ("knock", "finish", "down", "kill", "maar diya") inside speech-anchored pieces of 10 s or more:
  - Median time from piece start to the first call: 11-28 s per video (pooled interquartile range about 5-30 s).
  - Median time from the last call to piece end: 2-12 s.
  - The numbers rest on only 2-9 pieces per video.
  - Source: caption alignment (`leadin.py`).

### Inferences
- **Keep ratio rule:** a record match keeps about 45% of its stream time, so a 25-30 min match gives 11-14 min. The ratio rises through the match, roughly 0.4 → 0.25 → 0.5 → 0.65 by quarter.
- **Cut granularity:** the speech-anchored pieces are typically 10-80 s with gaps of 10-60 s, plus 3-7 big jumps of 1-4 min per match where nothing happens (looting, bots, driving, recall, side chat). Music-covered fight montages (the first 2-3 minutes of the 72-kill video) are cut faster than the anchors can show.
- **Lead-in:** keep roughly 10-30 s of call-outs before the first kill of a fight and about 5-10 s after the last kill, then jump. This is weakly measured (see Gaps).
- **Selection inside the session:** only the record match is used; other 40-50+ kill matches in the same stream are either skipped or (once) given to Plays. Selection rests on the headline number, not on the session as a whole.

### Gaps
- The 62-kill zombie video ([Car5bJ_yP-E](https://www.youtube.com/watch?v=Car5bJ_yP-E)) did not match any of the 9 September YouTube streams checked (12, 13, 14 and 17 Sep among them; at most 52 anchors, the noise level). Its captions ask viewers to "follow" and mention "300 followers", which suggests a stream on another platform (for example Kick, whose logo is in his overlay). The source is unconfirmed.
- "Per kill 1000" ([KzSEzZBOpns](https://www.youtube.com/watch?v=KzSEzZBOpns)), "₹5000 per kill sniper" ([7bmUiiUuAdE](https://www.youtube.com/watch?v=7bmUiiUuAdE)) and "₹1000 per kill in scrims" ([3i83F-jSotA](https://www.youtube.com/watch?v=3i83F-jSotA)) were not found in the streams checked. 3i83F appears to be from Jonathan's stream.
- Kill-by-kill lead-in and lead-out could not be measured precisely. Fight audio in the highlight is often under music, so its captions do not match the stream's, and visual matching of 5 s and 10 s storyboards was too noisy. An exact measure needs the frames themselves, which would mean downloading video; that is off-limits.

## 4. Shorts on both channels

### Takeaway
The main channel has effectively stopped posting Shorts: the newest is from 6 Feb 2026, and the one before that from Dec 2024. LoLzZz Plays posts about 2 Shorts a week. Its Shorts are mostly short reactions to esports and to teammates (Jonathan, Spower), funny mode moments and stream chat bits, and only rarely clips of his own records. The one record Short (72 kills) is a 26 s vertical teaser of the final kill → WWCD → MVP proof, with a top caption and an end card pointing to the full video. It was posted 5 hours after the main video.

### Cited Findings
- **LoLzZz Plays, newest 45 Shorts** (13 Oct 2025 to 11 Nov 2026; 41 of them since 18 Jun 2026):
  - median 33 s (interquartile range 27-40 s, range 12-111 s), median 111K views;
  - top: "JONATHAN CAUGHT SLEEPING AT LAN" 3,239,265 views (29 s, [zC2CyyUHKG0](https://www.youtube.com/shorts/zC2CyyUHKG0)) and "LoLzZz REACTION ON HARSH'S MOM EMOTIONAL MOMENT" 1,242,612 (36 s, [iO0BZnnozSQ](https://www.youtube.com/shorts/iO0BZnnozSQ));
  - posting times spread across the day, most often 17:00-20:00 (19:00 ×8, 17:00 ×6) and 09:00-10:00 (×7);
  - they come in topic bursts: 8 "MECCHA CHAMELEON" hide-and-seek Shorts in 18 Jun-2 Jul, esports reactions in Aug-Oct.
  - Source: per-Short metadata.
- **The 72-kill Short** "72 SOLO KILLS WORLD RECORD 💀😱" ([FyHDoGMnHO4](https://www.youtube.com/shorts/FyHDoGMnHO4), 26 s, 115,557 views) went up 25 Oct 2026 at 17:00, five hours after the main video (12:00). Storyboard:
  - Vertical split, with the gameplay crop on top (about 60%) and the stream facecam below (about 40%).
  - Top caption "JUST A NORMAL RECORD" (white, one word in yellow) over the last kills, 0:00-0:10.
  - Scope kill at 0:05; WWCD banner at 0:11-0:12; a yellow wipe transition at 0:13.
  - "THE RECORD…" caption over the lobby with a meme sticker, 0:14-0:17.
  - MVP screen showing "72", 0:18-0:21.
  - Black end card "FULL VIDEO IS ON YOUTUBE / LoLzZz GAMING", 0:22-0:25.
- That same morning (25 Oct 09:30) Plays posted "LoLzZz GAMING CORE 💀" (43 s, [6OfjJ5R7e5E](https://www.youtube.com/shorts/6OfjJ5R7e5E)) — per-Short metadata.
- **Main channel, newest 12 Shorts:**
  - median 49 s (range 21-60 s), median 739K views, mostly posted at 12:00-13:00.
  - Single clutches and sniper shots ("Sniper God bolte!" 1,764,167 views, 22 s, [E2lr611OqRc](https://www.youtube.com/shorts/E2lr611OqRc)), plus two sponsor Shorts (realme, Boult).
  - The latest, "1v4 CLUTCH IN BGIS ROUND 2" (46 s, [OqEMk59-Z1o](https://www.youtube.com/shorts/OqEMk59-Z1o)), is gameplay on top with tournament handcam below for 0:00-0:20, then full-height gameplay; a black-and-white freeze with a skull emoji on the death (0:28-0:29); no text caption.
  - Source: per-Short metadata and storyboard.
- Plays Shorts carry the stream description template (Streamlabs link, Instagram, Twitter, chat rules) — [qxX7OBsUino](https://www.youtube.com/shorts/qxX7OBsUino) metadata.

### Inferences
- For his own record, the Short is a **trailer for the long video**, built from its last 20 seconds: final kills, the WWCD banner, then the MVP screen with the number, plus a one-line ironic caption and a "full video on YouTube" end card. The cold open is not reused for it. The Short goes up the same afternoon, after the long video.
- Most of the Shorts volume is not highlight-derived. It is reaction and personality content, which Kaatclip's match pipeline would not produce.

### Gaps
- Only the newest 45 Plays Shorts and 12 main Shorts were timed and dated, out of 390 and 107.
- Only 2 Shorts were inspected frame by frame.

## 5. Upload practice: titles, thumbnails, descriptions, timing, what performs

### Takeaway
Highlights go up the next day: main channel at 12:00 IST, Plays at 09:00-10:00 IST, about 12 hours after the record match. Titles and thumbnails are templates shared by both channels: the number first, "WORLD RECORD", his "shh" studio photo, a gameplay card and a shocked emoji. Main-channel record videos ship with no description or tags at all; Plays videos ship with the stream description template. Record videos draw several times the comments of other formats, and among records, views track the novelty of the number (a new personal best) more than its size.

### Cited Findings
- **Upload times:**
  - Main highlights: 12:00 (72, 64, 62, 55 Naruto 12:10, 61 12:08, 100-in-3, 94-squad, 80-squad and others), with a few at 12:30-14:30.
  - Plays highlights: 09:00-10:00 (51 at 10:00, ₹5000 at 10:00, reactions at 09:00-09:42), with 50-in-4.4 at 11:32.
  - Source: per-video `timestamp`, e.g. [-qpx-ejuq9Q](https://www.youtube.com/watch?v=-qpx-ejuq9Q), [EJTupVtHuY8](https://www.youtube.com/watch?v=EJTupVtHuY8)
- **Delay from match to upload:** 11.5-12.5 h in 5 of the 6 mapped cases; 34 h for the 55-kill video, posted the day after Plays posted the 51-kill match from the same stream (table in section 3).
- **Descriptions and tags:**
  - 72, 62, 64 and 55 have empty descriptions; 72, 62, 55 and per-kill-1000 have no tags.
  - 61 has a title repeat, an Instagram link, "#lolz #61KILLS #bgmi" and 6 tags.
  - Plays videos use the stream template ("Support the stream: streamlabs.com/…", Instagram, Twitter) and 6 identical channel tags.
  - No chapters anywhere; language "hi".
  - Source: yt-dlp metadata of [Gn1AvcFXl-Y](https://www.youtube.com/watch?v=Gn1AvcFXl-Y), [EJTupVtHuY8](https://www.youtube.com/watch?v=EJTupVtHuY8) and others.
- **Thumbnail template** (8 inspected: 55, 51, 61, 64, 50-in-4.4, ₹5000, 62, ₹1000):
  - The same studio photo of him (white tee, glasses, finger-to-lips "shh" or adjusting glasses) on one side.
  - A rounded gameplay card on the other side.
  - Two-line text: "N SOLO KILLS" in yellow over "WORLD RECORD!!" in white, in a heavy condensed italic.
  - A shocked emoji and a "rex" designer watermark.
  - Cash challenges replace the second line with "PER KILL 5000 INR CHALLENGE" and add the donation card ("LOLZZZ KA FAN HU ₹5000.00 – HAR KILL PE 5000 RS CHALLENGE") with a red arrow. The ₹1000 scrims thumbnail has Jonathan fanning cash.
  - The Plays thumbnails are indistinguishable from the main channel's.
  - Source: [55](https://i.ytimg.com/vi/fbVXWfefL8c/hqdefault.jpg), [51](https://i.ytimg.com/vi/EJTupVtHuY8/hqdefault.jpg), [₹5000](https://i.ytimg.com/vi/7bmUiiUuAdE/hqdefault.jpg)
- **Title templates:**
  - Main: "I MADE A (NEW) WORLD RECORD OF N SOLO KILLS (IN mode/update) | {persona tag: CLASSIC HACKER OR WHAT / TAG LoLzZz OR WHAT}".
  - Plays: the same, plus emojis and "TAG LoLzZz" ("I MADE A WORLD RECORD OF 51 SOLO KILLS IN BGMI | TAG LoLzZz NEW EVENT RECORD 😱").
  - Cash challenges: "I GOT ₹N PER KILL WITH {weapon} CHALLENGE AND THIS HAPPENED..😱".
  - Source: the videos tabs.
- **Performance:**
  - Main records 2026: 72 → 990,648 views and 1,100 comments; 61 → 751,570 and 1,600; 62 → 595,971 and 354; 64 → 484,187 and 1,200; 55 → 360,625 and 310; 50-in-4.3 → 238,624 and 385.
  - Plays: ₹5000-per-kill 365,038 (the channel's best 2026 gameplay video); 51 → 265,859; 50-in-4.4 → 184,882.
  - Likes per view are highest on the 61 (6.0%) and 64 (7.2%) videos, against 3.0% on the 72 and 2.9% on the 55 and 62.
  - Source: yt-dlp `view_count`, `like_count`, `comment_count`.

### Inferences
- Views follow "new personal best" status:
  - The 61 (first past 60 in that run) and the 72 (all-time best) beat the 62 and 64, which came days after a similar number.
  - The 55 posted after the Plays 51 from the same night did worst of the main records.
  - A Kaatclip title and cover generator should flag "new personal best" as the hook and avoid posting two near-identical numbers in a row on one channel.
- The empty descriptions on the main channel mean packaging effort goes into the title and thumbnail only; Kaatclip can skip description generation for this creator style (low value).

### Gaps
- Retention, CTR and the impressions source are private. "Why" a video did well is inferred from public counts only.
- How the thumbnail photo was made (a separate shoot, judging by the identical pose and clothes across videos) was not verified.

## 6. Rules an automatic editor could follow to make LoLzZz-style challenge highlights

### Takeaway
Treat the highlight as one match, chosen by its headline number, told in order at about 45% of its length. Use a 30-60 s cold open stitched from the stream's own goal line, teaser kills and the final catchphrase. Cut the mid-game hardest and the end zones least. Add a garnish insert every 1-2 minutes, end on the game's own proof screens plus the facecam celebration, and post it the next day with a templated number-first title and thumbnail and a 20-30 s vertical teaser. Everything below is **inference** from the measurements above. Numbers marked (m) are measured; the rest are design choices.

### Cited Findings
- The measured inputs for these rules are in sections 2 and 3 (keep ratios and quarter profiles from the six mappings; cold-open sources; end sequences; upload delays). Representative sources: [-qpx-ejuq9Q](https://www.youtube.com/watch?v=-qpx-ejuq9Q) ← [wq2fjFmms1U](https://www.youtube.com/watch?v=wq2fjFmms1U); [Gn1AvcFXl-Y](https://www.youtube.com/watch?v=Gn1AvcFXl-Y) ← [KsDcjdMrBzw](https://www.youtube.com/watch?v=KsDcjdMrBzw); [fbVXWfefL8c](https://www.youtube.com/watch?v=fbVXWfefL8c) and [EJTupVtHuY8](https://www.youtube.com/watch?v=EJTupVtHuY8) ← [-vMIYNYkLAA](https://www.youtube.com/watch?v=-vMIYNYkLAA).

### Inferences
**A. Selection**
1. Split the stream into matches. Lobby/plane → landing → … → WWCD, death or spectate → results/MVP → lobby. In event modes, a parachute mid-match after a recall is **not** a new match (m: recall drops in 3 of the videos).
2. Score each match by its final kill count (HUD/MVP OCR). Make a "record" highlight when a match beats the creator's previous best, or clears the goal parsed from the stream title or speech ("70 SOLO KILLS TODAY?", "mera target 70 hai") (m: titles state the goal; highlights are made only on headline numbers).
3. If a session has two qualifying matches, make the best one the main highlight and offer the other as a secondary or second-channel cut (m: 8 Sep stream → 55 main, 51 Plays). Skip other similar matches.
4. Multi-match challenges ("100 in 3", "per kill ₹N" with a donation goal) use every match of the challenge in order. Each match gets about 5-9 min (m: 5.4, 8.4 and 7.9 min).

**B. Cold open (target 30-60 s; measured median about 0:39, range 0:29-1:09)**
1. Open on 0.5-1 s of black.
2. Then a full-screen crop of the stream facecam saying the day's goal. Take it from the first 15 minutes of the stream, or from the previous day's stream if the goal ran over several days (m: lines from 0:02:45-0:14:27 into the stream; the 72 open borrowed from the previous day). Optionally black-and-white.
3. Then 2-3 teaser shots of 3-5 s each (scope kills, the multi-kill), cut against facecam reactions.
4. Then the record catchphrase or the final number from the end of the match, over music (m: "…record tere bhai ka 64", "let's go 55"). Optionally flash the MVP screen as a spoiler (m: the 61 open).
5. 0.5-1 s of black, then the match. Keep a donation or challenge read from the lobby if one exists, as stakes (m: the 61 "token for 51 kills").

**C. Body (chronological, about 45% keep)**
1. Start at the landing, or at the drop map plus parachute (a 5-20 s bridge). Drop the lobby, plane talk and plugs (m).
2. Keep ratio by quarter of match time: about 0.4 / 0.25 / 0.5 / 0.65 (m, median of six). A 25-30 min match lands at 11-14 min (m: 10.6-14.4 min of gameplay).
3. Keep pieces of 10-80 s around fights. Start a piece about 10-30 s before the first kill or knock of a fight (the call-outs: "upar hai, do squad upar"), and end it about 5-10 s after the last kill. Merge fights less than about 20 s apart. The lead-in and lead-out numbers are weakly measured.
4. Drop the following, replacing them with a hard cut (no card): bot-only kills, looting, driving with no enemies, route discussion, side chat with visitors or chat, recalls, waiting (m: the content of the 250 s and 192 s cuts in the 72-kill match).
5. Keep the running count lines he speaks ("35 kill aur chahiye", "saat kill aur") when they fall in kept pieces; they replace an on-screen counter (m: no counter overlay seen).
6. Inserts:
   - one every 60-120 s in the first half: a meme cutaway of 2-4 s with a name label ("ENEMY :", "IGL", the squad names), or a 2-5 s full-screen facecam punch-in right after a multi-kill;
   - a colour-bars or whip transition at most 1-2 times per video;
   - the strongest mid-match squad wipe should fall around 40-65% of the runtime (m: the global heatmap maximum sits at 40-66% in 8 of 13).
   - For Kaatclip, use only licence-safe or creator-supplied meme clips; the labelled-meme habit is the part with copyright risk.

**D. Ending (about 40-75 s after the record kill; m)**
1. The final kill, with a zoom or punch-in.
2. Full-screen facecam celebration with the catchphrase (5-20 s).
3. The game's WWCD screen (3-10 s), then the MVP screen showing the kill count (5-15 s); the results table for squad or multi-match challenges.
4. A short facecam reflection ("57 tha ye…", "always on top").
5. 5-10 s of black for YouTube end-screen elements.
6. Cut all post-match plugs, thanks and lobby chatter after that.

**E. Packaging and timing**
1. Title: "I MADE A (NEW) WORLD RECORD OF {N} SOLO KILLS (IN {mode/update}) | {creator tag} OR WHAT". Cash variant: "I GOT ₹{N} PER KILL ({weapon}) CHALLENGE AND THIS HAPPENED..😱".
2. Thumbnail: creator cutout (a reused pose), a rounded gameplay frame, "{N} SOLO KILLS" in yellow over "WORLD RECORD!!" in white, one shocked emoji. For challenges, add the donation card and an arrow.
3. Description and tags optional; no chapters.
4. Publish at about 12:00 the day after the stream (about 12 h after the match). Publish a 20-30 s vertical teaser the same day, about 5 h later, made from the final kills, the WWCD banner and the MVP screen, with a top caption and a "full video on YouTube" end card.
5. Don't post two near-identical numbers on one channel within a few days; send the lesser one to a secondary channel or skip it.

**F. What Kaatclip must detect to do this**
- Match boundaries (including recall).
- The HUD kill count over time and the final count from the MVP screen.
- Fight windows from kill and knock times.
- The goal line and catchphrase from the transcript (Hindi/Hinglish).
- WWCD, MVP and results screens.
- The facecam rectangle (for full-screen punch-ins).
- Dead time: bots, looting, driving and chat, from the absence of kills and enemy call-outs.

### Gaps
- These rules come from one creator's challenge format. Six source mappings back the cut ratios, and thin, partly music-masked caption evidence backs the lead-in and lead-out seconds. Kaatclip's own test streams should tune the per-fight lead-in/out, the insert frequency and the quarter keep ratios before they are fixed.
- How music is mixed (level under comms, when it drops out) could not be measured without audio.
