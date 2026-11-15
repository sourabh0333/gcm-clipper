# Highlights Stage 2: the comedy highlight

Written 15 November 2026, after the owner closed Stage 1 ("for now it's okay, moving to next part"). Built on the JokerClips research ([research_notes/BGMI highlight channels deep study/joker_deep.md](../research_notes/BGMI%20highlight%20channels%20deep%20study/joker_deep.md) section 6, [research_notes/BGMI creators content A to Z/jokerclips.md](../research_notes/BGMI%20creators%20content%20A%20to%20Z/jokerclips.md)), the viewer study ([reports/What holds BGMI viewers.md](../reports/What%20holds%20BGMI%20viewers.md)), and a check of the test streams on 15 Nov. **Nothing here is built until the owner approves this plan.**

**Stage 2 goal:** from one stream, Kaatclip makes **a funny-session highlight**: the stream's best banter, roasts, rage and fails, in stream order, with the face zoomed in on every punchline and the key line written on screen. This is the JokerClips format (159 videos, median 185K views, its steady earner). It is offered next to the kill highlight, with its own Shorts, and nothing posts by itself.

**Done when:**
1. On Joker's own streams, read through their captions only, Kaatclip's picks overlap what JokerClips' editor kept (section 4).
2. On GtxPreet, the comedy cut is a watchable 6-9 minute video: every unit runs from the setup to the punchline, no sentence is cut, and the face is on screen for the jokes.
3. The owner, watching it on the phone, says it is funny and the kind of video he meant.

---

## 1. What the check found (15 Nov)

| # | Finding | Effect on Stage 2 |
|---|---|---|
| C-1 | **Only one test stream talks enough.** GtxPreet runs at 95 words a minute, with 30 Gemini moments (24 inside matches) and 420 shouts or laughs. DIPENDU runs at 36 words a minute with 6 moments. ANJI's transcript is marked broken (22% coverage), with no moments. Joker's streams run at 107-156 words a minute. | GtxPreet is the only full test. The **real test is Joker's own streams, read through their YouTube captions** (C-2). A beta creator's talk-heavy stream is the final check. |
| C-2 | **The truth already exists, without any footage.** The research matched 25 JokerClips videos to their source streams word by word through captions. That shows exactly which stream minutes the editor kept: 15-30 units, median 13 s, mostly in stream order, from 30-160 minutes of a stream. | Captions (allowed: no video or audio) of about 8 pairs become a test set. The unit finder runs on caption text and laugh tags, and its picks are scored against the editor's. |
| C-3 | **Gemini finds too few units for 8 minutes.** Today's talk pass returns about 1 moment per 6 minutes (30 in 3.1 h), median 17 s. An 8-minute comedy cut needs 15-30 units from about 2 hours. | A denser second pass over the chosen window only: every funny unit, with its setup start, punchline end, the key line and a one-word label. About 6 free-tier requests a stream, cached. |
| C-4 | **Most parts already exist.** The stream map (BGMI parts, matches, deaths, results), the talk scores, shouts and laughs, markers ("clip that", !clip), the transcript, the facecam box, punch-ins held for the sentence, subtitles, cards, the cold open and the render lane all come from Stage 1. | Stage 2 is a new unit finder and a new cut (`comedy.py`), rendered by the Stage 1 highlight renderer, plus a few new looks. |
| C-5 | **Laughter alone misleads.** In Joker's streams laughter is 2-4 times denser in GTA RP and Among Us than in BGMI, and piles up late in the stream. | Units come only from the BGMI parts of the map, and laughter is scored against the BGMI part's own normal level. |
| C-6 | **Speakers can't be told apart.** The transcript is one voice track: the streamer and teammates on voice chat mixed. The viewer study says a teammate's reply and a named person lift a moment most. | Not in Stage 2 (decision 8). A back-and-forth (several short lines in a few seconds) is used as the stand-in for a reply. |

---

## 2. Decisions for Stage 2

