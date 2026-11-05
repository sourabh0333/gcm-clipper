"""Brand-safety checks and the sponsor-safe bleep.

Flags, not blocks: the creator decides. Checks come from the rules that cost money or reach: swearing in
a title limits ads even though YouTube now allows it in the audio; betting and real-money-gaming mentions
are a legal problem in India since the August 2025 ban; Krafton's BGMI terms bar promoting other games; a
title that promises more than the clip shows is clickbait YouTube acts on. The bleep mutes Hinglish gaali
in the audio using the word-level transcript, for a second "sponsor-safe" export.
"""

import re

# Hinglish gaali in Latin and Devanagari, as stems so spelling variants match (chutiya, chutiye, chuttiyaan).
# Short English words are whole-word only, to keep "ass" out of "assault".
GAALI = re.compile(
    r"(?:\bch+u+t+i*y|\bbh?en+ ?ch|\bb?h?ehen ?ke\b|\bbhen ?ke\b|\bmadar ?ch|\bmaa ?ki ?ch|\bm+c\b|\bb+c\b|\bbsdk\b|"
    r"\bg+a+n+d+u*\b|\bgaand\b|\blawd|\blund\b|\bl+o+d+[aeu]\b|\bran+d+i\b|\bhar+am+i\b|\bkamin|\bkutt?e\b|\bsaal[ae]\b|"
    r"\bbhosd|\bbhosad|\bchod\b|\bchodu\b|\bteri maa\b|\bbakchod|"
    r"\bfuck|\bshit\b|\bbitch|\basshole\b|\bmotherf|\bwtf\b|"
    r"चुत|भेन|भैन|मादर|गांड|गाँड|लौड|लंड|रंडी|हरामी|भोसड|चोद|बकचोद|कमीन|कुत्त|साल[ाे])", re.I)
# Slurs that YouTube and sponsors treat more harshly than ordinary swearing.
SLURS = re.compile(r"\b(?:chakka|hijra|hijda|chhakka|katua|mulla|chamar|bhangi|retard)\b|छक्का|हिजड़ा|कटुआ|चमार|भंगी", re.I)
BETTING = re.compile(r"\b(?:betting|bet ?365|1 ?x ?bet|parimatch|stake\.com|satta|casino|rummy ?circle|teen ?patti|"
                     r"ludo ?(?:supreme|king)|jeeto ?paise|paise ?jeeto|earn ?money ?app|withdraw ?bonus|dream ?11|mpl\b|"
                     r"winzo|zupee|my ?11 ?circle|real ?money)", re.I)
OTHER_GAMES = re.compile(r"\b(?:free ?fire|garena|cod ?mobile|call of duty|valorant|fortnite|apex|pubg ?(?:new ?state|pc)|"
                         r"farlight|blood ?strike|indus)\b", re.I)
# Stat claims in a title that the clip's labels can check.
CLAIM_KILLS = re.compile(r"\b(\d+)\s*(?:kills?|finishes|finish|eliminations?|elims?)\b", re.I)
CLAIM_SQUAD = re.compile(r"\b1\s*v\s*(\d)\b", re.I)
CLAIM_WIN = re.compile(r"chicken|dinner|winner|wwcd|booyah", re.I)


def _hits(words, *patterns):
    """Indexes of words that are part of a match, matching across word boundaries ("bhen ke lode")."""
    words = list(words)
    text, spans, pos = "", [], 0
    for w in words:
        spans.append((pos, pos + len(w["word"])))
        text += w["word"] + " "
        pos += len(w["word"]) + 1
    hit = set()
    for pattern in patterns:
        for m in pattern.finditer(text):
            hit.update(i for i, (a, b) in enumerate(spans) if a < m.end() and b > m.start())
    return [words[i] for i in sorted(hit)]


def check(title, description, words=(), labels=None):
    """A list of flags for a clip; empty means nothing found. Each flag has kind, where, and the text."""
    flags = []
    for where, text in (("title", title or ""), ("description", description or "")):
        for kind, pattern in (("profanity", GAALI), ("slur", SLURS), ("betting", BETTING), ("other_game", OTHER_GAMES)):
            for m in pattern.finditer(text):
                flags.append({"kind": kind, "where": where, "text": m.group(0)})
    words = list(words)
    spoken = _hits(words, GAALI, SLURS)
    if spoken:
        flags.append({"kind": "profanity", "where": "audio", "text": ", ".join(dict.fromkeys(w["word"] for w in spoken)),
                      "count": len(spoken)})
    bet = _hits(words, BETTING)
    if bet:
        flags.append({"kind": "betting", "where": "audio", "text": " ".join(w["word"] for w in bet)})
    if labels and title:
        kills = labels.get("kills") or 0
        m = CLAIM_KILLS.search(title)
        if m and int(m.group(1)) > kills:
            flags.append({"kind": "overclaim", "where": "title", "text": f"{m.group(0)} but the clip has {kills}"})
        m = CLAIM_SQUAD.search(title)
        if m and int(m.group(1)) > max(kills, 1):
            flags.append({"kind": "overclaim", "where": "title", "text": f"{m.group(0)} but the clip has {kills} kills"})
        if CLAIM_WIN.search(title) and not labels.get("win"):
            flags.append({"kind": "overclaim", "where": "title", "text": "says win, no chicken dinner in the clip"})
    return flags


def mute_spans(words, pad_s=0.08):
    """[(start, end)] in clip seconds to mute for a sponsor-safe export, merged when they touch."""
    spans = []
    for w in _hits(words, GAALI, SLURS):
        a, b = max(0.0, w["start"] - pad_s), w["end"] + pad_s
        if spans and a <= spans[-1][1]:
            spans[-1] = (spans[-1][0], max(spans[-1][1], b))
        else:
            spans.append((a, b))
    return [(round(a, 2), round(b, 2)) for a, b in spans]


def mute_filter(spans):
    """An ffmpeg audio filter that silences the spans."""
    return ",".join(f"volume=enable='between(t,{a},{b})':volume=0" for a, b in spans)


def sponsor_safe(flags):
    return not any(f["kind"] in ("profanity", "slur", "betting") for f in flags)
