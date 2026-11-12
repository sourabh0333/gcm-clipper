# vHLz6WDqJkk_full (GtxPreet, 3 h 8 min, Erangel squads, update 4.6)

Labels: `vHLz6WDqJkk_full.json`. 7 matches: 1 aborted on the spawn island, 3 chicken dinners, placements 6, 20 and 3 for the others.

| # | start | end | ended | placement | kills |
|---|------:|----:|-------|----------:|------:|
| 1 | 738 | 768 | left | - | 0 |
| 2 | 826 | 1898 | death | 6 | 4 |
| 3 | 2204 | 3919 | dinner | 1 | 7 |
| 4 | 4078 | 5143 | death | 20 | 6 |
| 5 | 5216 | 6792 | death | 3 | 17 |
| 6 | 6920 | 8509 | dinner | 1 | 10 |
| 7 | 8624 | 10514 | dinner | 1 | 15 |

## How it was labelled
- Contact sheets every 30 s over the whole file to find the parts, then 5 s and 2 s sheets around every match start and end.
- The Remaining/Eliminations HUD cropped every 10 s across every match, to read kills. Kill times are the midpoint of the 10 s window where the counter rose (so about ±5 s).
- Full frames every 5 s wherever the counter went down or jumped around, to tell deaths and spectating from kills.
- `vision.json` was used only to know where to look. Everything here was checked on frames.

## What is uncertain
- **Match 1** is only 30 s on the spawn island, followed by settings, loading and the lobby. I counted it as a match that ended with `left` because the in-match HUD was on screen. Drop it if the scorer should count only played matches.
- **Ends with `death` (matches 2 and 4)** are the streamer's *final* death: the moment the counter switches to a teammate's and never comes back. The team kept playing and the result screen came later (2028 and 5169). If the scorer uses the result screen as the end instead, matches 2 and 4 end 130 s and 26 s later.
- **Placement 20 in match 4** is shown as "#20 /97", while the other matches show "/25". I copied the number as shown.
- Kill times for double kills (two kills in one 10 s window) are given as the same time. In match 7 the 3->5 jump was split at 9092 and 9100, which matches what vision.json saw and fits the 10 s window.
- `knocked_streamer` lists the times the streamer went down and was **eliminated**, not knocked. Some were followed by a recall (see below). I did not look for knocks that teammates revived. Matches 5 and 7 show no deaths before the end in the 10 s counter samples. A short death where the spectated teammate happened to have the same count would not show up.

## Things that would fool an automatic detector
- **Recall / respawn.** In this mode a dead player can come back. The screen says "Don't give up! Your teammates can still recall you" and "Spectating Teammate", and while he spectates, the **Eliminations counter shows the teammate's count**, for example 4 -> 0 -> back to 1 in match 2, and 5 -> 7 -> 3 -> back to 5 in match 4. vision.json reads some of these as kills (5 -> 7 at 3793 is real, but there are others in match 4). After the recall the streamer flies back in on a pink plane ("Returning to the battleground"), so **a plane in the middle of a match does not mean a new match.** The counter does not reset, and Remaining can go up.
- **Virtual world (Ocean Palace).** A blue, tiled underwater area that players enter mid-match. It looks nothing like Erangel, and there are pink/green planes flying in and out of it. All of it is the same match.
- **Final 7 in match 4 is a teammate's.** The streamer died at about 5142 on 6 kills, and the counter then showed the spectated teammate's 7 until the #20 screen.
- **Face scene inside a match.** In match 7 the streamer switched to the full-screen face/chat scene from 8650 to 8745, while he was on the spawn island and boarding the plane. Before matches 3 and 6 the same scene hid the spawn island, so those matches start at the first game frame (2204 plane, 6920 spawn island).
- **Like-goal overlay.** A big green thumb with "N / M" (sometimes "THANK YOU!") covers the centre of the frame, mainly on dinner/result screens (3925-4000, 8510-8650, 10555-10650) but also in-game at 4078 and 8745. After the last match it sits on a black screen for about 90 s.
- The stream starts with about 6.5 min of face chat, then a black screen with the phone home screen before the game boots (393-424).
