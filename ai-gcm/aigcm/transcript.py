"""A transcript of the whole section, with word times, from Whisper running on the laptop.

The default model is Oriserve's Whisper-Hindi2Hinglish-Swift (Apache 2.0), which writes Hinglish in Latin
script the way creators type it and runs at about 0.05-0.25 s per second of audio. It has to be converted
for faster-whisper once (see README); without it, Whisper `small` writes Hindi in Devanagari instead.
Moments read the transcript to find conversations, and captions cut their words from it.
"""

import wave

import numpy as np

from .config import ROOT
from .jobs import log

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


def resolve_model(settings):
    """(model name or folder, language) for faster-whisper; Hinglish models are told the text is English."""
    folder = ROOT / "models" / settings.whisper_model
    if folder.is_dir():
        return str(folder), "en"
    if settings.whisper_model.startswith("hinglish"):
        log(f"transcript: models/{settings.whisper_model} not found, using Whisper 'small' (Hindi in Devanagari)")
        return "small", settings.caption_language
    return settings.whisper_model, settings.caption_language


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


def transcribe(wav_path, settings):
    from faster_whisper import WhisperModel

    name, language = resolve_model(settings)
    model = WhisperModel(name, device="cpu", compute_type="int8")
    with wave.open(str(wav_path), "rb") as w:
        rate = w.getframerate()
        samples = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    segments, dropped = [], 0
    step = rate * CHUNK_S
    for offset in range(0, len(samples), step):
        base = offset / rate
        parts, _ = model.transcribe(samples[offset:offset + step], language=language, word_timestamps=True,
                                    vad_filter=True, beam_size=1, condition_on_previous_text=False)
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
    if dropped:
        log(f"transcript: dropped {dropped} looping lines")
    return {"model": name, "language": language, "segments": segments}


def words_between(transcript, start, end):
    """Words spoken between start and end, with times made relative to start."""
    return [dict(w, start=round(w["start"] - start, 2), end=round(w["end"] - start, 2))
            for seg in transcript["segments"] if seg["end"] > start and seg["start"] < end
            for w in seg["words"] if w["start"] >= start and w["end"] <= end]


def text_between(transcript, start, end):
    return " ".join(seg["text"] for seg in transcript["segments"] if seg["end"] > start and seg["start"] < end)
