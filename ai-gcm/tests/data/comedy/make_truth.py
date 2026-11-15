"""Build the comedy truth set (Highlights Stage 2, S2.1) from YouTube auto-captions only: which minutes of Joker's
streams JokerClips' editor kept, and the stream's speech around them.

Inputs (not in git): the research's caption files (`<id>.hi-orig.vtt`) and its matched-segment tables
(`seg_<highlight>.txt`, from research_notes/BGMI highlight channels deep study/joker_deep.md section 3).
Output: one `<highlight>.json` per session highlight here, with numbers only (no stream text):

    {"highlight": id, "length": s, "kind": "session" | "single_match",
     "streams": [{"id", "kept": [[s0, s1], ...], "window": [w0, w1],
                  "lines": [[t0, t1, words, laugh, question], ...]}]}

`kept` are the stream spans whose speech matches the highlight word for word (the true cut edges are a few
seconds wider). `lines` are the caption lines inside `window` (the used span plus 20 minutes either side):
start, end, number of words, 1 if the captioner wrote a laugh tag or "ha ha", 1 if it ends in a question.

python tests/data/comedy/make_truth.py SEG_DIR SUBS_DIR
"""

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
SESSIONS = {"3c0nLXL8k6U": "session", "8Au8-kSBhgg": "session", "TIDXJ1YeirM": "single_match",
            "Ul5mEjNyzu4": "session", "VSK7Q7FH5rk": "session"}
PAD_S = 1200
LAUGH = re.compile(r"\[हंसी\]|\[hansi\]|\[laugh|(?:हा\s*){3,}|(?:ha\s*){3,}", re.I)
ROW = re.compile(r"^\s*\d+\s*\|\s*([\d:]+)-([\d:]+)\s*\|\s*[\d.]+\s*\|\s*(\S{11})\s*\|\s*([\d:]+)-([\d:]+)")


def secs(text):
    parts = [float(p) for p in text.split(":")]
    out = 0.0
    for p in parts:
        out = out * 60 + p
    return out


def kept_spans(seg_file):
    spans = {}
    for line in Path(seg_file).read_text(encoding="utf-8").splitlines():
        m = ROW.match(line)
        if m:
            spans.setdefault(m.group(3), []).append([secs(m.group(4)), secs(m.group(5))])
    return {k: sorted(v) for k, v in spans.items()}


def caption_lines(vtt):
    """One line per word-timed caption cue: (start, end, words, laugh, question)."""
    out = []
    for block in Path(vtt).read_text(encoding="utf-8").split("\n\n"):
        rows = block.strip().split("\n")
        if not rows or "-->" not in rows[0]:
            continue
        timed = [r for r in rows[1:] if "<c>" in r]
        if not timed:
            continue
        a, b = (secs(x.strip().split()[0]) for x in rows[0].split("-->"))
        text = re.sub(r"<[^>]+>", "", " ".join(timed))
        words = [w for w in text.split() if w.strip("[]।?.,!")]
        out.append([round(a, 2), round(b, 2), len(words), int(bool(LAUGH.search(text))), int("?" in text)])
    return out


def main(seg_dir, subs_dir):
    for hl, kind in SESSIONS.items():
        kept = kept_spans(Path(seg_dir) / f"seg_{hl}.txt")
        streams = []
        for sid, spans in kept.items():
            vtt = Path(subs_dir) / f"{sid}.hi-orig.vtt"
            if not vtt.exists():
                print(hl, "missing captions for", sid)
                continue
            w0, w1 = max(0.0, spans[0][0] - PAD_S), spans[-1][1] + PAD_S
            lines = [ln for ln in caption_lines(vtt) if w0 <= ln[0] <= w1]
            streams.append({"id": sid, "kept": spans, "window": [w0, w1], "lines": lines})
        length = None
        meta = Path(seg_dir) / f"seg_{hl}.txt"
        m = re.search(r"dur (\d+)s", meta.read_text(encoding="utf-8"))
        if m:
            length = int(m.group(1))
        (HERE / f"{hl}.json").write_text(json.dumps({"highlight": hl, "length": length, "kind": kind,
                                                     "streams": streams}, separators=(",", ":")), encoding="utf-8")
        print(hl, kind, [(s["id"], len(s["kept"]), len(s["lines"])) for s in streams])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
