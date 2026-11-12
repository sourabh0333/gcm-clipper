# One stream feeds a week of videos

Goblin, Joker and LoLzZz each run two YouTube pipelines, and the line between them is the same for all three: **the second channel is fed by the creator's own stream recording, cut with the overlay and facecam left in**, while the main channel holds something a stream cannot give. For Joker that is camera-shot vlogs (86 of 89 main-channel uploads in 2025-26). For Goblin it is about one clean phone-recorded tournament edit a month. LoLzZz is the exception: his main channel still runs on his own stream, but it takes only the night's headline record match, about 16 edited videos a year against roughly 250 streams. Inside the stream-fed channels, **the stream segment decides the video**: a classic match becomes a match cut, a custom room becomes a round-by-round session, a crate opening becomes a pull-by-pull reaction video, a chat answer becomes a talk clip. Each type has its own keep ratio, length and ending, measured below from caption-aligned source maps. Across all six channels, **titles and videos built on people and rivalry beat kill numbers**, custom rooms and TDM are the strongest stream-only long format, and crate openings are cheap and frequent but only mid-table on views. All three creators have also streamed off YouTube (Loco in 2022-23, Kick in 2026), so a local OBS recording is the right input, and Kaatclip already accepts it. Between a third and a half of each second channel's long videos are within reach of a tool that edits one creator's own recording. The rest need someone else's footage: an opponent's stream, a tournament broadcast, a creator video being reacted to, or a camera. This report covers what each creator makes, how, and what that means for Kaatclip. It contains no build plan.

Evidence: six channel studies made on 12 Nov 2026 from public YouTube data only (yt-dlp metadata, auto-captions, storyboards, heatmaps, thumbnails; no video or audio downloaded). Source claims rest on matching a video's Hindi auto-captions word by word against stream captions: about 40 Goblin pairs, 19 Joker pairs and 14 LoLzZz pairs. Views are a one-day snapshot. "(Inference)" marks reasoning beyond what was measured. All times are IST.

## 1. Summary for the owner: ten things that change how Kaatclip should think

| # | What we learned | What it means for Kaatclip |
|---|---|---|
| 1 | **Two pipelines per creator.** Second channels run on the creator's own stream (overlay kept). Joker's main is now camera vlogs; Goblin's main is clean phone edits; LoLzZz's main takes only headline records from his stream. | Kaatclip's natural home is the second channel, plus LoLzZz-style record videos on a main channel. |
| 2 | **A stream is a variety show, not one long match.** Facecam chat (5-35 min), crate and inventory blocks (5-15 min), other games, watch parties and matches sit in one file. | Split the stream into segments first, then rank inside each segment. Never rank 5 hours as one pool. |
| 3 | **The segment decides the recipe.** One match, one custom-room bout, one crate session, one chat answer: each has its own keep ratio (3-65%), length and ending. | One "highlight" template mis-cuts crates and custom rooms. Each segment type needs its own recipe. |
| 4 | **Laughter alone mis-ranks.** In Joker's streams, GTA RP and Among Us carry 2-4 times more laughter tags than BGMI, and laughter piles up late in the stream. | If the promise is BGMI highlights, laughter must be read inside BGMI segments only. |
| 5 | **People beat kill numbers** on every channel: named teammates, rivals or co-stars lift median views by roughly 1.2x to 2x. | Default titles should name the people in the lobby when Kaatclip can find them; the kill number goes second. |
| 6 | **Custom rooms and TDM are the strongest stream-only long format.** Goblin's second channel: 89K median, all 22 cut from his stream. LoLzZz's TDM hits (847K) are two-POV, though. | A single-POV custom-room session is proven and in reach; the cross-cut rivalry version is not. |
| 7 | **Crate openings are cheap, frequent and detectable, but mid-table.** They recur in a third of Goblin's stream titles, yet as videos they draw 31K-177K medians, below match and session cuts on most channels. | A low-effort extra product, not a headline feature. |
| 8 | **Streams moved partly off YouTube.** Loco in 2022-23 (Joker proven, Goblin inferred), Kick from Jun 2026 (Goblin) and from 22 Sep 2026 on alternate days (LoLzZz). | Local OBS files, which Kaatclip already takes, are the right input. A YouTube-link-only tool would miss whole streams. |
| 9 | **One stream becomes a batch drip-fed over days.** Goblin's 9.75 h stream gave 4 long videos, a crate video and 2 Shorts over 11 days; first cuts land 17-30 h after the stream. | Offer a batch per stream with a suggested posting schedule, not one video. |
| 10 | **Half or more of each second channel's long videos are out of reach.** Opponent POVs (LoLzZz Plays' 135 "vs streamer" videos), LAN broadcasts (105 Goblin videos), reactions to others' videos, camera vlogs and clean phone edits all need footage that is not in one stream file. | Say plainly in the product what Kaatclip does not make, and do not chase these. |

## 2. Each creator, both channels

### Goblin: a clean-phone hero channel and a stream-cut volume channel

Goblin's two channels split cleanly. **@goblinbgmi** has 380 videos, 100 streams and only 4 Shorts. Since May 2023 its regular upload is one long tournament highlight cut from a clean phone screen recording, about one a month in 2025-26, clustered around events ([@goblinbgmi/videos](https://www.youtube.com/@goblinbgmi/videos)). **@goblinsh0rts** (131K subscribers) is the volume channel: 526 long videos and 438 Shorts, with Shorts bringing **77% of its 107.7M views** ([@goblinsh0rts/shorts](https://www.youtube.com/@goblinsh0rts/shorts)).

| | @goblinbgmi (main) | @goblinsh0rts (second) |
|---|---|---|
| Output now | 11 videos in 2026, 25 public streams | 112 long videos and 86 Shorts in 2026 |
| Main source | Clean phone recording (2.06-2.17:1, full HUD, no facecam) | His own stream, overlay and facecam kept (292 of 526 long videos) |
| Other sources | Broadcast inserts, camera vlogs, 2 stream cuts in 2025 | Clean phone POV (104), LAN broadcast (105), camera (24) |
| Shorts | 4 in total | 438; stacked stream layout most common |
| Editing | Comms-led hero edit with a teaser label and a WWCD/MVP ending | Light: cold open, facecam punch-ins, round and result screens kept |

**Content types and what each is based on.** The main channel's mix went through five phases, from 2021's near-daily 30-second clutch clips to today's monthly hero edit ([@goblinbgmi/videos](https://www.youtube.com/@goblinbgmi/videos)). The second channel's long-video types are the richer set for Kaatclip:

| Type (channel) | n | Median length | Median views | Footage source |
|---|---|---|---|---|
| Single-match highlight (main) | 116 | 355 s | 71K (134K since May 2023) | Phone recording; stream cut in 2022-24 |
| Tournament or day reel (main) | 18 | 332 s | 174K | Phone POV plus broadcast inserts |
| TDM or custom room (main) | 9 | 568 s | 196K (339K since 2023, n=5) | Phone POV |
| Challenge or funny stream cut (main, 2022-23) | 8 | 265 s | 231K | Stream (Loco era, inferred) |
| Short clutch clip (main, 2020-23) | 187 | 32 s | 26K | Phone POV, horizontal |
| Match or scrims cut (second) | 91 | 175 s | 34K | Stream 58, POV 33 |
| Clutch clip (second) | 110 | 56 s | 29K | Stream 82, POV 28 |
| TDM/WOW custom room (second) | 22 | 442 s | **89K** | Stream, 22 of 22 |
| Classic solo-vs-squad pub (second) | 25 | 428 s | 58K | Stream 14, POV 11 |
| Funny or banter edit (second) | 49 | 105 s | 49K | Stream, 43 of 49 |
| Talk or news clip (second) | 27 | 95 s | 36K | Stream, 23 of 27 |
| Crate opening (second) | 17 | 360 s | 31K | Stream, 17 of 17 |
| LAN broadcast match (second) | 73 | 239 s | 19K | Official broadcast |
| Vlog or celebration (second) | 22 | 621 s | 54K | Camera |

