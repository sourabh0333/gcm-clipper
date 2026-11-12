# Pylusnav-1Q_full (DIPENDU, 2 h 3 min, vertical 720x1280)

## How I labelled it
- Coarse contact sheet every 30 s over the whole file (top 56% of the frame: game + counter strip) to find the parts.
- One ffmpeg pass that cropped the counter strip (x 0-360, y 638-694) every 2 s for the whole file; kill times
  come from tiling those crops at 4-6 s steps (counter rises bracketed to <= 6 s, time given as the midpoint).
- 2-4 s full sheets around every match start, death and result screen.
- `vision.json` was used only as a hint; it is wrong in several places (see below).

## Summary
6 matches, all Ranked classic Erangel ("Midnight Hunters" theme, which has respawns/recalls). All ended in death.

| # | start | end | kills | placement |
|---|-------|-----|-------|-----------|
| 1 | 0 (file starts mid-match) | 776 | 0 | null (rank cropped) |
| 2 | 967 | 1815 | 4 | 15 (top half of digits only) |
| 3 | 1875 | 2307 | 2 | null (probably #24) |
| 4 | 2633 | 3194 | 4 | null |
| 5 | 3310 | 4407 | 5 | null |
| 6 | 4712 | 5864 | 2 | null (<= 12 from promotion screen) |

After match 6 (from ~1:38) there is no more gameplay: ~24 min of lobby, crates, shop and inventory, then the
last minute is the mirroring app / face cam only.

## Uncertain
- **Placement**: the rank on the result screen ("#NN BETTER LUCK NEXT TIME!") sits off the left edge of the main
  game crop. Only its top half shows in the counter strip, because the "NEW GAMING KEYBOARD & MOUSE GOAL" banner
  covers the bottom half. Only match 2 ("#15") is readable with some confidence. The others are null, with what
  can be seen written in each match's notes.
- Match 1 start is the start of the file: the stream begins mid-match with Remaining 57.
- Kill times are +/- 3 s (6 s brackets). The 2->4 jumps in matches 2 and 4 are two kills inside one bracket.

## Traps for an automatic detector
- **Respawns inside a match.** In match 2 (~1369-1381) the streamer is finished, spectates a teammate (the
  counter jumps to the teammate's 5) and then comes back. In match 4 (~3017-3026) the streamer dies, gets a
  "Respawn Countdown" and re-enters **by plane** mid-match (plane + Jump button with Remaining 91, Eliminations
  4). Neither one is a match end or a new match start. "Remaining" also goes up at times because of respawns
  and recalls.
- **Counter switches to a teammate while spectating** after the final death: 11 after match 2; 1-2 after
  match 3; 3 after match 4; 0/1/0 after match 5; 3/4/5 after match 6. `vision.json` reads this as streamer kills,
  e.g. "5 -> 9" at 4411 and "eliminations 11 -> 0" as a match start at 1950.
- `vision.json` misses most of the match starts (it has 1950, 2706 and 4782, all late or wrong; the real
  starts are 967, 1875, 2633, 3310 and 4712), and misses most of the kills in match 5 (3467, 3491, 3671, 3797).
- The spawn island shows "Players NN" in the counter strip instead of "Remaining", often behind a "Notice"
  popup. Match start = first frame with that HUD.
- The screen mirror drops out at times: the game area goes black or shows the mirroring app's help screen
  (785-811, end of file), and there are short glitches (~1856).
- The face cam (lower half) is always on screen. Nothing ever covers the counter strip during play.
