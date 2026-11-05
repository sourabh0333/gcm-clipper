# India-specific and gaming-specific feature candidates for GCM Clipper (as of 5 November 2026)

Scope: features no global clipping tool (Opus Clip, Eklipse, Vizard, etc.) offers, but a small Indian team could build. For each candidate: evidence of demand (clearly separated from our assumptions), how it would work, dependencies, and cost. Prices are given with the date and currency the source states. Where a fetch failed or no source exists, it is listed as a gap, not guessed.

Overall ranking (my read of the evidence, see each section):

| # | Candidate | Demand evidence | Feasibility | Cost to run | Verdict |
|---|---|---|---|---|---|
| 1 | WhatsApp/Telegram control surface | Assumed (no direct evidence creators want it; WhatsApp ubiquity is the argument) | High (Telegram) / Medium (WhatsApp, Meta approval + per-message fees) | Telegram ₹0; WhatsApp ₹0.145/utility msg + BSP fee | Build Telegram first, WhatsApp later |
| 2 | Match recap cards / result-screen OCR | Indirect: Scrymz exists for organisers; year-end "recap" articles | High (fixed-layout OCR, Scrymz proves BGMI result screens are machine-readable) | Near zero (local OCR) | Strong "only we do this" candidate |
| 3 | Squad multi-POV merge | None found for BGMI squads; POV rights fights show orgs value POV | Medium (sync by audio/kill-feed) | Low | Park; assumption-only |
| 4 | Esports orgs / organisers as customers | BMPS 2026 729K peak viewers; orgs have in-house teams; no evidence they buy tools | Low as a sales motion for a small team | — | Not a launch segment |
| 5 | Rooter / Loco plug-in | Rooter is commerce-first (70% revenue from shop); Loco says India "not a priority"; neither shows a public API | Low | — | Drop |
| 6 | Regional captions/titles | Strong: Tamil gaming channels at 2.9M–4.1M subs; Telugu creator tournaments | High | IndicTrans2 MIT/free; Sarvam ₹30/hr STT; Gemini 2.5 Flash-Lite $0.10/M in | Build (Tamil/Telugu first) |
| 7 | Low-bandwidth "mark then upload" | Strong structural: India median mobile download ~40 Mbps (May 2026), uploads much lower; VOD route is barred by YouTube API policy | High for marker-segment upload | Zero extra | Build; do NOT rely on YouTube VOD download |
| 8 | Brand-safety / sponsor tools | YouTube rules make bleeping relevant; brand platforms pull data from YouTube API directly, so "analytics export" demand is weak | Medium | Low | Build auto-bleep; skip media-kit export |
| 9 | Hindi UI | Indirect: ShareChat engagement rose when English removed (2018); ~70% of Indian users prefer Indic languages (Google) | High (string files) | Near zero | Build Hinglish/Hindi toggle |
| 10 | Live-stream tie-ins | API feasible: streamList 5 units per call; OBS/Discord free | Medium | ₹0 within default 10,000 units/day | Build later, behind a flag |
| 11 | India pricing packaging | Razorpay 2%+GST on UPI; UPI AutoPay ₹15,000 cap; Apple Creator Studio ₹399/mo sets a local anchor | High | 2.36% of revenue | ₹49-a-stream via UPI is viable |

---

## 1. WhatsApp as the control surface (notifications, "reply 1 to post", clip delivery)

### Takeaway
Technically feasible but WhatsApp is now pay-per-message in India (marketing ₹1.09, utility ₹0.145 per delivered message from 1 Jan 2026; service messages charged beyond 1,000/month from 1 Oct 2026), needs Meta approval and a BSP, and I found no evidence creators specifically want WhatsApp over push notifications. Telegram's Bot API is free, allows 50 MB file sends, and is the cheaper first implementation.

