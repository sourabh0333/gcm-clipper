# acc_rajput_small_hindi: labelling notes

How: contact sheets every 30 s for the overview, the counter strip (crop 0,0.286,0.175,0.012 of the 1080x1920 frame) every 5 s over the whole file, then 1 s steps around every counter change, and 1-3 s full game-band sheets around each start, death and result.

Summary: 3 matches, all Livik squads (Ranked Classic TPP).
- M1: running at 0 s (counter 0 at 0 s), 4 kills (34, 36, 59, 231), death ~501, result #6/12.
- M2: 585-1097, 1 kill (691), death 1097, left the match at ~1215, result #31/50.
- M3: 1280-1793, 4 kills (1392, 1436, 1437, 1593), died ~1617, recalled ~1719, died again ~1793, file ends while spectating. No result screen.

Uncertain:
- M2 placement "#31 /50" is what the result screen shows after he left; the "/50" looks odd for squads, so treat it with care. The map comes from the snowy plane view and Livik loading screens.
- M3 ending: the match uses recall, so the streamer's death at 1617 was not the end. I split it into match / between (spectating) / match parts. The final death at 1793 is labelled ended=death, but a recall was still possible when the file ended.

Things that would fool a detector:
- The HUD counters are tiny (the game is a letterboxed band in a vertical frame). Remaining/Eliminations sit at about y 0.29 of the full frame.
- While spectating, the Eliminations counter shows the teammate's kills: 6 at 8:28-8:38 (vision.json logs this as "4 -> 6" at 508), and 0/2/3 values during 1097-1215 and 1617-1719. Counter drops from 4 to 3 or 0 there are not new matches. vision.json's "match_start" at 1114 is a spectating switch, not a match start; its "1103 1 -> 2" is a teammate's kill.
- Recall mode: after a death the streamer can come back (1719), so the counter jumps back to his own value (4).
- A result banner "#6 BETTER LUCK NEXT TIME" flashes at 8:24 while the death replay and spectating are still going, before the real result screen at 8:39.
- vision.json has no "remaining" data for this job at all, and no match_start at 585 or 1280.
