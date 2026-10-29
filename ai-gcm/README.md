# AI-GCM prototype

Turns a long BGMI recording or YouTube livestream into ranked 9:16 clips with captions, plus a review page where you keep or reject each clip.

It is a prototype for testing whether the idea works on real footage. Everything runs on this laptop for free. A free Gemini API key is optional and improves ranking, titles and captions.

## How it works

Each step saves its result in the job folder, so a crashed or stopped run continues where it left off.

| Step | What it does | Output |
|---|---|---|
| `ingest` | Downloads the YouTube video (or copies a local file) and extracts the audio | `source.mp4`, `audio.wav`, `info.json` |
| `vision` | Reads the Eliminations and Remaining counters and on-screen messages with OCR | `vision.json` |
| `audio` | Measures loudness, gunfire-like bursts and voice excitement every half second | `audio.npz` |
| `sounds` | Tells laughter, screaming, speech, gunfire and music apart about once a second (YAMNet) | `sounds.npz` |
| `transcript` | Writes down everything said, in Hinglish, with word times (Whisper on the laptop) | `transcript.json` |
| `moments` | Groups kills into fights that start where the shooting started, finds funny and lively talk, scores and ranks them | `moments.json`, `talk.json` |
| `judge` | Optional: Gemini watches each candidate and rates it, names the moment and trims the cut | `judge/*.json` |
| `captions` | Cuts each chosen clip's words from the transcript | `captions/*.ass` |
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

Hinglish speech model (one time, about 5 minutes). Converting it needs `torch` and `transformers`, so use a separate throwaway venv:

```
python -m venv %TEMP%\convert-venv
%TEMP%\convert-venv\Scripts\python -m pip install --index-url https://download.pytorch.org/whl/cpu torch
%TEMP%\convert-venv\Scripts\python -m pip install transformers ctranslate2
%TEMP%\convert-venv\Scripts\ct2-transformers-converter --model Oriserve/Whisper-Hindi2Hinglish-Swift --output_dir models\hinglish-swift --quantization int8 --copy_files tokenizer.json preprocessor_config.json
```

Without it, transcripts and captions fall back to Whisper `small`, which writes Hindi in Devanagari.

Optional free Gemini key: create one at https://aistudio.google.com/apikey, copy `.env.example` to `.env` and paste it in.

## Use

```
.venv\Scripts\python -m aigcm run "https://www.youtube.com/watch?v=..." --section 0:30:00-1:30:00
.venv\Scripts\python -m aigcm run D:\recordings\stream.mp4
.venv\Scripts\python -m aigcm status jobs\<job>
.venv\Scripts\python -m aigcm frames jobs\<job> --at 600,1200
.venv\Scripts\python -m aigcm eval jobs\<job> labels.csv
```

## App

```
.venv\Scripts\python -m aigcm serve
```

Then open http://localhost:8765 on the laptop, or the `http://192.168.…:8765` address it prints on a phone on the same Wi-Fi (allow Python through the Windows firewall the first time). Paste a YouTube link, watch the progress, swipe right to keep a clip and left to reject it, then download the kept clips. The laptop does the processing, so it has to stay on while a job runs. Installing to the home screen and sharing need HTTPS, which the plain Wi-Fi address doesn't have.

Without the app, open `jobs\<job>\review.html` in a browser to review clips. "Export decisions" saves your keep/reject choices, which become labelled training data.

`python make_demo.py` builds three demo jobs in `demo\` (finished with placeholder clips, still processing, failed) for working on the app without a real stream. Set `AIGCM_JOBS_DIR=demo` to use them.

`eval` compares the chosen clips with a hand-made list of good moments (`start,end,type,rating` in seconds, rating 1–5). It reports how many of the 4–5 rated moments were found and how many clips matched a real moment.

## Next improvements

- **Trained kill detector.** Roboflow's BGMI dataset (about 1,435 images labelled `kill`, `knock out` and `chicken dinner`, CC BY 4.0, attribution required) can replace or check the OCR step: https://universe.roboflow.com/bgmi-meb2n/bgmi-0wljr
- **Hinglish captions in Latin script.** Oriserve's Whisper-Hindi2Hinglish models (Apache 2.0) write Hinglish the way creators type it; Whisper `small` mostly writes Hindi in Devanagari.
- **Clip-level labels.** Exported review decisions plus `eval` scores show which moment types are missed.