### Cited Findings
- Meta replaced conversation-based pricing with per-message pricing on 1 July 2025; only business-sent messages are charged; India marketing rate rose 1 Jan 2026; India authentication-international rose 1 Apr 2026; Meta changes prices only on 1 Jan/1 Apr/1 Jul/1 Oct — [Meta WhatsApp pricing](https://developers.facebook.com/docs/whatsapp/pricing)
- Free tier is 1,000 service messages per business phone number per month; from 1 Oct 2026 the 1,001st service message in a month is charged, and utility messages inside the 24-hour service window are also charged — [Meta WhatsApp pricing](https://developers.facebook.com/docs/whatsapp/pricing)
- India per-message rates effective 1 Jan 2026 (INR): marketing ₹1.09, utility ₹0.145, authentication ₹0.145, service free inside the 24-hour window (BSP reseller page, not Meta's rate card) — [AiSensy news, Jan 2026](https://news.aisensy.com/123053-whatsapp-per-message-pricing-update-effective-january-1-2026)
- Third-party guides disagree on the marketing rate (₹0.66, ₹0.78–₹0.90, ₹1.09 per message) and note BSP platform fees plus 18% GST on top — [MyOperator 2026](https://myoperator.com/blog/whatsapp-business-api-pricing-india-2026); [Baat.ai](https://baat.ai/blog/whatsapp-api-pricing-india); [AiSensy pricing guide](https://m.aisensy.com/blog/whatsapp-business-pricing/)
- Vendor estimate of all-in BSP cost for a small India operation: $42–$90/month (2026, vendor blog) — [Setsmart broadcast guide](https://setsmart.io/blog/whatsapp-broadcast)
- WhatsApp Channels: vendor guides say Channels are free with no creator payouts and no API in 2026; another vendor describes an "API newsletter" option, so API access to Channels is unclear — [Kanal Channels guide 2026](https://getkanal.com/blog/whatsapp-channels-feature-guide); [Setsmart](https://setsmart.io/blog/whatsapp-broadcast)
- Telegram Bot API is free; bots send files up to 50 MB; limits roughly 1 message/second per chat, 20/minute in groups, ~30 messages/second bulk without paid broadcasts — [Telegram Bot FAQ](https://core.telegram.org/bots/faq)

### Inferences
- A "reply 1 to post" flow is a user-initiated message, so WhatsApp replies from the creator are free and the app's confirmation inside the 24-hour window counts against the 1,000 free service messages per month per number. At ~10 streams/creator/month and ~5 messages per stream, one shared number covers ~20 creators free; beyond that it is ~₹0.145 per utility message (negligible, but each utility template needs Meta approval).
- The real costs are fixed: a BSP subscription (vendor figures ~$39/month and up), Meta business verification, and template approvals. For a zero-spend policy, Telegram first, email second, WhatsApp only when paying users exist.
- Clip delivery: WhatsApp media messages are the same per-message price; Telegram's 50 MB bot limit fits a 30–60 s 9:16 clip at typical bitrates. (Our assumption on clip size.)
- Demand is our assumption. No source showed creators asking for WhatsApp control; the argument is only that WhatsApp is the default Indian messaging app.

### Gaps
- Meta's official India rate card (CSV/PDF) was not fetched; the ₹1.09/₹0.145 figures come from a BSP's summary.
- Whether WhatsApp Channels can be posted to via API in 2026 is unresolved (sources conflict).
- No survey or creator interview evidence on preferred notification channel.

---

## 2. Match recap cards, stats overlays and stream recap with chapters (BGMI / Free Fire)

### Takeaway
BGMI result screens are machine-readable: Scrymz already turns BGMI/PUBG Mobile result screenshots into points tables for tournament organisers using AI extraction, and open-source projects do the same for Apex and Valorant with fixed-coordinate OCR. No creator-side tool generating per-match recap cards or a chaptered stream recap was found, so this is a genuine gap, though demand is inferred rather than measured.

### Cited Findings
- Scrymz: "AI match scanner + points table maker for esports organizers"; upload match screenshots, AI extracts team names, kills and placements, matches them to a slot list, builds points tables, graphics and Excel exports; supports BGMI and PUBG Mobile "for now"; works without predefined templates; focus is India's grassroots scrim community; no pricing or accuracy numbers given — [Scrymz on Product Hunt](https://www.producthunt.com/p/scrymz-ai-points-table-maker/scrymz)
- Andern provides real-time stats for official BGMI tournaments (data feed, not OCR) — [Andern app listing](https://mwm.ai/apps/andern/6548005442)
- Open-source Apex Legends OCR tool watches for the match summary screen and parses stats; author notes consistency of interpretation was a weak point — [apex-ocr GitHub](https://github.com/Rosswell/apex-ocr)
- Valorant scoreboard extraction from screenshots relies on fixed screen coordinates — [valorant-data-extraction GitHub](https://www.github.com/tam0w/valorant-data-extraction)
- Year-end "BGMI 2025 Recap" guides exist, showing players care about kills/wins stats summaries — [GamingNewsLab](https://gamingnewslab.com/news/bgmi-2025-recap-how-to-check-your-total-kills-wins-and-year-end-stats/)
- YouTube is discontinuing viewer-facing Clips and giving creators a Studio "Video Clips" tool that clips from videos and archived live streams, with "auto-suggestions" of clippable moments slated for later in 2026 — [Tubefilter, 17 Apr 2026](https://www.tubefilter.com/2026/04/17/youtube-clipping-tool-viewer-clips-shorts/)

### Inferences
- How it works: the pipeline already finds the HUD; add a "result screen" detector (fixed layout, same phone resolution per creator), run local OCR (Tesseract/PaddleOCR, free) on kills, placement, damage, survival time; render a PNG card with the creator's branding; attach it to the approve-then-post flow as a Community post or Instagram image. Cost: CPU only.
- Stream recap long video: the per-match result timestamps give chapters for free ("Match 1 – 12 kills – #2"), which doubles as YouTube chapter markers in the description.
- Scrymz proves the OCR is reliable enough for organisers to trust points tables, so creator-grade accuracy (one squad, one screen) should be easier. Must handle Free Fire's different result layout separately.
- YouTube's own Studio clipping tool is generic; it does not read game stats, so recap cards remain a differentiator. Demand for the cards themselves is our assumption; the evidence is that organisers pay attention to the same data.

### Gaps
- No usage or pricing data for Scrymz; no measured demand for recap cards among individual creators.
- Free Fire result-screen OCR feasibility not checked by any source.

---

## 3. Squad POV merging (multi-POV clips from teammates' recordings)

### Takeaway
No source describes multi-POV tooling or demand for it among BGMI squads or Indian orgs; the only related evidence is that orgs fought for POV streaming rights in 2024 as a revenue source, and ESL/Plays.tv offered player-POV recordings for IEM. Treat demand as assumed and park it.

### Cited Findings
- BGMI orgs pushed for POV streaming rights in the 2024 season; one team leader said they would not play a tournament without POV rights because they "have to look at other opportunities of earning" beyond prize pools — [AFK Gaming](https://afkgaming.com/mobileesports/news/bgmi-teams-to-refrain-from-playing-tournaments-on-mondays)
- ESL and Plays.tv offered per-player POV recordings with player audio for Intel Extreme Masters — [ESL FACEIT Group](https://eslfaceitgroup.com/?p=3699); [GamesBeat](https://gamesbeat.com/?p=104404)
- Krafton's BGMI marketing leans on squads and real-life friendships (Diwali campaign) — [BW Marketing World](https://bwmarketingworld.com/article/krafton-india%E2%80%99s-diwali-bgmi-campaign-celebrates-real-life-friendships-537788)

### Inferences
- Feasibility: four phone recordings can be aligned by the shared match clock in the HUD (kill-feed timestamps or the zone timer) plus audio cross-correlation of Discord voice; render as 2x2 or picture-in-picture 9:16. Requires all four teammates to use the app (adoption hurdle) and upload four files (bandwidth hurdle, see candidate 7).
- Demand is our assumption only. The squad-content angle fits how BGMI is marketed, but no org or creator was found asking for it.

### Gaps
- No evidence of demand from squads, orgs or esports organisers; no existing multi-POV product for mobile games found.

---

## 4. Esports orgs and tournament organisers as customers

### Takeaway
BGMI esports is big (BMPS 2026 finals 729K peak viewers; BGMS Season 5 finals Sept 2026) and the top orgs run in-house content teams, but I found no evidence that S8UL, GodLike, Nodwin or Skyesports buy third-party clipping tools, and no current editor job postings for them. Not a launch segment for a small team.

### Cited Findings
- BMPS 2026: GodLike Esports won; finals ended 21 June 2026; 729K peak viewers — [Outlook Respawn](https://respawn.outlookindia.com/gaming/gaming-news/bmps-2026-sets-record-as-godlike-wins-first-bgmi-title); [SportsDigest](https://sportsdigest.in/?p=196853)
- BGMS Season 5 Grand Finals scheduled for 5 September 2026 (Nodwin) — [Digital Terminal](https://digitalterminal.in/amp/story/gaming/nodwin-gaming-reveals-indias-bgmi-team-for-esports-nations-cup-2026)
- Sportskeeda publishes day-by-day BGMS standings and highlight write-ups, showing daily editorial coverage demand — [Sportskeeda BGMS 2025](https://widgets.sportskeeda.com/bgmi/news-bgms-2025-league-stage-overall-standings-highlights)
- S8UL was named Content Group of the Year at Esports Awards 2022 and planned to expand as an international content team — [AFK Gaming](https://afkgaming.com/esports/news/s8ul-esports-emerges-as-the-content-group-of-the-year-at-the-esports-awards-2022)
- Rooter signed GodLike in May 2022 for exclusive live-streaming rights (BGMI, Free Fire, CODM) as part of a ₹100 crore esports investment; GodLike moved from Loco — [Free Press Journal, 25 May 2022](https://www.freepressjournal.in/business/rooter-signs-gaming-team-godlike-as-part-of-its-rs-100-cr-investment-in-indias-e-sports-industry)
- India gaming video-editor postings found in 2026: SuperGaming (Pune, 18 Feb 2026), BLAST (Mumbai, 24 Mar 2026); none from S8UL, GodLike or Nodwin — [SuperGaming on Marketing Monk](https://www.marketingmonk.so/jobboard/jobs/video-editor-at-supergaming-97flex); [BLAST on Marketing Monk](https://www.marketingmonk.so/jobboard/jobs/video-editor-jioblast-at-blast-xzijbc)

### Inferences
- Orgs already employ editors and have exclusive platform deals; selling them a tool means procurement, SLAs and custom branding a two-person team cannot support. Better: let individual pro players and org-affiliated streamers use the creator plan; orgs come later via "agency" seats (candidate 11).
- Organisers (Nodwin/Skyesports) publish standings and highlights daily during leagues; a "tournament highlights pack" is plausible but entirely our assumption.

### Gaps
- No data on who edits S8UL/GodLike/Nodwin daily content, team sizes, or tooling budgets.
- No Skyesports 2026 BGMI event found in this search.

---

## 5. Rooter and Loco: APIs, clip features, creator programmes

### Takeaway
Rooter has pivoted to gaming commerce (Rooter Shop ~70% of FY25 revenue of ₹82 crore) and shows no public developer API or partner tooling; Loco sold a majority stake to UAE-based Redwood, laid off 36% of staff and said India is "not a priority". Neither is a platform worth integrating with for an India-first YouTube-first app.

### Cited Findings
- Rooter FY25 revenue ₹82 crore (up from ₹38 crore), ~70% from users not advertisers, Rooter Shop ~70% of revenue, targeting $90M GMV run-rate by March 2026, still loss-making — [Business Today, 28 May 2025](https://www.businesstoday.in/latest/corporate/story/rooters-gaming-push-pays-off-fy25-revenue-hits-rs-82-crore-user-spends-average-rs-24k-a-month-478152-2025-05-28); [CXOToday](https://cxotoday.com/media-coverage/rooter-expands-into-gaming-commerce-records-120-yoy-revenue-growth-in-fy25/)
- Rooter's site today: live streams, short videos/Reels, Rooter Shop, "Buy Pro", Play Games; no creator programme terms, no developer API or partner tooling mentioned — [rooter.gg](https://rooter.gg)
- Loco's AVOD model failed and it is reassessing monetisation; "no plans to cease operations" — [Storyboard18](https://www.storyboard18.com/gaming-news/locos-avod-model-fails-will-it-bounce-back-37278.htm)
- Loco laid off ~36% (40 of 110 staff) — [LatestLY](https://www.latestly.com/technology/layoff-game-streaming-platform-loco-lays-off-36-of-its-workforce-40-employees-from-total-staff-of-110-5597348.html)
- Loco sold a majority stake to UAE-based Redwood for ~$65M; says India is not a priority; Lumikai took an all-cash exit — [Storyboard18](https://www.storyboard18.com/gaming-news/loco-sells-majority-of-stake-to-uae-based-tech-company-says-india-not-a-priority-43430.htm); [BusinessWorld](https://businessworld.in/article/loco-sells-majority-stake-to-uae%E2%80%99s-redwood-for-65-mn-534602); [Lumikai](https://lumikai.com/post/lumikai-sees-an-all-cash-exit-from-loco)
- Loco launched in Brazil in January 2025 — [Señal News](https://senalnews.com/es/digital/llega-a-brasil-la-plataforma-loco-con-foco-en-la-comunidad-gamer)

### Inferences
- Rooter still hosts streams (GodLike exclusivity), so some creators record there, but with no API the only integration is "upload the recording file", which the app already supports. Rooter Shop suggests Rooter's creator relationships are commerce-led, not tooling-led.
- Loco is effectively out of India; ignore.

### Gaps
- Rooter's Google Play listing could not be read (truncated); no FY26 figures or 2026 creator-programme announcements found.
- No Rooter developer documentation found anywhere; absence is strong but not conclusive.

---

## 6. Regional-language captions and titles (Tamil, Telugu, Bengali, Marathi, Malayalam)

### Takeaway
Demand evidence is real: Tamil gaming channels reach 2.9M (PVS Gaming) and 4.1M (Gaming Tamizhan) subscribers in 2026, Telugu-only Free Fire tournaments exist, and Google says ~70% of Indian internet users prefer Indic languages. The cheapest route is IndicTrans2 (MIT-licensed, free, 22 languages) for translation, with Sarvam STT at ₹30/hour and Gemini 2.5 Flash-Lite at $0.10/M input tokens as paid fallbacks.

### Cited Findings
- PVS Gaming (Tamil, Free Fire): 2.9M YouTube subscribers as of Aug 2026 (third-party estimate) — [Qoruz](https://qoruz.com/PVSGAMING/youtube); older reports 2.22M — [Sportskeeda](https://www.sportskeeda.com/free-fire/pvs-gaming-id-number-monthly-income-free-fire-stats)
- Gaming Tamizhan (Tamil): 4.1M subscribers as of Jul 2026 — [Qoruz](https://qoruz.com/youtuber.vicky/youtube)
- Sharp Tamil Gaming 1.56M (Jul 2025); Tamil Gaming 536K (Jun 2025) — [vidIQ](https://vidiq.com/youtube-stats/channel/UCjvNWB4Zw5AeOxDKP7WM9Ng); [vidIQ](https://vidiq.com/youtube-stats/channel/UCCPWi_OwWMR5JTiujn7v-7g)
- Free Fire MAX Telugu Championship brought 48 Telugu YouTubers together — [The Reel Stars](https://www.thereelstars.com/?p=21509)
- YouTube India: Tamil, Telugu, Kannada and Bengali are the most popular after Hindi; regional gaming creators grew from <5,000 subs in 2018 to six figures — [KrASIA](https://kr-asia.com/youtube-sees-gaming-as-its-next-growth-driver-in-india); [Hans India](https://www.thehansindia.com/tech/hungry-indian-gaming-creators-arrive-on-youtubes-global-map-582283)
- Google report: ~70% of Indian internet users prefer Indic languages over English — [Entrepreneur India](https://entrepreneur.com/en-in/technology/sharechat-is-changing-how-next-billion-users-will-interact/367196)
- YouTube AI auto-dubbing covers Bengali, Hindi, Malayalam, Punjabi, Tamil, Telugu, with Kannada, Gujarati, Marathi, Assamese planned — [Deccan Herald](https://www.deccanherald.com/amp/story/technology%2Fartificial-intelligence%2Fyoutube-brings-ai-powered-auto-dubbing-language-feature-to-all-users-3888480)
- Qoruz: gaming influencers reached ~467,000 by end-2024 (213% growth 2020–22) and gaming projected to lead in 2025 — [Social Samosa](https://www.socialsamosa.com/report/gaming-influencers-set-to-rival-fashion-projected-to-reach-467k-in-2025-report-8675317); [Storyboard18](https://www.storyboard18.com/how-it-works/indias-creator-economy-sees-322-growth-surpassing-4-million-influencers-in-2024-qoruz-report-55815.htm)
- IndicTrans2: MIT-licensed checkpoints (commercial use OK), all 22 scheduled languages; NLLB is CC-BY-NC by contrast — [AIKosh](https://aikosh.indiaai.gov.in/home/models/details/indic_trans2.html); [arXiv 2305.16307](https://arxiv.org/abs/2305.16307v1); [SourcePulse](https://www.sourcepulse.org/projects/1990086)
- Sarvam API pricing (INR, 2026): Speech-to-Text ₹30/hour billed per second; STT + diarization ₹45/hour; STT + translate ₹30/hour; saaras:v3 with mode="translate" replaces the legacy translate endpoint — [Sarvam pricing](https://docs.sarvam.ai/api/pricing); [Sarvam changelog](https://docs.sarvam.ai/changelog)
- Sarvam LLM (sarvam-105b) price rose to ₹29.28 / ₹10.98 / ₹73.2 per 1M tokens (input/cached/output) effective 5 Aug 2026, from ₹4 / ₹2.5 / ₹16 — [Sarvam changelog](https://docs.sarvam.ai/changelog)
- Gemini API (USD per 1M tokens, Standard tier, page read 5 Nov 2026): gemini-2.5-flash-lite $0.10 in / $0.40 out (audio in $0.30); gemini-3.1-flash-lite $0.25 / $1.50; gemini-3.6-flash and 3.8-flash $0.75 / $3.75 through 31 Dec 2026, doubling on 1 Jan 2027; batch ~50% off; free tier tokens are free for these models; gemini-2.5-flash routes to 3.5-flash-lite from 1 Dec 2026 — [Google AI Studio pricing](https://aistudio.google.com/docs/pricing)

### Inferences
- Cost per stream: a 4-hour Hinglish stream is ~30–40k words of transcript; translating titles/captions for 10 clips is a few thousand tokens, i.e. well under ₹1 with Flash-Lite or ₹0 with IndicTrans2 on the laptop. Regional STT (if a creator speaks Tamil, not Hinglish) is the bigger cost: Sarvam ₹120 for a 4-hour stream; Whisper locally is free but weaker on Indic languages (our assumption from the Hinglish work, not sourced here).
- Tamil first, then Telugu: the largest regional gaming channels found are Tamil; a Telugu creator tournament scene exists.
- The whole pipeline (Hinglish ASR tuned on BGMI vocabulary + Indic translation) is something Opus Clip/Vizard do not tune for; this is an "only we" feature with demand evidence.

### Gaps
- No consolidated 2025–26 count of regional-language gaming channels; figures are per-channel third-party estimates.
- Sarvam realtime API price not found; Sarvam page may be cached/out of date (LLM price mismatch noted).
- Indic-script tokenisation overhead on Gemini not quantified.

---

## 7. Low-bandwidth and phone-only creators (uploading 4-hour recordings)

### Takeaway
Uploading full recordings over mobile data is the real bottleneck (India median mobile download ~40 Mbps in May 2026; uploads historically single-digit to ~15 Mbps), and the obvious shortcut, processing from the YouTube VOD, is explicitly barred by YouTube API policy even for a creator's own video. "Mark then upload only the minutes around markers" is the feasible route.

### Cited Findings
- India median mobile download speed 39.94 Mbps in May 2026 (36.78 Mbps in April); India ranked 56th — [Outlook Business, 1 Jun 2026](https://www.outlookbusiness.com/news/india-climbs-3-spots-to-56th-in-global-mobile-speed-ranking-for-may-ookla-index-news-296789)
- Jio 5G median upload 14.54 Mbps in H2 2024 (Jio 5G only) — [ThePrint](https://theprint.in/economy/jio-led-mobile-internet-market-in-key-performance-metrics-in-h2-2024-ookla/2575445/)
- Older all-India mobile averages: 12.07 Mbps down / 4.31 Mbps up (undated) — [Telecom Talk](https://telecomtalk.info/india-ranked-countries-mobile-internet-speeds/305886/)
- YouTube API Services Developer Policies III.E.1: API clients must not "download, import, backup, cache, or store copies of YouTube audiovisual content without YouTube's prior written approval"; no exception for channel owners' own videos; must not "separate, isolate, or modify the audio or video components"; scraping prohibited (III.E.6); accessing API data via other technology prohibited (III.I.14) — [YouTube API Developer Policies](https://developers.google.com/youtube/terms/developer-policies)
- YouTube Studio's new Video Clips tool lets creators clip from archived live streams inside YouTube — [Tubefilter, 17 Apr 2026](https://www.tubefilter.com/2026/04/17/youtube-clipping-tool-viewer-clips-shorts/)

### Inferences
- At 5 Mbps real-world upload, a 4-hour 1080p phone recording of ~10–15 GB takes 5–7 hours and often fails; even at 15 Mbps it is ~2 hours (our arithmetic; file sizes assumed).
- "Mark then upload": creator taps a marker during/after the stream (or the app reads the kill-feed on-device), then the phone uploads only ±2 minutes around each marker (e.g. 15 markers x 4 min = 1 hour of footage, ~3 GB, a quarter of the full file). Full-stream detection runs on the laptop only when Wi-Fi is available. Zero extra cost; it is a client-side ffmpeg trim plus resumable upload.
- The YouTube VOD route must be rejected explicitly in the product plan: using yt-dlp on a creator's own VOD with consent still violates the API developer policies and risks the app's YouTube OAuth access, which the approve-then-post feature depends on. YouTube's own Studio clipping tool is the only compliant way to clip a VOD, and it is YouTube's, not ours.
- On-device pre-trim and marker-segment upload are features no global tool emphasises because their users are on fibre; this is a genuine India differentiator with structural (not surveyed) demand.

### Gaps
- No 2026 Ookla India median mobile upload figure found (only download).
- No source on typical BGMI screen-recording bitrates/file sizes; our estimate.

---

## 8. Brand-safety and sponsor features (auto-bleep, sponsor slot tracking, media kit)

### Takeaway
Auto-bleep is useful and cheap: YouTube still restricts ads for high-frequency strong profanity and profanity in titles/thumbnails (the first-7-seconds penalty was dropped July 2025), and a 2026 guide says bleeped profanity does not affect ad suitability. The "analytics export for brand platforms" idea is weak: Qoruz already pulls creator data straight from YouTube's Creator Partnerships API, and no evidence shows Kofluence/Qoruz want creator-side exports.

### Cited Findings
- July 2025: YouTube removed the strong-profanity penalty for the first 7 seconds; gaming creators were a main beneficiary — [PPC Land](https://ppc.land/youtube-removes-strong-profanity-restrictions-from-first-7-seconds/); [Storyboard18](https://www.storyboard18.com/amp/digital/youtube-loosens-profanity-rules-allowing-swearing-in-first-7-seconds-for-monetized-videos-77887.htm)
- High-frequency strong profanity still faces restrictions; profanity in titles or thumbnails still limits ads — [Social Media Today](https://www.socialmediatoday.com/news/youtube-eases-monetization-restrictions-content-profanity/756398/); [MediaPost](https://www.mediapost.com/publications/article/407807/)
- 2026 third-party guide: bleeped profanity does not affect ad suitability; suggests bleeping heavy-swearing gaming content — [vidIQ profanity rules 2026](https://vidiq.com/ru/blog/post/youtube-profanity-update)
- Qoruz integrated YouTube's Creator Partnerships API for first-party creator data; offers language, city-tier and audience-authenticity filters — [ThePrint/ANI](https://theprint.in/ani-press-releases/qoruz-deepens-partnership-with-youtube-to-integrate-direct-creator-data-into-campaign-planning/2893765); [Outlook India](https://www.outlookindia.com/hub4business/from-niche-experiment-to-enhancing-indias-creator-economy-qoruz)
- Kofluence: app-based creator network, deep in nano/micro creators; 52% of marketers prefer micro-influencers (10K–100K) for regional campaigns; creator economy estimated at ₹3,500 Cr+ (2025 report) — [Kofluence report 2025](https://kofluence.com/inside-kofluences-influencer-marketing-research-report-2025/); [Tribune India](https://www.tribuneindia.com/news/business/indias-3-5-4-5-million-creator-economy-powers-3500-crore-influencer-marketing-industry-growth-kofluence-influencer-marketing-report-2025)
- Qoruz: ~4.06M Indian influencers in 2024, gaming ~467K — [Storyboard18](https://www.storyboard18.com/how-it-works/indias-creator-economy-sees-322-growth-surpassing-4-million-influencers-in-2024-qoruz-report-55815.htm)

### Inferences
- Auto-bleep for Hinglish gaali is an "only we" feature: global tools' profanity lists are English; a Hinglish list (Hindi/Hinglish swear words in Latin and Devanagari script, as transcribed by the ASR) is small to build and runs on the existing transcript; cost ₹0. Output a "sponsor-safe" variant alongside the raw clip.
- Sponsor slot tracking (marker type "sponsor read", calendar reminder, proof-of-delivery clip): plausible, cheap, but demand is our assumption.
- Media kit / analytics export: brand platforms already have the data via YouTube APIs and the YouTube developer policies (30-day storage limit, no derived metrics without audit) make a creator-side analytics product legally awkward. Skip.

### Gaps
- No official YouTube page for 2026 advertiser-friendly guideline changes was fetched; relying on 2025 press plus a 2026 vendor guide.
- No evidence from Kofluence/Qoruz/Plixxo/Winkl/OPA on wanting creator-side exports; Plixxo, Winkl and OPA not researched.

---

## 9. Hindi UI for the app itself

### Takeaway
Indirect but consistent evidence that Indic-language interfaces lift engagement for Bharat users (ShareChat's Oriya-only build; Google's ~70% Indic preference), and vernacular apps (Josh: 12 languages) treat language coverage as the differentiator. No source was found on creator-tool UIs specifically, and no official list confirming YouTube Studio's interface languages, so the case rests on general-market evidence and is cheap to act on.

### Cited Findings
- ShareChat built an Oriya-only interface using locally prevalent words; removing English made engagement go up (2018 reporting) — [Business Standard](https://www.business-standard.com/article/companies/messenger-app-sharechat-now-in-oriya-117111001058_1.html); [FactorDaily](https://archive.factordaily.com/?p=3423)
- Josh is available in 12 Indian languages and claims 100M+ reach; its content lead concedes the short-video apps "all look the same in terms of the interface" — [WARC](https://www.warc.com/newsandopinion/opinion/Brand_in_action_How_shortvideo_app_Josh_leverages_differentiation_and_data/6081); [Wikipedia](https://en.wikipedia.org/wiki/Josh_(app))
- Google-KPMG: Hindi internet users (201M) set to overtake English users (199M); Google: ~70% of Indian users prefer Indic languages — [MyMobile India](https://www.mymobileindia.com/do-your-thng-launches-app-in-3-more-languages-to-support-creator-market-in-india/amp/); [Entrepreneur India](https://entrepreneur.com/en-in/technology/sharechat-is-changing-how-next-billion-users-will-interact/367196)
- Creator platform Do Your Thng launched its app in three more Indian languages to support the creator market — [MyMobile India](https://www.mymobileindia.com/do-your-thng-launches-app-in-3-more-languages-to-support-creator-market-in-india/amp/)
- Third-party guide says YouTube Studio lets creators set a channel default language to Hindi, but no official Studio interface-language list was found — [Transliterate blog](https://all-blogs-8rl.pages.dev/Transliterate.Blog/guides--type-hindi-in-youtube)

### Inferences
- BGMI creators already speak Hinglish on stream; a Hinglish (Latin-script) UI copy, not pure Devanagari, is probably the better fit and avoids font/layout issues. Cost: a string table, near zero; keep English as default and A/B which the creators keep.
- No global clipping tool ships Hindi/Hinglish UI; it is a differentiator in marketing more than in function.

### Gaps
- No research on Indian creator-tool UI language preference; no data on what fraction of BGMI creators would switch a Hindi toggle on.
- YouTube Studio supported UI languages not confirmed from an official page.

---

## 10. Live-stream tie-ins (OBS overlay, Discord bot, mod commands, Super Chat-triggered markers, YouTube live chat quota)

### Takeaway
Reading live chat is feasible inside YouTube's default 10,000 units/day: both liveChatMessages.list and streamList cost 5 units per call, and streamList keeps one connection open (reconnect with the last token), so an 8-hour stream costs a handful of units rather than the ~14,400 units a 5-second REST poll would burn. OBS browser-source overlays and Discord bots are free. Demand is our assumption.

### Cited Findings
- liveChatMessages.list costs 5 quota units; clients must respect pollingIntervalMillis or get rateLimitExceeded; streamList "pushes new messages to the client as they become available" and "helps to avoid exceeding your quota" — [liveChatMessages.list](https://developers.google.com/youtube/v3/live/docs/liveChatMessages/list)
- liveChatMessages.streamList costs 5 units per call; server-streaming connection sends recent history then new messages; nextPageToken lets you resume after disconnect; maxResults 200–2000 (default 500); rate-limit errors if reconnecting too fast — [liveChatMessages.streamList](https://developers.google.com/youtube/v3/live/docs/liveChatMessages/streamList)
- Default YouTube Data API quota is 10,000 units/day (shared with Live Streaming API methods), reset at midnight Pacific — [YouTube quota cost reference](https://developers.google.com/youtube/data/determine_quota_cost)
- Third-party estimate: REST polling every 5 s is 360 calls/hour ≈ 1,800 units/hour, i.e. ~14,400 units for an 8-hour stream, exceeding the default; their worker prefers the streaming interface — [Lumio docs](https://lumio-docs-prod.pages.dev/developer-guide/youtube-api-quota)
- Telegram bots are free with ~30 msg/s bulk and 50 MB sends (for "clip saved" pings) — [Telegram Bot FAQ](https://core.telegram.org/bots/faq)

### Inferences
- Design: open one streamList connection per live stream (5 units + a few reconnects), watch for mod commands ("!clip"), Super Chat events (the streamList page does not document Super Chat fields; the list resource does include superChatDetails in the YouTube Data API, but confirm in the resource doc) and chat spikes; write a marker with the stream timestamp. An OBS browser source shows "clip saved" from a local WebSocket. Discord bot posts the same. All free.
- A chat-spike detector adds a signal for "funny moments" the HUD cannot see; combined with the existing kill detection this is unique to a tool that also owns the detection pipeline.
- Risk: the app's OAuth client is the same one used for posting Shorts; live-chat reads share that 10,000/day quota, so budget it (streamList is cheap; list polling is not).

### Gaps
- Whether streamList messages include superChatDetails was not confirmed on the streamList page.
- No evidence of demand from BGMI streamers or mods for a "!clip" command on YouTube (Twitch culture does not map 1:1).

---

## 11. Pricing packaging unique to India (UPI pay-per-stream, yearly plans, reseller/agency pricing)

### Takeaway
A ₹49-per-stream UPI price is operationally viable: Razorpay charges 2% + 18% GST (~2.36% all-in) on UPI with no setup fee, so a ₹49 charge nets ~₹47.8. Recurring UPI AutoPay works up to ₹15,000 per debit without extra authentication. Local anchors: Apple Creator Studio at ₹399/month or ₹3,999/year (Jan 2026); global clipping tools still bill in USD ($29–$49/month) with no INR pricing, which is the gap to exploit.

### Cited Findings
- Razorpay standard plan: 2% platform fee plus 18% GST, no setup/AMC; applies to UPI despite zero MDR; T+2 settlement; corporate/international cards 3% + GST; possible fee waiver for new merchants from 1 Jul 2026 (unconfirmed) — [ProductGrowth](https://productgrowth.in/numbers/payment-gateway-charges-india/); [dev.to comparison](https://dev.to/techiestark/payment-gateway-pricing-compared-high-roi-options-in-india-in-2026-39h6); [Razorpay blog](https://razorpay.com/blog/?p=27895)
- Cashfree standard fee reported at 1.95%; UPI AutoPay: ₹7.5 mandate creation plus ₹5 per presentation below ₹1,000 — [Cashfree](https://www.cashfree.com/blog/recurring-payment)
- UPI AutoPay: ₹15,000 per-debit AFA-free limit for standard subscriptions; higher tiers up to ₹1 lakh for specific categories; Razorpay Subscriptions supports mandates up to ₹1,00,000 — [Razorpay blog](https://razorpay.com/blog/payment-gateway-support-for-subscription-businesses-key-considerations-in-2026/); [PhonePe](https://business.phonepe.com/articles/how-to-accept-subscription-payments-in-india-upi-auto-pay-vs-e-nach-vs-cards); [Razorpay docs](https://razorpay.com/docs/payments/subscriptions/supported-payment-methods.md)
- Possible 0.4% MDR on UPI above ₹2,000 from 15 Oct 2026 reported by one source; another says MDR for large merchants remains a proposal as of July 2026 — [IRPR](https://irpr.agency/blog/top-upi-payment-gateways-india-comparison-2026); [Razorpay blog](https://razorpay.com/blog/?p=27317)
- Apple Creator Studio India (launched 28 Jan 2026): ₹399/month, ₹3,999/year; students ₹199/month, ₹1,999/year; one-month free trial — [Free Press Journal](https://www.freepressjournal.in/tech/apple-creator-studio-subscription-launched-in-india-final-cut-pro-logic-pro-pixelmator-pro-priced-at-399-per-month); [Telecom Talk](https://telecomtalk.info/apple-creator-studio-launched-in-india-for-rs-399-per-month/1003519/)
- Picsart India ~₹690/month monthly, ~₹590/month yearly (2026) — [Zoutons](https://zoutons.com/news/picsart-gold-plan-worth-it-indian-creators-2026)
- vidyo.ai (Indian-founded clipping tool) prices in USD only: Free, Lite $29, Essential $39, Growth $49/month (checked 13 Jun 2026); ~$16.66/month billed yearly — [CostBench](https://costbench.com/software/ai-video-editing-saas/vidyo-ai/); [Spotsaas](https://www.spotsaas.com/product/vidyo-ai/pricing)
- InVideo bills in USD with no INR list; Indian users pay FX plus GST (~₹2,100/month Plus at ~₹83/USD) — [FluxNote guide](https://fluxnote.io/guides/invideo-price-in-india)
- FluxNote (Indian tool) accepts UPI; Rise ₹999/month, Pro ₹1,699/month (May 2026; vendor's own guide, figures vary) — [FluxNote pricing guide](https://fluxnote.io/guides/fluxnote-pricing-guide)
- Rooter users who spend average ₹2,400/month on gaming commerce (FY25) — [Business Today](https://www.businesstoday.in/latest/corporate/story/rooters-gaming-push-pays-off-fy25-revenue-hits-rs-82-crore-user-spends-average-rs-24k-a-month-478152-2025-05-28)

### Inferences
- Packaging that fits the evidence: (a) pay-as-you-go ₹49–₹99 per stream via one-tap UPI (Razorpay Payment Links, no mandate needed; net ~97.6%); (b) monthly ₹399 (Apple's anchor) via UPI AutoPay; (c) yearly ₹2,999–₹3,999 paid up front (avoids mandate friction entirely); (d) an "editor/agency" plan with multi-channel seats, since Indian creators commonly hire freelance editors (assumption; editor-marketplace postings exist but no India-specific count).
- Per-stream pricing works only if the per-stream variable cost stays under ~₹10 (local models on the laptop; Sarvam/Gemini only for regional add-ons, see candidate 6). Global tools cannot match ₹49/stream because they pay cloud GPU per minute.
- Keep GST registration in mind: 18% GST on SaaS applies once turnover crosses the threshold; prices should be shown GST-inclusive (our note, not sourced here).

### Gaps
- No published Indian creator survey on willingness to pay per stream vs monthly; the ₹49 figure is our assumption anchored only on competitor price points.
- UPI MDR status after 15 Oct 2026 unresolved (sources conflict).
- No evidence on agency/reseller pricing norms for Indian creator tools.

---

## 12. Added candidates not in the brief

### Takeaway
Two further "only we" ideas surfaced: (a) a Hinglish ASR + BGMI vocabulary model is itself a moat since Sarvam prices Indic STT at ₹30/hour and nobody tunes for gaming slang; (b) YouTube's April 2026 move to kill viewer Clips and ship Studio clipping with "auto-suggestions" later in 2026 means generic AI clipping is being commoditised by YouTube itself, so India/game-specific signals (HUD, Hinglish, chat spikes, result screens) are where a small team should sit.

### Cited Findings
- YouTube is discontinuing viewer Clips; Studio "Video Clips" republishes clips from videos and archived live streams; "auto-suggestions" of clippable moments and Video Clips for Shorts slated for later in 2026; YouTube says third-party clipping tools will fill the viewer-clip gap — [Tubefilter, 17 Apr 2026](https://www.tubefilter.com/2026/04/17/youtube-clipping-tool-viewer-clips-shorts/)
- Sarvam STT ₹30/hour (2026) — [Sarvam pricing](https://docs.sarvam.ai/api/pricing)
- Scrymz imports WhatsApp registrations for scrims, showing WhatsApp is already the workflow surface in grassroots BGMI esports — [Scrymz on Product Hunt](https://www.producthunt.com/p/scrymz-ai-points-table-maker/scrymz)

### Inferences
- Scrim-community tie-in: grassroots scrim organisers run on WhatsApp and screenshots; a lightweight "scrim recap" (candidate 2 cards for a whole lobby, from the creator's own result screen) could ride that behaviour. Demand assumed.
- Prioritise, in order: 7 (marker-segment upload), 6 (regional captions), 2 (recap cards), 8 (Hinglish auto-bleep), 9 (Hinglish UI), 11 (UPI per-stream), 1 (Telegram bot then WhatsApp), 10 (live chat markers). Drop 5; park 3 and 4.

### Gaps
- No primary data from BGMI creators themselves (interviews/surveys) exists in any of the above; every demand signal is either market-level or inferred from adjacent products.
