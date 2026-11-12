# Joker Ki Haveli and JokerClips: how the comedy highlights are made, cut and uploaded (deep study)

Method (12 Nov 2026). Public YouTube data only, read with yt-dlp; no video or audio was downloaded. It extends `research_notes/BGMI highlight video structure/joker_comedy.md` and does not repeat it.
- **Full flat listings with approximate dates**:
  - main channel: 499 videos, 1,310 streams, 273 Shorts;
  - JokerClips: 659 videos and 152 Shorts. JokerClips has no streams tab.
- **Full metadata and Hindi auto-captions** (word-level timing) for:
  - 21 JokerClips highlights, 2023-2026;
  - 10 Shorts;
  - 36 of Joker's live streams (all BGMI and chat streams from 12 Jul to 16 Oct 2026, plus one from 8 Sep).
- **Storyboard preview frames**:
  - every ~4.9 s for 19 highlights;
  - every ~1 s for 9 Shorts;
  - every 10 s around selected stream moments.
- **Source mapping**: highlight captions were aligned to stream captions by matching 4-word sequences, then extended word by word at the same time offset. Six highlights were mapped. The overlay counters seen in the frames (a follower counter and a charity donation total, both only ever rising within a stream) were used to check the order.

Scripts and raw data are in `C:\Users\soura\AppData\Local\Temp\claude\21027423ba80eb72\ab9e7281-b606-4050-82cb-606e6c8ce9f9\scratchpad\yt_research\joker_deep\` (`fetch.py`, `cap.py`, `segtable.py`, `seg_*.txt`, `inventory.txt`, storyboard sheets in `sb\` and `sbr\`).

Measurement caveat: the "matched speech" spans below are where the auto-captions of highlight and stream agree word for word. The real clip edges are a few seconds wider. Parts with music, meme inserts or no speech cannot be matched by captions.

## 1. What the two channels upload and how they split the work

### Takeaway
The main channel (@Jokerkihavelii) is the live-stream and vlog channel: about 13-15 streams a month of 3-5 h each, plus a few vlogs. Every BGMI highlight lives on JokerClips (@jokerclipss). Since late 2023 JokerClips has posted a steady **8:00-8:10 "funny session highlight"** cut from those streams (median 488 s, 69 of 133 exactly 480-489 s), plus esports watch-party reactions, crate openings and "vs" challenges. Output has slowed to about 5-10 long videos a month in 2026. Views of the session format have fallen from a median of about 220K (2024-25) to 139K (Dec 2025 to Oct 2026), and the main co-star changed from Snax (2023-25) to Rega (2026).

### Cited Findings
**Main channel**
- **Streams tab:** 1,310 past streams, median 5 h (IQR 4-6 h).
  - Since Dec 2025 there have been 160 streams (about 14.5 a month), median 5 h, median 143K views.
  - Titles in that period: 87 mention BGMI, 18 GTA RP, 16 "Baat chit", 14 challenges, 13 crate openings, 13 watch parties, 10 IRL, 10 Meccha Chameleon and 5 Valorant.
  - Stream starts on the 36 dated streams fell between 19:56 and 22:19 IST (mostly 20:30-22:15).
  - Examples: [X_QBQqfO-9g](https://www.youtube.com/watch?v=X_QBQqfO-9g) (7 Sep 2026, 4.07 h), [nu0fl7M3v8A](https://www.youtube.com/watch?v=nu0fl7M3v8A) (Nepal charity stream, 31 Aug to 1 Sep 2026, 9.44 h, 584K views); full list via the [streams tab](https://www.youtube.com/@Jokerkihavelii/streams).
- **Typical stream mix:** one stream mixes games. "VALORANT INDIA NOW | BGMI DONE" means BGMI was played first. A sponsor banner (iQOO Z11) or a donation QR code with a running total sits on the layout. Each JokerClips highlight takes **one slice** of such a stream, for example the first 30-60 min of BGMI. — [X_QBQqfO-9g](https://www.youtube.com/watch?v=X_QBQqfO-9g), [4jHoA5A-Q7E](https://www.youtube.com/watch?v=4jHoA5A-Q7E)
- **Videos tab:** 499 videos, median 781 s, median 291K views. Only 37 have BGMI in the title (median 481 s, 157K). Since Dec 2025 it has had only about 1-7 uploads a month, mostly vlogs. — [videos tab](https://www.youtube.com/@Jokerkihavelii/videos)
- **Shorts tab:** 273 Shorts, dominated by lifestyle series: "Ramadan Routine Ft IND vs ENG" (52M), "My Daily Routine In London" (14M). Gaming Shorts are a minority. Examples: "Goldy Dada Gussa Ho Gaye 🤣" (40 s, 5.47M, 7 Jul 2025) and "International lobby 🥵🤯" (30 s, 444K, 9 Aug 2026). — [9gy3caHoOMs](https://www.youtube.com/shorts/9gy3caHoOMs), [PVmTr-gdojA](https://www.youtube.com/shorts/PVmTr-gdojA)

**JokerClips**
- **Size and mix:** 659 videos (median 248 s, median 96K views) and 152 Shorts. Categories by title keywords and length:

| Category | Count | Median length | Median views |
|---|---|---|---|
| BGMI funny session (420 s or more, not reaction, crate or challenge) | 133 | 488 s (IQR 482-506) | 185K |
| Short clips under 3 min | 177 | 70 s | 42K |
| Esports reactions and watch parties | 159 | 200 s | 72K |
| Vs and challenge | 83 | 481 s | 123K |
| Crate openings | 30 | 481 s | 114K |
| Other games (Meccha Chameleon, Chained Together) | 11 | n/a | 93K |
| IRL | 15 | n/a | 67K |

  — [JokerClips videos tab](https://www.youtube.com/@jokerclipss/videos)
- **Length histogram (420-720 s, 10 s bins):** 480-489 s has 111 videos, 490-499 s 37, 500-509 s 19, 510-519 s 15. Only 54 are 520-720 s, and none are 420-479 s. — same listing
- **History, by YouTube's "N years ago" buckets:**

| Bucket (approx.) | Uploads | Mostly | Session highlights | Their median views | All uploads, median views |
|---|---|---|---|---|---|
| About 2022 | 43 | Short clips and reactions | n/a | n/a | n/a |
| About 2023 | 279 | 168 clips under 3 min, 84 reactions | 1 | n/a | 48K |
| About 2024 | 141 | 8-minute sessions | 44 | 224K | n/a |
| About 2025 | 121 | 8-minute sessions | 53 | 211K | n/a |
| Dec 2025 to Oct 2026 | 75 (5-10 a month) | 8-minute sessions | 35 | 139K | 139K |

  Monthly counts for the last period: 7, 9, 7, 7, 5, 6, 5, 10, 8, 7, 4. — same listing
- **Co-stars named in titles:**

| Period | Videos | Most named |
|---|---|---|
| About 2023-2024 | 463 | Snax 91, SouL 47, Rega 36, Mavi 25, Scout 25, Goldy 23 |
| About 2025 | 121 | Snax 45, Goldy 25, SouL 19, Aman 16 |
| Dec 2025 to Oct 2026 | 75 | Rega 26, Krutika 9, SouL 6, Snax 5, Mazin, Sheek and Viper 3 each |

  — same listing
- **Top views on JokerClips:**
  - Formats other than session highlights: "Jonathan Raids Joker Again After 4 Years" (402 s, 1.4M); "Joker Reaction On Carryminati Collab…" (1,507 s, 1.4M); "JOKER SHOCKED BY GAMERFLEET NEW HOUSE" (1,388 s, 994K).
  - Session highlights: "Joker & Snax *TRIGGERED* Goldy Bhai" (482 s, 1.0M); "Joker SHOCKED by Pakistani Pro Player" (487 s, 933K); "Moye Moye In BGMI" (691 s, 762K).
  - Sources: [tt1gwGtxjlU](https://www.youtube.com/watch?v=tt1gwGtxjlU), [YI0ntgz9Y_o](https://www.youtube.com/watch?v=YI0ntgz9Y_o), [xlAtlvjotlE](https://www.youtube.com/watch?v=xlAtlvjotlE), [E6h-WNsY7jM](https://www.youtube.com/watch?v=E6h-WNsY7jM), [lyHdl-U4yNQ](https://www.youtube.com/watch?v=lyHdl-U4yNQ)

**Who runs JokerClips**
- Joker addresses his editor live on stream, and the editor uses those lines in the highlight:
  - "Editor, clipping ke liye ready ho ja. Tere ko highlight de raha hoon… bahut din se tu complaint kar raha tha highlight nahi aa rahi" (editor, get ready to clip; I'm giving you a highlight). This is the cold-open line of [Ul5mEjNyzu4](https://www.youtube.com/watch?v=Ul5mEjNyzu4) at 0:00 and is said again at 1:40.
  - He calls "Shabbir" into the room in the same video ("Shabbir kamre mein aao").
  - In [TIDXJ1YeirM](https://www.youtube.com/watch?v=TIDXJ1YeirM) at 1:30: "clip kaatna hai na aapko, starting wali kaat lo na" (you want to cut a clip; cut the starting one).
  - A 2025 title reads "Goldy Bhai Exposed Joker & His Editor😭" ([6slUusTfbH4](https://www.youtube.com/watch?v=6slUusTfbH4)).
  - Every description starts "Main Channel: https://youtube.com/@Jokerkihavelii".

### Inferences
- JokerClips is run by Joker's own in-house editor (possibly named Shabbir, which is unconfirmed), not by a third party. The streamer flags moments live, partly as a running joke.
- The split is: the main channel holds the raw streams and vlogs; JokerClips holds every edited BGMI highlight. Kaatclip's "post the highlight to a second channel" use case matches this real practice.
- Highlights get only about 1 in 2-3 streams' worth of material. With about 14 streams a month and 5-10 JokerClips uploads a month, many streams yield no highlight. Some streams yield two (see section 3).

### Gaps
- JokerClips' first upload date and total count beyond the 659 listed items are unknown. YouTube's "N years ago" dates make the yearly buckets approximate (±6 months).
- The editor's identity is not confirmed by any public source.

## 2. Anatomy and editing of the highlights (21 videos, 2023-2026)

### Takeaway
A JokerClips session highlight is about 8:00-8:10 of **gameplay with the stream's facecam, constantly zoomed and cut**. Talk and banter run nearly non-stop: 77-94% of seconds have speech, at 88-179 words a minute. The main devices are:
- a full-screen **facecam zoom-in** for every verbal punchline;
- **meme image or video inserts with one-word labels** ("JOKER", "CHAT", "Tiger", "Teammates");
- **burned-in subtitle lines** for the key quote;
- SpongeBob-style **"THE NEXT DAY…" / "2 SECONDS LATER…" cards**;
- since about Apr 2026, an **"IN THIS VIDEO" cold-open teaser of 10-22 s**.

There are no chapters. Ending styles vary: some videos stop mid-moment, some run 10-20 s of "SUBSCRIBE" end screen, and two 2026 videos tack on an unrelated IRL or vlog clip.

### Cited Findings
**Caption metrics** (speech = share of seconds with a captioned word within ±1.5 s, a stricter measure than the earlier note's 95-100%; teaser = number of 4-word phrases from the first 20 s that recur after 30 s; heatmap = YouTube "most replayed" top bin)

| Upload | Video | Length | Views | Speech | wpm | Laugh tags | Teaser repeats | Top replay (s) |
|---|---|---|---|---|---|---|---|---|
| 21 Dec 2023 | [E6h-WNsY7jM](https://www.youtube.com/watch?v=E6h-WNsY7jM) TRIGGERED Goldy | 481 | 1.06M | 0.86 | 119 | 0 | 1 | 294 |
| 22 Feb 2024 | [SyOwtmHTAfQ](https://www.youtube.com/watch?v=SyOwtmHTAfQ) Snax rank push | 401 | 496K | 0.81 | 100 | 1 | 0 | 192 |
| 24 Feb 2024 | [Fn9HwxPd89k](https://www.youtube.com/watch?v=Fn9HwxPd89k) SNIPING | 612 | 718K | 0.87 | 145 | 0 | 0 | 0 |
| 4 Apr 2024 | [G4dIkpIpLOw](https://www.youtube.com/watch?v=G4dIkpIpLOw) Rega chaotic duo | 480 | 363K | 0.77 | 90 | 0 | 0 | 456 |
| 10 May 2024 | [Bt9V4vDhH30](https://www.youtube.com/watch?v=Bt9V4vDhH30) Naughty duo | 514 | 330K | 0.69 | 88 | 0 | 0 | 77 |
| 1 Sep 2024 | [lKRhsBLUHtg](https://www.youtube.com/watch?v=lKRhsBLUHtg) Trolled by Scout Snax Mavi | 487 | 338K | 0.87 | 121 | 0 | 0 | 209 |
| 29 Jun 2025 | [u3y_yfkkej4](https://www.youtube.com/watch?v=u3y_yfkkej4) Never-ending kalesh | 495 | 350K | 0.82 | 123 | 0 | 0 | 267 |
| 5 Aug 2025 | [h8UUyyKQMcY](https://www.youtube.com/watch?v=h8UUyyKQMcY) Suk Rosemary | 480 | 326K | 0.85 | 127 | 0 | 0 | 355 |
| 11 Aug 2025 | [C9pvcRmEGYE](https://www.youtube.com/watch?v=C9pvcRmEGYE) Reply on Snax roasting | 482 | 574K | 0.94 | 179 | 0 | 0 | 255 |
| 24 Aug 2025 | [kl9ibgyjlt4](https://www.youtube.com/watch?v=kl9ibgyjlt4) Goldy defends Joker | 480 | 352K | 0.83 | 120 | 0 | 13 | 432 |
| 5 Sep 2025 | [rpbg7zhuZXE](https://www.youtube.com/watch?v=rpbg7zhuZXE) 2v2 AKM power | 633 | 722K | 0.88 | 153 | 0 | 3 | 151 |
| 10 Mar 2026 | [AKw_7q-I8lA](https://www.youtube.com/watch?v=AKw_7q-I8lA) Snax triggered by mic spam | 482 | 258K | 0.79 | 117 | 3 | 0 | 236 |
| 25 Apr 2026 | [DQNn8LYVdEs](https://www.youtube.com/watch?v=DQNn8LYVdEs) Joker being Joker for 8 min | 481 | 140K | 0.77 | 92 | 0 | 10 | 81 |
| 14 May 2026 | [y52CMXbQ0IE](https://www.youtube.com/watch?v=y52CMXbQ0IE) Manya joins | 482 | 187K | 0.80 | 124 | 5 | 51 | 448 |
| 5 Aug 2026 | [VSK7Q7FH5rk](https://www.youtube.com/watch?v=VSK7Q7FH5rk) Spider-Man mode | 510 | 196K | 0.85 | 113 | 5 | 0 | 367 |
| 5 Sep 2026 | [8Au8-kSBhgg](https://www.youtube.com/watch?v=8Au8-kSBhgg) Joker vs Goblin reflex | 488 | 337K | 0.85 | 120 | 8 | 30 | 317 |
| 11 Sep 2026 | [TIDXJ1YeirM](https://www.youtube.com/watch?v=TIDXJ1YeirM) Gun Game duo | 492 | 170K | 0.84 | 121 | 9 | 0 | 330 |
| 16 Sep 2026 | [Ul5mEjNyzu4](https://www.youtube.com/watch?v=Ul5mEjNyzu4) Gameplay 0% | 497 | 201K | 0.81 | 102 | 11 | 20 | 333 |
| 24 Sep 2026 | [3c0nLXL8k6U](https://www.youtube.com/watch?v=3c0nLXL8k6U) Rega chaotic duo back | 480 | 213K | 0.93 | 154 | 3 | 20 | 418 |
| 5 Oct 2026 | [TZCVFWl7NtM](https://www.youtube.com/watch?v=TZCVFWl7NtM) Crate opening w/ Mazin | 481 | 147K | 0.84 | 113 | 8 | 26 | no heatmap |

**What the storyboards show** (a strip of the first 35 s and the last 20 s of 18 highlights was compared side by side)

*Cold open*
- An "IN THIS VIDEO" label (white italic, top left) sits over 10-22 s of quick teaser cuts. It appears in [E6h-WNsY7jM](https://www.youtube.com/watch?v=E6h-WNsY7jM) (Dec 2023, the channel's top video) and then not again until [DQNn8LYVdEs](https://www.youtube.com/watch?v=DQNn8LYVdEs) (Apr 2026).
- It is present in [y52CMXbQ0IE](https://www.youtube.com/watch?v=y52CMXbQ0IE), [8Au8-kSBhgg](https://www.youtube.com/watch?v=8Au8-kSBhgg), [Ul5mEjNyzu4](https://www.youtube.com/watch?v=Ul5mEjNyzu4), [3c0nLXL8k6U](https://www.youtube.com/watch?v=3c0nLXL8k6U) and [TZCVFWl7NtM](https://www.youtube.com/watch?v=TZCVFWl7NtM).
- It is absent in all 2024-2025 videos and in the single-match videos [VSK7Q7FH5rk](https://www.youtube.com/watch?v=VSK7Q7FH5rk) and [TIDXJ1YeirM](https://www.youtube.com/watch?v=TIDXJ1YeirM). The caption "teaser repeats" column agrees.
- In Apr-May 2026 the teaser shots were shrunk into a black frame (boxed). From Sep 2026 they are full-frame or slightly desaturated, with burned-in subtitles ("Usdin lolzzz ka bhi call aaya tha", "Zindagi teri kharab h").

*Without a cold open*
- 2024-2025 videos open straight on a moment: zoomed facecam reacting ([G4dIkpIpLOw](https://www.youtube.com/watch?v=G4dIkpIpLOw)), a lobby ([rpbg7zhuZXE](https://www.youtube.com/watch?v=rpbg7zhuZXE)), or mid-action ([u3y_yfkkej4](https://www.youtube.com/watch?v=u3y_yfkkej4)).
- In 2024 [Fn9HwxPd89k](https://www.youtube.com/watch?v=Fn9HwxPd89k) opened on Joker browsing to Snax's live stream; its top replay bin is 0-6 s.

*Base layout*
- The stream layout is shown as is: game feed full frame, Joker's facecam bottom right, and a bottom-left "JOKER" mascot banner with a live follower counter. The counter read 722K in Apr 2024, 1.02M in Jun 2025, 1.09M in Sep 2025, 1.56M in Apr 2026 and 2.25-2.30M in Aug-Sep 2026.
- Sponsor overlays (iQOO Z11 bar) and charity QR codes stay in.

*Facecam zoom*
- Talk moments cut to the facecam region scaled up to full frame. Part of the green or gameplay edge of the layout stays visible at the left, so it is a crop-zoom, not a separate camera.
- With a co-streamer on call, the zoom becomes **two webcams side by side** (Rega left, Joker right; [3c0nLXL8k6U](https://www.youtube.com/watch?v=3c0nLXL8k6U) 3:20-6:00).
- About 25-45% of storyboard frames in the 2026 videos are such zooms.

*Other creators' footage*
- Cuts to the co-streamer's own stream POV ("REGALTOS" overlay, 3c0n 5:37-5:42).
- Side-by-side split of two players' POV and cam ([Ul5mEjNyzu4](https://www.youtube.com/watch?v=Ul5mEjNyzu4) 1:03-1:43).
- Full-screen cut-ins of a friend's webcam (Goldy and others, in [u3y_yfkkej4](https://www.youtube.com/watch?v=u3y_yfkkej4) 0:24 and [8Au8-kSBhgg](https://www.youtube.com/watch?v=8Au8-kSBhgg) 0:44).

*Meme inserts*
- 1-3 s Bollywood or news clips with a white bold one-word label naming who it stands for: "Joker", "Chat", "Tiger" (3c0n 0:39, 0:58, 1:42); "JOKER / CHAT" (8Au8 0:59); "Teammates" (Ul5m 0:34).
- Others: a Modi speech (G4dI 0:44), Rajpal Yadav's face (Ul5m 1:58), a "REC" camcorder frame (Ul5m 6:58), a "Wasted" card (VSK7 end).
- Typically 3-6 per video.

*Text*
- Burned-in subtitles of the key line, either white sentence-case at the bottom ("Gym waale bande se diet plan maang liya", 3c0n 0:14-0:29) or caps meme captions at the top ("YE DANCE WALA KISNE MAARA JOKER BHAI SACH BATANA", G4dI 0:24; "LEKIN BGMI DHOKA NAHI DEGA", Fn9H 1:13).
- Sticker-style callout boxes ("Galti se Division A ka baccha Division D me aagya💀", 8Au8 0:24).
- In-video title cards ("Joker Vs Goblin's Reflex", 8Au8 4:36).
- Labels "*EXPECTATION*" and "*IRL*" (Fn9H 0:54-0:59), "Hector in chat" with a face sticker (3c0n 0:04, 4:09), "Goblin will Donate 10k 🥹" (8Au8 2:52).

*Time cards*
- Full-screen SpongeBob-style title cards: "THE NEXT DAY…" (3c0n 2:56, 8Au8 5:00, Ul5m about 5:30) and "2 SECONDS LATER…" (Ul5m 6:43). The earlier note also heard "one hour later" in 2023.
- Each card is 4-6 s long.

*Other effects*
- Black-and-white freeze frames for mock drama (G4dI 0:58, u3y_ 1:33).
- Letterboxed "cinematic" facecam with caption "Motivation Lelo Guys" (8Au8 3:27).
- The scope view zoomed for snipes.
- Results and MVP screens kept: "#3 congratulations" (G4dI 2:36), "#8 You made the Top 10" (Ul5m 3:31), "VICTORY" (TIDX 7:22), "MVP" (8Au8 4:55).

*Endings*
- "SUBSCRIBE" black end screen of 10-20 s in E6h, G4dI, C9pv and DQNn.
- Abrupt stop on a facecam reaction or gameplay in u3y_, h8UU, rpbg, 8Au8 and TIDX.
- An unrelated IRL clip as the last 49 s in [3c0nLXL8k6U](https://www.youtube.com/watch?v=3c0nLXL8k6U) (7:11-8:00, Joker spilling Red Bull into a protein shaker at an event) and a party or dance clip at the end of [TZCVFWl7NtM](https://www.youtube.com/watch?v=TZCVFWl7NtM).
- The last heatmap bin is near zero in every video with a heatmap.

**Minute-by-minute: [3c0nLXL8k6U](https://www.youtube.com/watch?v=3c0nLXL8k6U) "Joker Rega THE CHAOTIC DUO Back" (480 s, 24 Sep 2026)**

| Time | What is on screen | Funny moment (setup, then punchline) | Type, length, laugh |
|---|---|---|---|
| 0:00-0:13 | "IN THIS VIDEO" teaser, 3 cuts, subtitles | Lines from 0:30, 5:35 and 4:11 | Teaser |
| 0:14-0:40 | Zoomed facecam (white shirt), subtitle "Gym waale bande se diet plan maang liya" | Asked a gym guy for a diet plan, then the list "salad aur fish… chicken… mutton… sugar cut sodium low" | Roast or banter in the lobby, about 25 s, no laugh tag |
| 0:39-1:10 | Meme "Joker"; lobby; meme "Chat" (woman laughing) | Brag "daily 50-50 finishes… Lolzzz ne call kiya mat maro", then a teammate laughs and Joker: "hasta kyon hai… main comedy karne aata hoon kya" | Boast deflated by laughter, about 25 s |
| 1:10-1:52 | Facecam; meme "Tiger" (police clip) at 1:42 | Running "tambaku doctor" roast of Tiger (overcharges, extra tablets), then "Shabbir bhai ki gaaf mein foda" [laughter] | Roast monologue, about 40 s, laugh |
| 2:02-2:51 | Gameplay fight, follower counter rising 2,292,066 to 2,292,231 | "kitne maaru?" kill-count bickering, then "all dead" | Fight with trash talk, about 45 s |
| 2:56-3:00 | "THE NEXT DAY…" card | n/a | Card |
| 3:00-3:17 | Gameplay: drop and death (counter 2,285,789) | "neeche koodo, gun leke", he dies, then "mera naseeb kharab hai, gameplay to yun hi badnaam hai" | Death, then self-deprecation, about 17 s |
| 3:17-3:40 | Two webcams side by side | "GG", then the roast "Zomato wala ban ja / labour banunga / Raju mistri" | Death, then teammate career roast, about 21 s |
| 3:47-4:11 | Side by side | "aisa content banate ho ki editor bhi edit nahi kar paate… chaar editor bhaag gaye" | Self-referential roast, about 20 s |
| 4:11-4:36 | "Hector in chat" sticker | Chat member gets teased ("Hector yahi to maar kha rahe ho"); Nebula esports bragging | Chat interaction, about 25 s |
| 4:40-4:55 | Gameplay knock calls | "ek knock hai…", then "khud mar jaate ho… clutch bhi dekh liya karo" | Knock, then blame, about 15 s |
| 4:56-5:41 | Side by side, Rega POV at 5:37 | Rega's 45 s roast of Joker (gym, Bigg Boss, "10 din ki roti"), ending "zindagi teri kharab hai, kama bhi tu hi raha hai" | Long roast monologue, 45 s |
| 5:52-6:17 | Facecam | "game tu hagega… kal se BGMI nahi aayega", then "duniya zaalim hai tere pe" / "main zaalim hoon" chant (the thumbnail line) | Argument escalating into a chant, about 25 s |
| 6:17-6:35 | Gameplay | "lag ho raha hai… koi hacker aaya hai kya" | Absurd game situation, about 15 s |
| 6:41-7:06 | Gameplay to facecam | "bandook chheen", then "baap re kahan daal diya bhai" [laughter] | Chaos, then group laugh, about 25 s, **top replay 408-423 s** |
| 7:11-8:00 | IRL clip at an event (sunglasses, crowd) | Red Bull in a protein shaker spills: "are maa ki gir gayi… carbonated hai" | IRL mishap as a tacked-on ending, 49 s |

**Minute-by-minute: [8Au8-kSBhgg](https://www.youtube.com/watch?v=8Au8-kSBhgg) "JOKER VS GOBLIN REFLEX" (488 s, 5 Sep 2026)**

| Time | Screen | Moment | Type |
|---|---|---|---|
| 0:00-0:22 | "IN THIS VIDEO": lobby with QR code and donation bar (₹3,45,352), plane, facecam | Teaser lines "miss kiya ki nahi tumhare bhai ko", "ye Owais tumko barbaad kar dega" | Teaser |
| 0:24-0:59 | Gameplay; white sticker caption "Galti se Division A ka baccha Division D me aagya💀"; a guest webcam cut-in at 0:44 | A pro player lands in their casual charity lobby | Caption framing a situation |
| 0:59-1:28 | Meme "JOKER / CHAT"; gameplay | Joker trolls an enemy pro on voice ("Scary Jord sun, ye Owais tumko barbaad kar dega"), then roasts a "destroyed player… LAN pe khelne ka sapna" | Trolling opponents, about 30 s |
| 1:30-1:40 | Gameplay | He gets knocked: "mere ko hi utaar diya… main player ko" | Knock, then indignation, about 10 s, **replay 0.9 at 92 s** |
| 1:40-2:30 | Facecam zoom; subtitle "Thunder bhi khelte hai" | Fake casting of SouL's POV ("toh nunu kaun hai… to Joker kya hai?") | Commentary parody, about 50 s |
| 2:32-2:57 | Facecam; "Goblin will Donate 10k 🥹" text | "decorate kar diya panda ko" [laughter]; Goblin pledges ₹10,000 to Nepal | Charity moment plus a joke, about 25 s |
| 3:00-3:31 | Gameplay; letterboxed facecam "Motivation Lelo Guys" | A lucky shot: "tukka… naya content creation start kiya hai, motivation de do" | Sarcasm, about 30 s |
| 3:36-4:10 | Gameplay | "paani mein info do" repeated about 10 times, then "mere ko jala kyon raha hai" (burned by his own team's molotov) | Repetition gag, then friendly fire, about 35 s |
| 4:10-4:58 | Ban warning pop-ups ("purposefully teamed"); title card "Joker Vs Goblin's Reflex"; scope; MVP screen | A 1v1 reflex face-off and the game's teaming warning | Skill moment plus absurd warning, about 45 s |
| 5:00-5:05 | "THE NEXT DAY…" card | n/a | Card |
| 5:05-5:45 | "Pothead ❌ Rebel ✅" label over a browser game; phone call | Mocks Rebel's game, Willy on call about rank push ("1200 rank… alag duniya hai") | Call banter, **replay 1.0 at 317 s** |
| 5:45-6:50 | BGMI lobby | "Erika" joins via team code ("Joker bhai bhool gaye aap?"); "naya mode aa gaya… ye Honor of Kings hai, sorry" | Lobby banter and fake-out, replay 0.7-0.83 at 381-400 s |
| 6:50-8:03 | TDM fight; facecam | "badla loonga… hum to mar ke bhi jeete hain", then "main streamer hoon bhai, meri izzat karo, mere ko gun do" | Death, then indignation; ends on facecam, no card |

**Minute-by-minute: [Ul5mEjNyzu4](https://www.youtube.com/watch?v=Ul5mEjNyzu4) "JOKER's Gameplay 0% BAKC**DI 100%" (497 s, 16 Sep 2026)**

| Time | Screen | Moment | Type |
|---|---|---|---|
| 0:00-0:12 | "IN THIS VIDEO" | "Editor, clipping ke liye ready ho ja…", "tum hamari gaon mein ghus jaate ho" | Teaser |
| 0:14-0:50 | Car chase, Spider-Man mode, QR code; meme "Teammates" at 0:34 | "tag waale maar liye"; "main gaali nahi de sakta, family dekhti hai"; nearly knocked: "bach gaya" | Near-death plus self-censorship, about 35 s |
| 1:00-1:43 | **Split screen**: Joker's POV and a friend's POV and cam | Spider-Man swinging; calls the editor Shabbir into the room: "ye match puri highlight hai" | Meta joke plus mode novelty, about 45 s |
| 1:43-2:57 | Facecam; Rajpal Yadav meme; drop and fight | "gun nahi hai to kyon kooda… ye pehle karne ka tha… mar gaya" | Death, then blame, about 60 s |
| 2:57-3:51 | Recall screen; "#8 You made the Top 10" rank screen | "recall ho jaana chahiye" | Recall begging, about 20 s |
| 3:56-4:45 | New match | "esports bana diya saalon ne… humaari ghaas mein ghus jaate ho"; sings "chal nikal" after each kill | Complaining about pros, then song taunts, about 50 s |
| 4:50-5:30 | Podcast-clip inset; squad wipe | "Eliminator hai Joker bhai… salaam walekum" | Kill streak plus a stock reaction, about 40 s |
| about 5:30 | "THE NEXT DAY…" | n/a | Card |
| 5:35-6:43 | iQOO Z11 banner stream | "I am noob and proved"; "hacker hoga" | Self-deprecation, hacker suspicion, **replay 1.0 at 333 s** |
| 6:43-6:48 | "2 SECONDS LATER…" card | n/a | Card |
| 6:48-7:45 | Camp found; "REC" meme | "camp nikaal diya"; roasts the enemy team's player ("usko Nutella chatao, shahad do") | Trolling opponents, about 55 s |
| 7:45-8:17 | Gameplay | "kya banda hai… mere saath kyon khelta hai… kabhi kabhi rona aa jaata hai" | Mock self-pity punchline; abrupt end |

**Minute-by-minute: [TIDXJ1YeirM](https://www.youtube.com/watch?v=TIDXJ1YeirM) "JOKER & REGA ULTIMATE DUO In BGMI Gun Game" (492 s, 11 Sep 2026)**

| Time | Screen | Moment | Type |
|---|---|---|---|
| 0:00-1:30 | Straight in at "Match starts in 5 seconds"; one Gun Game match on the Library map; counter rising 2,285,690 to 2,285,697 | "latak ji / jhatak ji" nickname bit; "inki guddi laal karna"; "jiggle hai kya" | Banter during fights; no teaser |
| 1:30-2:45 | Facecam zooms at 0:34, 1:53 and 2:03 | "clip kaatna hai na aapko, starting wali kaat lo"; "Salman Khan ji ko main aa raha hoon"; "chup chup… bahut buri awaaz hai" | Meta joke and teasing |
| 2:45-3:45 | Subtitle "Logo ko head dete hue dekha h" (3:26) | A chat question "aap head kaise maar dete ho", then "maine bahut logon ko head dete hue dekha" | Chat question, then a double-entendre punchline |
| 3:45-5:30 | Fights; laugh at 4:15 and 5:05 | "kha kha kha kha… ke aa raha hoon" [laughter]; "dono bhi nahi maar paaye" [laughter] | Repetition gag; a fail with a laugh; replay peak at 330 s |
| 5:30-7:22 | Crossbow fights; VICTORY screen at 7:22 | "crossbow reload kaise aa gaya"; "kutton ko baandh ke rakhna chahiye" | Absurd weapon moment; win |
| 7:27-8:11 | Lobby chat from **earlier** in the stream (counter 2,285,616-621, lower than the match) | "Is saal maine Scout ko bhijwaya hai (Bigg Boss)… Big Sister" | Tacked-on chat bit as the ending |

**Speakers.** In all four, the voices are Joker, his on-call co-streamer (Rega in 3c0n and TIDX), 1-2 more squad members, and occasionally a donation or chat line read aloud. The best-replayed bits are a teammate's roast or a group laugh, not Joker's solo play. This is inferred from caption content; auto-captions do not mark speakers.

### Inferences
- **Mix of moments** across the about 55 moments classified above:
  - banter, roasts and arguments with no game trigger: about 40%;
  - a death or knock followed by blame or self-deprecation: about 20%;
  - trolling opponents or pros: about 10%;
  - absurd game situations (hacker, lag, friendly fire, new mode, ban warning): about 10%;
  - chat, donation and meta-editor jokes: about 10%;
  - skill or win screens: about 10%.
  These shares are rough counts.
- **Unit length:** 15-60 s, median about 25-30 s, including setup.
- **Edit density:** in the 2026 videos, a visual change (zoom in or out, meme, card, subtitle) happens roughly every 5-10 s, because the storyboard frame differs at nearly every 4.9 s tile. Kaatclip's comedy output therefore needs automatic zoom-to-facecam on speech peaks and occasional labelled reaction inserts. Plain gameplay alone would look nothing like this.
- **Two production modes exist:**
  - **Single-match mode**: one continuous match, few edits, no teaser, a results screen near the end (TIDX, VSK7, rpbg).
  - **Compilation mode**: 2 streams, a teaser and time cards (3c0n, 8Au8, Ul5m, TZCV).

### Gaps
- Exact on-screen times of each zoom or meme (±5 s, the storyboard step) and any sound effects cannot be measured without the video.
- Music use is known only from caption [संगीत] tags (0-6 per video).
- Who speaks each line is inferred from content, since auto-captions carry no speaker labels.
- Moments inside music or no-speech stretches were not classified.

## 3. Source mapping: which stream segments go into a highlight

### Takeaway
Six highlights were mapped to their source streams. Four findings stand out:
- An 8-minute highlight draws on **30-160 minutes of one stream** (once only 17 min, when a single match was kept almost whole). It does **not** draw on the whole 4-9 h stream.
- **Compilations join two different streams**, and the "THE NEXT DAY" card often jumps **backwards** in time.
- Within one stream the order is **mostly chronological**: 93 forward jumps against 11 backward, and the backward ones are the teaser, an ending bit or a local swap.
- Kept speech units are short (median matched span 13 s; IQR 7-19 s). The stream gap between consecutive kept units is a median 64 s (IQR 16-416 s).

Highlights go up **4-6 days** after the stream. Leftover material from older streams appears **2-3 weeks** later in two-stream compilations.

### Cited Findings
**A. [TZCVFWl7NtM](https://www.youtube.com/watch?v=TZCVFWl7NtM) Crate opening with Mazin & Shinchan (481 s, 5 Oct 2026). Source: [JcPWCyVw8f8](https://www.youtube.com/watch?v=JcPWCyVw8f8) "120000 UC CRATE OPENING | BACK FROM JAPAN" (30 Sep 2026, 3.25 h).** Delay 5 days.

| # | Highlight | Stream | Matched length | Stream gap since previous |
|---|---|---|---|---|
| 0 | 0:00-0:05 (teaser) | 0:16:02 | 6 s | n/a |
| 1-2 | 0:18-0:50 | 0:15:53-0:16:36 | 29 s | +15 s |
| 3-5 | 0:53-1:30 | 0:22:47-0:23:51 | 35 s | +371 s, then +7 and +14 s |
| 6-9 | 1:32-3:07 | 0:37:55-0:40:01 | 76 s | +844 s, then +14, +14, +20 s |
| 10-11 | 3:33-4:33 | 0:40:33-0:42:18 | 58 s | +32 s, +46 s |
| 12-14 | 4:34-5:24 | 0:54:06-0:58:35 | 41 s | +708 s, +210 s, +15 s |
| 15 | 5:32-5:43 | 1:29:14 | 11 s | +1,839 s |
| 16 | 6:32-6:47 | 1:52:06 | 16 s | +1,359 s |
| 17 | 6:55-6:59 | 2:36:12 | 4 s | +2,630 s |
| 18 | 7:33-7:38 | 2:51:37 | 5 s | +922 s |

- 19 matched units. Span used: 0:15:53-2:51:42 (156 min of a 195-min stream). 281 s of 481 s matched.
- Fully chronological except the teaser. Density thins sharply after the first hour: 6:00 of the video covers 0:16-0:58, and the last 2 minutes cover 1:29-2:51.

**B. [8Au8-kSBhgg](https://www.youtube.com/watch?v=8Au8-kSBhgg) Joker vs Goblin Reflex (488 s, 5 Sep 2026). Part 1 (0:00-5:00) source: [nu0fl7M3v8A](https://www.youtube.com/watch?v=nu0fl7M3v8A) Nepal charity stream (31 Aug 2026, 9.44 h).** Delay about 5 days.

| Highlight | Stream | Notes |
|---|---|---|
| 0:00-0:18 | 3:49:09, 3:08:08, 3:15:58 | Teaser, 3 lines of about 4 s each |
| 1:00-1:28 | 3:08:06-3:08:49 | Two units, 18 s and 12 s |
| 1:30-2:27 | 3:15:27-3:18:47 | 5 units of 4-19 s; one local swap (3:20:49 placed before 3:17:31) |
| 2:32-2:58 | 3:27:07-3:50:25 | Three units |
| 3:20-3:27 | 3:56:22 | 7 s |
| 3:51-4:38 | 4:33:42-4:35:22 | Three units (18, 10, 5 s); one 48 s swap |
| 4:57-5:04 | 4:36:11 | 7 s, just before the "THE NEXT DAY" card |

- Span 3:08-4:36: **88 minutes became about 4.5 minutes** (about 5%).
- The donation total on screen rises steadily: ₹2,89,752 at 0:24, ₹3,14,041, ₹3,22,880, ₹3,46,799 and ₹3,50,392 at 4:55. That confirms the order.
- Part 2 (5:05-8:03, after "THE NEXT DAY") matched none of the 36 fetched streams (13 Jul to 16 Oct 2026). **Uncertain**: possibly a stream not checked, such as an Aug 2026 watch party, or footage from another creator.

**C. [Ul5mEjNyzu4](https://www.youtube.com/watch?v=Ul5mEjNyzu4) Gameplay 0% (497 s, 16 Sep 2026). Sources: [z7DJeIR7z90](https://www.youtube.com/watch?v=z7DJeIR7z90) (2 Sep, 4.52 h) and [4jHoA5A-Q7E](https://www.youtube.com/watch?v=4jHoA5A-Q7E) (27 Aug, 5.0 h).**

| Highlight | Stream | Order |
|---|---|---|
| 0:12-0:30 | z7DJ 0:32:44 | n/a |
| 0:36-0:50 | z7DJ 1:57:21 | Forward |
| 1:00-1:40 | z7DJ 2:08:22-2:09:02 | Forward (Spider-Man match) |
| 1:40-4:20 | No caption match | Gameplay and rank screen; the counter (2,254,409-2,254,446) is below the 0:39 frame's 2,254,585, so it is earlier in the same stream |
| 4:20-4:44 | z7DJ 1:11:18 | **Backward** |
| 5:12-5:26 | z7DJ 1:20:56 | Forward |
| "THE NEXT DAY" | n/a | Card |
| 5:39-8:09 | 4jHoA 1:27:45, 1:43:53-1:47:03, 1:57:53, 2:34:06-2:35:05, 3:42:59-3:43:19 | All forward; "2 SECONDS LATER" card at 6:43 |

- The **later** stream (2 Sep) comes first. Its Spider-Man match (from about 2 h in) is put first as the hook. The earlier match of the same stream (about 1:11) follows.
- The second part, after "THE NEXT DAY", is from **five days earlier** (27 Aug).
- Spans used: z7DJ 0:32-2:09 (96 min) and 4jHoA 1:27-3:43 (136 min). Upload delay 14 and 20 days.

**D. [3c0nLXL8k6U](https://www.youtube.com/watch?v=3c0nLXL8k6U) Rega Chaotic Duo Back (480 s, 24 Sep 2026). Sources: [2z0aPlOy9yg](https://www.youtube.com/watch?v=2z0aPlOy9yg) "PLAYING VALORANT INDIA" (8 Sep, 3.36 h) and [X_QBQqfO-9g](https://www.youtube.com/watch?v=X_QBQqfO-9g) "VALORANT INDIA NOW | BGMI DONE" (7 Sep, 4.07 h).**

| # | Highlight | Stream | Matched length | Gap |
|---|---|---|---|---|
| 0 | 0:00-0:03 (teaser) | 2z0a 0:11:12 | 4 s | n/a |
| 1 | 0:14-0:24 | 2z0a 0:02:08 | 10 s | Back |
| 2-3 | 0:26-0:40 | 2z0a 0:11:05-0:11:37 | 14 s | +528 s |
| 4-5 | 0:42-1:09 | 2z0a 0:13:50-0:14:23 | 30 s | +133 s |
| 6 | 1:12-1:44 | 2z0a 0:15:08-0:15:43 | 32 s | +45 s |
| 7 | 1:48-2:01 | 2z0a 0:16:00 | 13 s | +17 s |
| 8 | 2:10-2:30 | 2z0a 0:19:32 | 21 s | +199 s |
| 9 | 2:45-2:58 | 2z0a 0:33:19 | 13 s | +807 s |
| card | 2:56 "THE NEXT DAY" | n/a | n/a | **Goes back one day** |
| 10-11 | 3:00-3:17 | X_QBQ 0:45:38-0:45:58 | 18 s | n/a |
| 12 | 3:17-3:38 | 0:50:06 | 21 s | +248 s |
| 13-15 | 3:47-4:11 | 0:54:30-0:55:56 | 22 s | +243 s, +62 s |
| 16 | 4:13-4:36 | 1:02:52 | 23 s | +416 s |
| 17 | 4:40-4:55 | 1:04:46 | 16 s | +90 s |
| 18 | 4:56-5:41 | 1:08:40-1:09:25 | **46 s** | +214 s |
| 19-22 | 5:52-6:30 | 1:09:45-1:11:28 | 36 s | +20, +45, +17, +4 s |
| 23 | 6:41 | 1:35:49 | 2 s | +1,461 s |
| 24 | 6:59-7:11 | 1:17:37 | 12 s | **Back** |
| tail | 7:11-8:00 | Unmatched IRL clip | 49 s | n/a |

- Spans used: 31 min of the 8 Sep stream (its first 33 min, the chat and BGMI part) and 50 min of the 7 Sep stream (0:45-1:35). 340 s of 480 s matched.
- The follower counter confirms it: 2,292,0xx in part 1 against 2,285,8xx in part 2. Part 2 is the earlier stream.

**E. [TIDXJ1YeirM](https://www.youtube.com/watch?v=TIDXJ1YeirM) Gun Game duo (492 s, 11 Sep 2026). Source: [X_QBQqfO-9g](https://www.youtube.com/watch?v=X_QBQqfO-9g) (7 Sep).** Delay 4 days.
- 0:00-7:40 is **one continuous Gun Game match**, stream 0:30:28 to 0:40:06 (9.6 min shown in 7.7 min). 14 units, each forward; the gaps between them are only +6 to +29 s, which trims dead seconds between fights.
- The ending, 7:41-8:11, is lobby chat from stream 0:23:15-0:23:48, **before** the match.
- 458 s of 492 s matched.
- The same stream also supplied 3c0n part 2 (0:45-1:35) **without overlap**. One stream produced two highlights, 4 and 17 days later.

**F. [VSK7Q7FH5rk](https://www.youtube.com/watch?v=VSK7Q7FH5rk) First time Spider-Man mode (510 s, 5 Aug 2026). Source: [r2uMjM4PFVA](https://www.youtube.com/watch?v=r2uMjM4PFVA) "NEW SPIDERMAN MODE IN BGMI" (30 Jul, 3.33 h).** Delay 6 days.
- 25 units with a median of about 14 s.
- The opening 0:00-0:14 is from stream 0:08:09, used as an unlabelled hook. The story then starts at 0:03:33 and runs forward.
- One early flash-forward: 1:37-1:57 comes from stream 1:10:22 and is placed before 0:22:19 material.
- From 2:36 the video runs strictly forward: 0:24 → 0:27 → 0:29 → 0:34 → 0:38 → 1:29 → 1:30 → 1:38 → 1:41 → 1:46 → 1:48 → 1:53 → 1:54 → 2:02 → 2:03.
- Span 0:03:33-2:03:28: 120 min to 8.5 min (about 7%).

**Aggregate over the 106 matched units after the first 20 s, from the six mappings**
- Matched length: median 12.9 s, IQR 7.1-18.8 s, max 109 s (a continuous Gun Game fight).
- Gaps between consecutive units from the same stream: 93 forward, 11 backward. Forward gaps:
  - 30 s or less in 39 cases, meaning dead seconds trimmed inside one conversation or fight;
  - 30-300 s in 24 cases, meaning looting, travel and lobby skipped;
  - over 300 s in 30 cases, meaning whole matches or chat periods skipped.

**Setup and aftermath around punchlines** (stream captions read around three units of 3c0n part 2)
- **Unit at 0:45:38-0:45:58.** Cut in at the drop call ("neeche koodo, gun leke"); about 9 s of setup to the death, then the punchline ("mera naseeb kharab hai…") for 8 s. Cut out about 1 s after it ends, dropping the next 40 s of call-outs.
- **Unit at 0:50:06-0:50:27.** Cut in at the death line "le ho gaya GG bhai" (about 2 s of setup), 18 s of roast riff, cut out right after the riff. The fly-ability chatter before it and the callouts after it were dropped.
- **Unit at 1:08:40-1:09:25.** Cut in mid-sentence as Rega's roast starts. The previous 30 s (chicken demands to chat, a subscriber target) were dropped. It ends on the punchline "kama bhi tu hi raha hai", which is also reused as the teaser line.
- Source: `ctx.py` output on [X_QBQqfO-9g](https://www.youtube.com/watch?v=X_QBQqfO-9g).

**What gets cut** (the content of skipped stream stretches in the mapped streams)
- Lobby waiting and chat requests ("chicken chahiye log demand kar rahe", subscriber targets).
- Callouts with no joke ("upar chal… do bande").
- Looting and travel.
- Most Super Chat reading.
- Whole later hours of the stream: TZCV used only four short units after the first hour.
- Other games played in the same stream (the Valorant parts of X_QBQ and 2z0a, GTA RP).

### Inferences
- **Selection unit:** "a reaction burst with its trigger". Typical shape: 2-10 s of setup (the death or knock, the question, or the first line of the roast), the punchline or riff, then a cut within 0-3 s of the last laughing line. Long roast monologues (20-46 s) are kept whole.
- **Order:** chronological within each stream. Exceptions: the teaser, a hook moment pulled to the front (VSK7 0:00, the Ul5m Spider-Man match), and a short chat bit used as the ending (TIDX). Across streams, compilations put the newer or better stream first and the older one after a "THE NEXT DAY" card. The card is narrative glue, not a literal timeline.
- **Coverage:** the editor uses mostly the first 30-120 minutes of the BGMI part of a stream. Later hours contribute little (TZCV) or nothing. This fits a "fresh session start is funniest" pattern, or simply editor time limits.
- **Productivity:** one stream can feed two highlights from different time ranges (X_QBQ fed TIDX and 3c0n). Material is used up within about 3 weeks.

### Gaps
- Real cut edges are about ±3 s of the matched spans. Unmatched parts of the highlights (music, meme inserts, gameplay without speech, card time) could not be placed on the stream timeline.
- 8Au8 part 2 and the IRL tails of 3c0n and TZCV were not located.
- Co-streamers' streams (Rega, Mazin) were not fetched. Some 3c0n footage carries Rega's overlay ("REGALTOS"), so some units probably come from his stream.
- Setup and aftermath seconds were read qualitatively for 3 units only. No laughter-timestamp analysis of the stream audio was possible without downloads.

## 4. Shorts on both channels

### Takeaway
Shorts are not cut from the long highlights in a systematic way.
- **JokerClips Shorts** (152, now rare) are 18-40 s single moments: IRL pranks and squad moments, often with a "Wait For The End😂" header. Some are trailers ending "Watch Full Video on JokerKiHaveli". The biggest got 5-8.6M views.
- **Main-channel gaming Shorts** are 30-40 s stacked vertical layouts: facecam on top, gameplay or a friend's facecam below, with emoji stickers.

### Cited Findings
- [GmZty_6yrQs](https://www.youtube.com/shorts/GmZty_6yrQs) "Wait For The Transition *SNAX SHOCKED*😂": 19 s, 8.63M views, 464K likes, 1 Oct 2023, shot in 4K vertical.
- [_RgXLRs1wx8](https://www.youtube.com/shorts/_RgXLRs1wx8) "When hacker meets developer😂": 31 s, 7.70M, 19 Aug 2025.
  - Layout: gameplay crop on the top half, Joker's facecam on the bottom half.
  - The first frame is a hook image (a shocked creator's face).
  - It ends on a black-and-white facecam with red caption text and a cut to another person's webcam.
- [SATVDilBDOY](https://www.youtube.com/shorts/SATVDilBDOY) "Goldy Bhai in End😂": 40 s, 7.02M, 18 Sep 2025. IRL footage letterboxed in the vertical frame, with a constant top header "Wait For The End😂".
- [tb7vUafHeso](https://www.youtube.com/shorts/tb7vUafHeso) "BATMAN ko DANCE karwa diya😂": 25 s, 222K, 14 Feb 2026. A vlog excerpt; the last 3 s show the main-channel video thumbnail with "Watch Full Video on JokerKiHaveli".
- [uTrHx260tq4](https://www.youtube.com/shorts/uTrHx260tq4) (18 s, 495K, 5 Dec 2025) and [Yo6nck1Zmok](https://www.youtube.com/shorts/Yo6nck1Zmok) (22 s, 360K, 2 Dec 2025).
- [icIr3BWd1nM](https://www.youtube.com/shorts/icIr3BWd1nM) "Sher ne Squad Wipe Kar Diya 🔥": 26 s, 145K, 3 Dec 2023. A kill Short does far worse than the comedy Shorts.
- All JokerClips Shorts metadata use the same "Main Channel…" boilerplate. — same links
- **Main channel**
  - [9gy3caHoOMs](https://www.youtube.com/shorts/9gy3caHoOMs) "Goldy Dada Gussa Ho Gaye 🤣": 40 s, 5.47M, 7 Jul 2025. A stacked layout of Joker's facecam on top and Goldy's webcam beneath, with full-screen cut-ins of Goldy's face at the angry beats. No gameplay.
  - [PVmTr-gdojA](https://www.youtube.com/shorts/PVmTr-gdojA) "International lobby 🥵🤯": 30 s, 444K, 9 Aug 2026. Facecam on the top ~45%, gameplay on the bottom ~55%, 💀 and 🥶 stickers over the gameplay, and a flash transition at 0:02. Description: "#jokerkihaveli #shorts #pubg".
- **Recency:** of the dated JokerClips Shorts, the newest is from Feb 2026, and the 20 most recent span about Dec 2023 to Feb 2026. Shorts have become occasional. — [JokerClips Shorts tab](https://www.youtube.com/@jokerclipss/shorts)

### Inferences
- The Shorts that win are relationship moments with a reveal at the end ("Wait for the end", "Goldy Bhai in End", "hacker meets developer"). They are not kills.
- For Kaatclip's comedy Shorts:
  - 18-40 s;
  - one moment whose payoff is in the last 3-5 s;
  - a constant top text promising the ending;
  - stacked facecam (top) and gameplay or friend cam (bottom), or full facecam when there is no relevant gameplay;
  - optionally a 2-3 s "watch full video" end card pointing to the long highlight.
- The streamer's own team does not cut a Short from every highlight. Same-day teaser Shorts are a Kaatclip idea, not Joker's practice.

### Gaps
- Upload dates were fetched for only 10 Shorts, so a Shorts cadence per month could not be measured. The flat listing has no dates for Shorts.
- Two Shorts (Iu0h5u9hvLE, IQkWDpXNhf0) failed with HTTP 429.

## 5. Upload practice: titles, thumbnails, descriptions, timing, what wins

### Takeaway
JokerClips uploads one edited highlight about every 3-6 days, 4-6 days after the source stream. Leftovers are compiled into a second video 2-3 weeks later. Titles follow a strict "[names] [conflict word in caps] [emoji] *FUNNY HIGHLIGHT!*" formula. Descriptions and tags are fixed boilerplate. Views depend far more on the co-star and the relationship hook than on the gameplay: the Snax and Goldy titles of 2023-25 reached 0.35-1.06M, while the Rega-era videos of 2026 sit at 100-260K.

### Cited Findings
- **Delay from stream to upload, measured:**

| Highlight | Stream date | Upload | Delay |
|---|---|---|---|
| [VSK7Q7FH5rk](https://www.youtube.com/watch?v=VSK7Q7FH5rk) | 30 Jul | 5 Aug 2026 | 6 days |
| [8Au8-kSBhgg](https://www.youtube.com/watch?v=8Au8-kSBhgg) | 31 Aug | 5 Sep | 5 days |
| [TIDXJ1YeirM](https://www.youtube.com/watch?v=TIDXJ1YeirM) | 7 Sep | 11 Sep | 4 days |
| [TZCVFWl7NtM](https://www.youtube.com/watch?v=TZCVFWl7NtM) | 30 Sep | 5 Oct | 5 days |
| [Ul5mEjNyzu4](https://www.youtube.com/watch?v=Ul5mEjNyzu4) | 27 Aug and 2 Sep | 16 Sep | 20 and 14 days |
| [3c0nLXL8k6U](https://www.youtube.com/watch?v=3c0nLXL8k6U) | 7 and 8 Sep | 24 Sep | 17 and 16 days |

- **Descriptions:** always "Main Channel: https://youtube.com/@Jokerkihavelii #jokerkihaveli #jokerclips #bgmi".
- **Tags:** the same 6 tags ('joker', 'joker clips', 'joker ki haveli', 'joker reaction', 'bgmi', 'funny highlight'). VSK7 swaps one for 'spiderman'.
- No chapters, no music credits, and no link to the source stream. — any of the linked highlights
- **Titles in 2026:**
  - Relationship and conflict hooks: "Joker & Rega *THE FUNNIEST DUO*😂", "WHO IS THE MOST *CHUGALKHOR* In S8UL?😂", "Snax Got TRIGGERED By Joker Mic Spamming😂".
  - Novelty hooks: "Joker First Time Playing New Spider-Man Mode", "BGMI NARUTO UPDATE 4.5".
  - Length-as-promise: "Joker Being Joker For 8 Minutes", "Joker's Rage & Laughter For 10 Minutes".
  - Money hooks: "₹2,00,000 Challenge", "₹12 Lakh Challenge".
  - Source: [JokerClips videos tab](https://www.youtube.com/@jokerclipss/videos)
- **Best 2026 session-type videos:**
  - [DCcMipfpEfw](https://www.youtube.com/watch?v=DCcMipfpEfw) "Joker Rega First Time Playing Scrims With Team SouL": 360K, an esports crossover.
  - [8Au8-kSBhgg](https://www.youtube.com/watch?v=8Au8-kSBhgg) Joker vs Goblin: 337K, an esports name.
  - [Kobcv7gzuAY](https://www.youtube.com/watch?v=Kobcv7gzuAY) "Meccha Chameleon First Time With S8UL": 276K.
  - [AKw_7q-I8lA](https://www.youtube.com/watch?v=AKw_7q-I8lA) Snax: 258K.
  - Weakest: Rega-only duo titles at 70-130K ([PN3OwuHQlxo](https://www.youtube.com/watch?v=PN3OwuHQlxo) 70K, [95Mtbj6Y8do](https://www.youtube.com/watch?v=95Mtbj6Y8do) 72K).
- **Engagement:** likes per view on 2026 highlights are 2.6-6.9% (8Au8 8.8K likes on 337K; Ul5m 7.7K on 201K). The 2023-24 highlights ran 4.6-7.1% (E6h 48.8K on 1.06M). — metadata of the linked videos
- **Thumbnails:** the 2-4 face collage plus speech bubble described in the earlier note still holds. The 3c0n bubble "ZAALIM HAI DUNIYA PAR TU!!" is the 6:00 line, so the thumbnail line is taken from the video's own peak argument. — [3c0n thumbnail](https://i.ytimg.com/vi/3c0nLXL8k6U/hqdefault.jpg)

### Inferences
- **What drives views:** a recognisable co-star with a conflict (Snax, Goldy, Goblin, SouL), novelty (a first-time mode or new update), or money stakes. The gameplay quality matters little.
- **For Kaatclip's packaging:** name the people, add one conflict or novelty word, use a caps keyword and 😂🤣. Suggest posting 3-7 days after the stream. Hold leftover moments for a second "part 2" compilation.

### Gaps
- No public source states JokerClips' posting rules. Delay and selection are inferred from six mappings.
- No YouTube Analytics data (retention, CTR) is available. Views are rounded public counts.

## 6. Rules an automatic editor could follow to make JokerClips-style comedy session highlights

### Takeaway
Reproduce the **selection and ordering** with measurable rules:
- one stream (or two for a compilation);
- the first 30-120 min of the BGMI part;
- about 15-30 reaction units of 7-45 s, each from its trigger to the punchline plus 0-3 s;
- chronological within a stream;
- a newer-stream-first compilation joined by a "THE NEXT DAY…" card;
- an 8:00-8:15 total.

Reproduce the **look** with a facecam crop-zoom on talk, results screens kept, labelled meme or emoji inserts, a burned-in subtitle for the key line, an optional 10-20 s "IN THIS VIDEO" teaser, and an abrupt or punchline ending.

### Cited Findings (measured targets)
- Length: 480-489 s for 111 of the 236 JokerClips videos of 420-720 s, and 69 of 133 session highlights. — [JokerClips videos tab](https://www.youtube.com/@jokerclipss/videos)
- Stream span used per highlight part: 17-156 min; 88 min became about 4.5 min (8Au8); 120 min became 8.5 min (VSK7). — sections 3A-F
- Kept unit length: median 12.9 s of matched speech, IQR 7.1-18.8 s; units up to 46 s for roast monologues and 109 s inside a single continuous fight. — section 3 aggregate
- Gaps: 39 of 93 forward gaps are 30 s or less (micro-trims), 24 are 30-300 s, 30 are over 300 s. — section 3 aggregate
- Speech in output: 77-94% of seconds; 88-179 wpm. — section 2 table
- Teaser: 10-22 s, 3-5 cuts of 3-5 s, lines taken from the later body. Present in 6 of 7 dated videos from Apr-Oct 2026 that join two streams or are long sessions. Absent in single-match videos. — section 2

### Inferences (proposed rules for Kaatclip; numbers marked "measured" are from this study, the rest are design choices)

**Moment detection (score every 1 s of the stream)**
1. Speech burst: words per minute above the stream's 75th percentile over 10 s; two or more voices overlapping; laughter (YAMNet "Laughter", "Giggle") or a shout within 3 s after a line.
2. Triggers that open a unit:
   - a death or knock (kill feed, "Spectating", "all dead");
   - a question or roast opener (Hinglish cues: "tu", "tera", "bhai sun", "kya kar raha", teammate names, "editor", "chat");
   - a donation or chat read-out;
   - a results, MVP or "Top 10" screen;
   - a new mode or first-time event.
3. Comedy keyword boosts: "naseeb kharab", "GG", "kahan kooda", "gun nahi", "recall de", "hacker", "lag", "meri galti", "kisne", "zaalim", "Zomato", "labour", repeated-word loops (the same word 3 or more times within 5 s, as in "paani mein info do" ×10 or "kha kha kha"), and singing over gameplay.
4. Explicit streamer flags: "clip kaat", "highlight", "editor", "ye clip banega" (measured: Joker says these on stream). Treat as a strong marker, like Kaatclip's existing markers.
5. Down-rank: callouts without laughter, lobby waiting, looting with under 30 wpm, other games (Valorant, GTA), and generic Super Chat thank-yous.

**Unit construction**

6. Start 2-10 s before the punchline line, at the trigger (death, knock, question). For a roast or monologue, start at its first sentence, even mid-stream-sentence (measured on 3 units).
7. End 0-3 s after the last laughing or punchline line. Do not run the next callout (measured).
8. Keep long monologues whole up to about 45 s. Inside one fight or match, allow a continuous unit of up to about 110 s, but trim internal silences over 5 s.
9. Merge units less than 30 s apart in the stream into one block, with micro-trims (measured: 39 of 93 gaps are 30 s or less).

**Selection and ordering**

10. Limit the source window to the first about 120 min of the BGMI part of a stream (measured: material after that is sparse).
11. Pick about 15-30 units, about 8 minutes in total. Spread them so that about one top-scoring burst lands every 60-90 s (this inference matches the heatmap spikes at 92, 317 and 381-400 s in 8Au8 and 333 s in Ul5m).
12. Keep stream order. Three allowed exceptions:
    - (a) one hook unit, the best moment from later in the session, at 0:00-0:15;
    - (b) a short chat or lobby bit from before the match as the ending;
    - (c) local swaps of under 5 min.
13. **Single-match mode:** if one match has dense comedy (speech above about 80% and at least 6 bursts) and lasts 8-12 min, keep it almost whole: drop dead seconds, add no cards, no teaser, and end on the results or VICTORY screen (TIDX measured: 9.6 min of the match became 7.7 min).
14. **Compilation mode:** if one stream yields under about 6 minutes, append the best block from another stream of the same creator from the last about 3 weeks, behind a "THE NEXT DAY…" card (measured: 3 of 6 mapped highlights did this, and 2 of the 3 went backwards in time). Use "2 SECONDS LATER…" style cards for jumps of a few minutes within a match.
15. Ensure no unit is reused across two highlights (measured: X_QBQ fed two highlights from separate ranges).

**Look**

16. Base: the stream's own layout at 16:9, overlays included (sponsor banners, counters, QR codes). On every talk unit, crop-zoom to the facecam region (about 3x) and return to the full layout for fights. With a second creator on call, place two webcams side by side.
17. Burn in one subtitle per unit for the punchline line. Use white sentence-case at the bottom, or a caps meme caption at the top for big lines.
18. Optional: 3-6 meme or emoji inserts of 1-3 s per video with a one-word label ("CHAT", the teammate's name). Kaatclip should use its own stickers rather than film clips, for copyright reasons (inference).
19. Teaser (compilation mode): an "IN THIS VIDEO" label over 3-5 cuts of 3-5 s, taken from the top-scoring punchline lines of the body. 10-22 s in total.
20. Ending: stop on the final punchline or facecam reaction, or a short "SUBSCRIBE" card of 10 s or less. Viewers leave at the end anyway (last heatmap bin about 0 in every video). Never end on a long quiet fight.
21. Length: fill to 480-495 s. A 10-11 min variant (600-700 s) only when the source is exceptionally rich (measured: rpbg 633 s, Moye Moye 690 s).

**Packaging**

22. Title: "[Streamer] & [Teammate] *[CONFLICT/NOVELTY WORD]*😂 *FUNNY BGMI HIGHLIGHT!*🤣", or "[Streamer] Being [Streamer] For 8 Minutes". Description: a link to the main channel plus 3 hashtags. Thumbnail speech bubble: the top punchline line, shortened.
23. Timing: propose the highlight 3-6 days after the stream. Keep leftover top units in a pool for a "part 2" within 3 weeks.

### Gaps
- Rules 6-9 rest on matched-caption spans (±3 s) and three hand-read units. Kaatclip's own laughter and loudness timestamps on full test streams should tune them.
- How the human editor ranks moments (beyond what was kept) is unknown, since the dropped stream content was only sampled.
- Diarisation of the squad voices was not tested. Auto-captions do not separate speakers.
