# Goblin (@goblinbgmi) A to Z: every content type, where its footage comes from, how it is edited and uploaded

Method (12 Nov 2026). Public data only. I used yt-dlp with `--skip-download`; no video or audio was downloaded.

**What was read**
- The full flat lists of the Videos tab (**380 items**), the Streams tab (**100**) and the Shorts tab (**4**). The channel has no Playlists tab.
- Full metadata for 474 of those 484 items. The other 10 are 8 members-only items and 2 deleted videos.
- Hindi auto-captions for 53 main-channel videos and 52 streams.
- One or two mid-video storyboard frames for **every** long video since July 2021 (125 videos) and every dated stream (93).
- Full storyboard contact sheets for 25 videos not covered before and 2 whole streams; the earlier study's 29 sheets were reused. Thumbnails for all 480 items.
- Kick's public API for kick.com/soulgoblin: the channel record, the last 3 VODs and all 74 public clips.

**Builds on.** This study extends `research_notes/BGMI highlight channels deep study/goblin_deep.md` and `research_notes/BGMI highlight video structure/goblin_esports.md`. Those studies saw only the newest 79 videos (May 2023 to Aug 2026) and the last 30 streams. Their findings are reused, not repeated. The second channel @goblinsh0rts is covered there and is referred to here only where it explains the main channel.

**Measures**
- **Caption alignment.** Every 3-word run of a highlight's captions is looked up in a stream's captions. The pair scores one point for each run that agrees on a time offset with at least 3 neighbours. Real pairs score 127 to 603. Non-pairs score 0 to 63, usually under 15.
- **Views and dates.** All views are as of 12 Nov 2026. All times are IST.

