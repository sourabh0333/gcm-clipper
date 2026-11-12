# acc_shlok_solo_vs_squad: labelling notes

How: contact sheets every 30 s for the overview, the counter crop (0.02,0,0.16,0.04) every 3-5 s across the file, then 1-4 s full-frame sheets around every load, spawn, death and result.

Summary: 6 matches, all Ultimate Royale (TPP) squad on Erangel (64 players / 16 teams, so results read "#N /16").
- M1: running at 0 s, counter 3 at 0 s, 0 kills inside the file, death 64, #6/16.
- M2: 111-337, 2 kills (240, 318), knocked ~330, death 337, #14/16.
- M3: 452-650, 0 kills, death 650, #15/16.
- M4: 748-846, spawn island and plane only; server time-out, then he leaves (ended=left).
- M5: 890-1030, 0 kills, death 1030, #15/16.
- M6: 1068-1800, 14 kills, still alive with Remaining 12 when the file ends (cut_off).

Uncertain:
- M1's map and mode come from the "/16" result and the other matches; that result's header was not read.
- Mode is "other" because Ultimate Royale is its own battle-royale variant, not classic. Change it to "classic" if the scorer treats it as BR.
- M6 kill times after 1228 come from 3 s steps (+-3 s).

Things that would fool a detector:
- The red "SHLOK IS LIVE" banner covers the bottom ~18% of the game (health bar, bottom HUD).
- Remaining starts at 64, not 100, and placements are out of 16 (teams), so a 100-player assumption breaks.
- In M4 the streamer never lands: a "server response timed out" dialog, then "Leave the match?", 98 s of spawn island and plane, with no result screen.
- Lobby phases include long "Add Friend" keyboard screens and career-stats screens (white or grey UI), which are BGMI but not a match.
- vision.json found no match starts at all and only the M6 kills from 1248 on. It missed the first three M6 kills (1195, 1217, 1228) and M2's two kills (240, 318). Its "remaining" track mixes values across matches.