The main channel's hero edits do **not** come from his YouTube streams. Thirty-one stream-cut and phone videos from 2021-24 were aligned against all 26 captioned YouTube streams of that period, and none matched: the best score was 10, against 192-603 for real pairs ([streams tab](https://www.youtube.com/@goblinbgmi/streams)). The two proven main-channel pairs are "Legend League 20 Solo Kills" ([_elUiudgCM8](https://www.youtube.com/watch?v=_elUiudgCM8)), cut from stream [TuxKc0QX2qg](https://www.youtube.com/watch?v=TuxKc0QX2qg) and keeping 35% of a 29-minute span in order, and "Top 10 Legend League Solo 21 Finishes" ([DFnr6WDiE6o](https://www.youtube.com/watch?v=DFnr6WDiE6o)), keeping 49%. Both went up 17-18 h after the stream. On the second channel, caption matching proves 40 long videos and 15 Shorts were cut from his streams, for example the crate video [2GJtTk-s_94](https://www.youtube.com/watch?v=2GJtTk-s_94) from stream [h4LBvmiT8yg](https://www.youtube.com/watch?v=h4LBvmiT8yg), uploaded 18.4 h later.

**How the main channel's hero edit is made.** The house style changed around Sep 2023 from music-bed edits (1-19 words a minute) to **comms-led edits (37-130 words a minute)**. Since then, the comms are the soundtrack, and music appears only in teasers and gaps ([bsezq1RtU7k](https://www.youtube.com/watch?v=bsezq1RtU7k), 130 wpm). The skeleton is fixed. In [9pG_cQv0-oA](https://www.youtube.com/watch?v=9pG_cQv0-oA) (507 s) it runs: black, a 20-second teaser under a red "IN THIS VIDEO" stamp, black, the drop at 0:34, the match in order, the WWCD at 8:07 and the results table at 8:17. From Nov 2025 to Feb 2026 the phone image sat inside a red branded side panel; since May 2026 it is uploaded in the phone's own shape. There is no kill counter and there are no chapters.

**How the second channel cuts each type.** The editing is light and formulaic. Stream cuts keep the frame untouched and add a 15-20 s "IN THIS VIDEO -" cold open, full-screen facecam punch-ins, and, in funny edits only, 2-6 meme inserts. Custom rooms keep **26-65% of the session** in 9-25 stretches, dropping respawn waits and keeping the game's "VICTORY" and "DEFEAT" cards. The 2v2 WOW [7TkLt-j3u4A](https://www.youtube.com/watch?v=7TkLt-j3u4A) (905 s, 272K) has punch-ins at seven points and ends on his face. Crate videos alternate reveal screens with facecam reactions every 5-15 s and run at about 120 words a minute. Talk clips are one continuous chat answer over the lobby screen, 95 s median at 163 words a minute ([Qw5AGoqlUks](https://www.youtube.com/watch?v=Qw5AGoqlUks)).

