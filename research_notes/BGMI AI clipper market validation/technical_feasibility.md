# Technical feasibility of AI-GCM: automatic highlight detection for mobile battle-royale gameplay (BGMI / PUBG Mobile / Free Fire), as of late 2026

Research date: 2026-10-26. About 18 tool calls. Several primary sources (BGMI Terms of Service, Eklipse engineering blog) returned HTTP 403 and could not be read directly; those gaps are flagged below. Where a figure is my own arithmetic from cited prices, it is marked "(derived)".

## 1. Which detection approaches are used in practice and research, and which work best for battle royale?

### Takeaway
No published, peer-reviewed system targets BGMI / PUBG Mobile / Free Fire specifically. The strongest practical recipe is a cheap multi-signal pipeline: HUD/kill-feed detection (YOLO-style detector plus OCR) and audio-energy/voice-excitement cues to find candidates, then a multimodal LLM (Gemini-class) only on candidate windows to judge and caption. Commercial clippers (Eklipse) use exactly this "on-screen signal + audio + chat" mix and report 80-90% usable clips on supported PC shooters. Battle royale suits novelty/burst detection because long quiet looting alternates with short fights.

### Cited Findings
**Research on game / stream highlights**
- Ringer & Nicolaou, "Deep Unsupervised Multi-View Detection of Video Game Stream Highlights" (FDG 2018), used **PUBG streams**. It is an unsupervised, novelty-based method combining game footage, the streamer's facial expression and speech. The authors chose PUBG because long low-intensity stretches alternate with short action bursts — [arXiv 1807.09715](https://arxiv.org/pdf/1807.09715); [Goldsmiths repository](https://research.gold.ac.uk/id/eprint/24109)
- A University of Leeds PhD thesis covers multimodal highlight detection for livestreams and esports — [White Rose eTheses](https://etheses.whiterose.ac.uk/32406/1/PhD_Thesis__Revised_.pdf) (contents not reviewed in detail)
- A University of Toronto project describes multimodal gameplay highlight detection for first-person shooters, aimed at kills and deaths. It is a summary page without method or accuracy details — [U of T project page](https://www.cs.toronto.edu/~edithal/projects)
- AMD's "Gameplay Highlights Generation" first identifies intervals where interesting events occur and then concatenates them. It appears to be video-only — [arXiv 2505.07721](https://arxiv.org/pdf/2505.07721)
- A 2026 controlled study of audio for sports highlights found that a **lightweight audio-only GRU is highly competitive with multimodal methods**, and that simple audio-visual fusion performs best. Commentary, crowd response and impact sounds carry complementary signal — [arXiv 2609.17923](https://arxiv.org/pdf/2609.17923)
- A dual-stream model using audio Mel-spectrograms plus grayscale frames reported up to **89.24% accuracy for audio and 83.00% for video** on sports highlights — [arXiv 2501.16100](https://arxiv.org/html/2501.16100v1)
- Costa et al. fused YAMNet audio-event features with NLP on transcribed commentary. They validated on SoccerNet but aimed at competitive gaming streams, and report that the fusion "significantly outperforms uni-modal baselines" — [UCP repository](https://repositorio.ucp.pt/entities/publication/6981957f-9c58-4f84-85c2-4f3353bdd987)
- AutoHighlight used crowd-sourced data (Twitch chat and similar) to detect highlights in League of Legends esports broadcasts — [CyI repository](https://repository.cyi.ac.cy/bitstream/CyI/1884/1/Autohighlight%20Highlight%20detection%20in%20League%20of%20Legends%20esports%20broadcasts%20via%20crowd%20sourced%20data.pdf)

**Generic video highlight detection and temporal grounding (QVHighlights)**
- Specialised DETR-style detectors lead QVHighlights: SG-DETR (with pre-training) scores **71.00 HIT@1 and 44.70 mAP** — [HyperAI leaderboard](https://vercel.hyper.ai/cn/sota/tasks/highlight-detection/benchmark/highlight-detection-on-qvhighlights) (the leaderboard may be stale)
- General video LLMs are much weaker at zero-shot highlight scoring. LLaVA-Video-7B scores **20.7 mAP / 34.8 HIT@1** and Qwen2-VL-72B **21.6 mAP / 37.5 HIT@1**. With NumPro frame-numbering prompts, Qwen2-VL-72B reaches **24.2 mAP / 44.3 HIT@1** — [CVPR 2025 NumPro supplement](https://openaccess.thecvf.com/content/CVPR2025/supplemental/Wu_Number_it_Temporal_CVPR_2025_supplemental.pdf)
- TemporalVLM reports **+1.9 mAP / +7.4 HIT@1** over TimeChat on highlight detection (self-reported) — [arXiv 2412.02930](https://arxiv.org/pdf/2412.02930)
- I found no published Gemini or GPT score on QVHighlights.

**Commercial practice**
- Eklipse says its pipeline identifies the game, then looks for kills, clutches, multi-kills, eliminations and chat-reaction spikes, and cuts each into a clip. Its help docs say clips are found by **detecting specific on-screen signals**: if overlays cover the HUD, the event is not detected and no clip is made — [Eklipse help: clips not detected](https://eklipse.gg/help/call-of-duty-black-ops-7-stream-setup/); [Eklipse vs OpusClip](https://eklipse.gg/help/how-is-eklipse-different-from-other-clipping-tools-like-opus-clip-or-streamladder/)
- Eklipse claims **80-90% usable clip rates** on Valorant, CoD, Apex and Fortnite, based on user feedback (a vendor claim). It is less reliable on strategy, Just Chatting and IRL streams — same Eklipse sources as above
- Eklipse's descriptions are inconsistent. One says it reads "kill feed activity, audio spikes, chat velocity, and engagement cues." A newer "Gameplay Intelligence" feature, on Premium VODs from 2026-06-01, says it decides based on "what is actually happening on screen, not just spikes in audio or the kill feed" — [Eklipse blog: Gameplay Intelligence](https://blog.eklipse.gg/streaming-tips/how-gameplay-intelligence-works-2.html) (page returned 403 on direct fetch; summarised from the search index)
- OpusClip "ClipAnything" is described as multimodal clipping from visual, audio and sentiment cues, with clips up to 15 minutes — [Castmagic review of OpusClip](https://www.castmagic.io/software-reviews/opus-clip)

### Inferences
- For battle royale, kill events are the most reliable anchor because the kill feed and the "You eliminated X" / kill-count HUD are deterministic on-screen text. A HUD detector plus OCR should give high precision on "kill" and "multi-kill" events at very low cost. That is what Eklipse's "on-screen signals" approach implies.
- General video LLMs are not yet good at precise zero-shot temporal localisation (about 20-25 mAP on QVHighlights versus about 45 for specialised detectors). Use them to **judge and describe** candidate windows found by cheap detectors, not to scan full VODs for boundaries.
- Audio is disproportionately useful and cheap: the 2026 sports-audio study, plus the streamer-reaction signal in Ringer & Nicolaou. For BGMI, gunfire density plus squad voice-chat loudness, laughter and shouting is likely a strong "interestingness" proxy.

### Gaps
- No peer-reviewed paper or benchmark exists for mobile battle-royale (BGMI / PUBG Mobile / Free Fire) highlight detection specifically, so there are no domain-specific accuracy numbers.
- I could not find OpusClip's technical description of gaming detection, or an independent accuracy evaluation of Eklipse.
- I could not confirm whether Eklipse supports PUBG Mobile, BGMI or Free Fire. Older Eklipse posts list "PUBG" without saying PC or mobile, and a reviewer said PUBG detection "felt a bit neglected" — [Eklipse PUBG tag](https://blog.eklipse.gg/tag/pubg); [Eklipse review](https://blog.eklipse.gg/featured/eklipse-gg-review.html). Eklipse claims 3,000+ games supported (July 2026) without a list — [Eklipse About](https://eklipse.gg/about). This looks like a possible competitive gap for India-specific mobile titles, but it is unverified.

## 2. Mobile-specific challenges: HUDs, overlays, resolutions, squad audio, Hindi/Hinglish ASR

### Takeaway
The main risks are HUD variance (custom layouts, facecam and overlays covering the kill feed) and Hinglish speech. Off-the-shelf Whisper is weak on Hindi-English code-mixing (about 30% WER). Indian-specialised ASR (Sarvam Saaras, AI4Bharat IndicWhisper, Trelis Tara) roughly halves that. Sarvam costs ₹30 per audio hour.

### Cited Findings
- **Overlays break HUD-based detection**: Eklipse states that if overlays cover the HUD, the event cannot be detected — [Eklipse help](https://eklipse.gg/help/call-of-duty-black-ops-7-stream-setup/)
- **Public BGMI training data is tiny but exists**. "BGMI Scoreboard" on Roboflow has about 601 images with classes `kill_feed`, `players`, `teams` — [Roboflow BGMI Scoreboard](https://universe.roboflow.com/setu-it3tm/bgmi-scoreboard-pfze2). "BGMI-OCR" has about 21 images, CC BY 4.0 — [Roboflow BGMI-OCR](https://universe.roboflow.com/harshalp-8acem/bgmi-ocr). "PUBG_Highlight_Detection_v2" is a community model — [Roboflow PUBG_Highlight_Detection_v2](https://universe.roboflow.com/1stbtln/pubg_highlight_detection_v2)
- **Whisper on code-switched Hindi-English**: whisper-large-v3 scores **29.74 WER** versus Sarvam Saaras-v3 **11.47** on CoSHE-500. On CS-FLEURS, Sarvam scores **16.47** and ElevenLabs Scribe-v2 **7.57**. Whisper's default normaliser strips Devanagari matras, which inflates WER. These numbers are self-reported by the vendor Trelis — [Trelis Tara model card](https://huggingface.co/Trelis/tara)
- Trelis Tara reports **8.37 WER on CS-FLEURS** and a 12.06 Vistaar Hindi mean, versus Sarvam Saaras-v3 at 12.32 (vendor-reported) — [Trelis Tara](https://huggingface.co/Trelis/tara). A Whisper-Hinglish fine-tune is also hosted — [Trelis whisper-hinglish-preview on Friendli](https://friendli.ai/models/Trelis/whisper-hinglish-preview)
- On LAHAJA, a multi-accent Hindi benchmark, **Whisper V3 scored 32.4 WER**, Google Chirp 22.3, and the best IndicASR model 14.3 — [LAHAJA, arXiv 2408.11440](https://arxiv.org/pdf/2408.11440)
- IndicWhisper (AI4Bharat Vistaar) was fine-tuned on about 10.7K hours across 12 Indian languages. It had the lowest WER on 39 of 59 Vistaar benchmarks, with an average 4.1 WER reduction. It is not Hinglish-specific — [Vistaar, arXiv 2305.15386](https://arxiv.org/abs/2305.15386)
- ASR WER typically rises **30-50% (relative)** on code-switched speech compared with monolingual speech — [HiACC corpus, PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12329218/)
- Gemini video input samples **1 frame per second by default**; custom fps (for example 0.5) and clip offsets (`start_offset` / `end_offset`) are supported — [Gemini video understanding docs](https://ai.google.dev/gemini-api/docs/video-understanding)

### Inferences
- HUD positions in BGMI are user-customisable (a common feature of the game; not verified from Krafton docs here). A robust system should not hard-code pixel regions. It should run a learned detector for kill-feed, kill-counter and "eliminated" banners across aspect ratios (19.5:9 and 20:9 phones, 16:9 recordings, letterboxed streams), and should mask detected facecam rectangles first.
- 4-person squad voice is overlapping, noisy speech mixed with gunfire. Expect ASR WER well above benchmark figures, which come from clean, read or conversational speech. So treat ASR mainly as a **caption** source and a **keyword or laughter** cue, not as the primary event detector. Prosody and loudness features (energy, pitch spikes, laughter detection) are language-agnostic and robust to Hinglish.
- Screen-recorded mobile footage often has variable frame rate and compression. That is fine for kill-feed OCR at 2-5 fps, but finer-grained visual analysis (for example detecting knock-downs from the crosshair) degrades. 1 fps LLM sampling can miss sub-second events, though kill-feed entries persist on screen for several seconds (persistence duration not verified).

### Gaps
- I found no measured WER on gaming voice chat or Hinglish gaming streams.
- No source documented the variety of BGMI custom-HUD layouts or of Free Fire HUD layouts.
- I found no open-source end-to-end BGMI / PUBG Mobile kill-feed detection repository on GitHub. The search surfaced only Roboflow datasets and generic YOLO+OCR repos for licence plates and ID cards.

## 3. Judging "funny" or "interesting" moments vs. kills; ranking and engagement prediction

### Takeaway
Kills are easy; "funny" or "interesting" is not. The research that exists uses viewer or streamer reaction as the proxy: chat velocity, streamer face and voice, laughter, commentary excitement. Multimodal LLMs are the practical tool for semantic judgement ("is this funny?") on short candidate windows, with ranking tuned later from creators' accept/reject decisions and post performance.

### Cited Findings
- Ringer & Nicolaou treat highlights as **novelty** in streamer face, speech and game footage, without needing labels — [arXiv 1807.09715](https://arxiv.org/pdf/1807.09715)
- AutoHighlight uses **crowd-sourced chat data** for LoL esports highlights — [CyI repository](https://repository.cyi.ac.cy/bitstream/CyI/1884/1/Autohighlight%20Highlight%20detection%20in%20League%20of%20Legends%20esports%20broadcasts%20via%20crowd%20sourced%20data.pdf)
- Eklipse includes **chat-reaction spikes** alongside kills and clutches — [Eklipse vs OpusClip](https://eklipse.gg/help/how-is-eklipse-different-from-other-clipping-tools-like-opus-clip-or-streamladder/)
- OpusClip ranks clips with a **"Virality Score"** (Starter plan and above) — [Castmagic review](https://www.castmagic.io/software-reviews/opus-clip); [OpusClip pricing](https://opus.pro/pricing?via=606ed5)
- Speech-emotion corpora such as RAVDESS and IEMOCAP are suggested for detecting vocal excitement in caster commentary — [CEUR workshop paper](https://ceur-ws.org/Vol-4055/icaiw_wdea_5.pdf)

### Inferences
- A practical ranking score: a weighted sum of event value (kill count in a window, last-squad-alive clutch, knock-to-kill speed), excitement (voice loudness and pitch, laughter, gunfire density), audience reaction (chat or super-chat rate, for livestream VODs only), and an LLM judgement ("funny / fail / clutch / skill", with confidence).
- A "Virality Score"-style model needs outcome data. At launch, use heuristics plus LLM judgement. Then learn per-creator weights from which clips users keep and post, and later from YouTube Shorts and Instagram Reels performance, if API access allows.
- "Funny" moments (vehicle fails, glitches, banter) often have **no HUD event**. They depend on audio (laughter) plus LLM understanding, so this is where Gemini-class models add the most value over a CV-only pipeline.

### Gaps
- No public dataset of labelled "funny" gaming moments, and no published engagement-prediction accuracy for gaming Shorts.
- No source on how OpusClip's Virality Score is computed or validated.

## 4. Clip boundaries, 9:16 vertical reframing with facecam, auto captions

### Takeaway
Boundaries are best set by rules around detected events: pad before the first shot or knock and after the last kill, and merge events within N seconds into one fight. Then refine with audio-energy segmentation and, optionally, LLM review. Reframing gameplay to 9:16 is a solved product feature (OpusClip offers it), but gaming needs a split layout (facecam on top, gameplay crop below) rather than face-tracking crops.

### Cited Findings
- Specialised moment-retrieval detectors (DETR family) hold the QVHighlights state of the art. Video LLMs lag well behind on temporal localisation — [HyperAI leaderboard](https://vercel.hyper.ai/cn/sota/tasks/highlight-detection/benchmark/highlight-detection-on-qvhighlights); [CVPR 2025 NumPro supplement](https://openaccess.thecvf.com/content/CVPR2025/supplemental/Wu_Number_it_Temporal_CVPR_2025_supplemental.pdf)
- Gemini can reference moments by MM:SS timestamps and accepts `start_offset` / `end_offset` to analyse only a sub-interval. Custom fps lets you sample candidate windows more densely — [Gemini video understanding docs](https://ai.google.dev/gemini-api/docs/video-understanding)
- OpusClip auto-reframes to 9:16, 1:1 and 16:9 — [OpusClip AI Reframe](https://www.opus.pro/ai-reframe). The Starter plan is reportedly 9:16-only; Pro adds multiple aspect ratios — [OpusClip pricing](https://opus.pro/pricing?via=606ed5)
- The AMD gameplay-highlights work identifies interesting intervals and concatenates them — [arXiv 2505.07721](https://arxiv.org/pdf/2505.07721)

### Inferences
- Recommended boundary logic (derived): build each "fight" from the first gunfire or damage cue to the last kill or knock, plus about 3-5 s of pre-roll and 2-4 s of post-roll for the reaction. Merge events less than about 10-15 s apart. Cap Shorts at 60 s, or offer longer cuts. Evaluate boundaries against human-cut clips using temporal IoU.
- 9:16 layout for mobile gameplay (landscape 16:9 or 20:9): facecam crop in the top third, centre-crop gameplay in the bottom two-thirds, keeping the crosshair and kill feed. Facecam detection can be a simple face detector plus rectangle detection on the overlay.
- Captions: word-level timestamps from the ASR (Sarvam or Whisper-family). Offer Hinglish in Roman script, which is common for Indian Shorts audiences, as well as Devanagari. Gemini can also write short titles and hooks in Hinglish.

### Gaps
- No published accuracy for gaming clip boundaries, and no evaluation of facecam-aware reframing from OpusClip or Eklipse.

## 5. Compute cost per hour of 1080p footage, latency, and viability at ₹299-₹999/month

### Takeaway
Raw AI cost is small if done smartly. Full-VOD analysis with Gemini Flash-Lite at default resolution costs about **$0.03-$0.12 per hour of footage** (derived). Flagship Flash costs about $0.27/hr, rising to about $0.54/hr after 2026-12-01. Pro models cost about $0.45-0.90/hr. Separate Hinglish ASR at ₹30/hr would dominate if run on all audio, so run it only on candidate clips. ₹299-₹999/month looks viable at about 20-60 hours of footage per user per month **if** cheap CV/audio filtering comes first and LLM calls are restricted to candidates. Rendering, storage and egress also need budgeting.

### Cited Findings
**Gemini token rates**
- Default (low) media resolution: **about 100 tokens per second** = 66 tokens/frame at 1 fps + 32 audio tokens/s. High resolution: **about 300 tokens/s** (258 tokens/frame). With 1M context, a video can be up to **3 h at low resolution or 1 h at high resolution** — [Gemini video understanding docs](https://ai.google.dev/gemini-api/docs/video-understanding)

**Gemini prices (USD per 1M tokens, standard paid tier, as listed Oct 2026)** — [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing)

| Model | Text / image / video input | Audio input | Output | Batch |
|---|---|---|---|---|
| gemini-2.5-flash-lite | $0.10 | $0.30 | $0.40 | 50% off |
| gemini-3.1-flash-lite | $0.25 | $0.50 | $1.50 | 50% off |
| gemini-3.5-flash-lite | $0.30 | $0.30 | $2.50 | 50% off |
| gemini-2.5-flash | $0.30 | $1.00 | $2.50 | 50% off |
| gemini-3-flash-preview | $0.50 | $1.00 | $3.00 | 50% off |
| gemini-3.6-flash / gemini-3.8-flash | $0.75 (rising to **$1.50 on 2026-12-01**) | not split out | $3.75 | 50% off |
| gemini-3.1-pro-preview | $2.00 (≤200k-token prompt; $4.00 above) | not split out | $12.00 | 50% off |
| gemini-2.5-pro | $1.25 (≤200k; $2.50 above) | not split out | $10.00 | 50% off |

- A free tier exists for most Flash and Flash-Lite models, but free-tier content may be used to improve Google's products — same pricing page.
- A third-party estimate for Gemini 2.5 Flash on a one-hour video: about **$0.33/hr at default resolution and about $0.11/hr at low resolution**, with batch halving it again — [Fora Soft, May 2026](https://www.forasoft.com/learn/ai-for-video-engineering/articles-ai/real-cost-of-ai-in-video-products-gemini-openai-pricing) (uses older resolution assumptions than the current docs)
- Video *generation* pricing (Gemini Omni Flash, about $0.10 per second of output video) is reported by third parties. It is **not relevant** to analysis cost — [aireiter guide](https://aireiter.com/es/blog/gemini-omni-flash-pricing-api-guide)

**ASR**
- Sarvam Speech-to-Text: **₹30 per audio hour**, billed per second; **₹45/hr with diarisation**; ₹1,000 free credits — [Sarvam pricing docs](https://docs.sarvam.ai/api/pricing)

**Retail benchmark**
- OpusClip charges **1 credit per minute processed**. Free: 60 credits/month. Starter: **$15/month for 150 credits**. Pro: **$29/month (or $14.50/month annual) for about 300 credits/month** — [OpusClip pricing](https://opus.pro/pricing?via=606ed5); [Castmagic review](https://www.castmagic.io/software-reviews/opus-clip)

**Derived cost per hour of footage at default resolution (1 fps)**
One hour = about 237,600 frame tokens + 115,200 audio tokens = about 360k tokens. Output is assumed to be about 5k tokens of JSON per hour, which is negligible.

| Model | Approx. cost per hour of footage (standard) | Batch |
|---|---|---|
| gemini-2.5-flash-lite | 237.6k × $0.10 + 115.2k × $0.30 ≈ **$0.06** | ≈ $0.03 |
| gemini-3.1-flash-lite | ≈ **$0.12** | ≈ $0.06 |
| gemini-2.5-flash | ≈ **$0.19** | ≈ $0.09 |
| gemini-3.8-flash | 360k × $0.75 ≈ **$0.27** (≈ **$0.54** after 2026-12-01) | — |
| gemini-2.5-pro, chunked into ≤200k prompts | ≈ **$0.45** | — |
| gemini-2.5-pro, single prompt above 200k | ≈ **$0.90** | — |

- High resolution (about 300 tokens/s) roughly triples these costs (derived).
- Separate Sarvam ASR on all audio: ₹30/hr. On candidate clips only (say 10% of footage): about ₹3/hr (derived).

### Inferences
- **Unit economics example (derived; assumes about ₹88/USD, which is not sourced):** a heavy BGMI streamer uploads 60 h/month.
  - Full-VOD Gemini 3.1 Flash-Lite in batch: 60 × $0.06 ≈ $3.6 ≈ ₹320.
  - ASR on candidates: about ₹180.
  - Rendering about 20-40 clips on CPU with ffmpeg, plus storage and egress: unpriced, likely tens of rupees on cheap cloud.
  - Total about ₹500-600 for a heavy user. That is near break-even at ₹499, comfortable at ₹999, and a loss at ₹299 unless hours are capped.
  - With a CV/audio pre-filter that sends only about 15-20% of footage to the LLM, LLM cost falls to about ₹50-70/month. Then ₹299 is viable for about 20-30 hours.
- OpusClip's retail rate of about $6/hour of footage (about ₹500/hr) shows an Indian product at ₹299-999 must cap hours (for example 10-30 h/month) or run a much cheaper pipeline than generalist clippers.
- **Latency (inferred):** Gemini processes uploaded video asynchronously. Batch mode trades latency (hours) for 50% savings. Interactive mode for a 1-hour VOD would likely take minutes. Upload of multi-GB 1080p files from Indian home connections may be the real bottleneck, so downscale to 720p or 480p client-side before upload, since the default Gemini token rate does not depend on input resolution.
- **Self-hosted GPU** (YOLO kill-feed detector at 2-5 fps plus an audio model): a single mid-range GPU can process many hours of footage per GPU-hour, so marginal cost is plausibly well under $0.05 per footage hour. This is an estimate; no sourced GPU benchmark was found.
- Price risk: Google's announced December 2026 to January 2027 increases (for example Flash input from $0.75 to $1.50) show model pricing can double. Design to be model-agnostic, with a fallback to open models such as Qwen-VL self-hosted.

### Gaps
- OpenAI GPT-4o/GPT-5 vision per-minute video pricing was not fetched. OpenAI does not take native video input; frames must be sent as images, which makes cost depend on frame count. This was not verified this session.
- No sourced GPU-hour benchmark for YOLO / OCR throughput on 1080p mobile gameplay.
- INR/USD rate not sourced (₹88/USD assumed).
- Upload bandwidth and storage cost on Indian connections not researched.

## 6. Legal / ToS: Krafton BGMI content policy; YouTube / Instagram reused-content rules

### Takeaway
I could not retrieve Krafton's official BGMI ToS text (403). Krafton's pattern elsewhere is to encourage creator content through programmes (KRAFTON Creator Network, PUBG Mobile creator funds) while treating monetised content as derivative work of its IP, sometimes requiring consent. On YouTube, auto-generated clips from a creator's **own** gameplay are monetisable if they add original value. Mass-produced templated output risks the "inauthentic content" policy, which can demonetise a whole channel. Legal review is needed before launch.

### Cited Findings
- KRAFTON Creator Network: PUBG: BATTLEGROUNDS creators joined on 2025-10-17 and earn through Creator Codes — [PUBG news 9315](https://pubg.com/en/news/9315). Creators earn **at least 5% of net revenue** from in-game purchases using their code. They must be **18+ with at least 1,000 followers** — [Game Developer press release](https://www.gamedeveloper.com/press-release/krafton-launches-krafton-creator-network-to-empower-global-game-creators)
- PUBG: New State's A-Squad Partners programme treats partner content as **"secondary work" built on Krafton's IP**, needing prior Krafton consent to earn revenue. Licensing content to unauthorised platforms is barred — [Digit](https://www.digit.in/news/gaming/pubg-new-state-announces-new-a-squad-partners-program-for-content-creators-62611.html)
- PUBG Mobile (Tencent / Level Infinite) runs a **$6M "Next Star" Global Creator** programme across eight regions — [NetInfluencer](https://www.netinfluencer.com/pubg-mobile-launches-6-million-global-creator-program/)
- Krafton has historically warned third-party BGMI tournament organisers against unapproved events, but creators said classic-match streaming remained allowed (2023 reporting) — [AFK Gaming](https://afkgaming.com/mobileesports/news/krafton-warns-third-party-tournament-organizers-to-halt-bgmi-tournaments); [Sportskeeda](https://www.sportskeeda.com/bgmi/news-we-can-run-house-without-bgmi-8bit-goldy-s8ul-s-stance-amidst-krafton-s-warnings)
- BGMI ToS and privacy policy launched in 2021 (coverage only; clause text not retrieved) — [Sportskeeda ToS coverage](https://www.sportskeeda.com/bgmi/news-battlegrounds-mobile-india-pubg-official-support-terms-service-play-store-link)
- An academic review of video-game user-generated-content policies (merit and monetisation) — [Internet Policy Review](https://policyreview.info/articles/analysis/merit-and-monetisation-video-game-user-generated-content-policies)
- YouTube says its **reused content policy** (commentary, clips, compilations, reactions) is unchanged. The **inauthentic content** policy (replacing "repetitious content", from 2025-07-15) targets mass-produced or templated videos and **applies channel-wide** — [YouTube Help 1311392](https://support.google.com/youtube/answer/1311392); [Tubefilter, July 2026](https://www.tubefilter.com/2026/07/13/youtube-inauthentic-content-monetization-policy-update/amp/). Tubefilter reports a July 2026 renaming to "Generic or Repetitive Content", with YouTube saying the rules have not changed.
- An unverified third-party claim of a YouTube Partner Program overhaul effective 2027-02-01 — [AIR Media-Tech](https://air.io/en/monetization/youtube-monetization-policy-changes-2026-a-complete-dated-timeline) (no corroboration found)

### Inferences
- The legal risk is low for creators clipping their **own** gameplay for their own channels. Publishers generally welcome this, and Krafton funds creator programmes. Risk rises if AI-GCM clips **other** streamers' VODs (copyright of the streamer's commentary and facecam) or offers a feed of compiled BGMI highlights. Position the product as a tool for creators processing their own content.
- The YouTube risk is product-design: if many users post near-identical auto-captioned templates, channels could be flagged as inauthentic. Varied hooks, creator-voiced captions and an edit step mitigate this.

### Gaps
- The exact clauses of Krafton's BGMI ToS on recording, streaming, monetisation and third-party tools could not be retrieved (403). Check battlegroundsmobileindia.com directly or ask Krafton India. A "third-party program" ban usually targets in-game cheats, not post-hoc video analysis, but this is unverified.
- Free Fire / Garena content policy not researched.
- Instagram / Meta reused or "unoriginal content" rules for Reels were not found in this session.
- Current BGMI regulatory status in India: one Sportskeeda explainer references the earlier government ban — [Sportskeeda](https://sportskeeda.com/bgmi/how-bgmi-s-ban-affected-players-content-creators). My understanding is that the game was later reinstated, but I did not verify that here.

## 7. Open datasets and open-source projects for PUBG/BGMI kill detection or highlights

### Takeaway
There are only small community datasets (Roboflow) and one academic PUBG-stream paper. No maintained open-source BGMI or PUBG Mobile highlight pipeline was found. A proprietary labelled dataset of BGMI HUD events would be a real moat.

### Cited Findings
- **BGMI Scoreboard**: about 601 images; classes `kill_feed`, `players`, `teams` — [Roboflow](https://universe.roboflow.com/setu-it3tm/bgmi-scoreboard-pfze2)
- **BGMI-OCR**: about 21 images, CC BY 4.0, with a hosted inference API — [Roboflow](https://universe.roboflow.com/harshalp-8acem/bgmi-ocr)
- **PUBG_Highlight_Detection_v2**: a community model and dataset — [Roboflow](https://universe.roboflow.com/1stbtln/pubg_highlight_detection_v2)
- The PUBG stream dataset used in Ringer & Nicolaou (2018); public release status unverified — [arXiv 1807.09715](https://arxiv.org/pdf/1807.09715)
- QVHighlights / Moment-DETR are general benchmarks (a leaderboard exists), not gaming-specific — [HyperAI leaderboard](https://vercel.hyper.ai/cn/sota/tasks/highlight-detection/benchmark/highlight-detection-on-qvhighlights)
- Generic YOLO-plus-OCR building blocks (Ultralytics custom training) — [Ultralytics YOLOv3 wiki](https://github.com/ultralytics/yolov3/wiki/)

### Inferences
- Bootstrapping plan: label 2-5k frames across HUD variants (BGMI, PUBG Mobile, Free Fire) for kill-feed, kill-counter, "eliminated"/"knocked" banners and facecam rectangles. Fine-tune a small YOLO model. Use the Gemini Flash-Lite free or batch tier to pre-label (weak supervision), with human review.
- Building the MVP is feasible for a small team in weeks for kill and multi-kill clips. "Funny" or "close escape" detection and robust handling of custom HUDs and overlays are the hard parts and need months of data collection.

### Gaps
- A direct GitHub search for "BGMI kill feed" / "PUBG kill feed YOLO" returned no end-to-end repository. A more exhaustive GitHub code search was not done.
- No open Free Fire highlight datasets found.
