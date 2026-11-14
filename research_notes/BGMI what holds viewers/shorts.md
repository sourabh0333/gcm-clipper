# What makes a BGMI Short get views (six channels, 171 Shorts, 14 Nov 2026)

**Method.** 171 Shorts were sampled from the six channels: @goblinbgmi 4 (all it has), @goblinsh0rts 34, @Jokerkihavelii 35 (all its stream and gaming Shorts), @jokerclipss 30, @LoLzZzGaming 34 and @lolzzzplays 34. On each channel I took the top 15 and the bottom 10 by views (the bottom 10 excludes the 6 newest uploads), plus the 9-12 most recent. On Goblin's second channel and JokerClips only gaming and stream Shorts were eligible; edits, IRL and skit Shorts were left out. For each Short I fetched fresh yt-dlp metadata: views, likes, comments, length, date and YouTube's "most replayed" heatmap, which exists for 126 Shorts, all with 81K views or more. I also took Hindi or English auto-captions (122 Shorts have speech) and the full sb0 storyboard, about 1 frame a second at 101x180. I read contact sheets showing the first 3 s, five middle frames and the last 3 s, and I measured dark first frames and black tails by script. Captions were matched against about 950 long-video and stream caption files already on disk to find where the Shorts came from. No video or audio was downloaded.

