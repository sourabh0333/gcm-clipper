# acc_lolzzz_landscape_bigcreator: labelling notes

How: contact sheets every 30 s for the overview, the top-left HUD crop (0.05,0,0.16,0.045) every 5 s over the whole file, 1 s steps over the first 12 kills, and 1-3 s full-frame sheets around the deaths, the end of the match and the results.

Summary: one long match (Ranked Classic TPP squad Erangel, vampire "Bloodline Awakening" event). It is already running at 0 s and ends at 1725, when the streamer is shot with 4 players alive. 28 kills, all inside the file. Results: #4/99 personal, #2/26 team. Then results, lobby and a loading screen to the end.

Uncertain:
- Placement: two ranks are shown. I used the team's #2/26; #4/99 is the personal rank.
- Kill times after 195 come from 5 s steps (+-3 s). The 2-kill steps at 47 and 111 are in one frame each.
- The bat counter (third HUD number) is an event counter (0-7, goes up and down). It is not kills.

Things that would fool a detector:
- The event HUD replaces the normal "Remaining | Eliminations" box with three icon numbers. OCR looking for the word "Eliminations" will find nothing; the kills are the middle (crosshair) number.
- Respawns inside one match: a death at ~358 shows a "Respawn Countdown 5..1" with the HUD hidden, and a death at ~1199 shows a "Join the vampires and return to the battleground?" dialog. Neither is a match end, and the counter keeps its value after them.
- vision.json's 9 -> 10 at 156 is late (the real kill is at ~146). Its "match_start 28 -> 0" at 1773 is the lobby, not a match.
- Two result screens in a row (#4/99, then #2/26) plus MVP; a detector reading the first "#4" gets the personal rank, not the team placement.
- The large "2,845,6xx" number by the facecam changes all the time and could be misread as a counter.
