"""Converts caption words between Hinglish in Latin letters and Hindi in Devanagari, with Gemini (a few hundred
words per clip, well inside the free tier; M3 plan, decision 5). Word by word, so each converted word
keeps its timing; the creator fixes any word by hand afterwards."""

import json
import os

PROMPT = """You convert the words of a Hindi/Hinglish gaming livestream transcript between scripts.
Target: {target}.
Rules: return a JSON object {{"words": [...]}} with exactly {count} strings, one per input word, in the same order.
Keep English gaming words (kill, knock, zone, clutch, squad, bro) as players write them in the target script.
Use the common way young Indian gamers write Hinglish (yaar, bhai, kya, hai), not formal transliteration.
Keep numbers and emoji unchanged. Never merge, split, add or drop words.
Input words: {words}"""

TARGETS = {"latin": "Hinglish in Latin (Roman) letters",
           "devanagari": "Hindi in Devanagari script (English words written as Hindi speakers would, e.g. किल, ज़ोन)"}
MAX_WORDS = 600


class Unavailable(RuntimeError):
    pass


def convert(words, script, api_key=None, model=None):
    """The same number of words in the target script. Raises Unavailable when Gemini can't be used."""
    if script not in TARGETS:
        raise ValueError("script must be latin or devanagari")
    if not words:
        return []
    if len(words) > MAX_WORDS:
        raise ValueError(f"at most {MAX_WORDS} words at a time")
    api_key = api_key or os.environ.get("GEMINI_API_KEY", "").strip()
    model = model or os.environ.get("AIGCM_GEMINI_MODEL", "gemini-3.5-flash-lite")
    if not api_key:
        raise Unavailable("Script conversion needs the Gemini key on the laptop.")
    try:
        from google import genai
        from google.genai import types
    except ImportError as exc:
        raise Unavailable("Script conversion isn't installed on this computer.") from exc
    client = genai.Client(api_key=api_key)
    prompt = PROMPT.format(target=TARGETS[script], count=len(words), words=json.dumps(words, ensure_ascii=False))
    try:
        response = client.models.generate_content(
            model=model, contents=[prompt],
            config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.0))
        out = json.loads(response.text).get("words")
    except Exception as exc:   # busy, quota, bad JSON: the creator can try again
        raise Unavailable(f"Gemini didn't answer ({type(exc).__name__}); try again in a minute.") from exc
    if not isinstance(out, list) or len(out) != len(words):
        raise Unavailable("Gemini returned a different number of words; try again.")
    return [str(w).strip()[:40] for w in out]