Raw data, scripts and contact sheets are in `C:\Users\soura\AppData\Local\Temp\claude\21027423ba80eb72\c7886632-c6c6-4a95-81c6-c6cbac2a769e\scratchpad\viewers\shorts\`: `meta\` (info JSON), `subs\`, `sb\`, `cs\` (contact sheets, with `cs\index.txt`), `obs.txt` (per-Short notes), `rows2.json` (all measures) and `match.json` / `match_out.txt` (source matching). In the tables below, "tops" means the top-tagged Shorts plus Joker-main Shorts over 500K (n=67). "Bottoms" means the bottom-tagged Shorts plus Joker-main Shorts under 150K (n=46). "Inference" marks reasoning beyond what was measured.

## Summary: the 10 findings that matter most

1. **The subject decides the views, not the edit.** Since 2023, **all 11 sampled Shorts above 2M views are person moments**: a friend shocked, a prank, a friend getting angry, a 1v1 against a named pro, a teammate caught sleeping, a rant, a revenge story. The best pure-skill Shorts since 2023 stop at 1.76M ([E2lr611OqRc](https://www.youtube.com/shorts/E2lr611OqRc)) and 1.48M ([OcYQ_xrdiaM](https://www.youtube.com/shorts/OcYQ_xrdiaM)). Plain skill clips topped views only in the 2020-21 PUBG Shorts boom (LoLzZz: 9.0M, 8.3M, 6.2M).
2. **Frame 1 is already the action, or the line.** Nearly every top Short opens mid-fight, already scoped in, or mid-sentence: speech starts at a median of 0.2 s. Only 3% of tops start on a dark frame, against 15% of bottoms. No top Short opens on a slow setup such as text on black or an empty lobby.
3. **Dead endings go with flops.** 28% of bottoms end on 3 s or more of black or end card, against 6% of tops. In the same era (LoLzZz main, Dec 2020-Jun 2021), 8 of 10 bottom Shorts (91-156K) end on 10-11 s "LIKE & SUBSCRIBE / THANKS FOR WATCHING" cards, while 10 of 12 top Shorts (0.9-9.0M) end within 1 s of the gameplay.
4. **The payoff sits in the middle or last third, and a reaction follows it.** Where heatmaps show a second peak (17 Shorts), the rewatched moment sits at 18-89% of the length, mostly 30-80%. After the payoff come 2-9 s of face reaction, a sticker freeze or the game's proof screen, then the Short cuts.
5. **The face carries the reaction, and the layout follows the moment.** The standard is game on top and face below (Goblin, LoLzZz) or face on top (Joker). The best Shorts switch to a full-height face for the reaction or the talk line ([LCZiW8i8zjk](https://www.youtube.com/shorts/LCZiW8i8zjk) 26-41 s, [5QoaTqu_u58](https://www.youtube.com/shorts/5QoaTqu_u58) 11-19 s, [GmZty_6yrQs](https://www.youtube.com/shorts/GmZty_6yrQs) at 11 s). Friends' webcams on a call are a top layout: 5.5M twice.
6. **On-screen text is house style, not a requirement.** Goblin's Shorts carry no text at all, only end stickers, and still reach 0.8-4.5M. Joker uses a 2-4 word caption chip over the game ("1v4 Clutch 😡"). LoLzZz (2024) burns in yellow subtitles of the key lines. JokerClips' 2025 hits open with a meme image plus text on frame 1 ("ABEY TAKLE", a shocked-face meme: 2.0M and 7.7M).
7. **"Promo" Shorts flop.** Shorts framed as ads for a long video ("☝️ Click Here to watch full video", "Full Video Tomorrow at 2PM", end cards "Watch full video on the channel") are 4 of Goblin's 10 bottoms (7-13K). A Short that stands on its own and only adds a 2-3 s end card can still do fine ([pfJ3EsMgBJk](https://www.youtube.com/shorts/pfJ3EsMgBJk) 293K).
8. **Length is not the lever.** Tops have a median of 39 s and bottoms 36.5 s. Hits run 15-60 s, plus 80-111 s in 2025-26 (1.24M at 80 s). Per-channel tops differ (JokerClips 22 s, Goblin 43 s, LoLzZz Plays 58 s), so length follows the moment.
9. **Likes per view run inverse to reach.** Bottoms get 0.118 likes per view and 0.78 comments per 1,000 views, against 0.064 and 0.17 for tops. Small Shorts are seen mostly by fans, so likes per view cannot rank moments.
10. **Shorts from highlights usually come from the long video's opening.** 6 of 10 caption-matched pairs map to the first 0-60 s of a long video (whose opening is the editor's chosen best beat). They go up 1-2 h after the long video, or 1.6-21 h before it as a teaser. Other hits come straight from a stream 5-6 days later, with no long video (5.5M, 836K).

---

## Q1-Q2. What is on screen in each Short: opening, text, layout, payoff position, ending

### Takeaway
Top Shorts are one continuous moment that starts in the action or in a spoken line. The layout is game plus face, with the face going full-screen for the reaction. The payoff lands in the middle or last third, and the Short ends within about 1-3 s of a reaction, a sticker freeze or the game's proof screen. Bottoms differ less in layout than in their dark or slow first frame, their long black or end-card tail, their promo framing and their generic subjects.

### Cited Findings
**Openings (first 1-2 s)**
- Dark first frame: 3% of tops (2 of 67: [obYMok4viHI](https://www.youtube.com/shorts/obYMok4viHI), [i92rYzZpMVI](https://www.youtube.com/shorts/i92rYzZpMVI), one black frame each) against 15% of bottoms (7 of 46, e.g. [EI-yN2e1U8k](https://www.youtube.com/shorts/EI-yN2e1U8k) 7.4K, [sqfVHkmv2BQ](https://www.youtube.com/shorts/sqfVHkmv2BQ) 8.7K, [cDTJAioWnJE](https://www.youtube.com/shorts/cDTJAioWnJE) 20K). Measured by script on the first storyboard frame (luminance under 20/255) — storyboards in `sb\`, `rows2.json`
- Speech starts at a median of 0.2 s in both tops and bottoms (auto-caption first cue), so the creators cut into a sentence and never into silence. Examples: "Joker bhai suno nahi bach paoge…" at 0 s ([CVqRiZ-wwNw](https://www.youtube.com/shorts/CVqRiZ-wwNw), 537K); "bhai ek baat bataun tum logon ko" at 0 s ([bmoICLbNemI](https://www.youtube.com/shorts/bmoICLbNemI), 2.23M); a teammate calling "Goblin go… mere paas aao saare" at 0 s ([iVF6tpnxnfA](https://www.youtube.com/shorts/iVF6tpnxnfA), 1.23M); the complaint about not getting food from 0 s ([9gy3caHoOMs](https://www.youtube.com/shorts/9gy3caHoOMs), 5.48M) — captions in `subs\`
- **Payoff on frame 1**: "JONATHAN CAUGHT SLEEPING AT LAN" shows Jonathan asleep on the desk from 0 s, with LoLzZz reacting below (3.26M, 29 s) — [zC2CyyUHKG0](https://www.youtube.com/shorts/zC2CyyUHKG0)
- **Hook graphic on frame 1** (JokerClips 2025): a shocked-face meme image at 0 s, then gameplay ([_RgXLRs1wx8](https://www.youtube.com/shorts/_RgXLRs1wx8), 7.71M); a meme still with "ABEY TAKLE 😡" over Joker shouting ([TH4R1ypnHCc](https://www.youtube.com/shorts/TH4R1ypnHCc), 2.0M); "MY EMOTIONS WHEN TEAM SOUL TAKES CHICKEN DINNER" ([aBL79oTbVdk](https://www.youtube.com/shorts/aBL79oTbVdk), 242K) — storyboards
- **Mid-fight or already scoped in**: the norm on Goblin, LoLzZz and Joker gameplay Shorts. Examples: [DfOcogRMngg](https://www.youtube.com/shorts/DfOcogRMngg) (4.52M), [TVZ2RLVXD7E](https://www.youtube.com/shorts/TVZ2RLVXD7E) (583K, scope at 0 s), [q2sIv9unm6o](https://www.youtube.com/shorts/q2sIv9unm6o) (1.97M, scope at 0 s), [UWFVd8F1Tj4](https://www.youtube.com/shorts/UWFVd8F1Tj4) (314K, scope at 0 s)
- **Setup openings among the tops are rare and always in motion**: the plane and map drop for a story Short ("Hacker ne -78 karwadiya", [0jvTiPOVkSM](https://www.youtube.com/shorts/0jvTiPOVkSM), 1.17M), or driving ([ntCFulFOPhw](https://www.youtube.com/shorts/ntCFulFOPhw), 1.45M)
- **Bottom openings** include text on black ("BUT THE ONE THING THEY LOVE MORE THAN A HERO", [yu4M4do-vvM](https://www.youtube.com/shorts/yu4M4do-vvM), 11K), a small letterboxed 16:9 frame on black ([ju_Xek0OV_4](https://www.youtube.com/shorts/ju_Xek0OV_4), 12.5K), a facecam talking over a lobby ([Tllb01bul2M](https://www.youtube.com/shorts/Tllb01bul2M), 8.4K), a parachute landing ([lSPpKn4zuJU](https://www.youtube.com/shorts/lSPpKn4zuJU), 123K, same era as 1-9M tops) and a stock sea clip ([54rE1HtrbL0](https://www.youtube.com/shorts/54rE1HtrbL0), 14K)

**On-screen text**
- Goblin second channel (2023-26): no titles, captions or chips inside the Short. The only graphics are end stickers (skull with crown, cowboy skull, crying-laughing skull, troll face) — e.g. [CdkN90FTUl8](https://www.youtube.com/shorts/CdkN90FTUl8) (795K), [GS0ib2FtnS0](https://www.youtube.com/shorts/GS0ib2FtnS0) (322K), [YK7JXrVblYQ](https://www.youtube.com/shorts/YK7JXrVblYQ) (313K)
- Goblin main: a fixed top title chip "Goblin 1v4 DRX" over a blurred-fill letterbox ([pfJ3EsMgBJk](https://www.youtube.com/shorts/pfJ3EsMgBJk), 293K), and a designed template with a "GOBLIN 64 CARNIVAL GAMING" header and a big "Day 2 WWCD Match 1" footer ([OdM-P3Ykios](https://www.youtube.com/shorts/OdM-P3Ykios), 164K)
- Joker main (2023-26): a 2-4 word caption chip over the game with an emoji ("1v4 Clutch 😡" on [CVqRiZ-wwNw](https://www.youtube.com/shorts/CVqRiZ-wwNw), "AKM + RED DOT 🔥" on [LCZiW8i8zjk](https://www.youtube.com/shorts/LCZiW8i8zjk), "Scout Clutch 😱🔥" on [LrS00Xs8ym0](https://www.youtube.com/shorts/LrS00Xs8ym0), "Submarine Buggati 😱🤣" on [wCzImt3k8hE](https://www.youtube.com/shorts/wCzImt3k8hE) 5.5M). Some carry a two-line "sher" quote caption ([_BO0YJZGLeI](https://www.youtube.com/shorts/_BO0YJZGLeI), 459K; [smR-drtg8oI](https://www.youtube.com/shorts/smR-drtg8oI), 149K), or a setup caption ("Lagta hai abhi hone wala hai SYSTUMM", [IQkWDpXNhf0](https://www.youtube.com/shorts/IQkWDpXNhf0), 546K)
- LoLzZz main (2023-24): burned yellow subtitles of key lines only ("HELLO!", "LINE ME NAAM AYA MERE TO" on [oz7YsNIcLb4](https://www.youtube.com/shorts/oz7YsNIcLb4), 734K; "AA RAHA HU", "BHAIII" on [rSY5o7XiIV4](https://www.youtube.com/shorts/rSY5o7XiIV4), 598K), and a name label on a meme insert ("MAYUR BHAI:-", [sq65JXmSjXM](https://www.youtube.com/shorts/sq65JXmSjXM), 1.13M)
- LoLzZz Plays 2026: no text, except the record teaser's top caption "JUST A NORMAL RECORD" ([FyHDoGMnHO4](https://www.youtube.com/shorts/FyHDoGMnHO4)) and a "Funny Chats 🤣🤣" header ([H8ee2ZHqaDM](https://www.youtube.com/shorts/H8ee2ZHqaDM), 546K)
- Word-by-word burned subtitles appear only on a few JokerClips Shorts ([icIr3BWd1nM](https://www.youtube.com/shorts/icIr3BWd1nM), 145K; [qXT48jNRkSc](https://www.youtube.com/shorts/qXT48jNRkSc), 606K)

**Layouts**
- Goblin second channel: stacked stream (game on top, face below); stacked LAN (broadcast on top, player-cam below); and in 2026 a broadcast letterbox with a blurred fill and no cam, which several 2026 Shorts switch into mid-Short ([aUQ77J2YJk8](https://www.youtube.com/shorts/aUQ77J2YJk8) moves to stacked at 25 s; [DSZcuIPViVY](https://www.youtube.com/shorts/DSZcuIPViVY) drops the cam at 22 s). Across all 438 Goblin Shorts the earlier census measured a 90K median for stacked against 46K for game-only crops, and 520K for stacked LAN (n=12) — [goblin_shorts.md](../BGMI%20creators%20content%20A%20to%20Z/goblin_shorts.md) section 4
- Joker main: three tiers — face on top (about 30%), game in the middle with a caption chip, and the "JOKER" banner with a follower counter at the bottom. Friends' calls go to 2-4 webcams on top ([xeUMV53DLmU](https://www.youtube.com/shorts/xeUMV53DLmU), 4 cams, 569K; [9gy3caHoOMs](https://www.youtube.com/shorts/9gy3caHoOMs), 2 cams, 5.48M; [wCzImt3k8hE](https://www.youtube.com/shorts/wCzImt3k8hE), 2 cams, 5.50M)
- JokerClips: game on top and face below, a screen share on top with face below ([nh5gRpJjWAk](https://www.youtube.com/shorts/nh5gRpJjWAk), 5.57M), an 8-person call grid ([buCYi2T04ro](https://www.youtube.com/shorts/buCYi2T04ro), 1.37M), and a switch to face-only on black with a label for a talk line ("BGMI vs FREE FIRE", [bmoICLbNemI](https://www.youtube.com/shorts/bmoICLbNemI) 6-16 s)
- LoLzZz (main and Plays): game on top (about 55-60%) and face below, the same in 2020-21 and in 2026. Reaction Shorts put another video, a chat screenshot or the LAN stage on top and his face below ([zC2CyyUHKG0](https://www.youtube.com/shorts/zC2CyyUHKG0), [iO0BZnnozSQ](https://www.youtube.com/shorts/iO0BZnnozSQ) 1.25M, [qxX7OBsUino](https://www.youtube.com/shorts/qxX7OBsUino) 682K)
- **The face goes full-height for the reaction or talk** and comes back for the play: [LCZiW8i8zjk](https://www.youtube.com/shorts/LCZiW8i8zjk) 26-41 s; [smR-drtg8oI](https://www.youtube.com/shorts/smR-drtg8oI) 20-31 s; [5QoaTqu_u58](https://www.youtube.com/shorts/5QoaTqu_u58) 11-19 s (3.42M); a friend's face with a name label "Snax" at 16-20 s in [IQkWDpXNhf0](https://www.youtube.com/shorts/IQkWDpXNhf0); Snax shocked, full-screen, at 11 s in [GmZty_6yrQs](https://www.youtube.com/shorts/GmZty_6yrQs) (8.63M). The editing study watched in Chrome found the same in [HhcQY2wm8Ug](https://www.youtube.com/shorts/HhcQY2wm8Ug): hard cuts to the face on a sentence, never mid-shooting — [editing_timing_watched.md](../BGMI%20creators%20content%20A%20to%20Z/editing_timing_watched.md)
- Showing the face is not enough on its own: 2022 LoLzZz Plays Shorts with a hooded, dark, barely visible face got 10-17K ([X1wGCJUsxoo](https://www.youtube.com/shorts/X1wGCJUsxoo), [Nhpl2MR9qPU](https://www.youtube.com/shorts/Nhpl2MR9qPU), [BbDaK7eJo9k](https://www.youtube.com/shorts/BbDaK7eJo9k)). 6 of Goblin's 15 tops have no cam in the game frame (game-only crops, LAN broadcast or venue camera)

**Where the payoff sits (heatmaps plus frames)**
- Shorts heatmaps peak at the very start and decay fast: the median value is 0.71 over the first 5% and 0.085 over the middle 40% (126 Shorts with heatmaps) — `rows2.json`
- 17 Shorts have a second peak of 0.4 or more after the first 15%. It sits on the payoff: [CdkN90FTUl8](https://www.youtube.com/shorts/CdkN90FTUl8) at 20 s of 31 (the bounty denial, peak 1.0); [Gl8hYRWMP1o](https://www.youtube.com/shorts/Gl8hYRWMP1o) at 34 s of 80 (peak 1.0); [g1WsZReW5VQ](https://www.youtube.com/shorts/g1WsZReW5VQ) at 11 s of 24 (the grenade kill seen at 12-15 s); [TVZ2RLVXD7E](https://www.youtube.com/shorts/TVZ2RLVXD7E) at 18 s of 22 (the kill at 16 s); [GS0ib2FtnS0](https://www.youtube.com/shorts/GS0ib2FtnS0) at 13 s of 35; [SoWmrN58UYA](https://www.youtube.com/shorts/SoWmrN58UYA) at 40 s of 54; [PVmTr-gdojA](https://www.youtube.com/shorts/PVmTr-gdojA) at 14 s of 30. Positions range from 18% to 89% of the length, mostly 30-80%
- A reaction tail follows the payoff: g1WsZReW5VQ has the kill at 12-15 s, then LoLzZz gets up from his chair until 23 s; GS0ib2FtnS0 has the kill at about 21 s, then a black-and-white freeze with a sticker for 8 s (26-34 s); [DfOcogRMngg](https://www.youtube.com/shorts/DfOcogRMngg) has the revenge kill at 18-27 s, then the full face at 33-34 s
- Story Shorts put the setup first and the payoff last: "Revenge" stitches a death (0-13 s) to a later clip with a different shirt, so a later stream, of the revenge kill ([DfOcogRMngg](https://www.youtube.com/shorts/DfOcogRMngg), 4.52M). "Why i got Banned?" answers its title with the ban notice at 11 s of 17 ([KP4ie-wf26Q](https://www.youtube.com/shorts/KP4ie-wf26Q), 1.04M). The crate Short reveals the item at the end ([jiqQW2mSqsU](https://www.youtube.com/shorts/jiqQW2mSqsU), "CONGRATULATIONS Mummy Set" at 44-46 s of 47)

**Endings**
- A black or end-card tail of 3 s or more: 4 of 67 tops against 13 of 46 bottoms — script on the last frames (luminance under 22/255; text cards on black count as dark)
- LoLzZz main in the same era (Dec 2020-Jun 2021): 12 tops (0.9-9.0M) have a median dark tail of 1.0 s, and only OmMt0L6eDDI (3.9 s) and fvgWBNVXOxI (6.9 s) run longer. 8 of the 10 bottoms (91-156K) end on 9.6-11.5 s of "THANKS FOR WATCHING", "LIKE & SUBSCRIBE" or logo cards ([pDONouwbY28](https://www.youtube.com/shorts/pDONouwbY28), [XKmkjk6qTxQ](https://www.youtube.com/shorts/XKmkjk6qTxQ), [AVJbu4PBiMI](https://www.youtube.com/shorts/AVJbu4PBiMI), [2liKUv4uRJ0](https://www.youtube.com/shorts/2liKUv4uRJ0)) — `rows2.json`, contact sheets `cs_f_01`-`cs_f_05`
- Endings among the tops:
  - the game's proof screen: "TEAM FINISHED TZ FINISHES 6" ([SoWmrN58UYA](https://www.youtube.com/shorts/SoWmrN58UYA)), "#1 WINNER WINNER CHICKEN DINNER" ([OcYQ_xrdiaM](https://www.youtube.com/shorts/OcYQ_xrdiaM)), a rank card ([ntCFulFOPhw](https://www.youtube.com/shorts/ntCFulFOPhw)), an item reveal ([jiqQW2mSqsU](https://www.youtube.com/shorts/jiqQW2mSqsU))
  - the face's reaction: [g1WsZReW5VQ](https://www.youtube.com/shorts/g1WsZReW5VQ), [rSY5o7XiIV4](https://www.youtube.com/shorts/rSY5o7XiIV4), [DfOcogRMngg](https://www.youtube.com/shorts/DfOcogRMngg), and a friend laughing in black and white on [wCzImt3k8hE](https://www.youtube.com/shorts/wCzImt3k8hE)
  - a sticker on a black-and-white freeze for 2-8 s (Goblin 2026)
  - a meme clip followed by TV colour bars for 1-2 s (LoLzZz Plays 2023: [q2sIv9unm6o](https://www.youtube.com/shorts/q2sIv9unm6o), [FuxPa24LkzM](https://www.youtube.com/shorts/FuxPa24LkzM); JokerClips: a man laughing hysterically on [bmoICLbNemI](https://www.youtube.com/shorts/bmoICLbNemI) and [TH4R1ypnHCc](https://www.youtube.com/shorts/TH4R1ypnHCc))
  - or a plain cut on the loot screen ([iVF6tpnxnfA](https://www.youtube.com/shorts/iVF6tpnxnfA))
- Short CTA cards at the end also appear on tops: "SUBSCRIBED" bell over a blur for 2 s ([pEAKmipzzrk](https://www.youtube.com/shorts/pEAKmipzzrk), 1.30M), "Follow me on Kick" for 3 s ([YK7JXrVblYQ](https://www.youtube.com/shorts/YK7JXrVblYQ), 313K), a giveaway card for 3 s ([zC2CyyUHKG0](https://www.youtube.com/shorts/zC2CyyUHKG0), 3.26M), and blurred "SUBSCRIBE NOW" for 2 s on 2023 Joker Shorts
- No sampled Short loops back to its own start visibly (no matching first and last frames)

### Inferences
- What hurts is dead air, at the start or at the end. A 2-3 s CTA card did not stop Shorts reaching 0.3-3M, but 5-11 s of card is up to a quarter of a Short with nothing happening (inference: viewers swipe away, and YouTube reads that as weak retention). The LoLzZz 2021 contrast is within one era, but tops and bottoms cluster in different months (tops mostly Dec 2020-Feb 2021, bottoms Mar-Jun 2021), so timing may also play a part.
- The heatmap second peak is the best automatic sign of where viewers found the payoff. It sits before the end, which supports ending 2-9 s after the payoff and not on it.

### Gaps
- Sound could not be heard: music beds, sound effects, the loudness of the reaction and voice-over hooks are unmeasured. Captions show only that speech starts at 0-1 s.
- Text smaller than about 10% of the frame height is unreadable at 101x180, so small subtitles may be missed. 2021-22 Shorts uploaded at low resolution have even smaller storyboards (48x27 to 50x90) and were not read in detail.
- The heatmap meaning for Shorts (loops against seeks) is not documented by YouTube; values are relative within each Short.

## Q3. Top against bottom: which openings, lengths, layouts, payoff positions, endings and subjects win

### Takeaway
Subjects separate tops from bottoms far more than any format variable. Person and relationship moments win: a named friend or teammate shocked, angry, pranked or caught; a rivalry; a rant; a revenge story. Generic kill clips with vague titles, promos, other people's plays, other games and random IRL clips lose. Among format variables, only a dark or slow start and a long dead tail separate the groups clearly. Length and likes per view do not.

### Cited Findings
- **Summary measures** (tops n=67 against bottoms n=46): median views 1,237,871 against 20,610; length 39 s against 36.5 s; likes per view 0.064 against 0.118; comments per 1,000 views 0.17 against 0.78; dark first frame 3% against 15%; dark tail of 3 s or more 6% against 28% — `rows2.json` (`agg.py`)
- **By channel:**

  | Channel, group | n | Median views | Median length | Likes per view | Tail of 3 s or more |
  |---|---|---|---|---|---|
  | Goblin second, top | 15 | 1,009,046 | 43 s | 0.047 | 13% |
  | Goblin second, bottom | 10 | 9,963 | 33.5 s | 0.167 | 40% |
  | JokerClips, top | 15 | 525,236 | 22 s | 0.072 | 0% |
  | JokerClips, bottom | 10 | 23,271 | 20 s | 0.092 | 0% |
  | LoLzZz main, top | 15 | 1,581,701 | 41 s | 0.053 | 13% |
  | LoLzZz main, bottom | 10 | 135,014 | 46.5 s | 0.108 | 90% |
  | LoLzZz Plays, top | 15 | 1,246,044 | 58 s | 0.104 | 0% |
  | LoLzZz Plays, bottom | 10 | 13,037 | 38.5 s | 0.157 | 0% |
  | Joker main, top 12 | 12 | 541,328 | 34.5 s | 0.074 | 8% |
  | Joker main, bottom 12 | 12 | 166,736 | 32 s | 0.085 | 8% |

  — `rows2.json`
- **Length buckets** (all 171): 0-15 s median 221K (n=22); 16-30 s 317K (n=48); 31-45 s 233K (n=48); 46-60 s 598K (n=49); over 60 s 717K (n=4). The 46-60 s bucket is lifted by LoLzZz's 2021 and 2023 hits, so there is no clean length effect — `rows2.json`
- **The 11 Shorts above 2M from 2023 on** are all person or relationship moments:

  | Short | Views | Length | Moment |
  |---|---|---|---|
  | [GmZty_6yrQs](https://www.youtube.com/shorts/GmZty_6yrQs) | 8.63M | 19 s | Snax shocked by an outfit transition |
  | [_RgXLRs1wx8](https://www.youtube.com/shorts/_RgXLRs1wx8) | 7.71M | 31 s | "When hacker meets developer" banter |
  | [nh5gRpJjWAk](https://www.youtube.com/shorts/nh5gRpJjWAk) | 5.57M | 22 s | Reacting to what Mortal shows |
  | [wCzImt3k8hE](https://www.youtube.com/shorts/wCzImt3k8hE) | 5.50M | 42 s | Prank on Mavi, the car driven into the sea |
  | [9gy3caHoOMs](https://www.youtube.com/shorts/9gy3caHoOMs) | 5.48M | 40 s | Goldy angry about food |
  | [DfOcogRMngg](https://www.youtube.com/shorts/DfOcogRMngg) | 4.52M | 36 s | Revenge |
  | [5QoaTqu_u58](https://www.youtube.com/shorts/5QoaTqu_u58) | 3.42M | 52 s | Goblin vs Neyo 1v1 |
  | [zC2CyyUHKG0](https://www.youtube.com/shorts/zC2CyyUHKG0) | 3.26M | 29 s | Jonathan asleep at the LAN |
  | [DiOrzVnAZNk](https://www.youtube.com/shorts/DiOrzVnAZNk) | 2.67M | 60 s | Jonathan's set crate |
  | [bmoICLbNemI](https://www.youtube.com/shorts/bmoICLbNemI) | 2.23M | 23 s | A "BGMI vs Free Fire" rant |
  | [TH4R1ypnHCc](https://www.youtube.com/shorts/TH4R1ypnHCc) | 2.00M | 23 s | Rage when an ad interrupts a LAN broadcast |

  The best pure-skill Shorts from 2023 on: "Sniper God bolte!" 1.76M ([E2lr611OqRc](https://www.youtube.com/shorts/E2lr611OqRc)), "Most intense Clutch" 1.48M ([OcYQ_xrdiaM](https://www.youtube.com/shorts/OcYQ_xrdiaM)), "Air strike in BGMI" 1.97M ([q2sIv9unm6o](https://www.youtube.com/shorts/q2sIv9unm6o); funny, with meme inserts) — `titles_sorted.txt`
- **In the 2020-21 Shorts boom, skill clips alone hit 5-9M**: "Sniper God Bolteee!!" 9.0M ([aSie600ul4Q](https://www.youtube.com/shorts/aSie600ul4Q)), "1 v 4 DBS Clutch in Apartment" 8.3M ([Css0AXuRBZQ](https://www.youtube.com/shorts/Css0AXuRBZQ)), "1v4 Clutch Impossible Solo vs Squad" 6.2M ([ISDNQNIa9lI](https://www.youtube.com/shorts/ISDNQNIa9lI)), "End Zone 1v4 Clutch" 5.7M ([OmMt0L6eDDI](https://www.youtube.com/shorts/OmMt0L6eDDI)) — metadata
- **Bottom subjects**:
  - generic gameplay with vague titles: "Frags 👿🔥" 13K, "SPRAY TOH HAI" 13K, "EASY 1v2" 12K, "Aim Hack is on" 12K, "I'm a clutchgod" 10K, "Champions 🎉🎊" 8.7K
  - promos: "☝️ Click Here to watch full video 💀" 7.4K and 8.6K; "Full Video Tomorrow at 2PM" 12.5K
  - other games: Valorant at 20-35K
  - someone else's play: "LoLzZz Shocked by KOOPS 1v4" 20K, against 141-178K for "SHOCKED BY HYDRO 1HP RUSH" and "FASTEST 1v4 IN BMSD"
  - an unlucky crate: 14K
  
  — `titles_sorted.txt`
- **Fails and losses are payoffs too**: "💀", ending on his own "ELIMINATED #15" screen, 921K ([uCmDja_0DIE](https://www.youtube.com/shorts/uCmDja_0DIE)); "Pro player killed me 😢" 1.43M; "RECALL NAHI DE PAYA 😭" 1.45M; "Car Fight with Sad Ending" 1.35M; "Why i got Banned?" 1.04M
- **Famous people help as inserts and as subjects**: LoLzZz Plays' 2023 hits insert clips of known Indian creators and personalities (Hindustani Bhau, CarryMinati, an "ENEMIES" two-YouTuber meme) at 19-53 s ([q2sIv9unm6o](https://www.youtube.com/shorts/q2sIv9unm6o), [FuxPa24LkzM](https://www.youtube.com/shorts/FuxPa24LkzM)). A named person or team (Snax, Mortal, Mavi, Goldy, Neyo, Jonathan, Team SouL, Harsh, Krutika and Regaltos) appears in the title of 11 of the 35 most-viewed sampled Shorts. The earlier study found the same on Goblin's channel: titles naming a person had a 158K median against 110K for 2025-26 Shorts — [goblin_shorts.md](../BGMI%20creators%20content%20A%20to%20Z/goblin_shorts.md)
- **Layout**: tops and bottoms on the same channel mostly share a layout (LoLzZz 2021 tops and bottoms are both game-over-face). Layout differences show only in the channel-wide census (Goblin stacked 90K against game-only 46K, n=124 and 107) — [goblin_shorts.md](../BGMI%20creators%20content%20A%20to%20Z/goblin_shorts.md)
- **Heatmaps**: Shorts whose curve ends high (last 5% at 0.4 or more, n=21) have a median of 313K views, against 817K for those ending low (under 0.1, n=76) — `rows2.json`

### Inferences
- Likes and comments per view are higher on bottoms because a Short that is not pushed is watched mostly by subscribers, who like and comment more. A Kaatclip ranker should not use likes per view from past Shorts as its target. Views, or retention when it is available, are the target.
- The shift from "any clutch gets millions" (2020-21) to "people moments get millions" (2023-26) fits a saturated BGMI-clip feed. For a creator's 2026 stream, the moments worth turning into Shorts are interactions: a teammate's shock, a friend's anger, banter with a named rival, a prank, a rant, a fail with a reaction. A clean kill with no reaction is weaker.
- A high heatmap end goes with lower views, which suggests viewers who reach the end without having swiped already are fans rewatching. Cause and effect cannot be separated here.

### Gaps
- Real retention ("viewed vs swiped away", average percentage viewed) is private to the channel owner; heatmaps are the only public proxy and exist only above about 80K views.
- Upload era confounds every top-against-bottom comparison (algorithm changes, channel size). Comparisons were kept within channel and, for LoLzZz 2021, within era, but they are not controlled experiments.
- Subjects were judged from titles plus frames, not from audio.

## Q4. Are Shorts cut from the same streams and highlights as the long videos?

### Takeaway
Yes, in three ways. Most often the Short is the first 30-60 s of a long video, posted 1-2 h after it, or before it as a teaser. Others come from the middle of a long video, often posted a day earlier on the other channel. Some come straight from a stream days later with no long video, and these include the biggest hits. A Short cut from a highlight therefore starts best at the highlight's opening beat, but it must stand alone: promo framing loses.

### Cited Findings
- Caption matches found in this study (score is shared 3-word sequences in one time cluster; offsets are ±25 s):

  | Short | Source | Where in source | Posted |
  |---|---|---|---|
  | [aUQ77J2YJk8](https://www.youtube.com/shorts/aUQ77J2YJk8) 52K | long [5oGAOwgtrK8](https://www.youtube.com/watch?v=5oGAOwgtrK8) "Goblin 1v4 OG" (267 s) | start (score 200) | 17.6 h after |
  | [YK7JXrVblYQ](https://www.youtube.com/shorts/YK7JXrVblYQ) 313K | long [s__lq3xZwKM](https://www.youtube.com/watch?v=s__lq3xZwKM) (187 s) | start (56) | 48.6 h after |
  | [Tllb01bul2M](https://www.youtube.com/shorts/Tllb01bul2M) 8K | long [sycnSTtAOKA](https://www.youtube.com/watch?v=sycnSTtAOKA) | start (44) | 1.0 h after |
  | [m_Z1P0gHuLs](https://www.youtube.com/shorts/m_Z1P0gHuLs) 14K | crate long [8uTVdSeesys](https://www.youtube.com/watch?v=8uTVdSeesys) | about 0:19 (64) | 1.2 h after |
  | [_RgXLRs1wx8](https://www.youtube.com/shorts/_RgXLRs1wx8) 7.71M | JokerClips video [V1TtI-fbVYo](https://www.youtube.com/watch?v=V1TtI-fbVYo) (71 s horizontal) | start (30) | 1.1 h after |
  | [pfJ3EsMgBJk](https://www.youtube.com/shorts/pfJ3EsMgBJk) 293K (Goblin main) | long [MQ8SC-_e8ZQ](https://www.youtube.com/watch?v=MQ8SC-_e8ZQ) "Drx v/s Team iQOOSouL" (384 s) | about 1:47 (29) | 7.3 h after, end card "Watch the full video on the channel" |
  | [OqEMk59-Z1o](https://www.youtube.com/shorts/OqEMk59-Z1o) 300K (LoLzZz main) | long [gJ_3K7mx8ZQ](https://www.youtube.com/watch?v=gJ_3K7mx8ZQ) "THIS BGIS CLUTCH SHOCKED EVERYONE" (489 s) | start (76) | **1.6 h before** |
  | [4C0MTz-S9sE](https://www.youtube.com/shorts/4C0MTz-S9sE) 294K (Joker main) | JokerClips long [AJETkuZ0K6A](https://www.youtube.com/watch?v=AJETkuZ0K6A) (703 s) | about 5:31 (150) | **21 h before**, on the other channel |
  | [9gy3caHoOMs](https://www.youtube.com/shorts/9gy3caHoOMs) 5.48M (Joker main) | stream [LN_XTfC4-fk](https://www.youtube.com/watch?v=LN_XTfC4-fk) "CHAINED TOGETHER WITH HOMIES" | 2:56:35 (47) | 117 h (4.9 days) after the stream |
  | [i6GGwJZroOY](https://www.youtube.com/shorts/i6GGwJZroOY) 836K (Joker main) | IRL stream [lwvfYT4cm4Q](https://www.youtube.com/watch?v=lwvfYT4cm4Q) "IRL PARIS ESPORTS WORLD CUP" | 1:24:21 (33 vs 14 for the runner-up) | 151 h (6.3 days) after; confirms the earlier "probably cut from that stream" inference in joker_main.md |

  — `match.json`, `match_out.txt`
- Earlier matches on Goblin's second channel (do not repeat): "50 Seconds of Bullying" 456K at 5:09 of its long video, posted 1.0 h after it. Three Shorts from stream [ds2q0wh-YE0](https://www.youtube.com/watch?v=ds2q0wh-YE0) went up 3-8 days before the long 2v2 WOW video. [V75ArTHWzQs](https://www.youtube.com/shorts/V75ArTHWzQs) 422K came from a stream with no long video — [goblin_shorts.md](../BGMI%20creators%20content%20A%20to%20Z/goblin_shorts.md)
- The LoLzZz record teaser Short ([FyHDoGMnHO4](https://www.youtube.com/shorts/FyHDoGMnHO4), 117K) went up on Plays 5 h after the main 72-kill video (990K). It is a proof sequence: "JUST A NORMAL RECORD" caption, scope, "#1 WINNER WINNER CHICKEN DINNER" at 13 s, "THE RECORD" at 15 s, MVP with 72 kills at 19 s, then a 3 s "FULL VIDEO IS ON YOUTUBE" card — storyboard; [lolzzz_plays.md](../BGMI%20creators%20content%20A%20to%20Z/lolzzz_plays.md)
- Promo framing underperforms: Goblin's promo Shorts have a median of 14K (n=8) against 84K for all Shorts ([goblin_shorts.md](../BGMI%20creators%20content%20A%20to%20Z/goblin_shorts.md)). In this sample, the promos "Click Here…" (7.4K, 8.6K) and "Full Video Tomorrow" (12.5K), and the long-video-start cuts with a 3 s "Watch full video" card ([Tllb01bul2M](https://www.youtube.com/shorts/Tllb01bul2M) 8K, [m_Z1P0gHuLs](https://www.youtube.com/shorts/m_Z1P0gHuLs) 14K), are all bottoms
- Cadence per stream (earlier studies): a good Goblin stream gives 2-4 Shorts over 1-12 days ([goblin_shorts.md](../BGMI%20creators%20content%20A%20to%20Z/goblin_shorts.md)); LoLzZz Plays posts about 2 Shorts a week ([lolzzz_plays.md](../BGMI%20creators%20content%20A%20to%20Z/lolzzz_plays.md)); Joker main posted 3 gaming Shorts in 2026 ([joker_main.md](../BGMI%20creators%20content%20A%20to%20Z/joker_main.md))

### Inferences
- A long video's opening is the editor's chosen best beat (its cold open), so "the first 30-60 s of the highlight" is a cheap, proven Short. The same cut can be a flop (Tllb01bul2M, 8K) or a hit (_RgXLRs1wx8, 7.7M); what decides is whether the moment is a person moment and whether the Short opens on it, not where in the video it sits.
- The biggest stream-derived hits (5.48M, 836K) are moments that never became a long video: a friend's tantrum, an IRL aura moment. A Shorts finder that scans only the highlight's chosen fights will miss talk and banter moments. Kaatclip should rank Shorts candidates over the whole stream, using the highlight as one source among others.

### Gaps
- Only 10 of 122 captioned Shorts matched a source with confidence. Many Shorts have too little speech (music, caster audio), and many source streams (Kick, Loco, LAN broadcasts) are not on disk.
- The 54rE1HtrbL0 match (score 32) points to a long video posted almost two years after the Short. It is probably that later video reusing the Short's clip; it was ignored.

## Rules for an automatic Shorts editor (Kaatclip)

Each rule is followed by its evidence.

1. **Pick the moment by its subject first.** Rank candidates higher when a named teammate, friend or rival reacts (shock, anger, laughter), on banter or a rant (a long run of fast talk with laughter), on a fail with a reaction, or on a story with a setup and payoff within 60 s. Rank a lone kill with no reaction below these. *Evidence: all 11 Shorts above 2M from 2023 on are person moments; the best skill-only Shorts reach 1.5-1.8M; generic "Frags", "Spray" and "Easy 1v2" sit at 10-20K.*
2. **Length = the moment plus a reaction tail, 15-60 s.** Default 20-45 s; allow up to 60 s for a clutch or a story; never pad. *Evidence: tops have a median of 39 s and bottoms 36.5 s (no length effect); hits run 19-60 s (8.6M at 19 s, 2.7M at 60 s).*
3. **Frame 1 = action or a spoken line.** Start at the first shot, the call ("idhar se aa raha hai") or the first word of the setup sentence, never on silence, a lobby, a parachute or black. Do not put text on black. *Evidence: dark first frame on 3% of tops against 15% of bottoms; speech at a median of 0.2 s; bottoms open on text on black, a parachute or a facecam over a lobby.*
4. **If the payoff is visual and instant (someone caught, a shocked face), show it in the first second.** Otherwise open on the setup line and land the payoff at 30-80% of the length. *Evidence: zC2CyyUHKG0 (3.26M) shows the payoff at 0 s; heatmap second peaks sit at 18-89% (mostly 30-80%) of the length.*
5. **End 2-6 s after the payoff, on the reaction or the game's proof screen.** Use the full-height face laughing or shouting, or WWCD, "TEAM FINISHED", a rank or MVP card, or an item reveal. Then cut. *Evidence: tops end on a reaction or proof screen (g1WsZReW5VQ, OcYQ_xrdiaM, SoWmrN58UYA, jiqQW2mSqsU, wCzImt3k8hE).*
6. **No dead tail.** Keep black, logo and CTA cards at 2 s or less (3 s at most), and only when the creator asks for one; never 5-11 s. *Evidence: 28% of bottoms against 6% of tops have a tail of 3 s or more; in LoLzZz 2021, 8 of 10 bottoms had 10-11 s cards and tops about 1 s.*
7. **Layout: game plus face stacked; face on top or below is the creator's choice; full-height face for talk and reaction beats.** Switch on a sentence or a reaction, never mid-shooting; hold the face for the whole line or reaction (about 3-15 s); return to the stack for play. For a call with friends, stack 2-4 webcams on top of the game. *Evidence: the full-face switches on LCZiW8i8zjk, 5QoaTqu_u58, GmZty_6yrQs and smR-drtg8oI; the HhcQY2wm8Ug timing watched in Chrome; Goblin census stacked 90K against game-only 46K; call layouts at 5.5M.*
8. **Skip the face when it says nothing.** If the facecam is dark, hooded or blank during the moment, use a game-only crop or a blurred-fill letterbox. *Evidence: 2022 LoLzZz Plays Shorts with a hooded face got 10-17K; 6 of Goblin's 15 tops have no cam in the game frame.*
9. **Text is optional and creator-styled. Never a paragraph; never on black.** Pick one style per creator from three proven ones:
   - (a) none, plus one emoji sticker on a 1-2 s black-and-white freeze at the payoff (Goblin);
   - (b) a 2-4 word caption chip over the game for the whole Short ("1v4 Clutch 😡") (Joker);
   - (c) burned subtitles of the key lines only, in big yellow words, 1-3 words at a time (LoLzZz 2024).
   
   For a talk moment, a 2-5 word label of the topic ("BGMI vs FREE FIRE") over the full face works. *Evidence: the house styles of channels with 0.3-4.5M Shorts.*
10. **One moment per Short. Stitch only to tell a story** (a setup then its payoff, even across streams), and say so in the title. *Evidence: "Revenge" (4.52M) stitches a death to a later revenge kill; nearly every other top is one continuous piece.*
11. **Don't make "watch the full video" Shorts.** The Short must work alone; at most a 2 s end card or a pinned-comment link. *Evidence: Goblin promo Shorts have a 14K median; the sample's promos sit at 7-13K.*
12. **Titles name the person or situation in 2-6 words plus one emoji** ("Goldy Dada Gussa Ho Gaye 🤣", "JONATHAN CAUGHT SLEEPING AT LAN 😭💀"). Avoid "Frags 🔥" and "Click here". *Evidence: the top titles against the bottom titles listed above; named-person titles reach a 158K median against 110K without (Goblin 2025-26).*
13. **Sources and count per stream:** offer 3-5 candidates per stream and expect the creator to post 2-4. Candidates are:
    - the highlight's opening beat (post 1-2 h after the long video, or as a teaser before it);
    - 1-2 other moments from inside the highlight;
    - 1-2 talk, banter or reaction moments from anywhere in the stream, including non-gameplay segments;
    - for a record or WWCD match, the proof teaser: the final kills, then WWCD, then MVP, in about 20-26 s, with a top caption.
    
    *Evidence: the caption matches above; Goblin 2-4 Shorts per good stream; the FyHDoGMnHO4 proof teaser.*
14. **Don't optimise for likes per view.** Use views or retention as the target when learning from a creator's past Shorts. *Evidence: bottoms have 0.118 likes per view against 0.064 for tops, and 0.78 against 0.17 comments per 1,000 views.*

## What I could not measure
- Audio: music, sound effects, loudness and voice tone; whether reactions are loud. Captions give the speech timing only.
- Exact cut timing below about 1 s (the storyboard rate) and small on-screen text.
- Real retention and swipe-away rates (private to channel owners). Heatmaps are relative, exist only for Shorts with about 80K views or more, and their meaning for looping Shorts is not documented.
- Thumbnails and the title's effect on the Shorts feed (Shorts are mostly served without the title being read first).
- Kick, Loco and Instagram Reels versions; Reels numbers were not collected. Everything here is YouTube Shorts.
- Causation: all comparisons are observational, and upload era, channel size and algorithm changes confound them.
