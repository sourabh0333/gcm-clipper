# Analysis improvement notes

Shared notes for making detection more accurate and adding funny moments and conversations as clips. Update before every push (see `CLAUDE.md`).

## Goal (owner, 28 Oct)

More accurate analysis, and clips from more than kills: understand the audio, and find funny incidents and funny conversations (jokes, roasts, banter with teammates, rage, big reactions) so they can be clipped and highlighted too.

## Pipeline now (29 Oct)

`ingest, vision, audio, sounds, transcript, moments, judge, captions, render, review`

- `sounds` (`aigcm/sounds.py`): YAMNet through MediaPipe scores laughter, screaming, speech, gunfire and music about once a second. About 10 s per 30 min. Downloads `models/yamnet.tflite` on first run.
- `transcript` (`aigcm/transcript.py`): the whole section in Hinglish with word times, using `models/hinglish-swift` (Oriserve Whisper-Hindi2Hinglish-Swift converted to int8; see README for the one-time conversion). Falls back to Whisper `small` if the folder is missing. Long segments are split into lines at pauses and sentence ends; looping and invented lines are dropped (gzip ratio, average log probability, one word repeated).
- `moments`: fight clips start where the gunfire began (`_gunfire_start`), never later than the 12 s lead-in. `aigcm/talk.py` adds talk clips: rules always, Gemini when a key is set.
- `judge`: Gemini now also gets the transcript of each candidate and is told talk can be worth posting without kills.
- `captions`: cut from the transcript, so no second transcription and Latin-script Hinglish.

## Talk rules (no key needed)

Score every 2 s from: laughter and scream spikes relative to the stream's own level (floor 0.01, so near-silence doesn't count), loudness, "haha" in the text, banter words (noob, pagal, abe, sorry, camper, bachcha…), swearing and insults (rage and roasts), and how much is being said. Peaks at least 45 s apart, 20 s of setup before and 8 s after, widened to whole lines, 15–45 s long. Talk clips score rule score × 3 (Gemini's rating × 5), so they rank with one- and two-kill fights. That weight is a guess; the owner's swipes should tune it.

## Findings

- **Chat replay** is too sparse on small streams (DIPENDU: 35 messages in 30 min). Only useful for big streamers.
- **Laughter detection** barely works on stream audio: game sound and music sit over the voices, and scores stay under 0.1. Gunfire (up to 0.98) and speech come through clearly.
- **Hinglish Swift** is fast (DIPENDU: 130 s for 30 min) and readable, and covered 325 of the 342 seconds where speech was detected. On ANJI it failed: speech was detected 47% of the time but only 309 words came out and 43 looping lines were dropped (918 s). A bigger model (Apex, large-v3-turbo based) might fix this but will be much slower on this laptop; not tested.
- **DIPENDU, read by hand:** lively talk at 12:08 (teammate's mic not working), 20:00 ("campar ka bachcha" roast after being knocked), 23:27–24:30 ("sori bhaiya, lag ho gaya" banter), 12:55 ("koi noob nahin hota"). The rules now find the first three; they miss 12:55.
- **New DIPENDU clips (12):** 3 talk clips (ranked #1, #4 and #10), 6 fights, 3 reactions. Fight starts barely moved, because the gunfire in these fights began inside the existing 12 s lead-in. Talk clip #1 (mic problem) outranking 2-kill fights is unproven.
- The owner said testing on one stream is enough for now (29 Oct), so ANJI was only transcribed and GtxPreet was not redone.

## Fixed on the way

- Rerunning a job without `--section` wiped its saved time range (the app then showed "Whole video" and wrong stream times). A resumed job now keeps its range; the three test jobs' ranges were restored by hand.
- Rerunning `moments` reused clip ids, so earlier keep/reject decisions pointed at different clips. They are now moved to `history/<time>/` with the clip list they belong to. The owner's 28 Oct phone review of DIPENDU is in `jobs/Pylusnav-1Q_1800-3600/history/20261028-reviewed-on-phone/`.
- ANJI's and GtxPreet's old clips were deleted by the reruns and were remade with the new pipeline (29 Oct). ANJI: 9 clips, the top 3 are talk clips picked mostly from laughter because its transcript is poor, so they likely outrank its fights wrongly. GtxPreet (transcript 511 s for 40 min): 12 clips, fights on top, 6 talk clips.

## Next

1. Owner reviews DIPENDU's new clips in the app; their keeps and rejects show whether talk clips are worth it and how to weight them.
2. Owner creates a free Gemini key (https://aistudio.google.com/apikey), then the AI reads the whole transcript for funny moments (`talk.from_gemini`, untested) and the judge rates every clip.
3. If ANJI-like streams are common, test the Apex model, or switch to it only when Swift's transcript looks broken.
4. Later: knock detection, a "missed a moment" button for measuring recall, learning weights from swipes.

## Not tested

- `talk.from_gemini` and the judge's new transcript prompt (no key yet).
- Talk rules on more than one stream with real dialogue.
