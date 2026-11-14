# What makes viewers rewatch, stay or leave in long BGMI videos (YouTube "most replayed" heatmaps)

Scope: long videos (over 2 minutes, not live VODs) on the six channels: @goblinbgmi, @goblinsh0rts, @Jokerkihavelii, @jokerclipss, @LoLzZzGaming and @lolzzzplays. Method: public YouTube data only, via yt-dlp `--skip-download`. I read each video's metadata (the `heatmap`, length, views, likes, comments and upload date), its Hindi auto-captions and its preview storyboard frames. No video or audio was downloaded. Most metadata comes from the 12 Nov 2026 scrapes in the earlier raw folders; 64 videos were re-fetched on 14 Nov 2026. Scratch data, scripts and contact sheets are in `C:\Users\soura\AppData\Local\Temp\claude\21027423ba80eb72\c7886632-c6c6-4a95-81c6-c6cbac2a769e\scratchpad\viewers\heatmaps\` (`heat_rows.json`, `bgmi_rows.json`, `stats_out.txt`, `ends_out.txt`, `rhythm_out.txt`, `decay_out.txt`, `peaks_log.md`, `classified.json`, `sheets\*.jpg`).

**Sample.** **779 BGMI long videos with a heatmap**: jokerclips 322, lolzzz_plays 109, joker_main 107, goblin_main 105, goblin_shorts 87, lolzzz_main 49. They run 2-45 min, were uploaded 2021-2026 (141 in 2026) and have 50K-2.33M views. Vlogs, other games and talk shows were removed by title. For **59 of them** I read what sits at the peaks: 49 checked against storyboard frames plus captions, 10 from captions only (marked "image not checked" in `peaks_log.md`). I also read the flattest stretch of 12 videos frame by frame.

