# AI-GCM prototype

Turns a long BGMI recording or YouTube livestream into ranked 9:16 clips with captions, plus a review page where you keep or reject each clip.

It is a prototype for testing whether the idea works on real footage. Everything runs on this laptop for free. A free Gemini API key is optional and improves ranking, titles and captions.

## How it works

Each step saves its result in the job folder, so a crashed or stopped run continues where it left off.

| Step | What it does | Output |
|---|---|---|
| `ingest` | Downloads the YouTube video (or copies a local file) and extracts the audio | `source.mp4`, `audio.wav`, `info.json` |
| `audio` | Measures loudness, gunfire-like bursts and voice excitement every half second | `audio.npz` |
| `vision` | Reads the on-screen kill and knock messages with OCR, only when the HUD changes | `vision.json` |
| `moments` | Groups events into fights, adds loud-reaction moments, scores and ranks them | `moments.json` |
| `judge` | Optional: Gemini watches each candidate and rates it, names the moment and trims the cut | `judge/*.json` |
| `captions` | Transcribes each chosen clip with Whisper on the laptop | `captions/*.ass` |
| `render` | Cuts 1080×1920 clips with captions burned in | `clips/*.mp4` |
| `review` | Builds a page to watch, keep or reject clips | `review.html` |

## Setup (one time)

Install Python 3.12 and ffmpeg (in PowerShell):

```
winget install -e --id Python.Python.3.12
winget install -e --id Gyan.FFmpeg
```

Then, from this folder:

```
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

Optional free Gemini key: create one at https://aistudio.google.com/apikey, copy `.env.example` to `.env` and paste it in.

## Use

```
.venv\Scripts\python -m aigcm run "https://www.youtube.com/watch?v=..." --section 0:30:00-1:30:00
.venv\Scripts\python -m aigcm run D:\recordings\stream.mp4
.venv\Scripts\python -m aigcm status jobs\<job>
.venv\Scripts\python -m aigcm frames jobs\<job> --at 600,1200
.venv\Scripts\python -m aigcm eval jobs\<job> labels.csv
```

Open `jobs\<job>\review.html` in a browser to review clips. "Export decisions" saves your keep/reject choices, which become labelled training data.

`eval` compares the chosen clips with a hand-made list of good moments (`start,end,type,rating` in seconds, rating 1–5). It reports how many of the 4–5 rated moments were found and how many clips matched a real moment.

## Next improvements

- **Trained kill detector.** Roboflow's BGMI dataset (about 1,435 images labelled `kill`, `knock out` and `chicken dinner`, CC BY 4.0, attribution required) can replace or check the OCR step: https://universe.roboflow.com/bgmi-meb2n/bgmi-0wljr
- **Hinglish captions in Latin script.** Oriserve's Whisper-Hindi2Hinglish models (Apache 2.0) write Hinglish the way creators type it; Whisper `small` mostly writes Hindi in Devanagari.
- **Clip-level labels.** Exported review decisions plus `eval` scores show which moment types are missed.
