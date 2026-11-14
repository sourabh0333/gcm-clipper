# How the best BGMI videos open and close, and how title and thumbnail promise the opening

Study of 14 Nov 2026 for Kaatclip. Sample: **93 long videos**, 15-16 per channel (Goblin @goblinbgmi and @goblinsh0rts, Joker @Jokerkihavelii and @jokerclipss, LoLzZz @LoLzZzGaming and @lolzzzplays). For each channel the sample is the top-viewed BGMI gameplay videos plus the 6 most recent, plus crate and custom-room videos where those two were missing. Vlogs, reactions and IRL videos are left out. Upload dates run from 2019 to Nov 2026.

For each video I fetched fresh metadata (views, likes, YouTube's "most replayed" heatmap) and the thumbnail, which I looked at. I also fetched the full sb0 storyboard: 320x180 frames, 2 s apart on videos under about 5 min, 5 s apart on most, and 10 s apart on five long ones. The auto-captions came from the earlier studies' folders or were downloaded fresh. For each video I built a contact sheet: the thumbnail, the frames from 0 to 60 s, and the frames from the last 30 s. I then labelled the opening and the ending by hand and checked them against the captions. **84 of 93 videos have a heatmap.** The 9 without one are recent and low-view: wDgeZBn80VM, -qpx-ejuq9Q, and the 2026 BMSD and second-channel uploads.

Raw data, scripts and labels are in `C:\Users\soura\AppData\Local\Temp\claude\21027423ba80eb72\c7886632-c6c6-4a95-81c6-c6cbac2a769e\scratchpad\viewers\openings\`. That folder holds `labels.jsonl` (one hand label per video), `rows.json` (labels joined with the numbers), `summary.txt`, `curve.txt`, `sheets\` and `pairs\` (contact sheets), `thumbs\`, `meta\` and `sb\`.

**How to read the heatmap numbers.** YouTube's heatmap has 100 points, one per 1% of the video, each valued 0-1. It is relative within one video and does not give absolute retention. Point 0 is high in almost every video, because every viewer starts there. I therefore divide each point by the video's own mean and use these measures:
- **p2**: point 1 (1-2% into the video) divided by the mean. This is the cleanest "did they stay past the first seconds" number.
- **f10**: the mean of the first 10 points divided by the overall mean.
- **dip**: the lowest of points 1-9 divided by the mean. This is how far the curve sinks inside the opening.
- **end5**: the mean of the last 5 points divided by the mean. **last** is the final point divided by the mean.

A point covers about 5 s in an 8-minute video.

---

## 1. One-screen summary: what to do (most important findings)

1. **Openings that start talking or fighting hold best. Openings that start slowly lose viewers.** Opening type and heatmap (n with heatmap): face or funny line at 0 s, p2 **1.73** and f10 **1.73** (9). Cold start in the middle of a fight, p2 1.50 and f10 1.38 (22). Labelled teaser montage, p2 1.25 and f10 1.36 (32). Goal statement, p2 1.26 and f10 1.15 (14). **Slow cold start** (lobby greetings, an official broadcast's map and plane, a context explanation), p2 **0.41** and f10 **0.88** (4 of the 6 have a heatmap). Only 7 of 84 videos have point 0 below their own mean, and every one of the 7 opens on talk, a lobby, a broadcast map, a black-and-white face teaser or a logo intro rather than action.
2. **The first words should be the line the thumbnail and title promise.** Videos whose opening shows the promised moment or line at once ("Y", 57 videos) have point 0 at 2.21x mean and f10 1.42. "Partly" (P, 23 videos) gives 1.58 and 1.23. Inside Joker's two channels the gap is large: f10 1.79 and 1.68 for "Y", against 0.97 and 1.17 for "P". The best hold in the whole sample is [3QRE7nzZvaM](https://www.youtube.com/watch?v=3QRE7nzZvaM) (f10 2.23, dip 1.69x, so the curve never sinks). Its first words are exactly the thumbnail's speech-bubble line ("PLANE MEIN JANA HAI INKO INTERNATIONAL").
3. **Do not give away the payoff a kill or Dinner video is built on. Hold it for the end.** When the promised moment (WWCD, VICTORY, the record number) is not in the opening (N, 13 videos), end5 is **1.84x** mean, against 0.92 for "Y". Viewers jump to the end or stay for it. The most-replayed endings are result screens: WWCD at 5.2x end5 ([67w15TWdikI](https://www.youtube.com/watch?v=67w15TWdikI)), VICTORY at 4.1x ([pnqQb35rwlE](https://www.youtube.com/watch?v=pnqQb35rwlE)), and DEFEAT with a last point of 3.9x ([LbEtDxz8Ink](https://www.youtube.com/watch?v=LbEtDxz8Ink)).
4. **Long cold opens get skipped.** In 18 of 38 videos whose story starts 10 s or more into the video, the heatmap spikes (1.5x or more above the cold-open level) exactly where the match or story begins. That is the signature of viewers seeking past the intro (inference). Extreme cases: a 45 s face talk ([cQRWK4Z0Yu8](https://www.youtube.com/watch?v=cQRWK4Z0Yu8), 14x spike at the duel start), a 35 s broadcast intro ([nkvIKh72uH8](https://www.youtube.com/watch?v=nkvIKh72uH8), 7.5x), and LoLzZz's 30-60 s cold opens (2.6-5x). Joker's 12-18 s "IN THIS VIDEO" teasers show the smallest effect.
5. **Each creator has his own opening, and it matches the content.** Goblin opens cold on a fight in 19 of 31 videos (his 2026 stream cuts start mid-fight with comms: p2 4.8x on [6jIQaYvIOGc](https://www.youtube.com/watch?v=6jIQaYvIOGc) and 4.9x on [khbJdsEChm0](https://www.youtube.com/watch?v=khbJdsEChm0)). Joker uses a labelled teaser in 14 of 30 and a funny line or face in 7. LoLzZz uses a goal statement or teaser (usually after a black first frame) in 26 of 32, and his story starts at a median of **30-38 s**, against **0 s** for Goblin and Joker main and **15 s** for JokerClips.
6. **Teasers are short and come from the body, not the end.** The median teaser is **22 s** (range 8-50; Joker 12-20, Goblin 8-35, LoLzZz 22-50). For 26 teasers I could trace through the captions, the lines come from 13-75% of the video. Only 8 also include a line from the last 10%, and 6 of those 8 are LoLzZz videos.
7. **A comedy video's ending is the weakest spot, and end cards empty it.** Comedy end5 is 0.32x (n=23), against 1.47x for match/esports. Ending type and end5: punchline or reaction **1.36**, result screen 0.98, black or logo 0.90, **end card 0.50 (last point 0.07)**, **abrupt cut 0.27**, "To Be Continued" meme **0.02** ([lyHdl-U4yNQ](https://www.youtube.com/watch?v=lyHdl-U4yNQ)). Joker's main channel adds a 10-25 s black "SUBSCRIBE" card, and almost nobody watches it.
8. **Thumbnails:** 83 of 93 show a face, 70 big text, 41 a number in the text, 24 "VS", 30 emoji, 18 arrows, and 12 a speech bubble (all 12 on Joker's channels). The 8 without design are Goblin's 2026 raw game frames (5 of his 6 newest main uploads). The thumbnail number is always the outcome (kills, points, UC), and the video then withholds that moment until the end.
9. **The opening should name the stake in the first 5 s.** The best custom-room, cash and crate openings state the stake or rules in the first seconds: "total team kill x ₹1000 if chicken" ([3i83F-jSotA](https://www.youtube.com/watch?v=3i83F-jSotA), p2 2.0), "challenge hai per kill 10,000" ([7bmUiiUuAdE](https://www.youtube.com/watch?v=7bmUiiUuAdE), p2 4.1), and "agar aaj kata to crate opening band" ([z1jXPJN8z-c](https://www.youtube.com/watch?v=z1jXPJN8z-c)). In streamer-vs-streamer videos the hook is the opponent's discovery line: "suno suno, hamare match mein LoLs aa gaye shayad" ([l2o5yycZ9HY](https://www.youtube.com/watch?v=l2o5yycZ9HY)).
10. **Black frames are a LoLzZz habit, not a rule.** Frame 0 is black on 20 of 32 LoLzZz videos and 8 of 61 others, and 12 of 32 LoLzZz videos end on 5 s or more of black. Openings with a black first frame do slightly worse (p2 1.25 against 1.37), and a 25 s black tail goes with end5 0.07 ([mZvHwwCDKfg](https://www.youtube.com/watch?v=mZvHwwCDKfg)). Kaatclip should not copy them.

---

## 2. Evidence by question

### Q1. What happens in the first 3, 10, 30-60 s and the last 30 s?

#### Takeaway
There are six opening types, and their use depends on the channel more than on the content. Goblin opens cold on a fight. Joker opens on a funny line or a 12-18 s labelled teaser. LoLzZz opens on black, a facecam goal line, teaser kills and the number, with the story starting at 30-40 s. Endings split into result screens for matches and duels and punchlines or reactions for comedy. Abrupt cuts, end cards and black tails also occur.

#### Cited findings: opening types (hand-labelled from the contact sheets and captions)
Definitions:
- **COLD**: the match or story is already running at 0 s, in order.
- **COLD_SLOW**: in order, but the first 10-35 s are low-energy (lobby greetings, the broadcast's map or plane, context talk).
- **TEASER**: a montage of later moments, usually under an "IN THIS VIDEO" label. **PAYOFF**, a subtype, also includes the ending's result or line.
- **GOAL**: a facecam or player states the target, the stake or the rules, usually with teaser shots.
- **FACE/FUNNY_LINE**: a facecam joke or banter line at 0 s, without a montage.
- **TITLE**: a logo or title card first.

| Channel | COLD | COLD_SLOW | TEASER (of which PAYOFF) | GOAL | FACE/FUNNY | TITLE | Median story start |
|---|---|---|---|---|---|---|---|
| Goblin main (15) | 11 | 0 | 3 | 0 | 0 | 1 | 0 s |
| Goblin second (16) | 8 | 3 | 2 | 2 | 1 | 0 | 1 s |
| JokerClips (15) | 2 | 1 | 7 | 2 | 3 | 0 | 15 s |
| Joker main (15) | 1 | 2 | 7 (1) | 1 | 4 | 0 | 0 s |
| LoLzZz main (16) | 2 | 0 | 6 (2) | 7 | 1 | 0 | 38 s |
| LoLzZz Plays (16) | 1 | 0 | 10 (4) | 3 | 0 | 2 | 30 s |
| **All (93)** | **25** | **6** | **35 (7)** | **15** | **9** | **3** | |

By content type: match/esports (23) has COLD 15, TEASER 5 and COLD_SLOW 3. Custom/TDM/vs (31) has TEASER 16, COLD 6 and GOAL 5. Funny session (24) has TEASER 11 and FACE/FUNNY 7. Crate (9) has GOAL 4, COLD 2, TEASER 2 and TITLE 1. Kill record (6) has GOAL 5 and TEASER 1. Source: `summary.txt`.

What the first seconds look like, second by second, per house style (from the storyboards):
- **Goblin stream cut, 2026.** 0 s: a fight is already on, with the stream overlay and a comms call such as "idhar se gaadi aa raha hai" ([wDgeZBn80VM](https://www.youtube.com/watch?v=wDgeZBn80VM)), "chal chal chal" or "fight ho rahi hai" ([xWvORedYbOs](https://www.youtube.com/watch?v=xWvORedYbOs)). No text, no card. The first knock comes in 5-15 s.
- **Goblin hero edit, 2023.** 0-20 s: teaser fights, with a caster line in [67w15TWdikI](https://www.youtube.com/watch?v=67w15TWdikI) ("stop the monster, 11 finishes already"). Then 1-5 s of black or a "Goblin" logo card. The drop comes at about 30 s ([OOnDKF-Wprs](https://www.youtube.com/watch?v=OOnDKF-Wprs), [MQ8SC-_e8ZQ](https://www.youtube.com/watch?v=MQ8SC-_e8ZQ)).
- **Goblin second channel, tournament videos.** Black, then the official broadcast's standings, plane and flight-path caster talk for 10-35 s ([nkvIKh72uH8](https://www.youtube.com/watch?v=nkvIKh72uH8), [xtE3WWqt1_E](https://www.youtube.com/watch?v=xtE3WWqt1_E), [7uZM0hKn5Yc](https://www.youtube.com/watch?v=7uZM0hKn5Yc)).
- **Joker channels, 2024-26.** 0-12/18 s: a red "IN THIS VIDEO" label (visible in the top-left of the frames) over 3-4 cuts of facecam lines with burned subtitles. Sometimes there is a black frame at about 15 s. The lobby or game follows, with a facecam zoom on every line. Examples: [3QRE7nzZvaM](https://www.youtube.com/watch?v=3QRE7nzZvaM), [tJFuxVbDiOA](https://www.youtube.com/watch?v=tJFuxVbDiOA), [kl9ibgyjlt4](https://www.youtube.com/watch?v=kl9ibgyjlt4), [Ul5mEjNyzu4](https://www.youtube.com/watch?v=Ul5mEjNyzu4). Without a teaser, the opening is a joke: "bhook lagi thi mujhe main paan kha gaya" over a "PAN" meme label ([J9EcR7MvhbM](https://www.youtube.com/watch?v=J9EcR7MvhbM)), or "chalo chalo chicken lena hai, only chicken dinner gameplay" ([G4dIkpIpLOw](https://www.youtube.com/watch?v=G4dIkpIpLOw)).
- **LoLzZz record videos.** 0 s black. 5 s: a facecam (often black and white) states the goal, e.g. "30 40 50 60 70 80 90 kills" and "mera target 70 hai" ([-qpx-ejuq9Q](https://www.youtube.com/watch?v=-qpx-ejuq9Q)). Then 10-20 s of teaser kills, the catchphrase "koi bhi ho, record tere bhai ka rahega" ([Car5bJ_yP-E](https://www.youtube.com/watch?v=Car5bJ_yP-E), [fbVXWfefL8c](https://www.youtube.com/watch?v=fbVXWfefL8c)), the number ("72" at 43 s), and an optional flash of the MVP screen ([Gn1AvcFXl-Y](https://www.youtube.com/watch?v=Gn1AvcFXl-Y) at 35 s). Then black, and the drop at 30-48 s.
- **LoLzZz Plays, vs-streamer videos.** Black, then the opponent's webcam reacting ("aapki lobby mein LoLs aaya hai", [DwvaNRtqy20](https://www.youtube.com/watch?v=DwvaNRtqy20)), teaser fights, and an IRL or skull meme with a joke caption ("abhi kill feed pe naam bhi aayega didi", [l2o5yycZ9HY](https://www.youtube.com/watch?v=l2o5yycZ9HY)). The plane comes at about 30 s.
- **Crates.** Either the stake is stated ("pehli baar car ki crate khol raha hoon, 60000 UC daal di", [bCJbLnqdfOQ](https://www.youtube.com/watch?v=bCJbLnqdfOQ)) or the spin starts at once ([mk_Ne_mk_70](https://www.youtube.com/watch?v=mk_Ne_mk_70), [-5i-6rSEtTg](https://www.youtube.com/watch?v=-5i-6rSEtTg) "are you guys ready... gaadi aane wali hai"). Joker's crate videos put a prank or loss payoff first ("₹1.5 lakh aapke account se gaye?", [TZCVFWl7NtM](https://www.youtube.com/watch?v=TZCVFWl7NtM)).
- **Teaser length** (35 teasers): 8, 8, 12×5, 13×2, 16, 17×2, 18×2, 20, 22×3, 24, 26, 28×4, 30×5, 33, 35×3, 50×2. **Median 22 s.**

#### Cited findings: ending types
| Ending | n | Median end5 | Median last point | Where |
|---|---|---|---|---|
| Result or payoff screen (WWCD, VICTORY/DEFEAT, MVP, results table, final reward), often then black | 35 | 0.98 | 0.66 | Goblin main 7/15, Goblin second 9/16, LoLzZz main 7/16, Plays 8/16 |
| Reaction or punchline (facecam laugh, title callback, a joke text card, sign-off talk) | 27 | **1.36** | 0.64 | all channels; Joker main 6/15 |
| Abrupt cut mid-gameplay | 10 | **0.27** | 0.29 | JokerClips 4, Goblin main 3 |
| End card ("SUBSCRIBE", "THANKS FOR WATCHING", "LIKE SHARE & SUBSCRIBE", subscribe screen) | 10 | 0.50 | **0.07** | Joker main 4, LoLzZz main 3 |
| Black or logo only | 9 | 0.90 | 0.52 | |
| "To Be Continued" meme | 1 | 0.02 | 0.00 | [lyHdl-U4yNQ](https://www.youtube.com/watch?v=lyHdl-U4yNQ) |

By content type: match/esports endings are 10 result, 5 abrupt and 5 black. Custom/vs endings are 14 result and 12 reaction. Funny endings are 9 reaction, 7 end card and 5 abrupt. Crates end on 5 result/payoff. Kill records end on 5 result (MVP or WWCD, then a reaction).

Examples:
- Joker main's end cards run 10-25 s of black with "SUBSCRIBE" ([C9pvcRmEGYE](https://www.youtube.com/watch?v=C9pvcRmEGYE) 25 s, [G4dIkpIpLOw](https://www.youtube.com/watch?v=G4dIkpIpLOw) 24 s, [E6h-WNsY7jM](https://www.youtube.com/watch?v=E6h-WNsY7jM) 10 s).
- LoLzZz main often ends on 5-25 s of black (12 of 32 LoLzZz videos have 5 s or more).
- Goblin's second channel ends funny edits on a meme sting: colour bars after "jita diya tere ko, paise aa jane chahiye" ([Ev6oMQTJVJ8](https://www.youtube.com/watch?v=Ev6oMQTJVJ8)), and a black text card "BHAROSA RAKHO CHICKEN AAGYA" ([-ieo36Gj9Hk](https://www.youtube.com/watch?v=-ieo36Gj9Hk)).
- A "part 2" tease appears only once (the TBC meme). Two titles are "PART 2" ([sT0sYDstN_k](https://www.youtube.com/watch?v=sT0sYDstN_k), [NpLfg9YU7NE](https://www.youtube.com/watch?v=NpLfg9YU7NE)), and the first has its heatmap peak at 10%. I infer that part-1 viewers jump straight to the action.

#### Inferences
- In every channel the opening carries the creator's voice or a fight within 0-5 s. The cold open's length is the main thing that differs.
- End cards and black tails exist for the end screen (subscribe and next-video elements), and viewers treat them as "video over".

#### Gaps
- Storyboard frames are 2-10 s apart, so cuts shorter than the interval are invisible. Teaser lengths are within ±5 s, ±10 s on five long videos.
- I cannot hear music or stings. Music is read only from the "[संगीत]" caption tags.

### Q2. Does the opening show what the title and thumbnail promise, and how fast?

#### Takeaway
Comedy videos show the promised line at once and do best when they do. Kill and Dinner videos promise an outcome (a number, WWCD) and **never open on that outcome**. Their openings show the way there (fights, the goal line) and keep the result for the end, which is the most-replayed part. The number in the title and on the thumbnail always equals the number on the final screen.

#### Cited findings
- Promise in the opening ("shown" flag, hand-labelled): Y = the promised line or moment appears in the opening, 57 videos. P = only a hint or context, 23. N = not at all, 13 (mostly WWCD or record promises kept for the end). The heatmap by flag:

| Flag | n with heatmap | Point 0 / mean | p2 | f10 | end5 |
|---|---|---|---|---|---|
| Y | 51 | 2.21 | 1.35 | 1.42 | 0.92 |
| P | 22 | 1.58 | 1.06 | 1.23 | 0.79 |
| N | 11 | 1.96 | 1.56 | 1.39 | **1.84** |

  Per channel, f10 for Y against P: JokerClips 1.68 vs 1.17 (n=10/4), Joker main 1.79 vs 0.97 (7/6), LoLzZz main 1.04 vs 0.76 (9/6), Plays 1.45 vs 1.41 (13/3). Goblin is the exception (Y 1.49, P 1.89, N 1.76). His "N" videos are WWCD stream cuts that still open on a fight. Source: per-channel breakdown run on `rows.json`.
- **Speech-bubble lines on thumbnails** appear on all 12 Joker-channel thumbnails that have one. In [3QRE7nzZvaM](https://www.youtube.com/watch?v=3QRE7nzZvaM) the bubble line is the first thing said, at 0 s (f10 2.23). In [2aHwYxucN24](https://www.youtube.com/watch?v=2aHwYxucN24) "AAJKAL PAHAD GHUM RHA HAI" comes back as the burned subtitle "Pahad chadh liye" at 39 s (heatmap max at 19%). In [tJFuxVbDiOA](https://www.youtube.com/watch?v=tJFuxVbDiOA) the "HE SENT ₹100,000" promise is the first line, "₹1 lakh ka jaldi kar" (f10 2.59, and the body start is 4-5x mean).
- **Kill-number thumbnails.** Every LoLzZz record thumbnail is "<N> SOLO KILLS WORLD RECORD!!" over a face with a "shh" finger (6 of 6 record videos). The opening shows the goal and teaser kills. The number appears as speech or a card, "72" at 43 s ([-qpx-ejuq9Q](https://www.youtube.com/watch?v=-qpx-ejuq9Q)) and "record tere bhai ka 64" at 34 s ([0inNw0cj1p0](https://www.youtube.com/watch?v=0inNw0cj1p0)). The final kill and MVP come at the end. The caption-traced teaser lines in [fbVXWfefL8c](https://www.youtube.com/watch?v=fbVXWfefL8c) come from 82-99% of the video: the teaser tells you the ending number but not the moment.
- **Goblin's "Solo 14 Kills WWCD" and similar.** Kills open the video (a teaser of fights), and the WWCD banner stays for the end. In [67w15TWdikI](https://www.youtube.com/watch?v=67w15TWdikI) the WWCD comes 15 s before the end, with end5 5.2x and the heatmap max at 96%. In [DwnMgerfI_M](https://www.youtube.com/watch?v=DwnMgerfI_M) (thumbnail "QUALIFIED FOR FINALS") the MVP card comes 10 s before the end, end5 3.0x, max at 94%. In [-ieo36Gj9Hk](https://www.youtube.com/watch?v=-ieo36Gj9Hk) ("SOLO 9 FINISHES WWCD ?") the end card and Dinner give end5 3.5x, max at 98%.
- **Promise-mismatch openings did worst.**
  - "SPIDERMAN IN BGMI": 60 s of facecam talk before the mode is seen, end5 0.19x ([VSK7Q7FH5rk](https://www.youtube.com/watch?v=VSK7Q7FH5rk)).
  - "PAKISTANI PUBG PLAYER FALAK": a context line, then a lobby, with f10 0.42 and point 0 below the mean ([lyHdl-U4yNQ](https://www.youtube.com/watch?v=lyHdl-U4yNQ)).
  - "WHEN MANYA CAME IN JOKER'S LOBBY": 20 s of greetings and earphone talk, f10 0.54 ([Xzzw4S0p3l0](https://www.youtube.com/watch?v=Xzzw4S0p3l0)).
  - "iQOOSouL 42 POINTS": 35 s of the broadcast's map and plane, p2 0.42 ([nkvIKh72uH8](https://www.youtube.com/watch?v=nkvIKh72uH8)).
- **Speed.** In "Y" videos the promised line or moment comes at 0-5 s in Joker's videos and in Goblin's cold starts. In LoLzZz videos the goal is at 0-7 s and the number at 34-45 s. Caption-traced teasers draw their lines mostly from the body: 26 of 35 teasers had a trace, 8 of the 26 include a line from the last 10%, and 6 of those 8 are LoLzZz videos (`summary` run).

#### Inferences
- Comedy promises a line, so say the line first. Kill and Dinner videos promise an outcome, so show the path first and pay off at the end. The outcome is already on the thumbnail, so the suspense is "how", not "whether".
- A payoff spoiler is fine as a number or a spoken goal, but not as the actual final-kill or WWCD footage. No video in the sample opens on its WWCD screen.

#### Gaps
- The Y/P/N labels are my judgement from 2-10 s frames and captions. Sample sizes per channel are small (1-13).

### Q3. Which openings and endings hold viewers best (heatmaps, views, likes per view)?

#### Takeaway
On heatmaps, openings that start talking or fighting win and slow openings lose clearly. Teasers and goal openings sit in the middle and are often skipped when they run past about 25 s. For endings, a punchline or reaction and a result screen hold. End cards, abrupt cuts and "to be continued" lose almost everyone. Views and likes per view follow the channel and topic more than the opening.

#### Cited findings
- **Heatmap by opening type** (median, n with heatmap; source `summary.txt`):

| Opening | n | p2 | f10 | dip | Median views | Likes/1000 views |
|---|---|---|---|---|---|---|
| FACE/FUNNY_LINE | 9 | **1.73** | **1.73** | 0.59 | 532,595 | 55 |
| COLD (fight running) | 22 | 1.50 | 1.38 | 0.44 | 272,715 | 60 |
| TEASER (incl. PAYOFF) | 32 | 1.25 | 1.36 | 0.51 | 421,445 | 47 |
| GOAL | 14 | 1.26 | 1.15 | **0.64** | 363,113 | 56 |
| TITLE/logo | 3 | 1.49 | 1.62 | 1.00 | 407,326 | 84 |
| **COLD_SLOW** | 4 | **0.41** | **0.88** | **0.20** | 178,796 | 41 |

- **Within channels:**
  - JokerClips: TEASER p2 1.69 and f10 1.64 (7), FACE/FUNNY 1.24 and 1.81 (3), against COLD 0.69 and 0.46 (2, both "cold" on context or music) and COLD_SLOW 0.41 and 0.54 (1).
  - Joker main: the GOAL video ([G4dIkpIpLOw](https://www.youtube.com/watch?v=G4dIkpIpLOw)) has p2 3.04 and f10 2.44, the COLD 1v1 ([ybSeAiAlA5A](https://www.youtube.com/watch?v=ybSeAiAlA5A)) 3.68 and 2.20, and FACE/FUNNY 1.73 and 1.54 (4), against TEASER 1.15 and 1.24 (7) and COLD_SLOW 0.94 and 0.88 (2).
  - LoLzZz Plays: GOAL p2 2.04 and dip 0.80 (3), against TEASER 1.07 and 0.52 (10).
  - LoLzZz main: GOAL dip 0.61 (7), against TEASER 0.24 (6).
  - Goblin main: COLD p2 2.18 (11), TEASER 1.76 (3).
  - Goblin second channel: COLD_SLOW p2 0.42 (3), the lowest.
- **The strongest openings** (p2): [Fn9HwxPd89k](https://www.youtube.com/watch?v=Fn9HwxPd89k) 4.75, a donation read plus the boast "mood banate taaki main 20 kill karu". [khbJdsEChm0](https://www.youtube.com/watch?v=khbJdsEChm0) 4.87 and [6jIQaYvIOGc](https://www.youtube.com/watch?v=6jIQaYvIOGc) 4.76, both a fight with comms at 0 s. [7bmUiiUuAdE](https://www.youtube.com/watch?v=7bmUiiUuAdE) 4.05, the rules of a ₹5000-per-kill challenge. [ybSeAiAlA5A](https://www.youtube.com/watch?v=ybSeAiAlA5A) 3.68, a 1v1 from 0 s.
- **The weakest** (p2): [E6h-WNsY7jM](https://www.youtube.com/watch?v=E6h-WNsY7jM) 0.11, a black-and-white facecam teaser. It still has 1.06M views, and its heatmap is dominated by a mid-video peak. [C9pvcRmEGYE](https://www.youtube.com/watch?v=C9pvcRmEGYE) 0.32, a context line about a roast. [Xzzw4S0p3l0](https://www.youtube.com/watch?v=Xzzw4S0p3l0) 0.41, greetings. [nkvIKh72uH8](https://www.youtube.com/watch?v=nkvIKh72uH8) 0.42, the broadcast's plane. [cQRWK4Z0Yu8](https://www.youtube.com/watch?v=cQRWK4Z0Yu8) 0.45, a 45 s face talk. [mZvHwwCDKfg](https://www.youtube.com/watch?v=mZvHwwCDKfg), with f10 0.29, opens on a 2019 logo intro.
- **Skip signature** (`curve` run). For the 38 videos whose story starts 10 s or later, I compared the heat at the story start with the median heat inside the cold open:

| Story starts at | n | Ratio (median) | Videos with a 1.5x+ spike at the story start |
|---|---|---|---|
| 10-20 s | 7 | 1.34 | 3 |
| 21-35 s | 16 | 1.71 | 9 |
| 36-60 s | 15 | 1.26 | 6 |

  Examples: [l2o5yycZ9HY](https://www.youtube.com/watch?v=l2o5yycZ9HY) cold-open heat 0.61, then 3.06 at the drop. [tCWQ4v5tYwo](https://www.youtube.com/watch?v=tCWQ4v5tYwo) 0.82, then 3.09. [fbVXWfefL8c](https://www.youtube.com/watch?v=fbVXWfefL8c) 0.68, then 2.50. [pnqQb35rwlE](https://www.youtube.com/watch?v=pnqQb35rwlE) 1.01, then 3.08.
- **Heatmap by ending** (`summary.txt`):

| Ending | n | end5 | last | Median views |
|---|---|---|---|---|
| REACTION/PUNCHLINE | 24 | 1.36 | 0.64 | 337,393 |
| RESULT/PAYOFF | 30 | 0.98 | 0.66 | 365,097 |
| BLACK/LOGO | 8 | 0.90 | 0.52 | 367,990 |
| ENDCARD | 10 | 0.50 | 0.07 | 554,182 |
| ABRUPT | 10 | 0.27 | 0.29 | 205,789 |

  The median curve of the last 8 points for REACTION is [0.69, 0.70, 1.02, 1.37, 1.57, 1.42, 1.11, 0.64]: it rises into the punchline. For ENDCARD it is [1.05, 1.06, 0.76, 0.67, 0.50, 0.49, 0.24, 0.06]: it drains during the card.
- **By content type, end5:** match/esports 1.47 (17), custom/vs 1.02 (31), kill record 0.92 (5), crate 0.69 (8), funny **0.32** (23). This matches the earlier finding (comedy falls off, esports holds) in `reports/BGMI highlight video structure.md`.
- **Within channels, end5:**
  - JokerClips: REACTION 1.40 (4), against ABRUPT 0.22 (4) and ENDCARD 0.21 (2).
  - Goblin second channel: REACTION/punchline 2.35 (5), against RESULT 0.95 (9).
  - LoLzZz main: RESULT 1.43 (7) and REACTION 1.45 (5), against BLACK 0.07 (1).
  - Goblin main: RESULT 1.47 (7) and REACTION 2.50 (2), against BLACK 0.93 (3).
- **Black first frame:** p2 1.25 (25 videos) against 1.37 (59). Confounded by channel, because it is mostly LoLzZz.

#### Inferences
- The opening affects the curve more than the views. The biggest views (4.06M [pnqQb35rwlE](https://www.youtube.com/watch?v=pnqQb35rwlE), 1.96M [cQRWK4Z0Yu8](https://www.youtube.com/watch?v=cQRWK4Z0Yu8), 1.06M [E6h-WNsY7jM](https://www.youtube.com/watch?v=E6h-WNsY7jM)) come from collab topics (Jonathan, Goldy/Snax) whatever the opening.
- For Kaatclip, the safest opening is the one with the fewest seconds before a voice line or gunfire. A teaser should be about 12-20 s, the length at which the skip signature is weakest. That threshold is my inference from the table above.

#### Gaps
- The heatmap measures replays and seeking, not the share of viewers left, so a peak can mean rewatching rather than staying.
- I have no retention or CTR data. Likes per view are confounded by channel (LoLzZz Plays has 21-58 likes per 1000 views; Goblin main has 30-136).

### Q4. Counts per channel and content type, and which perform best
The counts are in the Q1 tables and the per-video table at the end. Best-performing combinations by heatmap, with n of 3 or more:
- **Comedy:** a teaser that starts on the thumbnail's line (JokerClips f10 1.64), or a funny line or face at 0 s (1.73).
- **Esports:** a cold start mid-fight with comms (Goblin p2 2.18).
- **Challenges with a stake:** a goal line plus teaser kept under 40 s (LoLzZz Plays p2 2.04).
- **Endings:** a punchline (comedy) or a result screen plus reaction (duels and records). Avoid end cards and abrupt cuts.

### Q5. Thumbnails and titles

#### Cited findings (93 thumbnails, looked at one by one)
- **Faces** appear in 83 of 93. Goblin uses back-to-camera jersey shots ("GOBLIN" on the back, pointing at it) in [OOnDKF-Wprs](https://www.youtube.com/watch?v=OOnDKF-Wprs) and [DwnMgerfI_M](https://www.youtube.com/watch?v=DwnMgerfI_M). LoLzZz always uses a "shh" finger pose on record and Plays thumbnails. Joker uses shocked, screaming or laughing faces in all 30.
- **Big text** appears in 70. A **number in the text** appears in 41: LoLzZz main 14 of 16, Plays 10 of 16, Goblin 9 of 31, Joker 8 of 30. **VS** appears in 24, all in custom/vs or duel videos. Emoji appear in 30 (19 of them Joker). **Arrows** appear in 18 (a red curved arrow from a face to the gameplay or the opponent). **Speech bubbles** appear in 12, all on Joker's channels, quoting a Hinglish line. Money or stake symbols (₹, UC, cash) appear in 9.
- **No design.** 8 thumbnails are raw gameplay or broadcast frames: Goblin main's 2026 uploads (a car with a skin, 5 of the 6 newest) and two BMSD broadcast frames. They still drew 134K-272K views, which works for an established name, as `reports/BGMI highlight video structure.md` already noted.
- **Which moment the thumbnail shows:**
  - Records and challenges: the outcome number plus the face.
  - Duels: both faces with the scoreline, e.g. "39-39" ([C76kBoyodHY](https://www.youtube.com/watch?v=C76kBoyodHY), [Ev6oMQTJVJ8](https://www.youtube.com/watch?v=Ev6oMQTJVJ8)) or "8-21 THE REMATCH" ([cQRWK4Z0Yu8](https://www.youtube.com/watch?v=cQRWK4Z0Yu8)).
  - Comedy: the faces and the quoted line.
  - Crates: the prize item, the UC spent and the face.
  - Tournaments: the official MVP card ([xtE3WWqt1_E](https://www.youtube.com/watch?v=xtE3WWqt1_E), [DLYH7QGTmTk](https://www.youtube.com/watch?v=DLYH7QGTmTk)) or the team at the LAN booth.
- **Titles repeat the thumbnail.** LoLzZz: "I MADE A NEW WORLD RECORD OF 72 SOLO KILLS IN BGMI | CLASSIC HACKER OR WHAT", with "72 SOLO KILLS NEW WORLD RECORD" on the thumbnail. Goblin: "Solo 14 Finishes | 29 Team Finishes domination", with "Solo 14 Finishes / 29 Team Finishes" on the thumbnail. Joker: the title names the people and the situation ("Joker Rega Shocked When He Sent ₹100,000 For This"), and the thumbnail carries the money line ("HE SENT ₹100,000 FOR THIS").

#### Inferences
- The thumbnail says what happened (number, people, line). The opening proves it is about to happen (goal, stake, first line). The ending delivers it.

---

## 3. Rules for an automatic editor

M = measured in this study. D = my design choice, consistent with the data, to be tuned on the owner's streams.

### Rules for every highlight
1. **Second 0 is never silent.** Frame 0 is a voice line or gunfire, not black, a logo, a lobby or a plane (M: COLD_SLOW p2 0.41 against 1.25-1.73 for every other type; 7 of 7 videos with point 0 below the mean open slowly or on an intro). If a black frame is needed for style, keep it at 0.3 s or less (D; M: black-first openings p2 1.25 against 1.37).
2. **Story starts by 20 s; cold open 12-20 s by default, never over 30 s.** The match or story itself starts by 20 s. Cap the cold open at 12-20 s by default and 30 s at most (M: skip spikes in 9 of 16 videos whose story starts at 21-35 s; LoLzZz's 30-60 s cold opens show 2.6-5x spikes at the drop; Joker's 12-18 s teasers hold best, with JokerClips teaser f10 1.64).
3. **Teaser contents:** 3-4 cuts of 3-5 s each, taken from the body's best moments (lines or fights from 15-75% of the video). Do **not** use the final kill, the WWCD or the VICTORY footage (M: 26 traced teasers come mostly from 13-75%; no video opens on its WWCD; "N" videos keep end5 1.84). The ending can be teased as a number or a spoken goal (M: LoLzZz's "72" at 43 s).
4. **Optional label:** "IN THIS VIDEO" (or a Hinglish equivalent) in the top-left for the teaser's length, followed by a 0.3-1 s cut to black or a hard cut into the story (M: Joker channels, Goblin's 2023 hero edits).
5. **Promise match:** the first spoken line of the video (teaser or story) is the line, stake or goal that the title and thumbnail use. The thumbnail number is the number shown on the final screen (M: Y videos f10 1.42 against 1.23 for P; Joker 1.68-1.79 against 0.97-1.17; every LoLzZz record number equals the final MVP count).
6. **End on the payoff and then stop.** Cut 3-10 s after the result screen or punchline, while the facecam reaction is still going. No end card over 5 s, no black tail over 2 s, and no "to be continued" (M: ENDCARD last point 0.07; ABRUPT end5 0.27; TBC 0.02; REACTION end5 1.36; a 25 s black tail gives end5 0.07). YouTube end-screen elements can sit over the final reaction (D).
7. **Never cut out of the game mid-action at the end** (M: abrupt endings end5 0.27). If the last segment is gameplay, end on the elimination or the result banner (D).

### By highlight type
| Type | First 3 s | First 10 s | First 30 s | Ending | Title and thumbnail |
|---|---|---|---|---|---|
| **Kill match** (high kills, no Dinner) | A gunfight already running with the streamer's call or a knock line ("chal chal", "ek knock") (M: Goblin cold starts p2 2.18, 4.8x on 6jIQ and khb) | Either the fight continues with the first knock or finish on screen by 5-10 s, or a 12-15 s teaser of 3 fights (M: Goblin hero teasers 8-22 s) | Story under way: the match in order from the first real fight. No plane, map or looting (M: broadcast plane openings p2 0.42) | The last fight, then the results or MVP screen with the kill count, then 3-8 s of reaction (M: MVP endings end5 1.4-3.0) | "<N> FINISHES" or "SOLO <N> KILLS" in big text plus the face and a frame of the best fight. The number equals the final count |
| **Chicken Dinner** | A fight with comms, never the WWCD (M: WWCD held to the end in all Dinner videos; WWCD end5 up to 5.2x) | As above. Optional spoken stake ("chicken lena hai, only chicken dinner gameplay": [G4dIkpIpLOw](https://www.youtube.com/watch?v=G4dIkpIpLOw) p2 3.0) | Story under way. A players-left count is a good stake card (D) | The final circle kept whole, the WWCD banner held 2-4 s, then the reaction or team cheer for 3-10 s. No end card | "WWCD" or "CHICKEN DINNER" plus the kill number plus the face. The teaser must not show the Dinner |
| **Funny session** | The funniest line, or the thumbnail's speech-bubble line, spoken in full with a burned subtitle (M: [3QRE7nzZvaM](https://www.youtube.com/watch?v=3QRE7nzZvaM) f10 2.23; FACE/FUNNY f10 1.73) | "IN THIS VIDEO" teaser of 3-4 lines, 12-18 s, ending on a laugh (M: Joker teasers 12-20 s) | Story starts by 15-20 s on the first bit. Cut greetings, earphone checks and lobby setup (M: [Xzzw4S0p3l0](https://www.youtube.com/watch?v=Xzzw4S0p3l0) f10 0.54; [rpbg7zhuZXE](https://www.youtube.com/watch?v=rpbg7zhuZXE) 0.98) | The last punchline, or a callback to the title or teaser line ([J9EcR7MvhbM](https://www.youtube.com/watch?v=J9EcR7MvhbM) "moye moye" end5 1.58; [kl9ibgyjlt4](https://www.youtube.com/watch?v=kl9ibgyjlt4) teaser line pays off at 95%), the laugh, cut within 3 s. No 10-25 s subscribe card | Faces (2-4, shocked or laughing), a speech bubble quoting the opening line, a people-plus-conflict title |
| **Custom room / TDM / vs streamer** | The stake or the challenge line ("aisa marenge saans nahi aayega": [vIfKetkuVbE](https://www.youtube.com/watch?v=vIfKetkuVbE) point 0 3.4x), or the opponent noticing ("hamare match mein LoLs aa gaye") | Rules in one sentence if cash or a bet is involved (M: [3i83F-jSotA](https://www.youtube.com/watch?v=3i83F-jSotA) p2 2.0, [7bmUiiUuAdE](https://www.youtube.com/watch?v=7bmUiiUuAdE) 4.1), then gunfire | First duel or round by 30 s. Not 45 s of talk (M: [cQRWK4Z0Yu8](https://www.youtube.com/watch?v=cQRWK4Z0Yu8) 14x skip spike) | The VICTORY or DEFEAT screen and score, then 3-10 s of reaction (M: last point 3.2x [xiqm0RdJR3o](https://www.youtube.com/watch?v=xiqm0RdJR3o), 3.9x [LbEtDxz8Ink](https://www.youtube.com/watch?v=LbEtDxz8Ink), end5 4.1x [pnqQb35rwlE](https://www.youtube.com/watch?v=pnqQb35rwlE)). Show defeats too | Both faces plus VS plus names, a scoreline if close, "1V1" or "2V2" big |
| **Crate opening** | The stake: UC spent or the target item ("60000 UC daal di", "agar aaj kata to band"), or the loss or prank payoff line | The first pull by 10 s (M: crate f10 0.94, the lowest type, so do not wait) | Pulls with reactions, the best pull teased once (D) | The final or best reward screen ("YOU GOT"), then the reaction or a total-loss line ([72gO2p-DjEg](https://www.youtube.com/watch?v=72gO2p-DjEg) "75000 lag gaye... khushi bhi nahi" end5 1.4), or a 10-20 s clip of the item in a match ([z1jXPJN8z-c](https://www.youtube.com/watch?v=z1jXPJN8z-c), [Uk7i_OEWB0c](https://www.youtube.com/watch?v=Uk7i_OEWB0c)) | The item screen plus the face (shocked, praying or crying) plus "<UC> UC" and the item name |
| **Kill record / goal** (LoLzZz-style) | The goal line in his own voice ("aaj target 70") (M: 7 of 7 LoLzZz main GOAL openings) | 2-3 teaser kills, 3-5 s each | The number or catchphrase by 20-25 s, then the drop. Story starts by 30 s at most (M: LoLzZz drop at 30-48 s with skip spikes; D: shorten) | The record kill, then MVP with the number, then 5-20 s of celebration. Black tail 2 s at most | "<N> SOLO KILLS" plus "RECORD", face. The number equals the MVP count |

### Measurable checks Kaatclip can run on its own output (D)
- `t_first_voice_or_shot ≤ 1.0 s`
- `story_start ≤ 20 s`
- `teaser_len` between 10 and 20 s (30 at most)
- `teaser_contains_final_result == false` for kill and Dinner videos
- `first_line ∈ {thumbnail line, title stake}`
- `tail_after_payoff` between 3 and 10 s
- `end_card_len ≤ 5 s`
- `black_tail ≤ 2 s`
- `thumbnail_number == final_screen_number`

---

## 4. What I could not measure
- **Sound.** I cannot hear the audio. Music, stings and laughter are known only from the caption tags ([संगीत], [हंसी], [प्रशंसा]) and from what is said.
- **Frame timing.** Storyboard frames are 2-10 s apart, so cut points, label durations and teaser lengths are accurate only to ±1 frame interval. Five long videos use 10 s frames ([7TkLt-j3u4A](https://www.youtube.com/watch?v=7TkLt-j3u4A), [PtvEiSN48Dk](https://www.youtube.com/watch?v=PtvEiSN48Dk), [fCCQkW1Uevk](https://www.youtube.com/watch?v=fCCQkW1Uevk), [0inNw0cj1p0](https://www.youtube.com/watch?v=0inNw0cj1p0), [kOccoMYydwI](https://www.youtube.com/watch?v=kOccoMYydwI)).
- **Heatmap limits.** The heatmap is relative and includes replays and seeking. It is not audience retention, and no CTR or impression data is available. 9 recent videos have no heatmap. Each heatmap point is 1% of the video (about 5 s), so the "first 3 s" cannot be resolved separately from the first 5-6 s.
- **Visual teaser matching.** Matching storyboard frames to find where teaser shots come from was unreliable (game scenes look alike at 5 s spacing), so teaser sources come only from caption-line matches. Those miss music-only teasers, and caster phrases can give false matches on tournament broadcasts. I ignored the matches on DLYH7QGTmTk and mjUFpXmaQH4.
- **Confounding.** Opening style is confounded with channel and era (2019-2023 logo intros and music beds against 2025-26 stream cuts). Group sizes are 3-35, and nothing is tested for significance.
- **Labels are mine.** The opening, ending and promise labels are hand judgements. A second rater would likely disagree on some MONTAGE/GOAL/PAYOFF borders.

---

## Appendix: all 93 videos
p2, f10 and end5 are relative to each video's own mean (see the top of the file). Opening and Ending are the hand labels. "Promise in opening" is Y, P or N as in Q2. Full notes per video, including the thumbnail description and the exact lines, are in `scratchpad\viewers\openings\labels.jsonl`.

| Video | Channel | Type | Views | Likes/1000 | Opening | Teaser s | Story starts s | Promise in opening | Ending | p2 | f10 | end5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [67w15TWdikI](https://www.youtube.com/watch?v=67w15TWdikI) | goblin_main | match/esports | 605,393 | 78 | MONTAGE | 8 | 12 | P | RESULT>BLACK | 1.76 | 1.89 | 5.24 |
| [aA98jrFkEPQ](https://www.youtube.com/watch?v=aA98jrFkEPQ) | goblin_main | match/esports | 540,712 | 63 | COLD | 0 | 0 | N | RESULT? | 2.02 | 1.33 | 1.47 |
| [lnAJghtGfow](https://www.youtube.com/watch?v=lnAJghtGfow) | goblin_main | match/esports | 496,296 | 94 | COLD | 0 | 0 | Y | ABRUPT | 2.67 | 2.09 | 1.72 |
| [OOnDKF-Wprs](https://www.youtube.com/watch?v=OOnDKF-Wprs) | goblin_main | match/esports | 459,685 | 93 | MONTAGE | 22 | 30 | P | RESULT>BLACK | 1.68 | 0.92 | 1.81 |
| [qy_BVesBY_M](https://www.youtube.com/watch?v=qy_BVesBY_M) | goblin_main | custom/vs | 440,271 | 70 | COLD | 0 | 0 | Y | RESULT | 2.16 | 1.2 | 0.55 |
| [DwnMgerfI_M](https://www.youtube.com/watch?v=DwnMgerfI_M) | goblin_main | match/esports | 410,863 | 78 | COLD | 0 | 0 | N | RESULT(MVP) | 0.94 | 1.84 | 3.04 |
| [HQOWD0OmdWU](https://www.youtube.com/watch?v=HQOWD0OmdWU) | goblin_main | funny | 407,326 | 136 | TITLE | 0 | 4 | Y | REACT | 1.33 | 1.62 | 1.39 |
| [C76kBoyodHY](https://www.youtube.com/watch?v=C76kBoyodHY) | goblin_main | custom/vs | 383,035 | 51 | COLD | 0 | 0 | Y | RESULT(spoken)>BLACK | 0.81 | 0.65 | 0.74 |
| [MQ8SC-_e8ZQ](https://www.youtube.com/watch?v=MQ8SC-_e8ZQ) | goblin_main | custom/vs | 382,102 | 47 | MONTAGE | 22 | 30 | P | BLACK | 2.14 | 1.94 | 0.93 |
| [6jIQaYvIOGc](https://www.youtube.com/watch?v=6jIQaYvIOGc) | goblin_main | match/esports | 272,715 | 30 | COLD | 0 | 0 | N | STICKER | 4.76 | 2.91 | 3.62 |
| [PiGMtVEVJKw](https://www.youtube.com/watch?v=PiGMtVEVJKw) | goblin_main | match/esports | 159,338 | 57 | COLD | 0 | 0 | Y | ABRUPT>BLACK | 2.58 | 1.49 | 0.28 |
| [xWvORedYbOs](https://www.youtube.com/watch?v=xWvORedYbOs) | goblin_main | match/esports | 142,899 | 60 | COLD | 0 | 0 | N | ABRUPT | 2.18 | 1.47 | 2.69 |
| [nk3MGVXKCFo](https://www.youtube.com/watch?v=nk3MGVXKCFo) | goblin_main | match/esports | 215,529 | 61 | COLD | 0 | 0 | Y | BLACK | 2.94 | 1.36 | 1.55 |
| [khbJdsEChm0](https://www.youtube.com/watch?v=khbJdsEChm0) | goblin_main | match/esports | 171,543 | 66 | COLD | 0 | 0 | Y | BLACK | 4.87 | 2.03 | 0.86 |
| [ml5FitUoqf8](https://www.youtube.com/watch?v=ml5FitUoqf8) | goblin_main | match/esports | 134,040 | 73 | COLD | 0 | 5 | N | RESULT | 1.63 | 1.76 | 1.01 |
| [6f0CK3fBrig](https://www.youtube.com/watch?v=6f0CK3fBrig) | goblin_shorts | match/esports | 469,875 | 56 | COLD | 0 | 0 | Y | ABRUPT | 0.75 | 1.93 | 0.26 |
| [7TkLt-j3u4A](https://www.youtube.com/watch?v=7TkLt-j3u4A) | goblin_shorts | custom/vs | 272,159 | 38 | COLD | 0 | 0 | Y | TALK_OUTRO | 1.07 | 0.81 | 1.01 |
| [xiqm0RdJR3o](https://www.youtube.com/watch?v=xiqm0RdJR3o) | goblin_shorts | custom/vs | 269,739 | 55 | COLD | 0 | 0 | Y | RESULT(VICTORY)>BLACK | 1.07 | 0.59 | 1.94 |
| [nkvIKh72uH8](https://www.youtube.com/watch?v=nkvIKh72uH8) | goblin_shorts | match/esports | 265,915 | 34 | COLD_SLOW | 0 | 39 | N | CELEBRATION(camera)>BLACK | 0.42 | 1.03 | 0.44 |
| [yincpYxqIrI](https://www.youtube.com/watch?v=yincpYxqIrI) | goblin_shorts | custom/vs | 246,375 | 39 | MONTAGE | 35 | 40 | Y | RESULT(table,MVP)>BLACK | 2.04 | 1.44 | 2.17 |
| [4QjX1jHoIvA](https://www.youtube.com/watch?v=4QjX1jHoIvA) | goblin_shorts | custom/vs | 232,846 | 43 | FACE | 0 | 9 | Y | RESULT(VICTORY)>TALK_OUTRO | 2.89 | 1.28 | 0.95 |
| [Ev6oMQTJVJ8](https://www.youtube.com/watch?v=Ev6oMQTJVJ8) | goblin_shorts | custom/vs | 224,949 | 53 | FACE_GOAL | 0 | 32 | P | PUNCHLINE>MEME(colour bars) | 1.14 | 1.51 | 1.34 |
| [-ieo36Gj9Hk](https://www.youtube.com/watch?v=-ieo36Gj9Hk) | goblin_shorts | match/esports | 224,571 | 70 | COLD | 0 | 0 | N | TEXT_CARD>MEME | 1.25 | 1.39 | 3.48 |
| [wDgeZBn80VM](https://www.youtube.com/watch?v=wDgeZBn80VM) | goblin_shorts | match/esports | 283,836 | 20 | COLD | 0 | 0 | Y | RESULT(#2)>BLACK | - | - | - |
| [mjUFpXmaQH4](https://www.youtube.com/watch?v=mjUFpXmaQH4) | goblin_shorts | match/esports | 22,443 | 28 | COLD | 0 | 0 | Y | LOGO>TEAM(camera)>BLACK | - | - | - |
| [xtE3WWqt1_E](https://www.youtube.com/watch?v=xtE3WWqt1_E) | goblin_shorts | match/esports | 38,960 | 23 | COLD_SLOW | 0 | 12 | N | CELEBRATION(camera,WINNER banner)>LOGO | - | - | - |
| [7uZM0hKn5Yc](https://www.youtube.com/watch?v=7uZM0hKn5Yc) | goblin_shorts | match/esports | 30,002 | 35 | COLD_SLOW | 0 | 10 | N | CELEBRATION(camera,DINNER banner)>LOGO | - | - | - |
| [j6kf-4MXXDc](https://www.youtube.com/watch?v=j6kf-4MXXDc) | goblin_shorts | funny | 57,730 | 29 | MONTAGE | 24 | 33 | Y | REACT/TALK | - | - | - |
| [DLYH7QGTmTk](https://www.youtube.com/watch?v=DLYH7QGTmTk) | goblin_shorts | match/esports | 15,915 | 67 | COLD | 0 | 0 | Y | TEAM(camera)>BLACK | - | - | - |
| [mk_Ne_mk_70](https://www.youtube.com/watch?v=mk_Ne_mk_70) | goblin_shorts | crate | 180,447 | 83 | COLD | 0 | 0 | Y | PAYOFF(upgraded gun)>REACT>BLACK | 0.82 | 0.54 | 0.71 |
| [-5i-6rSEtTg](https://www.youtube.com/watch?v=-5i-6rSEtTg) | goblin_shorts | crate | 60,255 | 105 | GOAL | 0 | 2 | Y | REACT>MEME | 1.29 | 0.64 | 3.37 |
| [lyHdl-U4yNQ](https://www.youtube.com/watch?v=lyHdl-U4yNQ) | jokerclips | funny | 934,741 | 33 | COLD | 0 | 0 | P | TBC_CARD | 0.56 | 0.42 | 0.02 |
| [J9EcR7MvhbM](https://www.youtube.com/watch?v=J9EcR7MvhbM) | jokerclips | funny | 763,038 | 53 | FUNNY_LINE | 0 | 0 | Y | CALLBACK | 1.91 | 1.84 | 1.58 |
| [U21BOYlKr2g](https://www.youtube.com/watch?v=U21BOYlKr2g) | jokerclips | funny | 675,920 | 55 | FACE_FUNNY | 0 | 20 | P | ENDCARD(THANKS FOR WATCHING) | 0.85 | 1.47 | 0.32 |
| [W9C_0b5q--M](https://www.youtube.com/watch?v=W9C_0b5q--M) | jokerclips | funny | 663,398 | 62 | MONTAGE | 13 | 20 | P | REACT>MEME | 0.89 | 0.87 | 1.3 |
| [J2OrUc4QizY](https://www.youtube.com/watch?v=J2OrUc4QizY) | jokerclips | funny | 628,090 | 63 | MONTAGE | 18 | 25 | Y | ABRUPT>BLACK | 0.64 | 0.86 | 0.23 |
| [vIfKetkuVbE](https://www.youtube.com/watch?v=vIfKetkuVbE) | jokerclips | custom/vs | 612,855 | 51 | GOAL | 0 | 30 | Y | MEME | 1.35 | 1.61 | 0.63 |
| [EjaP5wHkv8w](https://www.youtube.com/watch?v=EjaP5wHkv8w) | jokerclips | custom/vs | 602,896 | 59 | COLD | 0 | 0 | Y | RESULT+TALK | 0.81 | 0.5 | 0.76 |
| [3ZtzS5VrEOg](https://www.youtube.com/watch?v=3ZtzS5VrEOg) | jokerclips | funny | 532,595 | 63 | FUNNY_LINE | 0 | 0 | Y | ENDCARD(LIKE SHARE SUBSCRIBE) | 1.24 | 1.81 | 0.11 |
| [ixzk66I3_g4](https://www.youtube.com/watch?v=ixzk66I3_g4) | jokerclips | funny | 107,023 | 53 | MONTAGE | 26 | 29 | Y | PAYOFF(car crate)+SCREAM | 2.0 | 1.74 | 0.68 |
| [72gO2p-DjEg](https://www.youtube.com/watch?v=72gO2p-DjEg) | jokerclips | crate | 98,141 | 63 | MONTAGE | 8 | 10 | Y | RESULT(YOU GOT)+PUNCHLINE | 1.93 | 1.45 | 1.36 |
| [Xzzw4S0p3l0](https://www.youtube.com/watch?v=Xzzw4S0p3l0) | jokerclips | funny | 91,677 | 59 | COLD_SLOW | 0 | 0 | N | ABRUPT(scream) | 0.41 | 0.54 | 3.24 |
| [2aHwYxucN24](https://www.youtube.com/watch?v=2aHwYxucN24) | jokerclips | funny | 214,934 | 71 | MONTAGE | 12 | 15 | P | ABRUPT | 1.76 | 1.64 | 0.14 |
| [3QRE7nzZvaM](https://www.youtube.com/watch?v=3QRE7nzZvaM) | jokerclips | funny | 116,336 | 71 | MONTAGE | 12 | 18 | Y | REACT | 1.69 | 2.23 | 1.49 |
| [tJFuxVbDiOA](https://www.youtube.com/watch?v=tJFuxVbDiOA) | jokerclips | funny | 134,545 | 68 | MONTAGE | 12 | 15 | Y | ABRUPT | 0.95 | 2.59 | 0.21 |
| [bCJbLnqdfOQ](https://www.youtube.com/watch?v=bCJbLnqdfOQ) | jokerclips | crate | 221,718 | 76 | GOAL | 0 | 5 | Y | BLACK/LOGO | 1.3 | 0.87 | 0.16 |
| [E6h-WNsY7jM](https://www.youtube.com/watch?v=E6h-WNsY7jM) | joker_main | funny | 1,064,139 | 46 | MONTAGE | 17 | 20 | P | ENDCARD(SUBSCRIBE 10s) | 0.11 | 0.28 | 0.29 |
| [rpbg7zhuZXE](https://www.youtube.com/watch?v=rpbg7zhuZXE) | joker_main | custom/vs | 722,497 | 51 | COLD_SLOW | 0 | 0 | N | RESULT+TALK | 1.56 | 0.98 | 0.27 |
| [Fn9HwxPd89k](https://www.youtube.com/watch?v=Fn9HwxPd89k) | joker_main | funny | 729,005 | 51 | FACE_FUNNY | 0 | 0 | P | TALK | 4.75 | 2.67 | 2.18 |
| [C9pvcRmEGYE](https://www.youtube.com/watch?v=C9pvcRmEGYE) | joker_main | funny | 575,769 | 47 | COLD_SLOW | 0 | 0 | P | ENDCARD(SUBSCRIBE 25s) | 0.32 | 0.78 | 0.06 |
| [SyOwtmHTAfQ](https://www.youtube.com/watch?v=SyOwtmHTAfQ) | joker_main | funny | 497,262 | 65 | FACE_FUNNY | 0 | 0 | Y | PUNCHLINE>FADE | 1.74 | 1.73 | 0.25 |
| [n7Gxs12rUo4](https://www.youtube.com/watch?v=n7Gxs12rUo4) | joker_main | match/esports | 382,599 | 103 | MONTAGE | 28 | 40 | P | ABRUPT | 1.14 | 0.71 | 0.35 |
| [ybSeAiAlA5A](https://www.youtube.com/watch?v=ybSeAiAlA5A) | joker_main | match/esports | 367,990 | 70 | COLD | 0 | 0 | Y | TRANSITION>BLACK | 3.68 | 2.2 | 0.8 |
| [G4dIkpIpLOw](https://www.youtube.com/watch?v=G4dIkpIpLOw) | joker_main | funny | 363,113 | 62 | GOAL | 0 | 0 | Y | ENDCARD(SUBSCRIBE 24s) | 3.04 | 2.44 | 1.5 |
| [kl9ibgyjlt4](https://www.youtube.com/watch?v=kl9ibgyjlt4) | joker_main | funny | 352,324 | 68 | PAYOFF | 17 | 20 | Y | PUNCHLINE(callback)>ENDCARD(SUBSCRIBE 10s) | 1.85 | 1.84 | 0.7 |
| [TZCVFWl7NtM](https://www.youtube.com/watch?v=TZCVFWl7NtM) | joker_main | crate | 147,194 | 29 | MONTAGE | 16 | 20 | Y | REACT(green-screen dance) | - | - | - |
| [3c0nLXL8k6U](https://www.youtube.com/watch?v=3c0nLXL8k6U) | joker_main | funny | 213,754 | 33 | MONTAGE | 12 | 15 | P | IRL_CLIP | 1.37 | 1.17 | 0.19 |
| [Ul5mEjNyzu4](https://www.youtube.com/watch?v=Ul5mEjNyzu4) | joker_main | funny | 201,446 | 38 | MONTAGE | 12 | 15 | Y | PUNCHLINE(laugh) | 0.99 | 1.4 | 1.86 |
| [TIDXJ1YeirM](https://www.youtube.com/watch?v=TIDXJ1YeirM) | joker_main | funny | 170,498 | 34 | FUNNY_LINE | 0 | 0 | Y | TALK | 1.08 | 0.88 | 0.32 |
| [8Au8-kSBhgg](https://www.youtube.com/watch?v=8Au8-kSBhgg) | joker_main | custom/vs | 337,393 | 26 | MONTAGE | 20 | 25 | P | REACT | 1.17 | 1.31 | 0.21 |
| [VSK7Q7FH5rk](https://www.youtube.com/watch?v=VSK7Q7FH5rk) | joker_main | funny | 196,643 | 56 | FACE | 0 | 0 | N | ABRUPT | 1.73 | 1.36 | 0.19 |
| [pnqQb35rwlE](https://www.youtube.com/watch?v=pnqQb35rwlE) | lolzzz_main | custom/vs | 4,064,347 | 33 | PAYOFF | 35 | 38 | Y | RESULT(VICTORY)+REACT | 1.64 | 1.74 | 4.06 |
| [cQRWK4Z0Yu8](https://www.youtube.com/watch?v=cQRWK4Z0Yu8) | lolzzz_main | custom/vs | 1,961,674 | 74 | FACE | 0 | 46 | N | MEME/REACT | 0.45 | 1.77 | 1.84 |
| [PtvEiSN48Dk](https://www.youtube.com/watch?v=PtvEiSN48Dk) | lolzzz_main | custom/vs | 1,573,733 | 37 | MONTAGE | 50 | 55 | P | TALK_OUTRO>BLACK | 1.07 | 1.55 | 0.34 |
| [LbEtDxz8Ink](https://www.youtube.com/watch?v=LbEtDxz8Ink) | lolzzz_main | custom/vs | 1,396,601 | 41 | COLD | 0 | 8 | Y | RESULT(DEFEAT)>STING>BLACK | 1.01 | 0.94 | 3.25 |
| [-qpx-ejuq9Q](https://www.youtube.com/watch?v=-qpx-ejuq9Q) | lolzzz_main | kill/record | 1,001,377 | 30 | GOAL | 45 | 48 | Y | RESULT(WWCD,MVP)+REACT>BLACK | - | - | - |
| [ed7TlkIqqQw](https://www.youtube.com/watch?v=ed7TlkIqqQw) | lolzzz_main | custom/vs | 912,756 | 73 | MONTAGE | 13 | 25 | P | ENDCARD(subscribe screen) | 1.58 | 0.95 | 1.31 |
| [mZvHwwCDKfg](https://www.youtube.com/watch?v=mZvHwwCDKfg) | lolzzz_main | match/esports | 875,190 | 56 | MONTAGE | 18 | 28 | P | BLACK(25s) | 0.5 | 0.29 | 0.07 |
| [zg6k4Xy_FUg](https://www.youtube.com/watch?v=zg6k4Xy_FUg) | lolzzz_main | custom/vs | 855,311 | 74 | MONTAGE | 28 | 40 | P | PAYOFF(money talk)>ENDCARD | 0.66 | 0.56 | 0.68 |
| [Car5bJ_yP-E](https://www.youtube.com/watch?v=Car5bJ_yP-E) | lolzzz_main | kill/record | 596,431 | 29 | GOAL | 25 | 30 | Y | REACT>BLACK | 0.95 | 1.06 | 1.45 |
| [fbVXWfefL8c](https://www.youtube.com/watch?v=fbVXWfefL8c) | lolzzz_main | kill/record | 360,748 | 29 | GOAL | 30 | 35 | Y | RESULT(MVP)>REACT | 0.68 | 1.17 | 0.91 |
| [fCCQkW1Uevk](https://www.youtube.com/watch?v=fCCQkW1Uevk) | lolzzz_main | custom/vs | 442,976 | 54 | PAYOFF | 35 | 40 | P | TALK>BLACK | 0.5 | 1.33 | 1.49 |
| [0inNw0cj1p0](https://www.youtube.com/watch?v=0inNw0cj1p0) | lolzzz_main | kill/record | 484,487 | 72 | GOAL | 35 | 39 | Y | RESULT(MVP)>BLACK | 1.25 | 1.31 | 1.93 |
| [Gn1AvcFXl-Y](https://www.youtube.com/watch?v=Gn1AvcFXl-Y) | lolzzz_main | kill/record | 751,957 | 60 | GOAL | 38 | 40 | Y | RESULT(MVP)>BLACK(10s) | 0.91 | 1.03 | 0.92 |
| [T4D5femzSco](https://www.youtube.com/watch?v=T4D5femzSco) | lolzzz_main | custom/vs | 255,186 | 72 | GOAL | 0 | 38 | P | PUNCHLINE(song) | 0.89 | 0.56 | 0.9 |
| [z1jXPJN8z-c](https://www.youtube.com/watch?v=z1jXPJN8z-c) | lolzzz_main | crate | 686,062 | 58 | GOAL | 28 | 29 | Y | PAYOFF(match in new skin) | 1.22 | 0.88 | 0.67 |
| [s5yEyRg705o](https://www.youtube.com/watch?v=s5yEyRg705o) | lolzzz_main | crate | 288,248 | 98 | COLD | 0 | 0 | Y | ENDCARD(thank you) | 1.38 | 0.99 | 1.17 |
| [tCWQ4v5tYwo](https://www.youtube.com/watch?v=tCWQ4v5tYwo) | lolzzz_plays | custom/vs | 884,453 | 30 | MONTAGE | 28 | 30 | P | STING>BLACK(10s) | 0.83 | 1.51 | 1.79 |
| [sT0sYDstN_k](https://www.youtube.com/watch?v=sT0sYDstN_k) | lolzzz_plays | custom/vs | 746,372 | 21 | TITLE | 0 | 13 | Y | LOGO(editor)>REACT>BLACK | 2.25 | 1.74 | 1.85 |
| [l2o5yycZ9HY](https://www.youtube.com/watch?v=l2o5yycZ9HY) | lolzzz_plays | custom/vs | 639,197 | 39 | PAYOFF | 30 | 30 | Y | RESULT(WWCD spoken)>BLACK | 0.72 | 1.31 | 0.94 |
| [kOccoMYydwI](https://www.youtube.com/watch?v=kOccoMYydwI) | lolzzz_plays | custom/vs | 585,520 | 42 | PAYOFF | 50 | 55 | P | LOGO>BLACK | 1.05 | 1.3 | 2.31 |
| [gsHFAzPJn5M](https://www.youtube.com/watch?v=gsHFAzPJn5M) | lolzzz_plays | custom/vs | 553,399 | 52 | MONTAGE | 30 | 30 | Y | TALK('bye bye')>BLACK | 1.59 | 2.13 | 0.4 |
| [_sRb7dEDYAA](https://www.youtube.com/watch?v=_sRb7dEDYAA) | lolzzz_plays | custom/vs | 541,509 | 47 | MONTAGE | 30 | 34 | Y | RESULT(DEFEAT)>BLACK | 2.42 | 1.45 | 1.37 |
| [LBQb6nboymg](https://www.youtube.com/watch?v=LBQb6nboymg) | lolzzz_plays | kill/record | 423,377 | 59 | PAYOFF | 30 | 45 | Y | RESULT(MVP,table)>BLACK | 2.86 | 1.79 | 0.55 |
| [f-mCo5PbnlM](https://www.youtube.com/watch?v=f-mCo5PbnlM) | lolzzz_plays | custom/vs | 421,445 | 39 | MONTAGE | 30 | 60 | Y | REACT>BLACK | 0.75 | 1.02 | 1.3 |
| [8nNyb8Tpc-A](https://www.youtube.com/watch?v=8nNyb8Tpc-A) | lolzzz_plays | match/esports | 146,195 | 28 | MONTAGE | 28 | 30 | P | REACT+LIKE_CTA>BLACK | - | - | - |
| [DwvaNRtqy20](https://www.youtube.com/watch?v=DwvaNRtqy20) | lolzzz_plays | custom/vs | 201,510 | 22 | PAYOFF | 33 | 35 | Y | RESULT(WWCD)+CTA>BLACK | 1.07 | 0.69 | 1.02 |
| [uuTVkDWOYus](https://www.youtube.com/watch?v=uuTVkDWOYus) | lolzzz_plays | custom/vs | 133,135 | 24 | MONTAGE | 22 | 25 | Y | REACT>BLACK | 1.33 | 0.96 | 0.39 |
| [3i83F-jSotA](https://www.youtube.com/watch?v=3i83F-jSotA) | lolzzz_plays | custom/vs | 198,326 | 31 | GOAL | 38 | 40 | Y | RESULT(MVP)>BLACK | 2.04 | 1.58 | 1.51 |
| [NpLfg9YU7NE](https://www.youtube.com/watch?v=NpLfg9YU7NE) | lolzzz_plays | funny | 205,345 | 33 | COLD | 0 | 0 | Y | EDITOR_CAM>ENDCARD(SUBSCRIBE) | 1.69 | 1.42 | 0.27 |
| [7bmUiiUuAdE](https://www.youtube.com/watch?v=7bmUiiUuAdE) | lolzzz_plays | custom/vs | 365,097 | 21 | GOAL | 33 | 35 | Y | RESULT(MVP)+REACT>BLACK | 4.05 | 1.81 | 3.55 |
| [va-OfDc6SYA](https://www.youtube.com/watch?v=va-OfDc6SYA) | lolzzz_plays | crate | 278,250 | 56 | GOAL | 0 | 5 | Y | PAYOFF(maxed suit)>BLACK | 1.27 | 1.13 | 0.15 |
| [Uk7i_OEWB0c](https://www.youtube.com/watch?v=Uk7i_OEWB0c) | lolzzz_plays | crate | 160,223 | 84 | TITLE | 0 | 10 | Y | PAYOFF(skin in match)>LOGO | 1.49 | 1.5 | 0.29 |
