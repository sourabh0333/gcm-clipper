# Analysis improvement notes

Shared notes for making detection more accurate and adding funny moments and conversations as clips. Update before every push (see `CLAUDE.md`). **Paused 28 Oct, 13:55, at the owner's request; resume on "start".**

## Goal (owner, 28 Oct)

More accurate analysis, and clips from more than kills: understand the audio, and find funny incidents and funny conversations (jokes, roasts, banter with teammates, rage, big reactions) so they can be clipped and highlighted too.

## Plan

1. **Sound detector** (laughter, screams, speech, gunfire) with YAMNet: free, on the laptop. *Started.*
2. **Full-stream Hinglish transcript** with Oriserve's Whisper-Hindi2Hinglish models (Apache 2.0, write Hinglish in Latin script): free, on the laptop. Also fixes the garbled captions. *Started.*
3. **Funny candidates** from laughs, screams and transcript cues (for example "haha"), with clip edges on sentence boundaries so the setup and punchline are both in.
4. **AI reads the conversation** around each candidate (Gemini free tier, needs the owner's free key) to decide if it's funny, name it and trim it.
5. Later: chat replay when a stream has enough chat, knock detection, a "missed a moment" button for measuring recall, and learning from keep and reject swipes.

## Findings so far

- **Chat replay:** 2 of the 3 test streams have it, but DIPENDU (425 subscribers) had only 35 messages in 30 minutes, with no link to the clips. Only useful for bigger streamers.
- **YAMNet on stream audio:** about 40 s per 30 min of audio. Speech and gunfire come through clearly (gunfire up to 0.98). Laughter scores stay below 0.1 on all 3 streams (top spots: DIPENDU 12:28, the same place the loudness check found a reaction; ANJI 27:02, 23:47, 16:15; GtxPreet 24:23, 4:52, 19:27). Not yet checked whether those spots are real laughs; that needs the transcript.
- **Model sizes:** Hinglish Swift is Whisper base (fast); Apex is large-v3-turbo (much better on paper, slower on CPU); Prime is large-v3 (too slow for this laptop).

## Done

- `aigcm/sounds.py` and a new `sounds` stage after `audio` (writes `sounds.npz`; downloads `models/yamnet.tflite` on first run). App and server know the new stage; demo jobs updated. Existing jobs need `--force sounds` to use it. Moments don't use it yet.
- `mediapipe` installed in `.venv` (not yet in `requirements.txt`).
- Hinglish Swift converted for faster-whisper into `models/hinglish-swift/` (int8, 76 MB). `models/` is not in git; the conversion used a separate venv with `torch` and `transformers`: `ct2-transformers-converter --model Oriserve/Whisper-Hindi2Hinglish-Swift --output_dir models/hinglish-swift --quantization int8 --copy_files tokenizer.json preprocessor_config.json`.

## Next (where to resume)

1. Compare Whisper `small` (now), Hinglish Swift and Hinglish Apex on the laugh spots above: quality and speed. Use `language="en"` for the Hinglish models (per the model card). A test with Whisper `small` ran very slowly while the converter was installing; rerun it on a quiet laptop.
2. Add `mediapipe` to `requirements.txt`.
3. Add a `transcript` stage (whole section), reuse it for captions.
4. Use `sounds` in moments: start fight clips where the gunfire starts; laugh and scream spikes, relative to the stream's own level, become funny candidates.
5. Run on DIPENDU and ANJI, check the new clips, then ask the owner for the free Gemini key.

## Not done or not tested

- Nothing in moments or captions uses the new signals yet, so clips are unchanged.
- The app server running on the laptop since 12:43 still has the old code; restart it to show the new stage.
