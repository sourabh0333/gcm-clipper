# How the editors cut and time things, frame by frame (Chrome, 14 Nov 2026)

Method: 15 new videos were opened in Chrome (sound muted the whole time, ads waited out or skipped), paused at
1080p (720p for two), and frames were drawn onto contact sheets at 0.125-2 s steps with the time written on each
frame. Moments were chosen from YouTube's "most replayed" heatmap (from saved metadata) and from the start and
end of each video. Speech timing comes from YouTube auto-captions (word-level times, about ±0.2 s). Nothing was
downloaded. Sheets and scripts: `scratchpad\viewers\frames\` (helper.js, scan.py, vtt.py, subs\).
This builds on `research_notes\BGMI creators content A to Z\editing_timing_watched.md` (3 videos: wDgeZBn80VM,
Kobcv7gzuAY, HhcQY2wm8Ug), so 18 videos have now been measured this way.

Videos studied (views from saved metadata):

| Channel | Long | Short |
|---|---|---|
| Goblin main | [67w15TWdikI](https://www.youtube.com/watch?v=67w15TWdikI) Sanhok Domination, 624 s, 604K; [aA98jrFkEPQ](https://www.youtube.com/watch?v=aA98jrFkEPQ) BGMS comeback, 521 s, 540K | [-vbAZpx5Iek](https://www.youtube.com/watch?v=-vbAZpx5Iek) "Why you Camp bro", 25 s, 1.04M (landscape) |
| GoBLiN shorts | [-ieo36Gj9Hk](https://www.youtube.com/watch?v=-ieo36Gj9Hk) Solo 9 Finishes WWCD?, 328 s, 225K | [DfOcogRMngg](https://www.youtube.com/watch?v=DfOcogRMngg) "Revenge", 36 s, 4.52M |
| Joker main | (streams only) | [CVqRiZ-wwNw](https://www.youtube.com/watch?v=CVqRiZ-wwNw) 1v4 Stream Snipers, 27 s, 536K; [NqUcnKv-mos](https://www.youtube.com/watch?v=NqUcnKv-mos) 1v3, 15 s, 383K |
| JokerClips | [tt1gwGtxjlU](https://www.youtube.com/watch?v=tt1gwGtxjlU) Jonathan raids Joker, 402 s, 1.42M; [1bSJjsh33kM](https://www.youtube.com/watch?v=1bSJjsh33kM) watch-party commentary, 567 s, 208K | [bmoICLbNemI](https://www.youtube.com/watch?v=bmoICLbNemI) BGMI vs Free Fire Player, 23 s, 2.22M |
| LoLzZz main | [PRaUeGY8Sr8](https://www.youtube.com/watch?v=PRaUeGY8Sr8) 94 squad kills record, 765 s, 853K; [5GNFp6GqCso](https://www.youtube.com/watch?v=5GNFp6GqCso) 2v2 TDM with Jonathan, 481 s, 847K | [Css0AXuRBZQ](https://www.youtube.com/watch?v=Css0AXuRBZQ) 1v4 DBS clutch, 40 s, 8.29M |
| lolzzzplays | [kOccoMYydwI](https://www.youtube.com/watch?v=kOccoMYydwI) 2v2 vs Admino & Godz, 918 s, 585K | [UhUauBjjrn8](https://www.youtube.com/watch?v=UhUauBjjrn8) Back to back clutch, 58 s, 1.09M |

---

## 1. Summary: what matters most

1. **No editor effect is ever put on a kill.** Across all 18 measured videos there are no zooms on kills, no slow
   motion, no replays, no freeze frames, no shakes and no flash frames added at a kill. Every fight that was sampled
   at 0.5 s or finer runs as one continuous take: 67w15TWdikI's final fight 589-612 s, aA98jrFkEPQ 419-435 s, the whole of
   Css0AXuRBZQ (0-40 s), NqUcnKv-mos (0-15 s), UhUauBjjrn8 (0-53 s), each clip of DfOcogRMngg. The bursts, flashes and blue
   glows seen at kills belong to the game: gun-skin kill effects, the blue zone, banners.
2. **Cuts sit between fights, never inside them.** The edges are hard cuts, a few black beats, one fade to black,
   and (LoLzZz only) a short whip or zoom-blur transition of 0.25-0.5 s when going from talk to gameplay.
3. **Effects are tied to words and reactions, not to gunfire.** The one measured face punch-in starts 0.1 s before the
   key word and ends 0.1 s after it ("A Gulrez", tt1gwGtxjlU 3.0-4.25 s, word 3.12-4.16 s). Face cutaways are 1.25-2.5 s long
   and land on a shout, a laugh or a line.
4. **LoLzZz cuts between cameras in duo and squad videos**: player POVs plus each player's face camera, with face
   reactions of 1.25-2.5 s between POVs. Sad or "dead" moments get the face in **black and white** (2.5-8 s), and the
   biggest heatmap peak of the record video is one of them (PRaUeGY8Sr8 260 s).
5. **Openings**: LoLzZz duo videos open on a ~20 s teaser that switches every 1-4 s between faces (talk) and POVs
   (action). Goblin main opens straight on gameplay or a 9.5 s broadcast clip. JokerClips opens on a full-screen face
   saying the hook line. Shorts open with shooting or the hook line already under way in the first frame.
6. **Short endings**: the last kill, then 1.0-1.5 s of the game, then a 1.25-3.5 s tail: a meme clip (a lion roar, laughing
   men), TV colour bars, or the face alone over a blur. Older raw Shorts simply end 1-2 s after the last kill.
7. **Long endings**: hold the result. A WWCD, defeat or record screen is held 5-24 s (scoreboard included); LoLzZz adds
   a 12 s face celebration. One Goblin second-channel video cuts away mid-final-fight to a 6 s black text card
   ("BHAROSA RAKHO CHICKEN AAGYA"), and its heatmap peaks (1.0) exactly there.
8. **Two clips are joined to tell a story with a black beat.** In DfOcogRMngg (4.5M) the death screen is held 1.25 s, then
   0.75 s of black, then the "revenge" clip.
9. **Labels are fixed, not timed.** A title band stays on the whole Short ("1v4 Clutch 😡", "BGMI vs FREE FIRE"). No
   subtitles or kill counters appear on any of the 15 new videos.
10. **Watch-party highlights add nothing.** In 1bSJjsh33kM the broadcast's own camera cuts carry it, and Joker's face cam
    stays small even while he screams (338-344 s).

## 2. The evidence, by question

### 2.1 Inside a fight: zooms, slow motion, replays, freeze frames, shakes

- Goblin main 67w15TWdikI, final fight and dinner, 589-624 s at 1 s steps: one continuous POV until the WWCD banner at
  613-615 s. No zoom, no slow motion. The heatmap peak is at 600 s (1.0).
- Goblin main aA98jrFkEPQ, heatmap peak 419-435 s at 0.5 s steps: scope in at 419-420, out at 420.5, in at 424 and at
  432. Every frame jump is the game's scope toggle; the HUD and position carry on.
- LoLzZz Css0AXuRBZQ (8.29M): 0-40 s at 1 s steps, one take of a stacked game and face recording; the map opens at 40 s,
  the end.
- Joker NqUcnKv-mos: 0-15 s at 0.5 s steps, one take; shots fired at 0.0, looting at 12-15.
- lolzzzplays UhUauBjjrn8: 0-53 s at 1 s steps, one take; the kill burst at 53.25 s is a gun-skin effect.
- Kill effects that look like edits but are the game: the purple burst at 137.5 s (5GNFp6GqCso), the green burst at
  417.5 s, the blue edge glow at 130-142 s in -ieo36Gj9Hk (that is the blue zone, which is how BGMI shows standing
  outside the zone).
- Counter-check: the 4 hit Shorts in this set (Css0AXuRBZQ 8.29M, DfOcogRMngg 4.52M, bmoICLbNemI 2.22M, UhUauBjjrn8 1.09M) use no
  kill zooms either.

### 2.2 How cuts are made and where they land

- **Hard cuts** are the default. Measured to 0.25 s, each switch happens between two consecutive frames with no
  dissolve: tt1gwGtxjlU 6.0→6.25 (face to stream screen), 15.25→15.5; 5GNFp6GqCso 129.5→129.75 and 131.0→131.25; CVqRiZ-wwNw
  24.0→24.25 (game to meme); DfOcogRMngg 32.25→32.5.
- **Fade to black, once**: 67w15TWdikI's broadcast cold open fades over about 0.75 s (brightness 97 at 9.25 s, 62 at 9.5,
  18 at 9.75, 0 at 10.0), holds full black 10.0-11.25 s, then hard-cuts to the POV at 11.5 s (brightness 0→114 in one step).
- **Black beat as a story joiner**: DfOcogRMngg holds the death screen 12.25-13.25 s, then black 13.5-14.0 s (0.75 s; hard cut in
  and out), then the "revenge" clip from 14.25 s (a different day: the shirt changes).
- **Whip and zoom-blur transitions** (LoLzZz only, when going into gameplay): kOccoMYydwI at 7.5 s, from the lobby line-up to
  the POV, is one blurred frame between 7.38 and 7.63 s (≤0.25 s, at 0.125 s steps). PRaUeGY8Sr8 at 86.0 s, from a face shot to
  a new attempt, is a motion blur ≤0.25-0.5 s (re-checked at 0.25 s steps).
- **A cut where the game would jump**: PRaUeGY8Sr8 hides a jump between two game moments under a 1.5 s face shot from
  another camera angle (41.0-42.5 s); the game resumes elsewhere at 42.75 s.
- **Cuts relative to speech** (JokerClips): tt1gwGtxjlU's face-to-stream cut at 6.25 s comes at the end of "...mera naam nahi
  likhta hoon" (last word ending 6.48 s); the next cut, at 15.5 s, falls 0.26 s before the next line starts ("momentum
  baith gaya", 15.76 s). Builds on the earlier finding that JokerClips cuts on the joke (Kobcv7gzuAY).
- **Cuts relative to kills** (LoLzZz duo): 5GNFp6GqCso switches from LoLzZz's POV to Jonathan's about 0.5 s after the kill
  burst (417.5 s burst, Jonathan's POV at 418.0 s). Showing the kill fully, then the other side.

### 2.3 Face punch-ins and face cutaways

- **Punch-in on the key word**: tt1gwGtxjlU 0-6 s is Jonathan's face full screen saying "Guys, write 'A Gulrez'". The frame
  jumps tighter at 3.0 s and back at 4.25 s, hard both ways. Caption words: "A" 2.72 s, "Gulrez" 3.12-4.16 s. So the
  punch-in starts about 0.1 s before the word and ends about 0.1 s after it; it lasts 1.25 s.
- **Reaction cutaways in duo videos** (5GNFp6GqCso): Jonathan's POV until 129.5 s, then his face camera 129.75-131.0 s (mouth
  open, shouting), then LoLzZz's POV from 131.25 s. Hard cuts, 1.25 s. Heatmap 130 s = 1.0.
- **Peak cluster** (kOccoMYydwI 517-535 s; heatmap 523 s = 1.0, 532 s = 0.87): the opponent's stream POV with his face
  (517-518.5 s, 2 s), LoLzZz's POV (519-525.5 s), the game's VICTORY banner (526.0 s), LoLzZz's face with his hand on his head
  (526.5-528.5 s, 2.5 s), the scoreboard (529.0-529.5 s, 1 s), POV (530-532 s), then **his face in black and white**
  (532.5-534.5 s, 2.5 s) as the caption "zero the kya kisi ke" begins (532.88 s; "kaun hai zero kill" at 529.52 s), then POV.
- **Black and white for despair**: PRaUeGY8Sr8 258.5-266.5 s shows a teammate's face cam in black and white for 8 s over "mere
  se nahi ho raha... neend... rehne dete, kal karte" (260.6-264 s). This is the video's heatmap maximum (260 s = 1.0). It
  follows 8 s of a failed-attempt scoreboard (250-258 s, "25 kill kam hai bhai" 253 s). The earlier GoBLiN shorts Short
  also put a teammate's reaction in black and white with a name label (HhcQY2wm8Ug 30 s).
- **Face-only endings on Shorts**: DfOcogRMngg switches at 32.5 s from game over face to the face alone, centred over a dark
  blur, for 3.5 s to the end.

### 2.4 Openings, the first 20 s

- **LoLzZz duo videos: a multi-camera teaser.** 5GNFp6GqCso 0-20 s: black 0-0.5; LoLzZz's face 0.5-3.0; Jonathan's face 3.5-7.5
  ("haath jodta"); LoLzZz's POV 8.0-9.0; Jonathan's POV 9.5-10.5; Jonathan's face laughing 11.0-13.5; Jonathan's POV
  14.0-15.5; LoLzZz's face 16.0-18.5; LoLzZz's POV 19.0 onward. Faces are held 2.5-4 s (while talking), POVs 1-2 s
  (action). kOccoMYydwI is the same: face 0.5-4.0, lobby line-up of the four players 4.5-7.0, zoom-blur 7.5, POV
  8.0-9.5, Jonathan's face 10.0, POV 10.5-11.5, face 12.0-15.0, POV 15.5-18.0, face 18.5-22.
- **LoLzZz record video: talking head first.** PRaUeGY8Sr8 opens on 33 s of LoLzZz explaining the record to camera ("welcome back
  to a brand new highlight ... 94 squad kills ... subah ke 6 baje"), ends on "let's go, enjoy karo" (32.6 s), and
  gameplay starts at 33.5 s.
- **Goblin main**: 67w15TWdikI opens on 9.5 s of broadcast spectator footage, the fade to black, then the POV at 11.5 s.
  aA98jrFkEPQ opens directly on the POV, driving a buggy into a compound; first contact at about 12-14 s. No text on
  either.
- **GoBLiN shorts long**: -ieo36Gj9Hk opens straight on the stream recording (overlay bar, face cam bottom right), driving
  for 11 s, then the first fight. Its captions are mostly "[संगीत]" (music), so it is a music-backed montage, unlike the
  talk-led stream cut wDgeZBn80VM.
- **JokerClips**: tt1gwGtxjlU opens on a full-screen face delivering the hook line (0-6.25 s, punch-in 3.0-4.25), then the
  raid on stream (6.25-15.25), then Joker's own camera (15.5 onward). Heatmap 4-12 s = 0.88-1.0.
- **Shorts open mid-action**: -vbAZpx5Iek has muzzle flash in the first frame; Css0AXuRBZQ's enemy is on the stairs at 0.0;
  NqUcnKv-mos fires at 0.0; CVqRiZ-wwNw starts on the line "Joker bhai suno" at 0.0 s; bmoICLbNemI on "bhai ek baat bataun"
  (0.16 s), over 2 s of game context before cutting to the face band at 2.5 s.

### 2.5 Short layouts and labels

- Stacked game over face cam: DfOcogRMngg (game ~60%, real camera ~40%), UhUauBjjrn8 (~55/45), Css0AXuRBZQ (~65/35).
- Three bands: CVqRiZ-wwNw (face strip ~20% on top, game in the middle with a fixed "1v4 Clutch 😡" label, a stream bar
  with "JOKER" at the bottom); NqUcnKv-mos (face on top, game, S8UL banner at the bottom).
- Face-only band with a title: bmoICLbNemI, the face centred on black with "BGMI vs FREE FIRE" above it from 2.5 s to 20 s.
- Old landscape Short: -vbAZpx5Iek is 1920x886, raw POV only, 1.04M views (2022).
- None of these Shorts had burned-in subtitles in the sampled frames.

### 2.6 Short endings, measured

- CVqRiZ-wwNw: final knock marker at 22.75 s, kill-feed lines at 23.0-23.25 s, POV to 24.0 s, **hard cut to a full-screen
  roaring-lion meme at 24.25 s** (1.0-1.25 s after the kill feed), held to 25.5 s (1.25-1.5 s), hard cut to black at 25.75
  s until the end (26.9 s).
- UhUauBjjrn8: final kill burst at 53.25 s, a different game shot over the same face camera 54.0-55.25 s (his hand over his
  mouth), then another person's face in close-up 55.5-57.75 s, **TV colour bars at 58.0 s** to the end (58.18 s). The
  GoBLiN shorts Short HhcQY2wm8Ug also used colour bars at the punchline.
- DfOcogRMngg: last kill about 32.25 s, the face alone over a blur 32.5-36.0 s (3.5 s).
- bmoICLbNemI: the acted punchline 15-20 s, then **laughing-men meme clips 20.5-22.5 s** (2 s) to the end.
- Raw older Shorts: Css0AXuRBZQ ends about 1-2 s after the last kill (map at 40 s); NqUcnKv-mos ends while looting, smiling.

### 2.7 Long endings, measured

- 67w15TWdikI: WWCD banner 613-615 s, the game carries on 616-621, scoreboard 622-624 s, end. That is 11 s after the WWCD.
- aA98jrFkEPQ: death or spectate 511-517 s, scoreboard 519-521 s, end.
- 5GNFp6GqCso (a loss): DEFEAT banner 474 s, DEFEAT scoreboard 475.5-480.5 s, end. A loss still ends on the result.
- PRaUeGY8Sr8: #1 at 696 s, WWCD medal 702, MVP 706-708, **scoreboard held 710-734 s (24 s, the record proof)**, LoLzZz's face
  celebrating 736-748 s (12 s), a record screen 750-752, scoreboard again 754-760, then 3 s of an end clip.
- -ieo36Gj9Hk: last gameplay frame at 322.0 s, mid-fight with a car incoming; **hard cut at 322.25 s to a black card with white
  text "BHAROSA RAKHO CHICKEN AAGYA"** ("trust me, the chicken came"), held to 328 s. The heatmap's maximum (1.0) is at
  322 s, the card itself. The title ends in "?". A withheld result works as a payoff that people rewatch or seek to.
- tt1gwGtxjlU: Joker's face full screen 392-401.9 s, talking; the video ends on his line.

### 2.8 What the heatmap peaks sit on (8 long videos)

- Final fight or WWCD: 67w15TWdikI 600 s; -ieo36Gj9Hk 322 s (the end card).
- A face reaction to a clutch: 5GNFp6GqCso 130 s (Jonathan's 1.25 s shout cutaway); kOccoMYydwI 523-542 s (the cluster of faces,
  black and white, opponent POV); 1bSJjsh33kM 341 s (the clutch on broadcast, then the team booth celebrating at 344-348 s).
- Despair or comedy: PRaUeGY8Sr8 260 s (the black-and-white teammate saying he can't go on).
- The hook: tt1gwGtxjlU 4-12 s.
- PRaUeGY8Sr8 84-100 s: a face shot (hands on head 83-85.75 s), the whip at 86.0 s, then a new drive into a fight. A YouTube
  mid-roll ad sat at about 86 s when watched (see section 4).

### 2.9 Watch-party format (JokerClips 1bSJjsh33kM)

- 0-20 s and both peaks (334-348 s, 486-493 s): only the broadcast's own observer cuts (1.5, 2.0, 4.5, 8.0, 13.0 and 17.5 s
  in the opening; a split screen at 341-343.5 s; the team booth at 344-348 s). Joker's face cam stays small at bottom
  left with his hands on his head (338-341 s) and is never enlarged. The scream ("No", 343.88 s) gets no effect.

## 3. Rules for an automatic editor (Kaatclip)

Each rule cites its evidence above.

**Fights and kills**
1. Never cut, zoom, slow down, replay or freeze inside a fight. Keep each fight as one take from its first shot (or the
   call before it) to at least 1.0-1.5 s after the last kill-feed line (2.1; 18 of 18 videos).
2. Do not add booms, shakes or flashes on kills. The game's kill effects and kill feed are the emphasis (2.1).
3. When cutting away after a kill, wait for the kill feed to show: cut no sooner than 0.5 s after the kill-burst or
   knock frame and 0.25 s after the kill-feed line appears (5GNFp6GqCso 417.5→418.0; CVqRiZ-wwNw feed 23.0, cut 24.25).

**Cuts between pieces**
4. Use hard cuts between pieces by default. Use a fade to black (about 0.75 s down, 1.0-1.5 s held, hard cut in) only
   once, after a cold open or broadcast intro, before the match proper (67w15TWdikI 9.25-11.5).
5. To join two clips that tell a story (death, then revenge; a fail, then a retry), hold the death or fail screen
   1.0-1.5 s, then 0.5-0.75 s of black, then the next clip (DfOcogRMngg 12.25-14.25).
6. Optional style (LoLzZz): one whip or zoom-blur of at most 0.25-0.5 s when going from talk, the lobby or a face shot into
   gameplay; never between two pieces of gameplay (kOccoMYydwI 7.5; PRaUeGY8Sr8 86.0).
7. Never cut in the middle of a sentence. Cut at the end of a line, or 0.2-0.5 s before the next line starts
   (tt1gwGtxjlU 6.25 and 15.5).

**Faces**
8. Face punch-in (tighter crop): only on a spoken key word or line; start 0.1-0.2 s before the word, end 0.1-0.3 s after
   the word ends; hard cut in and out; 1.0-1.5 s long (tt1gwGtxjlU 3.0-4.25).
9. Face cutaway (full-frame face or face-only layout): only on a shout, laugh or reaction line, 1.25-2.5 s, hard cuts,
   placed after the action it reacts to, not during shooting (5GNFp6GqCso 129.75-131.0; kOccoMYydwI 526.5-528.5).
10. Despair, failure, "dead" moments: show the face in black and white for 2.5-8 s, covering the whole line
    (PRaUeGY8Sr8 258.5-266.5, the heatmap maximum; kOccoMYydwI 532.5-534.5).
11. A face shot can cover a jump between two pieces of gameplay (1.5 s, PRaUeGY8Sr8 41.0-42.5), but only if there is talk
    or a reaction in it.

**Openings**
12. Long highlights: either start straight on gameplay heading into the first fight (first contact within 12-15 s,
    aA98jrFkEPQ), or open with a 15-20 s teaser that switches every 1-4 s: faces 2.5-4 s while someone talks, gameplay 1-2 s
    on action (5GNFp6GqCso, kOccoMYydwI). Put the strongest spoken hook in the first 6 s (tt1gwGtxjlU, heatmap 0.88-1.0 at 4-12 s).
13. Shorts: frame 0 is already action or the hook line (gunfire, "bhai suno"). No build-up (2.4).
14. A Short may carry one fixed title band for its whole length ("1v4 Clutch 😡") instead of timed text (2.5).

**Endings**
15. Shorts: after the last kill, keep 1.0-1.5 s of gameplay, then a 1.25-3.5 s tail: the face alone over a blur, a
    reaction, or a meme or colour-bars stinger; then end, or 1 s of black (CVqRiZ-wwNw, UhUauBjjrn8, DfOcogRMngg, bmoICLbNemI).
16. Long highlights: hold the result screen. WWCD banner, then 5-10 s of post-game or MVP, then the scoreboard for at
    least 2-5 s. For a record or big win, hold the scoreboard 10-24 s and add 10-12 s of face celebration if there is a
    face cam (67w15TWdikI, 5GNFp6GqCso, PRaUeGY8Sr8). End on a loss screen too if the match was lost.
17. Optional payoff ending: cut away mid-final-fight to a 5-6 s black card with one line of white text about the result
    (-ieo36Gj9Hk, heatmap 1.0 at the card). Use it only when the title asks a question.

**Layouts**
18. A 16:9 highlight keeps the streamer's own layout (stream bar, face cam corner) unchanged. Shorts use game over face
    (game 55-65%) while shooting, and the face alone over a blur or dark band for talk and reactions (2.5, 2.3).

## 4. What could not be measured

- No sound. Sound effects (whooshes under the whip transitions, booms), music beats and loudness could not be heard.
  Music is inferred only from "[संगीत]" captions (-ieo36Gj9Hk, PRaUeGY8Sr8 at about 87 s). Whether cuts land on music beats is
  unknown.
- Frame accuracy is about ±0.1 s. Seeking a paused YouTube video shows the nearest decoded frame. Most sheets used
  0.25-1 s steps, so an effect shorter than the step could be missed (for example a 1-2 frame flash at a kill).
- A pixel-difference cut detector was tried but could not tell edits from the game's own scope toggles and camera
  whips (scope-in changed brightness 110→45 within 0.06 s), so cuts were read by eye from the sheets.
- YouTube mid-roll ads appear in seeks. Two frames first read as part of the edit were ad frames: PRaUeGY8Sr8 at about 86 s
  (a payments-app ad; the sidebar showed the same advertiser), and probably kOccoMYydwI at 520-521 s (a text screen and an
  unknown man, absent when re-sampled at 0.5 s). The contact-sheet helper now labels ad frames "AD". A heatmap peak right
  after a mid-roll position may partly reflect ad timing.
- Caption timing is auto-generated (about ±0.2 s) and sparse on watch parties, music montages and Goblin's videos
  (aA98jrFkEPQ has a single caption line), so speech-to-cut timing was measured only on tt1gwGtxjlU, kOccoMYydwI and PRaUeGY8Sr8.
- Only one face punch-in was timed at word level. The rule (start 0.1 s before the word) rests on it plus Kobcv7gzuAY's zoom
  0.5 s before the line; more examples are needed.
- Joker's main channel has no long BGMI highlight (streams and IRL only), so it contributed two Shorts. JokerClips
  long videos were a raid moment and a watch party, not a match highlight.
- Whole-video cut counts were not taken for the long videos. Only the openings, 2-3 heatmap peaks and the endings were
  sampled.
