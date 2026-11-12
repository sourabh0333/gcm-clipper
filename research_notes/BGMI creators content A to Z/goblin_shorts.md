# GoBLiN shorts (@goblinsh0rts), A to Z: what the channel posts, what each type is based on, how it is made and uploaded

Method (12 Nov 2026). This study uses public YouTube data only. It was read with yt-dlp `--skip-download`, and no video or audio was downloaded. It builds on `research_notes/BGMI highlight channels deep study/goblin_deep.md` and does not repeat that study's five second-by-second stream-cut maps; those are referenced where needed.

What was collected:
- **Inventory.** Full metadata for **all 526 long videos and all 438 Shorts** on the channel: exact upload time, length, views, likes, description, resolution and storyboard links. The channel has no Playlists tab.
- **Main channel streams.** The full Streams tab of @goblinbgmi (100 entries), plus metadata for 18 older streams.
- **Captions.** Hindi auto-captions for 26 older streams (Jul 2024 to Nov 2025), 91 more second-channel long videos and 26 Shorts. These were added to the 21 stream captions and 61 video captions from the earlier study.
- **Layout census.** A storyboard frame strip (8 to 12 frames per item) for **every one of the 526 videos and 438 Shorts**, each item labelled by eye for layout and source.
- **Detailed reads.** Full storyboards for 12 items, read minute by minute.
- **Thumbnails.** 48 thumbnails were inspected.

Source proof relies on matching captions. Every 3-word sequence of a video's captions is looked up in each stream's captions. A stretch of the video counts as cut from the stream only when 3 or more sequences agree on the same time offset (±1.5 s). Real pairs score 140 to 1,109 agreeing anchors; unrelated pairs score 0 to 63.

