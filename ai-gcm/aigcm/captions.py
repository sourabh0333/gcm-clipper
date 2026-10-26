"""Burned-in captions from Whisper running on the laptop: a few words at a time, timed to speech."""

import wave

import numpy as np

from .jobs import log, write_json
from .media import extract_audio

WORDS_PER_CHUNK = 3
MAX_CHUNK_S = 1.4

ASS_HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,Nirmala UI,78,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,6,2,2,60,60,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def _stamp(seconds):
    cs = int(round(max(0.0, seconds) * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"


def chunk_words(words):
    chunks, current = [], []
    for w in words:
        if current and (len(current) >= WORDS_PER_CHUNK or w["end"] - current[0]["start"] > MAX_CHUNK_S):
            chunks.append(current)
            current = []
        current.append(w)
    if current:
        chunks.append(current)
    return [{"start": c[0]["start"], "end": c[-1]["end"], "text": " ".join(w["word"].strip() for w in c)}
            for c in chunks]


def to_ass(chunks, margin_v):
    lines = [ASS_HEADER.format(margin_v=margin_v)]
    for c in chunks:
        text = c["text"].replace("{", "(").replace("}", ")").upper()
        lines.append(f"Dialogue: 0,{_stamp(c['start'])},{_stamp(c['end'])},Caption,,0,0,0,,{text}")
    return "\n".join(lines) + "\n"


class Transcriber:
    def __init__(self, model_name, language=None):
        from faster_whisper import WhisperModel
        log(f"captions: loading Whisper '{model_name}' (first run downloads it)")
        self.model = WhisperModel(model_name, device="cpu", compute_type="int8")
        self.language = language

    def words(self, wav_path):
        # Pass samples rather than the path: faster-whisper's own file decoding (PyAV) breaks with some
        # PyAV versions, and the clip audio is already 16 kHz mono.
        with wave.open(str(wav_path), "rb") as w:
            samples = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
        segments, info = self.model.transcribe(samples, language=self.language, word_timestamps=True,
                                               vad_filter=True, beam_size=1)
        words = [{"start": w.start, "end": w.end, "word": w.word}
                 for seg in segments for w in (seg.words or [])]
        return words, info.language


def caption_clips(job, source, clips, settings, margin_v):
    out_dir = job.path("captions")
    out_dir.mkdir(exist_ok=True)
    transcriber = None
    for clip in clips:
        ass_path = out_dir / f"{clip['id']}.ass"
        if ass_path.exists():
            continue
        if transcriber is None:
            transcriber = Transcriber(settings.whisper_model, settings.caption_language)
        wav = out_dir / f"{clip['id']}.wav"
        extract_audio(source, wav, start=clip["start"], duration=clip["end"] - clip["start"])
        words, language = transcriber.words(wav)
        wav.unlink(missing_ok=True)
        chunks = chunk_words(words)
        write_json(out_dir / f"{clip['id']}.json", {"language": language, "chunks": chunks})
        ass_path.write_text(to_ass(chunks, margin_v), encoding="utf-8")
        log(f"captions: {clip['id']} ({language}, {len(words)} words)")
