# Prototype test results

Three public BGMI livestreams, tested 26–28 October 2026 on a laptop (Intel i5-11300H, 8 GB RAM, no graphics card), with no Gemini key. Downloaded only for private testing.

## Summary

| Stream | Layout | Section | Kills found | Fake kills | Time (HUD / captions / clips) |
|---|---|---|---|---|---|
| GtxPreet (2.1M subscribers) | Landscape, facecam, donation bar, QR code | 40 min | 7 in one match, plus Ace Eliminator | 0 | 13 / 5 / 2 min |
| ANJI is LIVE | Vertical: facecam top, small gameplay window, banners below | 30 min | 3 | 0 | 6 / 5 / 1 min |
| DIPENDUisLIVE | Vertical: gameplay top, HUD counters moved to a large bar, facecam below | 30 min | 8 across 3 matches | 0 seen | 20 / 1 / 2 min |

Downloading a 30–40 minute section at 720p took a further 15–20 minutes on the test connection.

"Fake kills" means none were found when the event list was checked against the HUD frames. There is no hand-labelled list of every real kill yet, so a missed kill would not show up here.

## What works

- **The Eliminations counter is the reliable kill signal.** Reading it every half second, accepting a new value only when two reads agree, and treating the counter as never going down within a match gives clean kill timestamps on all three layouts.
- **It finds the counter in any layout.** It looks in the top-left corner first, then searches the whole frame at 2× if needed. This handled a gameplay window inside a vertical stream (ANJI) and counters the streamer had moved and enlarged (DIPENDU).
- **Spectating is handled.** When the streamer dies, BGMI shows "Spectating" and the counter switches to a teammate's. It is ignored while that text is on screen. A reset to 0 counts only after the Remaining counter jumps to a fresh lobby, or holds for 10 seconds when the layout hides it.
- **Clips include the fight.** A 12-second lead-in before the first kill and a 6-second tail give 15–38 second clips that show the build-up, the kill and the reaction.
- **Vertical streams are rendered as they are** (they are already Shorts); landscape streams go over a blurred fill.

## Problems found and fixed during testing

| Problem | Cause | Fix |
|---|---|---|
| 6 fake kills on GtxPreet | Counter showed a teammate's eliminations while spectating | Ignore the counter while "Spectating" is on screen; resets need a new lobby |
| "Painkillers" and mission text counted as kills | Matching any "kill" text | Only specific phrases count; the counter is the kill source |
| OCR took about 4 s per read | RapidOCR enlarged small crops to 736 px | Cap the long side; read digit boxes without text detection |
| "0" never read | The Chinese/English model reads BGMI's square 0 as 口 or 品 | Count those shapes as 0 and decode digits only |
| Kill counted twice on ANJI | 2 s flicker to 0 with no Remaining counter in the layout | Without a lobby signal, a reset must hold for 10 s |
| Clips showed only the aftermath | The counter changes at the kill; the lead-in was 4 s | 12 s lead-in, 15 s minimum |
| Vertical streams downloaded at 360×640 | Download limited the height, not the shorter side | Limit the shorter side, so vertical streams come down at 720×1280 |
| HUD reading took 31 min for 30 min of vertical video (ANJI) | Whole-frame "Spectating" check every 4 s | Check only when the counter seems to change. The next vertical stream (DIPENDU) took 20 min: better, but still about 3× slower than landscape |

## Product findings

- **Two of the three streams picked at random were vertical "Shorts live" streams.** Vertical streaming looks common among Indian BGMI creators. Their clips need no reframing, but each streamer's layout is different, and YouTube's own livestream highlights target this format.
- **Streams carry heavy overlays** (donation bars, QR codes, goal banners, Super Chat alerts). They don't affect detection, but they take screen space in landscape clips.
- **Every kill is an event, but not every kill is a good clip.** Without a judgement pass (the optional Gemini step), single kills rank close together, and "loud reaction" moments are hit and miss.

## Known weaknesses

- **Captions:** Whisper `small` writes garbled Hindi in Devanagari. A Hinglish model (for example Oriserve's Whisper-Hindi2Hinglish) or Sarvam is needed.
- **No judgement of how good a moment looks** without a Gemini key, so funny moments and clutches (as opposed to kills) are not recognised.
- **Knocks are not detected**, only kills; knock messages were not reliably visible in the test footage.
- **Speed:** a full 3–4 hour stream would take 1–3 hours end to end on this laptop.
- **Only three streams so far** and no hand-labelled ground truth, so recall (kills missed) is not measured.
