# M3 Studio: reviewed plan

Written 9 November 2026 before any M3 code, after reviewing the [master plan](GCM%20Clipper%20master%20plan.md) section 4.4 and the M3 row, the engine's cutting code (`render.py`, `captions.py`, `media.py`), the M2 platform, and the outside facts below. Each finding marked "tested" was checked on the laptop on 9 Nov. Progress is tracked in [ai-gcm/BUILD_NOTES.md](../ai-gcm/BUILD_NOTES.md).

**M3 goal (from the master plan):** edit model, library, editor with length presets, layouts and zoom, black-band hook and captions, brand kit, thumbnails and cover frames, compilation with commentary and chapters, sound safety, export. **Done when** every 4.4 "done when" is met and phone-tested.

---

## 1. What the review found

| # | Finding | Effect on M3 |
|---|---|---|
| S-R1 | **Sources are deleted 14 days after clips are made** (`source_keep_days`), but an edit list needs the source to re-render. Keeping whole 1.5–4 GB sources is too much disk. | When a clip is **kept**, the worker saves a **working window** of the source around it (stream copy, no re-encode, a few seconds of work). Edits and exports use the window, so the 3-hour source can still be deleted. The window covers the clip ±60 s and its whole fight, up to 4 minutes. |
| S-R2 | **A phone can't preview from the source.** Tested: a 4-minute 540p preview copy takes 38 s and is 51 MB. Making one for all 12 clips of every stream would add 8 minutes per stream. | Preview copies (540p, 1 keyframe per second for quick seeking, about 1 Mbps) are made **only for kept clips**, in the background right after Keep, with a filmstrip image and a sound wave for the timeline. |
| S-R3 | **ffmpeg's subtitle renderer draws Hindi correctly but emoji only as flat outlines** in the text colour, not in colour (tested with the gyan.dev build, libass with HarfBuzz). Pillow here has no complex-text support (`raqm` off), so it can't draw Hindi. | Text (hook, captions, lower-third) is drawn by libass. Each emoji is drawn as a **colour image** from the Noto Emoji set (Apache 2.0) at the spot libass leaves for it: the text is rendered once with a uniquely coloured placeholder box where the emoji goes, its pixels give the exact place and size, then the final text leaves the box clear and the emoji image is laid over it. |
| S-R4 | **Preview and export must look the same**, but the browser and ffmpeg draw differently. | The hook band is rendered **on the server as a PNG** (a single ffmpeg frame, under 0.3 s) and the editor shows that same image. Video panels are drawn in the browser on one canvas from one video element (`drawImage` with the same crop numbers ffmpeg uses), so layouts match exactly. Word captions use the same bundled fonts in both. |
| S-R5 | **Fonts must not depend on Windows.** Captions use "Nirmala UI" today, which phones and a later Linux worker don't have. | Bundle open fonts in the repo: **Anton** (heavy condensed caps for hooks), **Noto Sans Devanagari** (Hindi), both OFL. ffmpeg gets them through `fontsdir`; the web app serves them with `@font-face`. |
| S-R6 | **Zoom on the kill needs a crop that changes size**, which ffmpeg's crop filter can't do frame by frame. | Tested: `scale` with `eval=frame` and a time-based width, then a fixed crop, gives a smooth zoom (120 frames, constant 1280×720 out). The kill times are already known from the HUD scan (`events`, `anchor`). |
| S-R7 | **Exports would wait an hour behind a stream job**: the worker runs one stream at a time. | A **second lane** in the worker: a render thread with its own queue table (preview copies, exports, thumbnails, compilations). It runs beside a stream job with ffmpeg limited to 3 of the laptop's 8 threads, so a 45 s export takes well under a minute and the stream job slows only a little. |
| S-R8 | **Two cutting paths would drift apart**: the engine's `render.py` and the new studio renderer. | The studio renderer becomes the only one. The engine's render step builds each clip's **default edit** and renders it through the studio renderer, so the swipe video already looks like the final Short. Done once hooks and captions work (M3.5). |
| S-R9 | **Shorts over 1 minute with any active Content ID claim are blocked worldwide**; under 1 minute they are not (YouTube Help, "three-minute Shorts"). Streamers often play background music. | Sound safety uses the sound detector's "Music" score: a clip with music gets a flag, and a clip over 60 s with music gets a strong warning and a one-tap "cut to 59 s". No added music anywhere; optional sound effects come from a bundled CC0 set (Kenney). |
| S-R10 | **Compilations of the creator's own streams are not "reused content".** YouTube's July 2025 change renamed "repetitious" to "inauthentic content"; reused-content rules target other people's footage with little added value. | Keep the plan's commentary clips, hook captions and chapters, because they make a better video, not because the policy forces them. Chapters go in the description (first at 0:00, at least 3, each at least 10 s). |
| S-R11 | **User text must never reach an ffmpeg filter graph**, where a quote or a colon could change the command. | All text goes through files (ASS subtitle files, PNG images). ASS text has `{`, `}` and `\` neutralised. Uploaded logos are re-encoded through Pillow; intro and outro videos are checked with ffprobe and re-encoded. |
| S-R12 | **What's free and already installed:** MediaPipe 1.2.0 (face detection for the facecam box, selfie segmentation for thumbnail cut-outs; Apache 2.0, small model files), OpenCV 5.0, SQLite with FTS5, ffmpeg with libass, HarfBuzz and x264. Android Chrome has canvas `filter` (blur fill), `requestVideoFrameCallback` and file sharing through the Web Share API. | No new paid service and no new heavy dependency. |
| S-R13 | **"Watch 20 top clips before S3"** (master plan section 11) can't be done from still images. | An owner task of about 15 minutes, with a short checklist (section 5). M3.4 uses sensible defaults until then. |

---

## 2. Decisions taken in this review

1. **The edit list** (JSON, version 1, stored per clip with its last 20 versions) holds: the working window, segments (in, out, speed), the layout as panels (each a crop of the source drawn into a rectangle of the 1080×1920 canvas), zooms (time, length, strength, centre), the hook (text, emoji, colour), captions (on or off, script, edited words), brand items (lower-third, intro, outro), the cover frame time, sound effects, and sponsor-safe. Undo works in the browser; Save writes a new version.
2. **Every clip gets a default edit** made from what the engine knows: layout from the source shape and the facecam box, hook from the chosen title, captions on for talk clips, zoom at each kill, length preset from the fight length. So old clips open as projects too.
3. **Length presets:** "moment" 20–45 s around the events; "full fight" 60–120 s covering the whole fight (events chained with gaps under 30 s, within one match); up to 180 s by hand.
4. **Layout templates:** band (black hook band, gameplay full width, blurred or black below), facecam top (cam 35–45% + gameplay), blur (gameplay over a blurred copy), native (vertical streams as they are). Each is just a starting set of panels the creator can move and resize.
5. **Captions:** word-level, 3 words at a time, in the transcript's script, on talk clips by default. Converting between Latin Hinglish and Devanagari uses Gemini (a few hundred words per clip, inside the free tier), with word editing for fixes.
6. **Library replaces the Kept tab:** all clips with a poster image, filters (stream, type, decision, flag, edited, exported) and search by what was said (SQLite FTS5).
7. **Export:** rendered files stay 30 days in the stream's folder. The phone can download, share through Android's share sheet, download all as a zip, and copy the title and description.
8. **Exports and preview copies count toward the 20 GB free-disk guard**; a kept clip's working window is deleted with the stream.

---

## 3. Steps

| Step | What | Done when |
|---|---|---|
| **M3.1 Edit model and renderer** | Edits table and migration; working windows and preview copies for kept clips (and a backfill for existing kept clips); the default edit; the studio renderer (panels, segments, speed, zoom, sponsor-safe mute); the worker's render lane and its queue; API to read and save edits and request exports | An old clip reopens as an editable project; its default export plays correctly |
| **M3.2 Library** | Poster per clip; library page with filters and spoken-word search; replaces Kept | 100+ clips browse smoothly on a phone |
| **M3.3 Editor basics and export** | Editor page: canvas preview, timeline with filmstrip and sound wave, trim, split, delete part, speed up a part, length presets, undo, save; export with download, share, zip and copy text | A clip is re-cut in under a minute on a phone and shared from it |
| **M3.4 Layouts and zoom** | Facecam box found automatically (MediaPipe faces + the overlay's steady edges), adjustable by drag; the four templates; zoom on each kill with its own control | Correct on the 3 test streams and 3 new ones |
| **M3.5 Hook and captions** | Server-rendered hook band with colour emoji; captions in Latin or Devanagari with word editing; bundled fonts; the engine's render step switched to the studio renderer | Looks right on vertical and landscape sources |
| **M3.6 Brand kit** | Logo, colours, caption style, intro and outro, standard description, hashtags, game disclaimer, lower-third (name, UPI ID, Instagram); applied to default edits | Set once, used on every export |
| **M3.7 Thumbnails and cover frames** | Cover-frame picker for Shorts; compilation thumbnails from a face cut-out plus 2–3 words of stat text, or the best kill frame without a cam; 3 titles and 3 thumbnails for long videos | Every long video has 3 and 3; every Short has a cover frame |
| **M3.8 Weekly compilation** | Pick the week's best (or by hand), full-fight cuts with talk clips between them, hook captions, chapters in the description, 16:9; a 9:16 version up to 3 minutes | A compilation renders from 10 clips with chapters and commentary |
| **M3.9 Sound safety** | Music flag from the sound detector; the over-60-s warning and "cut to 59 s"; bundled CC0 sound effects | No added track can cause a claim |
| **M3.10 Phone check** | Every done-when above checked on the owner's phone over the Funnel address | M3 done |

---

## 4. Versions and new files

No new Python or web packages. New bundled files, all free to redistribute: Anton and Noto Sans Devanagari fonts (SIL Open Font License), a small set of Noto Emoji PNGs (Apache 2.0), a few Kenney sound effects (CC0), and MediaPipe's face detector and selfie segmenter models (Apache 2.0, downloaded once into `models/`, not committed).

---

## 5. What the owner does for M3 (all free)

1. **Strict swipes** on the five accuracy streams and GtxPreet (still open from M1). Kept clips are the ones the editor works on first.
2. **Watch 20 top BGMI Shorts** from big Indian channels (about 15 minutes) and note for each: is there a zoom on the kill, a speed-up, added music, facecam on top, a text band on top. A plain list in chat is enough. Before M3.4 if possible.
3. **Try the editor on the phone** at each step's end, and say what feels slow or confusing.

---

## 6. Changes to the master plan from this review

- M3 row links this plan.
- Section 4.4 "Captions and hook": emoji are drawn as images (S-R3).
- Section 4.4 "Sound safety": the 60-second Content ID block (S-R9).
- Section 5 "Editing": working windows for kept clips, so sources can still be deleted after 14 days (S-R1).
