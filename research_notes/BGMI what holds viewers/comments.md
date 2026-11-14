# What viewers want, love and complain about: comments on six BGMI channels

Study of 14 Nov 2026 for Kaatclip. Source: YouTube comments only (text metadata via yt-dlp, top-sorted, up to 200
top-level comments per video, no replies), plus the videos' auto-captions and "most replayed" heatmaps. No video or
audio was downloaded. "(Inference)" marks reasoning beyond what was counted. All quotes are under 15 words, without
usernames, spelling as written.

**Sample.** 80 videos: 55 long, 25 Shorts. Per channel: @goblinbgmi 9 long + 3 Shorts, @goblinsh0rts 10 + 6,
@jokerclipss 11 + 4, @Jokerkihavelii 5 BGMI long + 5 Shorts, @LoLzZzGaming 10 + 1, @lolzzzplays 10 + 6. Mostly high-view
videos, plus 13 low-view ones for contrast (12K-98K). **9,593 top-level comments** were read by script; the top 5 of
each video (400 comments) were hand-coded; every comment that quotes a time (637 comments, 655 timestamps) was grouped
into **393 moments** (mentions within 6 s of each other) and each moment was hand-labelled using the comment text and the
Hindi auto-captions at that time (captions were available for 70 of the 80 videos). Raw data and scripts:
`C:\Users\soura\AppData\Local\Temp\claude\21027423ba80eb72\c7886632-c6c6-4a95-81c6-c6cbac2a769e\scratchpad\viewers\comments\`
(`raw\*.info.json` = metadata + comments, `ts_labeled.json` = labelled moments, `top5.txt`, `labels1.txt`, `labels2.txt`)
and `...\viewers\scripts_comments\`.

---

## 1. One-screen summary

1. **Viewers timestamp talk more than kills.** Of 393 moments viewers pointed to by time, **51% are talk or people**
   (a funny line 25%, banter between players 16%, a named person's entry or presence 6%), **17% are gameplay skill**
   (kill bursts 14%, movement, clutches), 7% funny gameplay (fails, chases), 4% editor meme inserts, and only **2%
   results/dinners**. In 31 of 57 videos the single most-liked timestamp is a line or banter; in 11 it is a kill.
2. **But skill moments get the biggest likes when they land.** Skill moments are 17% of moments but **35% of all
   timestamp likes**; on Goblin's main channel they are 45% of moments and 72% of likes. What viewers praise in a kill is
   *how* he went in: "confidence", "movement", "drop shot", "reflex", "aim switch", not the kill count.
3. **The ending is the most-quoted part.** The last third of long videos holds **47% of timestamp likes** (first third
   29%, middle 23%). The last 60 s holds 51 of 393 moments and 21% of likes, mostly funny lines and the after-fight
   talk. Three of the top-12 moments sit in the final 26 s of their video (9:58 of 10:24, 8:20 of 8:29, 15:02 of 15:23).
4. **Lines said after a fight are what people repeat.** The most-liked comments quote dialogue: "Joker : Damage diya
   na re maine 😅 Goblin : ha ek 1 hp the sare" (1,500 likes), "8:20 Legit: Or Kidhar Hai?? Joker : Lobby Mein"
   (351). A teammate's catchphrase ("Badhiya, badhiya") made viewers rewrite the title (4 comments, 353 likes together).
5. **Top comments are viewer jokes, people and status, almost never requests or complaints.** Hand-coding the top 5 per
   video: viewer jokes/memes 17% of comments but **32% of their likes**, another person 16%, a specific moment 11%,
   team/fan cheering 11%, the creator's skill/status 10%, quoting a line 9%, the editor 4.5%, requests 3.5%.
6. **Requests for "full match / part 2 / uncut" are rare**: 13 + 2 comments out of 9,589 (0.16%). Complaints about
   music (5), cuts (0), length (0) or clickbait (0) are near zero. The common "complaint" is a **missing moment that live
   viewers remember** ("Legends know why erangel match clip ended at 2;32"; "Bathroom wala scene missing hai"), 8
   comments, and viewers love it when the editor keeps the blooper ("17:07 Lolzzz be like :- ye nahi dalna tha", 87).
7. **Highlight viewers are often the live audience coming back.** 77 comments say they watched it live ("Live Dekhne ka
   ghamand hai", 401 likes), 56 of them on LoLzZz's main channel. They know the stream's famous moments and notice when
   one is cut.
8. **Low-view videos give viewers nothing to talk about.** On long videos under 150K views, comments are twice as often
   team cheering (8.1% vs 4.3%) and less than half as often quote a line (1.5% vs 3.6%) as on videos over 300K. A 39K
   tournament WWCD cut got 18 comments, none about anything in the video.
9. **Shorts comments quote a line or a reaction, not a time.** Shorts got 7 timestamps in 2,972 comments; 27% of their
   top comments are viewer jokes and 11% quote the line said ("Bro be like:- ja puchke aa", 780). Kill-only tournament
   Shorts drew 12-59 comments of cheering.
10. **Game sound is loved, music under gameplay is the one sound complaint.** "That ting ting sound is permanent"
    (516 likes), "1:56 satisfying sound ting ting" (19); two comments complain about background music over gameplay.
11. **Editor praise exists only where the editor adds jokes.** 146 comments mention the editor, edit or thumbnail; most
    are on LoLzZz videos (editor "Ryloz": "Editor is insane", 501) and praise meme timing ("Meme ki timing ek dum badiya
    the", 67). Editor meme inserts are 4% of moments but 67% of them sit in the video's top replay quartile.
12. **Comments are written in Roman script**: 0.4% use Devanagari; the rest is Roman Hinglish, English and emoji
    (9% emoji only). Subtitles and titles for this audience should be Roman Hinglish.

---

## 2. Evidence by question

### Q1. Which moments do viewers quote by timestamp? (counts by type and channel)

#### Takeaway
Half the timestamped moments are talk (lines, banter, people), and on comedy channels two thirds or more; kills dominate
only on Goblin's main channel. Skill moments earn outsized likes; results and dinners are almost never quoted.

#### Cited findings
- **Moments by label (393 moments, 655 mentions, 13,371 likes on those comments):**

  | Moment type | Moments | % | Comments | Likes % |
  |---|---|---|---|---|
  | Funny line (creator or teammate says something funny) | 100 | 25.4 | 157 | 16.9 |
  | Banter (exchange between players, rival taunts) | 63 | 16.0 | 136 | 24.1 |
  | Kill / kill burst / spray / drop shot | 55 | 14.0 | 88 | 29.0 |
  | Funny gameplay (fail, chase, odd death) | 29 | 7.4 | 46 | 4.7 |
  | A named person (entry, presence) | 25 | 6.4 | 36 | 4.1 |
  | Editor meme insert | 14 (+1 edit) | 3.8 | 39 | 4.1 |
  | Movement / game-sense call / clutch | 13 | 3.3 | 19 | 5.8 |
  | Result screen / dinner / record reached | 7 | 1.8 | 13 | 3.1 |
  | Wholesome moment | 6 | 1.5 | 10 | 3.1 |
  | Reaction face | 5 | 1.3 | 5 | 0.1 |
  | Intro | 5 | 1.3 | 6 | 1.4 |
  | Other (questions, song names, spam, off-topic) | 71 | 18.1 | 100 | 3.7 |

- **By channel (moments):**

  | Type | @goblinbgmi | @goblinsh0rts | @jokerclipss | @Jokerkihavelii | @LoLzZzGaming | @lolzzzplays |
  |---|---|---|---|---|---|---|
  | Kill | 17 | 11 | 7 | 1 | 17 | 2 |
  | Clutch / movement / game sense | 4 | 4 | 2 | 1 | 1 | 1 |
  | Funny line | 4 | 13 | 38 | 16 | 17 | 12 |
  | Banter | 8 | 13 | 14 | 3 | 11 | 14 |
  | Person | 2 | 2 | 5 | 1 | 6 | 9 |
  | Wholesome / reaction | 1 | 0 | 8 | 1 | 1 | 0 |
  | Funny gameplay | 4 | 3 | 9 | 2 | 7 | 4 |
  | Meme insert | 0 | 0 | 0 | 3 | 9 | 2 |
  | Result / dinner | 0 | 2 | 0 | 0 | 4 | 1 |
  | Intro | 1 | 0 | 0 | 0 | 4 | 0 |
  | Other | 5 | 5 | 14 | 1 | 33 | 13 |
  | Videos with timestamps | 10 | 8 | 13 | 6 | 10 | 10 |

  Share of moments / share of likes by group: @goblinbgmi skill 45% / 72%, talk 32% / 19%; @goblinsh0rts talk 52% /
  53%, skill 28% / 36%; @jokerclipss talk 67% / 84%; @Jokerkihavelii talk 72% / 76%, meme inserts 10% / 12%;
  @LoLzZzGaming talk 31% / 29%, skill 16% / 39%, meme 8% / 10%; @lolzzzplays talk 60% / 69%, funny gameplay 6% / 14%.
- **Most-liked timestamp per video (57 videos):** funny line 15, banter 12, kill 8, funny gameplay 5, person 3, meme
  insert 2, game-sense call, movement, clutch, wholesome, result, intro 1 each, other 6.
- **The top moments** (likes summed over comments in the moment):
  - 869: kill, [67w15TWdikI](https://www.youtube.com/watch?v=67w15TWdikI) at 9:58 of 10:24: "Bhai itna confidence lata
    kaha se h" (the solo push into a squad).
  - 669: kill, [5GNFp6GqCso](https://www.youtube.com/watch?v=5GNFp6GqCso) 6:55: "hacker or watt 💀🥴" (Jonathan's kill).
  - 447: funny line, [W9C_0b5q--M](https://www.youtube.com/watch?v=W9C_0b5q--M) 3:13: "Joker bahi spitting facts".
  - 445: banter, [xiqm0RdJR3o](https://www.youtube.com/watch?v=xiqm0RdJR3o) 8:20 of 8:29: "Legit: Or Kidhar Hai?? Joker :
    Lobby Mein".
  - 428: kill, same video 2:25: "confidence bro".
  - 344: banter, [uRE9t_73aVk](https://www.youtube.com/watch?v=uRE9t_73aVk) 0:41: "Iska alag hi hai" (about Aman).
  - 277: movement, [C76kBoyodHY](https://www.youtube.com/watch?v=C76kBoyodHY) 8:45: "uff that movement by godlin".
  - 241: wholesome, [C1kM4225P6Y](https://www.youtube.com/watch?v=C1kM4225P6Y) 5:30: "For reall pyaar toh hai".
  - 230: banter, [PtvEiSN48Dk](https://www.youtube.com/watch?v=PtvEiSN48Dk) 17:10: "kya troll kiya lolzz ne jonny ko".
  - 211: kill (grenade), 5GNFp6GqCso 2:15: "was epic".
  - 203: meme insert, 5GNFp6GqCso 3:13: "Telugu meme😂😂😂".
  - 202: result, [C1RNs4p8uJg](https://www.youtube.com/watch?v=C1RNs4p8uJg) 15:02 of 15:23: the 8,300-damage record
    reached, with his celebration.
- **The words viewers use on kill moments** describe the approach and the hands: "confidence" (two of the top five),
  "movement", "ghost peaks", "drop shot" (3 moments), "reflex" (3), "aim switch", "spray", "game sense call", "Show some
  mercy Gobu". None quotes a kill number. — comments on 67w15TWdikI, xiqm0RdJR3o, C76kBoyodHY, [qy_BVesBY_M](https://www.youtube.com/watch?v=qy_BVesBY_M), [aA98jrFkEPQ](https://www.youtube.com/watch?v=aA98jrFkEPQ)
- **Funny lines are often the reply or reaction after a fight**: the captions at the 8:20 moment show Legit asking where
  the last enemy is and Joker answering "lobby mein" after the round is won; at [7TkLt-j3u4A](https://www.youtube.com/watch?v=7TkLt-j3u4A) 12:54 (best-liked moment of that video, and its heatmap peak at 12:58) the line "pagla gaya vo" follows a fight; at [yincpYxqIrI](https://www.youtube.com/watch?v=yincpYxqIrI) 7:49 ("gotem ne punk phaad diya", 115 likes) the caption shows Nakul's line right after a teammate's kill.
- **Endings and openings.** Last third of long videos: 135 moments and 47% of timestamp likes (6,321 of 13,303); first
  third 133 moments, 29%; middle 119, 23%. Final 60 s: 51 moments, 2,844 likes (21%): 17 funny lines, 7 banter, 6 kills,
  4 results. First 30 s: 20 moments, 4 of them about the intro ("0:20 clean intro 🥵", 177, [MQ8SC-_e8ZQ](https://www.youtube.com/watch?v=MQ8SC-_e8ZQ)).
- **Timestamps agree with the replay curve.** On the 47 long videos with a heatmap, the timestamped moments sit at the
  **74th percentile** of their own video's replay curve (median); 49% are in its top quartile. By type: skill 84th
  percentile (57% top quartile), funny gameplay 83rd (63%), meme inserts 78th (67%), talk 74th (50%), other 59th (32%).
  The video's single highest replay peak had a timestamped moment within about 10 s in **26 of 47** videos.

#### Inferences
- (Inference) A ranker that scores only kills, kill bursts and loudness would miss the moments viewers name most often
  (lines and banter) and would mis-order the comedy channels completely. Talk moments and skill moments need separate
  scores, both high.
- (Inference) "Confidence" moments are the run-in: the decision to push and the first shots. The fight's approach must
  be kept, not just the frames around the kill feed.

#### Gaps
- Storyboard frames were not used to map moments; mapping used captions (70 videos) and the comment text. For 10 videos
  without captions the label rests on the comment text alone.
- Labels are one coder's; boundaries between "funny line" and "banter" are soft.
- Timestamps come from the most commented long videos; low-view videos had few or none.

### Q2. What do the comments say? (praise, editing, requests, complaints, people, laughter)

#### Takeaway
The top of the comment section is jokes about the situation, people (teammates, rivals) and the creator's status.
Requests and complaints are a few percent and mostly about people and content, not about the edit. The "complaint" that
matters for an editor is a missing moment the live audience remembers.

#### Cited findings
- **Hand-coded top 5 comments of all 80 videos (400 comments):** viewer joke/meme 16.8% (32.3% of the likes), another
  person (teammate, rival, co-star) 16.2% (15.4%), specific moment 11.2% (4.7%), team or fan cheering 10.8% (4.4%),
  creator skill/status 10.2% (12.6%), quoting a line 9.0% (8.3%), other 8.5%, editor/edit/thumbnail 4.5% (3.6%),
  request 3.5% (1.1%), nostalgia/journey 2.5%, hacker banter 1.8%, pure laughter 1.8%, wholesome/personal 1.5%,
  BGMI-vs-Free-Fire debate 1.0% (4.9% of likes, one Short), creator's reaction 0.8%.
- **Whole set by pattern (9,589 non-uploader comments):** laughter emoji/words in 27.6% of long-video comments and 35% of
  Shorts comments; skill words in 14.7% / 11.7%; another named person in 15.5% / 9.8%; a timestamp in 11.8% / 0.7%.
  Comments mentioning someone other than the creator: @goblinbgmi 23%, @goblinsh0rts 24%, @jokerclipss 18%,
  @Jokerkihavelii 6%, @LoLzZzGaming 6%, @lolzzzplays 7%.
- **People named most:** on @goblinbgmi Neyo 92 comments, Akshat 69, Regaltos 58, Jonathan/Jonny 82, Omega 38;
  @goblinsh0rts Jonathan/Jonny 92, Rega 53, Joker 44, Neyo 39; @jokerclipss Scout 57, Snax 39, Goldy 36, Rega 19, Aman 17;
  LoLzZz channels Jonathan/Jonny 77, Mayur (T2), Fury, Manya, Aashi. — script counts over the 9,589 comments
- **Rivalry and status carry the most-liked comments:** "No Competition is liye Soul vs Soul ho rha hai" (4,300,
  [DfOcogRMngg](https://www.youtube.com/shorts/DfOcogRMngg)); "Legends join soul after clutching them" (2,200,
  [iF7cZNBIGKc](https://www.youtube.com/shorts/iF7cZNBIGKc)); "Aab stream sniper bolke dikha de" (2,000,
  [f-mCo5PbnlM](https://www.youtube.com/watch?v=f-mCo5PbnlM)); "In the ERA of DBS there is a player dominating with his
  AKM" (2,800, 67w15TWdikI); "3 bar Jonny pel diya aaj gobu ne" (627, [TVZ2RLVXD7E](https://www.youtube.com/shorts/TVZ2RLVXD7E)).
- **Quoted lines:** 247 comments use a quote pattern ("be like", "X:-", "said"), 87 of them on @goblinbgmi. Examples:
  "Le Akshat after Goblin's every kill : Badhiya , badhiya , badhiya" (619, qy_BVesBY_M); "Omega- Aage mat jana,
  Goblin- Thik hai" then he pushed solo (506, aA98jrFkEPQ); "Maasum sa chehra" (756, [zC2CyyUHKG0](https://www.youtube.com/shorts/zC2CyyUHKG0)).
- **Viewers retitle videos after a person's catchphrase:** "The title should be 6 minutes of Akshat saying BADHIYAAA"
  (298) and three more variants (55) on qy_BVesBY_M ("Carrying @AkshaTxBGMI in TDM battle", 440K).
- **Editor and editing:** 146 comments. Concentrated on LoLzZz videos: "Editor is insane" (501) and "Respect for
  Raylozzz editing" (333) on PtvEiSN48Dk; "Ryloz in BGMI 🤡 Ryloz at editing 💀" (290, [RsiHZgsCMtw](https://www.youtube.com/watch?v=RsiHZgsCMtw)); "Editor knows how to cook well" (61, [lOAtTbOsCzQ](https://www.youtube.com/watch?v=lOAtTbOsCzQ)); on JokerClips "Editor OP . Meme ki timing ek dum badiya the" (67, [sUexqXxy1mA](https://www.youtube.com/shorts/sUexqXxy1mA)). On Goblin's videos editing is rarely mentioned except a Short ("Editor dange kravyega", 2,000, DfOcogRMngg) and a music complaint.
- **Requests (precise patterns):** full match/uncut 13 comments in 13 videos (e.g. "full gameplay kaha hai?" on Short
  [iVF6tpnxnfA](https://www.youtube.com/shorts/iVF6tpnxnfA); "pls put full video of scrims"; "Bhai wo 29 kills wala video dalo
  na last tk bilkul"; "omega ne jo daala vo unedited daalna shorts me"); part 2/3: 2; a collab or matchup with a named
  person: 35 (e.g. "Snax x Joker content please", "Jona se 1v1 karo"); song/music name: 28 (13 on LoLzZz main);
  settings/device/handcam: 83 (43 on @goblinsh0rts, mostly one viewer repeating "layout 1 pr wapas shift kr"); "more like
  this / series / upload regular": 16 ("Loved this tdm contest We request more like this", 150, [L6AEilrZnX8](https://www.youtube.com/watch?v=L6AEilrZnX8); "Need more this type of videos with other t1 players", 149, C76kBoyodHY; "Joker bhai please upload regular and long videos i can't watch streams", 23, [3ZtzS5VrEOg](https://www.youtube.com/watch?v=3ZtzS5VrEOg)); "Chained together ke highlights dalo" (119, uRE9t_73aVk).
- **Complaints (precise patterns):** music over gameplay 2 real ones: "Bhai yeh music gameplay mein accha nhi lgta" (9,
  [9pG_cQv0-oA](https://www.youtube.com/watch?v=9pG_cQv0-oA)); "Editor bhai baar baar same background music disturb kr
  rha" (3, MQ8SC-_e8ZQ). Too short or too many cuts: 0. Clickbait: 0 (one praises the opposite: "click bait to nhi kiya
  kamsekam"). Boring/cringe: 9, scattered. Missing moment: "Legends know why erangel match clip ended at 2;32 and not the
  end" (33, aA98jrFkEPQ), "First match ka jo rush kar k mara hai wo kat diya hai" (aA98jrFkEPQ), "wo balcony ya window …
  wala knock nhi dala" (7, MQ8SC-_e8ZQ), "Bathroom wala scene missing hai" (13, [fCCQkW1Uevk](https://www.youtube.com/watch?v=fCCQkW1Uevk)), "Pura clip nhi dale ho bhai 6:26" ([8Au8-kSBhgg](https://www.youtube.com/watch?v=8Au8-kSBhgg)), "legends know that he naded himself after that clutch" (7, [Css0AXuRBZQ](https://www.youtube.com/shorts/Css0AXuRBZQ)), "bro edited out every instance of johnny calling him LULLIIIIII" ([3jfUBJ-Ihbs](https://www.youtube.com/watch?v=3jfUBJ-Ihbs)), and on a Short that stops right after the 1v3: "ek baar kya 1v3 maar diyaa isne to reel hi kaat dii" (188, TVZ2RLVXD7E).
- **Bloopers kept are loved:** "17:07 Lolzzz be like :- ye nahi dalna tha" (87, [9tOJ5bdmkWE](https://www.youtube.com/watch?v=9tOJ5bdmkWE)); this moment is the video's top replay peak (1027 s).
- **Live audience:** 77 comments say they saw it live, 56 on @LoLzZzGaming: "Live Dekhne ka ghamand hai" (401,
  [z1jXPJN8z-c](https://www.youtube.com/watch?v=z1jXPJN8z-c)), "I got goosebumps on live" (125, 67w15TWdikI), "Raat ko
  dekha live Fir bhi dobara dekh raha Hu" (37, [GI59p_ZSYik](https://www.youtube.com/watch?v=GI59p_ZSYik)). One asks for faster uploads: "Video Edit karke itna late koro ki Audience already Live Pe jakar he dekh le" ([xuag6MDiNI0](https://www.youtube.com/watch?v=xuag6MDiNI0)).
- **Hacker banter is praise:** 111 comments use hack/hacker/ESP/aimbot near a person; on LoLzZz "classic hacker" is a
  fan nickname (48 comments). "The biggest disrespect for hacker" is the top comment (7,000) on Joker's 7.7M Short
  [_RgXLRs1wx8](https://www.youtube.com/shorts/_RgXLRs1wx8). Real accusations exist but are a minority.
- **Nostalgia and old teams:** 38 comments ("Pure nostalgia 🥹", 129, and "Old times when scout raid jokerrr", 355, on
  [2aHwYxucN24](https://www.youtube.com/watch?v=2aHwYxucN24); "Rega in his prime", 350, 7TkLt-j3u4A).
- **Sound:** "That ting ting sound is permanent 💀💀" (516, C76kBoyodHY), "1:56 satisfying sound ting ting" (19,
  xiqm0RdJR3o); "Patt se headshot!" voice line quoted twice at 15:02 and 17:12 on PtvEiSN48Dk (82).
- **Language:** 0.4% of comments contain Devanagari; 37% match a short Hinglish word list, 54% other Roman text, 9%
  emoji only.

#### Inferences
- (Inference) For an automatic editor the useful complaint is "a moment I saw live is missing", not pacing. Stream
  moments that made the live chat explode are the ones the returning audience checks for.
- (Inference) Cutting immediately after a clutch, before the aftermath, reads as hiding something; viewers joke about it.
- (Inference) The requests Kaatclip can serve from one recording: an extended or uncut cut of a match, a Short of a
  specific moment, segments from other games in the same stream (Chained Together), song credit and settings in the
  description.

#### Gaps
- Top-sorted comments over-represent early and popular comments; complaints may sit lower in the list. Only 200 per
  video were read, and replies were excluded.
- Pattern counts miss misspellings; the hand-coded top-5 set is the more reliable view.

### Q3. High-view vs low-view, Shorts vs long, main vs second channel

#### Takeaway
High-view videos give viewers a line, a person or a status moment to joke about; low-view ones get cheering and
"first". Shorts get jokes and quoted lines, long videos get timestamps. Each creator's main channel draws status and
skill talk (Goblin) or live-audience pride (LoLzZz); the second channel draws people and banter.

#### Cited findings
- **Long videos ≥300K vs <150K (rates per comment, averaged per video):** laughter 30.6% vs 26.8%, skill words 16.3% vs
  12.2%, quoting a line 3.6% vs 1.5%, team/fan cheering 4.3% vs 8.1%, "watched live" 1.0% vs 0.2%, timestamps 12.0% vs
  13.3%, another person 15.1% vs 13.7% (24 vs 10 videos with ≥15 comments).
- **Hand-coded top 5, videos ≥300K vs below:** jokes 21% vs 11%, people 16% vs 15%, skill/status 10% vs 10%, moments 10%
  vs 12%, quotes 9% vs 8%, cheering 5% vs 16%.
- **Low-view examples:** [xtE3WWqt1_E](https://www.youtube.com/watch?v=xtE3WWqt1_E) (BMSD domination, 39K, 18 comments): top
  comment "As A Tag Fan 😅 I am Shocked How Soul Reached # 1", nothing about a moment. [j6kf-4MXXDc](https://www.youtube.com/watch?v=j6kf-4MXXDc) (58K, 10 comments): all five are tournament wishes. Crate video [2GJtTk-s_94](https://www.youtube.com/watch?v=2GJtTk-s_94) (14K, 11 comments): "First comment". WWCD Short [Wl187oS_j9I](https://www.youtube.com/shorts/Wl187oS_j9I) (16K, 12 comments): cheering only.
- **Same moment, two uploads:** "Goblin quick 1v3 TAG" [TVZ2RLVXD7E](https://www.youtube.com/shorts/TVZ2RLVXD7E) (22 s,
  583K, 200+ comments of rivalry jokes) vs "Goblin Quick 1v3 TAG in BGMS" [kAuHGN3hG1I](https://www.youtube.com/shorts/kAuHGN3hG1I)
  (38 s, uploaded a day earlier, 12.5K, 59 comments). One comment on the weaker one asks for more: "dangerous player wala
  interview b ajata toh last may maza ajata" (14). (Inference: views here are mostly decided by distribution, not by
  comments; the pair only shows that the shorter cut got the reach.)
- **Shorts vs long:** timestamps 0.7% vs 11.8% of comments (7 vs 630). Shorts top-5 codes: jokes 27%, people 16%, quotes
  11%, skill 10%, other 9%; long: people 16%, moments 15%, cheering 13%, jokes 12%, skill 10%, quotes 8%. Shorts
  comments quote the clip's line or reaction: "I can hear his laugh !!" (1,200, [CdkN90FTUl8](https://www.youtube.com/shorts/CdkN90FTUl8)); "Joker : Damage diya na re maine…" (1,500, iVF6tpnxnfA); "Bro be like:- ja puchke aa" (780, [qxX7OBsUino](https://www.youtube.com/shorts/qxX7OBsUino)); "My enemy - nade Lolz enemy - rush" (1,800, [UhUauBjjrn8](https://www.youtube.com/shorts/UhUauBjjrn8)).
- **Goblin, main vs second:** main long videos: skill words in 29.9% of comments (second channel 15.9%), top-5 codes
  skill/status 21%; timestamped moments 45% skill with 72% of likes; one funny challenge stream cut ([gs8thi_U_fU](https://www.youtube.com/watch?v=gs8thi_U_fU)) has 55% laughter. Second channel: other people in 24% of comments, top-5 codes people 23% and fan cheering 22%, timestamped moments 52% talk; the WOW-mode customs collect the banter quotes (xiqm0RdJR3o, 29 timestamped comments).
- **Joker, main vs JokerClips:** both laugh-led (45% and 41% of long-video comments); timestamped moments 72% vs 67% talk;
  main-channel BGMI highlights draw few comments for their views (23-52 comments on 147K-337K) and their top comments ask
  for the old duo ("Snax and joker duo I want it's my order", 45, [TIDXJ1YeirM](https://www.youtube.com/watch?v=TIDXJ1YeirM)). JokerClips has the wholesome and personal comments ("mai pichale 1 mahine se hospital mai hu…", 303, C1kM4225P6Y).
- **LoLzZz, main vs plays:** main: "watched live" 2.7% of comments, editor mentions 3.5%, record and status talk, 33
  "other" moments (song names, "live dekhne ka ghamand"), skill moments 39% of likes. Plays: fan cheering 13.1% ("TAG ON
  TOP 🖤"), rival taunts against a streamer opponent (f-mCo5PbnlM: 38 timestamped comments, the most in the sample), 60% of
  moments talk.

#### Inferences
- (Inference) What separates a high-view highlight in the comments is a quotable thing: a line, a person's reaction, a
  rivalry beat. A video that is only "we won" gives fans nothing to repeat.
- (Inference) For Goblin-style esports cuts the skill moment is the product; for Joker-style cuts the line is; LoLzZz
  sits between and adds editor jokes. One ranking weight for all three would be wrong.

#### Gaps
- View counts were not controlled for age, subscriber base or Shorts distribution; the comparison shows what comments
  contain, not why a video got views.
- Only 13 low-view videos were sampled, several with under 20 comments.

---

## 3. Rules for an automatic editor and for titles

Each rule cites the evidence above. Numbers are proposals for Kaatclip to test, not measured editor settings.

**Moments that must never be cut**
1. **Keep the talk after a fight.** A fight segment ends no earlier than the end of the first sentence spoken after the
   last kill or knock, plus 1.5 s, capped at 20 s past the last shot. Evidence: the most-liked quoted lines are after-
   fight replies (8:20 "Lobby mein", "Damage diya na re maine", "pagla gaya vo" at the 7TkLt-j3u4A heatmap peak).
2. **Keep the run-in before the kill.** Start a fight segment at the call or the first movement toward the enemy, not
   at the first kill; viewers praise "confidence", "movement", "drop shot" (top-2 and top-5 moments).
3. **Rank talk as high as kills.** Score each speech moment (laughter in the voice, a teammate's reply within 3 s, a
   named person speaking, repeated phrase) on the same scale as kill bursts; on comedy streams talk should fill at least
   half the cut. Evidence: 51% of quoted moments are talk; most-liked timestamp is talk in 31 of 57 videos.
4. **Keep the aftermath of a clutch or record**, 5-10 s, even if it is a fail or a blooper. Evidence: "ye nahi dalna
   tha" kept at 17:07 is the top replay peak of 9tOJ5bdmkWE; cut-off endings get mocked ("reel hi kaat dii", "Legends
   know why … ended at 2;32").
5. **Keep the moments the live chat reacted to.** When a chat log or Kick clip list is available, any moment with a chat
   spike or a viewer-made clip is forced into the cut. Evidence: returning live viewers (77 comments) notice missing
   scenes (8 comments).
6. **Keep the ending, and make it a line, not a results screen.** End the video on the last laugh or the post-match talk;
   hold at least 5 s after it. Evidence: final third = 47% of timestamp likes; final 60 s = 21%; results/dinner are only
   1.8% of quoted moments.

**What to open with**
7. **Open with the best quoted-type moment of that stream**: for esports streams the hardest push/kill with its call; for
   comedy streams the best line with its reply. Keep it under 15 s and make sure the same moment appears again in full
   later. Evidence: skill moments sit at the 84th replay percentile, talk at the 74th; viewers note a "clean intro"
   (177 likes) but rarely quote the first 30 s (20 of 393 moments).

**Sound, captions, effects**
8. **Game sound stays audible; no music bed under fights or speech.** Music only in a teaser or a gap with no speech and
   no shooting. Evidence: "ting ting sound is permanent" (516); the only sound complaints are about background music over
   gameplay.
9. **Captions in Roman Hinglish**, on the line that is the joke (and in Shorts on every line). Evidence: 0.4% of comments
   use Devanagari; viewers retype the line itself ("Badhiya, badhiya").
10. **Effects only on the line or reaction, never on the kill feed.** Optional meme stings or punch-ins at a punchline;
    none on kills. Evidence: editor meme inserts are 67% in the top replay quartile and draw editor praise when timed to
    the joke ("Meme ki timing ek dum badiya"); no comment praises a kill zoom.

**Shorts**
11. **A Short must contain a spoken line or a visible reaction, and should end on it.** A kill-only Short needs a
    rivalry or status hook (a named rival, a 1vN against a known team). Evidence: Shorts comments quote lines and
    reactions (1,200-1,800-like comments); kill-only tournament Shorts drew 12-59 cheering comments.
12. **Do not stop a Short on the kill frame**; let the reaction or next line play out (2-5 s). Evidence: "reel hi kaat
    dii" (188).

**Titles and packaging**
13. **Name the person and quote the phrase.** Default title pattern: "{teammate} saying '{catchphrase}'" or "{creator} vs
    {rival}" when ASR finds a repeated phrase or a named opponent; the kill number goes second. Evidence: viewers retitled
    qy_BVesBY_M after Akshat's "Badhiya" (4 comments, 353 likes); rivalry/status comments carry the top likes.
14. **No result-only titles for low-stakes matches.** "WWCD moment" videos drew cheering only (Wl187oS_j9I 16K,
    xtE3WWqt1_E 39K).

**What viewers ask for that Kaatclip can give from one stream recording**
15. **An extended cut** of a match or custom room (whole fights, all talk kept) alongside the short highlight; small but
    explicit demand ("full gameplay kaha hai?", "29 kills wala video dalo na last tk bilkul", "unedited daalna shorts me").
16. **Segment videos from non-BGMI parts of the stream** (Chained Together, Meccha Chameleon) when the creator wants them
    ("Chained together ke highlights dalo", 119).
17. **Description template with song credit and settings** (28 song-name and 83 settings/device questions).
18. **Speed**: a first highlight within hours of the stream, while the live audience is still talking about it (one
    explicit complaint about late uploads; 77 "watched live" comments).

---

## 4. What could not be measured

- **No audio was heard.** "Funny line" labels rest on comment text and auto-captions; tone, laughter volume and music
  levels in the videos are unknown.
- **Storyboard frames were not used** for the timestamp mapping; I did not check what is on screen at each moment.
  Captions were missing for 10 videos (auto-captions not offered or HTTP 429 on retry).
- **Comment samples are top-sorted and capped at 200 top-level comments**, replies excluded; yt-dlp overwrote the
  comment_count field with the number fetched, so total comment counts were not re-measured here.
- **Single coder.** Moment labels and top-5 codes were assigned by one reader; no inter-rater check.
- **Views are a one-day snapshot** and are not adjusted for upload age, channel size or Shorts distribution, so the
  high-vs-low comparison shows what comments contain, not causes.
- **Heatmaps** exist only for videos YouTube shows them on (47 of 55 long videos here); the 100-point curve is about
  5-15 s per point on these lengths, so "within 10 s" matches are approximate.