**His streams as input.** Public YouTube streams are scrims plus UC crate openings: "scrims" is in 39 of 93 titles and crate or UC opening in 31. They run 2-7 h (median 4.6 h in 2026) and start at 19:00-21:00 ([@goblinbgmi/streams](https://www.youtube.com/@goblinbgmi/streams)). The 7-hour [GVKHZ9-erB8](https://www.youtube.com/watch?v=GVKHZ9-erB8) shows the shape: 23 minutes of full-screen facecam talk, then matches of about 20-25 minutes, separated by 5-15 minute blocks of inventory and crate grids. The overlay is fixed: the game full-width, an iQOO banner along the bottom and the facecam bottom-right. **Since June 2026 his daily grind is on Kick.** In his own words on [7dUemvoJ1c0](https://www.youtube.com/watch?v=7dUemvoJ1c0) he will stream "regularly" on Kick and members-only on YouTube, and his Kick channel has 20,587 followers and 74 public clips from 26 Kick streams between 15 Jun and 7 Nov ([Kick API](https://kick.com/api/v2/channels/soulgoblin)). The 31 second-channel cuts that match no YouTube stream cluster from 28 Jun 2026, so most mid-2026 cuts probably come from Kick (inference). His 2022-23 stream cuts likewise probably come from **Loco**, which his descriptions linked at the time and where Sportskeeda reported 154K followers ([Sportskeeda](https://sportskeeda.com/bgmi/soul-goblin-bgmi-id-stats-f-d-ratio)).

**Packaging and timing.** Main-channel titles follow a stat formula ("Solo {k} Finishes WWCD | {team} | {event}"). Single-match hero edits get a designed face cut-out with a big number; tournament reels since 2025 get a raw gameplay frame. Descriptions are hashtags only, with no playlists and no chapters. Single-match highlights go up most often at 12:00-14:00, and also at 16:00-20:00. On the second channel, a good stream yields **1-3 long videos plus 2-4 Shorts over 1-12 days**: 17 of 40 matched videos went up within a day (2.8-21.5 h), 13 within 1-5 days and 10 within 5-12 days. The 9.75-hour stream [7dUemvoJ1c0](https://www.youtube.com/watch?v=7dUemvoJ1c0) fed a 1v2 TDM, a 2v2 WOW, a trolling session, a 4v4 WOW, a crate video and 2 Shorts. Second-channel thumbnails are always designed: a cut-out of Goblin, a scope frame, two lines of yellow and white text, red arrows, or a "VS" split for custom rooms ([7TkLt-j3u4A](https://www.youtube.com/watch?v=7TkLt-j3u4A)). Videos go up at 11:00 or 18:00-22:00, Shorts at 21:00-22:00.

**What performs.** On the main channel since May 2023, titles naming people or opponents have a median of **165K views against 130K for kill-number titles** (n=24 and 40, overlapping groups). Status and rivalry moments lead: "Goblin 1v4 Drx 🇰🇷 in WOW" (293K Short), "New SouL vs Old SouL". On the second channel, 2025-26 titles naming a person have a median of **72.8K against 34.2K** without, and Shorts 158K against 110K. The best Short layout is a stacked LAN broadcast over his player-cam (520K median, n=12), and a clutch with named shocked teammates ([iVF6tpnxnfA](https://www.youtube.com/shorts/iVF6tpnxnfA), 1.23M) far outruns plain clutch Shorts (30K median in 2024).

### Joker: a vlog main channel and an eight-minute stream-cut channel

Joker's main channel stopped being a gaming channel in 2023. **@Jokerkihavelii** holds 499 videos, about 1,310 streams and 273 Shorts. In 2021, 48 of its 60 uploads were stream cuts. In 2025-26, **86 of 89 uploads were camera-shot**; the other 3 were BGMI challenge videos in 2025 ([@Jokerkihavelii/videos](https://www.youtube.com/@Jokerkihavelii/videos)). The last regular BGMI compilation on the main channel was 13 Sep 2023. **@jokerclipss** (JokerClips, 280K subscribers) took over all the stream-based work: 659 videos and 152 Shorts, almost all cut from Joker's own YouTube streams ([@jokerclipss/videos](https://www.youtube.com/@jokerclipss/videos)).

| | @Jokerkihavelii (main) | @jokerclipss (second) |
|---|---|---|
| Output now | 34 videos and 112 Shorts in 2026; 10-15 streams a month | 63 videos and 1 Short in 2026; **none since 5 Oct 2026** |
| Main source | Camera: vlogs, IRL challenges, "24 hours as X" | His own YouTube streams, overlay kept |
| Other sources | 9 stream-recorded BGMI challenges or collabs (2024-25) | Co-streamers' or raiders' streams (about 10% of frames seen), vlog re-cuts, Loco streams in 2022-23 |
| Shorts | Phone-shot routine and skit series (2.8M median for routines) | Stream moments and IRL friend clips; nearly stopped |
| Editing | Documentary-style 13-25 min edits | The full comedy kit, padded to 8:00-8:20 |

**Content types and their sources:**

| Type (channel) | n | Median length | Median views | Footage source |
|---|---|---|---|---|
| Vlog / IRL (main) | 271 | 921 s | 339K | Camera |
| Social experiment, "24 hours as X" (main) | 18 | 968 s | 678K | Camera, produced shoot |
| BGMI challenge or collab (main, 2024-25) | 9 | 791 s | 546K | Mostly stream; one IRL shoot |
| BGMI stream compilation (main, 2021-23) | 21 | 434 s | 142K | Stream |
| Among Us / party-game highlight (main, 2020-24) | 21 | 530 s | 332K | Stream (Loco watermark in 2022) |
| Gaming Shorts (main) | 35 | 34 s | 304K | Stream, stacked |
| Routine mini-vlog Shorts (main) | 81 | 90 s | 2.8M | Phone, native vertical |
| BGMI funny session (second) | 159 | 485 s | **185K** | Stream, 1-2 streams |
| BGMI challenge or "vs" (second) | 50 | 486 s | 166K | Own stream; opponent's stream in some |
| Crate opening (second) | 28 | 481 s | 118K | Stream |
| Esports watch-party reaction (second) | 48 | 491 s | 75K | His stream showing the official broadcast |
| Reaction to creators or media (second) | 89 | 132 s | 60K | His stream showing another creator's video |
| Short BGMI or stream moment (second, 2022-23) | 133 | 79 s | 52K | Stream |
| Stream-talk, call or IRL moment (second) | 99 | 97 s | 45K | Stream (chat, video calls, IRL streams) |
| Party and indie games (second) | 10 | 492 s | 144K | Stream |

On JokerClips **the stream type decides the product**. BGMI streams become sessions, challenges, crate openings and short moments; watch-party streams become esports reactions; "baat chit" and call streams become talk cuts; "REACTION AND BGMI" streams become creator reactions; IRL streams become 3-4 minute IRL clips. Nineteen highlights are caption-mapped to their source. The crate video [72gO2p-DjEg](https://www.youtube.com/watch?v=72gO2p-DjEg) uses 64 minutes of stream [u3KbWR2zR_M](https://www.youtube.com/watch?v=u3KbWR2zR_M) as 30 units in order. The watch-party video [GOJlT6ZGLJ0](https://www.youtube.com/watch?v=GOJlT6ZGLJ0) turns 4 hours into 24.8 minutes and went up **56 minutes** after the stream ended. The Meccha Chameleon video [iStTbFVJeMM](https://www.youtube.com/watch?v=iStTbFVJeMM) is built from four streams.

**How each type is made.** Effort scales with the type. Sessions, challenges and crate openings get the full comedy kit: a visual change every 5-10 s, facecam crop-zooms on every talk beat, meme inserts with one-word labels, burned subtitles of key lines, black-and-white freezes, time cards and, since 2025-26, an "IN THIS VIDEO" teaser. Watch parties are almost raw: long chronological units of 8-141 s, no teaser, ending on the trophy. Talk and call cuts are two webcams side by side for the whole video. The crate recipe is one pull plus its reaction per unit (median about 13 s), in spending order, with the payoff the total loss at the end: "75,000 lag gaye" closes [72gO2p-DjEg](https://www.youtube.com/watch?v=72gO2p-DjEg), where the replay peak sits at 410-528 s. The main channel's 2025 challenge video [WBq__Fc-pqM](https://www.youtube.com/watch?v=WBq__Fc-pqM) shows a story template: the terms ("55 kills plus a chicken dinner wins ₹3 lakh"), a first attempt that falls 3 kills short, the next day's stream, the result screen, and the celebration. On stream he says "ye highlight main channel pe jaayegi" at 8:51.

**His streams as input.** A Joker stream is a 3-6 hour evening show with a fixed running order: a 2-3 minute intro song, 5-35 minutes of full-screen facecam "baat chit", 2-4 hours of BGMI with friends on voice, often a second game (GTA RP most often), then a short good-night chat ([G4W1WwLmIDo](https://www.youtube.com/watch?v=G4W1WwLmIDo)). In 34 captioned streams from Jul-Oct 2026, 80-93% of seconds carry speech at 107-156 words a minute; 2026 streams start at a median 21:06. The layout has been stable since 2022: game full frame, facecam bottom-right, a "JOKER" mascot banner with a live follower counter bottom-left. GTA RP moves the facecam top-left. **Laughter is uneven.** The captioner's laughter tags run about 2-4 times denser in GTA RP and Among Us than in BGMI in the streams measured, and the last third of a stream holds more laughter (37%) than the first (26%). He talks to his editors on stream in 25 of 34 streams, and says "clip" or "highlight" 0-16 times a stream. In 2022-23 he also streamed on Loco: the watermark is on JokerClips' "Snax VS Joker *CALL FIGHT*" ([QqqL1qmOXzs](https://www.youtube.com/watch?v=QqqL1qmOXzs), 697K).

**Packaging and timing.** JokerClips packaging is fully templated: since Aug 2023 one boilerplate description ("Main Channel: …" plus 3 hashtags) on 412 uploads, one 6-tag set, no chapters, and titles built from named S8UL co-stars plus a capitalised conflict word plus emoji. Since 2024 about half of the long videos go up at **08:00-12:00**, most often at 09:00-10:00. Delay depends on effort: watch parties 13-56 minutes after the stream, IRL and call cuts about a day, crate and novelty sessions 2-3 days, other games 3-7 days, comedy sessions 4-6 days, two-stream compilations 14-20 days. Thumbnails are face collages with a speech bubble quoting the video's peak line.

**What performs.** On JokerClips, titles with a co-star name have a median of **187K against 147K**, and "ft." or an @handle 202K against 162K. Capitalised asterisk words and emoji make no measurable difference, and money words do worse (123K against 178K). Reach follows the co-star: Snax in the title gives a 231K median (n=66), Goldy 230K, Rega 141K. The biggest long videos are one-off events with outside stars: the Carryminati collab reaction (1.48M) and Jonathan's raid (1.42M) ([YI0ntgz9Y_o](https://www.youtube.com/watch?v=YI0ntgz9Y_o), [tt1gwGtxjlU](https://www.youtube.com/watch?v=tt1gwGtxjlU)). The switch to 8-minute videos in 2023-24 coincided with long-video median views rising about 4x, from 44-54K to 221K, though the cause is not proven. Output has since fallen from 375 uploads in 2023 to 64 in 2026, with a record-low 4.0% like rate in 2026 H2: the channel looks deprioritised (inference). Joker himself complained on stream on 7 Sep 2026 that four editors in a row quit his vlog footage after doing 20% of the work ([X_QBQqfO-9g](https://www.youtube.com/watch?v=X_QBQqfO-9g), 15:40), which shows the editing capacity problem Kaatclip addresses.

### LoLzZz: a record channel and an everything-else channel, both from one nightly stream

LoLzZz is mostly a live streamer. **@LoLzZzGaming** has **2,972 streams (about 13,000 hours since Jul 2019)** against 418 long uploads and 107 Shorts, and its edited output fell from 95-98 uploads a year (2019-22) to **16 in the last 12 months** ([@LoLzZzGaming/streams](https://www.youtube.com/@LoLzZzGaming/streams)). Streams average about 500K views each in 2026. **@lolzzzplays** (386K subscribers) carries the overflow: 835 videos, 390 Shorts and 62 of its own streams ([@lolzzzplays/videos](https://www.youtube.com/@lolzzzplays/videos)). Unlike Goblin and Joker, both of his channels are fed by the same nightly stream. On 8 Sep 2026 one stream gave a 51-kill match to Plays the next morning and a 55-kill match to the main channel a day later ([EJTupVtHuY8](https://www.youtube.com/watch?v=EJTupVtHuY8), [fbVXWfefL8c](https://www.youtube.com/watch?v=fbVXWfefL8c)).

| | @LoLzZzGaming (main) | @lolzzzplays (second) |
|---|---|---|
| Output now | 16 long uploads in 2026; about 253 streams | 101 long videos Jul 2025-Oct 2026; Shorts back in 2026 |
| Main source | Own stream: the night's headline record match | Own stream: second records, crates, cash challenges, talk |
| Other sources | Teammates' streams (Jonathan), BGIS device recordings, studio shoots, brand agencies | Other streamers' VODs (required for "vs streamer"), third-party videos in reactions, BGIS device POV |
| Shorts | 12 since Oct 2023, last on 6 Feb 2026 | Stacked reaction Shorts; the record teaser Short |
| Editing | One house style: black-led cold open, garnish every 1-2 min, proof ending | The same house style, plus dual-POV cross-cutting |

**Content types and their sources:**

| Type (channel) | n | Median length | Median views | Footage source |
|---|---|---|---|---|
| Single-match record, "N SOLO KILLS" (main, newest 52) | 22 | 779 s | 274K | One match of his own stream |
| TDM / 1v1 / 2v2 vs Jonathan (main, newest 52) | 3 | 756 s | **847K** | His stream cross-cut with Jonathan's |
| Multi-match, UR, "bonus matches" (main, newest 52) | 4 | 1,368 s | 224K | Several matches of his own streams, not in time order |
| Tournament POV, BGIS (main, newest 52) | 4 | 1,122 s | 299K | Clean device recording plus caster audio |
| Cash challenge (main, newest 52) | 3 | 622 s | 272K | Own stream |
| Brand or sponsored (main, newest 52) | 5 | 586 s | 88K | Studio or agency shoot |
| Crate opening (main, all years) | 14 | 526 s | 177K | Segment of his own stream |
| Clutch compilation, "Top 10" (main, all years) | 23 | 522 s | 242K | Many streams over weeks |
| "vs streamer" (Plays) | 135 | 634 s | 112K | His stream plus the opponent's public stream |
| Record or domination (Plays) | 80 | 594 s | 108K | Own stream; Jonathan's POV in squad records |
| Reaction (Plays) | 29 | 492 s | 150K | His stream showing others' content |
| TDM / 2v2 collab (Plays) | 16 | 548 s | **210K** | Both players' streams |
| Cash challenge (Plays) | 10 | 648 s | 198K | Own stream |
| Crate opening (Plays) | 18 | 512 s | 82K | Own stream |
| Mini clip, horizontal (Plays, 2021-23) | 518 | 33 s | 50K | Own stream, some phone IRL |

The on-screen **subscriber counter works as a clock**. It climbs steadily inside one match of a record video (2,798,802 to 2,798,848 in [-qpx-ejuq9Q](https://www.youtube.com/watch?v=-qpx-ejuq9Q)), so records are one match. It jumps backwards after a "BONUS MATCHES" card in [lOAtTbOsCzQ](https://www.youtube.com/watch?v=lOAtTbOsCzQ), so multi-match videos reorder matches. It shows six different values in the 9-minute compilation [tEK_UYkgVmE](https://www.youtube.com/watch?v=tEK_UYkgVmE), so compilations pull from weeks of streams. Teammates' overlays carry their own counters (Jonathan about 6.7-7.9M), which is how the study found that **5 of 9 non-record gameplay highlights from 2025-26 use a teammate's stream**, for example the PMGC scrims video [fCCQkW1Uevk](https://www.youtube.com/watch?v=fCCQkW1Uevk), which alternates his POV and Jonathan's every 10-40 s. On Plays, the "vs streamer" format needs the opponent's own stream: in [DwvaNRtqy20](https://www.youtube.com/watch?v=DwvaNRtqy20), Malkin Plays' stream [xhaouSLZ7mc](https://www.youtube.com/watch?v=xhaouSLZ7mc) lines up with his to the same clock minute, and the video replays the final fight from her side before closing on her 3rd-place screen. Opponents are mostly small streamers (live counters of 1.2K-2.7K), and only 4 of 41 descriptions checked credit them.

**How each type is made.** One house style covers every stream-based edit. It opens with a 30-60 s cold open (black, a facecam stating the goal, 2-3 teaser shots, a stylised title, black). The match then runs in order on the unchanged stream layout, with garnish every 1-2 minutes: full-screen facecam punch-ins, a black-and-white facecam with a joke subtitle as an "inner voice", labelled film or TV memes, colour bars. It ends on proof (WWCD, MVP, results table, "VICTORY"), then the facecam, then 5-10 s of black. **White-on-black "MATCH 2", "MATCH 7" or "BONUS MATCHES" cards appear only when the video jumps to another match** ([cLVYuMe5LJk](https://www.youtube.com/watch?v=cLVYuMe5LJk) at 7:25 and 14:21). Compilations put a one-line Hinglish joke card before each clip ("CLUTCH NO.7 MATLAB THALA FOR A REASON", [tEK_UYkgVmE](https://www.youtube.com/watch?v=tEK_UYkgVmE)). Plays' crate videos compress a spin, result and face loop about 4x, then **show the new skin and play a match in it** ([xuag6MDiNI0](https://www.youtube.com/watch?v=xuag6MDiNI0)), keeping 24-27% of a 39-52 minute span. Record matches keep 30-52% of the match.

**His streams as input.** In 2026, 79 of 103 exactly timed streams started at 21:00-21:59, and 75 of 102 gaps between streams were one day. Gameplay streams last 5-7 hours and end around 02:00-04:00. The goal is stated three times: in the title ("70 SOLO KILLS POSSIBLE??"), on the LIVE thumbnail, and in the first 5-15 minutes of talk ([wq2fjFmms1U](https://www.youtube.com/watch?v=wq2fjFmms1U): "aaj apna target aapko pata hi hai, 70 solo kills" at 1:20). About 15 minutes of talk and membership plugs come before the first match; then come roughly 10-14 matches of 25-30 minutes (inference from one timeline). The overlay is a bottom bar with KICK, a payment number, his wordmark, iQOO and AMD logos, the live subscriber count, and a small facecam bottom-left. **Since 22 Sep 2026 he alternates days with Kick** ("ek din YouTube ek din Kick", [w1NB9sVC8k0](https://www.youtube.com/watch?v=w1NB9sVC8k0) at 2:00). His YouTube streams fell from 28 in August to 15 in September, and the 62-kill record video ([Car5bJ_yP-E](https://www.youtube.com/watch?v=Car5bJ_yP-E)) matches no YouTube stream (inference: a Kick stream). His most-watched streams are all 2026 esports watch parties, up to 2.1M views ([hNCb6AT6dwc](https://www.youtube.com/watch?v=hNCb6AT6dwc)), and crate-opening streams have the highest median among his gameplay streams (548K).

**Packaging and timing.** Effort goes into the title and thumbnail: his studio photo, a huge yellow and white condensed-italic headline, and one proof element (a gameplay frame, rank card or product). Descriptions are empty or an Instagram link plus hashtags, playlists stopped in 2021, and there are no chapters. In his documentary he describes the routine himself: "abhi ek stream karta hoon aur subah main highlights wagairah daalunga" ([9vzttojcMwA](https://www.youtube.com/watch?v=9vzttojcMwA) at 32:00). Main-channel edits go up at **12:00-12:51 the next day** in 29 of 37 cases. Plays posts at 09:00-11:30, before the main slot, 13 hours to 10 days after the stream. The 72-kill teaser Short went up on Plays 5 hours after the main video, with a "FULL VIDEO IS ON YOUTUBE" end card ([FyHDoGMnHO4](https://www.youtube.com/shorts/FyHDoGMnHO4)).

**What performs.** Rivalry with a bigger creator beats everything long-form. His all-time top upload is "Can i Defeat @JONATHAN GAMING in 1v1 TDM?" (about 4.0M, [pnqQb35rwlE](https://www.youtube.com/watch?v=pnqQb35rwlE)), and TDM collabs run 847K median among the newest uploads against 274K for records. New personal bests come next (the 72-kill record, 990,648 views), then self-contained gameplay (compilations 185K, multi-match 224K), with brand videos last (88K). On Plays, Jonathan is named in 5 of the top 8 long videos, "girl gamer" and "streamer reported me" framings beat neutral fight titles, and reactions get views but the lowest like rate (3.7%).

## 3. Patterns across all three: the grammar of a BGMI highlight

### The shared grammar holds on every stream-fed channel

The six channels use one visual language, and none of it is hard to automate except the meme clips. **The stream layout stays untouched** in long videos: game, facecam box, sponsor or name banner, live counter. No editor crops a long video to a clean game feed; the clean look exists only where the source itself was a clean recording (Goblin's phone, LoLzZz's BGIS device POV). **Cuts are chronological inside a unit**, and the only reordering is the cold open (plus LoLzZz's "bonus matches" and Joker's two-stream compilations). **The opening is a labelled teaser**: "IN THIS VIDEO -" for 15-20 s on Goblin's second channel ([VF0fmimwQKc](https://www.youtube.com/watch?v=VF0fmimwQKc)), 10-22 s on JokerClips, and a 30-60 s goal-led cold open on LoLzZz's channels. **Faces carry the reactions**: full-screen facecam punch-ins appear on nearly every edited stream-based type on all three creators' channels; JokerClips' near-raw watch parties are the exception. **The game's own screens are the proof**: WWCD, "#N place", MVP, "VICTORY", "CONGRATULATIONS", "YOU GOT". No channel adds a running kill counter, and chapters are absent: none on 526 Goblin second-channel videos, none on any JokerClips upload, none on 87 LoLzZz items. **Cards appear only on jumps**: between matches (LoLzZz), between streams ("THE NEXT DAY", Joker and Goblin), or as a time skip ("A FEW MINUTES LATER"). **The ending is short**: a result screen, a facecam reaction, then black or an end card asking viewers to follow (Goblin's "Follow me on Kick" card on [YK7JXrVblYQ](https://www.youtube.com/shorts/YK7JXrVblYQ)).

The device that does not transfer safely is the **labelled film, TV or news meme cutaway**, used by all three (Modi, Arnab and Bollywood clips in Goblin's [gs8thi_U_fU](https://www.youtube.com/watch?v=gs8thi_U_fU); "KRAFTON:" film memes in LoLzZz's [z1jXPJN8z-c](https://www.youtube.com/watch?v=z1jXPJN8z-c)). LoLzZz's black-and-white facecam with a subtitle "inner voice" does the same comic job using only the creator's own footage and words, so it is the safe substitute (inference).

### Per-type recipes that hold across creators

| Type | Unit | Keep | Order and opening | Ending | Length | Evidence |
|---|---|---|---|---|---|---|
| **Single classic match** | One match: WWCD, a near-win, a record or a named rival | 23-31% for a fight story (Goblin); 30-52% for a record (LoLzZz) | Chronological; teaser 15-25 s (Goblin) or goal-led cold open 30-60 s (LoLzZz) | Result screen, MVP, facecam, black | 4.5-7.5 min (Goblin stream cut); 10-15 min (LoLzZz record) | [wDgeZBn80VM](https://www.youtube.com/watch?v=wDgeZBn80VM), [-qpx-ejuq9Q](https://www.youtube.com/watch?v=-qpx-ejuq9Q) |
| **Multi-match session or challenge** | 2-5 matches of one goal (N kills in M matches, ₹ per kill, a day's scrims, UR "bonus") | Per match, as above | "MATCH N" card on each jump (LoLzZz); a "next day" card between streams (Joker) | Final result and celebration | 18-35 min (LoLzZz); 8-10 min (Joker) | [cLVYuMe5LJk](https://www.youtube.com/watch?v=cLVYuMe5LJk), [WBq__Fc-pqM](https://www.youtube.com/watch?v=WBq__Fc-pqM) |
| **Crate opening** | One crate session, first spin to last reward | 3-43% (Goblin), about 25% (LoLzZz Plays); 27-30 units of about 13 s (Joker) | Chronological; 10-15 s teaser of the best pull and angriest line | The total-loss line (Joker), the best pull and outfit (LoLzZz main), or a match in the new skin (Plays) | 5-9.5 min | [72gO2p-DjEg](https://www.youtube.com/watch?v=72gO2p-DjEg), [z1jXPJN8z-c](https://www.youtube.com/watch?v=z1jXPJN8z-c), [xuag6MDiNI0](https://www.youtube.com/watch?v=xuag6MDiNI0) |
| **Custom room / TDM / WOW** | One room session, every round | 26-65% in 9-25 stretches; respawn waits cut | Chronological; teaser from a later round | Final "VICTORY" table, then facecam | 7-15 min | [7TkLt-j3u4A](https://www.youtube.com/watch?v=7TkLt-j3u4A), [Ev6oMQTJVJ8](https://www.youtube.com/watch?v=Ev6oMQTJVJ8) |
| **Funny session** | The first 30-120 min of the BGMI part, or a whole dense match | 1-60% of a span; units of about 13 s from trigger to punchline | Stream order; "IN THIS VIDEO" teaser; facecam zoom on every talk beat | A punchline or a short end card | 8:00-8:20 (JokerClips); 2-10 min (Goblin) | [VF0fmimwQKc](https://www.youtube.com/watch?v=VF0fmimwQKc), [Kobcv7gzuAY](https://www.youtube.com/watch?v=Kobcv7gzuAY) |
| **Talk cut** | One continuous answer to chat, a reveal, a defence | Long runs kept | None or a short teaser | A black end card | 1.5-6 min | [Qw5AGoqlUks](https://www.youtube.com/watch?v=Qw5AGoqlUks), [49r8dHshj5o](https://www.youtube.com/watch?v=49r8dHshj5o) |
| **Milestone cut** | 10-15 min around a counter crossing or celebration | About half | Chronological | The moment the counter crosses | About 7 min | [nUz6ZI6xjkY](https://www.youtube.com/watch?v=nUz6ZI6xjkY), [1N27KdUAnkc](https://www.youtube.com/watch?v=1N27KdUAnkc) |

The table shows why a single template fails. A crate video's payoff is the **cumulative loss or the best pull late in the session** (heatmap peaks at 75% on [z1jXPJN8z-c](https://www.youtube.com/watch?v=z1jXPJN8z-c) and 410-528 s of 561 on [72gO2p-DjEg](https://www.youtube.com/watch?v=72gO2p-DjEg)), so cutting to the "best moment" would spoil it. A custom room has no looting, so it keeps far more than a classic match. A talk cut has no game event at all.

### Shorts use three layouts and do three jobs

The **stacked layout** (game on top, facecam below, or the reverse) is the common gaming Short on all three creators' channels. On Goblin's second channel it has a 90K median (n=124) against **46K for a game-only vertical crop** (n=107). Joker's stacked gaming Shorts keep the banner and counter and add a 2-4 word caption chip and an emoji sticker at the payoff ([CVqRiZ-wwNw](https://www.youtube.com/shorts/CVqRiZ-wwNw)). LoLzZz's 2026 reaction Shorts put the content on top (about 55%) and the facecam below, with no burned caption ([zC2CyyUHKG0](https://www.youtube.com/shorts/zC2CyyUHKG0), 3.24M). The **subject matters more than the layout**: relationship and identity moments win and plain kills lose. JokerClips' BGMI gameplay Shorts have a 70K median against 149K for stream-moment Shorts. Goblin's top Shorts are "Revenge" (4.52M), nostalgia edits and "Krutika and Regaltos shocked by Goblin's Crazy 1v3" (1.23M).

Goblin's second channel shows the **three jobs a Short does**. A teaser posted before the long video: three Shorts from stream [ds2q0wh-YE0](https://www.youtube.com/watch?v=ds2q0wh-YE0) went up 3-8 days before the 2v2 WOW video from the same session. A "best 30-60 s" posted about an hour after the long video ([HhcQY2wm8Ug](https://www.youtube.com/shorts/HhcQY2wm8Ug), 456K, from 5:09 of its long video). And a standalone moment from a stream with no long video ([V75ArTHWzQs](https://www.youtube.com/shorts/V75ArTHWzQs), 422K). LoLzZz adds a fourth: the **proof teaser** built from the last 20 seconds of a record. The owner's direction, Shorts cut from the highlight plus a same-day teaser, matches the second and fourth jobs. The first and third are also common.

### Five rules the evidence supports across creators

**Segment first.** Every creator's stream mixes states that are never used in a match cut: full-screen facecam talk, lobby and inventory, crate grids, other games, watch parties. Goblin's 7-hour stream has 5-15 minute non-gameplay blocks between every match ([GVKHZ9-erB8](https://www.youtube.com/watch?v=GVKHZ9-erB8)); Joker's streams switch game halfway; LoLzZz's crate block sits at 0:47-1:05 of [w1NB9sVC8k0](https://www.youtube.com/watch?v=w1NB9sVC8k0). The layouts make the states visible: a full-screen face means chat, a different facecam position means a different game, a browser frame means a reaction.

**Stream type decides the recipe.** JokerClips mirrors each stream genre with its own product, and Goblin's second channel cuts "the session the title promises". The keep ratio follows the promise: about a quarter of a match for a fight story, about half for a record, a few per cent of a session for comedy, and about half of a custom room.

**Laughter alone mis-ranks.** Laughter is denser in non-BGMI games and in the late hours of Joker's streams, and the top 10% of 10-minute bins hold 28% of a stream's laughter. A comedy ranker must work inside the BGMI segment, and the deeper study's evidence says Joker's editor uses mostly the first 30-120 minutes of it.

**People and rivalry beat numbers.** The title effect repeats on all six channels (section 2), and the top long videos on every channel involve another named person: Jonathan (LoLzZz), Snax and Goldy (Joker), Drx, Krutika, Regaltos and "old teammates" (Goblin).

**Speed costs edit density.** Raw types go up fast: JokerClips watch parties within an hour, Goblin's custom room [Ev6oMQTJVJ8](https://www.youtube.com/watch?v=Ev6oMQTJVJ8) 2.8 hours after the stream. Edited comedy takes 2-6 days. A tool that edits in minutes can offer edited types at raw-type speed (inference).

## 4. What Kaatclip can make from one creator's own recording

### In reach

"Has" lists what the Kaatclip engine already does according to the build notes and earlier reports: HUD reading of the eliminations and players-left counters, the fresh-lobby reset with per-match kill counts, the Chicken Dinner banner, kill-feed knocks (best effort by layout), "Spectating", a Hinglish transcript with word times, YAMNet laughter and shout scores, the Gemini talk judge, moment markers (button, chat !clip, spoken "clip karo"), the facecam finder, stacked Shorts layouts, the 16:9 compilation renderer with title cards, thumbnails with a face cut-out, the title maker, and local OBS file upload (including while streaming). The match map is planned (Stage 1) but not built.

| Format | Signals needed | Kaatclip has | Kaatclip is missing | Difficulty | Evidence of performance |
|---|---|---|---|---|---|
| **Single classic match, stream layout kept** (Goblin second-channel cut, LoLzZz record) | Match start and end, kills, fights, final circle, result and MVP screens, comms | Counters, lobby reset, Chicken Dinner, knocks, transcript | Match map (planned), result and MVP screen reading, recall-mode handling, own vs team kills | Medium | LoLzZz main records 274K (n=22); Plays records 108K; Goblin match cuts 34K |
| **Record match with goal-led cold open** | The above, plus the goal from the title or first 15 min, and a personal best | Transcript, stream title | Goal parse, stored personal best | Medium | 72 SOLO KILLS 990,648 ([-qpx-ejuq9Q](https://www.youtube.com/watch?v=-qpx-ejuq9Q)) |
| **Multi-match challenge or session** (N kills in M matches, ₹ per kill, scrims day, "bonus matches") | Per-match score, running tally, donation or challenge read, "MATCH N" cards | Per-match kills, title cards | Match map, goal tracker | Medium | LoLzZz multi-match 224K, cash 272K (main) and 198K (Plays); Joker challenge 673K ([WBq__Fc-pqM](https://www.youtube.com/watch?v=WBq__Fc-pqM)) |
| **Custom room / TDM / WOW session, own POV** | Mode (no plane, round timer, score), "VICTORY"/"DEFEAT" round cards, respawn gaps, opponent names from the lobby | Kill counter (on the TDM HUD: untested), facecam | Mode detection, round-card reading | Medium | Goblin second channel 89K median, 225K in 2025 (n=9), 22 of 22 from his stream |
| **Crate opening** | Crate and inventory screens, "YOU GOT" and "CONGRATULATIONS" cards, reaction peaks, spoken UC totals | Laughter and shout, transcript, facecam | Crate-screen detection, a segment type for it | Easy-Medium | JokerClips 118K (n=28); LoLzZz main 177K (n=14); Plays 82K; Goblin 31K |
| **Funny session** (8 min comedy) | Laughter, speech density, trigger-to-punchline units, BGMI-only window | Laughter and shout, transcript, Gemini judge, markers | Segment restriction, unit builder, speaker labels | Hard | JokerClips sessions 185K (n=159); Goblin funny edits 49K |
| **Talk cut** | Full-screen facecam or static lobby, long continuous speech, topic start and end | Transcript, Gemini judge, facecam finder | A "chat" segment type, topic boundaries | Medium | Goblin talk clips 36K (n=27); Plays talk 198K (n=2); JokerClips talk and call 45K |
| **Milestone or celebration cut** | Overlay counter crossing a round number, donation or chat spikes | Nothing specific | Counter reading | Medium | [nUz6ZI6xjkY](https://www.youtube.com/watch?v=nUz6ZI6xjkY) 130K; Goblin's 500K celebration [1N27KdUAnkc](https://www.youtube.com/watch?v=1N27KdUAnkc) |
| **Stacked gaming Short** | Best 20-60 s beat, facecam box | Moment ranking, stacked layouts, covers | A relationship-moment preference | Easy | Goblin stacked 90K vs game-only 46K; Joker gaming Shorts 304K |
| **Teaser or "best of" Short from a highlight** | The highlight's ending proof or best beat | Renderer | The highlight itself | Easy once highlights exist | [FyHDoGMnHO4](https://www.youtube.com/shorts/FyHDoGMnHO4); [HhcQY2wm8Ug](https://www.youtube.com/shorts/HhcQY2wm8Ug) 456K |
| **Horizontal one-moment clip** | One clutch or banter beat | The current clip engine | None | Easy | Goblin 2021 clips 26K; Plays mini clips 50K; all three channels dropped this format by 2023 |
| **Clutch compilation across streams** ("Top 10") | 1vN clutch detection, a library of past jobs, a caption card per clip | Knocks (best effort), compilation renderer | Clutch detection, cross-stream library | Hard | LoLzZz compilations 242K (n=23, all years) |
| **Single-POV streamer encounter** | Streamer name in the kill feed, speech cues ("stream snipe", "report") | Kill feed (best effort), transcript | Name matching | Medium, weak product | Loses the opponent's reaction, which is the hook of Plays' 112K format |
| **Clean "hero" edit** | A second, clean game recording | Nothing | The input itself | Needs the creator to record a clean source | Goblin phone-sourced match videos 169K vs stream-cut 124K (confounded by stakes) |

Measured as a share of output, the in-reach types cover about **53% of JokerClips' uploads** (sessions, own-POV challenges, crates, short moments and stream Shorts), and Goblin's stream-layout videos are **292 of 526 long videos and 61% of long-video views** on his second channel. On LoLzZz Plays, own-stream records, crates, cash challenges and talk make up to about 110 of roughly 317 long videos (some squad records also use Jonathan's POV). On Joker's main channel, almost nothing since 2024 is in reach.

### Out of reach

| Format | Seen on | Why Kaatclip cannot make it from one recording |
|---|---|---|
| "vs streamer" and dual-POV collab TDM or scrims | Plays (135 vs-streamer videos), LoLzZz main (Jonathan TDMs, 847K), JokerClips 1v1 | Needs the other streamer's stream, synced on the clock, plus their consent. Only 4 of 41 Plays descriptions credit the opponent |
| LAN and tournament broadcast cuts, interviews | Goblin second channel (105 videos, 19K median) | The organiser's footage and rights; a creator's stream does not contain the observer feed |
| Watch-party highlights | JokerClips (48), LoLzZz streams (his most watched) | The broadcast fills the frame; only the facecam is the creator's. Takedown risk (inference) |
| Reactions to other creators' videos, reels or vlogs | JokerClips (89 + 12), Plays (29, top video 1.22M) | The third-party video is the content; a high copyright risk and no game signal |
| Camera vlogs, IRL challenges, social experiments, documentaries | Joker main (most of it), Goblin second channel (2026 LAN weeks), LoLzZz | Camera footage, story and voice-over |
| Sponsored studio videos and brand shows | LoLzZz (OPPO, Lenovo, Google Play), Goblin, Joker | Separate shoots with product B-roll |
| Clean phone hero edits and tournament device POV | Goblin main, LoLzZz BGIS videos | Need the device recording, which a stream does not contain |
| Lifestyle, skit and IRL-friend Shorts | Joker main (2.8M median routines), JokerClips 2025 burst | Shot natively vertical on a phone |
| Nostalgia and hype edits, fan edits | Goblin second channel (54 edit Shorts, up to 2.7M) | Old footage, photos and film clips; made outside |
| Film, TV and news meme inserts | All three | Content ID risk; own stickers and the B/W facecam caption are the safe substitute |
| Other games (GTA RP, Among Us, party games) | JokerClips, Joker streams, Plays fun modes | Not BGMI; an audio-only mode is possible, but BGMI detectors do not transfer |

## 5. Corrections to the two earlier reports

The new notes win wherever they disagree with "BGMI highlight video structure" (the first report) and "BGMI highlight channels deep study" (the second).

| Earlier claim | Report | Correction from the A-to-Z notes |
|---|---|---|
| @goblinsh0rts is Goblin's "stream-cutting channel" | Deep study | **Too narrow.** Stream-layout cuts are 292 of 526 long videos; there are also 105 broadcast cuts, 104 clean POV videos and 24 camera videos. In 2026 the mix was stream 65, broadcast 28, camera 19 ([@goblinsh0rts](https://www.youtube.com/@goblinsh0rts/videos)) |
| Goblin keeps banter out of match highlights and off the main channel | First report | **Era-dependent.** In 2022-23 the main channel posted 8 challenge and funny stream cuts with heavy meme editing at a 231K median, its best long-form numbers that year ([gs8thi_U_fU](https://www.youtube.com/watch?v=gs8thi_U_fU)) |
| Goblin's highlights are clean tournament POV because they come from tournament recordings | First report | **Refined.** They are phone screen recordings (2.06-2.17:1). From 2022 to 2025 the main channel also published 30 stream-cut long videos with overlay and facecam, two of them proven against YouTube streams |
| Goblin's comms are the narration, music stays out of the way | First report | **Only since Sep 2023.** Before that his highlights ran on music beds at 1-19 words a minute, and his second channel's 2023-25 POV videos still run at 28 |
| Goblin streams scrims on YouTube 0-6 times a month | Deep study | **His daily grind moved to Kick in Jun 2026.** The public YouTube streams since then are occasional event-like streams ([7dUemvoJ1c0](https://www.youtube.com/watch?v=7dUemvoJ1c0)) |
| Goblin's custom rooms keep 43-48% | Deep study | **26-65%** across 8 mapped sessions, in 9-25 stretches |
| Goblin's first stream cut goes up 9.6-19.9 h after the stream | Deep study | **2.8 h to 12 days.** 17 of 40 within a day, 13 in 1-5 days, 10 in 5-12 days; one stream drip-fed over 11 days |
| Goblin's Shorts are not systematically cut from his highlights | Deep study | **Partly corrected.** In May-Jun 2026 four Shorts were cut from long videos and posted 0.9-1.5 h after them, and others were posted days before their long video |
| Goblin's 2026 hero thumbnails are raw game frames | Deep study | **Raw frames are for tournament reels** since 2025. Single-match hero edits kept designed face-and-number thumbnails into early 2026 |
| LoLzZz uses no "Match 2" cards; results screens and spoken checkpoints are the transitions (rule 10) | Deep study | **Wrong for the main channel.** Every multi-match video uses white-on-black "MATCH 2", "MATCH 7" or "BONUS MATCHES" cards ([cLVYuMe5LJk](https://www.youtube.com/watch?v=cLVYuMe5LJk), [lOAtTbOsCzQ](https://www.youtube.com/watch?v=lOAtTbOsCzQ)). Plays' multi-match vs-streamer videos use the opponent's death screen and a wipe instead |
| LoLzZz's main channel got 16 edited videos in 2026, almost all record matches | Deep study | **About 7 of 16** are single-match records. The rest are BGIS POVs (3), multi-match UR (2, one from Jonathan's POV), a sing-a-song collab, PMGC scrims, a cash challenge and a Lenovo video |
| LoLzZz's streams list stops at 600 | Deep study | The full tab has **2,972 streams**, about 13,000 hours since Jul 2019 |
| LoLzZz streams 15-28 times a month on YouTube | Deep study | **Down to 15 in Sep 2026**, because he alternates days with Kick from 22 Sep |
| JokerClips posts about 1.6 a week / 5-10 a month | Both | **Stalled.** 64 uploads in 2026, 1 in October, none since 5 Oct 2026 |
| JokerClips' "IN THIS VIDEO" teaser was absent in 2024-25 | Deep study (via joker_deep) | **Only sessions lacked it.** The Chained Together video used it in Jul 2025, and Joker's main channel used it from Jan 2024 ([5szLSGgb5bE](https://www.youtube.com/watch?v=5szLSGgb5bE)) |
| Comedy length is 8:00-8:10 | Both | **A channel choice, not a property of the material.** Joker's own main channel took 4-7 minute compilations before Dec 2023 (median 434 s), and JokerClips' watch parties and co-op games run 8-25 minutes |
| Dedicated highlight channels post about one long video a week | First report | **Far more for these three.** Goblin's second channel posted 12-23 long videos a month in mid-2026 and Plays 13-15 in Aug-Sep 2026 |
| Highlights carry no added cards | Deep study | Still true inside one match. **Compilations add a caption card per clip**, and multi-match videos add match cards |
| The second channel is the place for stream cuts (Kaatclip's "natural place is the fast one") | Deep study | **Holds for Goblin and Joker, not fully for LoLzZz.** His main channel's records are themselves own-stream cuts, the most direct match for Kaatclip |

## 6. Open questions for the owner

Only the questions that change what gets built are listed. Each has a default if you do not answer.

| # | Question | Why it matters | Default if unanswered |
|---|---|---|---|
| 1 | Should Kaatclip split a stream into segments (chat, lobby and inventory, crate, match, custom room, other game, watch party) as the first step, before any ranking? | All three creators' streams mix these states, and laughter and talk rank the wrong parts without it | Yes: segmentation comes first, as part of the match map |
| 2 | After the classic kill match, which session type comes next? | Custom rooms are the best stream-only long format on Goblin's channels; crates are cheaper but mid-table; talk cuts need no game detection | Custom room / TDM next, then crate, then talk cut |
| 3 | Should titles lead with people instead of kill numbers when Kaatclip can name the teammates or rivals in the lobby? | People in titles beat kill numbers on all six channels, but names come from the kill feed and speech, which are best effort | Offer both; put the people title first when a name is found with confidence |
| 4 | Should one stream produce a batch (1-4 long videos plus 2-4 Shorts) with a suggested schedule spread over several days? | That is how the second channels post daily from a few streams | Yes, suggested only; never auto-post |
| 5 | Should Kaatclip let a creator mark outputs for a second channel, or connect two channels? | Every creator studied splits work across two channels | Label each output "main" or "second channel" as a suggestion; one connected channel for now |
| 6 | What should Kaatclip do with segments it must not publish (watch parties, reactions to other people's videos, other games)? | They are a large part of Joker's and LoLzZz's streams and the riskiest footage | Detect and skip them, and tell the creator why; no output |
| 7 | Should Kaatclip ever accept a second recording (a teammate's or opponent's file) for dual-POV videos? | That format is behind Plays' volume and LoLzZz's biggest hits, but needs consent and clock sync | Not now; single-POV versions only; revisit after the beta |
| 8 | Should Kaatclip keep leftover moments from each stream for "part 2" videos and cross-stream compilations? | JokerClips compiles two streams and LoLzZz builds "Top 10" compilations from weeks of streams | Keep each job's leftover units for three weeks; no compilation feature yet |

## 7. Gaps and limits of the research

**The evidence is public data only.** No video or audio was downloaded. Laughter, music and voice overlap were read from YouTube's caption tags, which three of Joker's 34 streams lack entirely. Storyboards show one frame every 1-10 seconds, so transitions under about 2 seconds, small on-screen text and sound effects were not measured. Views are a one-day snapshot, not normalised for age, and click-through, retention and traffic sources are private. Many "what performs" comparisons rest on small, overlapping groups (Goblin's main-channel TDM median rests on n=5), so they are indicative, not proof.

**Off-YouTube sources are inferred.** Loco VODs (2022-23) and Kick VODs (2026) could not be opened, so the claim that specific Goblin and LoLzZz videos come from Kick rests on non-matching captions, timing and the creators' own words. Joker's Loco era is proven only by on-screen watermarks. Members-only streams and videos were not read.

**Source maps are few per type.** About 40 Goblin pairs, 19 Joker pairs and 14 LoLzZz pairs were caption-aligned. The crate recipe rests on about 8 mapped videos, the custom-room recipe on 8, and the Joker challenge template on one video in depth. Type labels come from title rules plus spot checks, with about ±10% error between neighbouring types.

**Three famous creators are not the market.** Goblin is an esports champion, Joker is in S8UL with millions of subscribers, and LoLzZz is one of India's most-watched YouTube streamers. Their reach follows status and famous friends, which a small creator does not have. How these formats perform for a 5K-subscriber streamer is unknown.

**Nothing was tested on the owner's own streams.** Every feasibility judgement in section 4 is an inference. Detection of crate screens, round cards, result screens and chat segments on varied OBS layouts is untested, the kill feed is already known to be unreadable on some layouts, and the rights questions (reusing an opponent's stream, a broadcast or a creator video) were not checked legally.

## Conclusion

The A-to-Z study changes the question Kaatclip should ask about a stream. The earlier reports asked "which match is best, and how should it be cut?" The six channels show that their editors first ask "what kinds of segments are in this stream, and which video does each one make?" A night of streaming holds a chat answer, a crate session, a custom room, three or four matches and maybe a watch party, and the second channels turn that night into a week of different videos, each cut by its own rule. Seen this way, the match map in Kaatclip's next step is one case of a stream map, and the product promise becomes "every postable video in your stream" rather than "one highlight per stream".

The study also marks a ceiling. The formats that made these creators biggest (rivalry cross-cuts with Jonathan, LAN broadcasts, reactions to famous creators, camera vlogs) need footage or relationships that a single recording does not hold. Kaatclip can match a second channel's volume, speed and recipes on the creator's own footage. It cannot supply the famous friend, and the data says the friend in the lobby, named in the title, is worth more than the kill count.
