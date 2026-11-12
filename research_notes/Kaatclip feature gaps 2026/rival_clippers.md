# Rival AI clippers: new features and launches, late 2025 to November 2026, vs Kaatclip

Scope note: research done 12 Nov 2026 with ~15 search/fetch calls. Items already in `reports/Competitor feature audit and creator gaps.md` (5 Nov 2026) and `reports/AI clipper autoposting and multigame gaps.md` (4 Nov 2026) are not repeated unless they changed. eklipse.gg pages still return HTTP 403 from this network (same as the 5 Nov audit), so Eklipse rows lean on third-party pages. Many findings come from vendor or competitor-written pages; these are flagged. Status key: **HAS** = Kaatclip has it, **PARTLY**, **MISSING**. "Value to gaming streamers": High / Medium / Low, with the basis stated.

## What did the main rivals launch or change in 2025-2026?

### Takeaway
The biggest 2026 moves are (1) OpusClip 4.0 (2 Nov 2026) shifting from "clipper" to "auto-editor" with reusable edit "Recipes", hook templates, motion graphics and an AI Producer that runs inside ChatGPT/Claude; (2) Twitch going native on clipping (Auto Clips, "Twitch Clip That", automatic clip captions, clip recaps, Dual Format vertical+horizontal streaming), which raises the free baseline on Twitch but does not touch YouTube or BGMI; and (3) Submagic adding direct publishing + analytics, B-Rolls 2.0 and an MCP server. None of these adds mobile-game detection or Hinglish.

### Cited Findings

