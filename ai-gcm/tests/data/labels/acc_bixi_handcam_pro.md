# acc_bixi_handcam_pro: labelling notes

How: contact sheets every 30 s for the overview, the counter crop (0.03,0.085,0.15,0.035) every 5 s over the whole file, 1 s steps around every counter change, and 1-4 s full-frame sheets around each death, load and spawn.

Summary: three Ranked Classic TPP squad matches on Erangel, vampire event.
- M1: running at 0 s, counter 6 at 0 s and still 6 at death (287), so 0 kills inside the file. Result #13/26.
- M2: 337-1004, 3 kills (623, 744, ~791). Died and respawned at ~791. At 1004 the video cuts straight to a loading screen (ended=unknown).
- M3: 1018-1800, 9 kills, still alive at the end (cut_off).

Uncertain:
- M2's end: no death, result or lobby. The video jumps from live fighting to the BGMI loading screen and then into a new match's spawn island (likely a disconnect or crash, or a quick leave).
- The M2 kill at ~791 happened while the HUD was hidden by the respawn countdown (+-4 s).

Things that would fool a detector:
- The hand cam bottom-left shows a phone screen with the game on it (a small second copy of the game), which could confuse frame classifiers.
- In-game Settings screens fill most of M2's spawn-island time (339-382), so no HUD shows for ~45 s after the match starts.
- Event respawn inside M2 (death at ~791, "Respawn Countdown", a second plane ride at 799-821). A second plane in the same match is not a new match.
- vision.json's match_start times (401, 1082) are 60+ s late; the real starts are 337 and 1018. Its "self_down" at 817 is during the respawn plane, so it is a stale or misread kill-feed line.
- The boss fight shows a purple health bar at the top centre (around 16:20-16:43), which is not the streamer's health.
