"""A transcript of the whole section, with word times, from Whisper running on the laptop.

The default model is Oriserve's Whisper-Hindi2Hinglish-Swift (Apache 2.0), which writes Hinglish in Latin
script the way creators type it and runs at about 0.05-0.25 s per second of audio. It has to be converted
for faster-whisper once (see README); without it, Whisper `small` writes Hindi in Devanagari instead.
Moments read the transcript to find conversations, and captions cut their words from it.
"""

import wave
from pathlib import Path

import numpy as np

from .config import ROOT
from .jobs import log, read_json, write_json

CHUNK_S = 300
# Whisper sometimes loops on one phrase over game noise ("I don't know" 50 times) or invents English over
# music. Looping text compresses far better than real speech; invented text has a low average log
# probability. Segments past either limit are dropped, as are lines that are mostly one repeated word.
MAX_COMPRESSION = 2.4
MIN_LOGPROB = -1.0
MIN_UNIQUE = 0.35
# The Hinglish model returns about 30 s per segment, too long to cut clips on, so segments are split into
# lines at pauses and at sentence ends.
PAUSE_S = 0.7
# faster-whisper's batched pipeline groups the speech chunks the VAD finds and runs them together: on the
# laptop that was 5x faster than one chunk at a time (35 s vs 183 s for 10 min of continuous Hinglish)
# and found more words.
BATCH_SIZE = 8
# The batched pipeline's own speech detector dropped a sixth of the words on a 3-hour stream (coverage 0.70
# against 0.86 for the plain pipeline). The sound detector already knows where speech is, so its spans
# drive the batched pipeline instead: 0.85 coverage at about twice the plain speed on the worst window.
SPEECH_LEVEL = 0.3
SPEECH_PAD_S = 0.5
SPEECH_GAP_S = 1.0
MAX_CLIP_S = 30.0


def speech_spans(sounds, start, end):
    """[{"start", "end"}] in seconds relative to `start`: where the sound detector heard speech between
    start and end, padded, merged across short gaps, and cut to the 30 s the batched pipeline takes."""
    t, speech = sounds["t"], sounds["speech"]
    m = (t >= start) & (t < end)
    spans = []
    for ti in t[m][speech[m] >= SPEECH_LEVEL]:
        a, b = max(0.0, ti - start - SPEECH_PAD_S), ti - start + 1.0 + SPEECH_PAD_S
        if spans and a - spans[-1][1] <= SPEECH_GAP_S:
            spans[-1][1] = max(spans[-1][1], b)
        else:
            spans.append([a, b])
    out = []
    for a, b in spans:
        b = min(b, end - start)
        while b - a > MAX_CLIP_S:
            out.append({"start": round(a, 2), "end": round(a + MAX_CLIP_S, 2)})
            a += MAX_CLIP_S
        if b > a:
            out.append({"start": round(a, 2), "end": round(b, 2)})
    return out


def _load(settings, batched=True):
    """(model name, language, model) for the configured Whisper model: the batched pipeline for a whole
    stream, or the plain model, which finds more words, for short windows."""
    from faster_whisper import BatchedInferencePipeline, WhisperModel

    name, language = resolve_model(settings)
    model = WhisperModel(name, device="cpu", compute_type="int8", cpu_threads=getattr(settings, "analysis_threads", 0))
    return name, language, (BatchedInferencePipeline(model=model) if batched else model)


def resolve_model(settings):
    """(model name or folder, language) for faster-whisper; Hinglish models are told the text is English."""
    folder = ROOT / "models" / settings.whisper_model
    if folder.is_dir():
        return str(folder), "en"
    if settings.whisper_model.startswith("hinglish"):
        log(f"transcript: models/{settings.whisper_model} not found, using Whisper 'small' (Hindi in Devanagari)")
        return "small", settings.caption_language
    return settings.whisper_model, settings.caption_language


def coverage(transcript, sounds, speech_level=0.5):
    """What share of the seconds the sound detector heard speech in have at least one transcribed word.
    ANJI's stream had speech 47% of the time but only 309 words: coverage there was far below this
    function's healthy range (DIPENDU, a good transcript, scored about 0.95)."""
    t = sounds["t"]
    speech = t[sounds["speech"] >= speech_level]
    if not len(speech):
        return None
    spoken = np.zeros(int(t[-1]) + 2, dtype=bool)
    for seg in transcript["segments"]:
        for w in seg["words"]:
            spoken[int(w["start"]):int(w["end"]) + 1] = True
    return float(spoken[speech.astype(int)].mean())


def looks_broken(transcript, sounds, min_coverage=0.5, min_speech_s=120):
    """True when a transcript misses most of the speech the sound detector heard, or dropped many lines."""
    t = sounds["t"]
    speech_s = float((sounds["speech"] >= 0.5).sum() * (t[1] - t[0] if len(t) > 1 else 1.0))
    if speech_s < min_speech_s:
        return False
    cov = coverage(transcript, sounds)
    return cov is not None and cov < min_coverage