Defaults from the research. **The owner answers the 8 questions in section 5**; until then these hold.

1. **What a comedy highlight is.** One stream's BGMI part, in stream order:
   - an optional **"IN THIS VIDEO" teaser** of 10-22 s: 3-5 punchlines from the body, subtitled;
   - **15-30 units**, each from its trigger (a death, a knock, a question, a roast opener, a donation read-out, a result screen) to the punchline plus 0-3 s; a roast or rant kept whole up to about 45 s, a funny fight up to about 110 s;
   - units less than 30 s apart in the stream joined with small trims;
   - about **one big laugh every 60-90 s**;
   - the ending on the last punchline or the face reacting, never on a quiet fight.
2. **Where it comes from.** The first ~120 minutes of the stream's BGMI part. If that gives under ~6 minutes, the best block from another stream of the same creator (last 3 weeks) is added after a **"THE NEXT DAY…"** card.
3. **Single-match mode.** When one match is dense with talk (speech above ~80%, 6+ laughs) and lasts 8-12 minutes, it is kept almost whole, dead seconds cut, ending on its result screen.
4. **The look.** The stream layout as streamed, 16:9:
   - the face **crop-zoomed** for every unit's punchline, held for the sentence (JokerClips: 25-45% of frames);
   - **one subtitle per unit** for the key line, big caps at the top for the biggest lines;
   - **Kaatclip's own stickers**: an emoji or a one-word label ("CHAT", "RAGE", a name) for 1-3 s, 3-6 a video. No film or TV meme clips (copyright);
   - "2 SECONDS LATER…" cards for jumps inside a match; the result screens kept.
