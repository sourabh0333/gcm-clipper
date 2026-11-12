# Joker Ki Haveli (@Jokerkihavelii) main channel, A to Z: every content type, its source, how it is made and uploaded

Research date 12 Nov 2026. Public YouTube data only (yt-dlp metadata, listings, auto-captions, storyboard images and thumbnails; no video or audio was downloaded) plus a few web profiles. This builds on `research_notes/BGMI highlight channels deep study/joker_deep.md` (JokerClips highlights, source mapping, Shorts) and `research_notes/BGMI highlight video structure/joker_comedy.md`, and does not repeat their JokerClips findings except where needed. Raw data and scripts are in `C:\Users\soura\AppData\Local\Temp\claude\21027423ba80eb72\c7886632-c6c6-4a95-81c6-c6cbac2a769e\scratchpad\a2z\joker_main\`: `meta.jsonl` and `meta_streams.jsonl` (metadata for all 499 videos and samples of Shorts and streams), `full\` (full metadata of 62 studied uploads), `subs\` (their captions), `sbr\` (storyboard sheets), `streamcap.json` (caption statistics of 34 streams). "Inference" marks reasoning beyond what was measured.

## 1. Full inventory: every upload, classified, and how the mix changed

### Takeaway
On 12 Nov 2026 the main channel holds 499 videos, 1,310 past streams and 273 Shorts. Streams are the constant: an estimated 8-38 a month since Oct 2020 (most in 2020-21, fewest in late 2022, 10-15 a month in 2026), 4-6 hours each. The videos tab changed completely. In 2020-21 almost every video was a cut from his streams (GTA RP comedy, Marfa dance raids, montages, early Shorts); in 2022 stream cuts (Among Us, reactions, BGMI) shared the tab with the first S8UL vlogs; from 2023 the tab became a camera-shot vlog channel (93% of 2023 uploads, 89-100% since), and stream-based gaming moved out: the last regular BGMI compilation on the main channel was 13 Sep 2023, and JokerClips began its 8-minute session highlights in Dec 2023. Since 2024 BGMI appears on the main channel only as a few "challenge" or collab videos (9 in total). Output fell from 147 videos in 2022 to 34 in 2026 while length rose from a median 533 s to 1,135 s and median views from 255K to 513K.

### Cited Findings
**Method.** Flat listings of the three tabs (taken earlier today for the deep study) and full metadata for all 499 videos, 137 of the 273 Shorts (every second one) and 83 streams (every 16th, plus 36 already dated), fetched with yt-dlp without downloading media. Every video was classified by title keywords with manual overrides, then checked against storyboard frames for 30 sampled uploads. Stream dates between dated samples were interpolated by listing order. Script and data: `scratchpad\a2z\joker_main\` (`vidcls.py`, `streamcls2.py`, `shortcls.py`, `meta.jsonl`).

**Videos tab (499), by type**

| Type | Source | n | Years | Median length | Median views | Max views |
|---|---|---|---|---|---|---|
| Vlog / IRL (family, travel, events, S8UL house, weddings) | Shot | 271 | Dec 2020-Oct 2026 | 921 s (IQR 723-1,110) | 339K | 3.1M |
| IRL challenge / game with S8UL or family | Shot | 54 | Nov 2021-Apr 2026 | 885 s | 332K | 1.8M |
| Social experiment / "24 hours as X" | Shot | 18 | Nov 2022-Nov 2026 | 968 s | 678K | 2.3M |
| Documentary | Shot | 2 | Nov 2025, Aug 2026 | 1,940 s | 608K | 769K |
| Tech, setup, sponsor | Shot | 9 | 2021-2024 | 483 s | 116K | 804K |
| GTA RP funny moments, trailers, music parodies | Stream | 35 | Oct 2020-Sep 2022 | 315 s | 32K | 172K |
| Marfa dance raids | Stream | 21 | Nov 2020-Aug 2022 | 411 s | 277K | 1.4M |
| Among Us / Pico Park / other-game highlights | Stream | 21 | Dec 2020-Dec 2024 | 530 s | 332K | 704K |
| Reactions | Stream | 14 | Jun 2021-Oct 2022 | 431 s | 258K | 1.7M |
| BGMI/PUBG stream highlights and compilations | Stream | 21 | Apr 2021-Sep 2023 | 434 s (IQR 385-473) | 142K | 382K |
| Montages | Stream/game | 4 | 2020-21 | 172 s | 15K | 25K |
| Shorts posted on the videos tab | Stream | 13 | Dec 2020-May 2021 | 48 s | 20K | 43K |
| BGMI challenge / collab (stream-recorded or IRL-shot) | Mixed | 9 | Jan 2024-Sep 2025 | 791 s | 546K | 695K |
| Milestone, motivational, announcement | Mixed | 7 | 2021-22 | 411 s | 30K | 408K |

— classification over the [videos tab](https://www.youtube.com/@Jokerkihavelii/videos); examples per row in sections 2-3

**Videos by year**

| Year | Uploads | Stream-based | Shot | Mixed | Median length | Median views (shot / stream) |
|---|---|---|---|---|---|---|
| 2020 (from 26 Oct) | 15 | 14 | 1 | 0 | 515 s | 16K / 30K |
| 2021 | 60 | 48 | 9 | 3 | 249 s | 51K / 24K |
| 2022 | 147 | 57 | 86 | 4 | 533 s | 281K / 195K |
| 2023 | 122 | 9 | 113 | 0 | 849 s | 269K / 183K |
| 2024 | 66 | 1 | 59 | 6 | 936 s | 429K / 59K |
| 2025 | 55 | 0 | 52 | 3 | 1,166 s | 508K / n/a |
| 2026 (to 12 Nov) | 34 | 0 | 34 | 0 | 1,135 s | 513K / n/a |

- Monthly uploads in 2025-26: 1-8 a month (median gap between uploads 5 days, longest 42 days). — upload dates
- The channel's first video is a GTA RP clip of 26 Oct 2020 ([T_o-Sl7lIfw](https://www.youtube.com/watch?v=T_o-Sl7lIfw)); its first stream, "NEW CHANNEL NEW JOURNEY | JokerKiHaveli | gaming live", is dated 21 Oct 2020. A web profile says he started on YouTube in 2016 with vlogs while working in Qatar, i.e. on an older channel. — [streams tab](https://www.youtube.com/@Jokerkihavelii/streams), [SportsDigest profile](https://sportsdigest.in/?p=156804)
- The switch to vlogs follows his move into S8UL: "Swagat Nahi Karoge Hamara | S8uL Bootcamp vlog" (21 Jun 2022, 1.1M) and the Short "Ye kya maar diya 1v3 S8uL mai aate sath" (24 Jun 2022) open the S8UL period; 77 vlogs followed in 2022. — [-UgHSCx7ly0](https://www.youtube.com/watch?v=-UgHSCx7ly0), [NqUcnKv-mos](https://www.youtube.com/shorts/NqUcnKv-mos)

**Where the stream compilations went (JokerClips)**
- Main-channel BGMI compilations ran Apr 2021-Sep 2023; the last two were "KON HAI BEST IGL… PART 2" (6 Sep 2023, 251K) and the mummy-cosplay crate opening (13 Sep 2023, 181K). In 2022-23 they drew a median 89K (2022) and 183K (2023), against 288K and 251K for that year's vlogs. — [hsewvcFNS_E](https://www.youtube.com/watch?v=hsewvcFNS_E), [XaztTwBGhJ0](https://www.youtube.com/watch?v=XaztTwBGhJ0)
- From Sep 2022 descriptions advertise "My shorts channel @jokerclipss", from 2023 "Second Channel @jokerclipss". JokerClips posted short stream clips (30-300 s) in 2022-23 and switched to the 8:00-8:10 session highlight in Dec 2023 (first: [E6h-WNsY7jM](https://www.youtube.com/watch?v=E6h-WNsY7jM), 21 Dec 2023, 1.06M). — [_7WVFXJ9hkk](https://www.youtube.com/watch?v=_7WVFXJ9hkk), [5szLSGgb5bE](https://www.youtube.com/watch?v=5szLSGgb5bE); deep study section 1
- After that, the main channel kept only BGMI videos with a hook beyond a session: a feud ("Goldy Bhai Got My *BGMI ID BAN*", Jan 2024, 547K), a gimmick ("I PLAYED BGMI WITH SCOUT'S *SENSITIVITY*", Jan 2024, 423K; "I Became PRESIDENT In BGMI", May 2024, 572K), a sponsor shoot ("JOKER vs SNAX IRL 1V1", May 2024, 662K), an IRL emote challenge (May 2025, 696K) or a money challenge ("I Won ₹3,40,000", Sep 2025, 673K). — [5szLSGgb5bE](https://www.youtube.com/watch?v=5szLSGgb5bE), [XAOEpLBp_Gg](https://www.youtube.com/watch?v=XAOEpLBp_Gg), [gnl2JShBGM8](https://www.youtube.com/watch?v=gnl2JShBGM8), [CFt9BX7llGY](https://www.youtube.com/watch?v=CFt9BX7llGY), [qTKpbt9E6bY](https://www.youtube.com/watch?v=qTKpbt9E6bY), [WBq__Fc-pqM](https://www.youtube.com/watch?v=WBq__Fc-pqM)

**Streams tab (1,310), by era (game labels from titles; one stream can carry several)**

| Year | Streams (est.) | Median length | Median views | Start time (median of dated streams) | Games named in titles |
|---|---|---|---|---|---|
| 2020 (21 Oct-Dec) | 73 | 6.3 h | 27K | 21:24 IST (2020-22) | GTA RP 51, BGMI/PUBG 39 |
| 2021 | 306 | 5.5 h | 20K | 21:24 | GTA RP 206 (Shinde on HTRP / Exo Life RP), BGMI 67, other games 30, Valorant 29 |
| 2022 | 203 | 4.7 h | 43K | 21:24 | GTA RP 94, BGMI 40, chat 27, Among Us 25 |
| 2023 | 175 | 4.6 h | 87K | 14:18 | BGMI 88, GTA RP (Soulcity, Gullu Dada) 51, Valorant 17 |
| 2024 | 196 | 4.6 h | 96K | 13:18 | BGMI 159, other games 38 (Black Myth Wukong, Resident Evil 4, Star Wars Outlaws, God of War) |
| 2025 | 230 | 4.4 h | 116K | 20:12 | BGMI 124, GTA RP 87 (57 of them members-only), chat 25, watch parties 22 |
| 2026 (to 12 Nov) | 127 | 4.5 h | 140K | 21:06 | BGMI 78, other games 20, chat 19, GTA RP 16, crate openings 12, watch parties 11, IRL 8 |

— per-year counts interpolated between about 120 dated streams; game labels by title keywords; [streams tab](https://www.youtube.com/@Jokerkihavelii/streams). Estimated streams per month: 22-38 in 2020-21, 8-12 from Aug 2022 to Apr 2023, 9-24 in 2024-25, 10-15 in 2026.

**Shorts tab (273)**: see section 5.

### Inferences
- Why the compilations moved (inference, no statement found): from 2022 the vlogs out-viewed the stream compilations on the same channel by 1.4-3x, so the main channel was kept for camera-shot content and the steady stream highlights went to a second channel where they no longer pull down the main channel's averages. The move also coincides with the vlogs getting longer and more produced (median 849 s in 2023, 1,166 s in 2025).
- For Kaatclip this creator is two customers in one: his streams feed a clips channel and gaming Shorts (in reach), while his main channel is a vlog business (out of reach).

### Gaps
- The classification is by title with manual fixes; a few vlog-titled videos may contain stream footage and vice versa.
- Stream counts per year and month before Dec 2025 are interpolated between about 120 dated streams; the yearly totals are approximate (±10%).
- No source explains the 2022-23 dip in streams (about 8-12 a month) beyond the Loco tags in titles.

## 2. What each content type is based on (source proof)

### Takeaway
Everything gaming on this channel comes from his own live streams, and the proof is on screen: the stream overlay (JOKER banner, follower counter, sponsor badges, Loco watermark, Super Chat alerts) is kept in the edit. GTA RP funny moments (2020-22), Marfa dance raids (2021-22), Among Us and reaction compilations (2022), BGMI funny compilations (2021-23), stream-based BGMI challenges (2024-25) and most gaming Shorts are all cut from streams. Everything else, which is now the bulk of the videos tab, is shot separately with cameras: vlogs, travel, family, IRL challenges with S8UL, "24 hours as X" social experiments, sponsored product videos and a documentary.

### Cited Findings
**Stream-based types (overlay evidence from storyboard frames)**

| Type | Example | Evidence it is a stream recording |
|---|---|---|
| GTA RP funny moments (Shinde character) | [wBcYpF_FgDM](https://www.youtube.com/watch?v=wBcYpF_FgDM) 27 Nov 2020, 427 s, 173K | GTA RP footage with his small facecam overlay; same server and character as the 2020-21 streams ("Officer Ismail Shinde… Exo Life RolePlay", [F8LzticZItQ](https://www.youtube.com/watch?v=F8LzticZItQ)); description asks for Paytm tips like the stream pages |
| Marfa dance raid | [9gH5HLGcLFg](https://www.youtube.com/watch?v=9gH5HLGcLFg) 30 Dec 2021, 482 s, 1.05M; [O9QCVmEZp84](https://www.youtube.com/watch?v=O9QCVmEZp84) 19 Dec 2021, 411 s, 1.49M | Two webcams side by side for the whole video (his and the other streamer's video call), with brief cuts to the other streamer's stream screen |
| Among Us with S8UL | [UcUCylFQ24I](https://www.youtube.com/watch?v=UcUCylFQ24I) 28 Oct 2022, 685 s, 610K | Loco watermark on every frame, his facecam bottom-left, cut-ins of other players' webcams |
| Reaction session | [_7WVFXJ9hkk](https://www.youtube.com/watch?v=_7WVFXJ9hkk) 4 Sep 2022, 416 s, 1.71M; [-nZQzlrIeXE](https://www.youtube.com/watch?v=-nZQzlrIeXE) 26 Sep 2022, 575 s, 1.04M | YouTube Super Chat alert boxes and a "DONATIONS" panel in frame (1:23, 3:05, 3:20); a Loco-branded grid of five S8UL webcams with a live counter |
| BGMI funny compilation | [VOvG30dwlq8](https://www.youtube.com/watch?v=VOvG30dwlq8) 31 Aug 2023, 420 s, 309K | JOKER banner and follower counter; counter runs 580,685 → 580,965, then 579,365, then 580,457: at least three different streams; shirt changes at 6:35 |
| BGMI crate opening | [XaztTwBGhJ0](https://www.youtube.com/watch?v=XaztTwBGhJ0) 13 Sep 2023, 480 s, 181K | Stream banner, counter rising 589,085 → 589,350 |
| BGMI highlight with co-streamer POV | [Du8VpIvMs04](https://www.youtube.com/watch?v=Du8VpIvMs04) 29 Jun 2023, 269 s, 183K | Cuts between Joker's layout and Payal Gaming's own stream layout ("PAYAL GAMING" banner) |
| BGMI "challenge" on main channel | [WBq__Fc-pqM](https://www.youtube.com/watch?v=WBq__Fc-pqM) 10 Sep 2025, 610 s, 673K | Stream layout with counter (~1.09M); on stream he says "ye highlight main channel pe jaayegi" (8:51, caption rendered "आइलैंड मेन चैनल पे जाएगी"); the stream tab has matching challenge streams with iQOO tags (e.g. "₹2,00,000 CHALLENGE IN BGMI", Jan 2026) |
| BGMI highlight 2024 | [5szLSGgb5bE](https://www.youtube.com/watch?v=5szLSGgb5bE) 22 Jan 2024, 540 s, 547K | Counter 655,5xx; family voices from the room ("Mazin ko bahar leke jao, Marzina do minute jao", 7:30) |
| Gaming Short | [CVqRiZ-wwNw](https://www.youtube.com/shorts/CVqRiZ-wwNw) 27 Nov 2024, 27 s, 536K | Vertical crop that keeps the JOKER banner and counter (900,115) under the gameplay |
| JokerClips session highlights | see the deep study | Caption alignment to six specific streams (previous note) |

- On stream he sometimes tells the editor what to do with a moment: "beech zara cinematic aur music daal ke dena" (add some cinematic shots and music in between), heard inside the 2023 compilation [VOvG30dwlq8](https://www.youtube.com/watch?v=VOvG30dwlq8) at 1:30; "editor, clipping ke liye ready ho ja" in the JokerClips video [Ul5mEjNyzu4](https://www.youtube.com/watch?v=Ul5mEjNyzu4).

**Shot (non-stream) types**

| Type | Example | Evidence |
|---|---|---|
| IRL vlog (event, family, travel) | [5nMlWDfU8co](https://www.youtube.com/watch?v=5nMlWDfU8co) 20 Oct 2026, 921 s, 2.5M (friend's wedding) | Handheld selfie camera, car and venue footage, no overlay |
| Produced social experiment | [CTVXMQ_3YUY](https://www.youtube.com/watch?v=CTVXMQ_3YUY) 8 Nov 2023, 951 s, 1.55M ("Working 24 hours as a Zomato rider") | Second camera operator, street B-roll, on-screen order-progress graphics |
| IRL group challenge with S8UL | [1LJGpvepf3Y](https://www.youtube.com/watch?v=1LJGpvepf3Y) 28 Jan 2024, 960 s, 1.72M; [qTKpbt9E6bY](https://www.youtube.com/watch?v=qTKpbt9E6bY) 4 May 2025, 1,173 s, 696K (BGMI emotes acted out in real life) | Multi-camera studio/gaming-house shoot, name and city title cards, no gameplay |
| BGMI IRL 1v1 (sponsored) | [CFt9BX7llGY](https://www.youtube.com/watch?v=CFt9BX7llGY) 26 May 2024, 792 s, 662K | Product B-roll for Boult earbuds, both players on a couch, phone screen recordings split "JOKER POV / SNAX POV" |
| Sponsored game video | [zGC5FiC8Dwg](https://www.youtube.com/watch?v=zGC5FiC8Dwg) 24 Dec 2024, 746 s, 60K (World of Tanks) | Costume intro shoot, sponsor read with promo code, a facecam layout unlike his stream |
| Documentary | [f-VuyqERGL8](https://www.youtube.com/watch?v=f-VuyqERGL8) 17 Nov 2025, 2,318 s, 769K, 8 chapters | Lit sit-down interviews (him, his mother, his wife, colleagues), "CHAPTER 2" cards, archive clips |
| Lifestyle Shorts | [liTFXMbHsrg](https://www.youtube.com/shorts/liTFXMbHsrg) 6 Mar 2026, 79 s, 52.4M ("Ramadan Routine Ft IND vs ENG") | Native vertical phone video, 1-2 s cuts through a day ending at a stadium |
| Skit Shorts | [nTbYY4kgYfI](https://www.youtube.com/shorts/nTbYY4kgYfI) 7 Apr 2026, 23 s, 2.17M; [s_zeXPa8RIM](https://www.youtube.com/shorts/s_zeXPa8RIM) 2 Mar 2025, 27 s, 5.97M | Staged vertical scenes with a fixed top caption ("That one friend who can't take jokes on himself") or a sticker label ("PERSONAL 😐") |

**Second channels, from the descriptions**
- 2020-22 descriptions point to "My Second Channel: youtube.com/c/GulrezKhan" (later "My VLOG Channel"); from Sep 2022 "My shorts channel @jokerclipss"; from 2023 "Second Channel @jokerclipss" and "Business enquiry jokerkihaveli@8bitcreatives.in". — [Iqz-a9mjqIg](https://www.youtube.com/watch?v=Iqz-a9mjqIg), [3xOrJq_DYGE](https://www.youtube.com/watch?v=3xOrJq_DYGE), [_7WVFXJ9hkk](https://www.youtube.com/watch?v=_7WVFXJ9hkk), [CTVXMQ_3YUY](https://www.youtube.com/watch?v=CTVXMQ_3YUY)
- His S8UL period starts mid-2022: the first S8UL bootcamp vlog is dated 21 Jun 2022 ([-UgHSCx7ly0](https://www.youtube.com/watch?v=-UgHSCx7ly0)), and a GuruGamer profile says S8UL co-founder Goldy persuaded him to make one more serious attempt before he joined, after he had considered returning to his job in Qatar ([GuruGamer](https://gurugamer.com/streamers/from-night-streams-to-nursery-rhymes-how-gulrez-khan-balances-gaming-and-fatherhood-24906)).

### Inferences
- Of the main channel's content types, only the stream-derived ones are in Kaatclip's reach. Today that is a small share of main-channel uploads (see section 1) but it is all of JokerClips and the gaming Shorts.
- The editor works from the stream VOD (or local recording) and keeps the overlay; nothing in the frames suggests separate clean game captures. A tool that cuts from the VOD with overlays intact matches the real look.

### Gaps
- For the 2020-22 GTA RP and Marfa videos, no stream from that week was caption-matched; the source is inferred from layout and character, not proven moment by moment.
- Whether the shot vlogs use any stream footage at all (e.g. stream clips inside the documentary) was seen only in the documentary (archive stream frames at 28:31-29:10).

## 3. How each content type is made (structure, devices, layout, length)

### Takeaway
The stream-derived long videos share one editing grammar that has barely changed since 2022: stream layout as the base, crop-zoom to the facecam for every talk beat, cut-ins of friends' webcams or their stream POV, meme inserts with one-word labels, burned-in subtitles of key lines, B&W freezes, time cards, scope/result screens kept, and a short outro card. What changed: length (4-11 min in 2021-23, a hard 8:00-8:10 on JokerClips from Dec 2023), the "IN THIS VIDEO" cold-open teaser (on the main channel from Jan 2024; on JokerClips once in Dec 2023 and regularly from Apr 2026), and multi-stream compilations. Shot vlogs and IRL challenges are 13-25 minute documentary-style edits; lifestyle Shorts are 60-80 s rapid montages.

### Cited Findings
**Minute-by-minute 1: [VOvG30dwlq8](https://www.youtube.com/watch?v=VOvG30dwlq8) "THE FUNNIEST BGMI MOMENTS 🤣 - Part 1" (main channel, 31 Aug 2023, 420 s, 309K; squad Snax, Goldy, Kaash)**

| Time | Screen | What happens |
|---|---|---|
| 0:00-0:14 | Black, then 3 gameplay shots (one from Goldy's stream with a "GOLDY" banner) | Hook montage |
| 0:19-0:24 | Full-frame friends' webcams laughing (Snax with cap, another friend) | Reaction hook |
| 0:29-1:38 | Joker's facecam zoomed full frame; pink subtitles ("washroom ho gaya", "hai na"); a woman-reaction meme at 0:44 | Excuse for being late ("10:30 ko nahi 11:15 ko gaya… thumbnail bana raha tha"), then the live instruction "beech zara cinematic aur music daal ke dena" |
| 1:43-3:12 | Gameplay with zooms to the facecam every 10-20 s; scope view at 3:07 | Rank-push fights ("serious khel bhai please") |
| 3:17-4:51 | Gameplay, facecam zooms, a game pop-up at 4:07, plane at 4:46 | Fights and banter |
| 4:56-6:30 | Gameplay from two other streams (counter 579,365, then 580,457) | Second and third session |
| 6:35-6:40 | Facecam in an orange shirt (another stream) | Closing reaction |
| 6:45-6:50 | "THANKS FOR / SUBSCRIBE" animated end card | Outro |

**Minute-by-minute 2: [gUArapQLbCo](https://www.youtube.com/watch?v=gUArapQLbCo) "RANDOMS KIDNAPPED ME | Funny BGMI Squad" (16 Jun 2023, 304 s, 158K)**

| Time | Screen | What happens |
|---|---|---|
| 0:00-0:05 | Gameplay hook | n/a |
| 0:09-0:14 | Animated neon "JOKER" logo sting | Channel intro |
| 0:19-1:08 | Zoomed facecam with sticker faces of the random teammates and their lines as captions ("*Ignored*", "Ye kaisi baat kr raha hai yr", "I am IGL", "Turn off your mic", "Deafen Go..", "You go play TDM", "I will survive") | Randoms bossing him around |
| 1:13-2:46 | Gameplay with "Shootout" text, facecam zooms | Fights |
| 2:56-3:11 | Map screen with sticker captions ("Pe utaringa", "Pura control lena hai") | Drop argument |
| 3:30-4:34 | A different stream (purple banner, yellow shirt), facecam laughing | Second session |
| 4:39-4:54 | End screen with subscribe button and two video tiles | Outro |

**Minute-by-minute 3: [UcUCylFQ24I](https://www.youtube.com/watch?v=UcUCylFQ24I) "KUCH KUCH HOTA HAI IN AMONG US" (28 Oct 2022, 685 s, 610K)**

| Time | Screen | What happens |
|---|---|---|
| 0:00-0:49 | Lobby, his zoomed facecam, voting screen, the name box "RAH(UL)", friends' webcams (Aman at 0:44) | Joker plays "Rahul" from Kuch Kuch Hota Hai and woos "Anjali" in voice chat |
| 1:09 | "SHHHHH!" impostor card | Role reveal |
| 1:14-5:52 | Game map, meeting screens ("Who is the impostor?"), "DEAD BODY REPORTED", B&W zoom at 4:13 | Rounds cut down to the accusations and votes |
| 6:47 | Bollywood film still with labels "SNAX" and "JOKER" | Meme insert |
| 7:01-9:50 | "Your role is Impostor", kill animations, votes | Second game |
| 10:35-10:55 | Joker at his desk talking to camera: "I hope aapne ye enjoy kiya hoga hamara Kuch Kuch Hota Hai" | Recorded outro |
| 11:05-11:15 | Animated "FOR…" end card | Outro |

**Minute-by-minute 4: [5szLSGgb5bE](https://www.youtube.com/watch?v=5szLSGgb5bE) "Goldy Bhai Got My *BGMI ID BAN* After This?" (22 Jan 2024, 540 s, 547K)**

| Time | Screen | What happens |
|---|---|---|
| 0:00-0:15 | "IN THIS VIDEO" label over 3 shots | Teaser (earliest teaser seen on the main channel) |
| 0:19-0:44 | Gameplay with facecam, sticker face of a random | "Aise time pe kya team up karoon, batao chat" |
| 0:44-1:09 | Gameplay, counter 655,52x | Gate-pun question from a teammate, then a fight |
| 1:30-2:30 | Gameplay, meme insert of a woman in yellow glasses at 2:23 | Begging for medkits and bandages from Goldy; revive |
| 3:00-3:50 | Gameplay, an old-man meme at 3:17, a dog meme at 3:42, a speech bubble at 3:27 | Landing argument, "Goldy bhai do shabd teamwork ke naam" |
| 4:36-5:11 | Facecam laughing, then Goldy's webcam full frame twice | Goldy's reaction |
| 5:16-7:00 | Gameplay with vehicles | Chase, "gaadi mein daal" |
| 7:00-8:00 | Gameplay | Swearing, then "Mazin ko bahar leke jao, Marzina do minute jao" (family in the room), "Krafton ko bol ke account ban karaya" |
| 8:04-8:44 | Counter drops to 655,50x (earlier footage), gameplay | "Main chal nahi pa raha hoon" (ID restricted); ends abruptly |

**Minute-by-minute 5: [WBq__Fc-pqM](https://www.youtube.com/watch?v=WBq__Fc-pqM) "I Won ₹3,40,000 Challenge in BGMI w/ @SnaxGaming" (10 Sep 2025, 610 s, 673K)**

| Time | Screen | What happens |
|---|---|---|
| 0:00-0:20 | "IN THIS VIDEO" teaser | Key lines |
| 0:29-0:40 | Facecam full frame, Joker holding phone | The terms: Snax pays ₹1,000 a kill; 55 kills plus a chicken dinner wins ₹3 lakh |
| 0:49-1:20 | Gameplay with counter (about 1.09M) | First match starts ("recall de bhai") |
| 1:20-2:30 | Facecam full frame | Negotiation recap ("2 kill to 2000… 50 hua to 50,000") |
| 2:38-3:40 | Gameplay | First attempt falls 3 kills short; "the next day…" spoken at 3:50 |
| 4:07-8:30 | Next-day stream (white T-shirt), gameplay with scope shots | Second attempt; kill count rising |
| 8:35-8:45 | Results/scoreboard screens | "58 maare… ye highlight main channel pe jaayegi" |
| 8:55-9:45 | Facecam, celebration and phone | "Tapasya thi yaar… aaj ke baad koi nahi bolega tujhe khelna nahi aata" |
| 9:55 | "THANKS FOR WATCHING" end card | Outro |

**Other stream-based formats (storyboards)**
- Marfa raid ([9gH5HLGcLFg](https://www.youtube.com/watch?v=9gH5HLGcLFg), 482 s): a single continuous video call cut to the dance and the other streamer's reaction; little else.
- Reaction ([_7WVFXJ9hkk](https://www.youtube.com/watch?v=_7WVFXJ9hkk), 416 s): glitch "JOKER" intro card at 0:05, Regaltos' old videos full frame with Joker's facecam top-left, label inserts ("REGALTOS", "REGA IN CHAT", skull "THA???"), colour-bars glitch transition at 5:13.
- Group reaction ([-nZQzlrIeXE](https://www.youtube.com/watch?v=-nZQzlrIeXE), 575 s): grid of five webcams, green "NEXT UP: ANKKITA / BINKS / SID" cards between turns.
- Older 2022 BGMI highlight ([D6Odowb1TPs](https://www.youtube.com/watch?v=D6Odowb1TPs), 437 s): purple 2022 layout, facecam zooms, "MAIYAAT" text card, B&W ending.
- 2023 compilations close with the same animated "THANKS / LIKE & COMMENT / SUBSCRIBE" card ([VOvG30dwlq8](https://www.youtube.com/watch?v=VOvG30dwlq8), [Du8VpIvMs04](https://www.youtube.com/watch?v=Du8VpIvMs04), [XaztTwBGhJ0](https://www.youtube.com/watch?v=XaztTwBGhJ0)).

**Shot formats**
- IRL challenge ([1LJGpvepf3Y](https://www.youtube.com/watch?v=1LJGpvepf3Y), 960 s): neon "HELLO" title, handheld single-camera rounds through the gaming house, big city-name cards ("MATHURA", "KOCHI") as the answers, subscribe button at the end.
- Documentary ([f-VuyqERGL8](https://www.youtube.com/watch?v=f-VuyqERGL8), 2,318 s): 8 YouTube chapters (the only chaptered upload in the sample), sit-down interviews with family and colleagues.
- Vlog ([5nMlWDfU8co](https://www.youtube.com/watch?v=5nMlWDfU8co), 921 s): selfie-camera talk to lens, gym, getting ready, car rides, the venue; no title cards.

**Length**
- | Format | Measured lengths |
|---|---|
| GTA RP funny moments 2020-22 | median 315 s (IQR 135-509), n=35 |
| Marfa raids 2020-22 | median 411 s, n=21 |
| Among Us / other-game highlights 2020-24 | median 530 s (IQR 464-605), n=21 |
| BGMI stream compilations 2021-23 (main channel) | median 434 s (IQR 385-473), n=21; none near 8:00 |
| JokerClips session highlights Dec 2023-2026 | 480-489 s in 69 of 133 (deep study) |
| BGMI challenge / collab 2024-25 (main) | median 791 s, n=9 |
| Vlogs / IRL | median 921 s; median of all uploads per year 849 s (2023), 936 s (2024), 1,166 s (2025), 1,135 s (2026) |
| Gaming Shorts | 14-60 s, median 34 s (24 dated) |
| Lifestyle routine Shorts | median 90 s, up to 154 s (41 dated) |

— durations from the listings and metadata

### Inferences
- The stream-derived editing grammar is learnable and mostly mechanical: base layout, facecam zoom on speech, friend cut-ins, label memes, subtitles, time cards, end card. That is close to what JokerClips does today, so the deep-study rules apply to the old main-channel compilations too.
- Before Dec 2023 the main channel also accepted 4-7 minute compilations (270-525 s); JokerClips later fixed 8:00. The length was a channel choice, not a property of the material.

### Gaps
- Sound effects and music choices cannot be seen in storyboards; only caption tags hint at them.
- Captions on 2021-23 uploads are sparse (old ASR), so those tables rely mostly on frames.

## 4. His live streams (Kaatclip's input): titles, schedule, length, structure, overlays, voices

### Takeaway
A Joker stream is a 3-6 hour evening show with a fixed running order: a 2-3 minute intro song over event footage, 5-35 minutes of full-screen-facecam "baat chit" (life updates, reading chat and Super Chats, people walking into the room), then 2-4 hours of BGMI with friends on voice, then often a second game (GTA RP most often; Valorant, Among Us, Meccha Chameleon, Rocket League...), and a short good-night chat. Talk is almost continuous: in 34 captioned streams (Jul-Oct 2026) 80-93% of seconds carry speech at 107-156 words a minute, and YouTube's captioner tagged laughter 14-100 times an hour. The layout has been stable since 2022: game full frame, Joker's facecam bottom-right, a "JOKER" mascot banner bottom-left with a live follower counter, sponsor badges; GTA RP moves the facecam to the top-left.

### Cited Findings
**Volume and length (streams tab, 1,310 items)**
- About 1,310 streams since 21 Oct 2020 (yearly table in section 1): median 4.4-6.3 h per year (longest 11.3 h, [F8LzticZItQ](https://www.youtube.com/watch?v=F8LzticZItQ)), median views rising from about 20K (2021) to 140K (2026). — [streams tab](https://www.youtube.com/@Jokerkihavelii/streams)
- 63 streams are members-only ("subscriber_only" in the listing); 57 of them are GTA RP ("MAYOR GULLU IN THE CITY | GTA V ROLEPLAY #Gameशुरू"). — [streams tab](https://www.youtube.com/@Jokerkihavelii/streams)
- Title conventions by era (counts over all 1,310 titles): "!Discord"/"!Insta"/"!Member" bot commands in 2021 (112 titles with !Discord); "!loco" in 2022-23 (17; he also streamed on Loco, whose watermark sits on the 2022 Among Us highlight [UcUCylFQ24I](https://www.youtube.com/watch?v=UcUCylFQ24I)); "ROAD TO 600K…2M" subscriber targets in 2023-26 (235 titles); "| JOKER IS LIVE" (48); "#Gameशुरू" campaign tag in 2025 (107); "#iQOO15/#iQOOZ11" sponsor tags in 2026; and the stacked format "X NOW | Y DONE" telling which game came first (DONE in 143 titles). — same listing

**Schedule (exact start times from YouTube's release timestamps)**
- 34 captioned streams 12 Jul-16 Oct 2026: start 19:56-23:21 IST, median 21:13; every weekday represented (Mon 6, Tue 6, Wed 6, Thu 5, Sat 5, Fri 3, Sun 3); length 2.5-9.4 h, median 4.5 h. — e.g. [G4W1WwLmIDo](https://www.youtube.com/watch?v=G4W1WwLmIDo) (Sun 11 Oct, 22:09, 3.4 h), [nu0fl7M3v8A](https://www.youtube.com/watch?v=nu0fl7M3v8A) (Mon 31 Aug, 19:56, 9.4 h charity)
- Earlier years started in the afternoon: [F8LzticZItQ](https://www.youtube.com/watch?v=F8LzticZItQ) began 15:35 IST on 7 Jan 2021 and ran 11.3 h; [h-gNAg2Llro](https://www.youtube.com/watch?v=h-gNAg2Llro) (20 Aug 2023) and [hW5XTW7tCh4](https://www.youtube.com/watch?v=hW5XTW7tCh4) (27 Apr 2024) began about 12:30. Across about 120 dated streams the median start was 21:24 IST in 2020-22, 14:18 in 2023, 13:18 in 2024, 20:12 in 2025 and 21:06 in 2026 (2023 streams began 10:29-13:52, 2024 streams 11:42-14:55, in the sample).
- A June 2025 profile says that after his son started school he streamed 1-7 PM instead of until 3-4 AM; the 2026 data show he is back to evening streams. — [GuruGamer, 13 Jun 2025](https://gurugamer.com/streamers/from-night-streams-to-nursery-rhymes-how-gulrez-khan-balances-gaming-and-fatherhood-24906)

**Running order (storyboard frames every 5 min, 10 streams 2021-2026)**

| Stream | Intro | Facecam chat | Main game | Second part | End |
|---|---|---|---|---|---|
| [F8LzticZItQ](https://www.youtube.com/watch?v=F8LzticZItQ) 7 Jan 2021, 11.3 h | "Stream starting" card | about 30 min, framed cam | GTA RP (HTRP, Shinde) ~10 h | n/a | facecam |
| [3xOrJq_DYGE](https://www.youtube.com/watch?v=3xOrJq_DYGE) Feb 2022, 6.2 h | n/a | 0:06-0:20 | BGMI 0:26-1:53 | GTA RP 2:00-5:50 | chat 5:53-6:00 |
| [h-gNAg2Llro](https://www.youtube.com/watch?v=h-gNAg2Llro) Aug 2023, 5.2 h | n/a | 0:00-0:15 | BGMI to the end | n/a | n/a |
| [hW5XTW7tCh4](https://www.youtube.com/watch?v=hW5XTW7tCh4) Apr 2024, 4.3 h | event clip | 0:02-0:10 | BGMI to the end (phone call on cam at 1:46) | n/a | n/a |
| [-THLgfTLTLs](https://www.youtube.com/watch?v=-THLgfTLTLs) May 2025, 3.2 h | crowd clip | 0:06-0:22 | BGMI 0:26-3:14 | n/a | n/a |
| [H8jtxF_KVZ4](https://www.youtube.com/watch?v=H8jtxF_KVZ4) 4 Aug 2026, 5.3 h | crowd clip | 0:03-0:20 (mixed with BGMI lobby) | BGMI 0:15-2:45 | GTA RP 2:50-5:19 | n/a |
| [2z0aPlOy9yg](https://www.youtube.com/watch?v=2z0aPlOy9yg) 8 Sep 2026, 3.4 h | intro | 0:03-0:08 | BGMI 0:10-0:33 | Valorant 0:40-3:00 | chat 3:02-3:15 |
| [G4W1WwLmIDo](https://www.youtube.com/watch?v=G4W1WwLmIDo) 11 Oct 2026, 3.4 h | street clip | 0:05-0:22 | BGMI incl. crate opening 0:25-2:25 | GTA RP 2:30-3:22 | good-night in GTA |
| [Hoie-YhTvBo](https://www.youtube.com/watch?v=Hoie-YhTvBo) 5 Oct 2026, 2.5 h | intro | 0:05-0:37 (son and a child walk in at 0:25) | browser game, then Rocket League 0:45-2:10 | n/a | chat 2:15-2:30 |
| [MAjDYoIKl1s](https://www.youtube.com/watch?v=MAjDYoIKl1s) 10 Oct 2026, 3.2 h | crowd clip | 0:05-0:27 | Among Us with S8UL 0:30-2:45 | n/a | chat 2:50-3:05 |

Sources: storyboard sheets built from each video's public storyboard images.
- The intro is a song ("chal mere saath… shaitanon ki ab buri hai nazar") playing for 2-3 minutes while Joker sings along, before "welcome back to another live stream, kya haal hai mere sheron… sirf teen cheezein: entertainment, entertainment, entertainment" ([G4W1WwLmIDo](https://www.youtube.com/watch?v=G4W1WwLmIDo) 0:00-2:30; [X_QBQqfO-9g](https://www.youtube.com/watch?v=X_QBQqfO-9g) 0:00-3:30, where he then unboxes new headphones on stream).
- The opening chat covers life news and plans: a friend's wedding reception, a fitness show diet, "kal uska vlog banayenge", fans mobbing him on the way to the gym; reading chat lines ("love from Bangladesh", "Joker bhai aaj kya kheloge?" "aaj main tumhare dil se khelne wala hoon"), shout-out requests; and introducing people in the room: "yeh hamare editor log hain" ([G4W1WwLmIDo](https://www.youtube.com/watch?v=G4W1WwLmIDo) 3:30-9:30).
- Endings: plans for the next stream, "good night, 9 baje uthunga, Mazin ko school chhodna hai… comments mein aao" ([G4W1WwLmIDo](https://www.youtube.com/watch?v=G4W1WwLmIDo) 3:20-3:23).
- Super Chats are read aloud and answered (e.g. a viewer asking help for a father's operation, a viewer saying his smile helps when sad), mostly in the chat and lobby gaps; his son on stream gets teased that he will earn "₹1000 Super Chats" ([aK1RteB3m8I](https://www.youtube.com/watch?v=aK1RteB3m8I) 0:27, 0:38, 0:49). Spoken "Super Chat" occurs 0-21 times per stream (half the raw count, since rolling captions repeat), 21 in the 9.4 h charity stream. — caption counts over 34 streams
- He talks about his editors on stream almost every time ("editor" spoken in 25 of 34 streams), from clip instructions to complaints. On 7 Sep 2026 he explained the vlog backlog: for four months "editor aata hai, poora footage download karta hai… intro banata hai, mere se voice-over leta hai, aur 20% kaam karne ke baad message aata hai: bro mere se nahi hoga"; a second and third editor did the same, a fourth was found with Willy ([X_QBQqfO-9g](https://www.youtube.com/watch?v=X_QBQqfO-9g) 15:40-16:20). On 22 Jul 2026 he floated a daily vlog on his "Gulrez Khan" channel and joked "editor bol raha hai mera PC phat raha hai, koi editor mera kaam nahi le raha" ([yYb7LVi5SM4](https://www.youtube.com/watch?v=yYb7LVi5SM4) 20:50-21:20).

**Speech and audio signals (Hindi auto-captions, 34 streams 12 Jul-16 Oct 2026)**
- Speech share 0.80-0.93 (median 0.865); 107-156 words a minute (median 123); captioner tags per hour (31 streams that carry tags): laughter [हंसी] median 26 (13.5-100), music 8.8, singing 4.9, screaming 4.4, bleeped swear 2.6. — computed from the caption files of e.g. [d2vLyeOUotc](https://www.youtube.com/watch?v=d2vLyeOUotc) (366 laughter tags in 3.7 h, the most), [BWnYw1Ds-sE](https://www.youtube.com/watch?v=BWnYw1Ds-sE) (no tags in its track)
- Laughter is not spread evenly: the top 10% of 10-minute bins hold a median 28% of a stream's laughter tags, and the last third of a stream holds more (median 37%) than the first third (26%).
- Laughter and talk depend on the segment (laughter tags per 10 minutes / words per minute; segment edges from the storyboards, 10-minute resolution):

| Stream | Chat (start) | BGMI | Second game | Chat (end) |
|---|---|---|---|---|
| [H8jtxF_KVZ4](https://www.youtube.com/watch?v=H8jtxF_KVZ4) | with BGMI: 3.2 / 111 | (same) | GTA RP 13.3 / 127 | n/a |
| [G4W1WwLmIDo](https://www.youtube.com/watch?v=G4W1WwLmIDo) | 2.5 / 145 | 2.2 / 112 | GTA RP 6.3 / 132 | n/a |
| [2z0aPlOy9yg](https://www.youtube.com/watch?v=2z0aPlOy9yg) | 0 / 145 | 7.3 / 122 | Valorant 7.5 / 144 | 5.0 / 137 |
| [MAjDYoIKl1s](https://www.youtube.com/watch?v=MAjDYoIKl1s) | 6.0 / 144 | n/a | Among Us 11.8 / 154 | 0.5 / 190 |
| [Hoie-YhTvBo](https://www.youtube.com/watch?v=Hoie-YhTvBo) | 6.2 / 144 | n/a | Rocket League 9.7 / 132 | 1.0 / 162 |

  BGMI has the lowest talk rate (111-122 wpm) and, in two of three streams, the lowest laughter; GTA RP and Among Us the highest laughter; the chat segments the fastest talk. — same caption files

**Layout and overlays (storyboards)**
- 2021: purple frame with a boxed facecam, GTA full frame ([F8LzticZItQ](https://www.youtube.com/watch?v=F8LzticZItQ)). 2022: purple "JOKER" banner bottom, facecam bottom-right ([3xOrJq_DYGE](https://www.youtube.com/watch?v=3xOrJq_DYGE), [D6Odowb1TPs](https://www.youtube.com/watch?v=D6Odowb1TPs)). 2023-26: "JOKER" mascot banner bottom-left with a live follower counter (573K in Aug 2023, 655K Jan 2024, 735K Apr 2024, 1.008M May 2025, 2.29M Sep 2026, 2.59M Oct 2026), facecam bottom-right, sponsor logos (Intel, ROG in 2023-24; iQOO in 2026), a UPI/QR donation code during charity streams.
- GTA RP: facecam top-left with counter, no banner ([G4W1WwLmIDo](https://www.youtube.com/watch?v=G4W1WwLmIDo) 2:30-3:22, [H8jtxF_KVZ4](https://www.youtube.com/watch?v=H8jtxF_KVZ4) 2:50-5:19). Valorant: facecam top-left ([2z0aPlOy9yg](https://www.youtube.com/watch?v=2z0aPlOy9yg)). Among Us: facecam bottom-left ([MAjDYoIKl1s](https://www.youtube.com/watch?v=MAjDYoIKl1s)).
- Chat segments are full-screen facecam (desk, mic, sometimes family or editors entering frame).
- IRL streams are handheld phone streams walking an event, 4 h at the Esports World Cup Paris ([lwvfYT4cm4Q](https://www.youtube.com/watch?v=lwvfYT4cm4Q), 605K views). Watch parties put his facecam beside the official broadcast ([zK9Fqa1XTzk](https://www.youtube.com/watch?v=zK9Fqa1XTzk), F1 Sim Racing, 2.7 h).

**Voices**
- BGMI: Joker plus 1-3 squad mates on voice call (S8UL friends such as Rega, Snax, Goldy, Mavi), plus random teammates and enemies in game voice; room voices (son, wife, editors); TTS or read-out donations. GTA RP adds proximity voice of many players. Spoken "call" appears 3-88 times per stream. — caption counts; voices inferred from content (auto-captions carry no speaker labels)

### Inferences
- The recording Kaatclip gets from a creator like Joker is not "a BGMI session": it is a variety show with segments. Step one for any tool is segmentation into intro / facecam chat / game A / game B / outro, which the layout makes easy (full-screen face vs. game frame vs. a different overlay position per game).
- A laughter-only ranker would over-pick GTA RP and party games (2-4x more laughter tags per minute than BGMI in two of the streams measured). If the product promise is BGMI highlights, rank within the BGMI segment, and offer other segments as separate products.
- The first 20-35 minutes of chat is real material (stories, roasts of people in the room, Super Chat answers) that JokerClips rarely uses; it suits talking-head Shorts.

### Gaps
- Exact start times exist only for the 34 dated 2026 streams and a small sample of older ones; the per-month counts before Dec 2025 are interpolated from the listing order.
- Speaker identity, the number of simultaneous voices and whether friends' voices are on the same audio track cannot be measured from captions.
- Laughter tags depend on YouTube's captioner (three streams have none at all), so they are a proxy, not a measurement of audio laughter.

## 5. Shorts in depth

### Takeaway
Shorts went from GTA RP character one-liners (2021) to friend and family skits (2023-25) to a daily-routine mini-vlog machine in 2026 (77 of 112 Shorts so far this year; 23 in March alone during "Ramadan Routine"). The routine series is where the views are (median 2.8M, up to 52M); it is shot on a phone and runs 60-154 s. Stream-cut gaming Shorts are a small minority (35 of 273 titles, 14-60 s, median 304K views) with a stacked facecam-plus-gameplay layout, and their number has fallen to 3 in 2026.

### Cited Findings
**Types (273 Shorts classified by title; durations and dates from a sample of 150 (137 sampled plus 13 fetched individually) fetched with full metadata)**

| Type (by title) | n | Median length (dated) | Median views | Max |
|---|---|---|---|---|
| Routine / mini-vlog series (Ramadan Routine, My Life in Paris/Japan, Daily Routine, ROAD TO ICN, N Days to Go) | 81 | 90 s (11-154) | 2.8M | 52M |
| Skit / friends / family moments | 111 | 22 s (8-88) | 733K | 21M |
| BGMI and gaming clips | 35 | 34 s (14-60) | 304K | 5.4M |
| GTA RP Shinde one-liners (2021-22) | 17 | 26 s (22-58) | 81K | 193K |
| Cricket / celebrity | 13 | 24 s (11-101) | 1.5M | 25M |
| Fitness / transformation | 12 | 19 s (12-97) | 1.3M | 8.5M |
| Sponsored (#Ad, phone, merch) | 3 | 42 s | 558K | 591K |
| Friends on call from a stream (Goldy) | 1 | 40 s | 5.4M | 5.4M |

| Year | Shorts | Main types | Median views | Median length (dated) |
|---|---|---|---|---|
| 2021 | 25 | GTA RP 14, skits 8, gaming 3 | 83K | 24 s |
| 2022 | 9 | skits 4, GTA RP 3, gaming 1 | 558K | 22 s |
| 2023 | 24 | skits 15, gaming 6 | 555K | 21 s |
| 2024 | 70 | skits 48, gaming 16 | 476K | 26 s |
| 2025 | 33 | skits 15, cricket/celebrity 8, gaming 6 | 623K | 25 s |
| 2026 (to 12 Nov) | 112 | routine series 77, skits 21, fitness 8, gaming 3 | 2.35M | 72 s (36 of 61 dated are over 60 s) |

— [Shorts tab](https://www.youtube.com/@Jokerkihavelii/shorts); years interpolated by listing order between 150 dated Shorts

**Layouts and devices by type (storyboard frames every 1-2 s)**
- *Stream-cut gaming Short* (stacked): facecam on top (about 25-45% of the height) and gameplay below, or gameplay on top and facecam below; the stream's JOKER banner and follower counter are often kept at the bottom; a short caption chip over the gameplay ("1v4 Clutch 😡", "AKM + RED DOT 🔥", "Submarine Buggati 😱🤣"); emoji stickers (💀, 🥶) at the kill; for the reaction the facecam grows to full height ([LCZiW8i8zjk](https://www.youtube.com/shorts/LCZiW8i8zjk) 0:21-0:47, 53 s, 398K) and a closing card ("Share karo aise dosto ko", "SUBSCRIBE NOW"). Examples: [CVqRiZ-wwNw](https://www.youtube.com/shorts/CVqRiZ-wwNw) (27 s, counter 900,115), [5CZYCQybc20](https://www.youtube.com/shorts/5CZYCQybc20) (26 s, Jul 2023), [qUFtM6TGeLE](https://www.youtube.com/shorts/qUFtM6TGeLE) (20 s, gameplay over facecam, skull sticker), [UWFVd8F1Tj4](https://www.youtube.com/shorts/UWFVd8F1Tj4) (30 s, three different streams stitched, shirt changes at 0:11 and 0:25), [HgVaBHrngzA](https://www.youtube.com/shorts/HgVaBHrngzA) (24 s).
- *Friends-on-call Short*: two webcams stacked over gameplay with a title chip, ending on both webcams laughing ([wCzImt3k8hE](https://www.youtube.com/shorts/wCzImt3k8hE) "We Pranked @MAVIOP", 42 s, 5.5M, 23 Jun 2023), or two webcams with no gameplay ([9gy3caHoOMs](https://www.youtube.com/shorts/9gy3caHoOMs) "Goldy Dada Gussa Ho Gaye", 40 s, 5.47M, earlier note).
- *Lifestyle routine / mini-vlog series*: native vertical phone video, 1-2 s shots through a day, 60-91 s ([liTFXMbHsrg](https://www.youtube.com/shorts/liTFXMbHsrg) 79 s, 52.4M; [SH5F-q_25Zs](https://www.youtube.com/shorts/SH5F-q_25Zs) 68 s, 24.5M; [yYVP14lEiEU](https://www.youtube.com/shorts/yYVP14lEiEU) 77 s, 14.1M; [jQj5xQD1jG0](https://www.youtube.com/shorts/jQj5xQD1jG0) 61 s, 10.5M; [Q-G7UT9Gwok](https://www.youtube.com/shorts/Q-G7UT9Gwok) 91 s, 8.1M).
- *Skit / family moment*: staged vertical scenes of 11-46 s with a fixed caption or sticker ([s_zeXPa8RIM](https://www.youtube.com/shorts/s_zeXPa8RIM) 27 s, 5.97M; [nTbYY4kgYfI](https://www.youtube.com/shorts/nTbYY4kgYfI) 23 s, 2.17M; [9r-mE7CHi80](https://www.youtube.com/shorts/9r-mE7CHi80) "Mazin Shocked", 46 s, 11.7M; [zj28bLjgSHs](https://www.youtube.com/shorts/zj28bLjgSHs) 15 s, 7.6M; [KBN80HkfGSM](https://www.youtube.com/shorts/KBN80HkfGSM) with Farah Khan, 11 s, 25.1M).
- *IRL event moment*: [i6GGwJZroOY](https://www.youtube.com/shorts/i6GGwJZroOY) "Aura in EWC 💀" (43 s, 835K, 23 Aug 2026), vertical footage at the Esports World Cup with a top caption and emoji; the shirt and venue match his 17 Aug IRL stream ([lwvfYT4cm4Q](https://www.youtube.com/watch?v=lwvfYT4cm4Q)), so it is probably cut from that stream or shot the same day (inference). [Iu0h5u9hvLE](https://www.youtube.com/shorts/Iu0h5u9hvLE) "Hacker 💀" (17 s, 373K) is a bowling-alley clip despite the gaming word.
- *GTA RP Shinde Shorts* (2021-22): character one-liners ("Shinde Sigma Rule…") at 41-193K views ([qdCQqwabpzM](https://www.youtube.com/shorts/qdCQqwabpzM), 42 s, 114K).
- Descriptions are empty or 2-4 hashtags; no tags; two gaming Shorts are members-only ([T30nVoA6xrU](https://www.youtube.com/shorts/T30nVoA6xrU), 45 s).

**Cadence and timing**
- - 1-6 Shorts a month in 2025; 7-23 a month in 2026 (23 in March during the Ramadan series, 15 in October with the Japan series). Series run daily during a trip or festival ("Day 1… Day 5", "Part 3… Part 15"). Published 09:00-22:00 IST, mostly 14:00-17:00. Descriptions are empty or 2-4 hashtags; no tags. — Shorts metadata

### Inferences
- - The Shorts that drive this creator's growth are phone-shot daily-life series; Kaatclip cannot make them. Kaatclip's Shorts compete with his gaming Shorts (a few a month in 2024, 0.2-0.6M views typical, 5.4M for a friends prank).
- The gaming Shorts that did best had a person-to-person payoff (a prank on Mavi, Goldy getting angry), not a clean kill; kill clips ("AKM GOD", "1v4 With Knife") sit at 0.2-0.4M.
- The stacked layout (facecam on one half, gameplay on the other, a 2-4 word caption chip, an emoji sticker at the payoff, the facecam enlarged for the reaction, a closing card) is easy to template from a stream recording.

### Gaps
- Durations and exact dates were fetched for a sample only; type counts use titles, which can mislead (a "Hacker" title on an IRL clip).
- Whether skit Shorts are scripted or caught on the vlog camera cannot be told from frames.

## 6. Titles, thumbnails, descriptions, upload timing and what performs

### Takeaway
On the main channel the camera-shot formats win: vlogs with famous friends or life events (weddings, a house, a car, a body transformation) and "I became X for 24 hours" experiments reach 1.5-3.1M, while stream-cut gaming videos peaked at 0.6-1.7M in 2022 and their medians were far lower (32K-332K by type). On Shorts the routine mini-vlog series (Ramadan, London, Paris, Japan) run at a median 2.8M views, about nine times the gaming Shorts (304K). Titles are short hooks with one emoji; thumbnails are cut-out faces with one big phrase; descriptions are minimal; long videos go up at 10:00-12:59 IST, Shorts through the afternoon and evening.

### Cited Findings
**Titles by type (examples from the listings)**
- Vlogs and IRL: English or Hinglish sentence hooks with an emoji: "I Became BATMAN For 24 Hrs In MUMBAI 🤯", "Working 24 HOURS as a ZOMATO RIDER", "Mr. Faisu Ki Shaadi ❤️ | The Wedding Vlog", "I BOUGHT MY FIRST HOUSE | Eid Special"; 2023-24 vlogs often end "- VLOG" ("RAMADAN IFTAR IN S8UL GAMING HOUSE 😇 | Gully Cricket"). — [videos tab](https://www.youtube.com/@Jokerkihavelii/videos)
- Stream-based gaming uploads: names of co-stars and a caps conflict word, "*FUNNY*" or "FUNNIEST", and 😂🤣: "MOST FUNNIEST BGMI SQUAD IN INDIA🤣 FT. @PAYALGAMING", "KUCH KUCH HOTA HAI IN AMONG US 🤣 FT. @S8ULGG @SnaxGaming", "Goldy Bhai Got My *BGMI ID BAN* After This ? 🤣", money in the title for challenges ("I Won ₹3,40,000 Challenge in BGMI w/ @SnaxGaming"). 2021-22 titles carried "*epic🤣*" and "#jokerkihaveli".
- Streams: short caps hooks plus the game order and a target ("PAGAL KAR DUNGA", "GTA V RP NOW | BGMI DONE", "5 CHICKEN CHALLENGE IN BGMI | ROAD TO 1.6M #iQOO #iQOO15R"). — [streams tab](https://www.youtube.com/@Jokerkihavelii/streams)
- Shorts: 2-4 words plus an emoji ("Bach Gaya Aaj 💀😂", "Personal Damage 😂", "Hawa Mein 1v2💀"); series titles with a day counter ("Ramadan Routine Part 4 🌙😆", "My Life in Japan 🇯🇵 Day 4", "ROAD TO ICN 🥇 Day 2"); 2023-24 Shorts appended "#shorts #jokerkihaveli". — [Shorts tab](https://www.youtube.com/@Jokerkihavelii/shorts)

**Thumbnails (12 inspected)**
- Vlogs: a huge pale "VLOG" word behind posed cut-outs of the people, circle insets of other moments, a red tag ("GOLDY BHAI NEW HOUSE") — [5nMlWDfU8co](https://i.ytimg.com/vi/5nMlWDfU8co/hqdefault.jpg), [UJtX9VpZPUI](https://i.ytimg.com/vi/UJtX9VpZPUI/hqdefault.jpg). Social experiments: Joker in costume or uniform with props and a "24 HOUR" badge or "1 MILLION+ VIEWS" chip — [CTVXMQ_3YUY](https://i.ytimg.com/vi/CTVXMQ_3YUY/hqdefault.jpg), [FeZs2fIkals](https://i.ytimg.com/vi/FeZs2fIkals/hqdefault.jpg).
- Stream-based gaming: 2-4 face cut-outs with exaggerated expressions, one big quote in yellow/white ("MERI GAAF MAI MUNH DAALDO", "TERA ID MEIN BAN KARWA DUNGA", "WHY ANJALI?"), emoji, red arrows, an in-game screenshot (a ban warning), money chips ("SOLO 22 FINISHES", "3.4 LAKH", a Super-Chat-style card "55 finishes for Rs. 3,40,000") — [VOvG30dwlq8](https://i.ytimg.com/vi/VOvG30dwlq8/hqdefault.jpg), [5szLSGgb5bE](https://i.ytimg.com/vi/5szLSGgb5bE/hqdefault.jpg), [WBq__Fc-pqM](https://i.ytimg.com/vi/WBq__Fc-pqM/hqdefault.jpg), [UcUCylFQ24I](https://i.ytimg.com/vi/UcUCylFQ24I/hqdefault.jpg).

**Descriptions and metadata**
- 2020-21: a long template ("Welcome to my channel… For Donations: Paytm…", "My Second Channel: GulrezKhan"). 2022: one funny line plus "THANK YOU SO MUCH FOR WATCHING LIKE, SHARE, COMMENT AND SUBSCRIBE", Discord and Instagram links. 2023-24: one line, the squad @-tags ("Squad - @SnaxGaming @8bitGoldygg @KaashPlays"), Instagram, "Business enquiry jokerkihaveli@8bitcreatives.in", "Second Channel @jokerclipss". 2025-26 vlogs: a 2-4 sentence story summary plus sponsor lines (e.g. Samsung Galaxy Z Fold7 hashtags in [UJtX9VpZPUI](https://www.youtube.com/watch?v=UJtX9VpZPUI)). Streams: a fixed block of social handles and "Haste Raho Hasate Raho". Shorts: empty or 2-4 hashtags ("#vlog #jokerkihaveli #cricket #minivlog"). — descriptions of the sampled videos
- Sponsors seen: ROG and Intel (2023-24 stream overlays and descriptions), Boult earbuds ([CFt9BX7llGY](https://www.youtube.com/watch?v=CFt9BX7llGY)), SoStronk, a real-money BGMI tournament app ("Play BGMI, Win ₹50,000 Daily", [gnl2JShBGM8](https://www.youtube.com/watch?v=gnl2JShBGM8)), World of Tanks ([zGC5FiC8Dwg](https://www.youtube.com/watch?v=zGC5FiC8Dwg)), iQOO (2026 stream titles), Samsung (2025 vlog).
- Chapters: none on any sampled upload except the documentary (8 chapters). Categories: "Gaming" for gaming and most Shorts, "Entertainment" for many vlogs. Tags: 6-15 keyword tags on long videos, none on Shorts.

**Upload timing**
- - Long videos 2023-26: 80% were published between 10:00 and 12:59 IST (median 11:45; 129 of 277 in the 11:00 hour), spread over all weekdays (Fri 47 to Sat 35). In 2020-22 the stream-cut videos went up later (median 14:36). — upload timestamps from metadata
- Shorts (150 dated): 09:00-22:00 IST, 66 of 137 timestamps between 14:00 and 17:59.
- Streams in 2026 start in the evening (median 21:06); see section 4.

**What performs**
- | Format | Median views | Top examples |
|---|---|---|
| Social experiment / 24 h (n=18) | 678K | "I Became Wukong & Pranked S8UL Creators" 2.3M; "I Became BATMAN For 24 Hrs" 1.8M; "Living As a BEGGAR In MUMBAI" 1.5M |
| BGMI challenge / collab, 2024-25 (n=9) | 546K | S8UL BGMI Emote Challenge 696K; I Won ₹3,40,000 673K |
| Vlog / IRL (n=271) | 339K | "A Day w/ Goldy Bhai & Snax in Delhi" 3.1M; "Mr. Faisu Ki Shaadi" 2.4M; "My 100 Day Body Transformation" 2.3M |
| IRL challenge / game (n=54) | 332K | "Calling them with their Real Name" 1.8M; "Guess The CITY By ACTION" 1.7M |
| Among Us / other game, 2020-24 (n=21) | 332K | "This is How you Win JESTER R0LE" 705K |
| Marfa raids, 2020-22 (n=21) | 277K | Marfa with Krutika 1.49M; with Godlike boys 1.2M |
| Reactions, 2021-22 (n=14) | 258K | "Joker Reacts on old Regaltos" 1.7M |
| BGMI stream compilations, 2021-23 (n=21) | 142K | "FUNNIEST BGMI GAMEPLAY WITH PAYAL, WILLY" 383K |
| GTA RP funny moments, 2020-22 (n=35) | 32K | "Shinde & Shiva Best Funny moments" 172K |
| Shorts: routine series (n=81) | 2.8M | Ramadan Routine Ft IND vs ENG 52M |
| Shorts: skits, friends, family (n=111) | 733K | "Her Smile Was Priceless" 21M |
| Shorts: cricket / celebrity (n=13) | 1.5M | with Farah Khan 25M |
| Shorts: gaming (n=35) | 304K | "We Pranked @MAVIOP" 5.5M |

— views on 12 Nov 2026 from the listings; older uploads had more time to collect views. The like-to-view ratio is higher on stream-cut uploads (median 12.1%) than on shot uploads (10.3%), and higher on gaming Shorts (8.2%) than on routine Shorts (4.1%).

### Inferences
- - His audience grew on stream comedy (GTA RP, Marfa, Among Us with S8UL), but reach now comes from the person, his family and his friends off-screen. Stream-gameplay content is loyal (higher like ratios) but small; for a creator like this, Kaatclip's value is in the clips channel and gaming Shorts, not the main channel.
- On the main channel a BGMI upload has to carry a hook bigger than a session (money, a feud, a gimmick, an IRL twist); routine sessions belong on the clips channel.
- Naming famous friends in titles and thumbnails is the strongest single lever across formats (Goldy, Snax, Faisu, Farah Khan, S8UL).

### Gaps
- No retention, CTR or revenue data; views are rounded public counts on 12 Nov 2026, and older videos have had longer to collect views.
- Thumbnail findings rest on 12 thumbnails here plus 5 in the earlier note.

## 7. What this means for an automatic tool (Kaatclip)

### Takeaway
From one of Joker's stream recordings Kaatclip can realistically make five of his content types: (1) the 8-minute BGMI comedy session highlight (JokerClips' format), (2) a goal-driven "challenge" highlight (main-channel format, 8-10 min, first attempt / next day / success), (3) crate-opening highlights, (4) stacked-layout gaming Shorts of 15-45 s, and (5) talking-head Shorts from the opening chat. The same audio-first pipeline could cover his GTA RP, Among Us and party-game segments, which carry more laughter than BGMI, but BGMI-specific event detectors do not transfer. Everything that made the main channel big since 2023 — vlogs, travel, family, IRL challenges, social experiments, the documentary, skits and lifestyle Shorts — is shot with cameras and is out of reach of a stream-recording tool.

### Cited Findings (measured inputs a tool must handle)
- Input shape: 3-6 h (median 4.5 h) variety stream; 2-3 min intro song; 5-35 min facecam chat; 2-4 h BGMI; optional second game; short good-night chat. — section 4 table
- Speech is continuous (80-93% of seconds, 107-156 wpm in streams; 77-94% and 88-179 wpm in finished JokerClips highlights). — section 4; deep study section 2
- Laughter tags: median 26 an hour in streams; 2-4x denser in GTA RP and Among Us than in BGMI in the streams measured; concentrated (the top 10% of 10-minute bins hold a median 28% of a stream's laughs). — section 4
- Explicit flags: "editor", "clip", "highlight" are spoken in most streams (clip/highlight 0-16 times per stream, editor in 25 of 34), and he sometimes names the destination ("ye highlight main channel pe jaayegi"). — section 4, [WBq__Fc-pqM](https://www.youtube.com/watch?v=WBq__Fc-pqM) 8:51
- Visual anchors in the layout: full-screen facecam = chat segment; JOKER banner + follower counter = BGMI; facecam top-left = GTA RP or Valorant; "YOU GOT" = crate result; scoreboard / "#N You made the Top 10" / VICTORY = match end; follower counter only rises within a stream, so it orders footage across streams. — section 4; deep study section 3
- What the human editor actually takes from a stream: the first 30-120 min of the BGMI part, 15-30 units of 7-45 s, chronological, compiled with a second stream behind "THE NEXT DAY" when one is not enough. — deep study section 3

### Inferences
**What Kaatclip can make, and the signals each needs**

| Output | Source segment | Needed signals | Feasibility |
|---|---|---|---|
| BGMI comedy session highlight, 8:00-8:15 | BGMI part, first ~2 h; second stream if short | Speech density, laughter (audio classifier, not only caption tags), overlapping voices, Hinglish roast/blame cues, knock/death/result screens, explicit "clip/highlight/editor" flags | High; this is the JokerClips recipe, already specified in the deep study |
| Challenge highlight, 8-10 min | A challenge stream (title has CHALLENGE / ₹ / N CHICKEN / N FINISHES) | OCR of kill counter, rank and result screens; transcript for the terms ("55 kill + chicken = 3 lakh"); attempt boundaries | Medium; needs a story template: terms → attempt 1 → "THE NEXT DAY" → final attempt → result and celebration |
| Crate opening highlight | Crate segment (title "UC CRATE OPENING") | "YOU GOT" / reveal screens by vision, loudness and laughter after reveals, UC spend mentioned | Medium-high; reveal screens are distinctive |
| Gaming Short 15-45 s | Any BGMI moment | Same moment scoring; stacked crop: facecam on one half (top or bottom), gameplay on the other, banner/counter optional, facecam enlarged for the reaction; a 2-4 word top caption with emoji ("1v4 Clutch 😡", "Submarine Buggati 😱🤣") | High; matches [CVqRiZ-wwNw](https://www.youtube.com/shorts/CVqRiZ-wwNw), [qUFtM6TGeLE](https://www.youtube.com/shorts/qUFtM6TGeLE), [wCzImt3k8hE](https://www.youtube.com/shorts/wCzImt3k8hE) |
| Talking-head / chat Short | Opening chat, Super Chat replies, people entering the room | Laughter, story completeness (an LLM pass over the transcript), face-only frame | Medium; no game events to anchor, so it rests on transcript understanding |
| Other-game highlight (GTA RP, Among Us, Valorant, party games) | Second-game segment | Audio-only ranking works; game events differ per title | Possible as "audio-only mode"; BGMI detectors do not apply |
| Watch-party highlight | Watch-party streams | Reactions over a third-party broadcast | Low; the broadcast is someone else's footage (copyright risk, inference) |

**Out of reach and why**
- Vlogs, travel, weddings, family, events: no stream footage exists; they come from hours of camera footage and need a story and voice-over (his editors even take a voice-over from him, [X_QBQqfO-9g](https://www.youtube.com/watch?v=X_QBQqfO-9g) 15:45).
- IRL challenges and social experiments (Zomato rider, Batman for 24 h, Guess the city): planned shoots with multiple cameras and graphics.
- Lifestyle and skit Shorts, which are the channel's biggest view-getters (tens of millions): shot natively vertical on a phone, scripted or montage-edited.
- The documentary: interviews and archive.
- IRL streams are stream recordings, but handheld, with no game events; only audio and face signals would apply.

**Product notes**
- Segment first, then rank inside segments; never rank a whole 5 h stream as one pool, or GTA RP and party games will crowd out BGMI.
- Treat spoken flags ("clip kaat", "highlight", "editor", "main channel") as markers; Joker uses them as instructions to his editors.
- Offer a destination choice per output (main channel vs. clips channel vs. Shorts), because this creator splits by channel: challenge and milestone gameplay to the main channel, routine sessions to JokerClips, single moments to Shorts.

### Gaps
- No audio was analysed; laughter and voice-overlap figures come from YouTube's caption tags, which are absent on some tracks.
- The challenge-highlight template rests on one example in depth ([WBq__Fc-pqM](https://www.youtube.com/watch?v=WBq__Fc-pqM)) plus stream titles.
