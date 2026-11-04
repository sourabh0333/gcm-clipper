# AI creator-feature feasibility for GCM Clipper (as of 4 Nov 2026)

Context: GCM Clipper is a Python pipeline on a CPU-only laptop (8 GB RAM) using Gemini API (gemini-3.5-flash-lite), faster-whisper + Oriserve Hinglish model, YAMNet, RapidOCR; may rent a GPU later. Prices below were read from the vendors' pages on 4 Nov 2026 unless another date is given. USD to INR conversions in Inferences use an assumed ~₹88/$ (not sourced; check the day's rate).

## 1. Running costs: Gemini free tier, paid prices, GPU rental

### Takeaway
Gemini text/video understanding is still free on the free tier for Flash-Lite and Flash models, and cheap on paid (3.5 Flash-Lite: $0.30 in / $2.50 out per 1M tokens), but image generation has no free tier anywhere in the Gemini API, and free-tier data is used by Google to improve products. Occasional GPU jobs cost roughly $0.12-0.90/hr globally (L4 / RTX 4090) and ₹50-362/hr + 18% GST at E2E Networks in India.

### Cited Findings
- Gemini 3.5 Flash-Lite: free tier "Free (all tokens)"; paid $0.30 per 1M input tokens (text/image/video/audio), $2.50 per 1M output; Batch $0.15 / $1.25. — [Google AI Studio pricing](https://aistudio.google.com/docs/pricing)
- Gemini 3.1 Flash-Lite: $0.25 in (text/image/video), $0.50 in (audio), $1.50 out; Gemini 2.5 Flash-Lite: $0.10 in / $0.40 out ($0.30 audio in). Both free on the free tier. — [Google AI Studio pricing](https://aistudio.google.com/docs/pricing)
- Gemini 3.8 Flash: $0.75 in / $3.75 out per 1M tokens through 31 Dec 2026, then $1.50 / $7.50; free tier available. — [Google AI Studio pricing](https://aistudio.google.com/docs/pricing)
- Gemini 2.5 Flash is deprecated; from 1 Dec 2026 requests to it route to Gemini 3.5 Flash-Lite and are billed at that rate. Gemini 2.5 Flash Image shuts down 15 Mar 2027. — [Google AI Studio pricing](https://aistudio.google.com/docs/pricing)
- On every model listed, free-tier content "used to improve products" = Yes; paid tier = No. — [Google AI Studio pricing](https://aistudio.google.com/docs/pricing)
- Free-tier RPM/TPM/RPD numbers are no longer printed on the docs page; they are shown per project in AI Studio. Limits are per project, not per API key; RPD resets at midnight Pacific. Tier 1 = link a billing account (cap $250); Tier 2 = $100 cumulative spend + 3 days. — [Gemini rate limits](https://aistudio.google.com/docs/rate-limits)
- Third-party blogs give conflicting Flash-Lite free-tier figures: 30 RPM / 1,000 RPD (Jan 2026 guide) vs a cut to 5 RPM / 100 RPD (Apr 2026 tracker); one says free tier was limited to Flash and Flash-Lite models from April 2026. — [agentdeals.dev](https://agentdeals.dev/gemini-api-pricing-changes); [yingtu.ai](https://yingtu.ai/blog/google-gemini-api-free-tier); [tinkerllm](https://tinkerllm.com/blog/gemini-api-free-tier-limits-rate-quotas/) (unofficial, conflicting)
- E2E Networks H100 on-demand ₹362/hr (~$3.77), excl. GST, Delhi NCR and Chennai. — [E2E H100 page](https://www.e2enetworks.com/gpus/nvidia-h100.md)
- E2E A100 40GB ₹170/hr, A100 80GB ₹220/hr (Nov 2025 blog). — [E2E blog](https://e2enetworks.com/blog/nvidia-a100-price-india)
- E2E L4 roughly ₹50-70/hr; spot about 65-70% below on-demand (E2E "cloud-terms" guide pages, not the rate card). — [E2E GPU rental India](https://e2enetworks.com/cloud-terms/gpu/gpu-rental-india); [E2E pricing](https://e2enetworks.com/pricing)
- 18% GST is added on top of E2E listed prices. — [E2E pricing](https://e2enetworks.com/pricing)
- IndiaAI subsidy can bring eligible startups' H100 access to about ₹67-92/GPU-hr, approval-gated. — [Hugging Face blog (Daya Shankar)](https://huggingface.co/blog/daya-shankar/nvidia-h100-price-india) (secondary)
- RunPod RTX 4090 Secure Cloud $0.89/hr (Oct 2026); older mid-2026 figures ~$0.34/hr community. Vast.ai RTX 4090 ~$0.25-0.40/hr; Vast.ai L4 $0.12-0.20/hr. — [gpuflow blog](https://gpuflow-blog.pages.dev/en/gpu-rental-pricing-comparison-2026); [deploybase.ai](https://deploybase.ai/articles/vast-ai-gpu-cloud-pricing-complete-guide-vs-hr-for-every-gpu); [spheron](https://www.spheron.network/blog/runpod-vs-vastai-2026/) (third-party, conflicting)

### Inferences
- A title+description+hashtags call (≈3,000 input tokens of transcript, ≈500 output) on 3.5 Flash-Lite paid costs about $0.0009 + $0.00125 ≈ $0.002 (~₹0.2) per clip; Batch halves this. On the free tier it is ₹0 until the daily cap.
- The "free tier trains Google's models" rule matters for a product: creators' stream audio/frames sent on the free tier may be used by Google. Before selling to creators, move to paid Tier 1 (just link billing) or disclose this in the privacy policy.
- For occasional jobs (thumbnail generation, TTS, BiRefNet batches), a Vast.ai/RunPod 4090 at ~$0.3-0.9/hr is cheaper than E2E's data-centre GPUs; E2E's advantage is INR billing, GST invoice and Indian data residency. An L4 at ~$0.15/hr (Vast) or ₹50-70/hr (E2E) is enough for whisper-large, SDXL/FLUX-klein-4B, and BiRefNet.
- Since 3.5 Flash-Lite is 3x the input price of 2.5 Flash-Lite, the cheapest paid path for bulk text jobs is 2.5 Flash-Lite ($0.10/$0.40) while it exists.

### Gaps
- Exact current free-tier RPM/RPD for gemini-3.5-flash-lite: not published on the docs page; must be read in AI Studio for the project.
- Video tokenisation rate (tokens per second of video) for the 3.x models was not checked this round; it drives cost of sending clips to Gemini.
- No official E2E L4 rate-card line found; only E2E guide pages.

## 2. AI thumbnails (frame pick + text + face cut-out + generation/editing)

### Takeaway
A CPU-only thumbnail feature is feasible now: pick frames from the pipeline's existing peaks, cut out the facecam with rembg/BiRefNet (MIT), and composite text with Pillow; AI image editing is an optional paid add-on (Gemini Nano Banana 2 Lite ≈ $0.034 per 1K image, $0.017 in Batch; no free tier). Open generators: FLUX.2 [klein] 4B is Apache 2.0 (commercial OK); FLUX.2 [klein] 9B is non-commercial.

### Cited Findings
- Gemini image models have no free tier ("Not available"). Nano Banana 2 Lite (Gemini 3.1 Flash Lite Image): $0.25/1M input, $0.0336 per 1K image; Batch $0.0168. Nano Banana 2.1: $0.0336 (1K), $0.0504 (2K), $0.113 (4K); Batch half. Nano Banana 2 (3.1 Flash Image): $0.067 (1K), $0.101 (2K). Nano Banana Pro: $0.134 (1K/2K). — [Google AI Studio pricing](https://aistudio.google.com/docs/pricing)
- FLUX.2 [klein] 4B (and 4B Base) released under Apache 2.0; FLUX.2 [klein] 9B under the "FLUX Non-Commercial License" (renamed from FLUX [dev] Non-Commercial License). Sources differ on whether 9B outputs may be used commercially. — [BFL blog](https://bfl.ai/blog/flux2-klein-towards-interactive-visual-intelligence); [HF LICENSE for klein-9B](https://huggingface.co/ModelsLab/FLUX.2-klein-9B/blob/main/LICENSE.md); [VentureBeat](https://venturebeat.com/technology/black-forest-labs-launches-open-source-flux-2-klein-to-generate-ai-images-in)
- rembg is MIT-licensed and ships BiRefNet variants (birefnet-general, birefnet-general-lite); the BiRefNet ONNX weights are listed as MIT. — [rembg GitHub](https://github.com/danielgatis/rembg); [rembg PyPI](https://pypi.org/project/rembg/2.0.71/); [ONNX model repo](https://huggingface.co/knowicki/rembg-models)
- One informal test: BiRefNet takes "seconds per image" on CPU and under 1 s per 1024×1024 image on GPU; rembg (u2net) is faster but has weaker edges. — [ice-ice-bear blog](https://ice-ice-bear.github.io/posts/2026-04-15-birefnet/) (anecdotal)
- YouTube announced (Dec 2024) stronger enforcement against "egregious clickbait" — titles/thumbnails promising something the video doesn't deliver — starting in India, focused on breaking news/current events; videos removed without strikes initially. — [Storyboard18](https://www.storyboard18.com/digital/youtube-to-crack-down-on-egregious-clickbait-in-india-51429.htm); [Social Samosa](https://www.socialsamosa.com/industry-updates/youtube-crack-down-misleading-clickbait-videos-8556876); [marketech-apac](https://marketech-apac.com/youtube-to-strengthen-enforcement-against-misleading-clickbait-in-video-titles-thumbnails-first-rollout-in-india)
- YouTube's altered/synthetic disclosure policy says using AI for "scripts, titles, or thumbnails" is production assistance and needs no disclosure. — [YouTube Help: disclosing altered or synthetic content](https://support.google.com/youtube/answer/14328491)

### Inferences
- Best MVP: deterministic thumbnails (best frame from existing kill/peak scores + facecam cut-out via birefnet-general-lite + Hinglish hook text from Gemini + template), cost ₹0 on the laptop; a few seconds per image on CPU is acceptable for a handful of thumbnails per job.
- AI-edited thumbnails (e.g., "add explosion, make face shocked") via Nano Banana 2 Lite cost ~₹3 per image (~₹1.5 batch); offer as a paid/limited feature. Running FLUX.2 klein 4B locally on 8 GB RAM CPU is not practical; it needs a rented GPU.
- Risk stays low for gaming thumbnails as long as the thumbnail shows something that happens in the clip; the India clickbait enforcement targets news, but "fake" scenes (e.g., generated characters not in the video) push towards misleading territory.

### Gaps
- No verified CPU benchmark of BiRefNet-lite vs u2net on an 8 GB laptop; needs a local test.
- FLUX.1 [schnell] licence (believed Apache 2.0) and SDXL licence (OpenRAIL++) not verified in this round.
- No 2025-2026 data on how many gaming videos were hit by the clickbait policy.

## 3. Titles, descriptions, hashtags, chapters in Hinglish/Hindi; free SEO data

### Takeaway
Technically easy and nearly free: the pipeline already has Hinglish transcripts, and a Flash-Lite call costs ~₹0.2 per clip on paid (₹0 on free tier). Free keyword data is the weak point: no official free keyword-volume API was found.

### Cited Findings
- Gemini 3.5 Flash-Lite paid prices $0.30/$2.50 per 1M tokens; Batch half; free tier free. — [Google AI Studio pricing](https://aistudio.google.com/docs/pricing)
- Sarvam also sells LLM chat (Sarvam 105B ₹15 in / ₹60 out per 1M tokens; Gemma 4 ₹35/₹90). — [Sarvam API pricing](https://www.sarvam.ai/api-pricing)
- YouTube says AI-written titles are production assistance and need no AI disclosure; clickbait enforcement covers titles that promise what the video doesn't deliver. — [YouTube Help](https://support.google.com/youtube/answer/14328491); [Storyboard18](https://www.storyboard18.com/digital/youtube-to-crack-down-on-egregious-clickbait-in-india-51429.htm)

### Inferences
- Chapters for long videos can come from transcript timestamps + highlight peaks already computed; Gemini only needs to name them.
- Sarvam 105B is ~4x cheaper per input token than 3.5 Flash-Lite at ~₹88/$ ($0.30 ≈ ₹26 vs ₹15), and may write more natural Hindi; worth an A/B test, but Gemini's free tier wins at zero spend.
- A free proxy for SEO: YouTube search autocomplete and trending titles in the creator's niche, plus the creator's own Analytics search terms. Treat these as unofficial signals.

### Gaps
- Did not find a free, official keyword-volume source for YouTube (Google Trends API / YouTube autocomplete terms of use not verified this round).
- No benchmark of Hinglish title quality across Gemini vs Sarvam.

## 4. Dubbing and subtitles into Tamil, Telugu, Bengali, Marathi, English

### Takeaway
Subtitles are cheap and feasible (translate the transcript: Sarvam ₹2 per 1,000 characters, or open IndicTrans2 (MIT) on CPU/GPU, or Gemini). YouTube's own free auto-dubbing does not cover the main need: from a Hindi original it only offers English and Bengali dubs, and Marathi is not supported at all. Paid AI dubbing via Sarvam is ₹40/min.

### Cited Findings
- YouTube auto-dubbing: Hindi originals can get English or Bengali dubs; Tamil and Telugu are dub targets only from English originals; Marathi is not listed. Excludes videos >120 min, music-only/little speech, too-fast speech, and videos containing copyrighted content. Lip sync is experimental, select channels only. Dubs can't be edited; creator can hold for manual publish. — [YouTube Help: automatic dubbing](https://support.google.com/youtube/answer/15569972)
- YouTube expanded auto-dubbing to 27 languages and all creators in Feb 2026, with "Expressive Speech" in eight languages. — [India TV](https://www.indiatvnews.com/technology/news/youtube-auto-dubbing-feature-expands-to-all-users-now-supports-27-languages-2026-02-05-1029070); [Storyboard18](https://www.storyboard18.com/digital/youtube-expands-auto-dubbing-to-27-languages-adds-more-natural-and-expressive-voices-88923.htm)
- Sarvam (INR, pay-as-you-go): translation ₹2.00 per 1,000 chars; transliteration ₹2.00; STT ₹0.49/min (₹0.59 with diarization); Bulbul V3 TTS ₹3.00 per 1,000 chars; Bulbul V4 Flash ₹1.00 per 1,000 chars (50% off until 12 Nov; normally ₹2.00); voice cloning ₹2.00 per 1,000 chars; audio/video dubbing ₹40/min; ₹100 free credits on signup, non-expiring. — [Sarvam API pricing](https://www.sarvam.ai/api-pricing)
- IndicTrans2 repository is MIT-licensed (AI4Bharat). — [ecosyste.ms](https://awesome.ecosyste.ms/projects/github.com%2FAI4Bharat%2FIndicTrans2); [HF LICENSE](https://huggingface.co/ai4bharat/indictrans2-indic-en-1B/blame/83e435874f48d25a38277197845c48dbf0a597ca/LICENSE)
- IndicF5 (polyglot Indic TTS, 1,417 hours of speech) listed as MIT on the government AIKosh portal; Indic Parler-TTS listed as MIT on AIKosh but Apache 2.0 by aggregators, and is gated by AI4Bharat. — [AIKosh IndicF5](https://aikosh.indiaai.gov.in/home/models/details/aibharat_indicf5.html); [AIKosh Indic Parler-TTS](https://aikosh.indiaai.gov.in/home/models/details/ai4bharat_indic_parler_tts_text_to_speech_model.html); [dev.co](https://dev.co/ai/llms/indic-parler-tts)
- Bhashini: aggregators say API access is free after registration (22 scheduled languages, ASR/TTS/translation), but CDO Magazine reports Bhashini is moving to a paid model (no date/terms found). bhashini.ai / bhashiniservices.com are private vendors, not the government platform. — [CDO Magazine](https://www.cdomagazine.tech/aiml/indian-govt-ai-translation-platform-bhashini-gears-up-for-monetization); [dev.to Indic localization costs](https://dev.to/mr_manushukla/22-scheduled-languages-one-app-what-indic-localization-actually-costs-to-ship-in-2026-12ag)
- Gemini TTS: 3.8 Flash-Lite TTS ~$0.0015 per 10 s of audio and 3.8 Flash TTS ~$0.00225 per 10 s through 31 Dec 2026 (then doubled); free tier available. — [Google AI Studio pricing](https://aistudio.google.com/docs/pricing)

### Inferences
- Per 60-second Short (~900 characters of Hinglish speech): subtitles in one extra language ≈ ₹2 via Sarvam, ~₹0 via Gemini free tier or IndicTrans2; a synthetic-voice dub ≈ ₹2 translate + ₹1-3 TTS ≈ ₹3-5 per language, vs ₹40 via Sarvam's full dubbing endpoint. Gemini Flash-Lite TTS ≈ $0.009/min (~₹0.8) through 2026.
- Gaming clips are hard for dubbing: fast, overlapping, slang-heavy speech, and game audio; YouTube excludes "too fast" speech and videos with copyrighted content. Subtitles (burned-in or uploaded caption tracks) are the safer first feature; dubbing should be a later experiment.
- IndicTrans2 1B is heavy for an 8 GB CPU laptop; the distilled 200M variants are the realistic CPU option, with GPU recommended for bulk.

### Gaps
- No found benchmark of IndicTrans2 vs Sarvam vs Gemini on code-mixed gaming Hinglish.
- Current Bhashini pricing/terms not confirmed from bhashini.gov.in.
- AI4Bharat's own HF model-card licences for Indic Parler-TTS not confirmed.

## 5. AI voice-over / commentary and legal/ethical issues

### Takeaway
Technically feasible (Gemini TTS, Sarvam Bulbul, IndicF5), cheap per clip. YouTube requires an "AI use" disclosure for realistic content that makes a real person appear to say something they didn't; cloning the creator's own voice for voice-over or dubs needs no disclosure. Cloning anyone else's voice without consent should be blocked.

### Cited Findings
- Must disclose: realistic content that makes "a real person appear to say or do something they didn't do", altered footage of real events, realistic scenes that didn't occur, AI music as main focus. Disclosure is via the "AI use" setting in Studio. — [YouTube Help](https://support.google.com/youtube/answer/14328491)
- No disclosure needed: non-realistic content, aesthetic edits, AI for scripts/titles/thumbnails, captions, audio repair, upscaling, and "cloning one's own voice for voice-overs or dubs". — [YouTube Help](https://support.google.com/youtube/answer/14328491)
- Disclosure alone doesn't limit reach or monetization; repeated non-disclosure can lead to removal or YPP suspension; YouTube may auto-label content with C2PA metadata or detected as AI. — [YouTube Help](https://support.google.com/youtube/answer/14328491)
- Sarvam sells real-time voice cloning at ₹2.00 per 1,000 characters. — [Sarvam API pricing](https://www.sarvam.ai/api-pricing)

### Inferences
- Product rule: allow voice cloning only of the account holder's own voice with a recorded consent step; generic narrator voices for "commentary" are fine and don't need disclosure unless they impersonate a real person.
- AI commentary that sounds like the streamer saying things they never said falls under the disclosure rule; the app should set or remind the "AI use" flag when it posts.

### Gaps
- Indian law on voice cloning/deepfakes (IT Rules amendments on synthetic content labelling) not researched in this round.

## 6. Compilations/montages with beat-synced cuts and licence-clean music

### Takeaway
Beat-sync cutting is easy on CPU (beat tracking + ffmpeg), but music licensing is the risk: even "free" Pixabay tracks can trigger Content ID claims because some composers register them; a claim usually redirects monetization rather than removing the video, and Pixabay's licence certificate is the dispute tool.

### Cited Findings
- Some Pixabay tracks are registered in Content ID and can trigger automated claims even when used legally; a Pixabay license certificate (available when logged in) can be used to dispute. — [HeyGen help](https://help.heygen.com/en/articles/8986144-content-id-claims-on-youtube); [Smart Hustlers blog](https://smarthustlers101.blogspot.com/2022/09/how-to-clear-youtube-content-id-claim.html)
- Pixabay has no direct Content ID integration to signal clearance to YouTube (claim by a competitor). — [Thematic vs Pixabay](https://hellothematic.com/thematic-vs-pixabay/) (vendor bias)
- A Content ID claim does not take the video down; the rights holder's policy (usually monetization) applies. — [newstory checklist](https://newstory-video-us.pages.dev/blogs/free-background-music-youtube-copyright-checklist)
- YouTube auto-dubbing skips videos containing copyrighted content, so a claimed music track can also block dubbing. — [YouTube Help: automatic dubbing](https://support.google.com/youtube/answer/15569972)

### Inferences
- Safest source is the YouTube Audio Library (used inside YouTube itself); the app should not bundle or redistribute tracks, but let the creator pick a track they downloaded, and store the licence certificate with the job.
- Game soundtrack/in-game music in BGMI footage is a separate Content ID risk the app can't fully remove; a "duck game music under commentary" option helps but is not a guarantee.

### Gaps
- YouTube Audio Library and Free Music Archive licence terms (attribution, CC-BY vs CC-NC per track) not fetched in this round; FMA tracks vary per track and NC licences block commercial use.
- No data on Content ID claim rates for Pixabay tracks.

## 7. Smart reframing, auto-zoom on kills, dead-time and silence removal

### Takeaway
All feasible on CPU with existing signals. Facecam detection and static reframing are cheap; per-frame subject tracking for zooms is the expensive part and is better done at low frame rate on CPU or on a rented GPU.

### Cited Findings
- No new external sources were collected for this feature in this round.

### Inferences
- Facecam position in BGMI streams is usually fixed: detect it once per stream (face detector on a few sampled frames, or RapidOCR/edge layout), then crop a fixed facecam box + gameplay box for 9:16 stacks. CPU cost is negligible.
- "Auto-zoom on kills": the pipeline already finds kill moments (OCR of kill feed, audio peaks), so a zoom keyframe (ffmpeg zoompan/crop at those timestamps toward the crosshair centre) needs no tracking model; true subject tracking is a GPU-era upgrade.
- Silence/dead-time removal can use energy thresholds + VAD from the existing whisper step plus YAMNet's non-speech classes; ffmpeg's silencedetect is a zero-cost baseline.

### Gaps
- No benchmark of face detectors (e.g., MediaPipe, YuNet) on 8 GB CPU for this pipeline; licences of those detectors not verified this round.

## 8. Comment analysis/reply suggestions in Hinglish; chat highlight detection from live chat replay

### Takeaway
Chat-replay-based highlight detection is feasible today and free: chat-downloader (no auth) and yt-dlp can pull a finished stream's chat replay, and message-rate spikes are a strong extra signal. Reply suggestions are cheap with Gemini, but posting replies through the YouTube Data API costs 50 quota units each against a default 10,000/day.

### Cited Findings
- chat-downloader (xenova) downloads chat from livestreams, videos and past broadcasts without authentication, via pip CLI or Python. — [chat-downloader GitHub](https://github.com/xenova/chat-replay-downloader/)
- yt-dlp supports `youtube_live_chat` and `youtube_live_chat_replay` protocols. — [yt-dlp source mirror](https://jfr.im/git/yt-dlp.git/blob/11233f2afdfc55d3672a7c17ad919a3f70005c19:/yt_dlp/downloader/youtube_live_chat.py)
- YouTube Data API default quota 10,000 units/day; commentThreads.list = 1 unit; commentThreads.insert and comments.insert = 50 units; even invalid requests cost ≥1 unit; resets midnight PT. — [YouTube Data API quota calculator](https://developers.google.com/youtube/v3/determine_quota_cost)

### Inferences
- Max ~200 posted replies/day per API project at default quota, shared across all users of the app; for a multi-creator product, "suggest, then the creator posts or bulk-approves" is safer, and a quota increase request would be needed at scale.
- Reading comments is cheap (1 unit per list page), so Hinglish sentiment/question clustering via Gemini Flash-Lite costs only token spend.
- Scraping chat replay via unofficial tools may break when YouTube changes its pages and sits outside the official API; it should be optional.

### Gaps
- YouTube API Services terms on storing/analysing chat and comment data for a commercial app not checked this round.
- No data on how well chat-rate spikes correlate with good BGMI clips.

## 9. Brand-safety scanning and auto-bleep

### Takeaway
Feasible on CPU: the pipeline already has word-level Hinglish transcripts, so a curated Hindi/Hinglish profanity lexicon + optional classifier gives timestamps to bleep with ffmpeg. Open Hinglish abuse classifiers exist but are research-grade or unverified.

### Cited Findings
- HinTox (Hugging Face): binary offensive/not-offensive classifier for Roman-script Hinglish covering obfuscated spellings, profanity, casteist slurs; no independent evaluation; licence not verified. — [HinTox model card](https://huggingface.co/Keshav0av/HinTox)
- HEOT (Hindi-English Offensive Tweet) dataset: non-offensive / abusive / hate-speech classes. — [ACL W18-3504](https://preview.aclanthology.org/fix_video/W18-3504.pdf)
- "Mind Your Language" (AAAI-19) built a 209-word Hinglish profanity dictionary. — [arXiv 1809.08652](https://arxiv.org/pdf/1809.08652v1.pdf); [MIDAS IIITD](https://midas.iiitd.edu.in/papers/paper/Mind-Your-Language.html)
- A 2023 ACL student paper found RoBERTa most accurate across English and Hinglish abuse datasets. — [ACL 2023 paper S5](https://virtual2023.aclweb.org/paper_S5.html)

### Inferences
- A lexicon over ASR word timestamps is the practical first version; the weak link is ASR misrecognising slurs (missed bleeps) and false positives, so offer a review screen before export.
- Text-trained classifiers (tweets) will transfer imperfectly to spoken gaming banter; treat model scores as flags, not automatic bleeps.

### Gaps
- Licences of HEOT data and HinTox weights not confirmed; commercial-use status unknown.
- No word-level accuracy figures for the Oriserve Hinglish whisper model on profanity.

## 10. Performance prediction / personal ranking from the creator's own analytics

### Takeaway
No sources were collected this round; with a single creator's small data (tens to low hundreds of Shorts), only simple, transparent methods are realistic.

### Cited Findings
- No external sources were collected for this question.

### Inferences
- With <200 videos, a learned predictor will overfit; realistic options are re-weighting the existing highlight scores by what has worked for this creator (e.g., which clip types—clutch, funny, kill streak—got above-median views/retention), presented as "your top patterns", not a prediction.

### Gaps
- YouTube Analytics API quotas, available metrics for Shorts (e.g., swipe-away rate, retention) and terms of use not verified this round.
- No published studies found on view-prediction accuracy with small single-channel datasets.
