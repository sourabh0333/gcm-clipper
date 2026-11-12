# Goblin deep study: how @goblinbgmi and @goblinsh0rts make, cut and upload BGMI highlights

Method (12 Nov 2026). Public YouTube data only, read with yt-dlp `--skip-download`; no video or audio was downloaded. Sources used: full metadata for 79 main-channel videos, 30 streams (7 Dec 2025 to 10 Nov 2026) and 4 main-channel Shorts; the flat list of all 526 long videos and 438 Shorts on the second channel; full metadata for 129 second-channel long videos (29 Aug 2025 to 11 Nov 2026) and 20 Shorts (25 Jun to 29 Oct 2026); Hindi auto-captions for 61 highlight videos and Shorts plus 21 full streams; and storyboard preview mosaics (the "sb0" images, one frame every 2 to 5 s in videos and every 10 s in streams) for 29 videos and 3 stream sections. These were viewed as contact sheets.

Source mapping works by aligning captions. Every 3-word sequence of a highlight's Hindi captions is looked up in the stream's captions. A stretch of the highlight counts as cut from a stream section only when at least 3 sequences in a row agree on the same time offset (±1.5 s). Real pairs scored 127 to 603 agreeing anchors. Non-pairs scored at most 63 (usually under 30).

All views are as of 12 Nov 2026 and all times are IST. "Heatmap" means YouTube's "most replayed" curve (100 bins). Scratch data, scripts and contact sheets are in `C:\Users\soura\AppData\Local\Temp\claude\21027423ba80eb72\ab9e7281-b606-4050-82cb-606e6c8ce9f9\scratchpad\yt_research\goblin_deep\`. This study extends `research_notes/BGMI highlight video structure/goblin_esports.md` and does not repeat it.

## 1. Inventory: what each channel uploads, how often, and how the two split the work

### Takeaway
The two channels run two different highlight pipelines. **The main channel (@goblinbgmi) never cuts its highlights from the YouTube livestream.** It posts about one highlight a month (2 to 5 in busy months), made from a clean on-device screen recording of a tournament or scrims match, with comms, branding and a teaser opening. **The second channel (@goblinsh0rts, "GoBLiN shorts") is the stream-cutting channel.** It posted 8 to 23 long videos a month in 2026: matches cut straight from his YouTube (and probably Kick) streams with the stream overlay left in, plus LAN broadcast cuts, vlogs, TDM/WOW customs, crate openings, funny edits and about 5 Shorts a month.

