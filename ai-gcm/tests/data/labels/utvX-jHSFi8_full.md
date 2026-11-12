# utvX-jHSFi8_full (ANJI, 2 h 9 min, vertical 720x1280)

## How it was labelled
- Coarse pass: a contact sheet of the game band (y 34-71 % of the frame) every 30 s over the whole file.
- Boundaries: 5 s and then 2 s sheets around every match start, end and result screen.
- Kills: the Eliminations box (130x42 px at x 0, y 462 of the 720x1280 frame) pulled every 2 s for the whole file with one
  ffmpeg pass. I read it every 10 s per match, then every 2 s around each change. The TDM fist counter was read every 5 s.
- `vision.json` was used only to know where to look. Every value here was checked on frames.

## Result
5 matches: 1 TDM (Warehouse, lost 35-40, 6 kills), then 4 Ranked Classic TPP games with the vampire event
(Erangel x3, the last one probably Livik): a chicken dinner with 3 kills, then deaths with 1, 0 and 3 kills.

## Uncertain
- **Placement for matches 3, 4 and 5 is null.** The vertical layout cuts the left edge of the game, and the big rank
  number on the "BETTER LUCK NEXT TIME!" screen sits there. Only "/100" or "/50" can be read. In match 5 the edge of a
  digit that looks like "2" is visible. Match 4 showed "You're in the top 10" while spectating.
- Match 5's map isn't certain: a 50-player lobby with snow, desert and farm terrain, probably Livik. It's labelled unknown.
- TDM has no fitting `ended` value. The team lost on score (DEFEAT screen), so it is labelled `unknown`.
- Knock times are approximate (about 5-10 s). The final death in match 3 happened in or near a car, and no knock was seen.

## Things that would fool an automatic detector
- **Respawns and recalls inside one match.** This event mode starts in a castle "virtual world" where death gives a
  Respawn Countdown and a second plane flight (30:47 in match 2, 1:00:19 in match 3). Later, on Erangel, dead players can
  be recalled. A death screen or a second plane does not mean a new match or the end of one.
- **The counter switches to a teammate's while the streamer is dead and waiting for recall:**
  - 3966-4032 shows 7 and then 5
  - 5630-5775 shows 7, 6 and 7
  - 6600-6626, after the final death, shows 9
  When the streamer comes back, the counter drops to their own value (1 or 0). This is what produced
  vision.json's fake "1 -> 6" kills at 3702 and its fake match_starts at 4925 and 5781.
- vision.json is also off elsewhere:
  - a self_kill at 206 in the lobby
  - match 3's kills at 3529, 3702 and 3972 (the only real kill is 3333)
  - match 5's first two kills merged into "0 -> 2" at 7500 (they are 7409 and 7499)
  - a match_start at 6975 instead of ~6913
- Stream-overlay animations pop up near match ends:
  - a black chicken-pan card reading "Winner Winner Chicken Dinner!" with "25" at 48:30, after the real in-game
    "#1 WINNER WINNER CHICKEN DINNER" banner at 48:20
  - a logo sting at 1:17:30
  - an "MVP" card at 2:07:40
  They can cover the result screen. The chicken card could be mistaken for the game's banner and should not be used as
  the end time.
- On the spawn island the Eliminations box isn't shown yet. It appears from the plane onwards. A notice pop-up
  covers the first seconds of each spawn island.