**OpusClip**
- OpusClip 4.0 announced 2 Nov 2026 (page metadata: published 1 Nov, modified 3 Nov). Features: "Auto-edit" ("Drop in raw footage or paste a link, then switch on speech cleanup, captions, B-roll and more"); "Every format" (one edit into 60–90 s highlights, 3–5 min extended cuts, or a lo-fi update); "Recipes" ("Save your setup as a Recipe, or start from one of ours"); "Viral Hook" (hook style from a template library applied to the first seconds); "Motion Graphics" (speech turned into animated icons, numbers, charts); "AI Producer" plugin in ChatGPT or Claude ("Show it a style you like and it edits your footage to match"). No gaming-specific feature, no new posting, collaboration, API or analytics item in the 4.0 post. Mentions a "Free Forever Plan" that lets you create and post one short a day. — [OpusClip blog: OpusClip 4.0](https://www.opus.pro/blog/opusclip-4-0)
  - Kaatclip: Recipes/saved edit presets **PARTLY** (brand kit + layouts, but no saved per-clip "recipe" of settings); Viral Hook templates **PARTLY** (hook title text with emoji exists; no template library of hook styles); Motion graphics **MISSING**; extended 3–5 min cut from same edit **PARTLY** (weekly compilation only); AI Producer/LLM plugin **MISSING**. Value: Medium for hook templates/presets (Indian creators judge output on "viral" style, per 5 Nov audit); Low for motion graphics (talking-head feature) and LLM plugin.
- Other 2026 OpusClip items from secondary aggregators (not verified against OpusClip release notes): 4K export for Pro (20 May 2026); "Duplicate Clips" to edit one copy without touching another (20 May 2026); new import sources incl. Zoom, Apple Podcasts and **Medal.tv** (22 May 2026) — [toolcolumn changelog](https://www.toolcolumn.com/tools/opusclip/changelog). AI video upscaling added to Starter/Pro/Business (week 26, June 2026) — [PricingSaaS diff](https://pricingsaas.com/companies/opus/diffs/2026W26). AI Producer, auto sound effects, retake detection, brand-aware editing, OpusSearch (finds moments across large archives), Agent Opus (Aug 2026 profile) — [YesPress profile](https://yespress.io/opusclip.md). AI dubbing for cross-language repurposing (low confidence, page last updated March) — [aitoolsatlas changelog](https://aitoolsatlas.ai/tools/opusclip/changelog).
  - Kaatclip: Duplicate clip/variants **MISSING** (value Medium: lets a creator make a Shorts cut and a sponsor-safe or alternate-hook cut; Kaatclip's sponsor-safe copy is a partial version); AI upscaling **MISSING** (Low–Medium: OBS PC recordings are already 1080p); auto sound effects **HAS** (SFX in editor; whether auto-placed is unclear); archive search across past streams ("find every 1v4 from last month") **MISSING** (Medium: feeds compilations/series); dubbing **MISSING** (known, Low for Hinglish audiences).
- OpusClip pricing 2026: Free 60 credits/month, watermark, clips expire after 3 days, no editor; Starter $15/mo; Pro $29/mo or $174/yr — [Two Average Gamers, 23 Apr 2026](https://www.twoaveragegamers.com/best-ai-clip-detection-tools-for-streamers-2026/); [BlitzCut, 9 Oct 2026 upd. 3 Nov](https://blitzcutai.com/blog/best-ai-clipping-tools). Credits: Starter 150, Pro 300/month, expire after 60 days; "running out of credits" is the most common complaint (competitor-written) — [BlitzCut](https://blitzcutai.com/blog/best-ai-clipping-tools).

**Twitch (platform-native; new since the 5 Nov audit only in detail)**
- TwitchCon Rotterdam, 30 May 2026: "Auto Clips automatically generates captioned clips from the best moments from your stream", using chat activity, vocal inflection and on-screen events; waitlist open, beta "in the coming months"; Twitch says 85% of Auto Clips streamers have a clip after a stream vs 50% overall. "Twitch Clip That" voice phrase makes a clip. **Automatic captions on community clips** from early June 2026, creator-editable text/timing/style; auto-crop and trim "being explored". **Clip recaps**: from June a sorted list of the stream's best clips sits at the top of the Stream Summary (also emailed at stream end) for one-tap sharing to Twitch Stories. **Dual Format**: stream horizontal and vertical at once, beta, rolling out June 2026. No posting to YouTube/TikTok mentioned. — [Twitch blog](https://blog.twitch.com/en/2026/05/30/everything-we-announced-at-twitchcon-rotterdam-2026/)
- Auto Clips reportedly English-only and Partners/Affiliates first (secondary) — [Badge Base](https://badgebase.de/blog/twitch-auto-clips/). Vertical version auto-generated for clips, vertical default in redesigned mobile clips feed (secondary, unconfirmed by Twitch) — [Gaming Careers newsletter](https://gaming-careers.pages.dev/newsletters/everything-twitch-just-announced-at-twitchcon-rotterdam/); [Tubefilter](https://www.tubefilter.com/2026/06/01/twitch-twitchcon-europe-rotterdamn-vertical-horizontal-dual-format-stream/amp/).
  - Kaatclip: end-of-stream emailed/pushed "best clips recap" **PARTLY** (Telegram notifications exist; a ranked recap message with one-tap approve is the gap if not already sent). Voice "clip that" **MISSING** (Kaatclip has button + `!clip`; the 5 Nov audit already noted Eklipse voice markers). Vertical source capture (dual-format/vertical OBS canvas as input) **MISSING** (Medium: Reddit streamers already keep a vertical replay buffer, per 5 Nov audit). No Kick-native clip feature found.

**Submagic**
- Changelog: "Automatically edit your videos in 1 click" (12 Jan 2026); "Publish your content directly from Submagic" (4 Mar 2026); "B-Rolls 2.0 is live" (9 Apr 2026); "Submagic MCP Server is live" (6 May 2026; uses existing API key); "New: Publish + Analytics, one video, every platform" (8 Jun 2026); "Add branded Intros & Outros to every video" (23 Dec 2025). No gaming, Hindi or team entries visible. — [Submagic changelog](https://submagic.canny.io/changelog)
- AI B-roll "powered by Sora 2" matched to script (vendor marketing via search summary) — [Submagic auto video editor](https://www.submagic.co/hu/features/auto-video-editor).
  - Kaatclip: publish **HAS** (YouTube only); per-post analytics **HAS/PARTLY** (channel stats by Shorts/live/videos; per-clip performance unclear); intros/outros **HAS**; B-roll **MISSING** (Low for gameplay: B-roll replaces the action viewers came for; generative B-roll may also trip YouTube's altered/synthetic disclosure); API/MCP **MISSING** (Low for creators, relevant only for agencies).

**Vizard, Klap**
- Vizard pages list AI B-roll matching, dynamic subtitles and custom brand templates; no dated changelog found — [Vizard: add B-roll](https://vizard.ai/tools/add-b-roll-to-video). Free 60 credits/month; Creator from 600 credits/month; Trustpilot 4.7 from ~2,500 reviews (second-hand via Castmagic) — [BlitzCut](https://blitzcutai.com/blog/best-ai-clipping-tools).
- Klap prices rechecked Nov 2026: Basic $14/mo (100 clips), Pro $39 (300), Pro+ $94 (1,000), billed yearly; one free video, no card; G2 4.8 (2 reviews), Trustpilot 3.7 (59 reviews) with ~30% one-star, several about billing/cancellation — [BlitzCut](https://blitzcutai.com/blog/best-ai-clipping-tools).

**StreamLadder**
- No 2026 StreamLadder announcement found by search. A 23 Apr 2026 review lists Free (manual editor, no watermark, 720p, 200 MB upload cap), Silver $9/mo, Gold $27/mo with "ClipGPT" (audio + chat-engagement detection), generated titles and hashtags, a **performance prediction score**, dual-cam layouts, **chat overlay import**, scheduled posting; Gold has credit quotas and per-stream clip caps — [Two Average Gamers](https://www.twoaveragegamers.com/best-ai-clip-detection-tools-for-streamers-2026/). **Conflict:** the 5 Nov audit read StreamLadder's live India page as Starter ₹1,455 / Creator ₹2,619 / Pro ₹3,783, so the Silver/Gold names are either outdated or wrong.
- "StreamLadder Just Priced Out Normal Streamers" Reddit thread reported second-hand by a competitor; not verified — [Eklipse: StreamLadder alternatives](https://eklipse.gg/compare/streamladder-alternatives/) (403 from here; via search summary).
  - Kaatclip: chat overlay burned into the clip **MISSING** (Medium: chat reactions are part of stream-clip style on Twitch; YouTube live chat could be captured live via the existing `!clip` listener). Performance prediction score **MISSING** (both earlier reports recommend skipping generic virality scores; still Low).

**Streamlabs (Ultra, Cross Clip, AI Game Highlighter)**
- No 2026 Streamlabs announcement found. AI Game Highlighter is a free beta in Streamlabs Desktop; 2025 game additions: Apex, BO6, CS2, LoL, Marvel Rivals, Overwatch; support guide says "platform integrations (like TikTok) on the horizon" — [Streamlabs support](https://support.streamlabs.com/hc/en-us/articles/39938192759451-Introducing-Streamlabs-AI-Game-Highlighter-An-Easy-Way-to-Capture-Your-Best-Gaming-Moments). Ultra page lists Cross Clip watermark removal and 1080p60 export; price "from $15.75/mo" (may be dated) — [Streamlabs Ultra](https://streamlabs.com/ultra). Still no mobile game listed.
- Podcast Editor: nothing new found.

**Medal**
- No dated 2026 AI launch found from Medal. Third-party comparisons say Medal posts to its own feed and Discord, with no direct TikTok/Shorts/Reels posting — [AutoClip vs Medal (vendor)](https://autoclip.dev/compare/autoclip-vs-medal). Medal "sessions" lets friends play, talk and "clip moments from every perspective in real time" (undated) — [GamesBeat](https://gamesbeat.com/?p=205846). OpusClip added Medal.tv as an import source (May 2026) — [toolcolumn](https://www.toolcolumn.com/tools/opusclip/changelog).
  - Kaatclip: multi-POV squad clipping **MISSING** (5 Nov audit parked it; still Low–Medium for BGMI squads). Discord sharing **MISSING** (Telegram instead; Medium for PC streamers whose communities live on Discord).

**CapCut, Captions, Clipchamp**
- CapCut keeps Auto Reframe (subject tracker) and a "Long video to shorts" one-click tool plus an "AutoCut agent"; sources are CapCut's own pages and dates are unclear — [CapCut auto reframe](https://www.capcut.com/create/capcut-auto-reframing-16-9-to-9-16-video); [Lindsey Gamble](https://www.lindseygamble.com/blog/capcut-launches-long-video-to-shorts-tool-to-turn-long-form-horizontal-videos-into-short-form-videos). CapCut is free and is what Indian BGMI tutorial channels teach (5 Nov audit), so it is the real "free baseline" for editing.
- No 2026 Captions-app or Clipchamp feature news was found in this pass.

### Inferences
- The market is moving from "find clips" to "finish the edit": OpusClip 4.0, Submagic Auto Edit and Twitch's auto-captions all aim to deliver a post-ready clip with no editing. Kaatclip already does this for gameplay; the visible gap is *style variety* (hook template library, saved recipes, duplicates/variants), not detection.
- Twitch's native clipping makes free AI clips the default for Twitch streamers in English, which pushes paid gaming clippers (Eklipse, StreamLadder) toward YouTube and multi-platform. That increases competition on Kaatclip's YouTube turf, but none of them reads mobile-game HUDs.

### Gaps
- OpusClip 4.0 pricing changes and whether "Free Forever" posting includes YouTube were not stated in the post.
- StreamLadder's current plan names/prices conflict between sources; its own site was not re-read.
- No primary 2026 release notes found for Medal, Streamlabs, Captions, Clipchamp or Klap.

## Which feature categories are new since the earlier audits?

### Takeaway
New or newly widespread categories: reusable edit "recipes" and hook-template libraries, LLM/agent integrations (MCP server, ChatGPT/Claude plugins), generative B-roll, motion graphics, clip duplicates/variants, archive-wide moment search, platform-native auto clips with end-of-stream recap, and dual-format (vertical) streaming. Several categories the brief asked about (Discord bots, team approval links, auto-thumbnail A/B) showed no new 2026 rival launches in this pass.

### Cited Findings
| Category | Who, when | Kaatclip | Value to gaming streamers |
|---|---|---|---|
| Saved edit presets ("Recipes") | OpusClip 4.0, 2 Nov 2026 — [OpusClip](https://www.opus.pro/blog/opusclip-4-0) | PARTLY (brand kit) | Medium: speeds daily review |
| Hook-template library for first seconds | OpusClip "Viral Hook", Nov 2026 — [OpusClip](https://www.opus.pro/blog/opusclip-4-0) | PARTLY (one hook style) | Medium–High in India (style-driven scene, 5 Nov audit) |
| AI agent / LLM plugin / MCP | OpusClip AI Producer (Nov 2026); Submagic MCP (6 May 2026) — [OpusClip](https://www.opus.pro/blog/opusclip-4-0); [Submagic](https://submagic.canny.io/changelog) | MISSING | Low (power users/agencies) |
| Generative / stock B-roll | Submagic B-Rolls 2.0 (9 Apr 2026), Sora-2 B-roll; OpusClip Auto-edit; Vizard — [Submagic](https://submagic.canny.io/changelog); [Vizard](https://vizard.ai/tools/add-b-roll-to-video) | MISSING | Low for gameplay |
| Motion graphics from speech | OpusClip 4.0 — [OpusClip](https://www.opus.pro/blog/opusclip-4-0) | MISSING | Low |
| Multi-length outputs from one edit | OpusClip "Every format" — [OpusClip](https://www.opus.pro/blog/opusclip-4-0) | PARTLY (length presets? compilation) | Medium |
| Clip duplicates/variants | OpusClip, 20 May 2026 (secondary) — [toolcolumn](https://www.toolcolumn.com/tools/opusclip/changelog) | PARTLY (sponsor-safe copy) | Medium |
| Archive-wide moment search | OpusSearch (secondary, Aug 2026) — [YesPress](https://yespress.io/opusclip.md) | MISSING | Medium (series, compilations) |
| Publish + per-post analytics in one tool | Submagic, 8 Jun 2026 — [Submagic](https://submagic.canny.io/changelog) | HAS for YouTube | Already table stakes |
| AI upscaling | OpusClip, Jun 2026 (secondary) — [PricingSaaS](https://pricingsaas.com/companies/opus/diffs/2026W26) | MISSING | Low |
| Native auto clips + end-of-stream recap + auto clip captions | Twitch, 30 May 2026 — [Twitch blog](https://blog.twitch.com/en/2026/05/30/everything-we-announced-at-twitchcon-rotterdam-2026/) | PARTLY (Telegram notify) | High on Twitch; irrelevant to YouTube-only BGMI creators except as expectation-setter |
| Dual-format vertical streaming | Twitch, June 2026 beta — [Twitch blog](https://blog.twitch.com/en/2026/05/30/everything-we-announced-at-twitchcon-rotterdam-2026/) | MISSING (no vertical-canvas input) | Medium |
| Clip "score" (virality/prediction/intensity) | OpusClip, StreamLadder, Eklipse, NexusClips — [Two Average Gamers](https://www.twoaveragegamers.com/best-ai-clip-detection-tools-for-streamers-2026/) | HAS (ranked clips; no exposed score) | Low as a number; earlier reports say users mistrust it |
| Chat overlay in clip | StreamLadder — [Two Average Gamers](https://www.twoaveragegamers.com/best-ai-clip-detection-tools-for-streamers-2026/) | MISSING | Medium |
| AI dubbing | OpusClip (low confidence) — [aitoolsatlas](https://aitoolsatlas.ai/tools/opusclip/changelog) | MISSING | Low (known) |

### Inferences
- The cheapest high-value adds for Kaatclip from this list are a small hook-template library + saved "recipe" presets, clip duplicates (alt hook/length), and a ranked end-of-stream recap message with approve buttons in Telegram. All reuse existing pieces.
- B-roll, motion graphics and dubbing are talking-head features; gaming reviewers do not ask for them, so they stay Low.

### Gaps
- No 2026 launches found for: Discord clip bots from major clippers, client/collaborator approval links (beyond those in the 5 Nov audit), thumbnail A/B tests inside clippers (YouTube's own "Test & Compare" exists but was not re-checked here), or public APIs from gaming clippers.

## Which rivals target gaming streamers or India, at what prices?

### Takeaway
Gaming-focused pricing sits at $5–27/month (Sizzle $4.99, StreamLadder ~$9–27 or ₹1,455–3,783, Eklipse $19.99–24.99), with OpusClip $15–29 as the general benchmark. New India/Hinglish entrants are tiny and USD- or one-time-priced; none is game-aware.

### Cited Findings
- Eklipse: Premium $19.99/mo with a free tier (15 clips/stream, 720p, watermark) as of April 2026; OCR game detection "1,000+ titles"; "Clip it!" voice marker; moment intensity score; ~80% accuracy per community reports; misses moments with no scoreboard/kill event — [Two Average Gamers, Apr 2026](https://www.twoaveragegamers.com/best-ai-clip-detection-tools-for-streamers-2026/). The 5 Nov audit found the free tier ended June 2026 and Premium at $24.99 (search summaries); the April review predates that, so not a contradiction, but neither is first-hand.
- Eklipse also markets an "AI edit" feature page ("The AI gaming video editor that finishes the clip for you") and claims a 4.2/5 Trustpilot rating from 900+ reviews (vendor claim; conflicts with the 2.3 Android rating and low-star Trustpilot pages in the 5 Nov audit) — [Eklipse AI edit (search result)](https://eklipse.gg/features/ai-edit); [Eklipse blog](https://blog.eklipse.gg/featured/eklipse-gg-review.html).
- Sizzle.gg: free (unlimited streams, 1080p, watermark), Starter $4.99/mo; video+audio+chat; ~40 games; processing up to 4 hours — [Two Average Gamers](https://www.twoaveragegamers.com/best-ai-clip-detection-tools-for-streamers-2026/).
- NexusClips (new 2026 entrant): free tier with watermark, ~$15–20/mo; hybrid audio+visual detection; Twitch and YouTube; gaming templates; scheduled posting; smaller game library — [Two Average Gamers](https://www.twoaveragegamers.com/best-ai-clip-detection-tools-for-streamers-2026/).
- BlitzReels (new): Starter $29/mo billed yearly, 15 AI credits, 30 exports; scheduling and mobile app "coming soon" — [BlitzCut](https://blitzcutai.com/blog/best-ai-clipping-tools) (author's own product).
- India/Hinglish: **Zoupyu**, a Hinglish Shorts generator listed 29 Jun 2026, one-time from $5.26, pitched on code-switched speech — [PeerPush](https://peerpush.com/p/zoupyu). **Clipify AI** claims Hindi/Tamil for Shorts and Reels, no price — [Product Hunt](https://www.producthunt.com/products/clipify-ai). **SnippetPro** lifetime deal ₹1,499 / $19, Hindi support not stated — [Product Hunt](https://www.producthunt.com/p/snippetpro/snippetpro). Simplified (Mumbai) launched "AI Clips" (date/pricing not in snippet) — [IndianTelevision](https://indiantelevision.com/news-headline/simplified-launches-revolutionary-ai-clips-tool-for-effortless-video-content-creation/). None mention gaming or BGMI.

### Inferences
- Hinglish clipping is getting crowded at the low end (Reap, Bol Studio, Zoupyu, Clipify), confirming the 5 Nov conclusion that Hinglish alone is not a moat; Hinglish + BGMI HUD still is.
- Sizzle at $4.99 and OpusClip's "post one short a day free" set a low price anchor; Kaatclip's ₹499 Starter (~$5.7) lines up with Sizzle, below everything else.

### Gaps
- No INR pricing found for any gaming clipper other than StreamLadder (from the earlier audit). Zoupyu and Clipify claims not verified on their own sites.

## What do users complain about in rivals?

### Takeaway
Complaints in 2026 sources repeat the earlier pattern (late cuts, missed build-up, audio-only detection, slow processing) and add two money themes: credit exhaustion/expiry (OpusClip, Vizard, BlitzReels) and billing/cancellation trouble (Klap ~30% one-star on Trustpilot). Direct Reddit text was not reachable; most complaint data here is second-hand.

### Cited Findings
- OpusClip: cuts late and skips gameplay action; Virality Score unreliable; free tier limited — [Two Average Gamers](https://www.twoaveragegamers.com/best-ai-clip-detection-tools-for-streamers-2026/). Credits run out; monthly credits expire after 60 days — [BlitzCut](https://blitzcutai.com/blog/best-ai-clipping-tools). Frequent TikTok connection drops and silent posting failures (search summary) — [Eklipse vs OpusClip, Two Average Gamers](https://www.twoaveragegamers.com/eklipse-vs-opusclip-head-to-head-for-gaming-streamers-2026/).
- Eklipse: cluttered interface; processing sometimes takes hours; "captures the final kill but misses the buildup"; captions inconsistent for non-English content (search summaries of review pages) — [Two Average Gamers Eklipse review](https://www.twoaveragegamers.com/eklipse-review-2026-hands-on-testing-for-streamers/); [Two Average Gamers](https://www.twoaveragegamers.com/best-ai-clip-detection-tools-for-streamers-2026/).
- Klap: Trustpilot 3.7/5 (59), ~30% one-star, billing and cancellation complaints — [BlitzCut](https://blitzcutai.com/blog/best-ai-clipping-tools).
- Vizard: unused credits forfeited on cancel — [BlitzCut](https://blitzcutai.com/blog/best-ai-clipping-tools).
- StreamLadder: pricing backlash ("priced out normal streamers"), AI limited on free plan, 200 MB free cap, clip caps per stream — [Two Average Gamers](https://www.twoaveragegamers.com/best-ai-clip-detection-tools-for-streamers-2026/); [Eklipse alternatives page (via search)](https://eklipse.gg/compare/streamladder-alternatives/).
- Sizzle: up to 4-hour processing — [Two Average Gamers](https://www.twoaveragegamers.com/best-ai-clip-detection-tools-for-streamers-2026/).

### Inferences
- "Non-English captions inconsistent" (Eklipse) and "misses the buildup" (Eklipse, OpusClip) are both things Kaatclip already targets (Hinglish/Devanagari captions; markers + fight-aware cuts). Worth stating in marketing.
- Credit expiry and cancellation pain suggest Kaatclip should keep hours-based plans with no expiring credits and one-tap cancel (or per-stream UPI), and say so on the pricing page.
- Processing time is a repeated pain (hours on Eklipse/Sizzle); a "clips ready in X min after stream ends" promise backed by upload-while-streaming is a measurable advantage Kaatclip already has the plumbing for.

### Gaps
- Reddit (r/streaming, r/Twitch, r/NewTubers), G2 and Trustpilot pages were not read first-hand in this pass; complaints above come from review blogs, several written by competing vendors (BlitzCut, Eklipse). Treat as directional.
- No 2026 Product Hunt reviews of OpusClip 4.0 or Submagic Publish found.