def retranscribe_windows(wav_path, windows, settings, transcript):
    """Transcribe only the given [(start, end)] windows with the plain (unbatched) pipeline and splice the
    result into `transcript`, replacing whatever it had there. The batched whole-stream transcript finds
    about 15% fewer words than the plain one; the chosen clips, a few minutes of audio, get the full read
    for their captions and safety check. The same path serves a bigger model when one is installed."""
    name, language, model = _load(settings, batched=False)
    with wave.open(str(wav_path), "rb") as w:
        rate = w.getframerate()
        samples = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    new = []
    for start, end in windows:
        a, b = int(start * rate), int(end * rate)
        parts, _ = model.transcribe(samples[a:b], language=language, word_timestamps=True, vad_filter=True,
                                    beam_size=1, condition_on_previous_text=False)
        for seg in parts:
            if seg.compression_ratio > MAX_COMPRESSION or seg.avg_logprob < MIN_LOGPROB:
                continue
            words = [{"start": round(start + w.start, 2), "end": round(start + w.end, 2), "word": w.word.strip()}
                     for w in seg.words or [] if w.word.strip()]
            for line in split_lines(words):
                if not looping(line):
                    new.append({"start": line[0]["start"], "end": line[-1]["end"],
                                "text": " ".join(w["word"] for w in line), "words": line})
    kept = [seg for seg in transcript["segments"]
            if not any(seg["end"] > s and seg["start"] < e for s, e in windows)]
    merged = dict(transcript, segments=sorted(kept + new, key=lambda s: s["start"]),
                  windows_redone_with=name, windows=[[round(s, 2), round(e, 2)] for s, e in windows])
    log(f"transcript: {len(windows)} clip windows redone with {Path(name).name}: {len(new)} lines")
    return merged


def fallback_model(settings):
    """A bigger Hinglish model to retry with when the default's transcript looks broken, if it is installed."""
    for name in ("hinglish-apex", "hinglish-prime"):
        if (ROOT / "models" / name).is_dir() and name != settings.whisper_model:
            return name
    return None


def split_lines(words):
    lines, current = [], []
    for w in words:
        if current and w["start"] - current[-1]["end"] > PAUSE_S:
            lines.append(current)
            current = []
        current.append(w)
        if w["word"].endswith((".", "?", "!")):
            lines.append(current)
            current = []
    if current:
        lines.append(current)
    return lines


def looping(line):
    tokens = [w["word"].strip(".,?!").lower() for w in line]
    return len(tokens) >= 12 and len(set(tokens)) / len(tokens) < MIN_UNIQUE


def transcribe(wav_path, settings, checkpoint=None, sounds=None):
    name, language, model = _load(settings)
    with wave.open(str(wav_path), "rb") as w:
        rate = w.getframerate()
        samples = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    segments, dropped, start = [], 0, 0
    step = rate * CHUNK_S
    # Each finished 5-minute chunk is saved, so a stopped or crashed run carries on from the next one.
    saved = read_json(checkpoint) if checkpoint else None
    if saved and saved.get("source") == [name, len(samples)]:
        segments, dropped, start = saved["segments"], saved["dropped"], saved["next_offset"]
        log(f"transcript: resuming at {start / rate / 60:.0f} min from the checkpoint")
    for offset in range(start, len(samples), step):
        base = offset / rate
        chunk_end = min(len(samples), offset + step) / rate
        clips = speech_spans(sounds, base, chunk_end) if sounds is not None else None
        if clips is not None and not clips:
            parts = []
        else:
            parts, _ = model.transcribe(samples[offset:offset + step], language=language, word_timestamps=True,
                                        vad_filter=clips is None, clip_timestamps=clips, beam_size=1,
                                        batch_size=BATCH_SIZE)
        for seg in parts:
            if seg.compression_ratio > MAX_COMPRESSION or seg.avg_logprob < MIN_LOGPROB:
                dropped += 1
                continue
            words = [{"start": round(base + w.start, 2), "end": round(base + w.end, 2), "word": w.word.strip()}
                     for w in seg.words or [] if w.word.strip()]
            for line in split_lines(words):
                if looping(line):
                    dropped += 1
                    continue
                segments.append({"start": line[0]["start"], "end": line[-1]["end"],
                                 "text": " ".join(w["word"] for w in line), "words": line})
        log(f"transcript: {min(len(samples), offset + step) / rate / 60:.0f} min done, {len(segments)} lines")
        if checkpoint:
            write_json(checkpoint, {"source": [name, len(samples)], "segments": segments, "dropped": dropped,
                                    "next_offset": offset + step})
    if dropped:
        log(f"transcript: dropped {dropped} looping lines")
    if checkpoint:
        Path(checkpoint).unlink(missing_ok=True)
    return {"model": name, "language": language, "segments": segments}


def words_between(transcript, start, end):
    """Words spoken between start and end, with times made relative to start."""
    return [dict(w, start=round(w["start"] - start, 2), end=round(w["end"] - start, 2))
            for seg in transcript["segments"] if seg["end"] > start and seg["start"] < end
            for w in seg["words"] if w["start"] >= start and w["end"] <= end]


def text_between(transcript, start, end):
    return " ".join(seg["text"] for seg in transcript["segments"] if seg["end"] > start and seg["start"] < end)