### Cited Findings
- Main-channel uploads, 79 videos from May 2023 to Aug 2026, grouped by title: 57 match or tournament highlights (median 381 s, middle half 298 to 503 s, median 148K views); 7 frag or clutch montages (median 255 s, 116K); 4 TDM/WOW custom-room videos (median 594 s, **360K, the best median**); 3 vlogs; 8 others — [@goblinbgmi/videos](https://www.youtube.com/@goblinbgmi/videos) (keyword grouping of yt-dlp titles)
- Main-channel long uploads per month, Aug 2025 to Nov 2026: 1, 0, 0, 3, 5, 1, 2, 0, 1, 1, 2, 0, 4, 0, 0, 0. They cluster after tournaments (5 in Dec 2025, 4 in Aug 2026 around BGMS) — [@goblinbgmi/videos](https://www.youtube.com/@goblinbgmi/videos)
- Streams: 80 on the Streams tab. The last 30 (Dec 2025 to Nov 2026) are 25 min to 9.75 h long (median 4.45 h). Per month from Dec 2025: 5, 1, 5, 2, 2, 6, 4, 1, 1, 0, 2, 1. 20 of 30 started between 19:00 and 21:00 IST. Typical title: "Scrims Live w iQOOSouL | GoBLiN is Live BGMI!" plus a UC crate-opening hook — [@goblinbgmi/streams](https://www.youtube.com/@goblinbgmi/streams)
- Second channel, all 526 long videos by title: 174 match or tournament highlights (median 196 s, middle half 112 to 336 s, median 26K views); 143 frag or clutch cuts (median 65 s, 26K); 43 funny or banter edits (123 s, 44K); 32 TDM/WOW customs (318 s, 66.5K); 22 vlogs or LAN journeys (621 s, 59.5K); 16 crate openings (360 s, 27.5K); 12 reactions (182 s, 27K); 9 interviews (204 s, 16K); 75 others — [@goblinsh0rts/videos](https://www.youtube.com/@goblinsh0rts/videos)
- Second-channel long uploads per month (129 dated videos), Sep 2025 to Oct 2026: 4, 6, 4, 3, 5, 6, 10, 2, 11, 17, 23, 12, 14, 8 (3 so far in Nov). The peak (Jun to Sep 2026) is the "Team Goblin" and PMGC-grind period, with many stream cuts — [@goblinsh0rts/videos](https://www.youtube.com/@goblinsh0rts/videos)
- The second channel has 438 Shorts (flat listing; median 83K views; top: "Revenge 💯🚀" 4.5M, [DfOcogRMngg](https://www.youtube.com/shorts/DfOcogRMngg)). Of the 20 most recent, 25 Jun to 29 Oct 2026, that is about 5 a month — [@goblinsh0rts/shorts](https://www.youtube.com/@goblinsh0rts/shorts)
- The main channel has 4 Shorts in total (2021 to 2026) — [@goblinbgmi/shorts](https://www.youtube.com/@goblinbgmi/shorts)
- No main-channel highlight matches a YouTube stream. 16 main-channel highlights from Nov 2025 to Aug 2026 were caption-aligned against all 30 streams of that period; the best score was 63 against 127 to 603 for real pairs, so none was cut from them. Their frames confirm a separate source: 1920x888, 3630-3840x1768 or 3840x2160 video (phone-screen shapes), with no stream banner and no facecam. Example: "Solo 14 Finishes | 29 Team Finishes" (24 Feb 2026, [ml5FitUoqf8](https://www.youtube.com/watch?v=ml5FitUoqf8)) does not match the 21 Feb scrims stream ([yUuB2x9H0Qg](https://www.youtube.com/watch?v=yUuB2x9H0Qg)), although three second-channel videos do — this study's alignment
- Second-channel videos matched to YouTube streams (anchor score in brackets): [wDgeZBn80VM](https://www.youtube.com/watch?v=wDgeZBn80VM)←[GVKHZ9-erB8](https://www.youtube.com/watch?v=GVKHZ9-erB8) (603); [-acpEOsyT7k](https://www.youtube.com/watch?v=-acpEOsyT7k), [5zW1ag4_d_o](https://www.youtube.com/watch?v=5zW1ag4_d_o) and [yucF5hCgl8o](https://www.youtube.com/watch?v=yucF5hCgl8o)←[yUuB2x9H0Qg](https://www.youtube.com/watch?v=yUuB2x9H0Qg) (346, 410, 314); [QF7VlJj-QZs](https://www.youtube.com/watch?v=QF7VlJj-QZs)←[7dUemvoJ1c0](https://www.youtube.com/watch?v=7dUemvoJ1c0) (435); [4cC844SCxUk](https://www.youtube.com/watch?v=4cC844SCxUk)←[AF_iszEug90](https://www.youtube.com/watch?v=AF_iszEug90) (127); [pdG-_XDypV4](https://www.youtube.com/watch?v=pdG-_XDypV4) and [nE67VClXWkM](https://www.youtube.com/watch?v=nE67VClXWkM)←[ghOiRl4hTk0](https://www.youtube.com/watch?v=ghOiRl4hTk0); [d-6B6fjDZSE](https://www.youtube.com/watch?v=d-6B6fjDZSE) and [aRwYyMCIUCI](https://www.youtube.com/watch?v=aRwYyMCIUCI)←[a4ZMq65OxGU](https://www.youtube.com/watch?v=a4ZMq65OxGU); [JXSFHpiHkS0](https://www.youtube.com/watch?v=JXSFHpiHkS0)←[mNRHxGdiRCU](https://www.youtube.com/watch?v=mNRHxGdiRCU); [UbdXp3UzFAA](https://www.youtube.com/watch?v=UbdXp3UzFAA)←[8gvGjQFygOM](https://www.youtube.com/watch?v=8gvGjQFygOM) (195); [Q_5n1fA6MO8](https://www.youtube.com/watch?v=Q_5n1fA6MO8) and [j6kf-4MXXDc](https://www.youtube.com/watch?v=j6kf-4MXXDc)←[xz-_mzU_UPE](https://www.youtube.com/watch?v=xz-_mzU_UPE) (279, 291); crate openings [1WPEK9prb2k](https://www.youtube.com/watch?v=1WPEK9prb2k)←[jzoF9i3ERIA](https://www.youtube.com/watch?v=jzoF9i3ERIA) and [8uTVdSeesys](https://www.youtube.com/watch?v=8uTVdSeesys)←[7dUemvoJ1c0](https://www.youtube.com/watch?v=7dUemvoJ1c0)
- Some second-channel highlights show the stream layout (the "iQOO 15R" banner and a facecam) but match no YouTube stream. Examples: "25 Kills Chicken Dinner in Practice Scrims | Solo 9 Kills" (110K, [6TnQbdev9Oo](https://www.youtube.com/watch?v=6TnQbdev9Oo)) and "Solo 14 Finishes Scrims" ([FAJBnkTxaAM](https://www.youtube.com/watch?v=FAJBnkTxaAM)). One second-channel Short's description links "Kick - https://kick.com/soulgoblin" ([eTf7izIhEiA](https://www.youtube.com/watch?v=eTf7izIhEiA))
- Second-channel LAN videos (BGMS, BMSD) are cut from the official broadcast VOD: observer camera, team-standings sidebar, player-cam inset, "REPLAY" stings, a "GRAND FINALS ... MATCH 14 – ERANGEL" card, and Hindi caster audio (100% of seconds have speech, about 200 words a minute). Examples: [xtE3WWqt1_E](https://www.youtube.com/watch?v=xtE3WWqt1_E), [5oGAOwgtrK8](https://www.youtube.com/watch?v=5oGAOwgtrK8), [7uZM0hKn5Yc](https://www.youtube.com/watch?v=7uZM0hKn5Yc), [DLYH7QGTmTk](https://www.youtube.com/watch?v=DLYH7QGTmTk)

### Inferences
- The split maps directly onto Kaatclip: **one premium "hero" match highlight** (main-channel style: teaser, branding, clean feed) and **many quick stream cuts** (second-channel style: one match or one funny run, with the stream overlay kept). The quick cuts are close to what Kaatclip can automate today. The hero edit adds a few graphic layers on top of the same cut list.
- One scrims stream regularly yields 2 or 3 second-channel videos. The 21 Feb 2026 stream gave a WWCD match, a #2 match and an Ultimate Royale match, uploaded over 3 days. The 2 Jun stream gave a 1v2 TDM, a 4v4 WOW video and a crate opening. **The highlight unit is "one match", and a stream yields several.**

### Gaps
- Who edits either channel is not public. Recent Shorts credit outside editors in the description ("Edit by - https://www.instagram.com/p/…", e.g. [3gtSMtb1osg](https://www.youtube.com/shorts/3gtSMtb1osg)), so at least the Shorts are partly fan- or team-made.
- The 50 older streams (before Dec 2025) were not dated, and Kick streams could not be checked. Source mapping for the stream-layout videos that match no YouTube stream is therefore open.
- The groupings come from title keywords and are approximate (the "other" bucket holds 75 second-channel videos).

## 2. Editing anatomy of 15+ highlights (structure, graphics, camera, audio, ending)

### Takeaway
There are three edit grammars. **(A) Main-channel hero match highlight:** a 15 to 25 s teaser of later fights under a text label ("in this video -" or a glitchy "COMING SOON"), then a black beat or logo card, then the parachute, then the match in order with comms on top, ending on the WWCD banner and in-game MVP screen. It is phone POV, often inside a branded red side panel, with no facecam. **(B) Second-channel stream cut:** no graphics at all. The stream frame (game plus the "iQOO 15R" banner plus a small facecam) is cut fight to fight in order, starting at a call before the first fight and ending on the result screen plus 15 to 30 s of reaction. **(C) LAN broadcast cut:** observer footage with caster audio and broadcast cards. Fights are kept whole. The cut points remove looting, driving without contact, scoping without kills, lobby and plane time.

### Cited Findings
Measured openings, from storyboards and captions (frames are about 5 s apart):
- "Solo 8 Finishes Chicken Dinner | 14 Total Finishes" (553 s, [-vFxWHPrv2s](https://www.youtube.com/watch?v=-vFxWHPrv2s)): 0:00 to 0:25 is a teaser of the final fight (orange car, smoke) with a glitchy "COMING SOON" text overlay. Its caption "…एक था ना" at 0:12 recurs at 7:50 in the final fight. The parachute and match start come at 0:29
- "Solo 10 Finishes Rondo gameplay" (490 s, [deJt870ksiE](https://www.youtube.com/watch?v=deJt870ksiE)) and "CEGC comeback match 15 finishes" (489 s, [lBswYFSS_rQ](https://www.youtube.com/watch?v=lBswYFSS_rQ)): a yellow "in this video -" label over a 15 to 20 s teaser. Its captions recur later: deJt870ksiE's 0:00 to 0:08 at 3:27 to 3:35, and lBswYFSS_rQ's "खत्म भाई खत्म" at 0:12 at 7:42. Then a black beat at about 0:20 and the parachute at about 0:25
- "CEGC Tournament Highlights Erangle + Miramar" (573 s, [KmjTasCQZ5U](https://www.youtube.com/watch?v=KmjTasCQZ5U)): a teaser (its 0:06 to 0:08 recurs at 4:40), then official broadcast frames with a "MATCH 2" lower-third card (about 0:20 to 0:25), black, then the parachute at about 0:35
- "Drx 🇰🇷 v/s Team iQOOSouL 🇮🇳 | 4v4 Pov" (384 s, [MQ8SC-_e8ZQ](https://www.youtube.com/watch?v=MQ8SC-_e8ZQ)): fight teaser from 0:00 to 0:20, a black card with a "Goblin" signature logo at 0:25, then gameplay. Heatmap at 0:00 is 0.89
- "Team SouL Domination | Solo 14 Kills WWCD" (2023, [OOnDKF-Wprs](https://www.youtube.com/watch?v=OOnDKF-Wprs)): teaser from 0:00 to 0:20, black, then the parachute with a big "Pecado" drop-location text at 0:30. "17 Finishes CD" ([Qws8NHx-_t4](https://www.youtube.com/watch?v=Qws8NHx-_t4)) opens instead with about 15 s of stylised cinematic shots (character, birdcage, aerial map); heatmap 0:09 to 0:19 is 0.99 to 1.00
- Two main-channel videos open with no teaser, straight on the parachute: "31 Finishes WWCD Solo 11" ([bsezq1RtU7k](https://www.youtube.com/watch?v=bsezq1RtU7k)) and "Solo 14 Finishes | 29 Team Finishes" ([ml5FitUoqf8](https://www.youtube.com/watch?v=ml5FitUoqf8)). The 2023 hit "Sanhok Domination" (604K, [67w15TWdikI](https://www.youtube.com/watch?v=67w15TWdikI)) opens on 5 s of broadcast footage with a "Champions Cup DAY 2 – MATCH 3" card, then the POV from mid-match
- Count across the 9 main-channel highlights whose openings were viewed: 6 have a teaser (5 recycled from later fights, 1 cinematic), 2 open on the parachute, and 1 opens on a broadcast card

Measured endings:
- Main channel: the WWCD banner, then the in-game "MVP" animation, then the team lobby or scoreboard, then the end. bsezq1RtU7k: WWCD 7:41, MVP 7:46, lobby 7:51, scoreboard 7:56, end 8:06. ml5FitUoqf8: WWCD 5:40, MVP 5:50, end 6:05. -vFxWHPrv2s: WWCD 8:48, MVP 8:58, end 9:13. That is about 15 to 25 s after the winning kill
- "SOLO WWCD And BGMS Highlights" (313 s, [6jIQaYvIOGc](https://www.youtube.com/watch?v=6jIQaYvIOGc)) ends on two editor zoom-ins: the minimap ("Fact…", 5:08) and the "#1 WINNER WINNER CHICKEN DINNER" banner (5:13). Its heatmap ends high (5:01 to 5:07 at 0.89 to 0.95)
- "Highlights BMPS 2026 | Onto Finals" (671 s, [nk3MGVXKCFo](https://www.youtube.com/watch?v=nk3MGVXKCFo)) is a different format: a multi-match frag reel. Map and skin change every 5 to 15 s, it has no result screen, and it cuts to black at 11:06
- Second-channel stream cuts end on the result screen plus the reaction: "#2 Congratulations on getting 2nd place" plus 18 s of comms ([wDgeZBn80VM](https://www.youtube.com/watch?v=wDgeZBn80VM)); WWCD plus MVP plus a stream transition (about 22 s after the last kill, [-acpEOsyT7k](https://www.youtube.com/watch?v=-acpEOsyT7k)); a 20 s facecam reaction after the #2 screen ([5zW1ag4_d_o](https://www.youtube.com/watch?v=5zW1ag4_d_o)); a facecam zoom at 8:17 to 8:27 ([4cC844SCxUk](https://www.youtube.com/watch?v=4cC844SCxUk))

On-screen graphics and camera:
- Main channel, Dec 2025 to Feb 2026: a red branded panel down the left of the frame (iQOO logo, team crest, a cartoon of Goblin) around the phone recording, on every frame — [-vFxWHPrv2s](https://www.youtube.com/watch?v=-vFxWHPrv2s), [bsezq1RtU7k](https://www.youtube.com/watch?v=bsezq1RtU7k), [ml5FitUoqf8](https://www.youtube.com/watch?v=ml5FitUoqf8). In 2026 tournament videos the phone recording fills the frame (the phone's notch pill is visible at the left edge, [6jIQaYvIOGc](https://www.youtube.com/watch?v=6jIQaYvIOGc))
- Banter pop-ups in the main highlight: in -vFxWHPrv2s, at 1:09 and 1:23 a cut-out of a teammate's face appears with a green subtitle quoting the line ("Joker to jaa raha hai na bhai", "shirtless dikh gaya na bhai"). A short meme or real-life clip is inserted at 0:59 — [-vFxWHPrv2s](https://www.youtube.com/watch?v=-vFxWHPrv2s)
- No kill counter, scoreboard overlay or chapter markers were seen on any of the 29 storyboarded videos. The in-game HUD (kill feed, "Remaining N", team kills) carries the stats
- Camera: always the player's own POV on the main channel, including dead time spent scoping or holding a rock. 67w15TWdikI keeps about 85 s of holding behind one rock (3:47 to 5:12), and even a phone control-centre frame at 0:44 ([67w15TWdikI](https://www.youtube.com/watch?v=67w15TWdikI)). Spectator or observer footage appears only in broadcast cuts and in short broadcast cards
- Audio: captions show comms over most of each video. Words a minute and share of seconds with speech: bsezq1RtU7k 130 wpm / 76%; KmjTasCQZ5U 123 / 71%; ml5FitUoqf8 100 / 65%; -vFxWHPrv2s 82 / 61%; the stream cut wDgeZBn80VM 159 / 85%. Lower values (40 to 50%) mark music-backed frag reels: nk3MGVXKCFo 51 wpm, khbJdsEChm0 42, WetiQFqJ3W8 51. The 2023 LAN video OOnDKF-Wprs is all music (23 caption words in 516 s). Only one description credits music: CC-BY-NC "Makai Symphony – Dragon Castle" via BreakingCopyright on a vlog ([cWxjZSKKHuM](https://www.youtube.com/watch?v=cWxjZSKKHuM))

Heatmap peaks of 0.6 or more, in seconds (main channel):
- [deJt870ksiE](https://www.youtube.com/watch?v=deJt870ksiE): 58, 147 to 151, 279, 323 to 328, and 470 to 475 (1.0)
- [lBswYFSS_rQ](https://www.youtube.com/watch?v=lBswYFSS_rQ): 78, 234, and 459 to 469 (1.0, the "khatam" final fight)
- [ml5FitUoqf8](https://www.youtube.com/watch?v=ml5FitUoqf8): 332 to 343 (1.0, just before the WWCD at 340)
- [bsezq1RtU7k](https://www.youtube.com/watch?v=bsezq1RtU7k): 466 to 471 (1.0, the end fight)
- [xWvORedYbOs](https://www.youtube.com/watch?v=xWvORedYbOs): 241 to 251 (1.0)
- [PiGMtVEVJKw](https://www.youtube.com/watch?v=PiGMtVEVJKw): 0 to 2 (0.84) and 209 to 249 (1.0)
- [4rDLrncqmCc](https://www.youtube.com/watch?v=4rDLrncqmCc): 0 to 9 (1.0) and 138 to 146
- [-vFxWHPrv2s](https://www.youtube.com/watch?v=-vFxWHPrv2s): 44 to 60 (1.0, the first fight plus the banter pop-ups) and 481 to 487
- [KmjTasCQZ5U](https://www.youtube.com/watch?v=KmjTasCQZ5U): 396 (1.0)

Minute by minute (selected):
- **[-vFxWHPrv2s](https://www.youtube.com/watch?v=-vFxWHPrv2s) (553 s, 108K, Dec 2025, main):** 0:00 to 0:25 teaser of the final fight with "COMING SOON"; 0:29 parachute; 0:34 to 0:49 landing, loot and first shots; 0:49 to 0:59 drive; 0:59 meme insert; 1:04 to 1:33 loot and banter with two face-sticker subtitles; 1:38 to 2:23 a long drive across the bridge (kept, comms continue); 2:28 to 2:47 scope fight; 2:52 to 3:50 vehicle fight with smokes and heals ("हील करो… स्मोक कर दे"); 3:57 to 5:15 compound fight with grenades ("नेड डाल"), "फिनिश भी हुआ"; 5:15 to 6:30 holding a building; 6:35 to 7:30 holding a roof and scope shots; 7:34 to 8:43 final circle (car push, smoke, the "नेड करके मार… एक था ना" finish); 8:48 WWCD; 8:58 MVP; 9:03 lobby; 9:13 end
- **[bsezq1RtU7k](https://www.youtube.com/watch?v=bsezq1RtU7k) (486 s, 179K, main):** 0:00 parachute; 0:09 to 1:48 hot-drop compound fight (about 100 s); 1:52 to 2:02 drive and map check; 2:07 to 2:32 ridge fight; 2:37 to 3:31 wall fight; 3:36 to 4:00 drive; 4:00 to 4:44 scope fights; 4:54 map ("Neox Factory"); 5:00 to 5:24 drive; 5:24 to 6:32 fights; 6:37 to 7:36 final zone with the car; 7:41 WWCD; 7:46 MVP; 7:51 lobby; 7:56 scoreboard; 8:06 end
- **[6jIQaYvIOGc](https://www.youtube.com/watch?v=6jIQaYvIOGc) (313 s, 272K, BGMS LAN, main):** 0:00 to 0:58 three short fights from other matches (a montage opener; heatmap 0:00 to 0:12 at 0.83 to 1.0); 0:58 to 1:13 cut to the winning match; 1:13 to 5:03 that match's endgame nearly continuous (blue car, smoke fight 1:47 to 2:21, about 20 scope shots, the final crawl 4:19 to 4:58); 5:08 zoom on the minimap; 5:13 zoom on the WWCD banner; end
- **[xtE3WWqt1_E](https://www.youtube.com/watch?v=xtE3WWqt1_E) (287 s, 39K, BMSD LAN broadcast, second channel):** 0:01 to 0:09 broadcast plane path and map card; 0:11 to 2:12 observer camera on iQOOSouL with the standings sidebar and player-cam inset; 2:14 to 2:24 broadcast "REPLAY" and a total-points table; 2:50 to 3:04 a split card ("MATCH 14 – ERANGEL" plus minimap); 3:06 onward the end fights to the WWCD; caster commentary throughout
- Stream cuts [wDgeZBn80VM](https://www.youtube.com/watch?v=wDgeZBn80VM), [-acpEOsyT7k](https://www.youtube.com/watch?v=-acpEOsyT7k) and [5zW1ag4_d_o](https://www.youtube.com/watch?v=5zW1ag4_d_o) are broken down to the second in section 3

### Inferences
- The main-channel teaser has a fixed shape: **15 to 25 s of fight clips taken from later in the same video** (usually the final fight), labelled "in this video -" or "COMING SOON", then a 3 to 5 s black or logo beat. That beat lets viewers who came for the payoff know it is coming, which fits the end-of-video heatmap peaks.
- The amount of graphics is low and fixed: one teaser label, an optional branded frame, an optional logo card, an occasional face-sticker subtitle on a funny line, an optional zoom on the WWCD banner. No kill counters and no chapters. Kaatclip can produce all of this from templates.
- Main-channel highlights keep some "boring" POV time (drives with comms, scoping, holding). The cut is by **fight cluster plus the bridges around it**, not kills only. That matches the flat heatmap stretches noted in the earlier study.

### Gaps
- Storyboards are about 5 s apart (2 s for short videos), so transitions under 2 s (whooshes, flashes) and exact text timing could not be seen. Music can only be inferred from caption gaps; it was not heard.
- The banter pop-ups were seen in one main-channel video (-vFxWHPrv2s). How common they are is not measured.

## 3. Source mapping: highlight to stream, cut by cut

### Takeaway
Three esports-type stream cuts of a single match (wDgeZBn80VM, -acpEOsyT7k, 5zW1ag4_d_o) keep **23 to 31% of the match**, measured from the plane to the result screen, and 1.4 to 2.8% of the stream. They keep it as **4 to 11 stretches, nearly all in time order**, each 25 to 162 s long, and the final fight is always kept whole (142 to 162 s). Removed: the lobby, inventory and between-match chat (10 to 21 min before each match), the plane, landing and first looting (2 to 6 min), and mid-match looting, driving and long scope sessions (gaps of 19 s to 11 min). Stretches start at the enemy call or on the shots (0 to 16 s before contact) and the video ends 15 to 30 s after the result. One video in four (5zW1ag4_d_o) adds a cold open taken from a fight that was cut from the body. Custom-room (4v4 WOW) and Ultimate Royale cuts keep more: 43 to 48% of the span.

### Cited Findings

**Map 1. "PMGC Grind with Old Teammates 👺🚀"** ([wDgeZBn80VM](https://www.youtube.com/watch?v=wDgeZBn80VM)): 362 s, 188,355 views, uploaded 11 Nov 2026 12:18. Source: stream "60000 Uc Crate opening | PMGC Grind" ([GVKHZ9-erB8](https://www.youtube.com/watch?v=GVKHZ9-erB8)), 7:07:42, started 10 Nov 19:33. The upload came **9.6 h after the stream ended**.

The stream's match timeline (storyboard): previous match result "#4" at 2:22:53; scoreboard, inventory and lobby from 2:23 to 2:32:53; plane at 2:33:13; landing at about 2:34:40; looting from 2:34:53 to 2:40:27; result "#2" at 2:56:12; stats screen at 2:56:32.

| # | Highlight | Stream | Kept | What it is | Cut before it |
|---|---|---|---|---|---|
| 1 | 0:00–1:27 | 2:40:27–2:41:54 | 87 s | Starts on the call "इधर से गाड़ी आ रहा है" (a car is coming); "फाइट ले लो" at 2:40:37; smokes, knocks, loot crate | 5:47 of landing and loot (plus 17:34 of lobby, inventory and plane since the last result) |
| 2 | 1:33–1:59 | 2:45:38–2:46:04 | 26 s (+6 s silent tail) | Drive, sniper shot | 3:44: looting houses, drive |
| 3 | 2:00–3:11 | 2:52:18–2:53:29 | 71 s | Drive into a fight at the rocks | 6:14: a 2-minute scope session (2:48–2:50), map checks, rotation |
| 4 | 3:17–6:02 | 2:53:48–2:56:30 | 162 s | Final circle behind a wrecked car, through the "#2" screen, plus 18 s of comms ("मेरा 200 पिंग चल रहा है… कोई नहीं गेम है भाई") | 0:19 |

Totals: about 352 s kept of a 1,397 s match (25%) and a 25,662 s stream (1.4%). Order: chronological. No cold open, no added graphics, the stream overlay (sponsor banner, facecam) kept. Alignment confidence is high (606 anchors).

**Map 2. "Goblin Solo 7 Finishes WWCD in Scrims 🚀💖"** ([-acpEOsyT7k](https://www.youtube.com/watch?v=-acpEOsyT7k)): 279 s, 25,162 views, uploaded 22 Feb 2026 12:34. Source: "80000 UC Wildsoul Warden Crate Opening | Scrims" ([yUuB2x9H0Qg](https://www.youtube.com/watch?v=yUuB2x9H0Qg)), 4:22:22, started 21 Feb 20:33. Upload 11.6 h after the stream ended.

The stream's match timeline: inventory at 30:17; lobby at 30:57; plane at 32:37; parachute at 33:17; landing at about 33:37; WWCD at 51:56; stats lobby at 52:16.

| # | Highlight | Stream | Kept | What it is | Cut before it |
|---|---|---|---|---|---|
| 1 | 0:00–0:26 | 35:53–36:18 | 25 s | First compound fight ("एक नीचे कर रहा हूं… एक और है") | 2:16 of looting after landing |
| 2 | 0:29–1:10 | 42:48–43:29 | 41 s | Enters mid-burst ("मारो मारो"), then the knock-to-finish and banter; the 12 s set-up call (42:36) was dropped | 6:30 of looting and rotation |
| 3 | 1:16–1:51 | 45:29–46:04 | 35 s | Zone call ("पूरा जोन… ब्लू साइड"), drive, map | 2:00 |
| 4 | 2:00–2:53 | 48:01–48:54 | 53 s | Fight at the triangle rocks | 1:57 |
| 5 | 2:57–3:48 | 49:51–50:42 | 51 s | Fight from the buggy | 0:57 |
| 6 | 3:55–4:39 | 51:25–about 52:12 | 27 s aligned + about 17 s | "लास्ट है", "1 HP… मर गया जोन से… बढ़िया नाइस", WWCD, MVP | 0:43 |

Totals: about 265 s of a 1,159 s match (23%) and 1.8% of the stream. Chronological, no cold open, starts on the first fight rather than the landing.

**Map 3. "Goblin in GodLiN mode Willy and teammates Shocked 💀💀🚀"** ([5zW1ag4_d_o](https://www.youtube.com/watch?v=5zW1ag4_d_o)): 448 s, 112,159 views, uploaded 22 Feb 2026 19:46, the same stream (18.8 h after it ended).

The stream's match timeline: previous result at 3:45:04; lobby at 3:45:24; full-screen facecam chat from 3:46:24 to 3:49:24; plane at 3:49:44; landing at about 3:50:24; "#2" result at 4:13:42; facecam reaction from 4:14:42.

| # | Highlight | Stream | Kept | What it is | Cut before it |
|---|---|---|---|---|---|
| CO | 0:00–0:26 | 4:02:27–4:02:54 | 27 s | **Cold open**: a mid-match fight that is not shown again (it lies inside the 11-minute gap below) | — |
| 1 | 0:41–1:40 | 3:51:26–3:52:25 | 59 s | Hot-drop fight about 60 s after landing (0:26–0:41 unaligned, likely the transition or plane) | 5:42 since the previous result |
| 2 | 1:47–2:12 | 3:52:56–3:54:24 | 5 s + 16 s | Follow-up fights | 0:31 and 1:06 |
| 3 | 2:33–3:35 | 3:57:51–3:59:20 | 24 s + 36 s | Compound fights | 3:27 |
| 4 | 4:15–4:25 | 4:00:00–4:00:15 | about 15 s | Short bits | 0:40 |
| 5 | 4:27–6:50 | 4:11:21–4:13:43 | 142 s | Final fight to the "#2" screen | 11:06 of rotation, drives and the cold-open fight |
| 6 | 7:05–7:25 | 4:14:14–4:15:38 | 6 s + 10 s | Facecam reaction after the match, which gives the title ("teammates shocked") | 0:31 |

Totals: about 448 s of a 1,438 s match (31%) and 2.8% of the stream. The body is chronological; the cold open is out of order. The 3:36–4:11 highlight stretch has no speech, so it is unaligned (possibly music or quiet play), which makes that row uncertain.

**Map 4. "iQOOSouL x iQOO8bit 4V4 WOW MODE 🚀"** ([QF7VlJj-QZs](https://www.youtube.com/watch?v=QF7VlJj-QZs)): 530 s, 128,105 views. Source: stream [7dUemvoJ1c0](https://www.youtube.com/watch?v=7dUemvoJ1c0) (9:45:15, started 2 Jun 2026); uploaded **10 days later** (13 Jun).
- Cold open at 0:19–0:25, from stream 2:04:51; the same moment returns in place at 4:11–4:34 (2:04:45–2:05:08).
- The body is 22 aligned stretches running in order from 1:55:13 to 2:15:59. Stretches last 2 to 44 s (median about 12 s), with gaps of 0 to 163 s (mostly 8 to 60 s: respawn, waiting between rounds, regrouping).
- Kept: 530 s of a 1,246 s span (43%).

**Map 5. "Goblin insane Clutches in Ultimate Royle | Teammates Shocked"** ([4cC844SCxUk](https://www.youtube.com/watch?v=4cC844SCxUk)): 512 s. Source: [AF_iszEug90](https://www.youtube.com/watch?v=AF_iszEug90) ("Down, Not out", 4:43:20, 23 Jun 2026); uploaded 34.8 h after the stream ended.
- 8 anchor stretches in order from 2:21:29 to 2:39:23; the storyboard shows the map and plane at 0:00, the parachute at 0:04 and a facecam-zoom ending at 8:17–8:27.
- Kept: 512 s of a 1,074 s span (48%).
- **Uncertain in detail**: the highlight has 20 speech-free stretches of 6 s or more (possibly music), so only about 200 s are anchored.

**Funny cuts, for contrast:**
- "goblin.exe" ([UbdXp3UzFAA](https://www.youtube.com/watch?v=UbdXp3UzFAA), 112 s): 9 snippets of 1 to 16 s from four places in [8gvGjQFygOM](https://www.youtube.com/watch?v=8gvGjQFygOM) (48:35–49:57, 2:54–3:11, 9:13–9:46, 14:42–14:52). **Not chronological**: it opens with the 48:35 bit, then jumps back. Uploaded 8.5 days after the stream.
- "goblin.exe ft. Joker" ([Q_5n1fA6MO8](https://www.youtube.com/watch?v=Q_5n1fA6MO8), 148 s): teaser bits from 15:38 and 22:54, then 17:13 to 19:35 in order, then a 22:03 ending. Source [xz-_mzU_UPE](https://www.youtube.com/watch?v=xz-_mzU_UPE).
- "Ragebaiting Joker" ([j6kf-4MXXDc](https://www.youtube.com/watch?v=j6kf-4MXXDc), 261 s): cold open 0:00–0:05 = 4:18:24 (repeated at 2:22), body 3:49:00 to 4:20:45 mostly in order, snippets of 1 to 48 s. Same source stream.

Upload lag after the stream ended, for the 15 matched pairs:
- 9.6 to 19.9 h for 7 of them: [wDgeZBn80VM](https://www.youtube.com/watch?v=wDgeZBn80VM), [-acpEOsyT7k](https://www.youtube.com/watch?v=-acpEOsyT7k), [5zW1ag4_d_o](https://www.youtube.com/watch?v=5zW1ag4_d_o), [JXSFHpiHkS0](https://www.youtube.com/watch?v=JXSFHpiHkS0), [nE67VClXWkM](https://www.youtube.com/watch?v=nE67VClXWkM), [aRwYyMCIUCI](https://www.youtube.com/watch?v=aRwYyMCIUCI), [sycnSTtAOKA](https://www.youtube.com/watch?v=sycnSTtAOKA)
- 1.5 to 3 days for 5: [yucF5hCgl8o](https://www.youtube.com/watch?v=yucF5hCgl8o), [pdG-_XDypV4](https://www.youtube.com/watch?v=pdG-_XDypV4), [4cC844SCxUk](https://www.youtube.com/watch?v=4cC844SCxUk), [Q_5n1fA6MO8](https://www.youtube.com/watch?v=Q_5n1fA6MO8), [d-6B6fjDZSE](https://www.youtube.com/watch?v=d-6B6fjDZSE)
- 7 to 10 days for 3: [j6kf-4MXXDc](https://www.youtube.com/watch?v=j6kf-4MXXDc), [UbdXp3UzFAA](https://www.youtube.com/watch?v=UbdXp3UzFAA), [QF7VlJj-QZs](https://www.youtube.com/watch?v=QF7VlJj-QZs)
- The first cut of a stream usually goes up the next day at 11:00 to 13:00 or 19:00 to 22:00 IST

Stream "most replayed" check: the chosen sections sit only moderately above the stream median. The best bin inside the used section ranked 13th to 21st of 100 (AF_iszEug90 0.53 against a median of 0.37; 7dUemvoJ1c0 0.42 against 0.24; xz-_mzU_UPE 0.59 against 0.24) — yt-dlp heatmaps of those streams

### Inferences
- The choice is **"the match worth telling"** (a WWCD, a near-win #2, or one with a named teammate or a crowd moment), not the stream's highest-energy minutes. Inside the match, the rule is "every fight with kills or knocks, plus the final fight uncut".
- Lead-in is short. Two of the stretch starts hit the call (about 10 to 16 s before shots, wDgeZBn80VM #1 and #3); one starts mid-burst (-acpEOsyT7k #2). A safe automatic default is 8 to 15 s before the first shot, or snapping back to the start of the nearest comms phrase.
- Lead-out: each fight stretch runs 5 to 20 s past its last kill (finish confirmations, banter); the match ends 15 to 30 s after the result screen or on a facecam reaction.
- The 1.4 to 2.8% stream-to-highlight ratio shows the second channel is not compressing whole streams. It is picking one match per video.

### Gaps
- The main channel's own source recordings are not public, so its cut ratio cannot be measured. Its highlights are 4 to 11 min per match or day.
- Stretches with no speech (music, quiet play) cannot be aligned by captions. Rows 3:36–4:11 of Map 3 and most of Map 5 are uncertain.
- Stream storyboards are 10 s apart, so cut points are known to ±2 s from captions but only ±10 s visually.

## 4. Shorts on both channels

### Takeaway
Shorts are 16 to 57 s vertical clips of **one clutch (1v3, 1v4) or one banter moment**. They use a stacked layout (cropped gameplay on top, facecam or LAN player-cam below) and a meme payoff at the end: a skull or crown sticker, a black-and-white flash, a phonk-style ending. Titles are one hook phrase plus emojis. Recent ones are often made by outside fan editors. The main channel effectively does not post Shorts.

### Cited Findings
- 20 recent second-channel Shorts (25 Jun to 29 Oct 2026): 16 to 57 s long, median 32.5 s; 1440x2560 or 1080x1920. Titles: "Goblin quick 1v3 TAG 🚀💀" (22 s, 582,761 views, [TVZ2RLVXD7E](https://www.youtube.com/shorts/TVZ2RLVXD7E)); "Denies bounty like a boss 😭😂" (31 s, 793,575, [CdkN90FTUl8](https://www.youtube.com/shorts/CdkN90FTUl8)); "Goblin 1v3 with MG3 in Scrims 💀" (26 s, 191,882, [4FAhf4pPnQ0](https://www.youtube.com/shorts/4FAhf4pPnQ0)); "Goblin quick 1v3 in Ultimate Royale 💀" (39 s, 177,722, [OKcO5mHf4rI](https://www.youtube.com/shorts/OKcO5mHf4rI)); "IGL ki call kon sunta hai 😏" (26 s, 200,958, [eTf7izIhEiA](https://www.youtube.com/shorts/eTf7izIhEiA)) — yt-dlp metadata
- Storyboards, 1 frame a second:
  - [OKcO5mHf4rI](https://www.youtube.com/shorts/OKcO5mHf4rI): gameplay crop on top (about 60%), the stream facecam on the bottom (about 40%); a skull-and-crown overlay at 0:32 to 0:35, then the facecam alone at the end
  - [CdkN90FTUl8](https://www.youtube.com/shorts/CdkN90FTUl8) and [TVZ2RLVXD7E](https://www.youtube.com/shorts/TVZ2RLVXD7E) (BGMS LAN): broadcast gameplay on top, the player cam on the bottom; skull or crown stickers and a black-and-white freeze at the payoff
  - [3gtSMtb1osg](https://www.youtube.com/shorts/3gtSMtb1osg): a fan-edited mix of off-game LAN photos and video (57 s)
- Fan editors are credited: "Edit by - https://www.instagram.com/p/…" on [3gtSMtb1osg](https://www.youtube.com/shorts/3gtSMtb1osg), [fmQWDd6rRNA](https://www.youtube.com/shorts/fmQWDd6rRNA) and [K0VxL67fBQ8](https://www.youtube.com/shorts/K0VxL67fBQ8); "Edit by: https://www.instagram.com/iqoosoul_updates/" on [in_PAsoNxME](https://www.youtube.com/shorts/in_PAsoNxME)
- Shorts captions are thin (8 to 71 caption words per Short), so music or effects dominate, and none could be caption-aligned to a stream — this study
- The top all-time Shorts are banter and nostalgia, not only clutches: "Revenge 💯🚀" 4.5M, "Goblin vs Neyo 1v1 with DBS 😂" 3.4M, "Form is Temporary but Class is Permanent" 2.7M, "Team SouL when camera Notices them 🤣" 1.7M — [@goblinsh0rts/shorts](https://www.youtube.com/@goblinsh0rts/shorts)
- The main channel has 4 Shorts in total; the top one is "1v3 SouL again Quick", 15 s, 1.05M ([iF7cZNBIGKc](https://www.youtube.com/shorts/iF7cZNBIGKc))

### Inferences
- For Kaatclip, a Goblin-style Short is the single best clutch or banter beat cut out of the same match map. It runs 20 to 40 s with no lead-in beyond about 3 to 5 s, uses a stacked game-over-facecam layout, and ends on a meme sting.

### Gaps
- Upload dates and durations are known only for the 20 most recent Shorts. The flat list of 438 has no dates.
- Exact text overlays inside the Shorts are not legible at storyboard resolution (101x180).

## 5. Upload practice: titles, thumbnails, descriptions, timing, what gets views

### Takeaway
The packaging is minimal. Descriptions are empty or hashtag-only, there are no chapters, and the formula titles name the number, the result and the event. Timing is "the next day" for stream cuts and "within a day of the match day" for LAN broadcast cuts. Views follow **people and story in the title** more than the kill number. Three videos cut from the same stream on the same weekend got 112K ("Goblin in GodLiN mode Willy and teammates Shocked") against 25K ("Goblin Solo 7 Finishes WWCD in Scrims") and 44K ("When a T1 Player Dominates in Ultimate Royale").

### Cited Findings
- Descriptions: 42 of 79 main-channel videos use one of a few fixed hashtag strings ("#goblin #goblinislive #soulgoblin" on 21; "#goblin #goblinbgmi #bgmi #iqoosoul #iqoosoulgoblin" on 11), 6 are empty, and 3 carry social links. 60 of 79 carry 22 tags and 19 carry none — [@goblinbgmi](https://www.youtube.com/@goblinbgmi/videos) metadata. Of the 40 most recent second-channel videos, 39 have empty descriptions — [@goblinsh0rts](https://www.youtube.com/@goblinsh0rts/videos)
- Upload hours (IST): main-channel videos peak at 11:00 to 14:00 (36 of 79) and 19:00 to 20:59 (19 of 79). Second-channel videos at 11:00 (6 of 40) and 21:00 to 22:59 (14 of 40). Streams start at 19:00 to 20:59 (20 of 30) — yt-dlp timestamps
- LAN broadcast cuts go up during the event: on 17 and 18 Oct 2026 (BMSD) the second channel posted [7uZM0hKn5Yc](https://www.youtube.com/watch?v=7uZM0hKn5Yc), [xtE3WWqt1_E](https://www.youtube.com/watch?v=xtE3WWqt1_E), [SMkb493VutI](https://www.youtube.com/watch?v=SMkb493VutI) (interview), [mjUFpXmaQH4](https://www.youtube.com/watch?v=mjUFpXmaQH4) and [PlgCUW6JbCw](https://www.youtube.com/watch?v=PlgCUW6JbCw) — 5 videos in 2 days
- The same stream, three cuts: [5zW1ag4_d_o](https://www.youtube.com/watch?v=5zW1ag4_d_o) 112,159 views (people plus reaction in the title, cold open, facecam ending) against [-acpEOsyT7k](https://www.youtube.com/watch?v=-acpEOsyT7k) 25,162 (stats title, a WWCD, no cold open) and [yucF5hCgl8o](https://www.youtube.com/watch?v=yucF5hCgl8o) 44,145
- Second-channel winners: LAN broadcast "iQOOSouL 42 Points in One Game | Total Destruction in BGMS" (615 s, 264,834, [nkvIKh72uH8](https://www.youtube.com/watch?v=nkvIKh72uH8)); custom rooms "S8uL 2v2 Wow Mode | Goblin + Krutika vs Regaltos + Joker" (905 s, 271,921, [7TkLt-j3u4A](https://www.youtube.com/watch?v=7TkLt-j3u4A)) and "IQOOSOUL VS JP 4V4 WOW MODE" (509 s, 269,668, [xiqm0RdJR3o](https://www.youtube.com/watch?v=xiqm0RdJR3o)); vlog "1 GOAL 🏆| THE BMSD JOURNEY BEGINS" (789 s, 205,547, [ah3rZZk3g44](https://www.youtube.com/watch?v=ah3rZZk3g44)); stream cut "PMGC Grind with Old Teammates" (188,355 within 1 day, [wDgeZBn80VM](https://www.youtube.com/watch?v=wDgeZBn80VM))
- Main-channel title style is unchanged from the earlier study ("Solo {k} Finishes WWCD | {team} Finishes | {event}"). Second-channel stream cuts use "Goblin + {teammate} …", "{team} {N} Kills Chicken Dinner in Practice Scrims | Solo {k} Kills", or a story phrase ("Patience is the key to success...", "This is how Goblin qualified for PMGC 2026 😭") — [@goblinsh0rts](https://www.youtube.com/@goblinsh0rts/videos)

### Inferences
- Titles that name teammates, an opponent or a reaction outperform plain stat titles on the second channel. Kaatclip's title maker should offer a "people + moment" template next to the number template.
- Posting the first cut the next day at about noon or 21:00 IST is the observed rhythm. A Kaatclip suggestion of "post tomorrow 12:00 or 21:00" fits it.

### Gaps
- Thumbnails of the second channel were not inspected in this pass. The earlier study covers 5 main-channel thumbnails.
- Views are a snapshot; views per day since upload were not normalised.

## 6. Rules an automatic editor can follow to reproduce Goblin-style esports match highlights

### Takeaway
Build the edit from the match map: pick one match (or one custom-room session), keep every fight stretch in order with a short lead-in and lead-out, keep the final fight whole, cut everything else, and end on the result plus a reaction. Optionally add a recycled 15 to 25 s teaser and minimal branding (the "hero" variant). The measured numbers below come from the maps and storyboards above. Thresholds marked (inferred) are design choices consistent with the data, not direct measurements.

### Cited Findings (the measurements each rule rests on)
- Ratio: 23 to 31% of a classic match and 1.4 to 2.8% of a stream ([wDgeZBn80VM](https://www.youtube.com/watch?v=wDgeZBn80VM), [-acpEOsyT7k](https://www.youtube.com/watch?v=-acpEOsyT7k), [5zW1ag4_d_o](https://www.youtube.com/watch?v=5zW1ag4_d_o)); 43 to 48% for custom-room or Ultimate Royale spans ([QF7VlJj-QZs](https://www.youtube.com/watch?v=QF7VlJj-QZs), [4cC844SCxUk](https://www.youtube.com/watch?v=4cC844SCxUk))
- Stretch lengths: 25 to 87 s for mid-match fights; 142 to 162 s for the final fight; 2 to 44 s in custom rooms (section 3 tables)
- Order: chronological in every classic-match map. The only out-of-order piece is a cold open (5zW1ag4_d_o, QF7VlJj-QZs, j6kf-4MXXDc)
- Teaser: 15 to 25 s, recycled from later fights, labelled, followed by a 3 to 5 s black or logo beat, on 6 of 9 main-channel videos ([-vFxWHPrv2s](https://www.youtube.com/watch?v=-vFxWHPrv2s), [deJt870ksiE](https://www.youtube.com/watch?v=deJt870ksiE), [lBswYFSS_rQ](https://www.youtube.com/watch?v=lBswYFSS_rQ), [KmjTasCQZ5U](https://www.youtube.com/watch?v=KmjTasCQZ5U), [MQ8SC-_e8ZQ](https://www.youtube.com/watch?v=MQ8SC-_e8ZQ), [OOnDKF-Wprs](https://www.youtube.com/watch?v=OOnDKF-Wprs))
- Ending: WWCD banner, then MVP, then lobby, 15 to 25 s after the last kill (main channel); or the result screen plus 15 to 30 s of comms or facecam (second channel)

### Inferences (the rule set)
1. **Unit and selection.** Split the stream into matches (lobby, then plane, then result screen). Score each match: WWCD, then #2 or #3 with a long final fight; total kills; a 1vN clutch; a named teammate or opponent; comms intensity in the last circle. Make **one video per qualifying match**; a strong stream yields 2 or 3 (as on 21 Feb 2026). For TDM/WOW custom rooms, treat the whole room session (15 to 25 min) as the unit.
2. **Always cut:** the lobby, inventory and loadout screens, waiting and full-screen facecam chat between matches; the plane (keep at most 3 to 5 s of parachute as the "match start" shot in the hero variant); looting after landing until the first contact; looting, driving or scoping with no knock or kill within 20 s; spectating after death (Goblin's cuts never show it); and the stats or results tables beyond 5 s.
3. **Fight stretches.** Group knocks and kills from the kill feed into fights with a gap of 25 to 45 s or more (inferred; the shortest real gaps between kept stretches were 19 to 57 s). Start each stretch **8 to 15 s before the first shot or knock**, snapped back to the start of the nearest comms phrase (the observed starts hit the enemy call, e.g. "इधर से गाड़ी आ रहा है"). End it **5 to 20 s after the last finish**, snapped to the end of the confirmation or banter phrase. Merge stretches less than about 20 s apart (wDgeZBn80VM rows 3 and 4 were 19 s apart).
4. **Final fight.** From the final-circle start (about 16 or fewer players left, or the last zone) through the result screen, keep it whole even if it runs 2.5 to 3 min. Then keep 15 to 30 s: the WWCD banner, the MVP animation and the post-match comms or facecam reaction. Optionally zoom in on the WWCD banner for 2 to 4 s (6jIQaYvIOGc).
5. **Bridges.** Keep at most one 10 to 30 s bridge (a drive with comms, a zone call, a map check) where the rotation changes the story, e.g. "पूरा जोन… ब्लू साइड" in -acpEOsyT7k. Drop the rest.
6. **Length targets.** A classic match gives 4.5 to 8 min (279 to 448 s observed). The hero variant with a teaser lands at 8 to 9.5 min (486 to 553 s on the main channel). Custom-room sessions run 8 to 15 min (445 to 905 s). Do not pad: if the match is short, publish a 4 to 6 min cut (the 188K-view PMGC video is 6:02).
7. **Cold open (hero variant, and optional in quick cuts).** Take 15 to 25 s from the top-scored fight. Prefer a fight cut from the body (as 5zW1ag4_d_o does) or the final fight (as -vFxWHPrv2s does). Put a short label on it ("in this video -" or the creator's own word), then a 3 to 5 s black or logo card, then the first stretch or the parachute shot.
8. **Graphics budget.** No running kill counter and no chapters. Optional: a branded frame or side panel when the source is narrower than 16:9 (the phone ratio of about 2.1:1 fills it); a face-sticker plus subtitle on at most 1 or 2 funny lines per video; a match or map card only for multi-match days ("MATCH 2", map name).
9. **Audio.** Comms at full level throughout. Music only under no-speech bridges, the teaser and frag montages (the frag reels run 40 to 50% speech, the match cuts 61 to 85%).
10. **Frame.** Quick-cut variant: keep the stream layout as is (Goblin keeps the sponsor banner and facecam). Hero variant: the clean game feed, no facecam.
11. **Titles and timing.** Offer "{who} + {moment}" ("Goblin + Nakul Domination", "teammates Shocked") alongside "Solo {k} Finishes WWCD | {team_k} Finishes | {event}". Suggest posting the next day at 12:00 or 21:00 IST.
12. **Shorts from the same map.** For each 1vN clutch or best banter beat: 20 to 40 s, starting 3 to 5 s before the first knock, stacked gameplay over facecam, ending on a meme sting.

### Gaps
- The fight-grouping gap and lead-in or lead-out numbers come from 3 fully mapped classic matches plus 2 partly mapped sessions. They should be tuned on Kaatclip's own test streams.
- How Goblin's editors pick which mid-match fights to drop, beyond "no kill or knock", cannot be seen from outside. Two mid-match sections with fights (Map 3: 4:00:15 to 4:11:21, which includes the 4:02 cold-open fight) were cut, probably for length.
