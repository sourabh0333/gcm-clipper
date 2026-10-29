"""Optional second opinion from Gemini's free tier. Each candidate is cut to a small 360p preview, Gemini
rates it like an editor would, names the moment and suggests a tighter cut. Results are cached per
candidate, so a run that hits the free-tier limit continues later without paying for repeats."""

import json
import time

from .jobs import log, read_json, write_json
from .media import cut_preview
from .transcript import text_between

TYPES = ["fight", "clutch", "multi_kill", "squad_wipe", "close_escape", "funny", "banter", "rage", "hype", "win",
         "reaction", "nothing"]

PROMPT = """You are a short-form video editor for an Indian BGMI (Battlegrounds Mobile India) gaming creator.
This is one candidate moment cut from a longer stream. A detector flagged it because: {reasons}.
What was said, from an automatic Hinglish transcript that has mistakes: {said}
Judge the gameplay and the talk: a funny or entertaining conversation is worth posting even without kills.

Watch it and reply with JSON only, using exactly these keys:
- "worth": integer 1-10, how likely the creator would post this as a YouTube Short or Instagram Reel. Be strict: most candidates are not worth posting.
- "type": one of {types}.
- "summary": one English sentence saying what happens.
- "title": a short, catchy title in the language mix the streamer speaks (Hinglish in Latin script if they speak Hindi).
- "start_trim_s": seconds to cut from the start (0 if the start is right). Remove dead time before the action.
- "end_trim_s": seconds to cut from the end (0 if the end is right). Keep the reaction after the last kill.
- "weak_points": short text naming anything that makes it weak (dead time, cut mid-fight, no action), or "".
"""


def _client(api_key):
    from google import genai
    return genai.Client(api_key=api_key)


def _ask(client, model, video_bytes, prompt):
    from google.genai import types
    response = client.models.generate_content(
        model=model,
        contents=[types.Part.from_bytes(data=video_bytes, mime_type="video/mp4"), prompt],
        config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.2),
    )
    return json.loads(response.text)


def _clean(raw, length):
    worth = int(raw.get("worth", 0))
    kind = raw.get("type") if raw.get("type") in TYPES else "nothing"
    start_trim = max(0.0, float(raw.get("start_trim_s", 0) or 0))
    end_trim = max(0.0, float(raw.get("end_trim_s", 0) or 0))
    if start_trim + end_trim > length * 0.6:
        start_trim = end_trim = 0.0
    return {"worth": max(1, min(10, worth)), "type": kind, "summary": str(raw.get("summary", "")),
            "title": str(raw.get("title", "")), "start_trim_s": start_trim, "end_trim_s": end_trim,
            "weak_points": str(raw.get("weak_points", ""))}


def judge_all(job, source, candidates, settings, transcript=None):
    out_dir = job.path("judge")
    out_dir.mkdir(exist_ok=True)
    client = _client(settings.gemini_api_key)
    gap = 60.0 / max(1, settings.gemini_rpm)
    last_call = 0.0
    for cand in candidates:
        cache = out_dir / f"{cand['id']}.json"
        if cache.exists():
            continue
        preview = out_dir / f"{cand['id']}.mp4"
        cut_preview(source, cand["start"], cand["end"], preview)
        said = text_between(transcript, cand["start"], cand["end"]) if transcript else ""
        prompt = PROMPT.format(reasons=", ".join(cand["reasons"]) or "a loud moment", types=", ".join(TYPES),
                               said=said or "(nothing transcribed)")
        for attempt in range(4):
            wait = gap - (time.time() - last_call)
            if wait > 0:
                time.sleep(wait)
            last_call = time.time()
            try:
                raw = _ask(client, settings.gemini_model, preview.read_bytes(), prompt)
                write_json(cache, _clean(raw, cand["end"] - cand["start"]))
                log(f"judge: {cand['id']} rated")
                break
            except Exception as exc:
                text = str(exc)
                if attempt < 3 and any(code in text for code in ("429", "RESOURCE_EXHAUSTED", "500", "503", "UNAVAILABLE")):
                    log(f"judge: {cand['id']} busy or over the free limit, retrying in {30 * (attempt + 1)}s")
                    time.sleep(30 * (attempt + 1))
                    continue
                raise
        preview.unlink(missing_ok=True)


def merge(job, candidates, settings):
    """Blend Gemini's rating into the ranking and apply its trims. Candidates without a rating keep their
    detector score."""
    top = max((c["score"] for c in candidates), default=1.0) or 1.0
    for cand in candidates:
        cand["detector_score"] = round(100 * cand["score"] / top, 1)
        verdict = read_json(job.path("judge", f"{cand['id']}.json"))
        cand["judge"] = verdict
        if verdict:
            cand["final_score"] = round(0.6 * verdict["worth"] * 10 + 0.4 * cand["detector_score"], 1)
            cand["type"] = verdict["type"] if verdict["type"] != "nothing" else cand["type"]
            start = cand["start"] + verdict["start_trim_s"]
            end = cand["end"] - verdict["end_trim_s"]
            if end - start >= settings.min_clip_s:
                cand["start"], cand["end"] = round(start, 2), round(end, 2)
        else:
            cand["final_score"] = cand["detector_score"]
    return sorted(candidates, key=lambda c: -c["final_score"])