**What the heatmap is.** YouTube shows a "Most replayed" graph above the progress bar. Higher points mark the parts viewers watched or replayed most. Only videos with enough views get one, and it was rolled out to everyone in May 2022 ([iMore](https://www.imore.com/youtube-highlighting-popular-parts-videos-new-most-replayed-feature); [Stuff](https://stuff.co.za/2022/05/19/youtubes-new-most-replayed-feature-will-let-viewers-skip-straight-to-the-popular-bits/); [Android Central](https://www.androidcentral.com/apps-software/youtube/youtube-spoilers)). I found no official YouTube help page that defines the exact metric. **In all 779 videos the 100 values are min-max normalised: the lowest point is exactly 0 and the highest exactly 1** (measured). So a value of 0 means "least watched in this video", not "nobody watched". The curve is relative within one video and says nothing about absolute retention. A peak can be people **skipping to** a moment as well as replaying it.

---

## Summary: the most important findings for highlights and Shorts that hold viewers

### Takeaway
Viewers of these long videos behave like skimmers. Everyone sees the first ~10-15 s. Then the heat falls to a low baseline, and viewers jump between 10-20 s spikes, one every ~1-2 minutes. Each spike is a kill burst, a clutch, a final fight with its result, a funny line with a laugh, or a crate jackpot, and it is usually paired with a visible reaction. Driving, holding, looting, spins and empty chat are the flat parts. The heatmap's shape does not predict a video's views.

### Cited Findings
1. **The opening is the most-watched stretch on every channel, but it halves within about 14 s.** Mean heat of the first decile is 0.27, against 0.16-0.17 for every later decile. The time until heat first falls below half of the first bin has a median of 13.7 s: 10.3 s on Goblin main, 19.8 s on LoLzZz main. The first bin is the video's single highest point in only 10% of videos (26% on Goblin main, 4% on both LoLzZz channels). — [stats_out.txt / heat_rows.json, all 779 videos](https://www.youtube.com/@goblinbgmi/videos)
2. **The video settles to its baseline by about 8% of the runtime and stays there.** Mean of the first 12 bins across all videos: 0.46, 0.32, 0.29, 0.26, 0.24, 0.23, 0.23, 0.22, 0.21, 0.21, 0.21, 0.21. On LoLzZz main, 67% of videos show a re-rise inside the first 10% (the first fight after the intro), against 24% on Goblin main. — [measured, 779 videos](https://www.youtube.com/@LoLzZzGaming/videos)
3. **Peaks are short and spaced out.** The top peak is about 15 s wide at half height (median 14.9 s; 10.8 s on LoLzZz Plays, 17.7 s on LoLzZz main). Around a peak, heat runs 0.11 → 0.44 → 0.74 → **1.0** → 0.66 → 0.31 → 0.16 at -30/-10/-5/0/+5/+10/+20 s. Videos carry a median of 4 peaks of at least 0.35, about 0.5 a minute, with a median gap of 72 s between them (52-62 s on Goblin and Jokerclips, 92-109 s on LoLzZz). Half of the 10-90% body sits below 0.1. — [rhythm_out.txt, decay_out.txt](https://www.youtube.com/@lolzzzplays/videos)
4. **What the peaks are (59 videos read).** The main peak after the first 5% breaks down as: kill burst 18, funny line or banter with a laugh 15, final fight plus result screen 13, reveal or crate pull 7, clutch or decisive round 6. On Goblin main, 6 of 12 main peaks are the final fight and the WWCD. Joker's peaks are group laughs, roasts, failures and prank payoffs. LoLzZz's are mid-match kill bursts, often with a meme insert or a facecam punch-in, and a record payoff at the end. — [peaks_log.md; e.g. 6jIQaYvIOGc](https://www.youtube.com/watch?v=6jIQaYvIOGc)
5. **The title's promise is where people jump.** In "Chicken dinner with pan" ([0Ug9nHMiD24](https://www.youtube.com/watch?v=0Ug9nHMiD24)), heat is 0.0-0.1 from 5% to 85% and 1.0 at the pan kill and WWCD at 95%. In "Solo 9 Finishes WWCD ?" ([-ieo36Gj9Hk](https://www.youtube.com/watch?v=-ieo36Gj9Hk)) the peak is the last bin, a troll card reading "BHAROSA RAKHO CHICKEN AAGYA". In "Sid calls Goblin's mom" ([LEwadYEz0Eo](https://www.youtube.com/watch?v=LEwadYEz0Eo)) the peak is the call itself at 70%. In "Handcam on, gameplay gone?" ([nucVWiaxxVg](https://www.youtube.com/watch?v=nucVWiaxxVg)) a peak is the phone-settings proof.
6. **Peaks pair the event with a reaction.** Examples: Jonathan laughing on facecam after the decisive 1v1 round ([PtvEiSN48Dk](https://www.youtube.com/watch?v=PtvEiSN48Dk), 1.0, with the next peak only 0.46); head in hands after the final kills and a warning pop-up ([fbVXWfefL8c](https://www.youtube.com/watch?v=fbVXWfefL8c)); a hand-over-face laugh after a squad wipe ([Ul5mEjNyzu4](https://www.youtube.com/watch?v=Ul5mEjNyzu4)); a shocked opponent line ([uuTVkDWOYus](https://www.youtube.com/watch?v=uuTVkDWOYus)); screams over a 1v2 clutch ([1bSJjsh33kM](https://www.youtube.com/watch?v=1bSJjsh33kM)).
7. **The flat parts.** The flattest stretch (heat below 0.08) in 12 edited videos lasted 47-203 s. It was car driving or rotation (ml5FitUoqf8, 7bmUiiUuAdE, Car5bJ_yP-E), holding or creeping in smoke or a compound (6jIQaYvIOGc, 67w15TWdikI with 162 s), looting houses (fbVXWfefL8c), crate spins without a jackpot even with a meme inserted (z1jXPJN8z-c), or two-facecam chat with no punchline (3c0nLXL8k6U). — [sheets/_lows.jpg](https://www.youtube.com/watch?v=67w15TWdikI)
8. **Endings split by channel type.** Goblin main and LoLzZz main rise into the end, with last-10% / mean at 1.31 and 1.65: the final fight and the WWCD. Joker main and Jokerclips fall (0.65 and 0.75). The very last bin drops on every channel; the cross-channel mean is 0.12. — [stats_out.txt](https://www.youtube.com/@Jokerkihavelii/videos)
9. **Ending right on the result keeps the end watched.** When the late climax is in the last 2 bins, the last bin is a median 58% of the climax's height (n = 57). With a ≤20 s tail it is 22% (n = 134); 20-60 s, 6% (n = 145); over 60 s, 5% (n = 239). In the classified set, the 6 videos that end ≤5 s after the result card have a median last bin of 0.56, against 0.11-0.12 for those with longer tails. — [ends_out.txt; e.g. kOccoMYydwI](https://www.youtube.com/watch?v=kOccoMYydwI)
10. **Heatmap shape does not predict views.** Across 779 videos, Spearman ρ with views relative to the channel median is −0.04 for opening strength, −0.02 for end strength, 0.02 for peak position and −0.05 for the number of high bins; no channel exceeds |0.36|. Likes per view correlate with age (+0.58) and length (−0.32), and only weakly with sustained interest: +0.18 for bins ≥0.6 and +0.19 for body mean. — [stats_out.txt](https://www.youtube.com/@jokerclipss/videos)
11. **Crates get the fewest views relative to each channel.** Within-channel relative views are 0.65 (Goblin second), 0.79 (Jokerclips), 0.81 (LoLzZz Plays) and 1.00 (LoLzZz main, n = 3). In crate videos the only peak is the jackpot pull: 75% in [z1jXPJN8z-c](https://www.youtube.com/watch?v=z1jXPJN8z-c), 86% in [mk_Ne_mk_70](https://www.youtube.com/watch?v=mk_Ne_mk_70), 95% in [72gO2p-DjEg](https://www.youtube.com/watch?v=72gO2p-DjEg). — [bgmi_rows.json](https://www.youtube.com/@goblinsh0rts/videos)

### Inferences
- (Inference) Because the curve is relative, "the opening is highest" mostly means everyone starts and many skip. The useful signal is **where the later spikes land**. Viewers scrub to fights, funny lines and payoffs, so an automatic editor can drop the stretches that skimmers skip anyway.
- (Inference) Since shape does not move views, the editor's job on retention is to remove skip-bait and pay off the title's promise. Getting views is the job of the title, thumbnail and people named (earlier studies).

### Gaps
- Absolute retention (the share of viewers still watching at time t) is not public. The heatmap cannot separate "skipped to" from "replayed".
- No official YouTube definition of the heatmap metric was found; it is described only in press coverage.

---

## Q1. Where are the peaks (top 3, points ≥0.6), and how do the first 10%, the post-intro dip and the last 10% behave?

### Takeaway
The single highest point sits anywhere. It is commonest in the first 10% (18%) and the last 10% (14%). Goblin's esports cuts cluster at both ends; LoLzZz Plays and Joker peak in the middle. Every video has a high start, a fall to baseline by about 8% and short spikes after that. Esports and kill videos rise again at the end; comedy and reaction videos fade.

### Cited Findings
- **Per-channel heatmap shape** (medians; "argmax" is the position of the highest point; data: `stats_out.txt`):

| Channel | n | Length s | Views | First 10% / mean | First 10% above mean | First bin | Highest point in first 10% | in 40-70% | in last 20% | Last 10% / mean | Any ≥0.6 in last 10% | Bins ≥0.6 | Likes/view |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Goblin main](https://www.youtube.com/@goblinbgmi/videos) | 105 | 349 | 159K | 1.62 | 79% | 0.58 | 34% | 19% | 30% | 1.31 | 43% | 5 | 8.1% |
| [Goblin second](https://www.youtube.com/@goblinsh0rts/videos) | 87 | 363 | 93K | 1.60 | 76% | 0.46 | 28% | 26% | 22% | 1.14 | 34% | 6 | 6.6% |
| [Joker main](https://www.youtube.com/@Jokerkihavelii/videos) | 107 | 514 | 343K | 0.94 | 43% | 0.32 | 11% | 33% | 24% | 0.65 | 22% | 5 | 9.7% |
| [Jokerclips](https://www.youtube.com/@jokerclipss/videos) | 322 | 482 | 156K | 1.23 | 61% | 0.39 | 17% | 28% | 21% | 0.75 | 27% | 6 | 7.5% |
| [LoLzZz main](https://www.youtube.com/@LoLzZzGaming/videos) | 49 | 755 | 304K | 1.47 | 90% | 0.32 | 12% | 27% | 29% | 1.65 | 49% | 5 | 6.8% |
| [LoLzZz Plays](https://www.youtube.com/@lolzzzplays/videos) | 109 | 578 | 118K | 1.20 | 66% | 0.26 | 7% | 40% | 17% | 1.14 | 27% | 4 | 6.0% |
| All | 779 | 486 | 160K | 1.30 | 65% | 0.38 | 18% | 29% | 23% | 0.96 | 31% | 5 | 7.3% |

- **Decile of the highest point** (counts, 0-10% … 90-100%): Goblin main [36, 5, 3, 6, 6, 3, 11, 3, 8, 24]; Goblin second [24, 5, 8, 5, 9, 6, 8, 3, 7, 12]; Joker main [12, 8, 9, 5, 11, 11, 13, 12, 17, 9]; Jokerclips [55, 27, 25, 24, 26, 29, 34, 34, 26, 42]; LoLzZz main [4, 2, 3, 5, 6, 2, 4, 5, 4, 10]; LoLzZz Plays [8, 6, 7, 9, 12, 17, 15, 16, 9, 10]; all [139, 53, 55, 54, 70, 68, 85, 73, 71, 107]. — [stats_out.txt](https://www.youtube.com/@goblinbgmi/videos)
- **All top-3 peaks** by decile, all channels: [424, 213, 187, 189, 205, 209, 205, 229, 201, 263]. Outside the opening, the top-3 peaks are spread almost evenly, with a modest bump in the last decile. — [stats_out.txt](https://www.youtube.com/@goblinbgmi/videos)
- **Mean heat by decile**: Goblin main 0.32, 0.18, 0.16, 0.16, 0.14, 0.14, 0.14, 0.12, 0.16, **0.26** (a U shape). Joker main 0.21, 0.18, 0.18, 0.16, 0.18, 0.19, 0.19, 0.21, 0.23, **0.16** (flat, fading at the end). LoLzZz main 0.25, 0.21, 0.16, 0.14, 0.15, 0.13, 0.12, 0.15, 0.15, **0.27**. LoLzZz Plays 0.21, 0.18, 0.15, 0.14, 0.14, 0.12, 0.15, 0.16, 0.14, 0.19. — [stats_out.txt](https://www.youtube.com/@LoLzZzGaming/videos)
- **Last 10 bins (90-99%)**: Goblin main 0.18, 0.21, 0.24, 0.28, 0.32, 0.33, 0.32, 0.27, 0.24, **0.15**. LoLzZz main 0.23 … 0.34 (96%), 0.33, 0.25, **0.15**. Joker main 0.20 … 0.14, 0.11, **0.07**. Jokerclips 0.19 … 0.15, **0.09**. The esports and record climax sits at about 94-97%, and the final 1-3% (end card or tail) drops. — [stats_out.txt](https://www.youtube.com/@goblinbgmi/videos)
- **By type** (first 10% / mean; highest point in last 20%; last 10% / mean): esports match 1.49 / 21% / 1.22; kills or record 1.36 / 32% / 1.39; challenge 1.45 / 20% / 1.01; versus or custom 1.37 / 20% / 1.03; banter or funny 1.18 / 21% / 0.77; crate 0.92 / 23% / 0.75; reaction 0.94 / 24% / 0.62. — [stats_out.txt](https://www.youtube.com/@goblinbgmi/videos)
- **By length**: 2-5 min videos open strongest (1.61; 38% have their highest point in the first 10%) and have the most high bins (median 8). In 10-20 min videos the highest point is in the first 10% only 7% of the time and in 40-70% 37% of the time. The 17 videos of 20-45 min have a weak opening (0.75) and a stronger end (1.17). — [stats_out.txt](https://www.youtube.com/@goblinbgmi/videos)
- **Shift over time**: the highest point fell in the first 10% for 31% of 2023 uploads and 9% of 2026 uploads, and in 40-70% for 18% (2023) against 43% (2026). The first bin fell from 0.53 (2023) to 0.26 (2026). Uploads also got longer over the same years (median 320 s in 2023, 510 s in 2026). — [stats_out.txt](https://www.youtube.com/@goblinbgmi/videos)

### Inferences
- (Inference) The drift of the main peak from the opening to the middle tracks the move to longer, multi-fight edits: the longer the video, the more the best fight sits mid-video. It also matches the lolzzz_deep finding that LoLzZz's maximum sits at 40-66% in 8 of 13 videos. This larger sample confirms it: LoLzZz Plays has its highest point in 40-70% in 40% of 109 videos.

### Gaps
- Heatmaps are missing for recent low-view uploads. Of the 53 recent long videos not yet in the earlier data, only 4 had one, so the sample under-represents October and November 2026.

---

## Q2. What is at the peaks, and what is not? (59 videos, captions plus storyboards)

### Takeaway
The peaks are moments with a payoff and a reaction: kill bursts and squad wipes; clutches and decisive rounds; the final fight running into the WWCD or VICTORY card; funny lines, roasts and prank payoffs with audible laughter; crate jackpots; reveals the title promised; and meme inserts on top of a kill. Flat parts are driving, rotations, holding in smoke or houses, looting, crate spins without a pull, and chat without a punchline.

### Cited Findings
**Classified main peaks (highest point after the first 5%) by channel:** Goblin main: final+result 6, kill burst 4, funny 1, reveal 1. Goblin second: kill 2, crate pull or reveal 2, funny 2, final+result 2. Joker main: funny 5, kill 1, crate 1. Jokerclips: funny 3, clutch 3, crate 2, kill 1, final+result 1. LoLzZz main: kill 4, clutch 3, final+result 3, funny 1, crate 1. LoLzZz Plays: kill 6, funny 3, final+result 1. — [classified.json, peaks_log.md](https://www.youtube.com/@goblinbgmi/videos)

**Kill bursts and squad wipes**
- [aA98jrFkEPQ](https://www.youtube.com/watch?v=aA98jrFkEPQ) (Goblin, 540K): ridge sniper kill burst at 84% ("ek aur le aao"), 1.0. The video ends on a #4 placing and the results table, and its end stays low.
- [6f0CK3fBrig](https://www.youtube.com/watch?v=6f0CK3fBrig) (Goblin second, 470K): rooftop multi-kill at 82%, 1.0.
- [kOccoMYydwI](https://www.youtube.com/watch?v=kOccoMYydwI) (LoLzZz Plays, 586K): hill fight with a cut to the opponent's POV and a double headshot at 58%, 1.0.
- [-9A2Hyty0Lg](https://www.youtube.com/watch?v=-9A2Hyty0Lg) (100-kill challenge): the match-3 kill burst at 84% as the count nears the goal; also 11% (0.95), early kills with an Oggy meme captioned in Hinglish.
- [Gn1AvcFXl-Y](https://www.youtube.com/watch?v=Gn1AvcFXl-Y) (61-kill record, 752K): a street kill burst plus a crowd-fight meme at 46% (1.0), and a garden fight plus memes at 16% (0.96).

**Clutch or decisive round**
- [lOAtTbOsCzQ](https://www.youtube.com/watch?v=lOAtTbOsCzQ): a 1v4 clutch with a facecam punch-in at 33%, 1.0.
- [lyHdl-U4yNQ](https://www.youtube.com/watch?v=lyHdl-U4yNQ) (935K): a pro's sniper 1v4 with a black-and-white freeze plus Joker's shock at 48%, 1.0; the next-highest point is 0.21.
- [lDPqaP7qvlg](https://www.youtube.com/watch?v=lDPqaP7qvlg) (593K): a TDM round that flips the score from 1-1 to 3-1 ("best comeback") at 37%, 1.0.
- [PtvEiSN48Dk](https://www.youtube.com/watch?v=PtvEiSN48Dk) (1.57M): the decisive 1v1 round in a side-by-side split, then the rival's facecam laughing at 70%, 1.0.

**Final fight plus result screen**
- [6jIQaYvIOGc](https://www.youtube.com/watch?v=6jIQaYvIOGc): final smoke fight to WWCD at 99% (0.95), ending about 5 s later.
- [pkXkzlxuNzw](https://www.youtube.com/watch?v=pkXkzlxuNzw) (669K): 99% (0.92).
- [67w15TWdikI](https://www.youtube.com/watch?v=67w15TWdikI) (605K): 97% (1.0).
- [ml5FitUoqf8](https://www.youtube.com/watch?v=ml5FitUoqf8): 94% (1.0).
- [MQ8SC-_e8ZQ](https://www.youtube.com/watch?v=MQ8SC-_e8ZQ) (382K): 84% and 92%; the video ends on the VICTORY card.
- [JAW7yVH8QCQ](https://www.youtube.com/watch?v=JAW7yVH8QCQ): 97% (1.0).
- [PRaUeGY8Sr8](https://www.youtube.com/watch?v=PRaUeGY8Sr8) (94-kill record, 853K): the kill count rising on the results table ("30 40 50 60 65… 25 short") at 35% (1.0), and the final chicken dinner with the count reaching 94 at 93% (0.76).

**Funny line, roast, failure or prank payoff, with laughter**
- [3c0nLXL8k6U](https://www.youtube.com/watch?v=3c0nLXL8k6U): a 1-HP chaos moment with a [laughter] tag, a meme and a facecam laugh at 88%, 1.0.
- [TIDXJ1YeirM](https://www.youtube.com/watch?v=TIDXJ1YeirM): "both of us couldn't kill him" with [laughter] at 68%, 1.0.
- [Du8VpIvMs04](https://www.youtube.com/watch?v=Du8VpIvMs04): the betrayal payoff with two facecams laughing at 89%, 1.0.
- [7TkLt-j3u4A](https://www.youtube.com/watch?v=7TkLt-j3u4A): a teammate thrown out of the zone by a car, [laughter], then the VICTORY round card at 87%, 1.0.
- [EjaP5wHkv8w](https://www.youtube.com/watch?v=EjaP5wHkv8w) (603K): the final round, VICTORY, then the loser's forfeit banter at 85-95% (0.9-1.0).
- Rival trash talk is dense in [sT0sYDstN_k](https://www.youtube.com/watch?v=sT0sYDstN_k) (746K), which holds 0.3-0.7 throughout.

**Crate pull or reveal**
- [z1jXPJN8z-c](https://www.youtube.com/watch?v=z1jXPJN8z-c) (686K): "YOU GOT" / CONGRATULATIONS jackpots intercut with celebrity reaction memes at 76%, 1.0. Heat at 0-65% is 0.0-0.3.
- [mk_Ne_mk_70](https://www.youtube.com/watch?v=mk_Ne_mk_70): the AKM obtained plus a KBC "7 crore" meme at 86%.
- [72gO2p-DjEg](https://www.youtube.com/watch?v=72gO2p-DjEg): the final set reveal at 95%.
- [ixzk66I3_g4](https://www.youtube.com/watch?v=ixzk66I3_g4): a lucky-draw pull inside a gameplay video at 73%, 1.0; everything else is 0.34 or lower.
- In the real-world mystery box [Vjc1H9rt7xI](https://www.youtube.com/watch?v=Vjc1H9rt7xI), every peak is an item reveal (47%, 16%, 70%).

**Meme or edit inserts**
- Peaks fall on labelled memes over kills in [EJTupVtHuY8](https://www.youtube.com/watch?v=EJTupVtHuY8) ("IGL / LOLZZZ" office meme at 45%), [PtvEiSN48Dk](https://www.youtube.com/watch?v=PtvEiSN48Dk) (black-and-white facecam with a caption meme, second peak at 34%) and [6f0CK3fBrig](https://www.youtube.com/watch?v=6f0CK3fBrig) ("Friday" meme, 10%).
- A meme inserted into a flat stretch does not lift it: [z1jXPJN8z-c](https://www.youtube.com/watch?v=z1jXPJN8z-c) 4:39 sits in a 64 s run below 0.08.

**Lobby can peak only with a joke**
- [U21BOYlKr2g](https://www.youtube.com/watch?v=U21BOYlKr2g) (676K): lobby chat-reading banter ("players are scared of my name") at 12%, 0.92.
- In [tt1gwGtxjlU](https://www.youtube.com/watch?v=tt1gwGtxjlU) (1.42M) the peaks are a raid and a chat call-to-action, not gameplay.

**What is not a peak.** These are the longest runs below 0.08, read frame by frame:

| Video | Run | What is on screen |
|---|---|---|
| [6jIQaYvIOGc](https://www.youtube.com/watch?v=6jIQaYvIOGc) | 113-160 s | creeping in smoke and scoping; comms plan nades and smoke |
| [67w15TWdikI](https://www.youtube.com/watch?v=67w15TWdikI) | 400-562 s | holding a compound, peeking, an inventory screen |
| [ml5FitUoqf8](https://www.youtube.com/watch?v=ml5FitUoqf8) | 237-285 s | car rotation, lying in grass, scope watching |
| [OOnDKF-Wprs](https://www.youtube.com/watch?v=OOnDKF-Wprs) | 393-460 s | prone on a hillside, car |
| [7bmUiiUuAdE](https://www.youtube.com/watch?v=7bmUiiUuAdE) | 219-375 s | driving across fields, scoping without kills |
| [fbVXWfefL8c](https://www.youtube.com/watch?v=fbVXWfefL8c) | 375-537 s | looting houses, running, car |
| [Car5bJ_yP-E](https://www.youtube.com/watch?v=Car5bJ_yP-E) | 357-560 s | the same yellow car driving, one facecam beat |
| [uuTVkDWOYus](https://www.youtube.com/watch?v=uuTVkDWOYus) | 306-434 s | rooftop running, car |
| [1bSJjsh33kM](https://www.youtube.com/watch?v=1bSJjsh33kM) | 57-131 s | scoping, a match-ranking table |
| [3c0nLXL8k6U](https://www.youtube.com/watch?v=3c0nLXL8k6U) | 250-337 s | two-facecam chat, lobby |
| [z1jXPJN8z-c](https://www.youtube.com/watch?v=z1jXPJN8z-c) | 253-317 s | low-tier "YOU GOT" spins, colour bars, a text meme |

Source: `sheets/_lows.jpg`.

### Inferences
- (Inference) A peak needs an event and a visible or audible payoff in the same 10-20 s: a kill feed plus a shout, a result card plus a facecam, a pull plus a meme, a line plus [laughter]. Gameplay-only kills without a reaction still peak on Goblin's clean POV edits, where the comms are loud.
- (Inference) Even in edited uploads the creators' editors keep 47-200 s of flat travel or holding. Kaatclip can compress these more than the human editors do without losing what viewers watch.

### Gaps
- I could not hear the audio. "Shout", "scream" and "laughter" come from auto-caption tags ([हंसी], [चीखने की आवाज़]) and words, and storyboard frames are 2-10 s apart. Ten classifications rest on captions only.

---

## Q3. Openings: high or low, and what do strong openings show?

### Takeaway
How high the first 10% sits relative to the rest depends mostly on the channel and the type of video. The kind of opening I could see made no measurable difference. Gameplay, esports and kill videos open relatively higher; reaction and crate videos lower. Every opening style seen (teaser, goal line, funny-line teaser, straight gameplay) sits in the same range. Whatever is shown, about half the viewers who start are gone from that point within ~10-20 s.

### Cited Findings
- **Opening styles in the 59 classified videos** (median first-10% heat; first 10% / mean; n):

| Opening style | Median first 10% | First 10% / mean | n |
|---|---|---|---|
| Funny line or "IN THIS VIDEO" teaser of funny lines | 0.29 | 1.47 | 11 |
| Teaser of later action | 0.19 | 1.43 | 9 |
| Goal or stakes statement | 0.16 | 1.17 | 19 |
| Straight gameplay | 0.16 | 1.41 | 19 |
| Caster hype clip | 0.25 | — | 1 |

Source: `classified.json`. The samples are small and the differences are within noise.
- **Teaser openings**:
  - Goblin's 20 s teaser of the final fight, then a signature card: [MQ8SC-_e8ZQ](https://www.youtube.com/watch?v=MQ8SC-_e8ZQ) starts at 0.9, dips to 0.2 at 4% and is back at 0.8 by 8-9%, the first fight after the card; [OOnDKF-Wprs](https://www.youtube.com/watch?v=OOnDKF-Wprs) is 0.6 and then 0.1.
  - The montage of three fights from other matches in [6jIQaYvIOGc](https://www.youtube.com/watch?v=6jIQaYvIOGc) is the video's highest point (1.0 at 2%).
- **Goal or stakes statements, typical on LoLzZz**:
  - "Can we reach 55 kills today?" ([Gn1AvcFXl-Y](https://www.youtube.com/watch?v=Gn1AvcFXl-Y)).
  - "Three games back to back, 100 kills" ([-9A2Hyty0Lg](https://www.youtube.com/watch?v=-9A2Hyty0Lg)).
  - Rules lines in per-kill challenges ([3i83F-jSotA](https://www.youtube.com/watch?v=3i83F-jSotA), [7bmUiiUuAdE](https://www.youtube.com/watch?v=7bmUiiUuAdE), [KzSEzZBOpns](https://www.youtube.com/watch?v=KzSEzZBOpns)).
  - Crate stakes: "if I lose today I stop crate openings" ([z1jXPJN8z-c](https://www.youtube.com/watch?v=z1jXPJN8z-c)).
  - Hater quotes ("he has no skills, just an average player") in [lOAtTbOsCzQ](https://www.youtube.com/watch?v=lOAtTbOsCzQ).
  - These openings sit at 0.1-0.4, and the first fight after them often re-rises: 67% of LoLzZz main videos re-rise inside the first 10%.
- **Funny-line openings**:
  - Joker's "IN THIS VIDEO" black-and-white teaser of three subtitled lines ([3c0nLXL8k6U](https://www.youtube.com/watch?v=3c0nLXL8k6U), [Ul5mEjNyzu4](https://www.youtube.com/watch?v=Ul5mEjNyzu4)) sits at only 0.1-0.4.
  - A single flirt line opening "Flirting with a girl challenge" ([gs8thi_U_fU](https://www.youtube.com/watch?v=gs8thi_U_fU), 330K) is the video's highest point (1.0), and nothing later passes 0.4.
  - A trash-talk opening ([sT0sYDstN_k](https://www.youtube.com/watch?v=sT0sYDstN_k)) starts at 1.0.
- **Straight gameplay openings**:
  - [4rDLrncqmCc](https://www.youtube.com/watch?v=4rDLrncqmCc) opens inside fights and holds 1.0 and 0.9 over the first two 5% blocks.
  - [ml5FitUoqf8](https://www.youtube.com/watch?v=ml5FitUoqf8) runs parachute into landing fight and holds 0.4-0.5 through 25%.
- **Opening falls by channel**: the median time for heat to halve is 10.3 s (Goblin main), 11.2 s (Goblin second), 12.6 s (Joker main), 14.4 s (Jokerclips), 16.1 s (LoLzZz Plays) and 19.8 s (LoLzZz main). — [measured](https://www.youtube.com/@goblinbgmi/videos)
- **Opening strength and views**: across quartiles of first-10% / mean, relative views are 1.01, 1.01, 0.97 and 1.01, and likes per view 7.7%, 7.2%, 7.0% and 7.3%. No relation. — [ends_out.txt](https://www.youtube.com/@goblinbgmi/videos)

### Inferences
- (Inference) An opening that is itself a payoff (a fight, a funny line, a trash-talk exchange) is watched as much as anything later in the video. A facecam goal statement or a stylised title card is watched less, though it may help the title promise. LoLzZz's pattern of a goal line followed by a fast first fight produces the second rise.
- (Inference) The "IN THIS VIDEO" teaser of funny lines does not keep Joker's first 10% above his channel's usual level (0.94-1.23 across his two channels). Its value, if any, is not visible in the heatmap.

### Gaps
- A causal test (the same video with different openings) is impossible from public data. Click-through and the share of viewers who leave in the first 30 s are not public.

---

## Q4. Endings: does attention hold to the result screen, and do short tails keep more?

### Takeaway
On match and record videos attention rises into the final fight and the result. Whatever follows the result loses most of its viewers within 10-20 s. Videos that end on the result card keep their final seconds watched at about half the climax level; tails longer than 20 s fall to about 5% of it. None of this shows up in views or likes.

### Cited Findings
- **Videos with a climax ≥0.5 in the last 30%**: 518 of 779. Last bin as a share of the climax (median): climax in the last 2 bins 0.58 (n = 57); tail ≤20 s 0.22 (n = 134); 20-60 s 0.06 (n = 145); over 60 s 0.05 (n = 239). The mean heat over the tail, as a share of the climax, is 0.63 / 0.47 / 0.30 / 0.20. Relative views by group are 1.01 / 0.96 / 0.95 / 1.02, and likes per view 6.7% / 7.2% / 7.9% / 7.1%. — [ends_out.txt](https://www.youtube.com/@goblinbgmi/videos)
- **Classified endings** (median last 10% and last bin):

| Ending | Last 10% | Last bin | n |
|---|---|---|---|
| Ends ≤5 s after the result card | 0.46 | 0.56 | 6 |
| Result then ≤20 s | 0.24 | 0.11 | 20 |
| Result then over 20 s of tail | 0.18 | 0.12 | 9 |
| No result screen, cut mid-play | 0.16 | 0.06 | 8 |
| Outro card or a different segment | 0.07 | 0.00 | 5 |

Source: `classified.json`.
- **Examples of ending on the card**:
  - [kOccoMYydwI](https://www.youtube.com/watch?v=kOccoMYydwI) ends on the final VICTORY card at 14:58; its last 3 bins are 0.4, 0.8 and 0.5 after a near-0 stretch.
  - [MQ8SC-_e8ZQ](https://www.youtube.com/watch?v=MQ8SC-_e8ZQ) ends on the VICTORY card at 6:14 (last 10% 0.3-0.8).
  - [6jIQaYvIOGc](https://www.youtube.com/watch?v=6jIQaYvIOGc) runs WWCD at 5:08 and ends about 5 s later, with the last bins at 0.89-0.95.
- **Examples of long tails**:
  - [lDPqaP7qvlg](https://www.youtube.com/watch?v=lDPqaP7qvlg): 50 s of facecam after the Defeat table (0.27).
  - [TIDXJ1YeirM](https://www.youtube.com/watch?v=TIDXJ1YeirM): 45 s of lobby chat after VICTORY (0.0-0.2).
  - [3c0nLXL8k6U](https://www.youtube.com/watch?v=3c0nLXL8k6U): a 45 s camera segment (0.0-0.1).
  - [Car5bJ_yP-E](https://www.youtube.com/watch?v=Car5bJ_yP-E): about 60 s of facecam celebration (0.3).
  - [Du8VpIvMs04](https://www.youtube.com/watch?v=Du8VpIvMs04): a "Thanks for watching" / subscribe card; last bin 0.0.
- **Where record payoffs hold**: [-9A2Hyty0Lg](https://www.youtube.com/watch?v=-9A2Hyty0Lg) (results table, then a facecam verdict) rises to 0.6 in the last 5% before falling to 0.2. [PRaUeGY8Sr8](https://www.youtube.com/watch?v=PRaUeGY8Sr8) (count to 94, then celebration) holds about 0.5. Viewers stay for the number.
- **A peak decays the same way wherever it is**: the curve around a late climax (n = 267) matches the curve around a mid-video peak (n = 534), at 0.31 of the peak after 10 s and 0.16 after 20 s. — [decay_out.txt](https://www.youtube.com/@goblinbgmi/videos)

### Inferences
- (Inference) After the payoff, viewers stop watching about as fast as they do after any other spike (within 10-20 s). A tail costs nothing in views but is barely watched: keep 3-8 s of result card and reaction, then end.
- (Inference) The no-result endings (cut mid-play, [4rDLrncqmCc](https://www.youtube.com/watch?v=4rDLrncqmCc), [PiGMtVEVJKw](https://www.youtube.com/watch?v=PiGMtVEVJKw)) still peak on their last big fight, so the final fight matters more than the card itself. The card helps the last seconds hold.

### Gaps
- I cannot tell whether a short tail changes session behaviour, such as clicking an end-screen video, which YouTube may reward. End-screen click-through is not public.

---

## Q5. Do the kind of peaks, the opening or the ending relate to views or likes per view?

### Takeaway
Within each channel, heatmap shape tells nothing about views. Peak type relates to views only through the type of video. Crate videos sit below their channel's median; versus and custom-room videos sit at or above it on Goblin. Likes per view are higher on older and shorter videos, and only slightly higher where interest is sustained.

### Cited Findings
- **Spearman ρ with relative views** (views / channel median) across 779 videos:

| Measure | ρ |
|---|---|
| First 10% / mean | −0.04 |
| Last 10% / mean | −0.02 |
| Position of the highest point | 0.02 |
| Bins ≥0.6 | −0.05 |
| Body mean | −0.02 |
| Length | 0.19 |

  The strongest per-channel values are Joker main's dip depth (−0.36) and length (+0.43). — [stats_out.txt](https://www.youtube.com/@goblinbgmi/videos)
- **Spearman ρ with likes per view**: age +0.58, length −0.32, bins ≥0.6 +0.18, body mean +0.19. Quartiles of body mean give likes per view of 6.8%, 7.0%, 7.5% and 7.8%. — [stats_out.txt, ends_out.txt](https://www.youtube.com/@goblinbgmi/videos)
- **Relative views by type within channel** (median, n): crate 0.65 (Goblin second, 3), 0.79 (Jokerclips, 25), 0.81 (LoLzZz Plays, 9). Versus or custom 1.68 (Goblin main, 8), 1.02-1.07 elsewhere. Kills or record 1.13 (Goblin second), 1.26 (Jokerclips), 1.04-1.10 (LoLzZz), but 0.75 on Goblin main (41). Reaction 1.67 on LoLzZz Plays (14), 0.86 on Jokerclips (61). — [bgmi_rows.json](https://www.youtube.com/@goblinbgmi/videos)
- **Main-peak class in the 59-video set** (median relative views, likes per view):

| Main peak | Relative views | Likes per view | n |
|---|---|---|---|
| Clutch or decisive round | 3.65 | 3.8% | 6 |
| Final + result | 1.71 | 7.0% | 13 |
| Kill burst | 1.70 | 4.1% | 18 |
| Funny or banter | 1.32 | 5.4% | 15 |
| Reveal or pull | 1.07 | 6.6% | 7 |

  The set was chosen to include each channel's top-viewed videos, so relative views are inflated. The clutch group includes the 1.57M LoLzZz-vs-Jonathan 1v1 and the 935K pro-reaction video. Likes per view are lower in that group because of its reaction videos and a cross-channel mix. — [classified.json](https://www.youtube.com/@goblinbgmi/videos)

### Inferences
- (Inference) Clutches and decisive 1v1 rounds may draw more views, which would fit "rivals and named people lift views" in the A-to-Z study. With n = 6 and a biased selection, this is a hypothesis, not a finding.
- (Inference) For Kaatclip, retention editing (what to keep or cut) and packaging (title, thumbnail, people) are separate levers. The heatmap informs only the first.

### Gaps
- Watch time, average view duration and impressions click-through are private, so whether a better curve raises recommendation could not be tested.

---

## Rules for an automatic editor (each with its evidence)

### Takeaway
Build the long highlight as a chain of payoff windows of about 15-25 s each, with the bridges between them cut hard. Open on a payoff, keep fights and their reactions whole, pay off the title's promise and end within seconds of the result. Every rule below is measurable.

### Cited Findings
1. **The first 3-10 s must be a payoff, not a title card or a wind-up.** Use the best kill burst or clutch, or the funniest line with the laugh (comedy), or trash talk (rivalry). Evidence: heat halves within a median 13.7 s. Openings that were themselves payoffs were each video's highest point ([6jIQaYvIOGc](https://www.youtube.com/watch?v=6jIQaYvIOGc) montage, [gs8thi_U_fU](https://www.youtube.com/watch?v=gs8thi_U_fU) line, [sT0sYDstN_k](https://www.youtube.com/watch?v=sT0sYDstN_k) trash talk). Facecam goal lines and title art sit at 0.1-0.4.
2. **Keep any spoken goal or stakes line, but put it right after the hook, keep it to one sentence, and follow it with action within ~10 s.** Evidence: LoLzZz's goal lines precede a re-rise inside the first 10% in 67% of his main-channel videos; the goal line itself sits at 0.1-0.4.
3. **Unit = a payoff window of about the peak minus 10-15 s to the peak plus 5-10 s.** Evidence: a peak runs from 0.44 at −10 s to 1.0 to 0.31 at +10 s, and the top peak's half-height width is a median 14.9 s.
4. **Keep fights whole from the first shot or knock to the last kill-feed line, and include the reaction after it.** Evidence: top peaks combine the event with the reaction ([PtvEiSN48Dk](https://www.youtube.com/watch?v=PtvEiSN48Dk) rival laugh, [fbVXWfefL8c](https://www.youtube.com/watch?v=fbVXWfefL8c) head in hands, [Ul5mEjNyzu4](https://www.youtube.com/watch?v=Ul5mEjNyzu4) laugh after a wipe, [uuTVkDWOYus](https://www.youtube.com/watch?v=uuTVkDWOYus) victim's line).
5. **Space the payoffs about every 50-90 s, and never leave more than ~30 s without one.** Evidence: the median gap between peaks ≥0.35 is 52-62 s on Goblin and Jokerclips and 92-109 s on LoLzZz. Even so, the human edits keep 47-203 s runs below 0.08.
6. **Cut or compress to 2-5 s:** driving, rotation, creeping or holding in smoke and compounds, looting and inventory, scoping with no kill, crate spins with no jackpot, and facecam or lobby chat with no punchline. Evidence: all of these sat in the flattest runs of 12 videos (`sheets/_lows.jpg`). A meme placed on top of such a stretch did not lift it ([z1jXPJN8z-c](https://www.youtube.com/watch?v=z1jXPJN8z-c) 4:39).
7. **Keep lobby or chat only when it carries a laugh or banter between named people.** Evidence: lobby banter peaked (0.92) in [U21BOYlKr2g](https://www.youtube.com/watch?v=U21BOYlKr2g); plain chat formed the flat runs in [3c0nLXL8k6U](https://www.youtube.com/watch?v=3c0nLXL8k6U).
8. **Find the moment the title promises and make sure it is in the edit, whole.** If the title asks a question ("WWCD ?"), the answer is the climax. Evidence: [0Ug9nHMiD24](https://www.youtube.com/watch?v=0Ug9nHMiD24) (heat ~0 until the pan WWCD at 95%), [-ieo36Gj9Hk](https://www.youtube.com/watch?v=-ieo36Gj9Hk), [LEwadYEz0Eo](https://www.youtube.com/watch?v=LEwadYEz0Eo), [nucVWiaxxVg](https://www.youtube.com/watch?v=nucVWiaxxVg).
9. **Put the best mid-match fight around 30-65% of a 6-20 min edit.** Keep the final fight for the last 10% only when the match was won or a record was reached. Evidence: the highest point falls in 40-70% in 37% of 10-20 min videos (40% on LoLzZz Plays), and in the last 20% in 30% of Goblin main videos, where the payoff is the WWCD.
10. **Record and challenge videos: show the running count, and end on the count reaching the goal.** Evidence: the count rising on the results table was the highest point of [PRaUeGY8Sr8](https://www.youtube.com/watch?v=PRaUeGY8Sr8) at 35%, and its end held about 0.5. [-9A2Hyty0Lg](https://www.youtube.com/watch?v=-9A2Hyty0Lg)'s results-plus-verdict end rose to 0.6.
11. **Crate segments: cut the spins to a few seconds each, build to the jackpot and end shortly after it.** Do not reveal the jackpot first, except as a 1-2 s "YOU GOT" flash. Evidence: the only crate peaks were jackpots at 75-95%; spins sat at 0.0-0.3 ([z1jXPJN8z-c](https://www.youtube.com/watch?v=z1jXPJN8z-c), [mk_Ne_mk_70](https://www.youtube.com/watch?v=mk_Ne_mk_70), [72gO2p-DjEg](https://www.youtube.com/watch?v=72gO2p-DjEg)). Crate videos also run below each channel's median views (0.65-0.81). Treat them as a low-priority product.
12. **End within 3-8 s after the WWCD, VICTORY or results card, or after the final punchline.** Never add more than ~10 s of facecam, lobby, "thanks for watching" or another segment. Evidence: the last bin is 58% of the climax when the video ends on it, 22% with a ≤20 s tail and 5-6% beyond that. The 6 videos ending ≤5 s after the card hold a median last bin of 0.56, against 0.11-0.12 with longer tails.
13. **Comedy cuts (Joker-style): rank units by laugh tags, roasts and failures between named teammates, and still keep squad wipes.** Evidence: Joker's main peaks were group laughs, prank payoffs and failures. A squad wipe with a laugh was the top peak of [Ul5mEjNyzu4](https://www.youtube.com/watch?v=Ul5mEjNyzu4). Comedy videos fade at the end (last 10% / mean 0.65-0.75), so end on the best laugh, not on a tail.
14. **A labelled meme, freeze or zoom can go on top of a real payoff, never in place of one.** Evidence: memes over kills peaked ([EJTupVtHuY8](https://www.youtube.com/watch?v=EJTupVtHuY8), [Gn1AvcFXl-Y](https://www.youtube.com/watch?v=Gn1AvcFXl-Y), [-9A2Hyty0Lg](https://www.youtube.com/watch?v=-9A2Hyty0Lg), and the black-and-white freeze on [lyHdl-U4yNQ](https://www.youtube.com/watch?v=lyHdl-U4yNQ)); memes in flat stretches did not.
15. **Shorts (inference from the long-video heatmaps): cut each Short from one peak window, start 1-3 s before the event, and end on the reaction or result card.** Evidence: windows of about 15-25 s hold the whole spike, and the reaction is part of what viewers rewatch. YouTube does not show "most replayed" on Shorts, so this could not be checked on Shorts themselves (a third-party guide says it does not appear on Shorts: [TubeRanker](https://tuberanker.com/blog/most-replayed-youtube-feature)).

### Inferences
- (Inference) Kaatclip's scorer can be tested against these heatmaps. For the 779 videos with known peaks, the windows Kaatclip ranks highest should overlap the top-3 heatmap peaks far above chance. This is possible only where the source stream is also available. It was not done here.

### Gaps
- None of these rules has been A/B tested on a Kaatclip upload. They describe what viewers of these six channels watch, not a proven effect on views.

---

## What I could not measure

### Takeaway
The heatmap is relative and coarse, and audio was unavailable, so all conclusions are about where attention concentrates, not how many people stayed.

### Cited Findings
- **The heatmap is min-max normalised (0-1) per video**: measured in all 779. It cannot give absolute drop-off or compare levels across videos, and only videos with enough views have one. Third-party guides say a video needs enough viewing data before the graph appears ([TubeRanker](https://tuberanker.com/blog/most-replayed-youtube-feature)); the smallest view count with a heatmap in this set is 50K.
- **Bins are 1% of the video** (2-27 s, depending on length), and storyboard frames are 2-10 s apart, so the moment inside a peak is located to within about 5 s. — [measured](https://www.youtube.com/@goblinbgmi/videos)
- **I could not hear the audio**. Shouts, laughter and music were inferred from auto-caption tags and words. Auto-captions are noisy, and some peaks have no captions (music-only).
- **Peak classification is my reading** of frames and captions. Ten of the 59 rest on captions alone, and the categories overlap (a clutch is also a kill burst).
- **Video type comes from titles**. Joker videos with names but no game words were counted as banter, which mixes some non-BGMI talk in. Views are a snapshot from 12-14 Nov 2026, and older videos have had years to accumulate views.
- **Recent uploads are missing**: 53 recent long videos lacked earlier data and only 4 had a heatmap, so October and November 2026 are thin. The sample also under-represents low-view videos, which have no heatmap at all.

### Inferences
- (Inference) The owner can see the full curve, including absolute retention and the drop in the first 30 s, in YouTube Studio for any channel he controls. Kaatclip's own uploads (or a pilot creator's) are the only way to measure the absolute effect of these rules.

### Gaps
- Retention curves, average view duration, click-through and traffic sources for these channels are private.

---

## Appendix: the 59 classified videos

Opening: T = teaser of later action, G = goal or stakes line, F = funny line or teaser of funny lines, S = straight gameplay, C = caster hype clip. Ending: R0 = ends ≤5 s after the result card, R = result then ≤20 s, RT = result then over 20 s, N = no result screen or abrupt cut, O = outro card or another segment, "-" = not a match video. Per-peak notes with timestamps are in `peaks_log.md`.

| Video | Channel | Length s | Views | Opening | Main peak (after first 5%) | Peak at | Ending | First 10% | Last 10% |
|---|---|---|---|---|---|---|---|---|---|
| [pkXkzlxuNzw](https://www.youtube.com/watch?v=pkXkzlxuNzw) | goblin_main | 166 | 669K | S | final+result | 98% (0.92) | R0 | 0.41 | 0.44 |
| [67w15TWdikI](https://www.youtube.com/watch?v=67w15TWdikI) | goblin_main | 624 | 605K | C | final+result | 96% (1.00) | R | 0.25 | 0.39 |
| [aA98jrFkEPQ](https://www.youtube.com/watch?v=aA98jrFkEPQ) | goblin_main | 521 | 540K | S | kill burst | 83% (1.00) | N | 0.23 | 0.19 |
| [OOnDKF-Wprs](https://www.youtube.com/watch?v=OOnDKF-Wprs) | goblin_main | 516 | 459K | T | kill burst | 49% (1.00) | R | 0.19 | 0.38 |
| [MQ8SC-_e8ZQ](https://www.youtube.com/watch?v=MQ8SC-_e8ZQ) | goblin_main | 384 | 381K | T | final+result | 83% (1.00) | R0 | 0.55 | 0.47 |
| [gs8thi_U_fU](https://www.youtube.com/watch?v=gs8thi_U_fU) | goblin_main | 287 | 329K | F | funny/banter | 21% (0.36) | - | 0.28 | 0.06 |
| [6jIQaYvIOGc](https://www.youtube.com/watch?v=6jIQaYvIOGc) | goblin_main | 313 | 272K | T | final+result | 98% (0.95) | R0 | 0.61 | 0.48 |
| [4rDLrncqmCc](https://www.youtube.com/watch?v=4rDLrncqmCc) | goblin_main | 164 | 239K | S | kill burst | 5% (0.94) | N | 0.73 | 0.25 |
| [0Ug9nHMiD24](https://www.youtube.com/watch?v=0Ug9nHMiD24) | goblin_main | 253 | 204K | S | final+result | 94% (1.00) | R | 0.14 | 0.58 |
| [PiGMtVEVJKw](https://www.youtube.com/watch?v=PiGMtVEVJKw) | goblin_main | 265 | 159K | S | kill burst | 92% (1.00) | N | 0.45 | 0.47 |
| [Vjc1H9rt7xI](https://www.youtube.com/watch?v=Vjc1H9rt7xI) | goblin_main | 708 | 154K | G | reveal/pull | 47% (1.00) | O | 0.26 | 0.17 |
| [ml5FitUoqf8](https://www.youtube.com/watch?v=ml5FitUoqf8) | goblin_main | 365 | 133K | S | final+result | 93% (1.00) | R | 0.44 | 0.52 |
| [6f0CK3fBrig](https://www.youtube.com/watch?v=6f0CK3fBrig) | goblin_shorts | 462 | 468K | S | kill burst | 81% (1.00) | N | 0.24 | 0.06 |
| [LEwadYEz0Eo](https://www.youtube.com/watch?v=LEwadYEz0Eo) | goblin_shorts | 292 | 272K | S | reveal/pull | 70% (1.00) | - | 0.06 | 0.04 |
| [7TkLt-j3u4A](https://www.youtube.com/watch?v=7TkLt-j3u4A) | goblin_shorts | 905 | 271K | S | funny/banter | 86% (1.00) | RT | 0.11 | 0.10 |
| [-ieo36Gj9Hk](https://www.youtube.com/watch?v=-ieo36Gj9Hk) | goblin_shorts | 328 | 224K | S | final+result | 98% (1.00) | R0 | 0.28 | 0.48 |
| [mk_Ne_mk_70](https://www.youtube.com/watch?v=mk_Ne_mk_70) | goblin_shorts | 269 | 180K | G | reveal/pull | 85% (1.00) | R | 0.07 | 0.15 |
| [wPQrk8ljIsA](https://www.youtube.com/watch?v=wPQrk8ljIsA) | goblin_shorts | 149 | 100K | F | funny/banter | 23% (0.94) | - | 0.84 | 0.22 |
| [gcMmuGTJekc](https://www.youtube.com/watch?v=gcMmuGTJekc) | goblin_shorts | 140 | 67K | G | final+result | 90% (1.00) | R | 0.30 | 0.52 |
| [qUh8vOrLo7w](https://www.youtube.com/watch?v=qUh8vOrLo7w) | goblin_shorts | 378 | 57K | T | kill burst | 51% (1.00) | N | 0.43 | 0.15 |
| [_7WVFXJ9hkk](https://www.youtube.com/watch?v=_7WVFXJ9hkk) | joker_main | 416 | 1711K | S | funny/banter | 54% (1.00) | - | 0.30 | 0.04 |
| [NhCXmkOWz_g](https://www.youtube.com/watch?v=NhCXmkOWz_g) | joker_main | 464 | 366K | G | reveal/pull | 95% (1.00) | R0 | 0.06 | 0.40 |
| [8Au8-kSBhgg](https://www.youtube.com/watch?v=8Au8-kSBhgg) | joker_main | 488 | 337K | F | funny/banter | 65% (1.00) | - | 0.29 | 0.06 |
| [3c0nLXL8k6U](https://www.youtube.com/watch?v=3c0nLXL8k6U) | joker_main | 480 | 212K | F | funny/banter | 87% (1.00) | O | 0.11 | 0.04 |
| [Ul5mEjNyzu4](https://www.youtube.com/watch?v=Ul5mEjNyzu4) | joker_main | 497 | 201K | F | kill burst | 67% (1.00) | N | 0.21 | 0.18 |
| [Du8VpIvMs04](https://www.youtube.com/watch?v=Du8VpIvMs04) | joker_main | 269 | 183K | F | funny/banter | 88% (1.00) | O | 0.41 | 0.19 |
| [TIDXJ1YeirM](https://www.youtube.com/watch?v=TIDXJ1YeirM) | joker_main | 492 | 170K | S | funny/banter | 67% (1.00) | RT | 0.07 | 0.08 |
| [tt1gwGtxjlU](https://www.youtube.com/watch?v=tt1gwGtxjlU) | jokerclips | 402 | 1419K | G | funny/banter | 27% (0.96) | - | 0.58 | 0.27 |
| [lyHdl-U4yNQ](https://www.youtube.com/watch?v=lyHdl-U4yNQ) | jokerclips | 487 | 933K | S | clutch/decisive | 47% (1.00) | O | 0.04 | 0.01 |
| [oPmzf8LnVTw](https://www.youtube.com/watch?v=oPmzf8LnVTw) | jokerclips | 242 | 879K | S | kill burst | 18% (1.00) | - | 0.48 | 0.07 |
| [U21BOYlKr2g](https://www.youtube.com/watch?v=U21BOYlKr2g) | jokerclips | 485 | 675K | F | funny/banter | 47% (1.00) | R | 0.40 | 0.35 |
| [EjaP5wHkv8w](https://www.youtube.com/watch?v=EjaP5wHkv8w) | jokerclips | 625 | 599K | S | final+result | 90% (1.00) | RT | 0.09 | 0.32 |
| [lDPqaP7qvlg](https://www.youtube.com/watch?v=lDPqaP7qvlg) | jokerclips | 1281 | 593K | F | clutch/decisive | 36% (1.00) | RT | 0.06 | 0.15 |
| [1bSJjsh33kM](https://www.youtube.com/watch?v=1bSJjsh33kM) | jokerclips | 567 | 207K | S | clutch/decisive | 60% (1.00) | - | 0.04 | 0.02 |
| [VuRDeNxsWrk](https://www.youtube.com/watch?v=VuRDeNxsWrk) | jokerclips | 650 | 150K | S | funny/banter | 66% (1.00) | - | 0.09 | 0.05 |
| [ixzk66I3_g4](https://www.youtube.com/watch?v=ixzk66I3_g4) | jokerclips | 560 | 106K | S | reveal/pull | 72% (1.00) | - | 0.15 | 0.05 |
| [72gO2p-DjEg](https://www.youtube.com/watch?v=72gO2p-DjEg) | jokerclips | 561 | 98K | F | reveal/pull | 94% (1.00) | R | 0.19 | 0.30 |
| [PtvEiSN48Dk](https://www.youtube.com/watch?v=PtvEiSN48Dk) | lolzzz_main | 1515 | 1573K | T | clutch/decisive | 69% (1.00) | R | 0.17 | 0.04 |
| [tjBXf-bRjxo](https://www.youtube.com/watch?v=tjBXf-bRjxo) | lolzzz_main | 1354 | 1065K | G | clutch/decisive | 77% (1.00) | O | 0.17 | 0.07 |
| [PRaUeGY8Sr8](https://www.youtube.com/watch?v=PRaUeGY8Sr8) | lolzzz_main | 765 | 852K | G | final+result | 34% (1.00) | RT | 0.23 | 0.53 |
| [Gn1AvcFXl-Y](https://www.youtube.com/watch?v=Gn1AvcFXl-Y) | lolzzz_main | 797 | 751K | G | kill burst | 46% (1.00) | RT | 0.16 | 0.18 |
| [z1jXPJN8z-c](https://www.youtube.com/watch?v=z1jXPJN8z-c) | lolzzz_main | 496 | 686K | G | reveal/pull | 75% (1.00) | N | 0.15 | 0.08 |
| [Car5bJ_yP-E](https://www.youtube.com/watch?v=Car5bJ_yP-E) | lolzzz_main | 812 | 595K | G | funny/banter | 40% (1.00) | RT | 0.12 | 0.17 |
| [fCCQkW1Uevk](https://www.youtube.com/watch?v=fCCQkW1Uevk) | lolzzz_main | 1179 | 441K | T | final+result | 46% (1.00) | R | 0.16 | 0.28 |
| [nucVWiaxxVg](https://www.youtube.com/watch?v=nucVWiaxxVg) | lolzzz_main | 887 | 405K | G | kill burst | 31% (1.00) | R | 0.17 | 0.05 |
| [-9A2Hyty0Lg](https://www.youtube.com/watch?v=-9A2Hyty0Lg) | lolzzz_main | 1451 | 370K | G | kill burst | 83% (1.00) | R | 0.31 | 0.20 |
| [fbVXWfefL8c](https://www.youtube.com/watch?v=fbVXWfefL8c) | lolzzz_main | 736 | 360K | T | final+result | 92% (1.00) | RT | 0.09 | 0.32 |
| [KzSEzZBOpns](https://www.youtube.com/watch?v=KzSEzZBOpns) | lolzzz_main | 619 | 272K | G | kill burst | 64% (1.00) | R | 0.14 | 0.21 |
| [lOAtTbOsCzQ](https://www.youtube.com/watch?v=lOAtTbOsCzQ) | lolzzz_main | 1183 | 257K | G | clutch/decisive | 32% (1.00) | R | 0.21 | 0.09 |
| [sT0sYDstN_k](https://www.youtube.com/watch?v=sT0sYDstN_k) | lolzzz_plays | 443 | 744K | F | funny/banter | 10% (0.72) | R | 0.43 | 0.34 |
| [kOccoMYydwI](https://www.youtube.com/watch?v=kOccoMYydwI) | lolzzz_plays | 918 | 585K | G | kill burst | 57% (1.00) | R0 | 0.22 | 0.21 |
| [7bmUiiUuAdE](https://www.youtube.com/watch?v=7bmUiiUuAdE) | lolzzz_plays | 577 | 365K | G | kill burst | 66% (1.00) | R | 0.15 | 0.17 |
| [EJTupVtHuY8](https://www.youtube.com/watch?v=EJTupVtHuY8) | lolzzz_plays | 731 | 265K | G | kill burst | 44% (1.00) | R | 0.07 | 0.14 |
| [DwvaNRtqy20](https://www.youtube.com/watch?v=DwvaNRtqy20) | lolzzz_plays | 668 | 201K | T | kill burst | 49% (1.00) | R | 0.09 | 0.11 |
| [3i83F-jSotA](https://www.youtube.com/watch?v=3i83F-jSotA) | lolzzz_plays | 549 | 198K | G | kill burst | 57% (1.00) | R | 0.10 | 0.07 |
| [kJYX-ojkSjQ](https://www.youtube.com/watch?v=kJYX-ojkSjQ) | lolzzz_plays | 197 | 155K | F | funny/banter | 45% (0.99) | - | 0.76 | 0.20 |
| [JAW7yVH8QCQ](https://www.youtube.com/watch?v=JAW7yVH8QCQ) | lolzzz_plays | 578 | 150K | T | final+result | 97% (1.00) | R | 0.20 | 0.48 |
| [uuTVkDWOYus](https://www.youtube.com/watch?v=uuTVkDWOYus) | lolzzz_plays | 493 | 133K | G | kill burst | 21% (1.00) | N | 0.11 | 0.06 |
| [exOuHIXBWEU](https://www.youtube.com/watch?v=exOuHIXBWEU) | lolzzz_plays | 636 | 86K | S | funny/banter | 50% (1.00) | RT | 0.16 | 0.20 |
