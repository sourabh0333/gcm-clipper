# BGMI open questions: desk check

Date checked: 2026-10-26. Desk research only (web pages, public docs, public APIs). No accounts created, nobody contacted, nothing bought.

Companion to `reports/BGMI AI clipper market validation.md`. This file does not repeat that report. It closes, or marks as still open, the gaps the report left.

Source labels used below:
- **[Official]**: the vendor's or platform's own docs, help centre, terms or model card.
- **[Vendor marketing]**: the vendor's own marketing page. Official, but promotional.
- **[Secondhand]**: press, blogs, third-party roundups, community trackers.
- **[Derived]**: my own calculation from official figures.

Corrections to the existing report are marked **Correction**.

---

## 1. YouTube livestream AI highlights / "Live recap" Shorts

**Answer:** Whether it is live in India could not be confirmed. YouTube's own help pages limit automatic "Short highlights" to vertical streams made in the YouTube mobile app and exclude screencasts, which rules out the two usual BGMI setups (phone screencast, and PC/OBS encoder streams). Hindi support and how moments are picked are not documented.

### Eligibility: the strongest finding [Official]
YouTube Help, "Promote your live stream", lists when a stream is eligible for a Short highlight ([support.google.com/youtube/answer/2524542](https://support.google.com/youtube/answer/2524542?hl=en)):
- "The live stream must be between 10 minutes and 12 hours."
- "The stream must be in a vertical format and streamed using the YouTube mobile app."
- "The stream cannot be a screencast."
- "The stream has chat enabled."
- Not set as "Made for Kids", and the stream must meet safety standards.

YouTube Help, "Create a live stream on mobile": when a mobile stream ends, the recap offers a Short highlight "automatically pulled from your live stream". It is saved as a private video by default, and the option "may depend on the eligibility of the live stream" ([answer/9228390](https://support.google.com/youtube/answer/9228390?hl=en)). Going live on mobile at all needs 50+ subscribers and a channel with no live-streaming restrictions in the last 90 days (same page).

What this means for BGMI (inference, not stated by YouTube):
- Most BGMI streamers either screencast from the phone, or capture the phone into OBS on a PC and stream horizontally through an encoder. Neither is a vertical camera stream from the YouTube app, so under the documented rules neither qualifies.
- None of the help pages mentions a subscriber minimum or YPP membership for highlights specifically. "Desktop" is not mentioned either, but "streamed using the YouTube mobile app" excludes encoder and webcam streams in practice.
- Because "chat enabled" is required, chat activity is probably an input to moment selection. YouTube does not say this.

### Announcement and rollout status
- [Official] YouTube Blog, 16 Sept 2025: the feature "finds the most compelling moments from the livestream and automatically creates ready-to-share Shorts". It gives no regions, eligibility or dates and links to a Community post for timing ([blog.youtube/news-and-events/live-updates](https://blog.youtube/news-and-events/live-updates/); Community post [support.google.com/youtube/thread/372291417](https://support.google.com/youtube/thread/372291417), which renders client-side and could not be read).
- [Secondhand] Social Media Today, 23 Sept 2025: in testing, with creators previewing the Short "in the recap screen upon ending the stream" in the mobile app ([socialmediatoday.com](https://www.socialmediatoday.com/news/youtube-adds-reply-filters-live-stream-highlights-shorts/760959/)). Dexerto (16 Sept 2025) and The Hans India (17 Sept 2025) repeat the announcement with no India, language or eligibility detail ([Dexerto](https://www.dexerto.com/youtube/youtube-launches-ai-powered-highlight-tool-to-automatically-create-stream-clips-3252018/); [Hans India](https://www.thehansindia.com/technology/tech-news/youtube-unveils-biggest-live-streaming-overhaul-with-ai-highlights-dual-layouts-and-interactive-tools-1007309)).
- [Official] The current YouTube "Creator updates" log (checked today) has no 2026 entry that widens highlights to encoder or desktop streams. The recent live-stream entries are Live Practice Mode and Playables on vertical streams ([answer/9072033](https://support.google.com/youtube/answer/9072033?hl=en)). A search snippet showed a Sept 2025 entry ("a Short pulled automatically from a mobile live stream"), but it has rolled off the live page.
- [Secondhand] Made on YouTube 2026 (23 Sept 2026) coverage aimed at Indian creators does not mention live highlights, and says most updates "weren't launched with India-specific dates" ([socialnationnow.com](https://www.socialnationnow.com/made-on-youtube-2026-new-features-indian-creators)).

### Hindi/Hinglish, gaming, moment selection
- Hindi/Hinglish: **not confirmed** by any source. The only related official live AI feature, the chat summary, is described as experimental and summarises chat rather than stream content ([answer/15270973](https://support.google.com/youtube/answer/15270973)).
- Gaming: **not confirmed**. The screencast exclusion is the only official statement that touches gameplay streams, and it points against them.
- Moment selection: YouTube says only "most compelling moments". The report's existing claim that it uses watch-time spikes and chat comes from one secondhand source and is still unverified.

### What could not be checked
- Reddit (blocked for this tool), Creator Insider transcripts and Team YouTube posts on X: none found that addresses India, Hindi or gaming. No first-hand creator reports of using the feature on a BGMI stream were found.
- **Still worth doing (validation step 1):** run a 10+ minute vertical, chat-enabled mobile *camera* stream and a screencast BGMI stream from an Indian channel with 50+ subscribers, and compare the recap screens.

---

## 2. Krafton BGMI terms of service and creator policy

**Answer:** Yes. Creators may make and monetise BGMI gameplay videos and streams on free-to-view platforms (ads, donations, free-to-view channel memberships), but not paywalled content, not sold or licensed content, and not content that promotes non-Krafton games. Nothing in the terms targets offline tools that process recorded footage. The anti-cheat clause covers programs that "affect the Game", and the closest risks for AI-GCM are the bans on commercial use without permission and on sold or licensed clips.

The documents were pulled directly from battlegroundsmobileindia.com (WebFetch got 403; a plain browser request worked). [Official]

### BGMI Terms of Service (effective/displayed date Jun 30, 2023)
URL: [battlegroundsmobileindia.com/terms](https://www.battlegroundsmobileindia.com/terms) (canonical `/en/terms_of_service/bgmi`; also served at terms.krafton.com).
- §1 Limited License grants a revocable right to "create live or recorded gameplay videos that leverage assets from the Game" ("Gameplay Videos"), and to distribute them on sites that let others view "without any charge of any kind".
- §1: you "may not license or sublicense your Gameplay Video to anyone else for a fee" without written authorisation.
- §1 requires a disclaimer at the start of a video, or near a live stream: "This video is subject to the Game's Terms of Service and was not endorsed or sponsored by KRAFTON INC." (Mandatory text, quoted in full because it must be reproduced verbatim.)
- §1: Krafton may end this licence "for any reason (or for no reason at all)".
- §3 Prohibited Uses: the Game is for "personal, non-commercial and entertainment purposes". §3(a) bars commercial exploitation "without written permission". Conduct "authorized in the Content Creation Guideline" is excepted.
- §3(b) bars use "in connection with unauthorized software, applications, services, or Devices".
- §3(w) bars "unauthorized third-party programs or Devices that may affect the Game", listing hacks, bots, macros and memory readers.
- §3(f) bars accessing or downloading content from the Game or Services with crawlers or "data mining tools". This is aimed at the game and service, not at video files.
- Governing law is the Republic of Korea (§14).

### BGMI Content Creation Guideline (Dec 13, 2023)
URL: [battlegroundsmobileindia.com/ccg](https://www.battlegroundsmobileindia.com/ccg) (canonical `terms.krafton.com/en/content_creation_guideline/bgmi`).
- §3 "Earning profit by using KRAFTON IP": "We're OK with you generating revenue from the content you make". Allowed: ad revenue on platforms such as YouTube and Facebook, ad revenue on personal websites, donations, and subscriptions where the stream "is also available for free", plus other platforms with written permission.
- Odd wording: the first allowed case reads "Advertising revenue generated from non-monetized videos". This is probably a drafting error, but read literally it is ambiguous. Flag it if legal review happens.
- Not allowed: content using BGMI IP that promotes "non-KRAFTON game titles", including sponsored ads. Content "for the sole purpose of seeking profit". You "may not limit to paid access, sell, or license your content" with BGMI IP.
- "In a nutshell": "stick to the main social media and video sharing platforms".
- §2 best practices: Krafton is "not fans of content which are simply re-posts", and creators must follow each platform's community guidelines. No mods or cheats, and nothing that "reflects poorly on KRAFTON".
- The Rules of Conduct ([terms.krafton.com/en/rules_of_conduct/bgmi](https://terms.krafton.com/en/rules_of_conduct/bgmi)) were scanned and contain no clause about streaming, recording or video tools.

### What this means for AI-GCM (inference, not legal advice)
- Offline processing of a creator's own recordings or VODs is not an "unauthorized program" in the §3(w) sense, because it does not touch the game client, the server or game memory. No clause addresses third-party editing or clipping tools.
- The clauses closest to biting:
  1. Clipping agencies or AI-GCM **selling clips containing BGMI footage to third parties** (B2B clip packages, clipper bounties) could fall under "sell, or license your content … for payment" and §1's ban on licensing for a fee. Organisers and broadcast partners usually hold their own Krafton agreements, so check this before any B2B pitch.
  2. Promoting other games (for example Free Fire MAX) in BGMI clips is banned, which matters for multi-game templates and sponsor overlays.
  3. Paywalled clip feeds are not allowed.
  4. AI-GCM's marketing should not imply Krafton endorsement. The "not endorsed" disclaimer could be offered as an auto-overlay.
- Unconfirmed: whether Krafton treats a SaaS tool that charges creators to process BGMI footage as "commercial use" of the Game under §3(a). No text addresses it, and asking Krafton (battlegroundsindia_support@krafton.com) is out of scope for this desk check.

---

## 3. Eklipse and BGMI / PUBG Mobile

**Answer:** Eklipse's own help article lists "PUBG Mobile" and "Freefire" as supported games, but that list was last updated in April 2023. BGMI is not named anywhere I could find. Its current PUBG marketing page is written for PC streamers. Local uploads (MP4, up to 10 GB, Premium only) are made from the web app, and you pick the game when uploading. The mobile app reviews and edits clips; it does not upload full mobile gameplay for detection. No user evidence of BGMI or PUBG Mobile results was found.

Note: eklipse.gg returns a Cloudflare block to this environment, so pages were read through Wayback Machine snapshots.

### Supported-games list [Official, dated]
"What games does Eklipse support?" (snapshot 13 Jul 2025, article "Updated on April 3, 2023") lists 20 titles, including **PUBG**, **PUBG Mobile**, **Freefire**, **Mobile Legend: Bang Bang**, **League of Legends: Wild Rift** and **Arena of Valor**. It does not list BGMI ([live URL](https://eklipse.gg/help/what-games-does-eklipse-support/); [snapshot](https://web.archive.org/web/20250713193753/https://eklipse.gg/help/what-games-does-eklipse-support/)).
- Eklipse now claims "3000+ more games supported". The full list sits in the web app (app.eklipse.gg/games), which is not archived and could not be checked.
- BGMI's HUD is close to PUBG Mobile's, so PUBG Mobile detection *might* carry over. This is untested.

### PUBG page [Vendor marketing]
"PUBG Clip Maker" (snapshot 9 Oct 2026) ([eklipse.gg/use-case/pubg-clips](https://eklipse.gg/use-case/pubg-clips/); [snapshot](https://web.archive.org/web/20261009052402/https://eklipse.gg/use-case/pubg-clips/)):
- Claims detection of chicken dinners, squad wipes, 1v4 clutches and long-range snipes by pairing "gameplay spikes" with chat, audio and facecam reactions.
- The framing is PC: Twitch, YouTube, Kick or Facebook VODs, "No Game Bar, no ShadowPlay, no OBS replay buffer", and 20–30-minute PC matches. The page never says "mobile" or "BGMI".
- Price on the page: Premium $24.99/month, or $179.99/year (about $14.99/month).

### Uploads and the mobile app [Official help]
- "How to Import Streams from Local Storage" ([snapshot 21 Apr 2026](https://web.archive.org/web/20260421231922/https://eklipse.gg/help/how-to-import-streams-from-local-storage/); article updated Nov 2023): Premium only, MP4 only, up to 10 GB per file, 1 credit per import, up to 10 imports a month. The steps include "Select game", so the chosen game drives detection.
- [Secondhand summaries of eklipse.gg help pages] The mobile app's AI Edit takes a single clip from the phone gallery (MP4, under 1 GB, 15 seconds to 3 minutes). Long recordings go through Import Stream on the web. The app is mainly for previewing, editing and posting clips from connected Twitch, YouTube or Kick channels ([help: can't upload to editor](https://eklipse.gg/help/cant-upload-to-editor/); [mobile app](https://eklipse.gg/features/mobile-app/)).
- [Vendor marketing, secondhand snippet] One Eklipse page says Mobile Legends, Free Fire and PUBG "record vertically already, so the editor skips the reframe". BGMI is normally played landscape, so this is either wrong or refers to vertical phone streams. Treat Eklipse's mobile handling as untested.

### User evidence
- No BGMI or PUBG Mobile user reports were found.
- The only PUBG-specific review is on Eklipse's own blog, by an ex-Athenascope user (roughly 2024). It says PUBG "felt a bit neglected" while Eklipse focused on Warzone 2 ([blog.eklipse.gg](https://blog.eklipse.gg/eklipse-news-and-guide/ex-athenascope-reviews-on-eklipse.html)) [Secondhand, hosted by the vendor].
- Eklipse's "PUBG Mobile" community page (eklipse.gg/community/pubg) existed in 2022 but returns 404 in archives.
- **Still open:** run one BGMI VOD through Eklipse (as in validation step 2).

---

## 4. Building blocks for a BGMI highlight detector

**Answer:** A small but usable seed exists. One CC BY 4.0 Roboflow set (about 1.4k images) already labels BGMI `kill`, `knock out` and `chicken dinner` banners, and a 757-image CC BY 4.0 set labels PUBG kill and knock messages. Everything else is player or enemy detection, esports scoreboard parsing, or tabular stats. Nothing useful was found on Kaggle or Hugging Face. No open, end-to-end BGMI highlight pipeline exists.

Figures were read from each Roboflow page today. "Updated" is as Roboflow displays it. CC BY 4.0 permits commercial use with attribution, but **check image provenance**: these are screenshots of Krafton's game, and Krafton owns the game IP (see §2).

### Roboflow Universe [Official listing pages; the data itself is user-contributed]
| Dataset | URL | Licence | Size | Labels | Notes |
|---|---|---|---|---|---|
| **BGMI** (workspace "BGMI") | [universe.roboflow.com/bgmi-meb2n/bgmi-0wljr](https://universe.roboflow.com/bgmi-meb2n/bgmi-0wljr) | CC BY 4.0 | 1,435 images, 5 versions, 5 models | `chicken dinner`, `kill`, `knock out` | YOLOv11n model, self-reported mAP@50 94.9%, P 96.1%, R 94.1%; updated about a year ago. **Most directly useful.** A fork at [rohits-win5s/bgmi-0wljr-hvylj](https://universe.roboflow.com/rohits-win5s/bgmi-0wljr-hvylj/model/1) exists. |
| **stg-kill-message** (OXO; formerly ELKROOM) | [universe.roboflow.com/oxo-3oodx/stg-kill-message](https://universe.roboflow.com/oxo-3oodx/stg-kill-message) | CC BY 4.0 | 757 images, 8 versions, 6 models | `pubg-kill`, `pubg-knock-down`, `pubg-medal`, `freefire-medal`, `cod-kill`, `cod-knock-down`, `cod-medal`, `codw-kill`, `bs-medal` | YOLOv8s, self-reported mAP@50 97.1%; updated 2 years ago. Covers multiple mobile games, so it is useful for the Free Fire MAX second title. Whether "pubg" means Mobile or PC is not stated. |
| **BGMI Scoreboard** (Setu) | [universe.roboflow.com/setu-it3tm/bgmi-scoreboard-pfze2](https://universe.roboflow.com/setu-it3tm/bgmi-scoreboard-pfze2) | CC BY 4.0 | 601 images, 1 model (Roboflow Instant) | `kill_feed`, `players`, `teams`, `Default-5XNB` | Updated about a year ago; no description. The classes suggest esports or observer screens. |
| **kill-feed-detection-main 2** (hmmmm) | [universe.roboflow.com/hmmmm/kill-feed-detection-main-2](https://universe.roboflow.com/hmmmm/kill-feed-detection-main-2) | CC BY 4.0 | 3,403 images, 0 models | `kill-block` | The game is not stated. The same author's other set is BGMI, so this is probably BGMI broadcast kill blocks, but that is unconfirmed. |
| **bgmi-result-detection** (hmmmm) | [universe.roboflow.com/hmmmm/bgmi-result-detection](https://universe.roboflow.com/hmmmm/bgmi-result-detection) | CC BY 4.0 | 236 images, 5 models | `team-block` | Tournament result screens. |
| **BGMI Scrims** | [universe.roboflow.com/bgmi-scrims/bgmi-scrims](https://universe.roboflow.com/bgmi-scrims/bgmi-scrims) | CC BY 4.0 | 67 images, semantic segmentation | `finishes_id`, `player_id`, `rank_id`, `slot_id`, `objects` | Scrim result-screen parsing. |
| **Enemy Find BGMI** / **bgmi** (323 images) / **eagle-star-bgmi** (60) | [enemy-find-bgmi](https://universe.roboflow.com/bgmi-7bdtq/enemy-find-bgmi); [bgmi-v73xl-c1sj0](https://universe.roboflow.com/javeds-workspace-o1hnz/bgmi-v73xl-c1sj0) | not checked | 279 / 323 / 60 | `Enemy` | Aim-assist style enemy detection. Not useful for highlights. |
| **pubg** (aipubg) | [universe.roboflow.com/aipubg/pubg-lmzib](https://universe.roboflow.com/aipubg/pubg-lmzib) | CC BY 4.0 | 1,501 images, 7 models | `wounded`, `crosshair`, `ADS`, `nameplate`, `parachute`, `gun`, `car`, `head`, `person` | Mobile or PC is unclear; updated 3 years ago; mAP@50 74.2%. `wounded` (knocked state) could help. |
| **pubg** (gwycc) | [universe.roboflow.com/gwycc/pubg-ij9vn](https://universe.roboflow.com/gwycc/pubg-ij9vn) | Public Domain | 897 images | enemy body parts, `dead_box`, `loot`, `vehicle`, `own_Player`, etc. | Updated 3 years ago. |
| **pubg mobile** (Ilya Kiselev) | [universe.roboflow.com/ilya-kiselev-9vk2f/pubg-mobile](https://universe.roboflow.com/ilya-kiselev-9vk2f/pubg-mobile) | CC BY 4.0 | 463 images | digits 0–9 plus Cyrillic letters | HUD digit OCR (Russian UI); updated 5 years ago. Marginal. |
| **pubg mobile** (alajouri) | [universe.roboflow.com/pubg-mobile-by-alajouri/pubg-mobile-7zm9r](https://universe.roboflow.com/pubg-mobile-by-alajouri/pubg-mobile-7zm9r) | not checked | 506 images | `head-person` | Not useful. |

A search for "chicken dinner" on Roboflow returned only food datasets. The `bgmi-0wljr` set is the only one labelling the win screen.

### Kaggle, Hugging Face [Official listings via public APIs]
- Kaggle "BGMI Dataset" ([kaggle.com/datasets/kashyapankush/bgmi-dataset](https://www.kaggle.com/datasets/kashyapankush/bgmi-dataset)): Apache 2.0, a single 660 MB file `BGMI Game Dataset.csv` (tabular), no description, March 2024. Not vision data.
- Kaggle "PUBG Mobile Win & Performance Prediction" and the classic PUBG finish-placement data are tabular match statistics ([link](https://www.kaggle.com/datasets/aliiihussain/pubg-mobile-win-and-performance-prediction-dataset)). Not useful.
- Hugging Face `oreo2000/pubgm-videos` ([link](https://huggingface.co/datasets/oreo2000/pubgm-videos)): unlabelled MP4s (an esports match, chunks, "highlightN.mp4"), no licence, no README, Dec 2025. Could serve as rough test footage only.
- Hugging Face `badbadal2000/Bgmiresults`: empty. No PUBG or BGMI vision models on Hugging Face (the "pubg" models found are image-generation LoRAs).

### GitHub and prior art [Official repos]
- **Kanhaiyaji/Automate-Yt** ([github.com/Kanhaiyaji/Automate-Yt](https://github.com/Kanhaiyaji/Automate-Yt)): MIT, 0 stars, 5 commits. A BGMI/PUBG Mobile/ScarFall pipeline that reads the `Finish: X` counter and "Double Finish" medals with OCR, plus audio energy and motion fight detection, then makes 9:16 Shorts. No weights or dataset included, and the OCR engine is not named. A useful reference design.
- **SawXu/pubg-highlight-trim** ([github.com/SawXu/pubg-highlight-trim](https://github.com/SawXu/pubg-highlight-trim)): GPL-3.0-or-later, Windows, PC PUBG NVIDIA Highlights. OCR-only (PP-OCR ONNX models in Rust) on a fixed centre-screen crop, matching "YOU KNOCKED OUT/KILLED" in English and Chinese. GPL means the code cannot be copied into closed source, but the approach (relative-coordinate crop, brightness prefilter, OCR keywords) carries over.
- **Pannawath/PUBG-MOBILE-Vmix-manul-control-live-ranking-killfeed**: a manual broadcast-graphics tool, not detection.
- **New competitor found: THUNDER, "PUBG Mobile Highlight Automation Studio"** ([github.com/MAAKTHUNDER/thunder-releases](https://github.com/MAAKTHUNDER/thunder-releases)), v1.0.0, repo active 24 Oct 2026. A closed-source Windows app needing an NVIDIA GPU. It claims "AI combat detection" of kills and knockdowns and 9:16 Shorts with kill-feed overlays and zooms [Vendor marketing]. Add it to the competitor table next to BGMI Clipper and pubgclipper.com.

### BGMI Clipper's approach [Vendor marketing]
[bgmiclipper.com](https://bgmiclipper.com/): a "custom-trained ONNX model recognises kill feed icons frame-by-frame", plus "Audio Gunshot Detection" (audio spikes). There are three modes (Auto = vision + audio, Audio Only, AI Only), and the output is one merged reel with fades. It runs fully offline on Windows 10/11 x64; the installer is about 14 MB and downloads about 2 GB of Python, FFmpeg and packages on first launch. No OCR, architecture, training data, accuracy figures or GitHub repo are published. Pricing is ₹0 (2 processes) / ₹499 / ₹699 one-time.

---

## 5. Pricing and free tiers (October 2026)

**Answer:**
- **Gemini:** every Flash and Flash-Lite model has a free tier, but free-tier inputs may be used by Google to improve its products, and the free-tier rate limits are visible only in AI Studio. Paid Flash-Lite costs $0.10–0.30 per 1M video tokens (about $0.04–0.11 per hour of video, input only).
- **Sarvam:** speech-to-text costs ₹0.49 a minute (about ₹29.4 an hour), and new users get ₹100 in free credits.
- **CPU Hinglish options:** Oriserve's Apache-2.0 Whisper-Hindi2Hinglish models (73M–1.5B parameters, romanised output), Vosk Hindi (Apache 2.0) and AI4Bharat IndicConformer (MIT).

### Google Gemini API [Official]
Pricing ([ai.google.dev/gemini-api/docs/pricing](https://ai.google.dev/gemini-api/docs/pricing), last updated 2026-10-22). Prices are USD per 1M tokens, paid Standard tier, for text, image and video input (audio in brackets where different):

| Model | Free tier | Input | Output | Batch input / output |
|---|---|---|---|---|
| gemini-2.5-flash-lite | Yes | $0.10 ($0.30 audio) | $0.40 | $0.05 / $0.20 (no free batch) |
| gemini-3.1-flash-lite | Yes | $0.25 ($0.50 audio) | $1.50 | $0.125 / $0.75 |
| gemini-3.5-flash-lite | Yes | $0.30 (all media) | $2.50 | $0.15 / $1.25 |
| gemini-2.5-flash | Yes | $0.30 ($1.00 audio) | $2.50 | $0.15 / $1.25 |
| gemini-3-flash-preview (legacy) | Yes | $0.50 ($1.00 audio) | $3.00 | $0.25 / $1.50 |
| gemini-3.6-flash / 3.8-flash | Yes | $0.75 | $3.75 | $0.375 / $1.875 |

- **Correction:** the 3.6 and 3.8 Flash prices **double on 1 Jan 2027** (to $1.50 input / $7.50 output, batch likewise), according to the pricing page as updated 2026-10-22. The existing report says 2026-12-01.
- The "Used to improve our products" row is **Yes on the Free tier and No on Paid**, for every Flash and Flash-Lite model. Creator footage sent on the free tier may therefore be used by Google. That is a privacy point for the product and for the Privacy Policy.
- Free-tier rate limits: the official rate-limits page (updated 2026-10-15) no longer publishes per-model numbers and says they "can be viewed in Google AI Studio" ([rate-limits](https://ai.google.dev/gemini-api/docs/rate-limits)). Limits apply per project and reset at midnight Pacific. Paid Tier 1 needs only a linked billing account; Tier 2 needs $100 spent plus 3 days; Tier 3 needs $1,000 spent plus 30 days. [Secondhand] Third-party trackers disagree. Flash-Lite figures range from 10 RPM / 500 RPD to 15 RPM / 1,000 RPD, and Flash from 5 RPM / 20 RPD to about 10 RPM / 1,500 RPD ([tinkerllm](https://tinkerllm.com/blog/gemini-api-free-tier-limits-rate-quotas/); [klymentiev, Oct 2026](https://klymentiev.com/blog/gemini-api-free-tier)). Treat these as unknown until checked in AI Studio.

Video limits ([video-understanding](https://ai.google.dev/gemini-api/docs/video-understanding), updated 2026-10-13; [files](https://ai.google.dev/gemini-api/docs/files), updated 2026-10-14):
- About 100 tokens per second of video at default/low media resolution (66 tokens per frame at 1 fps, plus 32 tokens per second of audio). At high resolution it is about 300 tokens per second (258 per frame).
- With a 1M-token context, a request can cover up to **3 hours at low resolution, or 1 hour at high resolution**.
- File size: Files API **2 GB per file** and 20 GB per project, files deleted after 48 hours, Files API itself free. The video page also says "20GB (paid) / 2GB (free)"; the Files page lists only 2 GB. Inline requests must stay under 100 MB (the page also says inline suits requests under 20 MB).
- **YouTube URLs** (preview, no extra charge): free tier up to **8 hours of YouTube video per day**, paid tier unlimited. **Public videos only** (not private or unlisted), and up to 10 videos per request on 2.5 and later models. This means AI-GCM can point Gemini at a creator's *public* YouTube Live VOD without uploading it, which is a real advantage for 3–6-hour streams on Indian upload speeds.
- Custom fps (for example 0.5) and `start_offset`/`end_offset` clipping are supported (static mode only), so candidate windows can be judged without re-uploading.
- Formats: MP4, MPEG, MOV, AVI, FLV, MPG, WebM, WMV, 3GPP.

[Derived] Input cost per hour of video at about 100 tokens per second (360k tokens), standard tier, before output tokens:
- 2.5 Flash-Lite: about $0.036
- 3.1 Flash-Lite: about $0.09
- 3.5 Flash-Lite and 2.5 Flash: about $0.11
- 3.8 Flash: about $0.27, rising to about $0.54 from 2027

Batch halves these. The report's figures were slightly higher, probably because they include output tokens. The conclusion does not change.

### Sarvam AI speech-to-text [Official]
- Pricing ([docs.sarvam.ai/api/pricing](https://docs.sarvam.ai/api/pricing)): Speech to Text (real-time, streaming or batch) costs **₹0.49/min** pay-as-you-go, ₹0.45 on Pro and ₹0.41 on Growth, billed per second. With diarization (batch) it costs ₹0.59 / ₹0.54 / ₹0.50 per minute. GST is extra. "Every verified user receives ₹100 in credits", which is about 3.4 hours of audio [Derived]. There is no separate free tier and no monthly fee.
- Models ([models page](https://docs.sarvam.ai/api-reference-docs/getting-started/models); [Saaras page](https://docs.sarvam.ai/api/getting-started/models/saaras)):
  - **Saaras v4** is the default, with 22 Indian languages plus Global and Indian English. Its modes are transcribe, translate, verbatim, translit and codemix.
  - Saaras v3 is still active. Saaras v2.5 is "deprecated soon".
  - **Saarika is no longer listed** on the current models pages; Saaras now covers transcription too.
- Hinglish output: `codemix` gives Devanagari Hindi with Roman English (for example "मेरा phone number है"). `translit` gives fully Roman text ("mera phone number hai"), which is the caption style Hinglish Shorts usually use.
- Limits:
  - The REST (synchronous) endpoint accepts **at most 30 seconds** of audio.
  - The Batch API accepts **up to 2 hours per file** and 20 files per job, with diarization for up to 20 speakers.
  - Timestamps are **chunk-level only** (phrase or sentence, not word). Word-level karaoke captions would need a separate forced-alignment step.
  - Rate limits are on a separate page that was not read.

### Free or cheap Hinglish ASR that runs on CPU [Official model cards/listings]
| Option | Licence | Size | Notes |
|---|---|---|---|
| **Oriserve/Whisper-Hindi2Hinglish-Swift** ([HF](https://huggingface.co/Oriserve/Whisper-Hindi2Hinglish-Swift)) | Apache 2.0 | about 73M parameters (Whisper-base) | Outputs **romanised Hinglish** directly; small enough for CPU. Vendor claims about 57% better than Whisper-base on its own benchmarks. |
| **Oriserve/Whisper-Hindi2Hinglish-Apex** ([HF](https://huggingface.co/Oriserve/Whisper-Hindi2Hinglish-Apex)) | Apache 2.0 | about 809M (large-v3-turbo) | Romanised Hinglish, tuned for noisy Indian-accented audio. Runs on CPU via faster-whisper or whisper.cpp after conversion (these conversions are generic Whisper tooling, not tested here); slower. |
| Oriserve/Whisper-Hindi2Hinglish-Prime ([HF](https://huggingface.co/Oriserve/Whisper-Hindi2Hinglish-Prime)) | Apache 2.0 | about 1.5B (large-v3) | Heaviest of the three. |
| **Trelis/tara** ([HF](https://huggingface.co/Trelis/tara)) | Apache 2.0 | about 1.5B | Vendor-reported 8.37 WER on CS-FLEURS Hindi-English, and a Vistaar Hindi aggregate of 12.06 against 12.32 for Saaras v3. Code-mix output (Devanagari plus Latin script). Large for CPU. |
| openai/whisper-large-v3-turbo ([HF](https://huggingface.co/openai/whisper-large-v3-turbo)) | MIT | about 809M | Baseline; weak on code-switching (see the Trelis numbers already in the report). |
| **ai4bharat/indic-conformer-600m-multilingual** ([HF](https://huggingface.co/ai4bharat/indic-conformer-600m-multilingual)) | MIT (gated: accept terms) | 600M | 22 Indian languages, CTC and RNNT decoding, ONNX runtime supported. Code-mixing and output script not stated. |
| **Vosk Hindi** ([alphacephei.com/vosk/models](https://alphacephei.com/vosk/models)) | Apache 2.0 | small 42 MB / full 1.5 GB | Very light on CPU. WER 20.9–24.7 (small) and 13.1–14.9 (full) on Hindi test sets. Devanagari output and not built for code-switching, so better suited as a cheap keyword or excitement cue than as captions. |

Also cheap, though not on CPU [Derived]: Gemini audio transcription at 32 tokens per second is about 115k tokens per audio hour, roughly $0.035 per hour on 2.5 Flash-Lite (audio at $0.30/M). Hinglish accuracy for squad voice chat is untested.

Not verified for any option: accuracy on four-person squad voice over gunfire. Every WER figure above comes from the vendor's own clean or benchmark audio.

---

## Still open after this desk check
1. Whether YouTube's highlight Shorts appear for Indian channels, and whether any route works for screencast or encoder BGMI streams. This needs the hands-on test in validation step 1.
2. Eklipse's current in-app game list (does it include BGMI?) and real output on a BGMI VOD. This needs an account (validation step 2).
3. Whether Krafton treats a paid clipping SaaS, or B2B clip sales, as "commercial use" that needs written permission.
4. Free-tier Gemini rate limits for Flash-Lite (visible only in AI Studio).
