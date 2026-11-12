# JokerClips (@jokerclipss): A-to-Z study of every content type, its source, how it is edited and how it is uploaded

**Method (12 Nov 2026).** Public YouTube data only, read with yt-dlp. No video or audio was downloaded.

- **Metadata:** full metadata (exact upload time, views, likes, tags, description, "most replayed" heatmap, maximum resolution) for **all 811 uploads**: 659 videos and 152 Shorts. 810 are dated; one is age-restricted. The channel has **no playlists tab** and no streams tab.
- **Classification:**
  - Every upload was classified with title and length rules plus 63 manual corrections. About 90 classifications were checked against storyboard frames.
  - Expect about ±10% error between neighbouring types, mainly "short stream moment" against "stream-talk moment".
- **Source mapping:** 13 new highlights were mapped to their source by aligning Hindi auto-captions word by word (4-word sequences). They are added to the 6 mapped in `joker_deep.md`.
  - Captions were fetched for 30 more source streams and vlogs: IRL, watch parties, Meccha Chameleon, Chained Together, Carry The Glass, crate openings and a 2M-celebration stream.
- **Storyboards:** 58 new uploads were read from storyboard frames, 2022-2026, every 1-10 s. Of these, 23 are Shorts read as contact sheets.
- **Raw data:** `C:\Users\soura\AppData\Local\Temp\claude\21027423ba80eb72\c7886632-c6c6-4a95-81c6-c6cbac2a769e\scratchpad\a2z\jokerclips\`, which holds:
  - `data/inventory.json` (every item with type, date, views);
  - `data/analysis2.txt`;
  - `data/seg_*.txt` (segment tables);
  - `data/sb/` (storyboards);
  - the scripts in `tools/`.

This note builds on `research_notes/BGMI highlight channels deep study/joker_deep.md`. Facts already there (the 8:00-8:10 rule, the six earlier mappings, the editing devices of 2026 sessions) are only referenced, not repeated.

"Inference" marks anything not directly measured. Views are public counts on 12 Nov 2026, so older videos have had more time to collect views.

## 1. Full inventory: what JokerClips has posted, by type, from 2021 to 2026

### Takeaway
JokerClips went through three distinct lives:

1. **Nov 2021 to Mar 2022: a Shorts-only reel channel.** 28 Shorts: GTA RP character skits ("Shinde", "Tiwari Seth"), trending-reel parodies and fashion reels.
2. **Aug 2022 to Dec 2023: a high-volume clip channel.** Up to 36 uploads a month of 30 s to 4 min single moments from Joker's streams: banter, reactions, GTA RP SoulCity and BGMI clutches, plus 2-15 Shorts a month.
3. **From mid-2023, and fully from 2024: an 8-minute highlight channel.** Funny BGMI sessions, challenges, crate openings and watch-party reactions, with almost no Shorts.

Output fell from 375 uploads in 2023 to 64 in 2026. There has been no upload since 5 Oct 2026, more than 5 weeks before this study. The long-video median view count rose from 44-54K (2023) to 130-220K (2024-2026). The only very large numbers on the channel are Shorts (up to 8.6M) and three one-off reaction or raid videos (1.0-1.5M).

### Cited Findings
**Channel facts**
- Joined **22 Nov 2021**; 280K subscribers, 191.3M total views and 811 uploads on 10 Nov 2026 — [vidIQ JokerClips stats](https://vidiq.com/youtube-stats/channel/UCwCniisl6QBsZzzcRi-0EFg)
- Views gained per month (vidIQ): 7-8M a month in Aug-Oct 2025, then 1.9-5.7M a month in Jan-Oct 2026 (Oct 2026: +1.9M). Subscribers gained: +11-13K a month in Dec 2023 to Feb 2024, against +1K a month in Sep-Oct 2026. — [vidIQ](https://vidiq.com/youtube-stats/channel/UCwCniisl6QBsZzzcRi-0EFg)
- The first upload is a Short, "Trend with Fukra Insaan" (22 Nov 2021, [bdoa8N9O0yU](https://www.youtube.com/shorts/bdoa8N9O0yU)). The first long video is from 27 Aug 2022. The last Short is from 14 Feb 2026 ([tb7vUafHeso](https://www.youtube.com/shorts/tb7vUafHeso)). The last upload is from 5 Oct 2026 ([TZCVFWl7NtM](https://www.youtube.com/watch?v=TZCVFWl7NtM)). Uploads stopped completely from late Mar 2022 to 19 Aug 2022. — [videos tab](https://www.youtube.com/@jokerclipss/videos), [Shorts tab](https://www.youtube.com/@jokerclipss/shorts)

**All 811 uploads by content type** (dur = length in seconds as p25/median/p75; views as p25/median/p75 and max; like% is the median of likes ÷ views)

| Type (what it is) | n | Dur s (p25/med/p75) | Views (p25/med/p75; max) | Like% | Active |
|---|---|---|---|---|---|
| **BGMI funny session** (squad banter highlight, 1-2 streams) | 159 | 481/485/501 | 131K/185K/258K; 1.06M | 7.2 | Jun 2023 to Sep 2026 |
| **Short BGMI or stream moment** (one moment, under 3-4 min) | 133 | 49/79/132 | 34K/52K/96K; 697K | 10.3 | Sep 2022 to Aug 2026 (111 in 2023) |
| **Stream-talk, call and IRL moment** (stories, replies, raids, celebrations, video calls, IRL streams, vlog re-cuts) | 99 | 58/97/164 | 27K/45K/85K; 1.42M | 10.6 | Aug 2022 to Sep 2026 |
| **Reaction to creators or media on stream** (vlogs, room tours, songs, shows, trailers) | 89 | 58/132/364 | 43K/60K/168K; 1.48M | 9.2 | Sep 2022 to Mar 2026 |
| **BGMI challenge or "vs"** (TDM 1v1, 2v2 or 4v4, money challenges, Wow-mode duels) | 50 | 391/486/518 | 105K/166K/247K; 722K | 7.3 | May 2023 to Sep 2026 |
| **Esports watch-party, casting and commentary** | 48 | 152/491/704 | 38K/75K/142K; 593K | 7.3 | Sep 2022 to Aug 2026 |
| **BGMI crate opening** | 28 | 254/481/502 | 92K/118K/154K; 222K | 8.6 | Jun 2023 to Oct 2026 |
| **GTA V RP (SoulCity) clips** ("Gullu Dada", "Shinde", "Dom") | 24 | 66/128/187 | 24K/39K/53K; 99K | 10.6 | Aug 2022 to Sep 2023 |
| **Reaction to pro or international players' videos** (DOK, Falak, Burst) | 12 | 217/263/487 | 130K/211K/438K; 933K | 4.6 | Jun 2023 to Aug 2025 |
| **Party and indie games** (Meccha Chameleon, Chained Together, Carry The Glass, Unfair Mario, Akinator) | 10 | 102/492/536 | 73K/144K/277K; 510K | 5.7 | Sep 2022 to Jul 2026 |
| Among Us | 4 | 98 (median) | 51K (median) | 12.2 | 2022-23 |
| Promo and other (music video "NOOB VOL 1", a "Genie" trailer, a Black Myth Wukong guide) | 3 | n/a | 25K-885K | 14.4 | 2023-24 |
| **Shorts: IRL skits, memes, "relatable" and trend reels** | 48 | 13/17/26 | 59K/123K/470K; 5.15M | 9.7 | Nov 2021 to Oct 2023 |
| **Shorts: stream moments** (stacked facecam and game, or calls) | 35 | 13/20/27 | 81K/149K/420K; 8.63M | 8.8 | Jan 2022 to Oct 2025 |
| **Shorts: BGMI gameplay moments** (clutch, spray, snipe) | 25 | 14/17/26 | 47K/70K/110K; 253K | 8.9 | Dec 2021 to Jan 2024 |
| **Shorts: IRL friend-group clips and vlog excerpts** | 19 | 14/20/33 | 168K/531K/1.68M; 7.02M | 4.1 | Dec 2021 to Feb 2026 |
| **Shorts: GTA RP character skits** | 15 | 15/25/38 | 12K/21K/39K; 245K | 10.8 | Nov 2021 to Sep 2023 |
| Shorts: cricket and sports | 6 | 17.5 (median) | 1.66M (median); 5.26M | 4.9 | Apr 2023 to Mar 2024 |
| Shorts: Valorant | 4 | 25.5 (median) | 34K (median) | 8.8 | 2022-23 |

— classification of the [videos](https://www.youtube.com/@jokerclipss/videos) and [Shorts](https://www.youtube.com/@jokerclipss/shorts) tabs (`data/inventory.json`)

**Uploads per half-year by type** (dated items)

| Type | 21H2 | 22H1 | 22H2 | 23H1 | 23H2 | 24H1 | 24H2 | 25H1 | 25H2 | 26H1 | 26H2 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BGMI funny session | 0 | 0 | 0 | 1 | 7 | 35 | 24 | 29 | 34 | 24 | 5 |
| Short BGMI or stream moment | 0 | 0 | 3 | 70 | 41 | 13 | 4 | 0 | 1 | 0 | 1 |
| Stream-talk, call and IRL | 0 | 0 | 25 | 33 | 21 | 2 | 5 | 5 | 0 | 2 | 6 |
| Reaction to creators or media | 0 | 0 | 7 | 46 | 13 | 3 | 8 | 6 | 2 | 4 | 0 |
| Challenge or vs | 0 | 0 | 0 | 1 | 7 | 11 | 11 | 8 | 7 | 4 | 1 |
| Esports watch party | 0 | 0 | 2 | 10 | 10 | 0 | 3 | 8 | 8 | 4 | 3 |
| Crate opening | 0 | 0 | 0 | 1 | 8 | 3 | 2 | 5 | 4 | 2 | 2 |
| GTA RP (long) | 0 | 0 | 4 | 19 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| Pro-player reaction | 0 | 0 | 0 | 2 | 4 | 0 | 4 | 1 | 1 | 0 | 0 |
| Party and indie games | 0 | 0 | 1 | 2 | 0 | 0 | 0 | 0 | 2 | 2 | 3 |
| All Shorts | 19 | 9 | 30 | 46 | 30 | 3 | 0 | 2 | 12 | 1 | 0 |
| **Total** | 19 | 9 | 75 | 233 | 142 | 70 | 63 | 64 | 71 | 43 | 21 |

  - Monthly peak: 36 videos and 4 Shorts in Jun 2023.
  - 2026 by month (videos/Shorts): Jan 8/0, Feb 6/1, Mar 5/0, Apr 7/0, May 7/0, Jun 9/0, Jul 5/0, Aug 9/0, Sep 6/0, Oct 1/0.
  - Source: same inventory.
- **Length of long videos per half-year:**
  - Median length was 82 s in 2022H2 and 70 s in 2023H1. It rose to 134 s in 2023H2, then 480 s in 2024H1, and has stayed at 485-493 s since.
  - Share of videos at 480-520 s: 0% (2022), 10% (2023H2), 40% (2024H1), 60% (2025), 74% (2026H1).
  - Share under 180 s: 91% (2022H2), 88% (2023H1), 62% (2023H2), 7% (2024H1), 0-3% (2025-26H1).
  - The first 480-489 s video is "Joker Reaction On Scout Journey" (23 May 2023, [ZWBO_XC8-ms](https://www.youtube.com/watch?v=ZWBO_XC8-ms)). The first session-type highlight is from 22 Jun 2023.
  - Source: same inventory.
- **Median views by half-year:**
  - Long videos: 27K (2022H2), 54K (2023H1), 44K (2023H2), 221K (2024H1), 136K (2024H2), 152K (2025H1), 197K (2025H2), 130K (2026H1), 140K (2026H2).
  - BGMI funny sessions only: 532K (2023H2, n=7), 235K, 141K, 168K, 206K, 132K (2026H1), 196K (2026H2, n=5).
  - Median like rate of long videos: 13.0% (2022H2), 10.2% (2023H1), 8.1-8.5% (2024), 6.7-6.9% (2025), 7.0% (2026H1), 4.0% (2026H2).
  - Source: same inventory.
- **Yearly totals:**

| Year | Uploads | Videos | Shorts | Views of that year's uploads |
|---|---|---|---|---|
| 2021 | 19 | 0 | 19 | 0.3M |
| 2022 | 84 | 45 | 39 | 11.4M |
| 2023 | 375 | 299 | 76 | 74.9M |
| 2024 | 133 | 130 | 3 | 36.1M |
| 2025 | 135 | 121 | 14 | 56.8M |
| 2026 | 64 | 63 | 1 | 11.9M |

  The 2025 total is lifted by 14 Shorts holding 41M of it. — same inventory
- **Top 25 uploads by views:**
  - 18 are Shorts:
    - "Wait For The Transition *SNAX SHOCKED*" 8.63M, [GmZty_6yrQs](https://www.youtube.com/shorts/GmZty_6yrQs);
    - "When hacker meets developer" 7.70M;
    - "Goldy Bhai in End" 7.02M;
    - "Ye Sab Kya Dekhna Pad Raha Hai @MortaLyt" 5.57M, [nh5gRpJjWAk](https://www.youtube.com/shorts/nh5gRpJjWAk);
    - "Gully Cricket With … Yuzvendra Chahal" 5.26M, [4azg_AzPrFU](https://www.youtube.com/shorts/4azg_AzPrFU);
    - "Dost party dene ko maan gaya" 5.23M, [_7xoj4uURm8](https://www.youtube.com/shorts/_7xoj4uURm8);
    - "Boys When No One's Home" 5.15M;
    - "Every Delivery Men Be Like" 5.07M.
  - The long videos in the top 25:
    - "Joker Reaction On Carryminati Collab…" 1.48M (30 Oct 2024, [YI0ntgz9Y_o](https://www.youtube.com/watch?v=YI0ntgz9Y_o));
    - "Jonathan Raids Joker Again After 4 Years" 1.42M (6 Apr 2026, [tt1gwGtxjlU](https://www.youtube.com/watch?v=tt1gwGtxjlU));
    - "Joker & Snax *TRIGGERED* Goldy Bhai" 1.06M (21 Dec 2023, [E6h-WNsY7jM](https://www.youtube.com/watch?v=E6h-WNsY7jM));
    - "JOKER SHOCKED BY GAMERFLEET NEW HOUSE" 994K (1 Mar 2026, [xlAtlvjotlE](https://www.youtube.com/watch?v=xlAtlvjotlE)).
  - Source: same inventory.

### Inferences
- **A three-step business model:**
  1. a Shorts and reels outlet (2021-22);
  2. a volume clip farm feeding the algorithm with 1-2 clips a day (2023);
  3. a fixed 8-minute "session" product at 1-2 a week (2024-26).

  The switch to 8 minutes in 2023H2-2024H1 coincides with long-video median views jumping about 4×, from 44-54K to 221K. Shorts were then dropped (only 3 in 2024). This is consistent with a deliberate move to mid-roll-eligible, longer videos (8:00 is YouTube's mid-roll threshold, an inference about motive).
- The 2026 slowdown (Oct: 1 upload; none since 5 Oct) and the lowest like rate on record (4.0% in 2026H2) suggest the second channel is being de-prioritised. The cause is unknown; it could be editor capacity or Joker's shift to vlogs and IRL.

### Gaps
- The 2022 gap (Mar to Aug 2022) and whether the channel changed hands or editors are not explained by any public source.
- Type boundaries are judgment calls. "Stream-talk moment" against "short BGMI moment" in particular is uncertain for about 10-15% of 2022-23 clips. Titles were not watched one by one.
- vidIQ's monthly view numbers are third-party estimates.

## 2. What each type is based on (source proof)

### Takeaway
**Almost everything JokerClips posts is cut from Joker's own YouTube live streams.** The stream type decides the product:

- BGMI streams become sessions, challenges, crate openings and short moments.
- Watch-party streams become esports reactions.
- "Baat chit" chat or call streams become talk and call cuts.
- "REACTION AND BGMI" streams become creator and pro-player reactions.
- GTA RP, Meccha Chameleon and other game streams become other-game highlights.
- IRL streams from Tokyo and London become IRL clips.

Four exceptions were proven:
- **re-cuts of main-channel vlogs** ([DAMPfDiX7xw](https://www.youtube.com/watch?v=DAMPfDiX7xw), [PE0ipDb4zTA](https://www.youtube.com/watch?v=PE0ipDb4zTA));
- **other creators' streams** used as the main footage, either the opponent's POV in a 1v1 or the raider's own stream (Jonathan);
- **2022-early 2023 clips cut from Joker's Loco streams** (Loco watermark);
- **natively shot vertical phone footage** for Shorts: 18 Shorts are 2160×3840, so they are not stream crops.

### Cited Findings
**Caption-matched sources** (13 new maps; delay = upload date minus stream date)

| Highlight (type, upload) | Source | Stream span used → output | Order | Delay |
|---|---|---|---|---|
| [72gO2p-DjEg](https://www.youtube.com/watch?v=72gO2p-DjEg) crate opening with Mazin, 15 Jul 2026, 561 s | [u3KbWR2zR_M](https://www.youtube.com/watch?v=u3KbWR2zR_M) "100000 UC MUMMY CRATE OPENING \| COSPLAY", 12 Jul, 4.76 h | 0:11:41-1:15:44 (64 min) → 9.3 min; 30 units; 470 of 561 s matched | Chronological; teaser at 0:00 | 3 d |
| [ixzk66I3_g4](https://www.youtube.com/watch?v=ixzk66I3_g4) "First Time Playing BGMI NARUTO UPDATE 4.5", 19 Jul 2026, 560 s | [aK1RteB3m8I](https://www.youtube.com/watch?v=aK1RteB3m8I) "100000 UC FERRARI CRATE OPENING", 17 Jul, 5.32 h | Part 1 from stream 1:37-2:44; part 2 from **earlier** 0:38-1:31 | Later block put first as the hook | 2 d |
| [iStTbFVJeMM](https://www.youtube.com/watch?v=iStTbFVJeMM) Meccha Chameleon "Trolling S8UL Creators", 27 Jul 2026, 536 s | **Four streams**: [5nJYjC8GLSk](https://www.youtube.com/watch?v=5nJYjC8GLSk) (25 Jul), [b0f7KTw5C9U](https://www.youtube.com/watch?v=b0f7KTw5C9U) (23 Jul), [BWnYw1Ds-sE](https://www.youtube.com/watch?v=BWnYw1Ds-sE) (14 Jul), [yYb7LVi5SM4](https://www.youtube.com/watch?v=yYb7LVi5SM4) (22 Jul) | 25 Jul at 0:50-1:33, then 23 Jul, 14 Jul, 25 Jul again, 22 Jul, 25 Jul; 32 units; 396 of 536 s matched | Newest first, then a mosaic; chronological within each stream | 2-13 d |
| [Kobcv7gzuAY](https://www.youtube.com/watch?v=Kobcv7gzuAY) "Meccha Chameleon For The First Time With S8UL", 24 Jun 2026, 483 s | [xxhe1u_UAEk](https://www.youtube.com/watch?v=xxhe1u_UAEk) "MECCHA CHAMELEON WITH FRIENDS", 17 Jun, 4.68 h | 0:13-3:54 (**221 min**) → 8 min; 26 units | Chronological | 7 d |
| [GOJlT6ZGLJ0](https://www.youtube.com/watch?v=GOJlT6ZGLJ0) BMPS watch-party reaction, 21 Jun 2026, **1,489 s** | [b91X1_1jYAg](https://www.youtube.com/watch?v=b91X1_1jYAg) "BMPS WATCHPARTY FROM LAN \| DAY 3", 21 Jun, 4.70 h | 0:20-4:20 (240 min) → 24.8 min; 40 units, up to 141 s each | Strictly chronological, ending on the trophy ceremony | **56 min after the stream ended** (timestamps) |
| [_413bOEizBA](https://www.youtube.com/watch?v=_413bOEizBA) "Crazy Reaction On GodLike Domination In PMWC", 8 Aug 2026, 816 s | [lblQJhPuBLo](https://www.youtube.com/watch?v=lblQJhPuBLo) "PMWC at EWC GROUP STAGE DAY 3 - WATCHPARTY", 8 Aug, 5.10 h | 0:56-4:47 → 13.6 min; units of 8-79 s | Chronological | **About 13 min after the stream ended** |
| [nUz6ZI6xjkY](https://www.youtube.com/watch?v=nUz6ZI6xjkY) "Family Emotional & Shreeman Legend Reaction On 2Million", 14 Jun 2026, 416 s | [zeMhk9nbmJM](https://www.youtube.com/watch?v=zeMhk9nbmJM) "BAAT CHIT & 2 MILLION", 13 Jun, 2.75 h | 0:47-1:01 (15 min) → 7 min; units up to 89 s | Chronological; the on-screen counter crosses 1,999,9xx → 2,000,449 | 1 d |
| [VuRDeNxsWrk](https://www.youtube.com/watch?v=VuRDeNxsWrk) "Joker Marfa With Fukra & Triggered Insaan", 2 Aug 2026, 650 s | zljKAi-oebA "GTA V RP NOW \| 50000 UC SUIT CRATE OPENING IN BGMI DONE", 1 Aug, 6.34 h | **4:59-6:13**, the end of the stream (a video call) → 10.8 min; 30 units | Chronological | 1 d |
| [FEbtdwSZBWY](https://www.youtube.com/watch?v=FEbtdwSZBWY) "Joker SHOCKED Japanese in TOKYO", 20 Sep 2026, 232 s | [d437IGsBCA8](https://www.youtube.com/watch?v=d437IGsBCA8) "IRL FROM JAPAN - TOKYO GAME SHOW", 19 Sep, 2.87 h | Mostly 0:02-0:21 plus one bit at 1:55 → 3.9 min | Teaser, then chronological | 20 h after the stream ended |
| [DAMPfDiX7xw](https://www.youtube.com/watch?v=DAMPfDiX7xw) "Joker Hua Mazin Se Pareshan", 31 Aug 2026, 143 s | **Main-channel vlog** [3t6ez7hvgFI](https://www.youtube.com/watch?v=3t6ez7hvgFI) "Mazin Ronaldo Nahi Bol Pata", 3 Jul, 1,242 s | Vlog 9:58-11:23, then 7:40, then 2:37 (backwards) | Reordered | 59 d |
| [PE0ipDb4zTA](https://www.youtube.com/watch?v=PE0ipDb4zTA) "Joker Video Call With Team 07!", 1 Sep 2026, 120 s | Same vlog [3t6ez7hvgFI](https://www.youtube.com/watch?v=3t6ez7hvgFI) | Vlog 18:31-19:29, one block | n/a | 60 d |
| [snn-fsC6M30](https://www.youtube.com/watch?v=snn-fsC6M30) "JOKER SNAX GOLDY BHAI PLAYING CHAINED TOGETHER PART 2", 6 Jul 2025, 653 s | [09BELLdxNnE](https://www.youtube.com/watch?v=09BELLdxNnE) "CHAINED TOGETHER PART 2 \| WORLD HEAVY TRIO", 3 Jul 2025, 5.43 h | 0:24-4:19 → 10.9 min; 29 units | Chronological | 3 d |
| [AJETkuZ0K6A](https://www.youtube.com/watch?v=AJETkuZ0K6A) "Joker Frustrated Snax In Carry The Glass", 4 Nov 2025, 703 s | [eATYZOFh1jY](https://www.youtube.com/watch?v=eATYZOFh1jY) (31 Oct, 0:33-3:19), then [uRo8oB7yJmE](https://www.youtube.com/watch?v=uRo8oB7yJmE) (1 Nov, 2:16-3:18, "ENDING") | Two streams, **older first** (the game's progress order) | 3-4 d |
| [bCJbLnqdfOQ](https://www.youtube.com/watch?v=bCJbLnqdfOQ) "JOKER 80,000 UC LAMBORGHINI CRATE OPENING", 27 Jul 2024, 502 s | [YKoZcBozQXc](https://www.youtube.com/watch?v=YKoZcBozQXc) "80,000 UC LAMBORGHINI CRATE OPENING", 19 Jul 2024, 3.97 h | 0:29-1:33 (64 min) → 8.4 min; 27 units | Chronological | 8 d |
| [TRopu3_PGAo](https://www.youtube.com/watch?v=TRopu3_PGAo) "80,000 UC New Porsche Crate Opening", 8 Dec 2025, 315 s | [4UGn-RWwnuc](https://www.youtube.com/watch?v=4UGn-RWwnuc) "80000 UC PORSCHE SUPER CAR OPENING", 5 Dec 2025, 5.49 h | 0:13-1:40 → 5.3 min | Chronological | 3 d |

— alignments in `data/seg_*.txt`. The upload-after-stream times use the stream's `release_timestamp` plus its duration, compared with the highlight's upload `timestamp`.

**Visual proof of the other source types** (storyboards)
- **Other creators' streams**
  - In [EjaP5wHkv8w](https://www.youtube.com/watch?v=EjaP5wHkv8w) "Joker Demotivated Snax In 1V1 *TDM CHALLENGE*" (12 Jul 2024, 600K), Joker's POV carries a large "JOKER" banner. At about 263 s the edit cuts to **Snax's own stream** ("SNAX" banner, Snax's follower counter 1,814,195).
  - In [tt1gwGtxjlU](https://www.youtube.com/watch?v=tt1gwGtxjlU) (Jonathan raid, 1.42M), the footage is **Jonathan's stream layout**: his cam on the left, Joker's call window and Jonathan's live chat column on the right. It opens on a browser showing Joker's stream (counter 1,529,201).
  - In Meccha [iStTbFVJeMM](https://www.youtube.com/watch?v=iStTbFVJeMM), 1:58-2:17 shows a female co-player's webcam layout, i.e. a co-streamer's POV.
  - In GTA RP [tFP76OqZrgU](https://www.youtube.com/watch?v=tFP76OqZrgU) (May 2023), the editor adds 2-3 other RP players' webcams as small inserts.
  - Source: the linked videos.
- **Loco streams in 2022-early 2023**
  - Among Us clip [E302l8_77GA](https://www.youtube.com/watch?v=E302l8_77GA) (2 Sep 2022) and "Snax VS Joker *CALL FIGHT*" [QqqL1qmOXzs](https://www.youtube.com/watch?v=QqqL1qmOXzs) (15 Jan 2023, 697K) both carry a "LOCO" watermark on GTA or Among Us footage.
  - Joker had a Loco account in 2022, alongside YouTube, when he joined S8UL in June 2022. — [Sportskeeda](https://www.sportskeeda.com/esports/news-i-still-getting-goosebumps-jokerkihaveli-shares-story-joining-s8ul)
- **Reaction sources**
  - [xlAtlvjotlE](https://www.youtube.com/watch?v=xlAtlvjotlE) is GamerFleet's house-tour video playing full frame with Joker's facecam bottom right, inside his stream layout (iQOO 15R sponsor bar).
  - [YI0ntgz9Y_o](https://www.youtube.com/watch?v=YI0ntgz9Y_o) is Carryminati's video with Joker's cam top left and the follower counter 889,5xx.
  - [lyHdl-U4yNQ](https://www.youtube.com/watch?v=lyHdl-U4yNQ) "Joker SHOCKED by Pakistani Pro Player" (933K) opens on a YouTube browser page and then plays Falak's video (ViewSonic watermark) beside Joker's cam (counter 894,164). It is **a reaction to the pro's uploaded video, not a lobby encounter**.
  - [oPmzf8LnVTw](https://www.youtube.com/watch?v=oPmzf8LnVTw) (DOK, 880K) and [9gsc9CJXV0Y](https://www.youtube.com/watch?v=9gsc9CJXV0Y) (Thunder) work the same way.
  - Source: storyboards of the linked videos.
- **Watch-party sources**
  - [1bSJjsh33kM](https://www.youtube.com/watch?v=1bSJjsh33kM) and [_413bOEizBA](https://www.youtube.com/watch?v=_413bOEizBA) show the PMWC broadcast (team table, kill feed) with Joker's facecam, a charity QR code and the follower counter (2,170,7xx, then a jump to 2,172,257 at 7:53, meaning two time ranges were joined).
  - [t0DVlWe9TOo](https://www.youtube.com/watch?v=t0DVlWe9TOo) (ESL LAN entry, 420K, Jan 2025) is the venue broadcast inside a YouTube player, with Joker's cam top left and the counter 930,778.
- **IRL streams.** [FEbtdwSZBWY](https://www.youtube.com/watch?v=FEbtdwSZBWY) shows a live-chat pop-up "@RJ12_VLOGZ GIAN KI AMMI KI SHOP PER JAAO" at 3:14-3:18, a stream overlay that confirms the IRL-stream source.
- **Native vertical Shorts:** 18 Shorts have a 2160×3840 maximum resolution (shot vertically on a phone). 74 are 720×1280 and 59 are 1080×1920 (crops or reposts). — Shorts metadata

### Inferences
- **Type follows stream type.** The editor does not invent formats; each JokerClips type mirrors a stream genre on the main channel:
  - **BGMI streams** become sessions, challenges, crate openings and short moments.
  - **Watch-party streams** become esports reactions.
  - **Baat chit / 2 MILLION / call streams** become talk and call cuts.
  - **"REACTION AND BGMI" streams** (e.g. [vEo1YmkmONI](https://www.youtube.com/watch?v=vEo1YmkmONI)) become creator and pro-player reactions.
  - **GTA RP streams** became RP clips until Sep 2023. RP was dropped afterwards even though Joker still streams GTA RP weekly (18 RP titles since Dec 2025, per `joker_deep.md`).
  - **Other games** (Meccha, Chained Together, Carry The Glass) become 8-10 min highlights in their launch weeks.
  - **IRL streams** become 3-4 min IRL clips.
- Two JokerClips clips (Aug-Sep 2026) were cut from a two-month-old main-channel vlog. JokerClips is also used to recycle Joker's vlog footage when there is no fresh stream material (inference, based on 2 cases).
- About 10% of footage seen in storyboards is another creator's stream (opponent, co-streamer or raider). Kaatclip cannot reproduce that from one recording.

### Gaps
- Not mapped:
  - [1bSJjsh33kM](https://www.youtube.com/watch?v=1bSJjsh33kM): Joker speaks little, and its probable source (PMWC Day 4, VkI9RlUUSpc) returned HTTP 429.
  - Paris clip [4I4p4QhCR1s](https://www.youtube.com/watch?v=4I4p4QhCR1s): not in [lwvfYT4cm4Q](https://www.youtube.com/watch?v=lwvfYT4cm4Q).
  - [FOfqOmIyqmY](https://www.youtube.com/watch?v=FOfqOmIyqmY).
  - The ESL and GC watch-party clips: their exact streams were not fetched.
- 2022-23 short clips were not caption-mapped, because their stream VODs mostly do not exist on YouTube (Loco). The source is inferred from watermarks.
- Whether the editor downloads co-streamers' VODs or receives files from them is unknown.

## 3. How each type is made (editing structure, devices, length)

### Takeaway
Each type has its own recipe, and the effort scales with the type.

- **Sessions, challenges and crate openings: the full comedy kit.** Many short units, facecam zooms, meme inserts, labelled stickers, subtitles and time cards. Since 2025-26 most open with an "IN THIS VIDEO" teaser. They are padded to 8:00-8:20.
- **Other-game highlights:** the same kit plus a short game-explainer intro.
- **Watch-party reactions: almost raw.** Broadcast feed plus facecam in long chronological units (8-141 s). Length is set by the event (8-25 min), not by the 8-minute rule.
- **Creator and pro reactions:** the video being watched plus the facecam, cut to the reaction peaks. 2-25 min.
- **Talk, call and IRL clips:** side-by-side webcams or handheld IRL footage. Light cuts, a few stickers, 2-11 min.
- **2023 short clips: one moment, 30-130 s.** A cold start on the trigger, a facecam-heavy crop, an abrupt end.

### Cited Findings
**Caption metrics of the new examples** (speech = share of seconds with a word; wpm = words a minute; laugh = [हंसी] tags; teaser = 4-word phrases from the first 20 s that repeat later; top replay = heatmap peaks in seconds)

| Upload | Video | Type | Length | Views | Speech | wpm | Laugh | Teaser | Top replay (s) |
|---|---|---|---|---|---|---|---|---|---|
| 15 Jan 2023 | [QqqL1qmOXzs](https://www.youtube.com/watch?v=QqqL1qmOXzs) Call fight | short moment | 221 | 697K | 0.56 | 73 | 0 | 0 | 128-132 |
| 27 Jul 2024 | [bCJbLnqdfOQ](https://www.youtube.com/watch?v=bCJbLnqdfOQ) Lamborghini crate | crate | 502 | 222K | 0.86 | 109 | 0 | 0 | 85, 446 |
| 31 Jan 2025 | [t0DVlWe9TOo](https://www.youtube.com/watch?v=t0DVlWe9TOo) ESL entry | watch party | 517 | 420K | 0.91 | 141 | 1 | 0 | 434-444 |
| 6 Jul 2025 | [snn-fsC6M30](https://www.youtube.com/watch?v=snn-fsC6M30) Chained Together | other game | 653 | 510K | 0.89 | 143 | 0 | 5 | 633, 450 |
| 4 Nov 2025 | [AJETkuZ0K6A](https://www.youtube.com/watch?v=AJETkuZ0K6A) Carry The Glass | other game | 703 | 462K | 0.88 | 142 | 26 | 0 | 597, 555 |
| 24 Nov 2025 | [rPrskSRLq_4](https://www.youtube.com/watch?v=rPrskSRLq_4) PMGC with Rega | watch party | 888 | 137K | 0.97 | 153 | 3 | 0 | 825, 452 |
| 1 Mar 2026 | [xlAtlvjotlE](https://www.youtube.com/watch?v=xlAtlvjotlE) GamerFleet house | creator reaction | 1,388 | 994K | 1.00 | 239 | 4 | 0 | 138-152 |
| 6 Apr 2026 | [tt1gwGtxjlU](https://www.youtube.com/watch?v=tt1gwGtxjlU) Jonathan raid | call or raid | 402 | 1.42M | 0.94 | 150 | 20 | 0 | **8-12** |
| 14 Jun 2026 | [nUz6ZI6xjkY](https://www.youtube.com/watch?v=nUz6ZI6xjkY) 2M celebration | stream moment | 416 | 130K | 0.89 | 141 | 12 | 0 | 212-216 |
| 21 Jun 2026 | [GOJlT6ZGLJ0](https://www.youtube.com/watch?v=GOJlT6ZGLJ0) BMPS | watch party | 1,489 | 134K | 0.97 | 164 | 2 | 0 | 1,384-1,399 |
| 24 Jun 2026 | [Kobcv7gzuAY](https://www.youtube.com/watch?v=Kobcv7gzuAY) Meccha first | other game | 483 | 277K | 0.90 | 137 | 29 | 0 | 309-362 |
| 15 Jul 2026 | [72gO2p-DjEg](https://www.youtube.com/watch?v=72gO2p-DjEg) Mummy crate | crate | 561 | 98K | 0.90 | 119 | 11 | 6 | 410-528 |
| 19 Jul 2026 | [ixzk66I3_g4](https://www.youtube.com/watch?v=ixzk66I3_g4) Naruto update | session (novelty) | 560 | 107K | 0.93 | 145 | 11 | 0 | 89, 403 |
| 27 Jul 2026 | [iStTbFVJeMM](https://www.youtube.com/watch?v=iStTbFVJeMM) Meccha trolling | other game | 536 | 147K | 0.87 | 130 | 11 | 0 | 353-364 |
| 2 Aug 2026 | [VuRDeNxsWrk](https://www.youtube.com/watch?v=VuRDeNxsWrk) Fukra call | call cut | 650 | 150K | 0.97 | 188 | 23 | 0 | 312-318, 429 |
| 8 Aug 2026 | [_413bOEizBA](https://www.youtube.com/watch?v=_413bOEizBA) PMWC | watch party | 816 | 47K | 0.49 | 43 | 1 | 0 | none |
| 9 Aug 2026 | [1bSJjsh33kM](https://www.youtube.com/watch?v=1bSJjsh33kM) GodLike commentary | watch party | 567 | 208K | 0.58 | 54 | 0 | 0 | 335-340, 488 |
| 24 Aug 2026 | [4I4p4QhCR1s](https://www.youtube.com/watch?v=4I4p4QhCR1s) Paris | IRL | 189 | 26K | 0.97 | 207 | 6 | 0 | none |
| 20 Sep 2026 | [FEbtdwSZBWY](https://www.youtube.com/watch?v=FEbtdwSZBWY) Tokyo | IRL | 232 | 43K | 0.96 | 145 | 4 | 10 | none |
| 31 Aug 2026 | [DAMPfDiX7xw](https://www.youtube.com/watch?v=DAMPfDiX7xw) Mazin | vlog re-cut | 143 | 97K | 0.87 | 142 | 3 | 0 | none |

— `tools/hlstats.py` over the auto-captions and heatmaps of the linked videos

**What the storyboards show, by type** (in addition to the 2026 session devices in `joker_deep.md`)
- **Crate opening** ([72gO2p-DjEg](https://www.youtube.com/watch?v=72gO2p-DjEg), [bCJbLnqdfOQ](https://www.youtube.com/watch?v=bCJbLnqdfOQ), [TRopu3_PGAo](https://www.youtube.com/watch?v=TRopu3_PGAo))
  - 0:00-0:13 is an "IN THIS VIDEO" teaser over the crate UI.
  - Then it alternates between the crate UI (spin grid, "CONGRATULATIONS" and "YOU GOT" result cards) with a small cam, the large "JOKER" stream banner, and full-frame cam zooms on his reactions.
  - Joker is in mummy cosplay in 72gO. His son Mazin is cut in at 0:54.
  - A meme insert with the label "Krafton" (1:33) appears when he blames the publisher ("Krafton, itna bhi mat looto").
  - Units follow the spending: every pull and its reaction (median unit about 13 s).
  - The heatmap peaks are the late big pulls (410-528 s in 72gO; 446 s in bCJb).
- **Party and indie games** ([Kobcv7gzuAY](https://www.youtube.com/watch?v=Kobcv7gzuAY), [iStTbFVJeMM](https://www.youtube.com/watch?v=iStTbFVJeMM), [snn-fsC6M30](https://www.youtube.com/watch?v=snn-fsC6M30), [AJETkuZ0K6A](https://www.youtube.com/watch?v=AJETkuZ0K6A))
  - A game-explainer intro: Kobc 0:00-0:28 shows the game's own trailer beside Joker's cam ("You literally become them!").
  - The stream layout has the facecam bottom left. Multi-cam layouts in co-op games put three webcams across the bottom in Chained Together and two side by side in Carry The Glass.
  - Speaker-labelled subtitles: a round avatar of the co-player plus their line ("Ye chat padhta h ye mafia chat padhta", "to bmps kon khel raha h").
  - Labels such as "*realisation*" over a zoomed facecam (3:31) and "CHAT" over a Bollywood clip.
  - A black-and-white freeze on falls in Chained Together (0:44), and a "18+ Wear Headphones" warning sticker opening Carry The Glass.
  - Round results ("Chameleons Win!" at 6:58), and an abrupt end mid-round at 8:02.
  - The "IN THIS VIDEO" teaser was already used in July 2025 on Chained Together. That **corrects `joker_deep.md`**, which found it absent in 2024-25; the absence held only for sessions.
- **Watch party** ([GOJlT6ZGLJ0](https://www.youtube.com/watch?v=GOJlT6ZGLJ0), [_413bOEizBA](https://www.youtube.com/watch?v=_413bOEizBA), [1bSJjsh33kM](https://www.youtube.com/watch?v=1bSJjsh33kM), [t0DVlWe9TOo](https://www.youtube.com/watch?v=t0DVlWe9TOo))
  - The tournament broadcast fills the frame. Joker's (and Rega's) facecam stays in the stream layout's corner.
  - No teaser, no memes and no zoom cards were seen.
  - Cuts drop the gaps between fights.
  - The video ends on the match result or the trophy ceremony (GOJl's last frames).
  - Kept units are long: GOJl's 40 units include 54-141 s blocks. 1,542 s of speech were matched in a 1,489 s video because Joker and Rega talk over the casters continuously.
- **Creator and media reaction** ([xlAtlvjotlE](https://www.youtube.com/watch?v=xlAtlvjotlE), [YI0ntgz9Y_o](https://www.youtube.com/watch?v=YI0ntgz9Y_o), [YZKzj66Rwx4](https://www.youtube.com/watch?v=YZKzj66Rwx4), [wZtsRJGWw-U](https://www.youtube.com/watch?v=wZtsRJGWw-U))
  - The watched video is full frame with the facecam box. The edit cuts to a full-frame facecam when he comments (xlAt at 3:00 and 3:30).
  - The watched video's own on-screen text is kept ("GARAGE", "GUEST ROOM" room cards).
  - The 2023 version ([wZtsRJGWw-U](https://www.youtube.com/watch?v=wZtsRJGWw-U), Playground show) is a **50/50 split**: Joker's cam on the left, the show on the right, 94 s.
  - xlAt is 100% speech at 239 wpm. These are talk-dense.
- **Talk and call cuts** ([VuRDeNxsWrk](https://www.youtube.com/watch?v=VuRDeNxsWrk), [nUz6ZI6xjkY](https://www.youtube.com/watch?v=nUz6ZI6xjkY), [QqqL1qmOXzs](https://www.youtube.com/watch?v=QqqL1qmOXzs), [rfOy23DfKkQ](https://www.youtube.com/watch?v=rfOy23DfKkQ))
  - Two webcams side by side (Joker plus the caller) for the whole video.
  - A brief insert of the donation or QR overlay, and in-room arrivals of friends or family. The 2M video shows his mother and wife entering as the counter passes 2,000,000.
  - The 2023 call fight cuts between the two webcams as full frames and goes black and white for the drama (1:01).
- **IRL clips** ([FEbtdwSZBWY](https://www.youtube.com/watch?v=FEbtdwSZBWY), [4I4p4QhCR1s](https://www.youtube.com/watch?v=4I4p4QhCR1s), [DAMPfDiX7xw](https://www.youtube.com/watch?v=DAMPfDiX7xw))
  - Wide action-cam or selfie footage, 16:9, no game.
  - Tokyo has a boxed "IN THIS VIDEO" teaser (0:00-0:10) and a caption sticker "Bro believed him" (3:12).
  - Paris has small circular face stickers popping in (0:12, 0:33).
  - All three are 2-4 minutes.
- **2022-23 short moments** ([QqqL1qmOXzs](https://www.youtube.com/watch?v=QqqL1qmOXzs), [E302l8_77GA](https://www.youtube.com/watch?v=E302l8_77GA), [tFP76OqZrgU](https://www.youtube.com/watch?v=tFP76OqZrgU), [J9EcR7MvhbM](https://www.youtube.com/watch?v=J9EcR7MvhbM))
  - A single conversation or fight.
  - A "JOKER KI HAVELI" logo bug sits bottom right on 2023 gameplay (J9Ec, U21B).
  - The face-sticker meme (Joker's head pasted on a still) is used in 2022.
  - "Moye Moye" ([J9EcR7MvhbM](https://www.youtube.com/watch?v=J9EcR7MvhbM), Dec 2023, 762K) shows the heaviest 2023 effects: dimmed, blurred and black-and-white frames around the meme song beats.
- **Challenge or vs** ([EjaP5wHkv8w](https://www.youtube.com/watch?v=EjaP5wHkv8w), [X_c7l5im3bY](https://www.youtube.com/watch?v=X_c7l5im3bY))
  - The match scoreboard (kills) stays visible at the top.
  - The edit switches between Joker's POV and the opponent's POV (Snax's stream, EjaP at 263 s).
  - Speech is sparse during fights (EjaP has single-word lines in many 30 s windows: "aaja aaja", "what the"). The trash talk sits between rounds.

**Heatmap shape by type** (long-video heatmaps; peak position = where in the video the highest replay bin falls)

| Type | n | Peak position (median) | Peak in first 5% | First 5 bins ÷ mean | Last bin ÷ mean |
|---|---|---|---|---|---|
| Sessions | 157 | 0.52 | 11% | 1.39 | 0.23 |
| Challenges | 46 | 0.63 | 15% | 1.78 | 0.30 |
| Crate openings | 24 | 0.58 | 8% | 1.11 | 0.13 |
| Watch parties | 31 | 0.53 | 3% | 1.00 | 0.37 |
| Creator reactions | 57 | 0.39 | 7% | 1.39 | 0.03 |
| Stream-talk / IRL | 47 | 0.25 | 45% | 2.12 | 0.10 |
| Short moments | 67 | 0.31 | 30% | 1.33 | 0.00 |
| Shorts (all kinds) | n/a | n/a | 94-100% | n/a | n/a |

— `tools/hm.py` over YouTube "most replayed" data

**Minute-by-minute: [Kobcv7gzuAY](https://www.youtube.com/watch?v=Kobcv7gzuAY) "Joker Played Meccha Chameleon For The First Time With S8UL" (483 s, 24 Jun 2026, 277K; source: 17 Jun stream 0:13-3:54)**

| Time | Screen | Moment |
|---|---|---|
| 0:00-0:28 | Joker's cam on the left; the game's trailer on the right ("You literally become them!", "Subscribe") | The game's pitch is read out ("objects literally become their entire body"); Joker: "bas hai samajh gaya" |
| 0:29-1:13 | Stream layout; colour picker; round 1 | "brush bada kaise hota hai", then a squad member in the cupboard ("toilet bana hua hai koi"); avatar subtitle "Ye chat padhta h ye mafia chat padhta" repeated twice (a looped punchline) |
| 1:04-1:30 | Barn map; avatar subtitles "Jo mujhe sabse pehle dhundta h", "to bmps kon khel raha h" | Insult banter between rounds; [laughter] |
| 1:43-2:30 | A co-player's cam inset; the hunt | "stream sniper" accusation, then "ye kaun hai? Ankita hai" [laughter] ×3 |
| 2:45-3:41 | Gold statue reveal; facecam zoom with the "*realisation*" label (3:31) | "heads off bhai… salute" for a disguise, then "itni der se toilet ke logo ko insaan samajh raha tha. I am noob, and proved" |
| 3:45-5:10 | Police-car map; Bollywood meme insert (5:10) | "Aman nahi pakda gaya" [laughter]; "chat, meri kaarigari achhi nahi lagi?" |
| 5:15-6:58 | A last-survivor round; "Chameleons Win!" (6:58) | "shaant raho… Joker bhai ne clutch kara hai", then "main game jeetne ke liye nahi, dil jeetne ke liye khelta hoon" (replay peak 5:09-6:02) |
| 7:00-8:02 | Penguin map; the round begins | "Krutika upar dekh", "ye kaun sa map lagaya hai"; **abrupt end mid-round** |

**Minute-by-minute: [72gO2p-DjEg](https://www.youtube.com/watch?v=72gO2p-DjEg) "Mazin Joins Joker For Black Mummy Crate Opening - 80,000 UC Lost" (561 s, 15 Jul 2026, 98K; source: 12 Jul stream 0:11-1:15)**

| Time | Screen | Moment |
|---|---|---|
| 0:00-0:13 | "IN THIS VIDEO" over the crate grid, then a cosplay cam | Teaser: "Krafton, itna bhi mat looto re… mummy tumhe milegi nahi" (the line comes back at 7:00) |
| 0:14-0:58 | Full-frame cam (mummy costume); Mazin cut-in at 0:54 | A "trick" ritual with an emote; the "540 UC" spin count |
| 0:59-1:48 | Mummy-set preview with the "JOKER" banner; "YOU GOT"; a "Chained Inferno Grenade CONGRATULATIONS" card | "main kitna bada crate opener hoon"; first junk pull |
| 1:28-2:12 | "Krafton" meme face (1:33); UC purchase pop-up; "Chaos Calamity" card | Blames Krafton; "4.5 ka update kiya hai" |
| 3:00-4:30 | Mazin's turn ("Mazin it's your turn") | A child's spin, then "tere baap ko baap kholega", "baraat mein naachu?" |
| 5:00-6:30 | "ek 10, ek 10" repeated pulls | A repetition gag; "36,000 UC mere paani mein gaye" (a [laughter] peak) |
| 7:00-8:10 | "most unluckiest crate opening"; "London mein luck kharab karke aaya" | Escalating loss; replay peak at 410 s |
| 8:10-9:20 | The final pulls and "75,000 lag gaye" | Ends on the total spent: the payoff is the loss figure (replay 522-528 s) |

**Minute-by-minute: [GOJlT6ZGLJ0](https://www.youtube.com/watch?v=GOJlT6ZGLJ0) "Joker Reaction On SouL & BMPS Champions GodLike" (1,489 s; uploaded 56 min after the 21 Jun stream ended)**

| Time | Screen | Moment |
|---|---|---|
| 0:00-2:44 | Broadcast spectator view; Joker's and Rega's cams; team table | Live commentary on SouL's drop and first fight; stream 0:20-0:36 |
| 2:45-8:30 | Fights, scope shots, an "ELIMINATED" banner | Reactions to each knock; units of 11-26 s, stream 0:36-1:18 |
| 8:30-15:50 | Later matches ("UTILITIES" overlay) | Stream 1:53-2:41; the skipped gaps (+1,390 s) are breaks between matches |
| 15:50-22:34 | Final match; a 114 s continuous block | Stream 3:21-4:14 |
| 22:34-24:49 | Champions announcement and trophy on stage | Ends on the ceremony; **replay peak 1,384-1,399 s** (the GodLike win) |

**Minute-by-minute: [VuRDeNxsWrk](https://www.youtube.com/watch?v=VuRDeNxsWrk) "Joker Marfa With Fukra & Triggered Insaan After Long Time" (650 s; source: the last 74 min of the 1 Aug stream)**

| Time | Screen | Moment |
|---|---|---|
| 0:00-1:30 | Two webcams side by side (Joker; Fukra Insaan with a chat overlay) | Football or cricket talk, then "apna banner laga… pehla banner" (career talk) |
| 1:30-3:45 | Same layout; full-frame Joker cam inserts at 1:04-1:19 | Diet and "calories" teasing; "khatron ke khiladi" banter |
| 2:09-2:13 | A black frame with a phone-screen donation or QR insert (₹19,8x,xxx) | Donation total shown |
| 4:30-6:45 | Same layout | Money and early-career story; IShowSpeed and KSI stream talk; "chacha dikhao apne dole" (a [laughter] cluster, replay 312-318 s) |
| 7:30-10:50 | Other people join Fukra's room (8:21), then Triggered Insaan | "Dharmendra sir / Remo D'Souza" mix-up; the accent-copying bit; warm ending: "bahut pyare insaan hai" |

**Minute-by-minute: [FEbtdwSZBWY](https://www.youtube.com/watch?v=FEbtdwSZBWY) "Joker SHOCKED Japanese in TOKYO" (232 s; source: the 19 Sep Tokyo Game Show IRL stream, mostly its first 21 min)**

| Time | Screen | Moment |
|---|---|---|
| 0:00-0:10 | "IN THIS VIDEO" boxed teaser, 5 shots | Cosplayers, a Japanese booth, a selfie |
| 0:11-0:36 | Selfie cam on the road, holding his phone | Arrival; reading chat ("pata chal gaya tha aap ja rahe ho") |
| 0:35-1:32 | Queue of cosplayers; group shots | "Gohan, what's your action?" with cosplayers; "nice cosplay, sabki taarif karenge" |
| 1:39-2:13 | Inside the hall | "Goldy bhai chat mein hai kya?" chat interaction |
| 2:46-3:12 | A Japanese mouse-pad booth; "Bro believed him" sticker; chat pop-up at 3:14 | Pranking a Japanese stall worker with Hinglish small talk (the title's "shocked Japanese") |
| 3:41-3:52 | Hall, at stream 1:55 | Closing line; abrupt end |

**Minute-by-minute: [QqqL1qmOXzs](https://www.youtube.com/watch?v=QqqL1qmOXzs) "Snax VS Joker *CALL FIGHT*" (221 s, 15 Jan 2023, 697K; Loco GTA RP stream)**

| Time | Screen | Moment |
|---|---|---|
| 0:00-0:02 | GTA RP scene with a "LOCO" watermark and a small cam | Hook frame from the stream |
| 0:02-1:00 | Full-frame alternation of Joker's webcam and Snax's webcam | Escalating mock argument on the call |
| 1:01-1:05 | Black-and-white freeze of Joker | A drama beat (replay peak 128-132 s comes later) |
| 1:05-3:33 | Cam ping-pong continues | The fight peaks around 2:08-2:12 |
| 3:33-3:44 | Back to the GTA RP feed with the LOCO watermark; a colour-bar glitch | End |

### Inferences
- **Effort ladder.** Measured by visible edit density in the storyboards, from most to least:
  1. sessions, challenges and crate openings (a change every 5-10 s; teaser, memes, cards);
  2. other games (the same plus an explainer);
  3. talk, call and IRL;
  4. creator reactions;
  5. watch parties (nearly raw).
- **Speed is the price of edit density.** Watch parties go up within 13-56 minutes of the stream ending, IRL within a day, and edited sessions 2-8 days later.
- **Length rule by type.** Edited comedy types are padded to 8:00-8:20 (or 10-12 min when the source is a co-op game). Event types (watch parties, reactions) take whatever the event needs, 8-25 min. Talk, IRL and short moments end when the story ends.
- **The 2023 short-clip recipe** (one moment, a hook frame, an abrupt end, 30-130 s) is effectively a horizontal Short. Its heatmaps peak in the first 5% in 30% of cases and the last bin is always 0, the same behaviour as Shorts.

### Gaps
- Sound effects, music cues and bleeps cannot be measured without audio. Caption tags show [संगीत] (music) only in a few videos (1-4).
- Storyboard steps of 1-10 s miss sub-second effects such as flash transitions.
- Minute-by-minute timings are ±5 s.

## 4. Shorts in depth

### Takeaway
JokerClips' 152 Shorts are mostly **not BGMI**:
- 48 are IRL skits, memes, "relatable" content and trend reels;
- 35 are stream moments;
- 25 are BGMI gameplay moments;
- 19 are IRL friend-group clips and vlog excerpts;
- 15 are GTA RP skits;
- 6 are cricket;
- 4 are Valorant.

They ran at 2-15 a month from Nov 2021 to Oct 2023, nearly stopped (3 in 2024), came back with **14 Shorts in Aug-Dec 2025** that averaged millions of views, and stopped again (1 in 2026).

What gets the most views is a relationship or IRL moment with a payoff at the end and a fixed text header promising it ("Wait For The End", "Goldy Bhai in End"). Pure BGMI gameplay Shorts have the lowest views (median 70K).

### Cited Findings
- **Volume by year:** 19 (2021), 39 (2022), 76 (2023), 3 (2024), 14 (2025), 1 (2026).
  - Median views by year: 14K, 69K, 117K, 1.99M, 1.62M, 222K.
  - Median length by year: 21, 23, 17, 15, 22.5, 25 s.
  - Overall duration bins: 0-9 s 7, 10-19 s 72, 20-29 s 44, 30-39 s 15, 40-49 s 11, 50-59 s 3.
  - Source: [Shorts tab](https://www.youtube.com/@jokerclipss/shorts)
- **Hashtags in titles:** 100% (2021), 87% (2022), 58% (2023), 33% (2024), 0% (2025-26). Shorts descriptions were "#jokerkihaveli #shorts #jokerclips" or similar, or empty, until the "Main Channel" boilerplate. — same
- **Types by year:**
  - GTA RP skits: 2021-22, median 21K.
  - IRL skits, memes, relatable content and trend reels: 2021-23, median 123K.
  - BGMI gameplay moments: 2021-24, median 70K.
  - Stream moments: 2022-23, then 5 in 2025, median 149K.
  - IRL friend-group clips and vlog excerpts: 9 in 2025, median 531K.
  - Cricket: median 1.66M.
  - Source: same
- **Formats seen in 23 Shorts' storyboards:**
  - **GTA RP skit** ([A9LGPp8zxp8](https://www.youtube.com/shorts/A9LGPp8zxp8), 2021, 58 s): GTA scenes intercut with Bollywood reaction memes.
  - **"Sigma rule" format** ([tmg4CturmLk](https://www.youtube.com/shorts/tmg4CturmLk), 245K): facecam on top, game below, a bold caption "RULE NO 1 BIWI KE AAGE KUCH NAHI".
  - **Stacked stream moment** ([GmZty_6yrQs](https://www.youtube.com/shorts/GmZty_6yrQs) 8.63M, [_RgXLRs1wx8](https://www.youtube.com/shorts/_RgXLRs1wx8) 7.70M, [bmoICLbNemI](https://www.youtube.com/shorts/bmoICLbNemI) 2.22M, [TH4R1ypnHCc](https://www.youtube.com/shorts/TH4R1ypnHCc) 2.0M, [MrhS2WbKaVA](https://www.youtube.com/shorts/MrhS2WbKaVA), [aBL79oTbVdk](https://www.youtube.com/shorts/aBL79oTbVdk)):
    - the facecam and the gameplay stacked (either order);
    - a top header ("BGMI vs FREE FIRE", "MY EMOTIONS WHEN TEAM SOUL TAKES CHICKEN DINNER", "Me in training ground / During match");
    - stickers ("ABEY TAKLE");
    - a cut to another person's webcam or a meme face as the payoff.
  - **IRL friend-group Shorts of 2025** ([SATVDilBDOY](https://www.youtube.com/shorts/SATVDilBDOY) 7.02M, [_7xoj4uURm8](https://www.youtube.com/shorts/_7xoj4uURm8) 5.23M, [wlGXh5IWeZ0](https://www.youtube.com/shorts/wlGXh5IWeZ0) 2.33M, [OXZ5boyFNUs](https://www.youtube.com/shorts/OXZ5boyFNUs) 1.55M, [CTQZMNXMr-E](https://www.youtube.com/shorts/CTQZMNXMr-E) 933K, [uTrHx260tq4](https://www.youtube.com/shorts/uTrHx260tq4) 495K, [Yo6nck1Zmok](https://www.youtube.com/shorts/Yo6nck1Zmok) 360K):
    - handheld home or hangout footage with S8UL friends;
    - a constant top header: "Wait For The End😂", "Goldy bhai AVOCADO Sandwich order maar diye", "When Bro Clean Shaves For The First Time😭", plus a footer such as "Congo for 1M Subs Dadah".
  - **2023 skits** ([wTP3Eh6uexE](https://www.youtube.com/shorts/wTP3Eh6uexE) 5.07M, [g7uHaaLdXX0](https://www.youtube.com/shorts/g7uHaaLdXX0) 997K, [hiD0iBCN1t0](https://www.youtube.com/shorts/hiD0iBCN1t0) 3.62M birthday prank): phone-shot IRL footage with burned-in Hindi captions.
  - **Reposted reels** ([Y9IWAJgbHos](https://www.youtube.com/shorts/Y9IWAJgbHos) 5.15M, [joZnBu2RSUw](https://www.youtube.com/shorts/joZnBu2RSUw) 2.02M, [ppfTdPTPURY](https://www.youtube.com/shorts/ppfTdPTPURY) 1.24M, [eitWMEsy894](https://www.youtube.com/shorts/eitWMEsy894)): a narrow clip on a blurred background, a sign of a repost of a vertical clip made for another app (inference).
  - **BGMI moment** ([icIr3BWd1nM](https://www.youtube.com/shorts/icIr3BWd1nM)): facecam on top with captions ("laser spray bolte bro"), gameplay below with the "JOKER KI HAVELI" logo, ending on a friend's reaction cam.
  - **Vlog excerpt** ([tb7vUafHeso](https://www.youtube.com/shorts/tb7vUafHeso), Feb 2026): ends with a "Watch Full Video on JokerKiHaveli" card plus the main-channel thumbnail.
  - Sources: the linked Shorts.
- **Heatmaps:** in every Shorts type with heatmaps, the most-replayed bin is in the first 5% (94-100%). The last bin is 0-0.45 × mean. — `tools/hm.py`
- **Upload hour (IST):** Shorts spread 10:00-21:00. 17:00-20:00 is the busiest (69 of 151). Long videos cluster in the morning (see section 5). — inventory timestamps
- **Native resolution:** 18 Shorts at 2160×3840 (phone-shot vertical), 59 at 1080×1920, 74 at 720×1280. — metadata

### Inferences
- **Two eras of Shorts:**
  - 2021-23: a volume play with low views per Short (median 14-117K), mostly reels and RP or stream skits.
  - 2025: a hit-driven play of only 14 Shorts with a 1.6M median. Almost all are IRL friend moments or BGMI-stream "relatable" memes with a header, not kills.

  The 2025 burst then stopped even though it worked. The reason is unknown; it could be editor capacity or a move of Shorts to the main channel, whose Shorts are lifestyle series (`joker_deep.md`).
- **The "wait for the end" device** is a text promise plus a payoff in the last 3-5 s. It suits relationship moments ("Goldy Bhai in End", "Wait For The Transition"), not gameplay.
- For Kaatclip's BGMI-only input, the Shorts JokerClips proves can be made from a stream are:
  - **stacked stream moments**: a funny line or reaction with a game trigger and a header caption;
  - **BGMI gameplay moments**, which are weak on views.

  The IRL and skit Shorts, the biggest earners, need footage Kaatclip will not have.

### Gaps
- Retention and swipe-away rates of Shorts are not public. Heatmaps are coarse for 10-20 s clips.
- Whether the 2025 IRL Shorts were cut from main-channel vlogs or from unpublished phone footage was not caption-checked (no Hindi captions fetched for most Shorts).

## 5. Upload practice: titles, thumbnails, descriptions, timing, what performs

### Takeaway
- **Packaging is templated:**
  - since Aug 2023, one boilerplate description ("Main Channel: …" plus 3 hashtags);
  - one 6-tag set;
  - no chapters on any upload;
  - titles built from named S8UL co-stars plus a caps conflict word in asterisks plus emoji.
- **Timing depends on the type:**
  - watch parties within an hour of the stream ending;
  - IRL and calls the next day;
  - edited sessions, crate openings and other games 2-8 days later;
  - vlog re-cuts about 2 months later.
- Long videos go up mostly at **09:00-11:00 IST** since 2024.
- The surest view drivers are a famous co-star (Snax, Goldy), a famous outside creator (Carryminati, GamerFleet, Jonathan) and a one-time event (a raid, a celebration, a first-time game). Caps words and emoji make no measurable difference.

### Cited Findings
- **Descriptions:**
  - 412 uploads (5 Aug 2023 to 5 Oct 2026) start with "Main Channel: https://youtube.com/@Jokerkihavelii", then "#jokerkihaveli #jokerclips #bgmi".
  - Earlier uploads used "#jokerkihaveli #shorts #jokerclips" (116), "#jokerkihaveli #shorts" (48) or nothing (107).
  - One exception carries an "esportsawards.com" voting link.
  - **No description links to the source stream. No upload has chapters.**
  - Source: inventory metadata
- **Tags:**
  - The 6-tag set ('joker', 'joker clips', 'joker ki haveli', 'joker reaction', 'bgmi', 'funny highlight') is on 280 uploads.
  - The 2022-23 sets started 'jokerkihaveli, joker ki haveli, jokerclips, joker clips, s8ul, shorts, gaming, funny…' (203 uploads).
  - 121 uploads have none.
  - Occasional extras, e.g. Kobcv7gzuAY adds 'Meccha chameleon', 'Mecha chameleon', 'S8ul'.
  - Source: same
- **Upload hour (IST, long videos):**
  - 2023: spread through the day, top hours 11:00, 18:00 and 12:00.
  - 2024: 60 of 130 at 08:00-12:00 (top 10:00).
  - 2025: 65 of 121 at 08:00-12:00 (top 10:00).
  - 2026: 32 of 63 at 08:00-12:00 (top 09:00).
  - The exceptions are watch-party cuts uploaded at night, right after the stream (20:38 IST for [_413bOEizBA](https://www.youtube.com/watch?v=_413bOEizBA)).
  - Weekdays are flat (Thu 103 to Sat 127).
  - Source: inventory timestamps
- **Gaps between long uploads** (median days): 0.9 (2022), 0.95 (2023, 56 same-day doubles), 2.1 (2024), 2.6 (2025), 4.0 (2026, no same-day doubles). — inventory
- **Delay from stream to upload, measured on 19 maps** (13 here, 6 in `joker_deep.md`):
  - watch parties: 13-56 min after the stream ended;
  - IRL and call and celebration cuts: about 1 day (20 h, 1 d, 1 d);
  - crate and novelty sessions: 2-3 days (72gO, ixzk, TRop);
  - other games: 3-7 days (snn-, AJET, Kobc), and 2-13 days for the four-stream Meccha compilation;
  - 2024 crate: 8 days;
  - comedy sessions: 4-6 days; two-stream compilations 14-20 days (`joker_deep.md`);
  - vlog re-cuts: 59-60 days.
  - Source: section 2 table
- **Title features** (212 sessions, challenges and crate openings, 2024-26; median views with the feature against without):
  - a co-star name: 68% of titles, 187K vs 147K;
  - "ft." or an @handle: 22%, 202K vs 162K;
  - starting with "When/How/If": 8%, 210K vs 167K;
  - "*CAPS*" asterisk words: 50%, 159K vs 186K;
  - "HIGHLIGHT": 45%, 175K vs 168K;
  - 😂/🤣: 61%, 167K vs 176K;
  - money (₹, UC, Lakh): 8%, 123K vs 178K;
  - "first time/new": 13%, 149K vs 179K.
  - Source: `tools/extra.py`
- **Co-star in title** (all long videos 2024-26, median views):

| Co-star | Videos | Median views |
|---|---|---|
| Kaash | 8 | 261K |
| Snax | 66 | 231K |
| Goldy | 29 | 230K |
| Scout | 8 | 217K |
| Payal | 5 | 195K |
| MortaL | 14 | 180K |
| Mavi | 20 | 175K |
| Mamba | 14 | 166K |
| Aman | 19 | 164K |
| Krutika | 16 | 144K |
| Rega | 33 | 141K |
| SouL | 17 | 134K |
| Viper | 7 | 109K |

  — same
- **The biggest long videos are one-off events with outside stars:**
  - Carryminati collab reaction (1.48M);
  - Jonathan's raid (1.42M; its replay peak is at 8-12 s, Jonathan's first appearance);
  - GamerFleet house (994K);
  - Snax first home (910K, [YZKzj66Rwx4](https://www.youtube.com/watch?v=YZKzj66Rwx4));
  - DOK reaction (880K);
  - "NOOB VOL 1" music video (885K, [9eY2MleOTy4](https://www.youtube.com/watch?v=9eY2MleOTy4)).
  - Source: inventory
- **Thumbnails:** a face collage with a speech bubble. The bubble line is taken from the video's peak line (`joker_deep.md`; not re-measured here).

### Inferences
- **Title rule that the data supports:** name the most famous people present (with "ft."), and frame it as a situation ("When … ", "Joker Reaction On …"). Asterisk caps and emoji are habit, not drivers.
- **The fall from about 230K (Snax, Goldy) to about 140K (Rega)** in 2026 titles mirrors the co-star switch. The channel's reach depends on who is in Joker's lobby, which Kaatclip cannot control but can surface in the title.
- **Morning publishing (09-11 IST)** of yesterday's or last week's stream suits Indian viewers before evening streams. This is an inference; no A/B data exists.

### Gaps
- No CTR or retention data. Thumbnails were not systematically measured across years.
- The upload times are those of public release. Scheduled uploads cannot be distinguished from manual ones.

## 6. What this means for Kaatclip (an automatic tool working from a creator's own stream recording)

### Takeaway
Of JokerClips' 811 uploads, the types Kaatclip can produce from **one creator's own BGMI stream recording** are:

| Kaatclip can produce | Uploads | Share | Median views |
|---|---|---|---|
| BGMI funny session | 159 | 20% | 185K |
| Challenge or vs (own POV only) | 50 | 6% | 166K |
| Crate opening | 28 | 3% | 118K |
| Short BGMI or stream moment | 133 | 16% | 52K |
| Stacked stream-moment Shorts and BGMI gameplay Shorts | 60 | 7% | 70-149K |
| **Total** | about 430 | **about 53%** | |

These are also the steady earners. A Kaatclip "esports watch-party" mode is technically easy (long chronological units) but carries a broadcast-rights risk.

Out of reach:
- other games and GTA RP, unless Kaatclip expands beyond BGMI;
- IRL and vlog material (a different input);
- reactions to other creators' videos (copyright, and no game signal);
- anything using co-streamers' or raiders' footage (not in the recording);
- reposted reels, skits and cricket Shorts.

### Cited Findings
- **The shares above** come from the type table in section 1 — inventory
- **Measured cut rules per Kaatclip-feasible type** (sections 2-3 and `joker_deep.md`):

| Type | Source window | Units | Order | Teaser | Length | Ending |
|---|---|---|---|---|---|---|
| Crate opening | 64 min (12 Jul 2026 stream 0:11-1:15; 19 Jul 2024 stream 0:29-1:33) | 27-30, median about 13 s | Chronological | 0:00-0:13 teaser | 8.4-9.3 min | On the total-loss or best-pull line |
| Comedy session | 30-160 min, 1-2 streams | 15-30 reaction units | `joker_deep.md` rules | Yes (2026) | 8:00-8:10 | Punchline |
| Novelty session (first time in a mode or update) | Can lead with a later block as the hook (ixzk: stream 1:37-2:44 first, then 0:38-1:31) | n/a | Hook first | n/a | n/a | n/a |
| Co-op party game | 3-4 h of one stream (Kobc 221 min; snn- 0:24-4:19), or 2-4 streams (AJET, iStT) | 26-32 | Chronological | Game-explainer intro | 8-12 min | Game result |
| Watch party | 4 h → 13-25 min | 8-141 s | Strictly chronological | None | 13-25 min | Trophy or result |
| Celebration or milestone | 15 min → 7 min | Up to 89 s | Chronological | n/a | 7 min | Around the counter crossing (2,000,000) |

- **Signals the edits key on** (observed):
  - a spoken trigger and punchline with laughter (Kobc 29 laugh tags; AJET 26);
  - repeated-word loops ("ek 10 ek 10", "ye chat padhta… ye mafia chat padhta" said twice);
  - result screens ("Chameleons Win!", "CONGRATULATIONS", "VICTORY", MVP);
  - money or UC spoken totals ("36,000 UC paani mein", "75,000 lag gaye");
  - an overlay counter crossing a milestone (2,000,000);
  - donation totals;
  - a co-player speaking (speaker-avatar subtitles);
  - a new mode or update launch (Spider-Man, Naruto 4.5).
  - Source: the linked videos

### Inferences (design implications for Kaatclip)
1. **Classify the session first, then apply the matching recipe.** The detectable classes are:
   - BGMI squad comedy;
   - crate opening (UC store and crate UI on screen, spin results, spoken UC numbers);
   - challenge or TDM (TDM scoreboard, rounds);
   - new-mode exploration;
   - chat or call (two-webcam or no-game frames);
   - milestone (counter crossing).

   JokerClips proves each has its own unit length, order, teaser use and target length. A single "highlight" template would mis-cut crate openings (whose payoff is the cumulative loss at the end) and watch parties (which want long, raw, chronological units).
2. **Crate-opening mode (new; cheap to build).**
   - Input signals: the crate UI and "CONGRATULATIONS" or "YOU GOT" result-card OCR, spoken UC amounts and laughter.
   - Rules: each pull plus its reaction is one unit (10-20 s). Keep them chronological over the first 60-90 min. Add a 10-15 s teaser built from the best result and the angriest line. End on the final total line. Aim for 8-9.5 min.
   - Crate openings are about 3% of JokerClips uploads (median 118K views). Crate streams recur on Joker's channel: 13 crate-opening stream titles since Dec 2025 (`joker_deep.md`).
3. **Milestone and celebration mode:** when the on-stream follower counter crosses a round number, or chat or donation spikes, cut the 10-15 min around it into a 5-7 min chronological video, released the next day.
4. **Hook-first ordering for novelty streams:** for a "first time in a new mode" session, put the best later block first (ixzk did this), with otherwise chronological units.
5. **Release timing per type:**
   - watch-party and celebration cuts: same night or next morning;
   - edited comedy and crate cuts: 2-6 days, as a 09:00-11:00 IST scheduled publish;
   - leftovers: a "part 2" within 3 weeks.
6. **Shorts:** Kaatclip should generate stacked (facecam plus game) Shorts of 15-30 s with a fixed top header. Pick relationship or meme moments (a teammate's line, a "Me in training ground / During match" contrast), not kill clips: JokerClips' BGMI-kill Shorts have a 70K median against 149K for stream-moment Shorts and 1.6-2.2M for the 2025 meme-headed stream Shorts.
7. **Out of reach, and why:**
   - **co-streamer, opponent or raider POV** (EjaP, tt1g, iStT): not in the creator's recording; would need multi-source input and permission;
   - **IRL, vlog and phone-shot Shorts:** a different input, with no game HUD signals;
   - **reactions to other creators' or pros' videos:** the third-party video is the content, so the copyright risk is high and there is no game signal;
   - **watch-party broadcasts:** tournament broadcast rights. JokerClips posts them, but a tool automating re-uploads of broadcast footage carries a takedown risk (inference);
   - **meme and film inserts:** copyright, as already decided in the earlier report: Kaatclip's own stickers only.
8. **Packaging defaults:**
   - title "[Streamer] & [Co-star] [situation]" with "ft. @handles" for everyone on call;
   - a description with a main-channel link and 3 hashtags;
   - no chapters needed (JokerClips uses none);
   - 6 fixed tags.

### Gaps
- The share of JokerClips content that Kaatclip "can produce" assumes BGMI-only support. If Kaatclip adds other games (Meccha Chameleon, Valorant, GTA RP), about 5% more becomes reachable, but no game-specific signals were studied.
- The crate-opening recipe rests on 4 mapped crate videos (72gO, bCJb, TRop and TZCV in `joker_deep.md`). The unit-length and teaser rules should be checked on the owner's own crate streams.
- No public evidence shows how JokerClips decides which streams get a highlight. Selection is inferred from what was posted.