Views are as of 12 Nov 2026 and all times are IST. Type labels for long videos come from title rules plus a manual source label (stream layout / clean phone POV / official broadcast / camera) on all 526 storyboard strips. Types for Shorts come from title rules plus a manual layout label on all 438. Raw data, scripts and contact sheets are in `C:\Users\soura\AppData\Local\Temp\claude\21027423ba80eb72\c7886632-c6c6-4a95-81c6-c6cbac2a769e\scratchpad\a2z\goblin_shorts\` (`rows_final.json`, `final_out.txt`, `visual_notes.md`, `maps\`, `census\`).

Layout codes used below:
- Long videos: **STR**, the stream layout (game plus Goblin's facecam plus the stream overlay or sponsor banner); **POV**, a clean phone-screen recording (no facecam, no overlay); **BC**, the official tournament broadcast (observer camera, team sidebar, casters); **CAM**, camera or vlog footage.
- Shorts: **SS**, stacked stream (game on top, facecam below); **VG**, a vertical crop of the game only; **LB**, a 16:9 frame letterboxed inside 9:16 with black bars; **SL**, stacked LAN (broadcast on top, player-cam below); **FC**, facecam only; **IRL**, phone or camera life footage; **ED**, edits (photos, film clips, text cards).

## 1. Full inventory: every upload, classified, with counts, lengths, views, cadence and how the mix changed

### Takeaway
GoBLiN shorts started on 9 Aug 2022 as the "Official Shorts Channel of Soul Goblin". It has posted **526 long videos (24.6M views) and 438 Shorts (83.1M views)**. Shorts bring **77% of the channel's views** with fewer uploads (median 84K views a Short against 30K a video). The mix moved through four eras:
- **2022 to 2023:** 30 to 120 s horizontal clips cut from Loco streams.
- **2024 (Carnival Gaming era):** short frag reels and clutch clips, plus clean POV recordings and LAN broadcast cuts.
- **2025:** fewer, longer videos (median 8 min): TDM/WOW custom rooms, classic solo-vs-squad, crate openings and LAN broadcast matches. Shorts carried the channel through the gaps.
- **2026:** volume back up. Single-match stream cuts, funny edits, talk clips, reactions and 18 vlogs, which are now the main LAN-week format.

### Cited Findings
- The channel has 131K subscribers, 526 videos, 438 Shorts and no Playlists tab — [@goblinsh0rts/videos](https://www.youtube.com/@goblinsh0rts/videos), [@goblinsh0rts/shorts](https://www.youtube.com/@goblinsh0rts/shorts) (yt-dlp tab listings; the playlists tab returns "This channel does not have a playlists tab")
- The first upload is "SoulGoblin Caught Red Handed Doing This" (9 Aug 2022, 66 s, 89K). Its description reads "Official Shorts Channel of Soul Goblin" — [mbHmgDE3oww](https://www.youtube.com/watch?v=mbHmgDE3oww). The first item on the Shorts tab is dated 4 Mar 2023: "The Campers Ft. SoulGoblin", 49 s, 397K — [LiD28WOHF_s](https://www.youtube.com/shorts/LiD28WOHF_s)
- Long videos per year: 2022: 32; 2023: 192; 2024: 130; 2025: 60; 2026 (to 11 Nov): 112. Median length per year: 58 s, 72 s, 118 s, **485 s**, 281 s. Median views per year: 38K, 37K, **15K**, 40K, 39K. Videos of 60 s or less: 19, 76, 15, 0, 3. Videos of 8 min or more: 0, 1, 1, **34**, 30 — channel metadata, this study
- Shorts per year: 2023: 40 (median 161K views); 2024: **165** (32K); 2025: 147 (110K); 2026: 86 (115K). Median Short length rose from 30 s (2024) to 39 s (2025) and 44 s (2026). 24 Shorts run 61 to 123 s (all from Sep 2025 onward, e.g. [cNKjdu5TbHI](https://www.youtube.com/shorts/cNKjdu5TbHI), 123 s) — [@goblinsh0rts/shorts](https://www.youtube.com/@goblinsh0rts/shorts)
- Long videos per month:
  - 2023: 3 to 27 (peak May 2023: 27)
  - 2024: 4 to 19
  - Jan to Aug 2025: 2 to 8, with **none in June 2025**
  - 2026: 5, 6, 11, 2, 11, 17, **23 (Jul)**, 12, 14, 8, 3 so far in Nov
  
  Shorts per month: 1 to 9 in 2023; 13 to 25 from Jun 2024 to May 2025; 0 to 1 in Jun and Jul 2025; 8 to 18 from Aug 2025 to May 2026; then **2 to 7 a month from Jun to Oct 2026** — channel metadata
- **Long videos by content type** (526). Views are medians.

  | Type | n | Years (22/23/24/25/26) | Median length | Median views | Max views |
  |---|---|---|---|---|---|
  | Clutch clip (one 1vN or spray, under 100 s) | 110 | 13/69/27/0/1 | 56 s | 29K | 106K |
  | Match or scrims cut (one match or a short highlight) | 91 | 4/40/33/2/12 | 175 s | 34K | 468K |
  | LAN or tournament broadcast match | 73 | 0/14/17/25/17 | 239 s | 19K | 265K |
  | Funny or banter edit | 49 | 10/16/2/3/18 | 105 s | 49K | 226K |
  | Frag montage ("Frags", "Scrims highlights") | 43 | 0/10/29/0/4 | 107 s | 26K | 78K |
  | Talk or news clip from stream chat | 27 | 2/14/3/2/6 | 95 s | 36K | 194K |
  | Classic, Ultimate Royale or solo-vs-squad pub | 25 | 1/5/6/9/4 | 428 s | **58K** | 193K |
  | Vlog, IRL or celebration | 22 | 0/2/1/1/18 | 621 s | 54K | 206K |
  | TDM/WOW custom room (1v1, 1v2, 2v2, 4v4) | 22 | 1/3/0/9/9 | 442 s | **89K** | 272K |
  | Crate opening or spending | 17 | 0/3/3/6/5 | 360 s | 31K | 180K |
  | LAN broadcast clutch clip | 13 | 0/7/3/0/3 | 61 s | 15K | 42K |
  | Reaction | 11 | 1/3/0/1/6 | 198 s | 27K | 273K |
  | LAN interview | 10 | 0/0/3/0/7 | 192 s | 16K | 50K |
  | Teaser or announcement | 8 | 0/5/3/0/0 | 99 s | 20K | 82K |
  | Other game (Chained Together, Sons of the Forest, Pokémon cards) | 4 | 0/0/0/2/2 | 511 s | 13K | 44K |
  | Other | 1 | | | | |

  Source: channel metadata and the layout census
- **Long videos by visual source and year.**

  | Year | Stream layout | Clean POV | Broadcast | Camera |
  |---|---|---|---|---|
  | 2022 | 32 | 0 | 0 | 0 |
  | 2023 | 123 | 37 | 28 | 3 |
  | 2024 | 45 | 59 | 24 | 2 |
  | 2025 | 27 | 8 | 25 | 0 |
  | 2026 | 65 | 0 | 28 | 19 |

  Over the whole channel: stream layout 292 (median 35K views, 15.0M total), POV 104 (29K), broadcast 105 (18K), camera 24 (54K) — layout census on all 526 storyboard strips
- The best custom-room year: in 2025, 9 TDM/WOW videos had a median of **225K views** (590 s). In 2026, 9 had 81K (440 s). Examples:
  - "S8uL 2v2 Wow Mode | Goblin + Krutika vs Regaltos + Joker", 905 s, 272K — [7TkLt-j3u4A](https://www.youtube.com/watch?v=7TkLt-j3u4A)
  - "IQOOSOUL VS JP 4V4 WOW MODE", 270K — [xiqm0RdJR3o](https://www.youtube.com/watch?v=xiqm0RdJR3o)
  - "Goblin vs Rony 1v1 TDM", 224K — [Ev6oMQTJVJ8](https://www.youtube.com/watch?v=Ev6oMQTJVJ8)
- The 2026 mix by month:
  - Jan to Mar: mostly broadcast matches (BGIS: 2, 2 and 5)
  - May and Jun: custom rooms, crates and match cuts
  - Jul: 7 match cuts, 6 funny edits, 3 talk clips
  - Aug: 4 interviews and LAN clips (BGMS)
  - Sep: **7 vlogs**, 3 reactions, 3 funny edits
  - Oct: 3 vlogs and 3 broadcast matches (BMSD)
  - Nov: a vlog and a stream cut
  
  Source: channel metadata
- The all-time most viewed long video is a 2023 clean-POV match: "Welcome to Pecado", 462 s, 468K — [6f0CK3fBrig](https://www.youtube.com/watch?v=6f0CK3fBrig). The most viewed Short is "Revenge 💯🚀", 36 s, 4.52M, a stacked stream clip — [DfOcogRMngg](https://www.youtube.com/shorts/DfOcogRMngg)

### Inferences
- The long-video side changed from **volume of tiny clips** (2023: 131 of 192 videos were 2 minutes or less) to **fewer 5 to 15 minute "sessions"** (2025 to 2026). The likely reason is that clips of 60 s or less moved to the Shorts tab once Shorts existed: the channel's first Short came in Mar 2023, and from 2024 Shorts outnumber long videos. This is an inference from timing; the channel owner has not stated it.
- The ups and downs follow Goblin's career:
  - Team SouL with S8UL in 2022 to 2023 (#soulgoblin hashtags on 190 of 192 videos in 2023)
  - Carnival Gaming in 2024 (#cggoblin on 114 videos and 131 Shorts in 2024)
  - About three months at Likitha Esports in early 2025 ([Sportskeeda](https://www.sportskeeda.com/bgmi/news-bgmi-star-goblin-returns-team-soul-ahead-bmps-2025)) and a return to SouL on 1 May 2025 (same source)
  - #iqoosoul tags from 2025
  
  The near-empty June and July 2025 (2 videos, 1 Short) falls right after the return to SouL. The channel's content is driven by the player's calendar (LANs, team changes), not by a fixed schedule.

### Gaps
- Type labels from titles are approximate. About 10% of items are ambiguous: for example, "Goblin Savage Reply to @OMEGAAAA by Doing 2v4 Clutch" is both a clutch and a banter clip. Layout labels were made by eye on 8 to 12 frames per item, so a few mixed-layout videos may be mislabelled.
- Views are a single snapshot and not normalised by age.

## 2. What each content type is based on (where the footage comes from), with proof

### Takeaway
There are **five footage sources**:
1. **Goblin's own live streams**, cut with the stream overlay and facecam left in. These feed match cuts, custom rooms, crate openings, funny edits, talk clips, reactions and most Shorts. The streams were on Loco in 2022 and 2023, on YouTube from 2024, and partly on Kick in mid-2026.
2. **Clean phone-screen POV recordings** with no facecam and no overlay. These feed the 2023 to 2025 POV matches, frag reels and solo-vs-squad pub videos.
3. **The official LAN broadcast VOD** with Hindi casters. This feeds LAN matches, LAN clutches, interviews and the stacked LAN Shorts.
4. **Camera or phone footage of real life**: vlogs, celebrations and IRL Shorts.
5. **Edits built from photos, film clips and old footage**: hype and nostalgia Shorts, some made by fan editors.

Caption matching proves the stream source for 40 videos (25 in this study plus 15 in the earlier one) and 15 Shorts.

### Cited Findings
**Streams → long videos (caption-matched pairs, anchor score, then how long after the stream ended the upload came):**
- Crate openings:
  - "80K UC PAGANI CRATE OPENING" [-5i-6rSEtTg](https://www.youtube.com/watch?v=-5i-6rSEtTg) ← [gXjpOByZU8s](https://www.youtube.com/watch?v=gXjpOByZU8s) (258; 21.1 h)
  - 75K UC Lambo crate [CsYk1Mmd0Ow](https://www.youtube.com/watch?v=CsYk1Mmd0Ow) ← [6p6G3xz6pok](https://www.youtube.com/watch?v=6p6G3xz6pok) (154; 29.8 h)
  - [x612VqS5HZQ](https://www.youtube.com/watch?v=x612VqS5HZQ) ← [fie4MzEEcBw](https://www.youtube.com/watch?v=fie4MzEEcBw) (242; 238 h)
  - [qQqy1Pfjs0k](https://www.youtube.com/watch?v=qQqy1Pfjs0k) ← [SKJskHDhZmg](https://www.youtube.com/watch?v=SKJskHDhZmg) (521; 28.9 h)
  - [gLr68sUlnj0](https://www.youtube.com/watch?v=gLr68sUlnj0) ← [i8dWph1XuPc](https://www.youtube.com/watch?v=i8dWph1XuPc) (210; 72 h)
  - [qVDUITGVlBw](https://www.youtube.com/watch?v=qVDUITGVlBw) ← [YpzRzY5w0R0](https://www.youtube.com/watch?v=YpzRzY5w0R0) (359; 27 h)
  - [mRQIXdDEsH0](https://www.youtube.com/watch?v=mRQIXdDEsH0) and [_Mjn2Faf1VQ](https://www.youtube.com/watch?v=_Mjn2Faf1VQ) ← [L0RFKcKTFDI](https://www.youtube.com/watch?v=L0RFKcKTFDI) (727 and 731; 69 h and 114 h)
  - [x3FmFvUKtF4](https://www.youtube.com/watch?v=x3FmFvUKtF4) ← [o2Aq0cIMMnM](https://www.youtube.com/watch?v=o2Aq0cIMMnM) (540; 21.4 h)
  - [2GJtTk-s_94](https://www.youtube.com/watch?v=2GJtTk-s_94) ← [h4LBvmiT8yg](https://www.youtube.com/watch?v=h4LBvmiT8yg) (901; 18.4 h)
- Custom rooms:
  - [Ev6oMQTJVJ8](https://www.youtube.com/watch?v=Ev6oMQTJVJ8) ← [Sfw7kY-pFNA](https://www.youtube.com/watch?v=Sfw7kY-pFNA) (549; **2.8 h**)
  - [-5zjIhAhSCg](https://www.youtube.com/watch?v=-5zjIhAhSCg) ← [y11I1DOIuzQ](https://www.youtube.com/watch?v=y11I1DOIuzQ) (683; 119 h)
  - [bWaofDQ7Dzg](https://www.youtube.com/watch?v=bWaofDQ7Dzg) ← [rBazJ1l_tMw](https://www.youtube.com/watch?v=rBazJ1l_tMw) (345; 21.4 h)
  - [yincpYxqIrI](https://www.youtube.com/watch?v=yincpYxqIrI) ← "Weekend Battle - iQOO SOUL vs iQOO RNTX" [yyhk-jbsACw](https://www.youtube.com/watch?v=yyhk-jbsACw) (436; 46.6 h)
  - [4QjX1jHoIvA](https://www.youtube.com/watch?v=4QjX1jHoIvA), [VfbRkzjGKl0](https://www.youtube.com/watch?v=VfbRkzjGKl0) and [7TkLt-j3u4A](https://www.youtube.com/watch?v=7TkLt-j3u4A) ← [ds2q0wh-YE0](https://www.youtube.com/watch?v=ds2q0wh-YE0) (672, 211, 836; 19.9 h, 138 h, 285 h): **three videos from one stream over 11 days**
  - [gkdmHs83TR4](https://www.youtube.com/watch?v=gkdmHs83TR4) ← [7dUemvoJ1c0](https://www.youtube.com/watch?v=7dUemvoJ1c0) (390; 87 h)
  - [eZWtpeZVsRc](https://www.youtube.com/watch?v=eZWtpeZVsRc) ← [h4LBvmiT8yg](https://www.youtube.com/watch?v=h4LBvmiT8yg) (287; 43 h)
- Funny edits:
  - "Goblin 999 IQ End Zone Gameplay | Funny Highlight" [7L0UYZ-1iVk](https://www.youtube.com/watch?v=7L0UYZ-1iVk) ← [EaP6AV_c9ZI](https://www.youtube.com/watch?v=EaP6AV_c9ZI) (995; 21.5 h)
  - "TROLLING RANDOMS IN BGMI" [hvq_G53fQp4](https://www.youtube.com/watch?v=hvq_G53fQp4) ← [rgaUmCMgbeE](https://www.youtube.com/watch?v=rgaUmCMgbeE) (347; 17.6 h)
  - "10 Minutes of Trolling @AmyaBhagat ft. @PAYALGAMING" [VF0fmimwQKc](https://www.youtube.com/watch?v=VF0fmimwQKc) ← [7dUemvoJ1c0](https://www.youtube.com/watch?v=7dUemvoJ1c0) (447; 198 h)
  - "3 Minutes of Roasting Scout and Neyo" [iAS4xO7xJPw](https://www.youtube.com/watch?v=iAS4xO7xJPw) ← [8pxVrhNj99A](https://www.youtube.com/watch?v=8pxVrhNj99A) (160; 20.4 h)
- Other: "500K Celebration with S8UL" [1N27KdUAnkc](https://www.youtube.com/watch?v=1N27KdUAnkc) ← [a2v-VmoND6w](https://www.youtube.com/watch?v=a2v-VmoND6w) (1,109; 8.8 h); "Chained Together" parts [mYp1yGubF_I](https://www.youtube.com/watch?v=mYp1yGubF_I) ← [rBazJ1l_tMw](https://www.youtube.com/watch?v=rBazJ1l_tMw) and [BksSd2q1vXQ](https://www.youtube.com/watch?v=BksSd2q1vXQ) ← [D-QOVIljNsE](https://www.youtube.com/watch?v=D-QOVIljNsE) (410; 194 h)
- The earlier study's 15 pairs (single-match scrims cuts, Ultimate Royale, goblin.exe, 4v4 WOW and crates) stand as published. Example: "PMGC Grind with Old Teammates" [wDgeZBn80VM](https://www.youtube.com/watch?v=wDgeZBn80VM) ← [GVKHZ9-erB8](https://www.youtube.com/watch?v=GVKHZ9-erB8) (603) — `goblin_deep.md`

**Loco, then YouTube, then partly Kick:**
- In 2023 Goblin "regularly streams" on Loco, and his YouTube is described as the place for "tournament highlights and scrims" — [Sportskeeda profile](https://sportskeeda.com/bgmi/soul-goblin-bgmi-id-stats-f-d-ratio) (modified 7 Aug 2023). On the @goblinbgmi Streams tab, only 5 streams are listed as about 3 or more years old (approximate dates) — [@goblinbgmi/streams](https://www.youtube.com/@goblinbgmi/streams). Yet the second channel posted 123 stream-layout videos in 2023, all with a green "goblin" overlay bar and a small facecam (census strips, e.g. [tHA0be7H9iE](https://www.youtube.com/watch?v=tHA0be7H9iE), [RM-WYe2lzWg](https://www.youtube.com/watch?v=RM-WYe2lzWg)). **Inference:** the 2022 and 2023 stream cuts come from Loco streams, which are not on YouTube.
- 24 uploads from 3 Jun to 24 Jul 2026 (18 videos and 6 Shorts) carry the description "Kick - https://kick.com/soulgoblin". Kick end cards appear on the Short [YK7JXrVblYQ](https://www.youtube.com/shorts/YK7JXrVblYQ) ("Follow me on Kick for more content like this", 0:38 to 0:42) and on the talk clips [obSaezZ2oZw](https://www.youtube.com/watch?v=obSaezZ2oZw) and [_ubDb8198vk](https://www.youtube.com/watch?v=_ubDb8198vk). The Kick channel "SouLGoBLiN" exists with 20.6K followers — [kick.com/soulgoblin](https://kick.com/soulgoblin)
- Of 56 stream-layout videos from 2024 to 2026 with captions, 25 match a YouTube stream (score 140 or more) and 31 do not (score 0 to 63). The non-matches cluster from 28 Jun 2026 onward: talk clips such as [Qw5AGoqlUks](https://www.youtube.com/watch?v=Qw5AGoqlUks) and [aFBMJVBYxyc](https://www.youtube.com/watch?v=aFBMJVBYxyc), funny clips such as [gPh6qB8s6_8](https://www.youtube.com/watch?v=gPh6qB8s6_8) and [csGetSqdQFg](https://www.youtube.com/watch?v=csGetSqdQFg), and reactions such as [UwBLTW7zAzw](https://www.youtube.com/watch?v=UwBLTW7zAzw) and [Qfdg2IzOUus](https://www.youtube.com/watch?v=Qfdg2IzOUus). The main channel streamed only 1, 1, 0 and 2 times in Jul to Oct 2026, while the second channel posted 23, 12, 14 and 8 videos in those months — this study's alignment; [@goblinbgmi/streams](https://www.youtube.com/@goblinbgmi/streams). **Inference:** most mid-2026 stream cuts come from Kick streams. During BGMS Season 5 (10 Aug to 6 Sep 2026), Kick held "exclusive" streaming of the event — [indiantelevision](https://indiantelevision.com/iworld/kick-bags-exclusive-streaming-rights-for-bgms-season-5/)

**Clean phone POV:**
- 104 videos (37 in 2023, 59 in 2024, 8 in 2025) show only the phone game screen. There is no facecam or overlay, and frame sizes such as 1920x886 or 1920x888 are phone-screen shapes (32 videos). Examples:
  - "Welcome to Pecado" (468K) [6f0CK3fBrig](https://www.youtube.com/watch?v=6f0CK3fBrig)
  - "Solo 8 Finishes" (202K) [hrkkD9arjDw](https://www.youtube.com/watch?v=hrkkD9arjDw)
  - "47 SOLO KILLS IN BGMI NEW UPDATE" (189K) [i8q-fV0zbeE](https://www.youtube.com/watch?v=i8q-fV0zbeE)
  - 2024 "Frags" reels such as [p7AF2YRqyiI](https://www.youtube.com/watch?v=p7AF2YRqyiI) and [3nouz_DfyDY](https://www.youtube.com/watch?v=3nouz_DfyDY)
  
  Captions on 8 POV videos run at a median of **28 words a minute with 38% speech coverage**, so they are mostly music, not comms (stream-layout videos: 117 wpm, 84%). The two titles saying "(POV)" are "Offline Match POV | Frags" [arHxH8lslB4](https://www.youtube.com/watch?v=arHxH8lslB4) and "Tournament Frags (POV)" [DQl18cDBx30](https://www.youtube.com/watch?v=DQl18cDBx30) — census and caption density
- No second-channel POV video is a re-upload of a main-channel video: duration-and-title matching across the main channel's 79 videos found no pairs.

**LAN broadcast:**
- 105 videos and 23 Shorts use the official broadcast. Its signs are the observer camera, the team-standings sidebar, the player-cam inset, "WWCD" stage graphics, map cards, and caster speech at **213 words a minute with 100% speech coverage** (20 videos with captions, 183 to 230 wpm). For comparison, stream cuts run at 117 wpm and POV at 28. Examples: [nkvIKh72uH8](https://www.youtube.com/watch?v=nkvIKh72uH8) (its captions start "ड्रॉप क्लैश हाई कुसोल एक बार फिर से…", caster talk), [Ovo5XpsUrdk](https://www.youtube.com/watch?v=Ovo5XpsUrdk) and [xtE3WWqt1_E](https://www.youtube.com/watch?v=xtE3WWqt1_E)
- Broadcast branding by era:
  - 2023: Skyesports, Upthrust and Nodwin cards ([D2j2iZqCavY](https://www.youtube.com/watch?v=D2j2iZqCavY), [o0NOpMvPw5E](https://www.youtube.com/watch?v=o0NOpMvPw5E))
  - 2024: Carnival's green sidebar and a "CG" end card ([oCg0a5xalcY](https://www.youtube.com/watch?v=oCg0a5xalcY), [0btzvbpUjwo](https://www.youtube.com/watch?v=0btzvbpUjwo))
  - 2025 to 2026: purple BGMS/BGIS sidebars with an "India Series" logo card ([Gl8hYRWMP1o](https://www.youtube.com/shorts/Gl8hYRWMP1o) at 1:09)
- Interviews (10, from 2024) are cut from the broadcast's stage-interview segment, for example [SMkb493VutI](https://www.youtube.com/watch?v=SMkb493VutI), [M_2PDtnpN5U](https://www.youtube.com/watch?v=M_2PDtnpN5U) and [3cSRcYnjywA](https://www.youtube.com/watch?v=3cSRcYnjywA)

**Camera footage:** 24 videos. Examples: the 2026 LAN-week vlogs [ah3rZZk3g44](https://www.youtube.com/watch?v=ah3rZZk3g44), [yVRqvpZR5-o](https://www.youtube.com/watch?v=yVRqvpZR5-o) and [cWxjZSKKHuM](https://www.youtube.com/watch?v=cWxjZSKKHuM); "S8uL BGIS Celebration" [RwydokVEQMc](https://www.youtube.com/watch?v=RwydokVEQMc); the Pokémon card opening [grK0UfjKMe0](https://www.youtube.com/watch?v=grK0UfjKMe0). Two vlogs ([cWxjZSKKHuM](https://www.youtube.com/watch?v=cWxjZSKKHuM), [FaqrL6G_rkU](https://www.youtube.com/watch?v=FaqrL6G_rkU)) cut in short broadcast gameplay shots.

**Edits:** 54 Shorts (ED layout) are built from photos, film clips, old LAN footage and text cards ("Form is Temporary but Class is Permanent" 2.7M [8TqWhvIeqZg](https://www.youtube.com/shorts/8TqWhvIeqZg); "Good Old Days" 2.4M [5y2DH4EvN0k](https://www.youtube.com/shorts/5y2DH4EvN0k)). In Oct 2026, four Shorts credit outside editors: "Edit by - https://www.instagram.com/p/…" on [3gtSMtb1osg](https://www.youtube.com/shorts/3gtSMtb1osg) and [fmQWDd6rRNA](https://www.youtube.com/shorts/fmQWDd6rRNA); "Edit by: …iqoosoul_updates" on [in_PAsoNxME](https://www.youtube.com/shorts/in_PAsoNxME).

### Inferences
- **Source by type:**

  | Type | Source |
  |---|---|
  | Match cut | Stream (58) or POV (33) |
  | Clutch clip | Stream (82) or POV (28) |
  | Frag montage | POV (29) or stream (14) |
  | Custom room | Stream (22 of 22) |
  | Crate opening | Stream (17 of 17) |
  | Funny edit | Stream (43 of 49) |
  | Talk or news | Stream (23 of 27) |
  | Reaction | Stream (10 of 11) |
  | Classic or pub | Stream (14) or POV (11) |
  | LAN match, clutch, interview | Broadcast (96 of 96) |
  | Vlog | Camera (16 of 22) |

  Source: census
- POV recordings were the main gameplay source in 2024 (59 of 130 videos, mostly "Frags" and "Solo N Finishes"). They vanish after early 2025, when the channel switched to stream cuts again.

### Gaps
- The Loco origin of 2022 and 2023 clips is an inference (no Loco VODs could be checked). The Kick origin of mid-2026 non-matching cuts is also an inference; Kick VODs were not checked and the Kick channel shows no listed past broadcasts.
- POV videos with music could not be traced to any recording.

## 3. How each type is made: structure, editing devices, layout, length

### Takeaway
The editing is **light and formulaic**. Stream-derived types keep the stream frame untouched (game, facecam box, sponsor or name banner) and are cut in chronological stretches. The added devices are few:
- a 15 to 20 s cold-open teaser under an "IN THIS VIDEO -" label (2025 to 2026)
- full-screen punch-ins on the facecam
- 1 to 5 s meme inserts (film clips, a screaming cat, a politician's speech)
- SpongeBob-style time cards ("THE NEXT DAY", "A FEW MINUTES LATER")
- a black end card

LAN broadcast cuts add nothing; all graphics are the broadcaster's. Vlogs are handheld camera days. Length follows the unit: 1 match gives 3 to 8 min, 1 custom-room session 7 to 15 min, 1 crate session 5 to 9 min, a talk point 1 to 2.5 min, and a vlog day 10 to 17 min.

### Cited Findings
**Stream cuts: how much of the source is kept**
- Classic single matches keep 23 to 31% of the match ([wDgeZBn80VM](https://www.youtube.com/watch?v=wDgeZBn80VM), [-acpEOsyT7k](https://www.youtube.com/watch?v=-acpEOsyT7k), [5zW1ag4_d_o](https://www.youtube.com/watch?v=5zW1ag4_d_o)) — `goblin_deep.md`
- Custom rooms keep **26 to 65%** of the session span:
  - Ev6oMQTJVJ8 26% (2,280 s span)
  - -5zjIhAhSCg 26%
  - yincpYxqIrI 29%
  - eZWtpeZVsRc 29%
  - 7TkLt-j3u4A 40%
  - gkdmHs83TR4 45%
  - 4QjX1jHoIvA 65%
  - QF7VlJj-QZs 43% (earlier study)
  
  Each runs as 9 to 25 stretches of 2 to 135 s, with gaps of 7 to 100 s (respawns and waits between rounds) and 0 to 3 order breaks.
- Crate openings keep 3 to 43% of their span (2GJtTk-s_94: 25 stretches in order, 43%; x3FmFvUKtF4: 3% of a 3.8 h span; CsYk1Mmd0Ow: 12%).
- Funny edits keep 1 to 60% (7L0UYZ-1iVk: 60% of 18 min; hvq_G53fQp4: 9% of 64 min with 2 order breaks; iAS4xO7xJPw: 74 s anchored across an 8 h stream).

Source: `maps\*.txt`, this study's alignment.

**Minute by minute, 2v2 WOW** — [7TkLt-j3u4A](https://www.youtube.com/watch?v=7TkLt-j3u4A) (905 s, 272K; source [ds2q0wh-YE0](https://www.youtube.com/watch?v=ds2q0wh-YE0) 3:44:36 to 4:22:29, 23 stretches, posted 11.9 days later)
- 0:00 to 0:20: a teaser that does not align in time, probably from a later round
- Throughout: stream frame (gameplay, facecam bottom right, "iQOO 15" banner bottom left)
- In-game round cards kept: "DEFEAT" at 2:47, "VICTORY" at 7:12 and 13:06
- Full-screen facecam punch-ins at 1:38, 3:26, 4:25 to 4:35, 5:54, 7:52, 14:05 and 14:35 to 14:55, ending on the facecam reaction
- A magenta flash transition at 3:36

**Minute by minute, funny session** — [VF0fmimwQKc](https://www.youtube.com/watch?v=VF0fmimwQKc) (600 s, 189K; source [7dUemvoJ1c0](https://www.youtube.com/watch?v=7dUemvoJ1c0) 3:28 to 3:53, 25 stretches)
- 0:00 to 0:19: cold open labelled "In This Video -"
- 0:24: meme insert (screaming cat)
- Meme or film inserts at 1:23 (politician speech), 2:32 (Bollywood clip), 6:13 (cat again) and 8:46
- Cutaways to the other streamer's facecam at 4:10 and 6:43
- Facecam punch-ins every 30 to 60 s (1:18, 2:02, 3:21, 3:51, 4:05, 4:40, 6:58, 8:11, 8:41)
- 9:40 to 9:45: outro clip; 9:50 to 10:00: black end card

**Minute by minute, crate opening** — [2GJtTk-s_94](https://www.youtube.com/watch?v=2GJtTk-s_94) (550 s)
- Crate animations (purple and gold spins) alternate with the framed facecam reaction every 5 to 15 s
- Meme inserts at 1:39 (baby clip) and 2:08 (Bollywood clip)
- "CONGRATULATIONS" reveal screens at 0:59, 7:01, 7:50 and 8:00
- Ends on the item showcase at 8:10
- Captions show 120 words a minute: crate videos are talk-heavy (16 videos: 91 to 156 wpm, 87% speech coverage)

**Minute by minute, LAN broadcast match** — [nkvIKh72uH8](https://www.youtube.com/watch?v=nkvIKh72uH8) (615 s, 265K, BGMS 2025)
- 0:00: black
- 0:04 to 0:34: broadcast split card (event panel and plane path) with casters previewing the drop clash
- 0:39 to 2:32: observer camera on iQOOSouL's town fight (team sidebar, player-cam inset)
- 2:37 to 4:15: rotations and rock fights, scope shots at 3:31 to 3:41
- 5:19 to 9:20: final zones on a sand ridge, almost continuous
- 9:25 to 9:35: broadcast "WWCD" stage banner
- 9:40 to 9:50: player-cam celebrations
- 9:55: map card; 10:05 to 10:15: black
- The editor added no text

The earlier study's [xtE3WWqt1_E](https://www.youtube.com/watch?v=xtE3WWqt1_E) follows the same shape, with "REPLAY" and "MATCH 14 – ERANGEL" broadcast cards.

**Minute by minute, vlog** — [ah3rZZk3g44](https://www.youtube.com/watch?v=ah3rZZk3g44) (789 s, 206K)
- 0:04 to 1:49: airport travel, handheld wide-angle camera
- 1:54 to 2:09: selfie close-ups
- 2:58: black-and-white letterboxed beat; 3:03 to 3:13: slow motion
- 3:43 to 4:27: hotel
- 4:32 to 6:17: team meal
- 6:22 to 8:36: media day in team jerseys
- 8:41 to 11:39: photo shoot on a black backdrop
- 11:44 to 12:59: late-night talk to camera from bed (outro)
- 13:04: black
- No gameplay at all. Vlogs run 10 to 17 min (18 in 2026, median 691 s) at 154 to 167 words a minute

**Minute by minute, POV match** — [6f0CK3fBrig](https://www.youtube.com/watch?v=6f0CK3fBrig) (2023, 462 s)
- One continuous clean phone POV in Pecado (Miramar), with fights back to back for 7.5 min
- One camera or meme insert at 0:46
- No overlay, no facecam; ends on black at 7:37

**Talk clips** — [Qw5AGoqlUks](https://www.youtube.com/watch?v=Qw5AGoqlUks) "GOBLIN REVEALED HIS NEW TEAM" (120 s), [obSaezZ2oZw](https://www.youtube.com/watch?v=obSaezZ2oZw), [aFBMJVBYxyc](https://www.youtube.com/watch?v=aFBMJVBYxyc), [GJq0QO6QMpw](https://www.youtube.com/watch?v=GJq0QO6QMpw)
- The stream's lobby screen with a framed facecam box, one continuous answer to chat, and a black end card ("Follow me on Kick")
- Talk clips run 95 s median, at 163 words a minute with 98% speech coverage
- The 2023 versions are the same idea with the Loco green bar ("Why Goblin is Benched ?" [IMxzWdu-4UY](https://www.youtube.com/watch?v=IMxzWdu-4UY), "Goblin Leaving SouL ?" [bQaTnJI-uHs](https://www.youtube.com/watch?v=bQaTnJI-uHs))

**Reactions** — [UwBLTW7zAzw](https://www.youtube.com/watch?v=UwBLTW7zAzw), [Qfdg2IzOUus](https://www.youtube.com/watch?v=Qfdg2IzOUus), [KA6gn2BBPsI](https://www.youtube.com/watch?v=KA6gn2BBPsI)
- The stream frame shows the old video in a window plus the facecam; Goblin watches his own old gameplay
- 198 s median, 140 words a minute

**Recurring devices** (census strips and detailed sheets):
- An "IN THIS VIDEO -" label over a 15 to 20 s cold open, on 2025 to 2026 stream cuts: [bWaofDQ7Dzg](https://www.youtube.com/watch?v=bWaofDQ7Dzg), [hvq_G53fQp4](https://www.youtube.com/watch?v=hvq_G53fQp4), [j6kf-4MXXDc](https://www.youtube.com/watch?v=j6kf-4MXXDc), [aRwYyMCIUCI](https://www.youtube.com/watch?v=aRwYyMCIUCI), [nE67VClXWkM](https://www.youtube.com/watch?v=nE67VClXWkM), [VF0fmimwQKc](https://www.youtube.com/watch?v=VF0fmimwQKc)
- SpongeBob-style time cards: "THE NEXT DAY" in [2YaXVaG40y4](https://www.youtube.com/watch?v=2YaXVaG40y4); "A FEW MINUTES LATER" in [a-UTwrUsQm8](https://www.youtube.com/watch?v=a-UTwrUsQm8) and [vTQzMyA5kUo](https://www.youtube.com/watch?v=vTQzMyA5kUo)
- A TV colour-bar card with a pixel-sunglasses meme face as a sting: [a-UTwrUsQm8](https://www.youtube.com/watch?v=a-UTwrUsQm8), [xkd8xrsWiWc](https://www.youtube.com/watch?v=xkd8xrsWiWc), [pdG-_XDypV4](https://www.youtube.com/watch?v=pdG-_XDypV4)
- A "WEAR HEADPHONES" opener card: [tHA0be7H9iE](https://www.youtube.com/watch?v=tHA0be7H9iE) (2023)
- No chapters on any of 526 videos
- Only one description credits music: CC-BY-NC "Makai Symphony – Dragon Castle" on the vlog [cWxjZSKKHuM](https://www.youtube.com/watch?v=cWxjZSKKHuM)

**Stream overlays by era:**
- 2022 to 2023: a green "goblin" bar along the bottom plus a small facecam bottom right
- 2024: a red "GOBLIN" bar ([_EQMb6vHbLk](https://www.youtube.com/watch?v=_EQMb6vHbLk), [lHB_jTSE5Vo](https://www.youtube.com/watch?v=lHB_jTSE5Vo))
- Late 2024 to early 2025: a green and black "GOBLIN" bar ([vESk5MLOplo](https://www.youtube.com/watch?v=vESk5MLOplo))
- Late 2025 to 2026: an "iQOO 15" sponsor banner plus a facecam box
- Mid-2026: a bright-bordered facecam box on a dark frame

**Speech density by type** (caption words a minute; share of seconds with speech):

| Type | Words a minute | Speech coverage |
|---|---|---|
| LAN broadcast | 213 | 100% |
| Talk clip | 163 | 98% |
| Vlog | 161 | 94% |
| Reaction | 140 | 94% |
| Match cut | 123 | 85% |
| Funny edit | 122 | 86% |
| Crate opening | 120 | 87% |
| Custom room | 80 | 73% |
| Frag montage | 72 | 65% |
| Classic or pub | 32 | 43% |

Source: 121 captioned videos. The last two are music-backed.

### Inferences
- **The cut unit is the "session" a title promises:**
  - one match (a WWCD or #2)
  - one custom-room bout, all rounds
  - one crate session from the first spin to the final reward
  - one chat answer
  - one LAN match from the broadcast
  - one travel or competition day
  
  The stretches inside run in order; the only reordering is the cold open.
- The edit budget is tiny and repeatable: about one cold open, facecam punch-ins on reactions, 2 to 6 meme inserts in funny edits only, and round or result screens kept. Everything except the meme choice could be templated.

### Gaps
- Storyboards are 5 to 10 s apart on long videos, so transitions shorter than 2 s and on-screen text timing were not measured. Music was inferred from caption gaps, not heard.
- Who edits the long videos is not public.

## 4. Shorts in depth (all 438)

### Takeaway
Shorts are the channel's main earner: 83.1M views, against 24.6M for the long videos. They come in nine kinds:
- banter clips (121)
- clutch and frag clips (118)
- LAN moments (63)
- hype and nostalgia edits (47)
- gameplay moments with emoji titles (38)
- IRL and community clips (25)
- custom-room clips (12)
- promos for long videos (8)
- crate clips (4) and other games (2)

The common layouts are stacked stream (SS, 124 Shorts) and a vertical game-only crop (VG, 107). **Stacked LAN broadcast plus player-cam (SL, 12) has the highest median, 520K**, and nostalgia edits hold several of the all-time tops. Shorts are posted at night (20:00 to 23:00 IST: 313 of 438), slowed to 2 to 7 a month from June 2026, and in Oct 2026 turned to fan-made edits.

### Cited Findings
- **Shorts by type** (all 438):

  | Type | n | Median length | Median views | Top example |
  |---|---|---|---|---|
  | Funny or banter | 121 | 50 s | 91K | "Struggle of an Esports Athlete" 1.33M [HVisBGxUkAI](https://www.youtube.com/shorts/HVisBGxUkAI); "Denies bounty like a boss" 794K [CdkN90FTUl8](https://www.youtube.com/shorts/CdkN90FTUl8) |
  | Clutch or frag | 118 | 30 s | 64K | "Krutika and Regaltos shocked by Goblin's Crazy 1v3" 1.23M [iVF6tpnxnfA](https://www.youtube.com/shorts/iVF6tpnxnfA); "Goblin Quick 1v3" 1.01M [obYMok4viHI](https://www.youtube.com/shorts/obYMok4viHI) |
  | LAN or tournament moment | 63 | 39 s | 84K | "Team SouL when camera Notices them" 1.77M [z8LmlEAbn-c](https://www.youtube.com/shorts/z8LmlEAbn-c); "Everyone Shocked by @neyo100's 1v4 Clutch" 1.27M [SoWmrN58UYA](https://www.youtube.com/shorts/SoWmrN58UYA); "GodLiN mode on 🚀Jinda pan in BGIS?" 1.24M [Gl8hYRWMP1o](https://www.youtube.com/shorts/Gl8hYRWMP1o) |
  | Hype or nostalgia edit | 47 | 27 s | **109K** | "Revenge 💯🚀" 4.52M [DfOcogRMngg](https://www.youtube.com/shorts/DfOcogRMngg) (a stacked stream clip); "Form is Temporary but Class is Permanent" 2.72M; "Good Old Days" 2.39M |
  | Gameplay moment, emoji or vague title | 38 | 26 s | 46K | "💀" 921K [uCmDja_0DIE](https://www.youtube.com/shorts/uCmDja_0DIE) |
  | IRL or community | 25 | 27 s | 64K | "Hello @legitbgmi" 899K [9kbqFskiaNI](https://www.youtube.com/shorts/9kbqFskiaNI) |
  | Custom room or TDM | 12 | 55 s | **118K** | "Goblin vs Neyo 1v1 with DBS" 3.42M [5QoaTqu_u58](https://www.youtube.com/shorts/5QoaTqu_u58) |
  | Promo for a long video | 8 | 34 s | 14K | |
  | Crate opening | 4 | 55 s | 26K | |

  Source: channel metadata plus title and layout labels
- **Median views by layout:**

  | Layout | n | Median views |
  |---|---|---|
  | SL (stacked LAN) | 12 | **520K** |
  | LB (letterboxed) | 34 | 99K |
  | ED (edit) | 54 | 95K |
  | FC (facecam only) | 36 | 90K |
  | SS (stacked stream) | 124 | 90K |
  | IRL | 63 | 76K |
  | VG (game-only crop) | 107 | 46K |

  Layout use by year:

  | Year | SS | VG | ED | IRL | LB | FC | SL |
  |---|---|---|---|---|---|---|---|
  | 2023 | 15 | 6 | 13 | 5 | 0 | 0 | 1 |
  | 2024 | 54 | 53 | 21 | 22 | 7 | 7 | 1 |
  | 2025 | 43 | 36 | 11 | 19 | 16 | 21 | 1 |
  | 2026 | 18 | 12 | 9 | 18 | 11 | 8 | 9 |

  Source: layout census
- Length: 35 Shorts run 15 s or less (median 87K views), 141 run 16 to 30 s (44K), 109 run 31 to 45 s (101K), 129 run 46 to 60 s (105K) and 24 run over 60 s (105K). Since late 2025, more Shorts run 61 to 123 s.
- Example anatomies (sb0, one frame a second):
  - [YK7JXrVblYQ](https://www.youtube.com/shorts/YK7JXrVblYQ) "Quick 1v3", 313K: stacked game over facecam; a single fight 0:00 to 0:33; a skull-and-crown sticker at 0:34 to 0:36; then the black end card "Follow me on Kick for more content like this" at 0:38 to 0:42. Its first 32 s are the first 32 s of the long "Tournament and Scrims Highlights" [s__lq3xZwKM](https://www.youtube.com/watch?v=s__lq3xZwKM) (43 anchors), posted 48.6 h later
  - [Gl8hYRWMP1o](https://www.youtube.com/shorts/Gl8hYRWMP1o), 80 s, 1.24M: broadcast observer on top, Goblin's LAN player-cam below; stage shots of the "SEMI-FINALS" wall at 0:35 to 0:45; WWCD stage at 1:03 to 1:07; "INDIA SERIES" logo at 1:09; ends on the player-cam reaction
  - [iVF6tpnxnfA](https://www.youtube.com/shorts/iVF6tpnxnfA), 59 s, 1.23M: stacked stream; one continuous 1v3 with no sticker
  - 2024 Shorts often end on a GoBLiN cartoon-logo card ([vtTxFZQ1dlo](https://www.youtube.com/shorts/vtTxFZQ1dlo), [29HOE0cTt58](https://www.youtube.com/shorts/29HOE0cTt58), [948icPF6mr8](https://www.youtube.com/shorts/948icPF6mr8)) or on a pixel-sunglasses meme face ([vd8eUoMDKkw](https://www.youtube.com/shorts/vd8eUoMDKkw), [N4enS_8V2lQ](https://www.youtube.com/shorts/N4enS_8V2lQ), [-XOAZ51cLz0](https://www.youtube.com/shorts/-XOAZ51cLz0)), with troll-face stickers on the payoff ([ARZiWGT1h7g](https://www.youtube.com/shorts/ARZiWGT1h7g), [GuIxQqKwa2w](https://www.youtube.com/shorts/GuIxQqKwa2w))
- **Where Shorts are cut from** (captions of 32 Shorts compared with streams and long videos; 15 matched):
  - **From a long video, posted 0.9 to 1.5 h after it (May to Jun 2026):**
    - "50 Seconds of Bullying @NakuL" 456K [HhcQY2wm8Ug](https://www.youtube.com/shorts/HhcQY2wm8Ug) = the long video [nE67VClXWkM](https://www.youtube.com/watch?v=nE67VClXWkM) at 5:09
    - [QbC6_EK8vGc](https://www.youtube.com/shorts/QbC6_EK8vGc) = [aRwYyMCIUCI](https://www.youtube.com/watch?v=aRwYyMCIUCI) at 6:17
    - [Tllb01bul2M](https://www.youtube.com/shorts/Tllb01bul2M) = [sycnSTtAOKA](https://www.youtube.com/watch?v=sycnSTtAOKA) at 0:00
    - [yrFOqzyI8ys](https://www.youtube.com/shorts/yrFOqzyI8ys) = [gkdmHs83TR4](https://www.youtube.com/watch?v=gkdmHs83TR4) at 5:37
  - **From a long video, posted 1 to 2 days after it:** [WhQAmJWsJ_U](https://www.youtube.com/shorts/WhQAmJWsJ_U) (440K) = [JXSFHpiHkS0](https://www.youtube.com/watch?v=JXSFHpiHkS0) at 6:27, 49 h later; [KpHVV2Hc8T8](https://www.youtube.com/shorts/KpHVV2Hc8T8) = [yincpYxqIrI](https://www.youtube.com/watch?v=yincpYxqIrI) at 1:01, 24 h later
  - **Before the long video:** [4FAhf4pPnQ0](https://www.youtube.com/shorts/4FAhf4pPnQ0) = [ZQxyFEYwLIw](https://www.youtube.com/watch?v=ZQxyFEYwLIw), 14 h before it. [iVF6tpnxnfA](https://www.youtube.com/shorts/iVF6tpnxnfA) (1.23M), [USeVEXljoXY](https://www.youtube.com/shorts/USeVEXljoXY) (398K) and [xhglu2i7RNY](https://www.youtube.com/shorts/xhglu2i7RNY) (473K) come straight from stream [ds2q0wh-YE0](https://www.youtube.com/watch?v=ds2q0wh-YE0) at 3:46:10, 3:27:51 and 3:33:33. They went up 4 to 9 days after the stream and **3 to 8 days before** the long 2v2 WOW video from the same session
  - **From a stream with no matching long video:** [6YLtfV5Ocu8](https://www.youtube.com/shorts/6YLtfV5Ocu8) (44 h after the stream); [V75ArTHWzQs](https://www.youtube.com/shorts/V75ArTHWzQs) (422K, 32 h after stream [NRlAkLKX6BM](https://www.youtube.com/watch?v=NRlAkLKX6BM)); [PEXSwSSNxCU](https://www.youtube.com/shorts/PEXSwSSNxCU) (523K) and [Abcyz2Qr7tU](https://www.youtube.com/shorts/Abcyz2Qr7tU), cut from other moments of stream [EaP6AV_c9ZI](https://www.youtube.com/watch?v=EaP6AV_c9ZI) 16 to 25 days after its long funny edit
- **Promo Shorts** (8, Dec 2024 to Apr 2026; median 14K views): "☝️ Click Here to checkout new video" (222K, [0-Lk3XjUHgk](https://www.youtube.com/shorts/0-Lk3XjUHgk)) shows scope gameplay and ends on the long video's thumbnail card. Others: "FULL VIDEO TOMORROW AT 2 PM" ([1YYxJLfhPoE](https://www.youtube.com/shorts/1YYxJLfhPoE), [ju_Xek0OV_4](https://www.youtube.com/shorts/ju_Xek0OV_4)); "Full video on main channel 📺" ([8PKa9k5eoCk](https://www.youtube.com/shorts/8PKa9k5eoCk))
- Upload hour: 313 of 438 Shorts went up between 20:00 and 23:59 IST (the peaks are 21:00 with 105 and 22:00 with 104). Weekdays are spread evenly (53 to 73 per day) — metadata
- Shorts titles have a median of 21 characters; 43 are emoji-only, such as "💀" and "😂". Long-video titles have a median of 40 characters — metadata
- Engagement: Shorts get a median of 0.100 likes per view and 0.67 comments per 1,000 views; long videos 0.089 and 2.13 — metadata

### Inferences
- The biggest Short wins are **emotion and identity, not skill alone**: revenge, nostalgia, a pro team spotted on camera, friends shocked by a clutch, a 1v1 rivalry. A clutch with named shocked teammates (iVF6tpnxnfA, 1.23M) beats plain "Quick 1v3" Shorts (2024 clutch median 30K).
- The channel does three different Short jobs:
  1. a teaser before the long video (Dec 2025)
  2. a "best 30 to 60 s" posted an hour after the long video (May to Jun 2026)
  3. a standalone moment from a stream with no long video (2024 to 2025 volume)
  
  Since Jun 2026 the Shorts output has dropped and turned to fan edits. That suggests the in-house Shorts work was cut back; this is an inference from counts and credits.

### Gaps
- On-screen text is not legible at storyboard resolution (50x90 to 101x180 per frame). Captions, stickers and fonts inside Shorts could not be read reliably.
- The source of most Shorts (406 of 438) was not caption-checked; only 32 were tried and 15 matched. Many Shorts have too little speech to align (8 to 71 caption words).

## 5. Relationship with the main channel; timing from stream to upload; how many videos one stream gives

### Takeaway
The work splits cleanly:
- **@goblinbgmi** holds the live streams and about one curated, branded phone-recorded tournament highlight a month. It barely posts Shorts (4 in total).
- **@goblinsh0rts** turns those streams (and Loco or Kick streams), LAN broadcasts and life footage into the volume: 24 to 192 long videos a year plus 40 to 165 Shorts.

A good stream yields **1 to 3 long videos plus 2 to 4 Shorts**, released over 1 to 12 days. The first cut usually goes up **17 to 30 h after the stream ends**, at about 21:00 IST.

### Cited Findings
- Main channel: 79 videos (May 2023 to Aug 2026, median 381 s), 100 streams on the Streams tab and 4 Shorts in total. Its highlights are not cut from its YouTube streams (best caption score 63) — `goblin_deep.md`; [@goblinbgmi/streams](https://www.youtube.com/@goblinbgmi/streams)
- No second-channel video is a re-upload of a main-channel video (duration-and-title check across all 79). One Short points viewers to the main channel ("Full video on main channel 📺", [8PKa9k5eoCk](https://www.youtube.com/shorts/8PKa9k5eoCk)).
- **Stream-end to upload lag for 40 caption-matched long videos:**
  - **Under a day:** 2.8 to 21.5 h for 17 of them. Examples: Ev6oMQTJVJ8 2.8 h, 1N27KdUAnkc 8.8 h, wDgeZBn80VM 9.6 h, hvq_G53fQp4 17.6 h, 2GJtTk-s_94 18.4 h, 4QjX1jHoIvA 19.9 h, iAS4xO7xJPw 20.4 h, -5i-6rSEtTg 21.1 h, x3FmFvUKtF4 21.4 h, bWaofDQ7Dzg 21.4 h, 7L0UYZ-1iVk 21.5 h
  - **1 to 5 days:** 13 of them (yucF5hCgl8o, pdG-_XDypV4, 4cC844SCxUk, Q_5n1fA6MO8, d-6B6fjDZSE from the earlier study; qVDUITGVlBw 27 h, qQqy1Pfjs0k 29 h, CsYk1Mmd0Ow 30 h, eZWtpeZVsRc 43 h, yincpYxqIrI 47 h, mRQIXdDEsH0 69 h, gLr68sUlnj0 72 h, gkdmHs83TR4 87 h…)
  - **5 to 12 days:** 10 of them (UbdXp3UzFAA, -5zjIhAhSCg 119 h, _Mjn2Faf1VQ 114 h, VfbRkzjGKl0 138 h, BksSd2q1vXQ 194 h, VF0fmimwQKc 198 h, x612VqS5HZQ 238 h, 7TkLt-j3u4A 285 h, QF7VlJj-QZs about 10 days, j6kf-4MXXDc 7 to 10 days)
  
  Source: this study's alignment plus `goblin_deep.md`
- **Videos per stream** (caption-matched):
  - [ds2q0wh-YE0](https://www.youtube.com/watch?v=ds2q0wh-YE0) (7 Dec 2025): 3 long videos (2v2 WOW ×3, posted 8, 13 and 19 Dec) plus 3 Shorts (11, 12 and 16 Dec)
  - [7dUemvoJ1c0](https://www.youtube.com/watch?v=7dUemvoJ1c0) (2 Jun 2026, a 9.75 h stream): 4 long videos (1v2 TDM 3 Jun, 2v2 WOW 6 Jun, trolling session 11 Jun, 4v4 WOW 13 Jun) plus crate [8uTVdSeesys](https://www.youtube.com/watch?v=8uTVdSeesys) plus 2 Shorts
  - [h4LBvmiT8yg](https://www.youtube.com/watch?v=h4LBvmiT8yg) (7 Jun 2026): crate (8 Jun) and 2v2 WOW (9 Jun)
  - [L0RFKcKTFDI](https://www.youtube.com/watch?v=L0RFKcKTFDI) (5 Aug 2025): 2 crate videos (8 and 10 Aug)
  - [EaP6AV_c9ZI](https://www.youtube.com/watch?v=EaP6AV_c9ZI) (27 Oct 2025): 1 funny long video plus 2 Shorts 2 to 3 weeks later
  - [yUuB2x9H0Qg](https://www.youtube.com/watch?v=yUuB2x9H0Qg) (21 Feb 2026): 3 match videos (earlier study)
- LAN events produce bursts: 5 videos in 2 days at BMSD (17 and 18 Oct 2026, earlier study); 8 BGMS videos in Aug 2026 (4 interviews plus broadcast clips); 11 vlogs between 21 Sep and 2 Nov 2026 — metadata

### Inferences
- **Stream-to-upload rhythm:** the most "storyable" segment is published the next evening, and the rest of the same stream is drip-fed over the following week (custom rooms, trolling sessions). That produces 1 to 2 uploads a day without a new stream.
- The clean POV videos (2023 to 2025) suggest Goblin also hands over raw phone recordings of scrims and tournaments to the second channel, not only to the main one. This is an inference; the hand-off itself cannot be seen.

### Gaps
- Loco and Kick VODs could not be checked, so lags for 2022 to 2023 and mid-2026 content are unknown.
- The share of streams that yield no video at all cannot be measured without the full stream list for those platforms.

## 6. Titles, thumbnails, descriptions, upload timing, and what performs best

### Takeaway
- **Titles:** a formula per type:
  - stats ("Solo 7 Finishes WWCD | …")
  - people ("Goblin + Nakul vs Legit + Joker 2v2 WOW Mode")
  - story ("Patience is the key to success...")
  - "N Minutes of …"
  
  Names of people in the title roughly double the median views.
- **Thumbnails:** always custom. A cut-out of Goblin, a gameplay or scope frame, 2-line bold yellow and white text, red arrows, and a "VS" split for custom rooms.
- **Descriptions:** hashtag strings, nothing else.
- **Timing:** videos at 11:00 or 18:00 to 22:00 IST; Shorts at 20:00 to 23:00.
- **Performance:** custom rooms (89K median) and classic or pub videos (58K) lead the long types. LAN broadcast cuts are the weakest (19K) but go up fastest.

### Cited Findings
- **People in the title:**
  - 2025 to 2026 long videos: 37 titles naming a person or group (teammates, randoms, @handles) have a median of **72.8K views**; 135 without have 34.2K
  - 2025 to 2026 Shorts: 158K against 110K
  - 2023 videos: 55K against 36K
  
  Source: title regex on all items
- Title features: the median long title is 40 characters; 240 of 526 use "|"; 316 contain a number; 235 contain "Goblin"; 29 contain an @handle — metadata
- **Thumbnails** (24 inspected across types):
  - Goblin cut-out (jersey) plus a scope or gameplay frame plus big condensed text ("WITH OLD TEAMMATES / PMGC GRIND" [wDgeZBn80VM](https://www.youtube.com/watch?v=wDgeZBn80VM); "TEAMMATES SHOCKED / GOBLIN IN GODLIN MODE" [5zW1ag4_d_o](https://www.youtube.com/watch?v=5zW1ag4_d_o))
  - Red arrows on the enemy ([6TnQbdev9Oo](https://www.youtube.com/watch?v=6TnQbdev9Oo), [6f0CK3fBrig](https://www.youtube.com/watch?v=6f0CK3fBrig))
  - A "VS" split with names for custom rooms ("GOBLIN + KRUTIKA vs REGALTOS + JOKER" [7TkLt-j3u4A](https://www.youtube.com/watch?v=7TkLt-j3u4A); KR vs IN flags [xiqm0RdJR3o](https://www.youtube.com/watch?v=xiqm0RdJR3o))
  - An MVP stat card for LAN ("MVP DAY 3 MATCH 14", damage 581 [xtE3WWqt1_E](https://www.youtube.com/watch?v=xtE3WWqt1_E))
  - Character art plus a reward grid plus a "SHOCKED" bubble for crates ([x3FmFvUKtF4](https://www.youtube.com/watch?v=x3FmFvUKtF4))
  - A "VLOG" tag with circle insets for vlogs ([ah3rZZk3g44](https://www.youtube.com/watch?v=ah3rZZk3g44))
  
  Thumbnail text often differs from the title: title "Goblin Solo 7 Finishes WWCD in Scrims" against thumbnail "CHICKEN DINNER / SOLO 7 FINISHES" ([-acpEOsyT7k](https://www.youtube.com/watch?v=-acpEOsyT7k))
- **Descriptions:**
  - Videos: 143 of 526 are empty; most others are one hashtag string tied to the team era ("#goblin #goblinislive #soulgoblin" 57; "#goblin #cggoblin #bgms #bmps…" 45; "#goblin #soulgoblin #iqoosoul…" 37)
  - Shorts: 35 of 438 are empty; the rest use a hashtag string (e.g. "#goblin #bgmishorts #cggoblin…" 93)
  - Tags: only 1 video uses tags
  - Links are rare: the 2022 Instagram links; a May 2023 "Vote For Goblin and Mortal" award link on 9 videos; the Kick link (Jun to Jul 2026); the Shorts edit credits (Oct 2026)
- **Upload hours (IST):**
  - Videos: 2023 spread over 13:00 to 18:00; 2024 peaked at 21:00 (30); 2026 split between **11:00 (30)** and 19:00 to 21:00 (45)
  - Shorts: 21:00 to 22:00 in every year from 2024
  - Weekdays: Saturday is the top day for videos (82) and Sunday for Shorts (73)
- **Speed of LAN cuts:** BGMS, BGIS and BMSD broadcast cuts go up during the event (5 BMSD videos in 2 days) and get 19K median (73 videos). The best is "iQOOSouL 42 Points in One Game" at 265K ([nkvIKh72uH8](https://www.youtube.com/watch?v=nkvIKh72uH8)) — metadata; `goblin_deep.md`
- **Engagement:** long videos get 2.13 comments per 1,000 views against 0.67 for Shorts — metadata

### Inferences
- The two strongest long formats are both **relationship formats**: rivalry custom rooms with named opponents (89K median, up to 272K) and classic solo-vs-squad "randoms shocked" videos (58K). Both put other people on screen reacting to Goblin. Plain stat titles do worst (the 2024 POV "Frags" reels: 16K median).
- LAN broadcast cuts are a time-sensitive news product: low median, but cheap (no editing) and occasionally a big hit when the team does something historic.

### Gaps
- Click-through rate and watch time are private, so "what performs" is judged on views only.
- Thumbnail A/B changes cannot be seen.

## 7. What this means for an automatic tool (Kaatclip)

### Takeaway
**More than half of this channel's long videos (292 of 526, carrying 61% of long-video views) and its stacked stream Shorts could be produced automatically** from a creator's own stream recording. These are the stream-layout types:
- single-match cuts
- custom-room session cuts
- crate-opening cuts
- funny or banter sessions
- talk clips
- reaction segments
- stacked 9:16 Shorts

They need a match and round map, a speech and chat map, a facecam box and a few templates. **Out of reach from a stream recording alone:**
- LAN broadcast cuts (another party's broadcast, and rights)
- clean POV hero edits (a separate phone recording)
- vlogs (camera footage)
- nostalgia edits (old footage, photos, film clips)
- fan edits

### Cited Findings (the measured rules a tool can follow)
- **Single match:** keep 23 to 31% of the match; stretches of 25 to 87 s; the final fight whole (142 to 162 s); result plus 15 to 30 s of reaction; 4.5 to 7.5 min — `goblin_deep.md`
- **Custom room (TDM/WOW):** keep 26 to 65% of the session; 9 to 25 stretches of 2 to 135 s; cut the respawn and round waits (gaps of 7 to 100 s); keep the in-game "VICTORY"/"DEFEAT" cards; facecam punch-ins on reactions; end on the facecam; 7 to 15 min (median 442 s). Examples: [7TkLt-j3u4A](https://www.youtube.com/watch?v=7TkLt-j3u4A), [Ev6oMQTJVJ8](https://www.youtube.com/watch?v=Ev6oMQTJVJ8), [4QjX1jHoIvA](https://www.youtube.com/watch?v=4QjX1jHoIvA)
- **Crate opening:** from the first spin to the final reward; alternate reveal screens with facecam reactions every 5 to 15 s; keep "CONGRATULATIONS" reveal screens; 5 to 9 min (median 360 s); 91 to 156 words a minute of talk. Example: [2GJtTk-s_94](https://www.youtube.com/watch?v=2GJtTk-s_94)
- **Funny session:** 1% to 60% of a span; snippets of 1 to 48 s; may reorder (0 to 2 order breaks); cold open plus "In This Video -" label; meme inserts every 1 to 2 min; 2 to 10 min. Examples: [VF0fmimwQKc](https://www.youtube.com/watch?v=VF0fmimwQKc), [hvq_G53fQp4](https://www.youtube.com/watch?v=hvq_G53fQp4), [UbdXp3UzFAA](https://www.youtube.com/watch?v=UbdXp3UzFAA)
- **Talk clip:** one continuous answer from the lobby or chat time (lobby screen plus facecam), 95 s median, 98% speech coverage. Examples: [Qw5AGoqlUks](https://www.youtube.com/watch?v=Qw5AGoqlUks), [IMxzWdu-4UY](https://www.youtube.com/watch?v=IMxzWdu-4UY)
- **Shorts:** 25 to 60 s; stacked game over facecam; one fight or one banter beat; an optional sticker at the payoff and an end card; posted the same evening about 1 h after the long video, or as a teaser before it. Examples: [HhcQY2wm8Ug](https://www.youtube.com/shorts/HhcQY2wm8Ug), [YK7JXrVblYQ](https://www.youtube.com/shorts/YK7JXrVblYQ), [iVF6tpnxnfA](https://www.youtube.com/shorts/iVF6tpnxnfA)

### Inferences (design implications; all are inferences from the data above)
1. **Segment the stream by session type before choosing cuts.** The signals are:
   - lobby or inventory screens (between matches; talk clips live here)
   - crate UI screens (crate session)
   - classic plane and map (match)
   - TDM/WOW round cards and short respawn loops (custom room)
   - facecam-only or IRL frames (chat or IRL)
   
   Each needs its own keep-ratio and length rule, as listed above.
2. **Signals per type:**
   - Match: kill feed and knock detection, result screen OCR (#1 to #4, WWCD), comms loudness
   - Custom room: "VICTORY"/"DEFEAT" round-card OCR, round timer, opponents' names from the lobby
   - Crate: crate UI template match, reveal-screen OCR ("CONGRATULATIONS"), voice-reaction peaks
   - Funny: laughter and shouting in audio, chat-rate spikes, speech without gameplay action
   - Talk: long continuous speech over a static lobby screen, question words, chat "?" spikes
   - Reaction: a second video window in the frame
   - Shorts: the single highest-scoring 20 to 60 s beat, with the facecam located for the stacked layout
3. **Packaging defaults Kaatclip can copy:**
   - an "IN THIS VIDEO -" cold open of 15 to 20 s, taken from the best beat
   - facecam punch-ins on peak reactions
   - optional meme inserts, from the creator's own library only (rights)
   - a black end card with the creator's call to action
   - title templates: "{who} vs {who} {mode}", "{N} Minutes of {verb}ing {who}", "Solo {k} Finishes WWCD in {event}" and "{who} Shocked"
   - a thumbnail spec: cut-out plus scope frame plus 2-line text plus an arrow, or a VS split
   - an upload suggestion: first cut the next evening (17 to 30 h after the stream), Shorts at 21:00 to 22:00 IST, the rest drip-fed over 3 to 10 days
4. **One stream should give a batch, not one video:** 1 to 4 long cuts (match, custom room, crate, funny) plus 2 to 4 Shorts, scheduled over a week. That is how GoBLiN shorts posts 12 to 23 videos a month from 1 to 6 YouTube streams.
5. **Out of reach, and why:**
   - LAN broadcast cuts: someone else's footage. They need the broadcaster's VOD and permission; a creator's stream does not contain the observer feed. Kaatclip could, at most, cut the creator's own co-stream if it is allowed.
   - Interviews: broadcast footage.
   - Vlogs: camera footage and story editing.
   - Hype or nostalgia edits: old clips, photos, film inserts and music beats; rights issues and creative choice.
   - Clean POV hero edits: need the phone's own screen recording.
   - Fan edits: made outside.
   - Meme inserts from films or TV: a Content ID risk. Kaatclip should only offer creator-supplied or licensed stickers and sounds.
6. **Priority for Kaatclip by value per effort on this channel's numbers:**
   - Custom-room session cuts first (89K median; fully from the stream; simple round logic)
   - Then stacked Shorts (90K median for SS)
   - Then funny or banter sessions (49K)
   - Then single-match cuts (34K)
   - Crate cuts last (31K; easy to detect, but lower interest)

### Gaps
- All thresholds come from 40 matched videos and 15 matched Shorts of one creator. They should be checked on the owner's own test streams.
- Detection accuracy for round cards, crate screens and lobby screens on varied OBS layouts is untested.
- How these formats behave for small creators is unknown: Goblin's results rest on a 131K-subscriber second channel and a famous player.