5. **Length:** about 8:00-8:15 when the material allows (JokerClips' rule: 69 of 133 sessions are 480-489 s; 8:00 is where YouTube allows mid-roll ads), shorter when it doesn't. Never padded with weak units.
6. **Shorts:** 2-4 from the best units (person moments first, as in Stage 1), 15-60 s, stacked layout, face alone while talking.
7. **Titles and thumbnail:** "[streamer] & [teammate] [conflict word] 😂" when names are said with confidence, otherwise the best line. The thumbnail's speech bubble quotes the top punchline (rule 48 of the viewer study).
8. **Which video is suggested.** The stream page offers both the kill highlight and the comedy cut when the stream has enough of each. The one the stream is richer in is listed first.

---

## 3. Steps

Each step ends with its own check, and BUILD_NOTES is updated after each.

| Step | What | How | Checked by |
|---|---|---|---|
| **S2.1 Caption truth set** | What JokerClips' editor kept | About 8 JokerClips session videos and their source streams, from the research's matches. Their auto-captions only (no video or audio). The kept stream spans are saved as `tests/data/comedy/*.json`: times, word counts and laugh tags, with no stream text beyond short cue words. | Each pair's matched spans re-checked against the research's tables |
| **S2.2 Unit finder** | `aigcm/comedy.py` | Scores every second of the BGMI parts: speech density against the stream's own level, back-and-forth, laughs and shouts within 3 s of a line, laugh words, Hinglish triggers and comedy cues (research rules 1-5), deaths and results from the map, markers, and the existing talk moments. Builds units trigger → punchline + 0-3 s, keeps rants whole to 45 s, joins units under 30 s apart, trims silences over 5 s. Works on captions-only input too, for S2.1. | Scored on the truth set: how many of the editor's units are found, and how many of the picks the editor also kept |
| **S2.3 Gemini unit pass** | Denser units | Over the chosen window only: every funny unit with its setup start, punchline end, key line, one-word label and type. Free tier, one request per 20 minutes, cached in `comedy.json`. Its units are merged with S2.2's. | The truth set again, with and without Gemini |
| **S2.4 Selection and cut** | The piece list | The window (decision 2), 15-30 units, about one big laugh every 60-90 s, stream order, the hook unit, single-match mode, the "THE NEXT DAY…" compilation from leftovers. Pieces carry their punch-ins, subtitles and stickers. | Unit tests; Claude reads GtxPreet's cut list against the transcript |
| **S2.5 The look** | Render | The Stage 1 renderer, plus big top captions, Kaatclip's own sticker labels and the time cards. The teaser from body punchlines; the punchline ending. | GtxPreet rendered and checked by frames |
| **S2.6 Shorts, titles, thumbnail** | The batch | Shorts from the best units; the comedy title; the speech-bubble thumbnail; suggested posting times in the calendar, as drafts. | The Shorts play and open in the editor; the batch lands in Posts |
| **S2.7 Phone** | Stream page | A **Comedy** card next to the kill highlight: the video, its units each with an on/off switch, Make again, titles, Plan the posts. | Web tests; checked at phone size on a database copy |
| **S2.8 Owner check** | The real test | The owner watches the GtxPreet comedy cut and its Shorts on the phone. | The owner's verdict in BUILD_NOTES |

The order is S2.1 → S2.3 first (the units must match a real editor's before anything is cut), then S2.4 → S2.7.

---

## 4. How "good" is measured

- **The units**, on the caption truth set:
  - at least half of the editor's kept units overlap one of Kaatclip's picks;
  - at least half of Kaatclip's picks overlap something the editor kept (the editor drops good material too, so this is a floor, not a target);
  - unit edges within about 3 s of the editor's at the punchline end.
- **The cut**, checked by Claude on GtxPreet:
  - no unit starts after its setup or ends before its punchline;
  - no cut inside a word;
  - no 90 s without a laugh, shout or rated line;
  - the face is on screen for the punchlines.
- **The owner's verdict** decides: is it funny, would a streamer post it?

---

## 5. Questions for the owner (defaults in brackets)

1. **Length:** aim for 8 minutes when there's enough, or just what the material gives? *(Aim for 8:00-8:15, never padded with weak units.)*
2. **Source window:** only the first ~2 hours of BGMI, or the whole stream? *(First ~2 hours; the editor rarely goes later.)*
3. **Two-stream videos:** add another stream's best part after "THE NEXT DAY…" when one stream is thin? *(Yes, same creator, last 3 weeks.)*
4. **Stickers:** Kaatclip's own emoji and word labels only, no film or TV meme clips? *(Yes, own stickers only, for copyright.)*
5. **Face zoom on every joke:** yes, or only the biggest ones? *(Every unit's punchline, held for the sentence.)*
6. **Which video first:** the kill highlight, the comedy cut, or whichever the stream is richer in? *(Whichever the stream is richer in; both offered.)*
7. **Names in titles:** only when a name is said clearly, otherwise the best line? *(Yes.)*
8. **Telling voices apart** (streamer vs teammates): skip for now? *(Skip; it is heavy to run on the laptop. A quick back-and-forth stands in for a reply.)*

---

## 6. Risks and what the owner needs to do

| Risk | What we do |
|---|---|
| Only one test stream (GtxPreet) is talk-heavy, and it is another streamer's | Joker's captions are the main measure; GtxPreet is checked by frames and never posted. **Owner task:** ask a talk-heavy beta creator for one full OBS recording. |
| Whisper's Hinglish transcript misses words, so units and subtitles drift | Units lean on sound (laughs, shouts, speech density) as much as words; subtitles only on lines the transcript caught well. ANJI-like broken transcripts get no comedy cut, and the page says why. |
| Humour is hard to judge by rules | Gemini's unit pass and the creator's own markers ("clip that", !clip) carry most of the weight; the creator can switch any unit off and make it again. |
| Gemini free tier limits | About 6 extra requests a stream, cached; without a key the rules alone make the cut. |
| Comedy cuts tempt meme clips from films and TV | Not used. Own stickers only. |

**Owner tasks in Stage 2:** answer the 8 questions (or keep the defaults); at S2.8 watch the comedy cut on the phone; ask a talk-heavy beta creator for one full recording.
