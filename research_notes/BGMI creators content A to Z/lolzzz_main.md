# LoLzZz Gaming (@LoLzZzGaming): every content type A to Z, where its footage comes from, how it is edited and how it is uploaded

Measured 12 Nov 2026 from public YouTube data only, with yt-dlp:
- flat listings of every tab (/videos 418, /streams 2,972, /shorts 107, /playlists 8);
- full metadata for 87 items;
- Hindi auto-captions (`hi-orig`) for 46 videos and streams;
- storyboard contact sheets for 37 videos (one frame every 5-10 s), a whole-stream timeline (one frame a minute) for 3 streams;
- 20 thumbnails.

No video or audio was downloaded. This note builds on, and does not repeat, `research_notes/BGMI highlight channels deep study/lolzzz_deep.md` (6 record matches mapped to their streams, cut ratios, record Shorts) and `research_notes/BGMI highlight video structure/lolzzz_challenge.md` (titles, record anatomy). Where this study corrects them, it says so.

Method notes:
- **Dates.** The flat /videos listing only gives YouTube's "N months/years ago", so older videos are put in one-year age bands (for example "Nov 2021-Nov 2022"). The 52 newest videos (Nov 2024-Oct 2026) have exact dates from metadata.
- **Stream dates.** The /streams listing gives no dates. 130 streams have exact start times. The rest were dated by interpolating between anchors every 100 streams, so per-year stream counts are approximate (about ±30 at year boundaries). Monthly counts before June 2026 are interpolation artefacts and are not used.
- **Types.** Every item was classified by title keywords with a script (`classv.py`, `classs.py`). The sampled videos were then checked by eye. The classes are approximate for the oldest PUBG Mobile era titles.
- **"Subscriber counter as a clock".** His stream overlay shows a live subscriber count, so the counter visible in a highlight tells which stream (and roughly which hour) a clip came from. A counter that jumps by thousands inside one video means the video stitches several streams or days. Teammates' overlays carry their own counters (Jonathan about 6.7-7.8M, Spower about 0.5M), which identifies their POV.
- **Raw data.** Raw data, scripts and contact sheets are in `C:\Users\soura\AppData\Local\Temp\claude\21027423ba80eb72\c7886632-c6c6-4a95-81c6-c6cbac2a769e\scratchpad\a2z\lolzzz_main\` (`streams_all.jsonl`, `streams_classified.json`, `videos_classified.json`, `meta2\`, `sb\`, `thumbs_*.jpg`, `stream_sample_dates.txt`, `pl_items.txt`). The earlier raw data is in `...\ab9e7281-...\scratchpad\yt_research\lolzzz\` and `...\lolzzz_deep\`.
- **Notation.** All times are IST. "HL" is a highlight video. "(I)" marks an inference.

## 1. Full inventory: what is on every tab, by type, and how the mix changed from 2019 to 2026

### Takeaway
The channel is mostly a live-stream archive: **2,972 streams (about 13,000 hours, Jul 2019 to 11 Nov 2026)** against 418 long uploads and 107 Shorts. The edited output has shrunk from about 95-98 uploads a year (2019-2022) to **16 in the last 12 months**. Those 16 are mostly one kind of video: the single-match "N SOLO KILLS" record, cut from his own stream, plus a few tournament POV videos, collabs and sponsored pieces.

Streams have grown longer (median 3.4 h in 2019, 6.4 h in 2026) and are now mainly rank pushes and kill-target challenges. Since 2026 they also include big esports watch parties, which are his most-watched streams.

Main-channel Shorts stopped in practice (12 since Oct 2023; the last on 6 Feb 2026). Shorts and overflow highlights moved to LoLzZz Plays. From late Sep 2026 he also streams on **Kick**, on alternate days.

### Cited Findings
**Tab sizes** ([videos](https://www.youtube.com/@LoLzZzGaming/videos), [streams](https://www.youtube.com/@LoLzZzGaming/streams), [shorts](https://www.youtube.com/@LoLzZzGaming/shorts), [playlists](https://www.youtube.com/@LoLzZzGaming/playlists)):
- /videos: 418 items, from the band Nov 2018-Nov 2019 to 25 Oct 2026.
- /streams: 2,972 items. The earlier study stopped at 600, the fetch limit; this time the whole tab was listed. The oldest is 26 Jul 2019 20:12 ("MK14 + 6x = AATANK!!… PAYTM ON SCREEN", [BQL63wRqs_s](https://www.youtube.com/watch?v=BQL63wRqs_s)), the newest 11 Nov 2026. The durations add up to about 13,027 h.
- /shorts: 107 items.
- /playlists: 8 playlists, all from the 2019-2021 PUBG Mobile era and no longer kept up. "Sniper God!!" lists 26 items (2 of them unrelated videos by other channels), "CLUTCHES" 20, "Montages" 6, "Gta 5" 2, "LIFESTORY OF LoLzZz" 2. "FUNNY HIGHLIGHTS", "LoLzZz vs Hackers" and "Conqueror" returned no items. Source: playlist listings ([Sniper God!!](https://www.youtube.com/playlist?list=PLmRym92F3NrbRJ2v6r5oVsJf9m4H3okeG), [CLUTCHES](https://www.youtube.com/playlist?list=PLmRym92F3NrZRi9zhnvgsC9_41tDwgbhx)).

**Streams by year** (interpolated dates; one row per year; source: [streams tab](https://www.youtube.com/@LoLzZzGaming/streams), with dated anchors such as [j8KeIp6P70U](https://www.youtube.com/watch?v=j8KeIp6P70U) 27 Nov 2024, [QUZqlUUKnew](https://www.youtube.com/watch?v=QUZqlUUKnew) 27 May 2022, [oRIx4OuqHbQ](https://www.youtube.com/watch?v=oRIx4OuqHbQ) 8 Mar 2020):

| Year | Streams | Hours | Median length (IQR) | Median views | Main stream types (share of that year's streams) |
|---|---|---|---|---|---|
| 2019 (from Jul) | ~252 | ~843 | 3.4 h (3.0-3.8) | 49.5K | "RUSH GAMEPLAY", PUBG Mobile on emulator, Paytm/donations on screen |
| 2020 | ~638 (often 2 a day) | ~2,350 | 3.7 h | 108K | generic rush gameplay 27%, custom rooms / elite customs 23%, rank push 23%, other games 13% (PUBG Mobile VN/KR during the India ban, GTA V, Among Us, PUBG PC) |
| 2021 | ~461 | ~1,789 | 3.8 h | 166K | elite customs and scrims; BGMI launch (Jul 2021); iOS and emulator streams |
| 2022 | ~382 | ~1,399 | 3.5 h | 210K | rank push 56%, generic 10%, scrims 9%, kill challenge 9%, chicken (WWCD) streak 8% |
| 2023 | ~320 | ~1,371 | 4.1 h | 282K | rank push, chicken streaks, KD pushes (BGMI back from mid-2023) |
| 2024 | ~348 | ~1,861 | 5.5 h | 468K | rank push 38%, kill challenge 20%, chicken challenge 17%, scrims 7%, crate opening 4% |
| 2025 | ~318 | ~1,880 | 5.9 h | 547K | rank push 51%, kill challenge 26%, crate opening 8% |
| 2026 (to 11 Nov) | ~253 | ~1,532 | 6.4 h | 510K | rank push 47%, kill challenge 13%, crate opening 9%, watch party 6%, scrims/tournament 5%, chicken 5%, cash challenge 3% |

- **Stream types over the whole archive** (title classes; median length, median views):
  - rank push 1,038 (4.7 h, 287K);
  - generic gameplay 528 (3.5 h, 108K; mostly 2019-2021);
  - tournament, scrims and custom rooms 490 (4.2 h, 153K; mostly 2020-2021);
  - kill-target challenge 289 (4.8 h, **437K**; rising from 2022);
  - chicken/WWCD-streak challenge 172 (4.7 h, 347K);
  - milestone/special 140; other games 103; crate opening 96 (5.2 h, **548K**); update exploration 36;
  - watch party 21 (4.8 h, **1.1M**; 16 of them in 2026);
  - other challenge 18; sponsored event 16; members-only 15; cash challenge 10 (9 in 2026).
  - Source: `classs.py` over [the streams tab](https://www.youtube.com/@LoLzZzGaming/streams).
- **His most-watched streams are all 2026 watch parties:**
  - "BMSD 2026 | GRAND FINALS DAY-1 WATCHPARTY", 2.1M views, 6.0 h ([hNCb6AT6dwc](https://www.youtube.com/watch?v=hNCb6AT6dwc)).
  - Day-3, 1.9M ([ASbJkj4MQFc](https://www.youtube.com/watch?v=ASbJkj4MQFc)).
  - "PMWC WATCHPARTY + RANK PUSH", 1.7M, 11.9 h ([JpUxjVTrWsE](https://www.youtube.com/watch?v=JpUxjVTrWsE)).
  - The best gameplay stream is "TAG LoLzZz IS HERE! | LIVE WITH TAG SQUAD | A NEW JOURNEY BEGINS", 1.3M, 29 Jun 2026 ([sOuXq86Gzdc](https://www.youtube.com/watch?v=sOuXq86Gzdc)).
  - Source: [streams tab](https://www.youtube.com/@LoLzZzGaming/streams).

**Long uploads (/videos, 418) by type** (title classes; median length; median views; when they were made). Source: [videos tab](https://www.youtube.com/@LoLzZzGaming/videos), `videos_classified.json`:

| Type | n | Median length | Median views | When |
|---|---|---|---|---|
| Single-match kill highlight ("N SOLO KILLS…", records, "N FINISHES") | 119 | 627 s | 204K | every year; 8 of the 16 in the last 12 months |
| Gameplay or clutch highlight without a number (solo vs squad, "THIS IS HOW…") | 37 | 508 s | 127K | mostly 2019-2021 |
| Vlogs, IRL, BTS, story | 34 | 690 s | 206K | 24 of them in Nov 2021-Nov 2022 (GodLike bootcamp vlog series #1-#12, BGIS behind-the-scenes) |
| Fun challenges and trolling (RIP English, singing, randoms, Omegle) | 26 | 588 s | 171K | mostly 2019-2021 |
| "Hacker / exposed / banned" drama gameplay | 24 | 574 s | 212K | 2019-2022, then occasional |
| Collab squad gameplay with Jonathan and GodLike ("Deadly Duo", "backup to Jonathan") | 24 | 603 s | **340K** | 2021-2025 |
| Compilations (Top 10 clutches, "Sniper King [Part N]") | 23 | 522 s | 242K | mostly 2019-2020; Parts 2-3 in 2024-25 |
| Tournament, scrims, customs POV | 21 | 519 s | 190K | 2020-21 elite customs; 2026 BGIS and scrims |
| Shorts-length items on /videos (≤61 s) | 20 | 40 s | 133K | 2020-2022 |
| TDM / 1v1 / 2v2 vs Jonathan and others | 14 | 530 s | **732K** | 2019-2025 |
| Squad-kill team records ("94 SQUAD KILLS") | 14 | 598 s | 250K | every year |
| Crate openings | 14 | 526 s | 177K | to mid-2024, then folded into kill videos |
| Cash/prize challenges ("₹/$/€ PER KILL", "$10,000 CHALLENGE") | 10 | 620 s | 195K | every year |
| Rank journeys ("JOURNEY TO CONQUEROR", "PLATINUM TO #1") | 8 | 526 s | 158K | 2019-2021, 2025 |
| Sponsored product videos | 7 | 828 s | 112K | 2020-2025 (plus 4 brand pieces classed elsewhere, see below) |
| Montages | 6 | 186 s | 41K | 2019-2020 only |
| Announcements and talks (copyright strike, "AM I A CHEATER") | 6 | 366 s | 77K | 2019-2020 |
| Other games (GTA V, Rogue Heist) | 5 | 557 s | 43K | 2019-2021 |
| Members-only | 1 | 3,540 s | n/a | "57 KILLS EXCLUSIVE FOR MEMBERS", 2025 ([4qFjEja74bk](https://www.youtube.com/watch?v=4qFjEja74bk)) |

**Uploads per one-year age band:**

| Band | Uploads |
|---|---|
| Nov 2018-Nov 2019 | 31 |
| Nov 2019-Nov 2020 | 98 |
| Nov 2020-Nov 2021 | 64 |
| Nov 2021-Nov 2022 | 95 |
| Nov 2022-Nov 2023 | 35 |
| Nov 2023-Nov 2024 | 43 |
| Nov 2024-Nov 2025 | 36 |
| Nov 2025-Nov 2026 | 16 |

Source: [videos tab](https://www.youtube.com/@LoLzZzGaming/videos)

**The newest 52 uploads** (exact dates, 12 Nov 2024 to 25 Oct 2026), types checked by hand:

| Type | n | Median length (range) | Median views (max) |
|---|---|---|---|
| Single-match record from his stream | 22 | 779 s (397-1,155) | 274K (990,648) |
| Squad record / collab gameplay | 5 | about 584 s | 254K (852,693) |
| Multi-match: Ultimate Royale / Legend / #1 journey | 4 | 1,368 s (614-1,874) | 224K (486,183) |
| Tournament / scrims POV | 4 | 1,122 s (897-2,121) | 299K (441,248) |
| Cash challenge | 3 | 622 s | 272K |
| 1v1 / 2v2 TDM collabs | 3 | 756 s | **847K** (1,572,738) |
| Comedy challenge collab | 1 | 556 s | 254K |
| Compilation | 4 | 559 s | 185K |
| "Exposed" | 1 | 887 s | 405K |
| Brand / sponsored | 5 | 586 s | **88K** (339,958) |
| Members-only | 1 | n/a | n/a |

Sources: metadata of each, e.g. [PtvEiSN48Dk](https://www.youtube.com/watch?v=PtvEiSN48Dk), [-qpx-ejuq9Q](https://www.youtube.com/watch?v=-qpx-ejuq9Q), [7nWKQjWnLOA](https://www.youtube.com/watch?v=7nWKQjWnLOA)

**2026 upload calendar (main channel, exact):**
- 16 Jan: UR Legend, from Jonathan's POV.
- 5, 7 and 14 Feb: BGIS 2026 rounds 1-3 POV.
- 21 Feb: 50 kills in a new mode.
- 20 Mar: 50 finishes in update 4.3.
- 6 May: sing-a-song challenge.
- 5 and 8 Jul: 61 and 64 kills.
- 16 Jul: per-kill ₹1000.
- 18 Jul: PMGC scrims.
- 10 Sep: 55 kills, Naruto mode.
- 17 Sep: UR multi-match.
- 19 Sep: 62 kills, zombie mode.
- 27 Sep: Lenovo/AMD laptop video.
- 25 Oct: 72 kills.
- Over the same period: about 253 streams.
- Source: per-video `timestamp`, e.g. [cLVYuMe5LJk](https://www.youtube.com/watch?v=cLVYuMe5LJk), [lOAtTbOsCzQ](https://www.youtube.com/watch?v=lOAtTbOsCzQ), [s3ixZgYaDGs](https://www.youtube.com/watch?v=s3ixZgYaDGs)

**Main-channel Shorts (107):**
- By topic: 44 titles are clutches (1v3/1v4/1v8), 23 sniping, 31 say "PUBG Mobile", 4 are sponsored (realme, Boult, Set Wet).
- Listing positions 51-107 are the 2020-2022 PUBG/BGMI clips: median 395K views, top **8,996,515** ("Sniper God Bolteee!!", 33 s, 17 Dec 2020, [aSie600ul4Q](https://www.youtube.com/shorts/aSie600ul4Q)) and **8,288,254** ("1 v 4 DBS Clutch in Apartment", 40 s, 30 Dec 2020, [Css0AXuRBZQ](https://www.youtube.com/shorts/Css0AXuRBZQ)).
- Positions 13-50 have a median of 283K.
- Only 12 Shorts since Oct 2023 (median 739K):
  - 10 between Oct 2023 and May 2024;
  - then 29 Aug 2024 (realme 13+), 20 Dec 2024 ("Rage quit on Mayur gaming's excuses") and 6 Feb 2026 ("1v4 CLUTCH IN BGIS ROUND 2", [OqEMk59-Z1o](https://www.youtube.com/shorts/OqEMk59-Z1o)).
- Source: [shorts tab](https://www.youtube.com/@LoLzZzGaming/shorts) and per-Short metadata.

**Companion channel.** LoLzZz Plays carries the overflow:
- ≥600 videos, 390 Shorts, 62 restreams;
- "vs streamer" fights, second record matches, cash challenges, esports reactions, about 2 Shorts a week.
- Measured in the deep study: [lolzzz_deep.md §1, §4](../BGMI%20highlight%20channels%20deep%20study/lolzzz_deep.md); [@lolzzzplays](https://www.youtube.com/@lolzzzplays/videos).
- On the 8 Sep 2026 stream he jokes about where things go, laughing: "LoLzZz Gaming channel pe … part two hi aayega; shorts LoLzZz Plays pe … reel aayegi Kick pe" — [-vMIYNYkLAA](https://www.youtube.com/watch?v=-vMIYNYkLAA) captions at 4:36:40.

### Inferences
- **(I) Four eras.**
  - 2019-2020, PUBG Mobile on emulator then mobile: many short daily highlights, trolling, sniper compilations and montages, with 3-4 h streams.
  - 2021-2022, GodLike bootcamp: vlogs and BTS series, collabs with Jonathan, the BGMI launch.
  - 2023-2025: the kill-record format and squad records take over, and Shorts stop.
  - 2026: one or two edited videos a month, almost all records or tournament POV, with 6-hour daily streams carrying the channel.
  - The edited share of his output keeps falling while stream hours stay at about 1,500-1,900 a year.
- **(I) The commercial centre is the stream, not the edit.** Streams average about 500K views each, 250+ a year. Long uploads average about 270K views, 16 a year.

### Gaps
- Exact dates for /videos older than Nov 2024 and for streams between the 100-stream anchors were not fetched (418 + 2,972 metadata calls would have been too heavy). Year and band counts are approximate.
- The Community tab, posts, and the channel's "Releases"/"Podcasts" shelves cannot be listed with yt-dlp.
- The members-only video and members-only streams could not be inspected.
- Three playlists returned no items (they may be empty or hidden).

## 2. What each content type is based on: where the footage comes from

### Takeaway
There are eight distinct footage sources:
1. **His own YouTube stream recording**, with the full overlay kept. This feeds records, cash challenges, crate openings, UR/rank journeys, compilations, "exposed" videos and most collabs.
2. **Teammates' streams**, cut in as a second POV (Jonathan, Spower and others), or used as the whole source.
3. **Clean device recordings with team comms**, for official tournaments (BGIS), where his stream overlay is absent.
4. **The official esports broadcast**, either co-streamed live (watch parties) or filmed off a monitor (BTS vlogs).
5. **Studio camera shoots** for sponsored phone and laptop videos, with a handheld "handcam" filmed over the phone and clean screen recordings.
6. **Handheld phone/camera vlogging** (meetups, bootcamp, travel).
7. **Agency-produced brand content** (Red Bull, Google Play) uploaded to his channel.
8. Since late Sep 2026, **Kick streams**, which may feed some highlights (unconfirmed).

Kaatclip's input, one creator's own stream recording, covers source 1 fully and nothing else.

### Cited Findings
| Type | Source of footage | Evidence (examples) |
|---|---|---|
| Single-match record | One match of his own YouTube stream, the next day | 6 matches mapped by captions in the deep study; the subscriber counter climbs steadily inside one match (2,798,802 → 2,798,848 in [-qpx-ejuq9Q](https://www.youtube.com/watch?v=-qpx-ejuq9Q)). The damage record keeps the stream overlay's own "DAMAGE COUNTER 0000 → 8336" widget ([C1RNs4p8uJg](https://www.youtube.com/watch?v=C1RNs4p8uJg), storyboard) |
| Record possibly from Kick | Unconfirmed: a non-YouTube stream | The 62-kill video matched no YouTube stream, and its captions mention "followers" ([Car5bJ_yP-E](https://www.youtube.com/watch?v=Car5bJ_yP-E)). He says on stream that "22 September" Kick starts and the plan is "ek din proper Kick hoga, chhe din YouTube" ([-vMIYNYkLAA](https://www.youtube.com/watch?v=-vMIYNYkLAA) 4:40, 4:44:00). On 26 Oct he says "ek din YouTube ek din Kick wo wala abhi system chal raha hai" and "aaj YouTube par continue karte hain, kal Kick karenge" ([w1NB9sVC8k0](https://www.youtube.com/watch?v=w1NB9sVC8k0) 2:00, 2:46:40). The 24 Oct stream ends "kal apan Kick pe live aayenge", with Bigg Boss watch-alongs planned there ([wq2fjFmms1U](https://www.youtube.com/watch?v=wq2fjFmms1U) 5:31:40). A KICK logo has been on his overlay bar since at least Oct 2026 (storyboard of wq2fjFmms1U) |
| Multi-match UR / "bonus matches" | Several matches of his own stream(s), not in time order | [lOAtTbOsCzQ](https://www.youtube.com/watch?v=lOAtTbOsCzQ): the counter reads 2,765,5xx in the main part, then **2,765,499** after a "BONUS MATCHES" card at 9:02 (an earlier hour), and 2,765,817 at the end |
| Legend / rank journey | Several days of his stream plus teammates' streams | [RsiHZgsCMtw](https://www.youtube.com/watch?v=RsiHZgsCMtw): his counter runs 2,470,743 → 2,493,134 (about 22K subscribers, so several days). It cuts to a **JONATHAN** overlay (7,336,xxx) and a **Spower** overlay (506,0xx) |
| UR Legend from Jonathan's stream | Jonathan's stream as the whole source | [69AEExuBZfU](https://www.youtube.com/watch?v=69AEExuBZfU): JONATHAN overlay, 7.4-7.9M counter (deep study) |
| Scrims highlight (PMGC prep) | His stream and Jonathan's stream, cross-cut | [fCCQkW1Uevk](https://www.youtube.com/watch?v=fCCQkW1Uevk): LoLzZz bar (2,697,582 → 2,698,260) alternating with JONATHAN bar (7,816,542 → 7,820,167) all through, plus both facecams |
| 1v1 / 2v2 TDM vs Jonathan | Both streams, cross-cut, one session | [PtvEiSN48Dk](https://www.youtube.com/watch?v=PtvEiSN48Dk): LoLzZz 2,140,46x-2,140,508 and JONATHAN 6,709,9xx-6,710,100 (about an hour of one session); a side-by-side split at 16:40-17:09 |
| Comedy challenge collab (sing a song) | Several creators' streams (Jonathan, Shreeman, Wolf) plus his | [T4D5femzSco](https://www.youtube.com/watch?v=T4D5femzSco): their facecams and phone-cams appear full-screen with name labels "SHREEMAN BHAU:", "WOLF MAHESHWARI:", "BHAU'S INNER VOICE:" |
| Official tournament POV (BGIS 2026) | Clean device recording (no stream overlay, no facecam) with team comms, plus official caster audio in the opening | [cLVYuMe5LJk](https://www.youtube.com/watch?v=cLVYuMe5LJk) storyboard: plain HUD only, "MATCH 2" and "MATCH 3" cards. The captions open with the broadcast caster ("dekhiye kitna behtar pradarshan hai, communication skills…") and then comms ("bugi aayi… Titu bhai idhar ghumao") |
| Compilation (Top 10 clutches) | Many streams over weeks | [tEK_UYkgVmE](https://www.youtube.com/watch?v=tEK_UYkgVmE): counters 2,203,362 / 2,213,067 / 2,219,908 / 2,243,488 / 2,245,507 / 2,246,111 in one 9-minute video |
| Crate opening | A segment of his stream (often the stream's announced opening) | [z1jXPJN8z-c](https://www.youtube.com/watch?v=z1jXPJN8z-c): overlay with a Paytm/G-Pay number, counter 1,782,4xx → 1,784,25x. On the "70K UC CRATE OPENING | ZOMBIES ARE BACK" stream ([w1NB9sVC8k0](https://www.youtube.com/watch?v=w1NB9sVC8k0), 6.6 h) the inventory and crate screens sit at about 0:47-1:05 and again near 2:46 ("chalo ek crate opening kar rahe") |
| "Exposed / handcam" | His stream | [nucVWiaxxVg](https://www.youtube.com/watch?v=nucVWiaxxVg): stream overlay, counter 2,180,8xx |
| Sponsored phone videos (OPPO Reno13/14, OnePlus Nord CE5) | A separate studio shoot: talking head in his studio, a "handcam" phone filmed by a second camera, a clean device screen recording with a hand-cam inset, product B-roll | [ML5Kk1ILBqE](https://www.youtube.com/watch?v=ML5Kk1ILBqE), [gaTQXGkRXnQ](https://www.youtube.com/watch?v=gaTQXGkRXnQ) (description "aim clicked at the right time on #OPPOReno14Series"), [ygTMhgAc9cA](https://www.youtube.com/watch?v=ygTMhgAc9cA) storyboards; no stream overlay in the gameplay |
| Sponsored laptop video | A studio shoot plus B-roll of PC games | [s3ixZgYaDGs](https://www.youtube.com/watch?v=s3ixZgYaDGs): description "#Collaboration Made in collaboration with Lenovo & AMD"; storyboard shows a Lenovo Legion 5 with spec captions |
| Brand event content | Produced by the brand or agency, multicam | "Google Play Squad Tournament - VIP Edition" ([7nWKQjWnLOA](https://www.youtube.com/watch?v=7nWKQjWnLOA)): a game-show studio, leaderboard graphics. "Cricket Madness… Team Jonathan… Team Techno" ([k7viYHrrVhg](https://www.youtube.com/watch?v=k7viYHrrVhg)): a Red Bull Showdown multicam vlog |
| Meetup and travel vlogs | Handheld phone/camera selfie vlogging | [R6WKP31A_CY](https://www.youtube.com/watch?v=R6WKP31A_CY): a crowd at a realme store, car selfie talk, ending on a desk talking head |
| BTS of a tournament (2022) | Phone vlog in the GodLike bootcamp plus the official BGIS broadcast filmed off a monitor | [tjBXf-bRjxo](https://www.youtube.com/watch?v=tjBXf-bRjxo) (1,065,281 views): handheld bootcamp shots, cooking, TV showing the iQOO BGIS overlays, "OVERALL TEAM STANDINGS" and "TOP 5 PLAYERS" |
| Life-story documentary | A seated interview shoot (2 cameras), an interview with a teacher (English subtitles), archive stream and emulator clips, a newspaper clipping, title cards | [9vzttojcMwA](https://www.youtube.com/watch?v=9vzttojcMwA) (2,273 s, 1,336,197 views, 5,600 comments) |
| Watch party (stream) | The official broadcast co-streamed with his small facecam | [ASbJkj4MQFc](https://www.youtube.com/watch?v=ASbJkj4MQFc) whole-stream timeline: BMSD broadcast full frame (pre-show, matches, standings, awards) with his cam bottom-left; full-screen facecam at the very end. The captions are mostly the official Hindi casting |
| Sponsored stream | His stream of a sponsor's game | "60 minutes. Unlimited chaos. One mission: WIN." (3,930 s, 11 Nov 2026), description "Download now: konami.jp/… Custom Tournament grind, Sunil Chhetri in the squad" ([Lrn1dFRc0Rk](https://www.youtube.com/watch?v=Lrn1dFRc0Rk)) |
| Old 2021 "Recorded Match" | Despite the title, his stream with overlay and facecam | [fEnBP236x7Q](https://www.youtube.com/watch?v=fEnBP236x7Q): LOLZZZ bar, facecam, a "ROAD TO TOP 10" card |
| 2020 Shorts | His stream (facecam present) | [Css0AXuRBZQ](https://www.youtube.com/shorts/Css0AXuRBZQ): vertical stack, gameplay crop over facecam |

- He describes his own long-run routine in the documentary: "abhi ek stream karta hoon aur subah main highlights wagairah daalunga" (stream at night, highlights the next morning) — [9vzttojcMwA](https://www.youtube.com/watch?v=9vzttojcMwA) captions 32:00
- For vlogs he says they will be "ekdam raw vlog… ye mat socho ki main efforts dunga" and that shoot days come first ("do-teen din shoot day hai… edit hoga, aa jayega") — [-vMIYNYkLAA](https://www.youtube.com/watch?v=-vMIYNYkLAA) 4:00-4:20

### Inferences
- **(I) The share of highlights built from more than one POV is high.** Of 9 non-record gameplay highlights sampled from 2025-2026, 5 use a teammate's stream: [fCCQkW1Uevk](https://www.youtube.com/watch?v=fCCQkW1Uevk), [T4D5femzSco](https://www.youtube.com/watch?v=T4D5femzSco), [PtvEiSN48Dk](https://www.youtube.com/watch?v=PtvEiSN48Dk), [RsiHZgsCMtw](https://www.youtube.com/watch?v=RsiHZgsCMtw) and [69AEExuBZfU](https://www.youtube.com/watch?v=69AEExuBZfU). The other four are [lOAtTbOsCzQ](https://www.youtube.com/watch?v=lOAtTbOsCzQ), [cLVYuMe5LJk](https://www.youtube.com/watch?v=cLVYuMe5LJk), [tEK_UYkgVmE](https://www.youtube.com/watch?v=tEK_UYkgVmE) and [nucVWiaxxVg](https://www.youtube.com/watch?v=nucVWiaxxVg). Plays' [3i83F-jSotA](https://www.youtube.com/watch?v=3i83F-jSotA) also uses a teammate's stream. Collabs are cut as **two-camera edits** by syncing two streams of the same session.
- **(I) The editor treats the stream VOD library as stock.** Compilations, "bonus matches" and journeys pull from any day, and the subscriber counter shows they are not in time order.
- **(I) Tournament highlights cannot come from his stream** (no overlay, no facecam in BGIS POV). They come from a device recording made during the match, probably for anti-cheat/POV purposes or by the team, plus the official broadcast.

### Gaps
- Which Kick streams feed which highlights could not be checked: Kick VODs were not fetched, and no outside source confirmed his Kick channel URL. Two web searches found no news of a LoLzZz Kick deal. The only Kick-and-BGMI news found was Kick's exclusive streaming rights for BGMI Masters Series Season 5 ([NODWIN/Kick](https://businessnewsthisweek.com/business/nodwin-gaming-awards-exclusive-digital-streaming-rights-for-bgmi-masters-series-season-5-to-global-streaming-giant-kick/)). The Kick evidence here rests on his own stream talk and his overlay logo.
- Who records the BGIS POV (the team, the organiser, a phone screen recorder) is not stated.
- Who edits is not stated anywhere public. Thumbnails carry a small "rex" designer watermark (deep study), and stream thumbnails carry an "apex" mark from his team (Team Apex Gaming, "TAG", since the 29 Jun 2026 stream [sOuXq86Gzdc](https://www.youtube.com/watch?v=sOuXq86Gzdc)).

## 3. How each type is made: structure, editing devices, layout and length

### Takeaway
All stream-based gameplay edits share one grammar:
- a **cold open of 30-60 s**: black → facecam (often black-and-white or blurred) → teaser shots → stylised graphic → black;
- the match(es) **in order on the unchanged stream layout**;
- **garnish every 1-2 minutes**: meme cutaways with name labels, full-screen facecam punch-ins, black-and-white facecam with a subtitle-style joke caption, colour bars and whips;
- an **ending on proof** (WWCD, MVP, results table, a "VICTORY" screen), then the facecam, then 5-10 s of black.

This study corrects the earlier "no match cards" finding. Every **multi-match** video uses plain white-on-black cards ("MATCH 2", "MATCH 3", "MATCH 7", "BONUS MATCHES"). Compilations put a Hinglish joke caption on a black card between clips. Multi-POV collabs cross-cut two streams and once use a side-by-side split. Sponsored, tournament, story and brand videos use completely different, shoot-based grammars.

### Cited Findings
**Editing devices seen across the 37 sampled storyboards** (counts are videos where the device was seen; timestamps are examples):
- **Cold open with black, facecam and teasers:** all stream-based edits.
  - Stylised graphics in the open: a fire/eye graphic and a neon-glasses logo at 0:09-0:39 ([lOAtTbOsCzQ](https://www.youtube.com/watch?v=lOAtTbOsCzQ)).
  - An animated "BEST MATCH OF CONQUEROR RANK PUSH" intro card in 2021 ([fEnBP236x7Q](https://www.youtube.com/watch?v=fEnBP236x7Q) 0:09-0:19).
  - A fast clip montage in the BGIS open ([cLVYuMe5LJk](https://www.youtube.com/watch?v=cLVYuMe5LJk) 0:09-1:09).
- **Text cards between matches** (white text on black, about 5 s):
  - "MATCH 2" ([fCCQkW1Uevk](https://www.youtube.com/watch?v=fCCQkW1Uevk) 9:04);
  - "MATCH 2"/"MATCH 3" ([cLVYuMe5LJk](https://www.youtube.com/watch?v=cLVYuMe5LJk) 7:25, 14:21);
  - "MATCH 7" ([HaDSOnXriO0](https://www.youtube.com/watch?v=HaDSOnXriO0) 17:57);
  - "BONUS MATCHES" ([lOAtTbOsCzQ](https://www.youtube.com/watch?v=lOAtTbOsCzQ) 9:02).
  - Single-match records have none (deep study).
- **Joke caption cards in compilations** (black cards with one Hinglish line before each clip): "ESE HI NAHI MILA LOLIYA KO CLASSIC HACKER KA TAG" 0:34, "EK GAADI ME JAA RAHE THE BANDE 3" 1:33, "AAKHIR ME BACHI THI MATR 4 GOLI" 2:08, "EK NADE SE FODE 3 BANDE" 4:06, "CLUTCH NO.7 MATLAB THALA FOR A REASON" 4:40, "AB DEKHO LOLIYA KA SABSE INTENSE CLUTCH" 6:09 — [tEK_UYkgVmE](https://www.youtube.com/watch?v=tEK_UYkgVmE)
- **Labelled meme cutaways** (film/TV/news clips with name tags):
  - "LoLzZz / ALOK" 0:49 and "JONNY / LoLzZz" 10:23 ([PtvEiSN48Dk](https://www.youtube.com/watch?v=PtvEiSN48Dk));
  - "UDA HUA BANDA AND HIS TEAMMATES" 2:53, "LALU BHAI" 3:38 ([nucVWiaxxVg](https://www.youtube.com/watch?v=nucVWiaxxVg));
  - "LoLzZz / T2" 4:36 ([tEK_UYkgVmE](https://www.youtube.com/watch?v=tEK_UYkgVmE));
  - "ZGOD:" 5:36 ([RsiHZgsCMtw](https://www.youtube.com/watch?v=RsiHZgsCMtw));
  - "KRAFTON" crash screen and "Mayur Bhai:" ([z1jXPJN8z-c](https://www.youtube.com/watch?v=z1jXPJN8z-c) 3:01, 5:04);
  - unlabelled film memes in the record, crate, sponsored and story videos.
- **Black-and-white facecam with a subtitle caption** (a comedic "inner voice"):
  - "BANDI NE 20000 KA CHUNA LAGAKAR KAAT DIYA" ([PtvEiSN48Dk](https://www.youtube.com/watch?v=PtvEiSN48Dk) 7:35);
  - "CRUSH KO BESTFRIEND KE SATH MERI BURAI KARTE DEKH LIYA" ([nucVWiaxxVg](https://www.youtube.com/watch?v=nucVWiaxxVg) 8:50);
  - "KHUD KO KHUD HI AASHVAASAN DENA SEEKH GAYA HU" and "JINDAGI ME KHUSHIYA MAANGI THI…" ([z1jXPJN8z-c](https://www.youtube.com/watch?v=z1jXPJN8z-c) 3:31, 4:39);
  - "SUBAH SE EK KNOCK KIYA THA VO BHI JONNY LE GAYA" ([T4D5femzSco](https://www.youtube.com/watch?v=T4D5femzSco) 5:34).
- **Full-screen facecam punch-ins** of him and teammates: every stream-based edit; in collabs, the other creator's cam too ([fCCQkW1Uevk](https://www.youtube.com/watch?v=fCCQkW1Uevk) 0:09-0:29 and 8:35-8:45).
- **Cross-cutting two streams** on alternate fights: [fCCQkW1Uevk](https://www.youtube.com/watch?v=fCCQkW1Uevk), [PtvEiSN48Dk](https://www.youtube.com/watch?v=PtvEiSN48Dk), [RsiHZgsCMtw](https://www.youtube.com/watch?v=RsiHZgsCMtw). A side-by-side split screen: [PtvEiSN48Dk](https://www.youtube.com/watch?v=PtvEiSN48Dk) 16:40-17:09.
- **TV colour bars**: [z1jXPJN8z-c](https://www.youtube.com/watch?v=z1jXPJN8z-c) 4:30 (also the 61-kill and 100-in-3 videos, deep study).
- **Other inserts.**
  - An Instagram reel of his own: "LOLZZZ INSTAGRAM REEL" ([PtvEiSN48Dk](https://www.youtube.com/watch?v=PtvEiSN48Dk) 8:25).
  - A news/TV clip: [lOAtTbOsCzQ](https://www.youtube.com/watch?v=lOAtTbOsCzQ) 2:18.
- **Proof endings.**
  - WWCD → MVP → facecam celebration ([C1RNs4p8uJg](https://www.youtube.com/watch?v=C1RNs4p8uJg) 14:14-15:03).
  - The trophy/trident "Trial of Fury" cinematic and WWCD after each match ([HaDSOnXriO0](https://www.youtube.com/watch?v=HaDSOnXriO0)).
  - The TDM "VICTORY" table ([PtvEiSN48Dk](https://www.youtube.com/watch?v=PtvEiSN48Dk) 24:55).
  - The results table plus "MATCH 2" ([fCCQkW1Uevk](https://www.youtube.com/watch?v=fCCQkW1Uevk) 8:55-9:04).
- **No added kill counter** in any edit. The one counter seen is part of the **stream overlay** (the damage counter in [C1RNs4p8uJg](https://www.youtube.com/watch?v=C1RNs4p8uJg)).

**Minute-by-minute: "WE ARE READY FOR PMGC | BGMI SCRIMS HIGHLIGHT"** ([fCCQkW1Uevk](https://www.youtube.com/watch?v=fCCQkW1Uevk), 1,179 s, 441,248 views, 18 Jul 2026 12:27; heatmap peak 543 s = 46%):
- 0:00 black.
- 0:09-0:29 facecam reactions: a teammate, LoLzZz, a teammate.
- 0:39-0:59 drop map "Novorepnoye" and a parachute (his POV).
- 1:09-1:29 Jonathan's POV (JONATHAN bar), then back to his POV at 1:39.
- 2:08-8:25 match 1 in about 10-40 s alternations between the two POVs, with sniper-scope shots at 2:48, 3:47, 5:17 and 7:25.
- 8:35-8:45 facecams (LoLzZz in a brown tee, the teammate stands up).
- 8:55 results table.
- 9:04 **"MATCH 2"** card.
- 9:14-18:49 match 2 on a desert map, again cross-cut, with facecam at 11:43, 13:12 and 17:50.
- 18:59-19:09 the teammate's facecam (relief).
- 19:19 lobby/map frame; end about 19:39.

**Minute-by-minute: "THIS IS HOW CLASSIC HACKER PLAYS IN ULTIMATE ROYALE"** ([lOAtTbOsCzQ](https://www.youtube.com/watch?v=lOAtTbOsCzQ), 1,183 s, 257,835 views, 17 Sep 2026; heatmap peaks 379 s (32%), 793 s, 616 s):
- 0:00 black.
- 0:09 a fire/eye graphic; 0:19-0:29 blurred facecam; 0:39 a neon glasses logo.
- 0:49 parachute into the UR match.
- 1:48 facecam punch-in.
- 2:18 a meme cutaway (TV interview clip with a "LOLZZZ" mic flag).
- 2:27-8:42 fights in time order on the stream layout (counter 2,765,5xx), facecam at 5:45 and 8:52 with the counter visible.
- 9:02 **"BONUS MATCHES"** card.
- 9:12-19:13 school-building fights from an earlier stretch (counter 2,765,499 → 2,765,477), facecam at 15:06 and 16:35.
- 19:23 squad end screen (counter 2,765,817); black from 19:33.

**Minute-by-minute: "INTENSE 1v1 AGAINST @JONATHANGAMINGYT"** ([PtvEiSN48Dk](https://www.youtube.com/watch?v=PtvEiSN48Dk), 1,515 s, 1,572,738 views, 30 Jan 2025; the heatmap's single strong peak is at 1,045 s = 69%, value 1.0, with the next at 0.46):
- 0:00 black.
- 0:09-0:19 teaser from Jonathan's POV; 0:29 his facecam.
- 0:39 a meme montage; 0:49 a "LoLzZz / ALOK" labelled meme.
- 0:59-1:09 his POV; 1:19-1:29 Jonathan's facecam laughing.
- 1:39-8:15 the TDM rounds in a warehouse map, cross-cut between the two POVs every 10-30 s, with facecam inserts at 2:08, 3:47, 5:16, 5:46 and 6:16.
- 7:35 B/W facecam with the subtitle joke.
- 8:25 his Instagram-reel insert.
- 8:34-17:09 a rooftop map. 10:23 a "JONNY / LoLzZz" meme; 10:53 B/W facecam; 11:33 and 12:22 Jonathan's facecam.
- 16:40-17:09 side-by-side split of both POVs at the decisive round, then 17:19-17:29 Jonathan's facecam reaction (the heatmap peak at 17:25).
- 17:39-24:45 a third map/round set; facecam at 18:19, 20:08, 21:17, 22:16, 24:05 and 24:35.
- 24:55 "VICTORY" table; 25:05 end.

**Minute-by-minute: "I GOT 4 MUMMY SET IN 16K UC | LUCKIEST CRATE OPENING"** ([z1jXPJN8z-c](https://www.youtube.com/watch?v=z1jXPJN8z-c), 496 s, 686,004 views, 3 Jul 2024; heatmap peak 372 s = 75%):
- 0:00 black.
- 0:04-0:14 facecam smiling, the purchase screen.
- 0:19 "YOU GOT" gun reveal.
- 0:29-1:52 crate spins and "YOU GOT" screens alternating with costume previews.
- 2:02-2:07 meme cutaways (fire, film).
- 2:17-3:16 more spins; 3:01 a "KRAFTON:" labelled film meme.
- 3:31 B/W facecam with a subtitle.
- 3:36-4:25 empty-looking "YOU GOT" screens (bad luck).
- 4:30 colour bars.
- 4:39 B/W facecam with a "JINDAGI ME KHUSHIYA…" subtitle.
- 5:04-5:09 "Mayur Bhai:" B/W with a subtitle; 5:14-5:19 a KRAFTON loading screen (a game restart).
- 5:38-6:08 film memes (celebration, SRK), the "Advanced Supplies" win.
- 6:13-7:17 costume and gun upgrade screens (the heatmap peak).
- 7:21 "LEVEL UP", the gun lab.
- 7:31-7:46 showing the outfits in the lobby (Paytm/G-Pay overlay visible).
- 7:56-8:11 the next match starts; end.

**Minute-by-minute: "From Zero to 2 Million: A Story of Struggles, Success & Inspiration"** ([9vzttojcMwA](https://www.youtube.com/watch?v=9vzttojcMwA), 2,273 s, 1,336,197 views, 128,640 likes, 5,600 comments, 28 Oct 2024 21:00; heatmap peaks 1,591 s, 636 s, 1,500 s):
- 0:00 black.
- 0:09 an old 2019 webcam clip in a rounded frame.
- 0:19-0:39 an interview shot (beige jumper, sofa, trophies, two camera angles).
- 0:49-1:19 dark title sequence: "BECAME", a crowd, "THE STORY OF LoLzZz GAMING".
- 1:29-5:47 interview with archive inserts (1:49-1:59 recent stream clips with overlay, 2:09 an old stream cam, 3:48 a hospital drip, 4:27 an aerial of his hometown).
- 5:57-6:46 interview with a teacher, with English subtitles ("teaching in St. Xavier's School…", "a YouTuber as LoLzZz Gaming").
- 8:55 an emulator-era clip; 9:15 a newspaper clipping; 9:45 handwriting.
- 10:55-11:14 a dark B-roll interlude.
- 12:14-12:44 screenshots of old social posts dated "18-03-201…".
- 13:53-14:53 old setup photos ("MARCH 2019").
- 15:52-19:41 interview cut with old PUBG emulator streams (facecam inset, subscriber counts 32-33K and 174K).
- The captions narrate the family car (31:00), not taking revenue for two years (29:20), streaming at night and posting highlights in the morning (32:00), and the first meetup in Vashi with 150-200 people (32:40).

**Minute-by-minute: "SING A SONG CHALLENGE ft Jonathan, Shreeman, Wolf"** ([T4D5femzSco](https://www.youtube.com/watch?v=T4D5femzSco), 556 s, 254,443 views, 6 May 2026; heatmap peak 428 s = 77%):
- 0:00-0:24 a cold open of four creators' facecams reacting (a stream cam, a studio cam, a phone-cam); 0:29-0:44 another creator's handcam view.
- 0:49-1:33 more cams; 0:54 a scope shot; 1:03 black.
- 1:48-1:58 B/W cam with "BHAU'S INNER VOICE:" labels.
- 2:03-3:26 gameplay on his stream (counter 2,614,1xx), cut with Shreeman's handcam.
- 3:41 "SHREEMAN BHAU:" meme; 4:30 a meme; 5:05 "WOLF MAHESHWARI:" meme; 5:34 a subtitle meme.
- 6:04 B/W death frame.
- 6:48 a political-rally meme.
- 6:53 a "#3" placement banner.
- 7:03-7:17 the next match.
- The title calls it "LOWEST KILL SINGING CHALLENGE" on the thumbnail: the lowest fragger sings.

**Other types in brief (from storyboards):**
- **Tournament POV (BGIS 2026)** [cLVYuMe5LJk](https://www.youtube.com/watch?v=cLVYuMe5LJk), 2,120 s:
  - Cold open 0:00-1:09: fast montage plus caster audio.
  - Then match 1 (about 1:09-7:15), "MATCH 2" 7:25, match 2 (7:35-14:11), "MATCH 3" 14:21, match 3 to the end.
  - Plain HUD, no facecam; each match is about 6-7 minutes of screen time.
  - Heatmap peak 1,400 s (66%).
- **Trial of Fury challenge** [HaDSOnXriO0](https://www.youtube.com/watch?v=HaDSOnXriO0), 1,167 s: 5+ matches, each ending on the trident cinematic and WWCD. A "MATCH 7" card at 17:57 brings in an earlier-counter segment. Facecam punch-ins every 2-4 minutes.
- **Records with an overlay counter** [C1RNs4p8uJg](https://www.youtube.com/watch?v=C1RNs4p8uJg): the same record grammar as the deep study's records. The heatmap peak is at 868 s (94%): the WWCD and MVP at the end.
- **Compilation** [tEK_UYkgVmE](https://www.youtube.com/watch?v=tEK_UYkgVmE), 557 s: 10 clips of about 30-60 s, each introduced by a black caption card, with labelled memes. It ends on a facecam outro at 8:42-9:07. The heatmap peak is at 33 s (6%), the first clip.
- **Sponsored phone video** [ML5Kk1ILBqE](https://www.youtube.com/watch?v=ML5Kk1ILBqE), 370 s:
  - A studio intro at 0:00-0:09 ("doston, aaj ka challenge hai 20 FINISHES on OPPO Reno13 Pro 5G").
  - Handcam B-roll 0:14-0:19, box shots with spec captions ("AI Adaptive Frame Stabilization").
  - Then the challenge match recorded on the phone (no stream bar), cut with studio reaction and "SUPERVOOC" callouts.
  - It ends on the box and his studio sign-off at 5:31-6:00.
  - [gaTQXGkRXnQ](https://www.youtube.com/watch?v=gaTQXGkRXnQ) (OPPO Reno14) and [ygTMhgAc9cA](https://www.youtube.com/watch?v=ygTMhgAc9cA) (OnePlus Nord CE5, plus CODM) follow the same pattern, adding meme cutaways and spec banners ("Mediatek Dimensity 8450", "1.47M+ AnTuTu").
- **Meetup vlog** [R6WKP31A_CY](https://www.youtube.com/watch?v=R6WKP31A_CY), 532 s: a crowd teaser (0:04-0:24), a selfie intro, a night drive, store chaos with balloons, a car selfie chat with friends, a café chat, a desk outro. The heatmap peak is at 106 s.
- **Brand game show** [7nWKQjWnLOA](https://www.youtube.com/watch?v=7nWKQjWnLOA), 1,196 s: a multicam studio, a host and the creators, round titles ("Combat & Cover"), leaderboard cards after each round, "Final Leaderboard" at 16:08. No heatmap; 42,004 views.

**Length rules by type** (measured):
- single-match record: 10-15 min (newest 22, median 779 s);
- multi-match challenge or tournament: 18-35 min (1,122-2,121 s);
- collab TDM/1v1: 8-25 min;
- crate opening: 7-9 min;
- compilation: about 9 min;
- sponsored: 6-10 min;
- vlog: about 9 min;
- story: 38 min.
- Sources: metadata above.

### Inferences
- **(I) The edit grammar is one house style applied to stream footage.** Whether the content is a record, a crate opening, a 1v1 or a compilation, the same devices recur: a black-led cold open, facecam punch-ins, B/W facecam plus a subtitle joke, labelled memes, colour bars, proof screen, black tail. This suggests one editor or team with a template; the identical thumbnail template across both channels points the same way.
- **(I) The edit rule for cards.** A card appears only when the video jumps to another match ("MATCH N", "BONUS MATCHES") or another clip (compilations). Inside one match the cut is hard, with no card.
- **(I) Two-POV collabs need sync.** The editor aligns two streams of the same lobby and alternates POV per fight, picking whichever player is in the action. Facecams of both creators are used as reaction shots.

### Gaps
- Overlays under about 5 s, sound effects and music cannot be seen or heard at storyboard resolution. The `[संगीत]` caption tags show music in cold opens and montage parts, as in the deep study.
- Only 6 of the new types got a minute-by-minute pass. The others were read at the level of structure.

## 4. The live streams themselves: schedule, length, what happens, overlays, how goals are stated

### Takeaway
In 2026 he streams almost daily:
- **79 of 103 exactly-timed 2026 streams started at 21:00-21:59 IST** (median start 21:20), and 75 of 102 gaps between streams were one day;
- gameplay streams last about 5-7 hours and end around 02:00-04:00;
- watch parties start at 13:00-16:00 and follow the esports calendar.

The goal is stated three times: in the **title**, in the **LIVE thumbnail**, and in his **first 5-15 minutes** of talk. The opening 15-18 minutes are talk before the first match: greetings, an apology for being late, the day's target, schedule announcements, a like goal and membership plugs.

The overlay is constant: a bottom bar with sponsor logos (KICK, iQOO, AMD Ryzen), a payment number, the LoLzZz wordmark, a live subscriber counter, and a small facecam bottom-left. Monetisation talk is dominated by **channel memberships**, not Super Chats.

From late September 2026 he alternates days between YouTube and **Kick**, which explains the drop from 28 YouTube streams in August to 15 in September.

### Cited Findings
- **Start times, 2026 (103 exact):**
  - 21:xx ×79, 20:xx ×4, 19:xx ×2, 13:00-17:00 ×18 (mostly watch parties).
  - Days are spread evenly (Mon 19, Fri 16, Sat 16, Thu 14, Wed 13, Sun 13, Tue 12).
  - Gaps between streams: 1 day ×75, 2 days ×18, 3 days ×6, 7 days ×1, same day ×2.
  - Watch-party starts: 13:18-16:10 (BMSD 8-11 Oct, PMWC 7-16 Aug, BMPS 19-21 Jun).
  - Source: `release_timestamp` of each stream, e.g. [hNCb6AT6dwc](https://www.youtube.com/watch?v=hNCb6AT6dwc), [wq2fjFmms1U](https://www.youtube.com/watch?v=wq2fjFmms1U).
- **History of start times:**
  - 2019-2021: either about 12:20-13:10 or about 20:05-20:35 (e.g. 12:41 [QdwgjXMAgZU](https://www.youtube.com/watch?v=QdwgjXMAgZU), 20:06 [e3L3MlVNTWA](https://www.youtube.com/watch?v=e3L3MlVNTWA)).
  - From 2022 it settles at 21:04-21:31 ([QUZqlUUKnew](https://www.youtube.com/watch?v=QUZqlUUKnew) 21:04; [uD-6jmsmJeg](https://www.youtube.com/watch?v=uD-6jmsmJeg) 21:31).
  - Source: sampled metadata.
- **2026 YouTube stream counts (exact from June):** 7-30 Jun 22; Jul 24; Aug 28; Sep 15; Oct about 20; 1-11 Nov 7.
- **Kick alternation.** On 8 Sep he said: "22 September Kick download kar lo… YouTube plus Kick ye dono ko parallely kaise chala payenge… schedule… management se aayega", and later "week me saat din, usme se ek din proper Kick hoga, chhe din YouTube… us din every time kuch giveaways honge… dopahar ko kabhi-kabhi live rahega… PC games" ([-vMIYNYkLAA](https://www.youtube.com/watch?v=-vMIYNYkLAA) 4:40-5:00, 4:44:00-4:44:40). By 26 Oct: "ek din YouTube ek din Kick" ([w1NB9sVC8k0](https://www.youtube.com/watch?v=w1NB9sVC8k0) 2:00).
- **What happens in a gameplay stream**, from captions of "AAJ 70 SOLO KILLS HOKE RAHENGE" ([wq2fjFmms1U](https://www.youtube.com/watch?v=wq2fjFmms1U), 24 Oct 2026, 5.5 h):
  - 0:40-1:20 greetings and "sorry, late ho gaya";
  - 1:20 "aaj apna target aapko pata hi hai, 70 solo kills";
  - 1:40-2:20 gym and personal chat;
  - 2:40-3:20 "limit khatam kare? 4-5 baje tak non-stop";
  - 3:40-7:20 watch-party plans and schedule;
  - 5:00 "2000 like pe apna aaj ka karyakram shuru hoga";
  - 10:00-10:40 announces his Ahmedabad meetup on the 31st;
  - 11:00-11:40 a bet with his squad ("70 kill… dance party hogi");
  - 12:40-16:20 a long free-membership redemption plug;
  - squad joins about 7:40 ("Titu bhi aa gaya… Mayur bhai");
  - first match about 16:40.
  - The match he set the record in ran 1:49:10-2:14:44 (deep study).
  - Last 3 minutes: "time to go… free membership le lo… kal apan Kick pe live aayenge… Bigg Boss ki permission…".
- **Talk density in that stream** (caption keyword hits per hour, hours 1-6):
  - "membership" 17 / 8 / 9 / 1 / 0 / 4 (39 total);
  - "like" 25 total;
  - "subscribe" 15;
  - spoken kill counts ("N kill") 38;
  - "Super Chat" 1;
  - rupee/donation words 5;
  - "Kick" 5.
  - The plugs bunch in the first three hours.
  - Source: [wq2fjFmms1U](https://www.youtube.com/watch?v=wq2fjFmms1U) captions.
- **Whole-stream timeline, "70K UC CRATE OPENING | ZOMBIES ARE BACK!"** ([w1NB9sVC8k0](https://www.youtube.com/watch?v=w1NB9sVC8k0), 6.6 h, 968,623 views; one frame a minute):
  - 0:00-0:04 full-screen facecam talk;
  - lobby and inventory;
  - about 0:47-1:05 a block of crate/inventory screens (the announced opening);
  - then about 5.5 h of continuous matches with WWCD screens about every 40-60 minutes;
  - occasional full-screen facecam (about 1:37);
  - full-screen facecam again at the very end (about 6:30).
  - The captions open the same way: "we are back… subah ki flight… shoot tha… stream Kick pe hi hai… zombies ka comeback… 50 kill possible… 60000 UC me nikal to jayega".
- **Whole-stream timeline, watch party** ([ASbJkj4MQFc](https://www.youtube.com/watch?v=ASbJkj4MQFc), 5.1 h, 1.9M views):
  - the official BMSD broadcast full frame from the show open, with team intros, matches, "Race to Smash" standings, the awards ceremony and the trophy;
  - his small facecam bottom-left throughout;
  - a full-screen facecam goodbye in the last minutes;
  - the captions are mostly the official casters.
- **Overlay:** a bottom bar with **KICK** · payment number (Paytm/G-Pay) · **LoLzZz** wordmark · **iQOO 15R** · **AMD Ryzen AI**; facecam bottom-left with an Indian flag and the **live subscriber count**. Some challenges add a live counter: "DAMAGE COUNTER" in [C1RNs4p8uJg](https://www.youtube.com/watch?v=C1RNs4p8uJg). Sources: storyboards of [wq2fjFmms1U](https://www.youtube.com/watch?v=wq2fjFmms1U), [z1jXPJN8z-c](https://www.youtube.com/watch?v=z1jXPJN8z-c).
- **Stream titles state the goal** as a question or a vow:
  - "70 SOLO KILLS POSSIBLE??", "#1 OR NOTHING", "AAJ CONQUEROR HOKE RAHEGA", "Rs 5,00,000 CHALLENGE FOR #1", "PER CHICKEN 5000 CHALLENGE", "STREAMING TILL I REACH CONQUEROR".
  - Then " | CLASSIC HACKER OR WHAT | BGMI LIVE | @LoLzZzGaming".
  - Event hooks: crate openings, a new update, "BIRTHDAY STREAM", "MARATHON STREAM".
  - Source: [streams tab](https://www.youtube.com/@LoLzZzGaming/streams).
- **Stream thumbnails** (8 inspected) are a template:
  - a red "● LIVE" badge, an "apex" team mark, his studio photo (white tee, glasses, often "shh");
  - the goal in huge yellow and white condensed italics ("70 SOLO KILLS POSSIBLE??", "GRAND FINAL WATCH PARTY", "ULTIMATE SET CRATE OPENING", "#1 OR NOTHING" with an in-game rank card, "Rs 5,00,000 CHALLENGE FOR #1").
  - Source: [wq2fjFmms1U](https://i.ytimg.com/vi/wq2fjFmms1U/hqdefault.jpg), [ASbJkj4MQFc](https://i.ytimg.com/vi/ASbJkj4MQFc/hqdefault.jpg), [Pf34L2Z2H7s](https://i.ytimg.com/vi/Pf34L2Z2H7s/hqdefault.jpg)
- **Stream descriptions and tags are empty** (wq2fjFmms1U: description "", tags []). Category Gaming; no chapters — [wq2fjFmms1U metadata](https://www.youtube.com/watch?v=wq2fjFmms1U)
- **Older monetisation:**
  - 2019-2021 titles end "PAYTM ON SCREEN", "DONATION(S) ON SCREEN", "!D for Discord", "5 RP GIVEAWAY ON LOCO" ([BQL63wRqs_s](https://www.youtube.com/watch?v=BQL63wRqs_s), [pxQEercMuEc](https://www.youtube.com/watch?v=pxQEercMuEc)).
  - 15 members-only streams (6 in 2025), e.g. "MEMBERS ONLY RANK PUSH" and "HANDCAM STREAM FOR MEMBERS" ([streams tab](https://www.youtube.com/@LoLzZzGaming/streams)).
  - The 8 Sep 2026 stream counts "300 membership already aa chuki hai" after a viewer gifted many ([-vMIYNYkLAA](https://www.youtube.com/watch?v=-vMIYNYkLAA) 4:59:00).

### Inferences
- **(I) The stream has a reliable shape:** about 15 min of talk, then 4-6 h of back-to-back matches (lobby → plane → match → WWCD or death → lobby, about 25-30 min each, so about 10-14 matches), then a 2-5 min goodbye.
  - The goal line is in the first 15 minutes, which is exactly where the record videos' cold opens get their "target" line.
  - Donation and membership reads sit mostly in lobbies, which the edit removes; the one exception kept was a donation read that set the stakes (the 61-kill video).
- **(I) Kick changes the input for an automatic tool.** On Kick days there is no YouTube VOD, so a creator like him needs Kaatclip to accept a local OBS recording or a Kick VOD, not only a YouTube link.

### Gaps
- Super Chat amounts, live chat, and chat replay were not fetched.
- Number of matches per stream was inferred from the WWCD rate on one timeline and the 25-30 min match length, not counted per stream.
- Kick stream times, lengths and viewership are unknown.

## 5. Titles, thumbnails, descriptions, tags, playlists, end screens, upload timing per type, and what performs best

### Takeaway
Packaging effort goes almost entirely into the **title and thumbnail**, from one shared template:
- his studio photo, a huge yellow/white condensed-italic headline, emoji, and one proof element (gameplay frame, rank card, donation card, product).

The rest is light:
- **descriptions** are empty or just an Instagram link and hashtags, except for brand deals, which carry disclosures and product copy;
- **tags** are missing or 4-6 generic words;
- **playlists** are abandoned;
- **no chapters**.

Highlights go up at **12:00 IST** the next day. Brand and story pieces go up at other times (12:30-21:00). The biggest performers per item are **collabs with Jonathan (TDM/1v1)**, the **life story**, **new personal-best records** and **watch-party streams**. Brand pieces are the weakest (median 88K).

### Cited Findings
- **Title templates by type:**
  - Record: "I MADE A (NEW) WORLD RECORD OF N SOLO KILLS (IN mode/update) | CLASSIC HACKER OR WHAT / TAG LoLzZz OR WHAT" ([-qpx-ejuq9Q](https://www.youtube.com/watch?v=-qpx-ejuq9Q)).
  - Multi-match: "THIS IS HOW CLASSIC HACKER PLAYS IN ULTIMATE ROYALE | BGMI HIGHLIGHT" ([lOAtTbOsCzQ](https://www.youtube.com/watch?v=lOAtTbOsCzQ)).
  - Tournament: "THIS IS HOW TLG QUALIFIED FOR ROUND 4 | BGIS 2026 HIGHLIGHT", "THIS MATCH QUALIFIED US TO BGIS ROUND 3😱" ([cLVYuMe5LJk](https://www.youtube.com/watch?v=cLVYuMe5LJk), [2bNv3hwSvAs](https://www.youtube.com/watch?v=2bNv3hwSvAs)).
  - Collab: "INTENSE 1v1 AGAINST @JONATHANGAMINGYT | LoLzZz VS JONATHAN | BGMI HIGHLIGHT" ([PtvEiSN48Dk](https://www.youtube.com/watch?v=PtvEiSN48Dk)).
  - Challenge: "THEY CHALLENGED CLASSIC HACKER TO REACH LEGEND & THIS HAPPEND!" ([RsiHZgsCMtw](https://www.youtube.com/watch?v=RsiHZgsCMtw)).
  - Crate: "I GOT 4 MUMMY SET IN 16K UC | LUCKIEST CRATE OPENING BY LoLzZz" ([z1jXPJN8z-c](https://www.youtube.com/watch?v=z1jXPJN8z-c)).
  - Brand: sentence case with the product name ("OPPO Reno13 Pro 5G – Ultra Smooth, Zero Lag! | 20 Finishes Challenge…", [ML5Kk1ILBqE](https://www.youtube.com/watch?v=ML5Kk1ILBqE); "1v4 turned into chaos real quick 😭 ft. GodLike Girls | New Phone", [gaTQXGkRXnQ](https://www.youtube.com/watch?v=gaTQXGkRXnQ)).
- **Thumbnails** (12 video thumbnails inspected in this study plus 8 in the deep study):
  - **Gameplay types** use his face (hands together pleading or "shh"), a big two-line headline in yellow over white, and a proof element:
    - Mummy-set costumes and gun for the crate video;
    - "TOP 10 CLUTCHES BY GODL LOLZZZ" with a "Remaining 2 Finished 40" HUD crop;
    - "COMPLETING 5 TIMES TRIAL FURY CHALLENGE IN ONE DAY" with the trophy screen;
    - "EXPOSED!! 60 SOLO KILLS?" with a handcam inset.
  - **Collabs** use split VS faces ("1V1 INTENSE BATTLE": red vs blue panels with name plates) or a group "shh" ("23 KILLS SCRIMS DOMINATION WITH TEAM APEX GAMING").
  - **BGIS:** "QUALIFIED FOR BGIS ROUND 4" with his player card ("TLGXLOLZZZ") and the India Series logo.
  - **Story:** "LOLZZZ GAMING: THE UNTOLD CHAPTERS" with old TVs "From Struggle" → "To Success".
  - **Vlog:** "AHMEDABAD MEETUP VLOG" over a crowd selfie.
  - **Sponsor:** "A STREAMERS DREAM LAPTOP?" with the product.
  - Source: [thumbnails](https://i.ytimg.com/vi/PtvEiSN48Dk/hqdefault.jpg), [9vzttojcMwA](https://i.ytimg.com/vi/9vzttojcMwA/hqdefault.jpg), [fCCQkW1Uevk](https://i.ytimg.com/vi/fCCQkW1Uevk/hqdefault.jpg).
- **Descriptions and tags (newest uploads):**
  - Empty description on 2026 records and on [lOAtTbOsCzQ](https://www.youtube.com/watch?v=lOAtTbOsCzQ) and [fCCQkW1Uevk](https://www.youtube.com/watch?v=fCCQkW1Uevk).
  - "#bgis #bgmi #lolzzz" on [cLVYuMe5LJk](https://www.youtube.com/watch?v=cLVYuMe5LJk).
  - An Instagram link plus 3 hashtags plus 4-6 tags on 2024-25 uploads (e.g. [z1jXPJN8z-c](https://www.youtube.com/watch?v=z1jXPJN8z-c): tags "set opening, bgmi, lolzz, lolz gaming, mummy set opening, crate opening").
  - **Brand videos carry long copy and disclosures**: "#Collaboration Made in collaboration with Lenovo & AMD…" ([s3ixZgYaDGs](https://www.youtube.com/watch?v=s3ixZgYaDGs)), Google Play tier copy ([7nWKQjWnLOA](https://www.youtube.com/watch?v=7nWKQjWnLOA)), Red Bull copy ([k7viYHrrVhg](https://www.youtube.com/watch?v=k7viYHrrVhg)).
  - The 2021-22 template was "Instagram… Discord… ⋙ Enjoyed the Highlights? Make sure You Like & Share" with 6 tags ([fEnBP236x7Q](https://www.youtube.com/watch?v=fEnBP236x7Q), [tjBXf-bRjxo](https://www.youtube.com/watch?v=tjBXf-bRjxo)).
  - No chapters on any of the 87 metadata items.
- **Playlists:** 8, all 2019-2021, not added to since (§1).
- **End screens:** stream-based edits end on 5-10 s of black or a dim frame:
  - [tEK_UYkgVmE](https://www.youtube.com/watch?v=tEK_UYkgVmE) 9:12, [nucVWiaxxVg](https://www.youtube.com/watch?v=nucVWiaxxVg), [lOAtTbOsCzQ](https://www.youtube.com/watch?v=lOAtTbOsCzQ) 19:33-19:43, [C1RNs4p8uJg](https://www.youtube.com/watch?v=C1RNs4p8uJg) 15:13, [R6WKP31A_CY](https://www.youtube.com/watch?v=R6WKP31A_CY) 8:47;
  - the records in the deep study too.
  - (I) This is the slot for YouTube end-screen elements, which yt-dlp cannot read.
- **Upload times (exact, 43 of the newest 52 with metadata):**
  - Non-brand edits: 12:00-12:51 in 29 of 37. The rest were 13:09-14:25 (5) and 20:51-21:17 (2 multi-day / compilation pieces).
  - Tournament POV: 12:11-13:38.
  - Brand: 12:30 (Lenovo/AMD), 13:59 (OPPO), 14:44 (OnePlus), 17:00 (Google Play), 17:39 (OPPO Reno14), 21:00 (Red Bull).
  - Story: 21:00 (28 Oct 2024).
  - Compilation: 21:17.
  - Source: per-video `timestamp` in §1 list.
- **Performance, newest 52** (median views by type, §1):
  - TDM/1v1 collabs 847K (max 1,572,738);
  - records 274K;
  - tournament POV 299K;
  - cash 272K;
  - squad/collab gameplay 254K;
  - multi-match journeys 224K;
  - compilations 185K;
  - brand pieces 88K.
- **All-time top long uploads:**
  - "Can i Defeat @JONATHAN GAMING in 1v1 TDM?" about 4.0M ([pnqQb35rwlE](https://www.youtube.com/watch?v=pnqQb35rwlE));
  - "How to get Demotivated in BGMI Ft. Jonathan | TDM" 1.9M ([cQRWK4Z0Yu8](https://www.youtube.com/watch?v=cQRWK4Z0Yu8));
  - "INTENSE 1v1 AGAINST JONATHAN" 1.57M;
  - "From Zero to 2 Million" 1.34M;
  - "1 Million Celebration with Godlike Bois" 1.2M ([QW96QQaILVc](https://www.youtube.com/watch?v=QW96QQaILVc));
  - BGIS BTS 1.07M;
  - "GODLIKE PREMIER LEAGUE BEFORE BGIS" 1.0M ([QzmmYtijyyA](https://www.youtube.com/watch?v=QzmmYtijyyA));
  - "INTENSE 2V2 TDM BATTLE PART 2" 1.0M ([UyTjzyo-y2A](https://www.youtube.com/watch?v=UyTjzyo-y2A));
  - 72 SOLO KILLS 990,648.
  - Source: [videos tab](https://www.youtube.com/@LoLzZzGaming/videos) (rounded listing views) and metadata.
- **Engagement:** the story video has 5,600 comments and 128,640 likes (9.6% like/view) — [9vzttojcMwA](https://www.youtube.com/watch?v=9vzttojcMwA). The Google Play brand show has 168 comments on 42,004 views — [7nWKQjWnLOA](https://www.youtube.com/watch?v=7nWKQjWnLOA).
- **Heatmap "most replayed" peaks by type** (position of the global maximum):
  - crate opening 75% (the big pull);
  - 1v1 69% (the split-screen decider);
  - scrims 46%;
  - BGIS 66%;
  - damage record 94% (WWCD/MVP);
  - sing-a-song 77%;
  - compilation 6% (the first clip);
  - OPPO sponsor 90%;
  - meetup vlog 20% (crowd arrival).
  - Source: yt-dlp `heatmap` of each linked video.

### Inferences
- **(I) What performs:** rivalry with a bigger creator (Jonathan, 7-8M subscribers) beats everything long-form. Then come personal milestones (a new personal-best record, the 2M story). Self-contained gameplay without a headline (compilations, UR multi-match) is mid-table, and brand content is lowest. In streams, watch parties of big esports finals draw 2-4 times a gameplay stream. They are also the content he cannot cut into highlights, because the footage is the organiser's broadcast.
- **(I) Brand deals buy a different, shoot-based video** (studio, handcam, spec banners) at about a third of a record's views. They are a revenue product, not an audience product.

### Gaps
- End-screen elements, cards, CTR, retention and traffic sources are private.
- The Community tab and Instagram cross-posting were not measured.

## 6. What this means for Kaatclip: which types it could make from a stream recording, the signals needed, and what is out of reach

### Takeaway
From one creator's own stream recording, Kaatclip can in principle make **six of his content types**:
1. the single-match record;
2. the multi-match / "bonus matches" session video;
3. the crate-opening video;
4. the "N in M matches" or cash challenge;
5. a clutch compilation across the creator's own past streams;
6. the record teaser Short.

It **cannot** make:
- multi-POV collabs (they need a teammate's stream);
- tournament POV (a different recording and the official broadcast);
- watch-party highlights (third-party broadcast rights);
- sponsored, story, vlog and brand videos (shoots, not streams).

Kick-only sessions need a local-file path. The house style can be approximated with rules, except the film/TV meme cutaways, which carry copyright risk.

### Cited Findings
- The evidence is in §2 (sources) and §3 (grammar). Representative cases:
  - own-stream records [-qpx-ejuq9Q](https://www.youtube.com/watch?v=-qpx-ejuq9Q) ← [wq2fjFmms1U](https://www.youtube.com/watch?v=wq2fjFmms1U);
  - multi-match [lOAtTbOsCzQ](https://www.youtube.com/watch?v=lOAtTbOsCzQ);
  - crate [z1jXPJN8z-c](https://www.youtube.com/watch?v=z1jXPJN8z-c);
  - compilation [tEK_UYkgVmE](https://www.youtube.com/watch?v=tEK_UYkgVmE);
  - two-POV [fCCQkW1Uevk](https://www.youtube.com/watch?v=fCCQkW1Uevk), [PtvEiSN48Dk](https://www.youtube.com/watch?v=PtvEiSN48Dk);
  - tournament [cLVYuMe5LJk](https://www.youtube.com/watch?v=cLVYuMe5LJk);
  - brand [ML5Kk1ILBqE](https://www.youtube.com/watch?v=ML5Kk1ILBqE), [7nWKQjWnLOA](https://www.youtube.com/watch?v=7nWKQjWnLOA);
  - story [9vzttojcMwA](https://www.youtube.com/watch?v=9vzttojcMwA);
  - watch party [ASbJkj4MQFc](https://www.youtube.com/watch?v=ASbJkj4MQFc).

### Inferences
**Feasibility by type (all (I)):**

| His content type | Kaatclip from own stream? | Signals needed | Notes |
|---|---|---|---|
| Single-match record (10-15 min) | **Yes** (core) | match boundaries incl. recall; HUD kill count and MVP OCR; fight windows; goal line from Hinglish ASR in the first 15 min; WWCD/MVP screens; facecam rectangle | Rules in the deep study §6 (keep ratio about 0.45, uneven by quarter; cold open from the goal line) |
| Multi-match session ("THIS IS HOW … PLAYS", "BONUS MATCHES") | **Yes** | per-match score (kills, WWCD, clutch count); choose the top 2-3 matches; "MATCH 2"/"BONUS MATCHES" cards | Cards are simple white-on-black text; the order can be by quality, not time |
| "N kills in M matches" / cash per kill / chicken streak | **Yes** | the goal from title and speech ("100 kill in 3 matches", "har kill pe 1000"); a running total across matches; the donation read (speech) | Use cards between matches; a per-match tally in the thumbnail |
| Crate opening (7-9 min) | **Yes**, if the stream has an opening | detect inventory/crate UI ("YOU GOT", "Congratulations", costume preview) by template or OCR; reaction peaks (loud audio, facecam motion) | Order: spins → bad-luck stretch → big pull at about 75% → show the outfit in the lobby → end as the next match starts |
| Clutch compilation (Top 10) | **Yes, across several of the creator's streams** | clutch detection (1vN: squad-mates dead plus kills), per-clip ranking; a caption card per clip | Needs a library of past recordings and a "best of N streams" mode |
| Record teaser Short (20-30 s) | **Yes** | from the highlight's end: final kills → WWCD → MVP number; a top caption; a "full video" end card | Matches the measured 72-kill Short (deep study) |
| "Exposed / handcam" drama | Partly | the gameplay part, yes; the framing ("exposed") is packaging | Title and thumbnail template only |
| Collab TDM/1v1, scrims with teammates, sing-a-song | **No** (only his own half) | would need the teammate's synced stream | Can make a one-POV version; the two-POV cross-cut is the hit format (847K median) and is out of reach without the other recording and permission |
| Official tournament POV (BGIS) | **No** | a clean device recording plus the official broadcast | Not in a stream recording; tournament rules often bar streaming |
| Watch-party highlights | **No** | the broadcast is the organiser's | Rights and Content ID risk; only his facecam reactions are his |
| Sponsored product videos, brand shows, vlogs, the life story | **No** | camera shoots, scripts, B-roll | Out of scope for a stream editor |
| Kick-day streams | Only via file upload | Kaatclip must take a local OBS/Kick file | The creator's YouTube VOD does not exist on Kick days |

**House-style rules an automatic editor can copy** (from the measurements):
1. Cold open of 30-60 s: black, then the facecam (optionally B/W) saying the goal, then 2-3 teaser shots, then a stylised title, then black.
2. Hard cuts inside a match; a white-on-black card only between matches or clips.
3. A full-screen facecam punch-in (crop of the facecam rectangle) after big moments, about every 1-2 minutes.
4. A B/W facecam with a subtitle line as the "inner voice" joke device. Kaatclip can generate this from the creator's own ASR line, with no third-party clip.
5. End on proof screens (WWCD, MVP, results, VICTORY), then the facecam, then 5-10 s of black for end screens.
6. Publish at 12:00 the next day; titles and thumbnails from the type templates in §5.

**Copyright line.** His labelled film, TV and news meme cutaways are the riskiest device. Kaatclip should offer creator-supplied or own-asset stickers and name labels instead.

**Signals Kaatclip does not yet have and would need for these types:**
- an inventory/crate UI detector;
- a multi-match goal tracker;
- a clutch (1vN) detector;
- a cross-stream library index for compilations;
- a "card" renderer;
- B/W facecam plus subtitle insert generation;
- an optional second-recording sync for collabs (later, with the partner's file).

### Gaps
- The feasibility judgements are inferences. None was tested on the owner's test streams.
- The two-POV sync (audio alignment of two recordings of one lobby) was not prototyped.
- Whether creators like LoLzZz would accept auto-made memes or B/W "inner voice" captions is untested.
- Sources for background facts used above: [Sportskeeda profile](https://www.sportskeeda.com/bgmi/lolzzz-gaming-s-bgmi-id-stats-rank-youtube-earnings) (real name Yash Thacker, from Bhuj, started on emulator) and [AFK Gaming](https://afkgaming.com/mobileesports/news/lolzzz-enters-the-top-10-most-watched-youtube-gaming-streamers-list) (most-watched YouTube streamer lists). These were search-result summaries, not read in full, so they are background only.