**Scratch data.** Inventory, metadata, captions, storyboards, mosaics and Kick JSON are in `C:\Users\soura\AppData\Local\Temp\claude\21027423ba80eb72\c7886632-c6c6-4a95-81c6-c6cbac2a769e\scratchpad\a2z\goblin_main\`. Key files:
- `inventory.json`: one row per upload, with class, date, length, views and resolution.
- `source_map.json`: the visual source label of every long video since 2021.
- `mid169a/b.jpg`, `midphone.jpg` and `mid_streams_a/b.jpg`: the mosaics.
- `kick_*.json`: the Kick data.

## 1. Full inventory: what the channel has posted since 2020, by type, and how the mix changed

### Takeaway
The main channel has gone through **five distinct phases**:
1. **2020 to mid-2021:** PUBG Mobile scrims and tournament highlights with a few hundred views.
2. **Jul 2021 to Jul 2022:** about 30 short horizontal clutch clips a month, and the channel's biggest view counts.
3. **Aug 2022 to Apr 2023, during the BGMI ban:** stream-cut challenge and funny videos with heavy meme editing.
4. **May 2023 to Dec 2024:** about 3 to 9 single-match tournament highlights a month.
5. **2025 to 2026:** about one tournament highlight a month, plus 25 to 32 public YouTube streams a year.

In total there are 380 Videos-tab uploads, 100 streams and 4 Shorts. Short clips (187) and single-match highlights (116) make up 80% of the Videos tab. Since 2023 the long highlight (4 to 11 min) has been the only regular upload.

### Cited Findings
- **Totals.** The Videos tab has 380 items, the earliest dated 25 Feb 2020 and the latest 31 Aug 2026. Three cannot be read: one members-only vlog ([qXmSMZtjWss](https://www.youtube.com/watch?v=qXmSMZtjWss)) and two "not available". The Streams tab has 100 items: 93 public (6 Jun 2021 to 10 Nov 2026) and 7 members-only. The Shorts tab has 4 items. There is no Playlists tab (yt-dlp: "This channel does not have a playlists tab") — [@goblinbgmi/videos](https://www.youtube.com/@goblinbgmi/videos), [/streams](https://www.youtube.com/@goblinbgmi/streams), [/shorts](https://www.youtube.com/@goblinbgmi/shorts)
- Classification of all 380 Videos-tab items (title keywords plus length, with 14 manual overrides after viewing). This is a measurement over the whole tab — [@goblinbgmi/videos](https://www.youtube.com/@goblinbgmi/videos):

| Type | n | Length, middle half (median) | Views, middle half (median) | First to last |
|---|---|---|---|---|
| Short clip, 100 s or less (one clutch, spray or banter beat; horizontal) | 187 | 18–60 s (32 s) | 3.7K–169K (26K) | Jul 2020 – Dec 2023 |
| Single-match highlight | 116 | 257–489 s (355 s) | 1.2K–143K (71K) | Apr 2020 – Aug 2026 |
| Frag or clutch montage | 28 | 137–239 s (195 s) | 1.9K–168K (19K) | Feb 2020 – Dec 2025 |
| Tournament or day reel (several matches) | 18 | 230–463 s (332 s) | 0.9K–207K (174K) | Oct 2020 – Aug 2026 |
| TDM or custom-room battle (1v1, 2v2, 4v4, WOW) | 9 | 384–708 s (568 s) | 158K–382K (196K) | Sep 2021 – Feb 2026 |
| Challenge or funny stream cut | 8 | 238–298 s (265 s) | 198K–329K (231K) | Aug 2022 – Mar 2023 |
| Announcement, hype or nostalgia | 7 | 31–154 s (61 s) | 2K–393K (265K) | Oct 2020 – Oct 2023 |
| Vlog or IRL (one members-only) | 4 | 587–1,195 s | 57K–144K | Feb 2024 – Jun 2026 |
| Sponsored, gift or unboxing | 2 | 216 s, 708 s | 144K, 155K | Oct 2023, Apr 2026 |
| Other game (Clash of Clans) | 1 | 552 s | 2.4K | Oct 2020 |

- Uploads per year by type (Videos tab; 3 undated items left out) — [@goblinbgmi/videos](https://www.youtube.com/@goblinbgmi/videos):

| Year | Short clip | Single match | Reel | Montage | TDM | Challenge | Announce | Vlog | Sponsor | Other | Total | Median views |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2020 | 20 | 37 | 5 | 5 | 0 | 0 | 1 | 0 | 0 | 1 | 69 | 982 |
| 2021 | 132 | 23 | 1 | 11 | 3 | 0 | 1 | 0 | 0 | 0 | 171 | 24K |
| 2022 | 32 | 5 | 0 | 3 | 1 | 7 | 4 | 0 | 0 | 0 | 52 | 331K |
| 2023 | 2 | 26 | 4 | 2 | 2 | 1 | 1 | 0 | 1 | 0 | 39 | 177K |
| 2024 | 0 | 11 | 2 | 4 | 1 | 0 | 0 | 2 | 0 | 0 | 20 | 107K |
| 2025 | 0 | 9 | 2 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 15 | 108K |
| 2026 | 0 | 4 | 4 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 11 | 159K |

- **Cadence**
  - Video uploads per month peaked at 34 in Sep 2021 and 37 in Oct 2021, when clips went up almost daily, often 2 a day.
  - Monthly uploads in 2023: 1, 4, 0, 5, 9, 4, 4, 4, 3, 2, 3 (Feb to Dec).
  - In 2025 the channel was active in 7 months, with 1 to 5 uploads in each. In 2026 it was active in 6 months, with 1 to 4 in each.
  - Since 2025, uploads cluster around events: 5 in Dec 2025 after CEGC, and 4 in Aug 2026 during BGMS — [@goblinbgmi/videos](https://www.youtube.com/@goblinbgmi/videos)
- **Short clips (Jul 2021 to Jul 2022).** There were 154 clips, with a median of 26.5 s and median views of 33.6K.
  - The 107 clips from Jul to Nov 2021 have a median of 22.5K views. The 47 clips from Dec 2021 to Jul 2022 have a median of 310K.
  - The channel's all-time top five are all such clips:
    - "Why you Camp bro 😎": 25 s, 1.04M views ([-vbAZpx5Iek](https://www.youtube.com/watch?v=-vbAZpx5Iek))
    - "Reflex khate khate bach Gaya 😂": 896K ([BV9NcUSaLN4](https://www.youtube.com/watch?v=BV9NcUSaLN4))
    - "SouLplayer4 🚀🥶?": 771K ([ZZx4Viy3Kg0](https://www.youtube.com/watch?v=ZZx4Viy3Kg0))
    - "1v4 7sea in BMOC🚀": 751K ([RwM6auLpXXU](https://www.youtube.com/watch?v=RwM6auLpXXU))
    - "Don't finish my teammate 👿": 748K ([CW7NztKAatI](https://www.youtube.com/watch?v=CW7NztKAatI))
  - 100 of the 2021 clips are phone-shaped 1920x886 frames, which is why they sit on the Videos tab and not the Shorts tab (yt-dlp metadata)
- **Top long videos**
  - "Sanhok Domination | Solo 12 Finishes WWCD | Nodwin Champions Cup", 604K ([67w15TWdikI](https://www.youtube.com/watch?v=67w15TWdikI))
  - "Comeback in BGMS Decider Matches", 540K ([aA98jrFkEPQ](https://www.youtube.com/watch?v=aA98jrFkEPQ))
  - "Solo 12 Kills BMOC highlights", 166 s, 669K ([pkXkzlxuNzw](https://www.youtube.com/watch?v=pkXkzlxuNzw))
  - "Frags 🚀🫀", 496K ([lnAJghtGfow](https://www.youtube.com/watch?v=lnAJghtGfow))
  - "Team SouL Domination | Solo 14 Kills WWCD", 459K ([OOnDKF-Wprs](https://www.youtube.com/watch?v=OOnDKF-Wprs))
- **Streams per year (public).** 2021: 10; 2022: 6; 2023: 7; 2024: 13; 2025: 32; 2026 (to 10 Nov): 25. The 7 members-only streams are undated; their titles are "Road to 400k | Members onlyyyyyy....", "kaise ho dostoooo", "i m back myyyy peopleeee" and "chain together" — [@goblinbgmi/streams](https://www.youtube.com/@goblinbgmi/streams)
- **Shorts tab (4 in total)**
  - "1v3 SouL again Quick": 20 Aug 2021, 15 s, 1.05M ([iF7cZNBIGKc](https://www.youtube.com/shorts/iF7cZNBIGKc))
  - "Best spray?": 21 Aug 2021, 8 s, 235K ([_gW0h_EJOCU](https://www.youtube.com/shorts/_gW0h_EJOCU))
  - "ESL LAN WWCD ✌": 4 Mar 2024, 58 s, 164K ([OdM-P3Ykios](https://www.youtube.com/shorts/OdM-P3Ykios))
  - "Goblin 1v4 Drx 🇰🇷 in WOW": 23 Feb 2026, 49 s, 293K ([pfJ3EsMgBJk](https://www.youtube.com/shorts/pfJ3EsMgBJk))
  - All Shorts work since 2022 has moved to @goblinsh0rts (438 Shorts there; see goblin_deep.md)
- **Context for the phase breaks**
  - Teams: Team SouL 2022–23, Carnival Gaming 2024, Likitha Esports early 2025, back to (iQOO)SouL from May 2025, and a "Team Goblin" entry for one event in Jul 2026 — [esportsverse](https://www.esportsverse.live/players/goblin)
  - The government banned BGMI in July 2022 — [Sportskeeda via search](https://sportskeeda.com/bgmi/news-players-streamers-move-pubg-new-state-free-fire-max-games-amidst-bgmi-ban)
  - His stream "BGMI IS BACK BOISS" on 29 May 2023 marks the return — [gRQYFNf0Lmc](https://www.youtube.com/watch?v=gRQYFNf0Lmc)
  - In March 2023 the channel was hacked; it then had about 382K subscribers and 356 videos — [AFK Gaming via search](https://afkgaming.com/mobileesports/news/soul-goblin-gives-an-update-about-his-hacked-youtubechannel)

### Inferences
- The channel moved from **volume to curation**. In 2021 to 2022 it posted many daily clips. Since 2023 it posts a few long hero edits, and the volume work went to @goblinsh0rts. The 2022 view jump of the clips (310K median from Dec 2021) came after he joined Team SouL (Mar 2022 per reports). The channel's reach followed his esports status more than any format change.
- "One long highlight per tournament day or best match" has been the stable main-channel format since May 2023. That is the format Kaatclip's esports preset copies.

### Gaps
- The format is approximate for about 10 items whose titles are ambiguous; for example, some "Highlights" titles are one match plus a frag opener.
- Three items could not be read, so their dates and lengths are missing. Videos deleted before 12 Nov 2026 (for example after the 2023 hack) cannot be counted.

## 2. What each content type is BASED ON: the footage source, proved per type and era

### Takeaway
The source has **changed with each era**. No main-channel highlight since 2025 is cut from a public YouTube stream, except two "Legend League" videos (Mar 2025), which were caption-aligned to their streams. The answer to the earlier puzzle has three parts:
- **(a) Main-channel match highlights are on-device phone screen recordings.** This holds for 46 phone-shaped uploads (2.16:1, no overlay, no facecam) and for 33 more 16:9 uploads that letterbox the phone image, some inside a red branded panel.
- **(b) The 2022 to 2024 stream-cut videos are not from his YouTube streams.** They carry his stream overlay, but none of the 31 videos tested aligns with any of the 26 public YouTube streams from Jun 2021 to Jun 2024 that have captions. In the ban era (2022 to 2023) his regular streams were on **Loco**: his video descriptions linked Loco, and Sportskeeda reported 154K Loco followers.
- **(c) Since June 2026 his regular streams are on Kick.** On YouTube he streams members-only or occasionally. Kick VODs carry the same iQOO overlay and facecam, so Kick is a source for @goblinsh0rts stream cuts but **not** for the clean main-channel edits.

Tournament footage comes from his phone POV, sometimes with short inserts from the official broadcast. Vlogs and sponsored videos are camera-shot.

### Cited Findings
**Source by era, from mid-video frames of all 125 long videos since Jul 2021.** Labels are from mosaics `mid169a/b.jpg` and `midphone.jpg`. Counts are of long videos (over 100 s) — [@goblinbgmi/videos](https://www.youtube.com/@goblinbgmi/videos):

| Half-year | Phone recording (clean HUD) | Stream cut (overlay plus facecam) | Camera or other |
|---|---|---|---|
| 2021 H2 | 26 (letterboxed; see note) | 0 | 0 |
| 2022 H1 | 5 | 0 | 0 |
| 2022 H2 | 0 | 11 | 0 |
| 2023 H1 | 10 | 9 | 0 |
| 2023 H2 | 13 | 3 | 2 |
| 2024 H1 | 6 | 4 | 2 |
| 2024 H2 | 8 | 0 | 0 |
| 2025 H1 | 3 | 3 (2 Legend League, 1 archive of 2022) | 0 |
| 2025 H2 | 9 (incl. red panel) | 0 | 0 |
| 2026 | 9 (red panel to Feb, then full-frame) | 0 | 2 |

**How the phone source shows**
- **Upload shape.** 46 long videos are uploaded at the phone's own shape: 1920x886 or 888 (2021 to 2024), or 3630 to 3644 x 1768 to 1772 (2023 to 2026, about 2.06 to 2.17:1). They show the full touch HUD on both edges and no stream bar or facecam. Examples: [aA98jrFkEPQ](https://www.youtube.com/watch?v=aA98jrFkEPQ), [OOnDKF-Wprs](https://www.youtube.com/watch?v=OOnDKF-Wprs), [6jIQaYvIOGc](https://www.youtube.com/watch?v=6jIQaYvIOGc), [nk3MGVXKCFo](https://www.youtube.com/watch?v=nk3MGVXKCFo)
- **Letterboxed inside 16:9.** 2024 examples are [9pG_cQv0-oA](https://www.youtube.com/watch?v=9pG_cQv0-oA), [vQI69QKrYMc](https://www.youtube.com/watch?v=vQI69QKrYMc) and [CjtBdcq1rqI](https://www.youtube.com/watch?v=CjtBdcq1rqI). Many show a black rounded pill at the left edge, the phone's camera cut-out area.
- **Red branded side panel.** All 9 main-channel videos from Nov 2025 to Feb 2026 put the phone image inside one, for example [lBswYFSS_rQ](https://www.youtube.com/watch?v=lBswYFSS_rQ), [_HMq3jgPsk8](https://www.youtube.com/watch?v=_HMq3jgPsk8) and [ml5FitUoqf8](https://www.youtube.com/watch?v=ml5FitUoqf8). These are storyboard observations.
- **The 2021 note.** His 2021 YouTube streams were phone-only streams: an orange "insane Goblin" bottom bar and no facecam, for example [4g9UUQk5GiM](https://www.youtube.com/watch?v=4g9UUQk5GiM) and [G6vOWOF_uV4](https://www.youtube.com/watch?v=G6vOWOF_uV4). A letterboxed 2021 highlight therefore cannot be told apart from a stream VOD by frame alone. Three 2021 highlights tested against all 10 public 2021 streams had none matching (best scores 9, 6, 0): [ZTuwmjGSqcw](https://www.youtube.com/watch?v=ZTuwmjGSqcw), [TkkTGA9zazs](https://www.youtube.com/watch?v=TkkTGA9zazs) and [3_ljn_orIuc](https://www.youtube.com/watch?v=3_ljn_orIuc). This is this study's alignment.

**Stream cuts: the overlay matches his stream look of the time, but the captions do not match YouTube streams**
- **The overlays by era.**
  - 2022 to 2023 stream-cut videos carry the green "GOBLIN" bottom bar with a facecam. That is the same overlay as his YouTube streams of that time, for example [akMKwx8Tv2M](https://www.youtube.com/watch?v=akMKwx8Tv2M) (Aug 2022) and [HfUc5xo7Gjg](https://www.youtube.com/watch?v=HfUc5xo7Gjg) (Sep 2023).
  - 2024 cuts carry the red "GOBLIN" Carnival-era bar ([fCsIPFa0EAs](https://www.youtube.com/watch?v=fCsIPFa0EAs), [_cibYWwUaC8](https://www.youtube.com/watch?v=_cibYWwUaC8)), or a UC top-up sponsor bar ([5yGzIrfD88Y](https://www.youtube.com/watch?v=5yGzIrfD88Y)).
  - These are storyboard observations.
- **Alignment test.** Thirty-one stream-cut and phone videos from 2021 to 2024 were aligned against **26 public YouTube streams**. That is every public stream from Jun 2021 to Jun 2024 that has captions: all 10 from 2021, all 6 from 2022, 6 of 7 from 2023 (one, [pJsHrcVum7s](https://www.youtube.com/watch?v=pJsHrcVum7s), has no captions) and all 4 from Jan to Jun 2024. Not one matched; the best score was 10, against 192 to 603 for real pairs. Videos with enough speech to test included:
  - [j2q2-5vLbOg](https://www.youtube.com/watch?v=j2q2-5vLbOg) (276 words), aligned against the 1 Sep 2022 "BGMI tournament live" stream [WU9WhYdDWtU](https://www.youtube.com/watch?v=WU9WhYdDWtU)
  - [1vvqX_zTkgc](https://www.youtube.com/watch?v=1vvqX_zTkgc), [L3dRvqwVfNw](https://www.youtube.com/watch?v=L3dRvqwVfNw) and [dZ_206yLWPY](https://www.youtube.com/watch?v=dZ_206yLWPY)
  - [JLj4nnIu0ZY](https://www.youtube.com/watch?v=JLj4nnIu0ZY), [fCsIPFa0EAs](https://www.youtube.com/watch?v=fCsIPFa0EAs) and [5yGzIrfD88Y](https://www.youtube.com/watch?v=5yGzIrfD88Y) (482 words)
- **YouTube streams were scarce in that period.** There were 6 public streams in 2022 and 7 in 2023, and none at all between 21 Sep 2022 and 18 May 2023 — [@goblinbgmi/streams](https://www.youtube.com/@goblinbgmi/streams). Yet 9 stream-cut videos were uploaded between Oct 2022 and May 2023 ([ew3PgA5cjwQ](https://www.youtube.com/watch?v=ew3PgA5cjwQ), [xKPBU_NqbK0](https://www.youtube.com/watch?v=xKPBU_NqbK0), [h6Q9m_ik99E](https://www.youtube.com/watch?v=h6Q9m_ik99E), [2c_XoSDSmmw](https://www.youtube.com/watch?v=2c_XoSDSmmw) and others)
- **Loco.**
  - Nine video descriptions from Mar to May 2023 link "⭐ LOCO :- https://loco.onelink.me/65Kg/SouLGoBLIN". Examples are [2c_XoSDSmmw](https://www.youtube.com/watch?v=2c_XoSDSmmw), [lXLAytUgcTo](https://www.youtube.com/watch?v=lXLAytUgcTo) and [zEka75PCAwk](https://www.youtube.com/watch?v=zEka75PCAwk), and the streams [39Ege1CuYkc](https://www.youtube.com/watch?v=39Ege1CuYkc) (Sep 2022) and [gRQYFNf0Lmc](https://www.youtube.com/watch?v=gRQYFNf0Lmc) (May 2023) do too.
  - Sportskeeda (Aug 2023): he "has found a strong footing on Loco, where he regularly streams Krafton's battle royale title", with "over 154K followers" — [Sportskeeda](https://sportskeeda.com/bgmi/soul-goblin-bgmi-id-stats-f-d-ratio)
  - An older 2021 stream is titled "Esports wala x LOCO Invitational" ([q_W_kqQo4VI](https://www.youtube.com/watch?v=q_W_kqQo4VI))
- **The one proved pair on the main channel since 2022.**
  - "Legend League 20 Solo Kills | New Record" (612 s, uploaded 5 Mar 2025 16:44, [_elUiudgCM8](https://www.youtube.com/watch?v=_elUiudgCM8)) aligns to "GoBLiN is Live | Ultimate Royale BGMI!" ([TuxKc0QX2qg](https://www.youtube.com/watch?v=TuxKc0QX2qg), started 4 Mar 2025 19:38, 4.3 h) with **277 anchors**. Its body runs 2:16:40 to 2:45:48 in the stream.
  - "Top 10 Legend League Solo 21 Finishes" ([DFnr6WDiE6o](https://www.youtube.com/watch?v=DFnr6WDiE6o), 6 Mar 2025 18:10) aligns to [7LttULfoql0](https://www.youtube.com/watch?v=7LttULfoql0) (started 5 Mar 2025 19:39) with **192 anchors**, spanning 3:51:21 to 4:13:25.
  - Both went up about 17 to 18 h after the stream ended. This is this study's alignment.

**Kick (2026).** These are the platform facts; the members-only arrangement is in the next item.
- **Account.** kick.com/soulgoblin (display name "SouLGoBLiN") is verified and an affiliate, with **20,587 followers** — [Kick API](https://kick.com/api/v2/channels/soulgoblin)
- **Last 3 VODs.** All are titled "ULTIMATE GRIND": 3 Nov 2026 (4.6 h, 5,572 views), 5 Nov (3.3 h, 3,390) and 7 Nov (2.1 h, 6,508). They started at 16:04 to 16:43 IST, in the BGMI category — [Kick videos API](https://kick.com/api/v2/channels/soulgoblin/videos)
- **Clips.** There are 74 public Kick clips from 26 Kick livestreams, 15 Jun to 7 Nov 2026. The earliest, on 15 Jun 2026, is titled "My first stream." (Just Chatting). Clip times run 14:00 to 00:30 IST.
- **Overlap with YouTube.** In the same window he had only 7 public YouTube streams (23 Jun, 28 Jun, 22 Jul, 31 Aug, 5 Oct, 26 Oct, 10 Nov), and only 31 Aug falls on a Kick clip day — [Kick clips API](https://kick.com/api/v2/channels/soulgoblin/clips)
- **Kick layout.** Kick clip thumbnails show the same layout as his YouTube streams: the game full-width, an "iQOO 15R … amazon specials" banner along the bottom and the facecam bottom-right. Aug to Sep 2026 clips are BGMS broadcast watch-alongs with a facecam. These are thumbnail observations (`kick/clips_sheet.jpg`).
- **BGMS 2026 on Kick.** BGMS 2026 (10 Aug to 6 Sep 2026) streamed "exclusively on KICK", starting at 4 pm IST daily — [indiantelevision.com](https://indiantelevision.com/iworld/kick-bags-exclusive-streaming-rights-for-bgms-season-5/). An 8Bit Creatives × Kick agency deal (9 Jul 2026) lists a "Goblin" among 48 creators. That identity is unconfirmed — [streamer.guide](https://streamer.guide/blog/8bit-creatives-kick-india-partnership-2026)

**His own words on the switch (YouTube members-only plus Kick)**
- In the 2 Jun 2026 stream he says that regularly he will be on Kick and on YouTube members-only "at the same time", with a "30 seconds delay" on Kick. He asks non-members to follow him on Kick and checks his Kick follower count (about 600). Hindi auto-captions, 10:14 to 10:40 and 23:12 — [7dUemvoJ1c0](https://www.youtube.com/watch?v=7dUemvoJ1c0)
- In the 28 Jun 2026 stream he says he cannot play songs on YouTube but plays them on Kick, and signs off "see you guys tomorrow Kick pe" — [1dyilJkeOeQ](https://www.youtube.com/watch?v=1dyilJkeOeQ), captions 1:06:01 and 4:59:34
- In the 22 Jul 2026 stream he says "कल 1:30 बजे आऊंगा मैं किक पे" (tomorrow at 1:30 on Kick) — [jjooz-JdgTU](https://www.youtube.com/watch?v=jjooz-JdgTU), 5:18:54
- **Descriptions.** All 9 YouTube stream descriptions since 2 Jun 2026 list "► Kick : https://kick.com/soulgoblin"; earlier ones list Discord in that place — [GVKHZ9-erB8](https://www.youtube.com/watch?v=GVKHZ9-erB8), [a4ZMq65OxGU](https://www.youtube.com/watch?v=a4ZMq65OxGU)
- **Members-only.** Other captions mention members-only streams ("15 दिन पहले ही मैंने मेंबर्स ओनली स्ट्रीम करी थी") and a members-only vlog — [mNRHxGdiRCU](https://www.youtube.com/watch?v=mNRHxGdiRCU) 5:02:04, [62uteBujkC8](https://www.youtube.com/watch?v=62uteBujkC8) 3:47:06

**Tournament broadcast, camera and other sources**
- **Broadcast inserts.** Official broadcast footage appears as short inserts inside phone-POV highlights, with the observer view, standings and "ELIMINATED" pop-ups:
  - [zw_7pRPDyK0](https://www.youtube.com/watch?v=zw_7pRPDyK0) (BGIS 2025 MVP), 0:55 to 1:12
  - "MATCH 2" and "Champions Cup DAY 2 – MATCH 3" cards ([KmjTasCQZ5U](https://www.youtube.com/watch?v=KmjTasCQZ5U), [67w15TWdikI](https://www.youtube.com/watch?v=67w15TWdikI))
  - A Nodwin "Day 4 – Match 5" broadcast plus "WINNER" card inside a vlog ([UFh9nf8TjsA](https://www.youtube.com/watch?v=UFh9nf8TjsA), 1:54 to 2:33)
  - These are storyboard observations
- **Camera-shot types.**
  - Vlogs ([UFh9nf8TjsA](https://www.youtube.com/watch?v=UFh9nf8TjsA), [2HUA9K4PivM](https://www.youtube.com/watch?v=2HUA9K4PivM), [Itq7dwuoGjc](https://www.youtube.com/watch?v=Itq7dwuoGjc) in 4K)
  - The studio group unboxing ([Vjc1H9rt7xI](https://www.youtube.com/watch?v=Vjc1H9rt7xI), 2560x1440), which is the edited version of the stream "I spent ₹8,00,000 on a Mystery Box… LIVE UNBOXING. FT. S8UL" ([kiqDrenoFP4](https://www.youtube.com/watch?v=kiqDrenoFP4), 11 Apr 2026, uploaded as a video on 13 Apr)
  - The Lenovo Legion laptop integration "Hector Gifted me this" ([2Co12jszI-4](https://www.youtube.com/watch?v=2Co12jszI-4))
- **Archive footage.** "BMPS 2022 nostalgia" (Jan 2025, [vRyPYuwYJGQ](https://www.youtube.com/watch?v=vRyPYuwYJGQ)) re-edits a 2022 stream recording that still has the green GOBLIN overlay.
- **Teammates' sources.** No main-channel video was found to use a teammate's POV or stream. Second-channel LAN cuts use the broadcast (goblin_deep.md).

### Inferences
- **Why main highlights do not match his streams.** For tournaments he records his own phone screen; he cannot stream official matches, and BGMS 2026 was Kick-exclusive. That gives a clean full-HUD file with team comms, which is what the main channel edits.
  - For streamed scrims or ranked matches in 2022 to 2024, the cut came from a stream on another platform (Loco in 2022 to 2023; 2024 unknown) using the same OBS overlay.
  - Since Jun 2026, most of his scrims streaming happens on Kick, in the afternoon, with VODs that expire. That would explain why @goblinsh0rts videos with the stream layout match no YouTube stream (goblin_deep.md, e.g. [6TnQbdev9Oo](https://www.youtube.com/watch?v=6TnQbdev9Oo)) and why its upload peak (Jun to Sep 2026) starts with his Kick streaming.
- **The red side panel** (Nov 2025 to Feb 2026) is how the editor filled a 16:9 frame around a 2.16:1 phone recording. Since May 2026, uploads are the phone shape itself (3636x1768), and YouTube adds the bars.
- **Clean source vs stream source.** The main channel's "hero" look needs a clean screen recording. A Kaatclip user who only has an OBS stream recording cannot get that look unless they record a clean game source too (see section 6).

### Gaps
- Loco VODs and older Kick VODs (before 3 Nov 2026) could not be checked, so the Loco and Kick source of specific videos is inferred, not proved. Whether he recorded clean phone video during streamed scrims (two parallel recordings) cannot be seen.
- Seven members-only streams and one members-only vlog could not be read.
- The 2024 stream-cut videos' platform is unknown; no 2024 source mentions Loco, Rooter or Kick.

## 3. How each content type is made (structure, devices, layout, length), with minute-by-minute examples

### Takeaway
Each type has a stable recipe, but the house style changed four times:
- **2020 to 2021:** music montages and raw phone clips.
- **Late 2022:** meme-heavy stream cuts, with captions naming speakers, film clips, TV-static stings and an "IN THIS VIDEO" opener.
- **2023:** music-backed stream cuts and phone highlights, with a "COMING SOON" or "IN THIS VIDEO" teaser.
- **Late 2023 onward:** comms-led phone highlights (40 to 130 words a minute), with a 15 to 25 s recycled teaser, an optional red panel and a WWCD or MVP ending.

Speech density is the clearest measurable shift. 2021 to mid-2023 highlights carry 1 to 19 wpm (music beds); late-2023 to 2026 ones carry 37 to 130 wpm (live comms).

### Cited Findings
**Audio, from captions of 38 main-channel videos (words a minute, and share of seconds with speech)** — this study's caption analysis:
- **Music-backed, 2021 to mid-2023:**
  - [gf-zwaTKXRs](https://www.youtube.com/watch?v=gf-zwaTKXRs) (2021): 1 wpm, 1%
  - [ew3PgA5cjwQ](https://www.youtube.com/watch?v=ew3PgA5cjwQ) (Oct 2022): 10, 8%
  - [xKPBU_NqbK0](https://www.youtube.com/watch?v=xKPBU_NqbK0): 6, 5%
  - [2c_XoSDSmmw](https://www.youtube.com/watch?v=2c_XoSDSmmw): 7, 6%
  - [lXLAytUgcTo](https://www.youtube.com/watch?v=lXLAytUgcTo): 5, 4%
  - [OOnDKF-Wprs](https://www.youtube.com/watch?v=OOnDKF-Wprs) (Sep 2023): 3, 4%
  - [6jVbUxDVZtg](https://www.youtube.com/watch?v=6jVbUxDVZtg) (Jan 2024): 10, 9%
- **Comms-led, from Sep 2023:**
  - [dZ_206yLWPY](https://www.youtube.com/watch?v=dZ_206yLWPY): 52 wpm, 42%
  - [fCsIPFa0EAs](https://www.youtube.com/watch?v=fCsIPFa0EAs): 51, 44%
  - [_elUiudgCM8](https://www.youtube.com/watch?v=_elUiudgCM8): 68, 49%
  - [bsezq1RtU7k](https://www.youtube.com/watch?v=bsezq1RtU7k): 130, 63%
  - [KmjTasCQZ5U](https://www.youtube.com/watch?v=KmjTasCQZ5U): 123, 61%
  - [6jIQaYvIOGc](https://www.youtube.com/watch?v=6jIQaYvIOGc): 96, 49%
  - [ml5FitUoqf8](https://www.youtube.com/watch?v=ml5FitUoqf8): 100, 50%
- **Montages and reels** sit lower: 42 to 72 wpm, 28 to 40% ([khbJdsEChm0](https://www.youtube.com/watch?v=khbJdsEChm0), [AZ5YmHyIDjc](https://www.youtube.com/watch?v=AZ5YmHyIDjc), [nk3MGVXKCFo](https://www.youtube.com/watch?v=nk3MGVXKCFo))

**Recipe by type**, from storyboards and captions:
- **A. Short clip (2021 to 2022, 10 to 100 s).**
  - Raw horizontal phone POV of one clutch, spray or banter beat, starting 0 to 3 s before the first shot and ending on the last knock or a reaction. No graphics, no teaser and no end card.
  - Examples: [-vbAZpx5Iek](https://www.youtube.com/watch?v=-vbAZpx5Iek) (25 s, one building fight), [BV9NcUSaLN4](https://www.youtube.com/watch?v=BV9NcUSaLN4) (39 s, scope sprays) and [gqZplWc5uxE](https://www.youtube.com/watch?v=gqZplWc5uxE) (44 s)
  - [ZZx4Viy3Kg0](https://www.youtube.com/watch?v=ZZx4Viy3Kg0) opens with 6 s of a "COMPETITIVE SCRIMS" stream frame, then cuts to clean POV
  - Titles are a hook plus emoji ("Why you Camp bro 😎") or "1vN {team}". Descriptions are hashtags only: 119 of 171 in 2021
- **B. Single-match highlight.**
  - **2023 to 2024 phone versions:** black, then a teaser under a red "IN THIS VIDEO" label (0:04 to 0:24), then black, then the drop at 0:34, then the match in order, then WWCD (8:07) and the results table (8:17). Example: [9pG_cQv0-oA](https://www.youtube.com/watch?v=9pG_cQv0-oA), detailed below.
  - **2025 to 2026 versions:** the same skeleton, with a "COMING SOON" or "in this video -" label, an optional red panel and an MVP ending (goblin_deep.md).
  - **Stream-cut versions:** the overlay is kept; a facecam reaction intro or zoom may be added ([_elUiudgCM8](https://www.youtube.com/watch?v=_elUiudgCM8), below).
  - Lengths: medians of 357 s (May 2023 to Dec 2024) and 486 s (2025 to 2026).
- **C. Tournament or day reel (multi-match).**
  - Opens on 3 to 5 short fights from several matches, then one match's endgame, or frag after frag with map and skin changes every 5 to 15 s.
  - Phone POV, sometimes with broadcast inserts. Examples: [S6qC9msN3VA](https://www.youtube.com/watch?v=S6qC9msN3VA) (frames change every 5 to 10 s, 3644x1772), [nk3MGVXKCFo](https://www.youtube.com/watch?v=nk3MGVXKCFo) and [6jIQaYvIOGc](https://www.youtube.com/watch?v=6jIQaYvIOGc)
  - Since 2025 its thumbnail is a raw gameplay frame
- **D. Frag or clutch montage (2 to 4 min).** Music-led kill reel with no result screen. Examples: [WetiQFqJ3W8](https://www.youtube.com/watch?v=WetiQFqJ3W8), [AZ5YmHyIDjc](https://www.youtube.com/watch?v=AZ5YmHyIDjc) and [3a8bRvJi1aA](https://www.youtube.com/watch?v=3a8bRvJi1aA). In 2020 the "T1 montage" versions were exactly 60 to 61 s long (10 videos)
- **E. TDM or custom battle (6 to 19 min).**
  - Phone POV of every round in order; very little is cut because a TDM round has no looting.
  - [_HMq3jgPsk8](https://www.youtube.com/watch?v=_HMq3jgPsk8) (1,122 s): the red side panel runs 0:00 to about 10:20, the image is plain letterboxed after 10:29, and the video ends on "MVP" and "VICTORY" screens at 18:22 to 18:32
  - [CjtBdcq1rqI](https://www.youtube.com/watch?v=CjtBdcq1rqI) (708 s) has a lobby or rematch screen at 3:22 to 3:27 ("REMATCH DUE TO OPPONENTS EXITED")
- **F. Challenge or funny stream cut (2022 to 2023, 4 to 5.5 min).** Example: [gs8thi_U_fU](https://www.youtube.com/watch?v=gs8thi_U_fU), detailed below. It has the stream overlay, a facecam, speaker-labelled yellow captions, film and news meme inserts, and an "IN THIS VIDEO" opener.
- **G. Vlog or IRL (10 to 20 min).** A home talking-head intro, then a handheld 4K camera following the day. It can carry a sponsor segment ([UFh9nf8TjsA](https://www.youtube.com/watch?v=UFh9nf8TjsA): a product unboxing and shave at 3:03 to 3:33) and a broadcast insert of the match day. One credited track: "Makai Symphony – Dragon Castle" (CC-BY-NC) on a vlog (goblin_deep.md).
- **H. Sponsored, gift or unboxing.** A multi-camera studio shoot with titled product shots ("LENOVO LEGION 5I PRO", "16-INCH 16:10 WQXGA+ GAMING DISPLAY") and a skit opening — [2Co12jszI-4](https://www.youtube.com/watch?v=2Co12jszI-4). Also a group unboxing with an S8UL cast and selfie-cam cutaways — [Vjc1H9rt7xI](https://www.youtube.com/watch?v=Vjc1H9rt7xI)
- **I. Announcement or hype.** "YOUR MVP IS BACK !!" ([-JrLHbhdDK8](https://www.youtube.com/watch?v=-JrLHbhdDK8), 154 s, Oct 2023): a talking head of another person, a team cinematic, gameplay, broadcast clips and a "MY TERRITORY" title card. The 2022 ban-era posts ("Missed me ?", "Will be missing this", "PMWI ka kya hoga") are 31 to 91 s nostalgia clips that drew 318K to 397K views ([Y38BNXRajJU](https://www.youtube.com/watch?v=Y38BNXRajJU), [pwupWVc_LoM](https://www.youtube.com/watch?v=pwupWVc_LoM), [gqZplWc5uxE](https://www.youtube.com/watch?v=gqZplWc5uxE))

**Minute by minute (new in this study)**
- **[_elUiudgCM8](https://www.youtube.com/watch?v=_elUiudgCM8): "Legend League 20 Solo Kills" (612 s, Mar 2025, stream cut aligned to [TuxKc0QX2qg](https://www.youtube.com/watch?v=TuxKc0QX2qg))**
  - 0:00 to 0:14: blurred teaser of a car fight
  - 0:19 to 0:39: the facecam enlarged in mid-frame over the game (his reaction and talk). Captions from 0:28 align to stream 2:16:40, so the talk is from just before the match
  - 0:44: plane and parachute
  - 0:53 to 2:06: fights, from 2:20:35 to 2:21:49 in the stream
  - 2:29 to 4:28: short stretches of 3 to 30 s from 2:25 to 2:35
  - 4:58 to 6:06: 41 s and 13 s stretches (2:39 to 2:40)
  - 6:51 to 10:01: **one continuous 190 s final stretch** (2:42:38 to 2:45:48: car fights, scope, last zone)
  - 9:57: "WINNER WINNER CHICKEN DINNER"; 10:02 lobby; 10:07 fade; end at 10:12
  - Overall: the stream overlay (GOBLIN bar, "LE" logo, facecam bottom-right) is kept throughout. About 612 s were kept from a 1,748 s span (35%), in chronological order
- **[DFnr6WDiE6o](https://www.youtube.com/watch?v=DFnr6WDiE6o): "Top 10 Legend League Solo 21 Finishes" (649 s)**
  - 14 aligned stretches of 2 to 80 s, in order, from stream 3:51:21 to 4:13:25. That is 649 s of a 1,324 s span (49%)
  - It has 24 speech-free gaps of 6 s or more (music bridges, or quiet play)
- **[9pG_cQv0-oA](https://www.youtube.com/watch?v=9pG_cQv0-oA): "Solo 9 Finishes Chicken Dinner | Carnival Dominating Erangle" (507 s, May 2024, phone)**
  - 0:00 black; 0:04 to 0:24 teaser clips with a red "IN THIS VIDEO" stamp; 0:29 black
  - 0:34 the car to the drop; 0:44 to 1:28 the first compound
  - 1:58 and 3:31 map checks (shown full-screen); 1:28 to 5:15 buggy rotation and fights
  - 5:15 to 7:08 a smoke-covered field fight; 7:13 to 7:47 holding behind a tree
  - 7:52 to 8:02 the final shots; 8:07 WWCD banner; 8:12 to 8:17 results table; 8:22 fade
  - Overall: letterboxed phone with no facecam. The structure equals the 2025 to 2026 hero edits minus the side panel
- **[gs8thi_U_fU](https://www.youtube.com/watch?v=gs8thi_U_fU): "Flirting With A Girl Challenge 😂" (287 s, Sep 2022, stream cut)**
  - 0:00 to 0:03: lobby with an "IN THIS VIDEO" caption; 0:05: TV colour-bars sting
  - 0:07 to 0:13: yellow captions explaining the challenge ("LOBBY MEI BULAYENGE AUR...")
  - 0:21, 0:25, 0:33: film and celebrity reaction inserts. About every 10 to 15 s there is a meme cutaway: a Modi speech clip at 1:31, Arnab at 1:17, Amitabh at 2:28, a cartoon duck at 3:59
  - From 0:43: captions labelled with the speaker ("BEAST – …", "NEYO", "GOBLIN"); the facecam is zoomed in on reactions
  - 2:06 to 4:11: lobby chat with the girl, captioned line by line
  - Overall: the green GOBLIN stream overlay is on every gameplay frame
- **[Itq7dwuoGjc](https://www.youtube.com/watch?v=Itq7dwuoGjc): "A day well spent 🩷" (1,195 s, Jun 2026, vlog)**
  - 0:00 to 0:50: talking head at home
  - 0:59 to 1:48: loading supplies into a car
  - 1:58 to 3:57: a talk with a shelter worker in the open
  - 4:06 to 6:35: walking through a dog shelter
  - 6:44 to 10:22+: a sit-down with dogs
  - Overall: thumbnail text "LEFT WITH A FULL HEART"; no gameplay at all
- **[Vjc1H9rt7xI](https://www.youtube.com/watch?v=Vjc1H9rt7xI): "I bought a Mystery box worth ₹800000+" (708 s, Apr 2026)**
  - 0:00 to 0:39: a solo sofa intro cut against group shots
  - From 0:44: six to seven people open boxes around a table, with reaction close-ups
  - 2:23 and 3:18: selfie-cam cutaways of another creator in a car
  - Overall: an edited, camera-shot version of the 1.2 h live unboxing stream [kiqDrenoFP4](https://www.youtube.com/watch?v=kiqDrenoFP4)
- **Earlier minute maps** (goblin_deep.md): [-vFxWHPrv2s](https://www.youtube.com/watch?v=-vFxWHPrv2s), [bsezq1RtU7k](https://www.youtube.com/watch?v=bsezq1RtU7k), [6jIQaYvIOGc](https://www.youtube.com/watch?v=6jIQaYvIOGc) and three @goblinsh0rts stream cuts

**Layout and frame by era (main channel)**
- 2020 to 2022: phone 1920x886, or 1920x1080 and 3840x2160 letterboxed
- 2022 to 2024 stream cuts: 16:9 with the bottom overlay
- Mid-2023 on: some phone uploads at 3840x1772 (2.17:1)
- Nov 2025 to Feb 2026: the red side panel
- May to Aug 2026: 3630 to 3644 x 1768 phone-shaped, with no panel
- No kill counter or chapters were seen. The only chapters are YouTube auto-chapters on 2 videos ([MhXerSIXoRA](https://www.youtube.com/watch?v=MhXerSIXoRA), [wKQrIEJsyVg](https://www.youtube.com/watch?v=wKQrIEJsyVg))
- Source: yt-dlp width and height, plus storyboards

### Inferences
- **The most important edit change** for Kaatclip is the switch, around Sep 2023, from music-bed edits to **live comms**. Since then every main-channel match video is "the match told in comms": the comms are the soundtrack, and music appears only in teasers, montages and gaps.
- **The 2022 meme style** (speaker-labelled captions, film cutaways, TV-static stings) drew 198K to 329K views, the best long-form numbers of its year. It fit a period when there were no tournaments (the ban) and the content was banter. A comedy-heavy Kaatclip mode is valid for creators whose streams are banter-driven.
- **Hero edits are low-graphics and template-friendly:**
  - a teaser label;
  - black or logo beats;
  - an optional panel;
  - a WWCD, MVP or results ending;
  - the facecam-zoom intro on stream cuts.

### Gaps
- Storyboards are 1 frame every 2 to 10 s, so transitions under 2 s, exact caption timing and on-screen text in small frames could not be measured. Music titles are not credited (except one vlog), so the music cannot be identified.
- The editor or editors are not publicly named. Searches found no credit, and descriptions credit no one.

## 4. His live streams (Kaatclip's input): titles, schedule, length, what happens, overlays and facecam

### Takeaway
His public YouTube streams are **scrims plus UC crate openings**, 2 to 7 h long (median 4.6 h in 2026), starting at 19:00 to 21:00 IST.
- **Structure:** a full-screen facecam just-chatting opener (5 to 23 min), then a series of scrims matches (about 20 to 25 min each), separated by 5 to 15 min of lobby, inventory and crate-opening screens.
- **Overlay:** a sponsor banner along the bottom (iQOO since May 2025) and a facecam bottom-right, with the game full-width above.
- **Other formats:** IRL team streams, launch-event streams and milestone "Champions are Live" streams.
- **Since Jun 2026**, his daily grind (afternoon scrims) is on Kick, so the public YouTube streams are the occasional, event-like ones.

### Cited Findings
- **Counts and lengths per year (public):**

| Year | Streams | Median length | Range | Median views |
|---|---|---|---|---|
| 2021 | 10 | 2.0 h | 0.7–2.8 h | 15K |
| 2022 | 6 | 1.2 h | | 346K |
| 2023 | 7 | 2.5 h | | 228K |
| 2024 | 13 | 3.3 h | 0.3–8.2 h | 175K |
| 2025 | 32 | 2.6 h | 0.4–8.6 h | 197K |
| 2026 | 25 | 4.6 h | 1.2–9.8 h | 237K |

  - Start times in 2026: 19:00 to 19:59 (9 streams), 20:00 to 20:59 (8), 21:00 to 21:59 (3). Weekdays, 2025 to 2026: Mon 14, Sun 9, Thu 9, Sat 8, Wed 7, Tue 6, Fri 4 — [@goblinbgmi/streams](https://www.youtube.com/@goblinbgmi/streams)
- **Title keywords across the 93 public streams.** "scrims" 39, crate or UC opening 31, tournament, POV or event 16, Ultimate Royale 6, classic 5, IRL 4, other games ("Chained Together", "CookieRun") 2. The 2026 template is "{N} UC {skin} Opening | Scrims | GoBLiN is Live BGMI! 🚀 #iQOO" — [@goblinbgmi/streams](https://www.youtube.com/@goblinbgmi/streams)
- **Top streams are milestone streams:**
  - "Your MVP is Live" (13 Jun 2022, 729K, [2DELA_LkTsU](https://www.youtube.com/watch?v=2DELA_LkTsU))
  - "⭐⭐The Champions are Live⭐⭐" (30 Mar 2026, after BGIS 2026, 678K, [yVe2RAkxznE](https://www.youtube.com/watch?v=yVe2RAkxznE))
  - "iQOOSouLGoBLiN is Back" (2 May 2025, 650K, [a2v-VmoND6w](https://www.youtube.com/watch?v=a2v-VmoND6w))
  - "The Champions are Home" (26 Oct 2026, after BMSD, 641K, [Kc_K_IPw4X0](https://www.youtube.com/watch?v=Kc_K_IPw4X0))
- **Inside a 2026 stream: "60000 Uc Crate opening | PMGC Grind"** ([GVKHZ9-erB8](https://www.youtube.com/watch?v=GVKHZ9-erB8), 7:07:42), sampled once a minute from the full storyboard:
  - 0:00 to 23:00: full-screen facecam talk
  - 23:58 to 44:58: match 1 (Miramar), with "MVP" at 44:58
  - 46:57 to 58:57: inventory grids, crate screens and black
  - 59:57 to 1:14:56: match 2, with MVP at 1:14:56
  - Further matches follow, separated by lobby and crate grids (1:32 to 1:35, 1:53 to 1:58, 2:25 to 2:31, 2:58 to 3:08, 3:30 to 3:42)
  - From about 3:43: back-to-back matches with short lobbies, to the end
  - The earlier map of this stream puts one match at 2:33:13 (plane) to 2:56:12 (#2) (goblin_deep.md)
- **Feb 2026 stream** ([yUuB2x9H0Qg](https://www.youtube.com/watch?v=yUuB2x9H0Qg), 4:22:22): a 5 min facecam opener, plane at 4:59, then matches about every 25 to 30 min. There are crate or lobby blocks at about 52 to 58 min and 2:47 to 2:53, and a full-screen facecam ending from 4:15 — storyboard
- **Talk density.** In 23 streams with captions he speaks 75 to 137 words a minute on average, with speech starting 0 to 101 s in. Talk covers chat, Kick, memberships ("member" up to 48 mentions a stream), crate openings and comms. This is this study's caption count.
- **Overlay and facecam by era**, from mid-stream frames of all 93 public streams (`mid_streams_a/b.jpg`):
  - 2021: phone feed with an orange "insane Goblin" bar and no facecam
  - 2022 to 2023: green GOBLIN bar plus a facecam bottom-right
  - 2024: red GOBLIN bar plus facecam (Carnival)
  - Early 2025: green bar with an "LE" logo
  - May 2025 onward: a rotating iQOO phone banner (iQOO Z10, Neo 10, 15, 15R, Z11x), "amazon specials" and the facecam bottom-right
  - IRL streams: camera only
- **Description template (2026).** Instagram, Kick, Shorts channel, the membership join link, donation (UPI), an "About me" block ("Esports Player for iQOOSouL Esports • Content Creator for S8uL Esports • Mumbai"), gear ("Device : iQOO Neo 10"), chat rules and hashtags. One stream adds a sponsor line ("Buy Pokémon TCG in India – tcgrepublic.in") — [GVKHZ9-erB8](https://www.youtube.com/watch?v=GVKHZ9-erB8), [Jb-BjVy5vLE](https://www.youtube.com/watch?v=Jb-BjVy5vLE)
- **Stream thumbnails** are designed every time: his face plus "GOBLIN IS LIVE" or crate or skin art, with templates reused across many streams — thumbnails of all 100 streams (`th_s.jpg`)
- **Engagement.** Streams have a median like rate of 6.9% and 0.36 comments per 1,000 views (2023+). Highlights have 8.5% and 1.71 — yt-dlp metadata

### Inferences
- A Goblin stream gives Kaatclip **8 to 15 matches per 7 h**, each with clear boundaries:
  - **Start:** plane or parachute after an inventory or lobby screen.
  - **End:** result or MVP screen.
  - **Between matches:** 5 to 15 min blocks that are never used in highlights: crate grids, inventory, full-screen facecam.

  A match segmenter should treat "full-screen facecam" and "inventory or crate grid" as non-gameplay states.
- **Crate openings** recur in 31 of 93 titles and are the hook of most 2026 stream titles. @goblinsh0rts turns them into separate videos (goblin_deep.md). They are a distinct, detectable unit: grid screens, then a reward animation, then a loud reaction.
- **The sponsor banner and facecam** are fixed in place (bottom strip, bottom-right box), so a crop to the game area above the banner is a stable transform for this creator.

### Gaps
- Kick streams (the daily afternoon grind) could not be studied beyond 3 VODs' metadata and clip thumbnails; Kick VOD contents were not opened.
- Super Chat and membership revenue, and stream chat logs, were not read.

## 5. Titles, thumbnails, descriptions, playlists, end screens, timing, and what performs best

### Takeaway
- **Titles:** a stat formula ("Solo {k} Finishes WWCD | {team} Finishes | {event}") plus emojis, with people and opponent names in about a third.
- **Thumbnails:** designed face-cutout art with big numbers for single-match hero edits (2023 to 2026). Raw gameplay frames for tournament reels and frag reels (since 2025) and for all 2021 to 2022 clips.
- **Descriptions and playlists:** hashtag-only descriptions; no playlists and no manual chapters.
- **Timing:** match highlights go up during or within days of the tournament, and stream cuts about 17 to 18 h after the stream.
- **What performs:** reach follows status (the MVP or champion moments) and story (comeback, decider, a named rival). Within 2023 to 2026, titles naming people or opponents have the highest median views (165K), and kill-number titles the lowest (130K).

### Cited Findings
- **Title features of 72 match-type videos (May 2023 onward), median views**: all 154K; event name 160K (n=38); result 152K (30); people or opponent 165K (24); kill number 130K (40); hook word 150K (27) — computed from [@goblinbgmi/videos](https://www.youtube.com/@goblinbgmi/videos)
- **Thumbnails** (all 380 viewed as mosaics `th_v0/1/2.jpg`):
  - 2023 to early 2026 single-match videos use his face cutout plus a large "SOLO {k} FINISHES", "WWCD" or "DOMINATION" text, with team or event logos. Examples: [bsezq1RtU7k](https://www.youtube.com/watch?v=bsezq1RtU7k), [ml5FitUoqf8](https://www.youtube.com/watch?v=ml5FitUoqf8), [67w15TWdikI](https://www.youtube.com/watch?v=67w15TWdikI)
  - The 2022 challenge videos use face collages of S8UL friends plus a comic headline ("FLIRTING WITH A GIRL – CHALLENGE GONE WRONG", [gs8thi_U_fU](https://www.youtube.com/watch?v=gs8thi_U_fU))
  - Since May 2025, tournament reels use a raw letterboxed gameplay frame with no text: [4rDLrncqmCc](https://www.youtube.com/watch?v=4rDLrncqmCc), [6jIQaYvIOGc](https://www.youtube.com/watch?v=6jIQaYvIOGc), [PiGMtVEVJKw](https://www.youtube.com/watch?v=PiGMtVEVJKw), [xWvORedYbOs](https://www.youtube.com/watch?v=xWvORedYbOs), [nk3MGVXKCFo](https://www.youtube.com/watch?v=nk3MGVXKCFo), [khbJdsEChm0](https://www.youtube.com/watch?v=khbJdsEChm0), [S6qC9msN3VA](https://www.youtube.com/watch?v=S6qC9msN3VA), [p9OVVBLMo-8](https://www.youtube.com/watch?v=p9OVVBLMo-8), [AZ5YmHyIDjc](https://www.youtube.com/watch?v=AZ5YmHyIDjc)
  - 2021 to 2022 clips show raw frames (scope, fight)
- **Descriptions by year:**

| Year | Empty | Hashtags only | Links or about | Text |
|---|---|---|---|---|
| 2020 | 52 | 0 | 2 | 15 |
| 2021 | 46 | 119 | 0 | 6 |
| 2022 | 4 | 43 | 1 | 4 |
| 2023 | 0 | 30 | 9 (the Loco link block) | 0 |
| 2024 | 0 | 17 | 3 | 0 |
| 2025 | 0 | 14 | 0 | 1 |
| 2026 | 6 | 3 | 2 | 0 |

  - The tag list is the median 22 tags in 2023 to 2025, and 0 in 2020 to 2022 and 2026 — yt-dlp metadata
- **No playlists tab and no manual chapters** — [@goblinbgmi](https://www.youtube.com/@goblinbgmi/videos)
- **Upload hour (IST, 2023+):**
  - Single-match highlights: 12:00 to 13:59 (12), 18:00 to 19:59 (11), 16:00 to 17:59 (10), 20:00 to 21:59 (7)
  - Tournament reels: 10:00 to 11:59 (6 of 12)
  - Streams start 18:00 to 21:59 (39 of 53)
  - Weekdays for 2023+ videos: Mon 17, Tue 16, Wed 14, Sun 11, Fri 10, Thu 10, Sat 7 — yt-dlp timestamps
- **Timing against events:**
  - BGMS 2026 ran 10 Aug to 6 Sep; uploads came on 16, 25, 29 and 31 Aug
  - CEGC 2025 ran 14 to 16 Nov; uploads came on 10, 16 and 17 Nov
  - BMPS 2026 ran 6 May to 21 Jun; uploads came on 5 May and 4 Jun
  - BGIS 2026 ran 17 Jan to 29 Mar; uploads came on 13 Jan and 23 to 24 Feb
  - Event dates are from [esportsverse](https://www.esportsverse.live/players/goblin); upload dates are from [@goblinbgmi/videos](https://www.youtube.com/@goblinbgmi/videos)
  - Stream cut lag: 16.8 to 17.7 h after the stream ended (the two Legend League pairs, section 2)
- **Engagement (2023+), median like rate:** announcements 18.9%; sponsor 12.3%; vlog 11.3%; single-match 8.5%; montage 8.0%; streams 6.9%; tournament reels 6.3%; TDM 5.1%. Comments per 1,000 views run 1.5 to 2.9 for videos and 0.36 for streams — yt-dlp metadata
- **Best performers by type since May 2023:**
  - TDM or custom: median 339K, n=5 ([MQ8SC-_e8ZQ](https://www.youtube.com/watch?v=MQ8SC-_e8ZQ) 382K; [C76kBoyodHY](https://www.youtube.com/watch?v=C76kBoyodHY) 383K)
  - Tournament reels: 207K
  - Single-match highlights: 134K
  - Montages: 116K
  - Vlogs: 57K to 144K
  - Source: [@goblinbgmi/videos](https://www.youtube.com/@goblinbgmi/videos)
- **Phone vs stream source.** Phone-sourced match videos (May 2023 to Jun 2024) have a median of 169K views (n=26); stream-cut match videos in the same window have 124K (n=10). This is computed from this study's source map.
- **End screens.** Not readable through yt-dlp (no data)

### Inferences
- **What performs.** For this channel, the strongest performers are status and rivalry moments: an MVP, a LAN, "India vs Korea" (Drx), "New SouL vs Old SouL" or a teammate 1v1. Single-match stat titles perform steadily but lower.
- **The source comparison is confounded.** Tournament POV beat scrims stream cuts, but tournaments also carry higher stakes, so the difference is not proof that a clean frame helps.
- **Thumbnail effort follows the format.** A hero match video gets a designed face-plus-number thumbnail. A reel or a time-sensitive tournament upload gets a raw frame. Kaatclip can mirror this: suggest a designed template for the hero cut, and the best gameplay frame for quick cuts.

### Gaps
- End screens, cards and pinned comments are not exposed by yt-dlp and were not seen.
- Views are a snapshot on one day, not normalised by age.
- The title-feature medians overlap (one title can have several features) and the groups are small, so the differences are indicative only.

## 6. What this means for an automatic tool: which types Kaatclip can make from a stream recording, the signals each needs, and what is out of reach

### Takeaway
From a creator's own OBS stream recording, Kaatclip can produce **five of Goblin's types well**:
- the single-match highlight in the stream-cut style (overlay kept);
- the multi-match day reel;
- the short clutch clip, horizontal or as a stacked Short;
- the crate-opening cut;
- the TDM or custom-room session.

It can produce the **hero edit** (clean HUD, phone shape, red panel, comms only) only if the creator also records a clean game source; cropping the stream frame can approximate it. Vlogs, sponsored skits, multi-camera unboxings and broadcast-insert tournament edits are **out of reach** from a stream file.

### Cited Findings (evidence each conclusion rests on)
- **Stream cut works as a main-channel format:** the main channel itself published 30 stream-cut long videos in 2022 to 2025, overlay and facecam kept. Two are proved to be single-match cuts of 35% and 49% of a span, in time order, ending on WWCD ([_elUiudgCM8](https://www.youtube.com/watch?v=_elUiudgCM8), [DFnr6WDiE6o](https://www.youtube.com/watch?v=DFnr6WDiE6o))
- **The hero look needs a clean recording:** all phone-sourced highlights are 2.06 to 2.17:1 full-HUD screen recordings with no facecam (section 2), and his stream frame always has a banner and facecam ([GVKHZ9-erB8](https://www.youtube.com/watch?v=GVKHZ9-erB8))
- **Day reels:** 18 on the main channel, median 174K views; they open on fights from several matches and use raw-frame thumbnails ([nk3MGVXKCFo](https://www.youtube.com/watch?v=nk3MGVXKCFo), [6jIQaYvIOGc](https://www.youtube.com/watch?v=6jIQaYvIOGc))
- **Short clips:** 187 on the main channel, median 32 s, each one clutch or one banter beat, starting 0 to 3 s before the first shot ([-vbAZpx5Iek](https://www.youtube.com/watch?v=-vbAZpx5Iek), [BV9NcUSaLN4](https://www.youtube.com/watch?v=BV9NcUSaLN4))
- **Crate openings:** in 31 of 93 stream titles; separate crate-opening videos exist on @goblinsh0rts (goblin_deep.md)
- **Comms over music:** since late 2023, match edits run 37 to 130 wpm of comms (section 3)
- **Out of reach:**
  - camera vlogs ([Itq7dwuoGjc](https://www.youtube.com/watch?v=Itq7dwuoGjc));
  - studio unboxings ([Vjc1H9rt7xI](https://www.youtube.com/watch?v=Vjc1H9rt7xI));
  - sponsor skits ([2Co12jszI-4](https://www.youtube.com/watch?v=2Co12jszI-4));
  - broadcast inserts, which need the tournament VOD ([zw_7pRPDyK0](https://www.youtube.com/watch?v=zw_7pRPDyK0));
  - meme film inserts ([gs8thi_U_fU](https://www.youtube.com/watch?v=gs8thi_U_fU)), which need licensed or third-party clips

### Inferences (rules and signals for Kaatclip)
1. **Single-match highlight (stream-cut style), the default.**
   - *Segmenter:* states for full-screen facecam, inventory or crate grid, lobby, plane or parachute, in-match and result. Use the result screen (WWCD, "#N", MVP) as the end anchor.
   - *Cut list:* every fight stretch in order, with the final circle whole (Goblin's final stretch was 190 s in [_elUiudgCM8](https://www.youtube.com/watch?v=_elUiudgCM8) and 142 to 162 s in goblin_deep.md). End 5 to 15 s after WWCD or MVP, or on a facecam reaction.
   - *Keep ratio:* 25 to 50% of the match span.
   - *Signals:* the kill feed, the "Remaining N" counter, result-screen text (OCR), comms speech rate and loudness, and the facecam reaction (audio peaks).
   - *Options:*
     - a facecam-zoom intro (his talk just before the match, as at 0:19 to 0:39 of _elUiudgCM8);
     - a 10 to 25 s teaser from the final fight with a label ("IN THIS VIDEO", "COMING SOON").
2. **Hero variant** (when a clean game recording is available, e.g. an OBS source recording or a phone screen recording):
   - the same cut list, rendered from the clean file;
   - 16:9 with a branded side panel, or the phone shape left as is;
   - comms only, no music under the action;
   - a WWCD, MVP and results ending.

   Without a clean file, offer a crop above the sponsor banner. Goblin's stream banner and facecam sit in a fixed bottom strip and the bottom-right corner, so this crop is stable. **Warn** that the facecam corner overlaps the game.
3. **Day reel:** pick the 3 to 5 best fights across all matches of the stream for a 30 to 60 s opener, then the best match's endgame. Length 4 to 11 min; use a raw best-frame thumbnail.
4. **Short clip or Short:**
   - the top clutch (1vN), a multi-knock spray or a banter beat;
   - start 0 to 3 s before the first shot and end at the last knock, plus up to 3 s of reaction;
   - 10 to 60 s long; horizontal for a "clip", or stacked game over facecam for Shorts (the goblin_deep.md Shorts rules).
5. **Crate-opening cut:**
   - *Detection:* crate grid screens, the reward animation, and the speech or loudness spike of the reaction.
   - *Unit:* one session of 3 to 10 min, a distinct video in his ecosystem.
6. **TDM or custom-room session:**
   - *Detection:* a TDM HUD (round timer, score) or custom-room mode.
   - *Cut:* keep all rounds and drop respawn waits and lobby, which keeps 43 to 48% (goblin_deep.md).
   - *Ending:* VICTORY or MVP. TDM and custom battles are this channel's best-performing long format (median 339K, n=5 since 2023).
7. **Packaging helpers:**
   - Titles from a stat template plus a people or opponent template; people titles do better.
   - Hashtag-only descriptions plus the creator's link block.
   - No chapters.
   - Suggested posting time: the next day at 12:00 to 14:00 IST, or within 24 h of a tournament day.
8. **Out of reach, so tell the user:**
   - camera vlogs, sponsored skits, multi-camera unboxings;
   - tournament broadcast inserts, unless the user supplies the broadcast VOD;
   - the clean hero look, unless a clean recording exists;
   - meme film inserts, which carry copyright risk.

### Gaps
- Not verified on Goblin's own raw files:
  - whether the "iQOO" banner and facecam positions stay fixed across all 2026 streams (the mid-frames suggest yes);
  - whether his Kick VODs carry identical audio.
- The TDM rules rest on 2 mapped sessions (goblin_deep.md) and 9 main-channel examples, and the day-reel rule on 18 examples viewed at storyboard resolution. All thresholds need tuning on the owner's own test streams.
