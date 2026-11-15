"""Score the comedy unit finder against what JokerClips' editor kept (Highlights Stage 2, S2.2-S2.3).

For each stream stretch in the truth set: the finder reads the stream's YouTube captions (cached locally in
data/comedy_captions/<id>.hi-orig.vtt, not in git) over the truth window, picks as many units as the editor
kept from that stretch, and is scored with comedy.overlap_scores. A random pick of the same number and length
of spans is the baseline. Gemini's answers are cached next to the captions (<id>.comedy.json).

python tests/data/comedy/evaluate.py [--no-gemini]
"""

import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from aigcm import comedy  # noqa: E402
from aigcm.config import Settings  # noqa: E402

HERE = Path(__file__).parent
CAPS = ROOT / "data" / "comedy_captions"


def random_baseline(w0, w1, n, length, kept, draws=300):
    rng = random.Random(7)
    r = p = 0.0
    for _ in range(draws):
        picks = []
        for _ in range(n):
            a = rng.uniform(w0, w1 - length)
            picks.append({"start": a, "end": a + length})
        rr, pp = comedy.overlap_scores(picks, kept)
        r += rr
        p += pp
    return round(r / draws, 3), round(p / draws, 3)


def main(use_gemini=True):
    settings = Settings.from_env()
    ask = comedy.gemini_ask(settings) if use_gemini and settings.gemini_api_key else None
    rows = []
    for f in sorted(HERE.glob("*.json")):
        truth = json.loads(f.read_text(encoding="utf-8"))
        for s in truth["streams"]:
            vtt = CAPS / f"{s['id']}.hi-orig.vtt"
            if not vtt.exists():
                print("missing", vtt.name)
                continue
            w0, w1 = s["window"]
            lines = [ln for ln in comedy.lines_from_vtt(vtt.read_text(encoding="utf-8")) if w0 <= ln[0] <= w1]
            units = comedy.rule_units(lines, w0, w1)
            if ask:
                units += comedy.gemini_units(lines, [(w0, w1)], CAPS / f"{s['id']}.{int(w0)}.comedy.json", ask)
            units = comedy.tidy(units, lines)
            n = len(s["kept"])
            picks = sorted(sorted(units, key=lambda u: (-u["funny"], u["start"]))[:n], key=lambda u: u["start"])
            mean_len = sum(u["end"] - u["start"] for u in picks) / max(1, len(picks))
            score = comedy.overlap_scores(picks, s["kept"])
            base = random_baseline(w0, w1, n, mean_len or 13.0, s["kept"])
            rows.append((truth["highlight"], s["id"], n, len(units), score, base))
            print(f"{truth['highlight']} {s['id']}: editor kept {n}, found {len(units)} units, "
                  f"recall/precision {score} vs random {base}", flush=True)
    if rows:
        r = sum(x[4][0] for x in rows) / len(rows)
        p = sum(x[4][1] for x in rows) / len(rows)
        br = sum(x[5][0] for x in rows) / len(rows)
        bp = sum(x[5][1] for x in rows) / len(rows)
        print(f"MEAN recall {r:.2f} precision {p:.2f} | random recall {br:.2f} precision {bp:.2f}")


if __name__ == "__main__":
    main("--no-gemini" not in sys.argv)
