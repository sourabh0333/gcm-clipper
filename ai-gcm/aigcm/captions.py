"""Burned-in captions: a few words at a time, cut from the section's transcript and timed to speech."""

from .jobs import log, write_json
from .transcript import words_between

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


def caption_clips(job, clips, transcript, margin_v):
    out_dir = job.path("captions")
    out_dir.mkdir(exist_ok=True)
    for clip in clips:
        ass_path = out_dir / f"{clip['id']}.ass"
        if ass_path.exists():
            continue
        chunks = chunk_words(words_between(transcript, clip["start"], clip["end"]))
        write_json(out_dir / f"{clip['id']}.json", {"model": transcript["model"], "chunks": chunks})
        ass_path.write_text(to_ass(chunks, margin_v), encoding="utf-8")
        log(f"captions: {clip['id']} ({sum(len(c['text'].split()) for c in chunks)} words)")
