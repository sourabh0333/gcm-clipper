# Gaming-specific AI highlight / clipping tools: competitor landscape (as of Oct 2026)

Research date: 2026-10-26. Method: web search plus direct page fetches. Several eklipse.gg pages returned HTTP 403 to the fetcher, so some Eklipse facts come from search-result summaries of Eklipse's own pages (marked "via search summary"). Many "comparison" and "alternatives" pages are written by competing vendors (Eklipse, FragCut, Medal, Insights.gg, AutoStreamPro). Treat them as marketing, not independent evidence.

## Q1. What each tool does, how it detects moments, games, mobile support, pricing, scale, weaknesses

### Takeaway
The category splits three ways. (a) PC capture clients detect events while you play: Medal, Outplayed/Overwolf, NVIDIA Highlights, SteelSeries Moments. (b) Cloud post-stream VOD clippers such as Eklipse, Sizzle, FragCut and StreamClipping AI. (c) Platform-native features: Streamlabs AI Highlighter and Twitch Auto Clips. Almost all are built around PC games and Twitch/YouTube/Kick VODs. Game-specific detection reads on-screen events (kill feed, round results) or uses game event APIs; anything else falls back to audio, chat and transcript spikes. Independent reviews agree that accuracy is mediocre, roughly 4 good clips in 10 by one user's count.

### Cited Findings

**Eklipse (eklipse.gg): the most direct cloud competitor**
- Connects to Twitch, Kick or YouTube, finds best moments and returns vertical clips reframed for TikTok, Reels and Shorts. — [Eklipse homepage (via search summary)](https://eklipse.gg/)
- Detection: says it reads kills and round results from frame graphics and on-screen markers. — [Eklipse blog: AI clip maker for gaming (via search summary)](https://blog.eklipse.gg/tools/ai-clip-maker-gaming.html)
- Claims coverage of "3,000+ games" (vendor claim). A third-party review says its tests used Valorant, Fortnite and Apex Legends. — [Eklipse AI Highlights (via search summary)](https://eklipse.gg/features/ai-highlights/); [agent-finder.co review](https://agent-finder.co/reviews/eklipse)
- Pricing (vendor): fully paid since June 2026. About US$14.99/mo billed annually (US$179.99/yr) or US$24.99 month to month. Monthly billing through the mobile app is reportedly US$27.99. — [Eklipse homepage/schema (via search summary)](https://eklipse.gg/)
- Conflicting third-party data: "free tier and paid plans start at $9.99/month (as of July 2026)". This is likely stale. — [agent-finder.co review](https://agent-finder.co/reviews/eklipse)
- Has an Android app, "Eklipse: AI Gaming Clip Maker". The fetcher could not read its listing details. — [Google Play](https://play.google.com/store/apps/details?id=com.eklip.se)
- Independent weaknesses: one Trustpilot reviewer put the hit rate at about 4 in 10 good clips, saying it tracks volume spikes, grabs banter and misses quiet gameplay. Another said it could not detect kills in a milsim game with little on-screen info. Others report output quality worse than the source on a paid plan, processing failures and slow service, and "poor or random clips that need manual fixes". — [Trustpilot AU](https://au.trustpilot.com/review/eklipse.gg); [Trustpilot UK p3](https://uk.trustpilot.com/review/eklipse.gg?page=3); [Trustpilot NZ p3](https://nz.trustpilot.com/review/eklipse.gg?page=3)
- A Product Hunt reviewer said most recommended clips were poor and complained about free-tier and processing limits. — [Product Hunt: Eklipse.gg](https://www.producthunt.com/products/eklipse-gg)
- Positive: reviewers say it saves hours of VOD scrubbing and surfaces moments they would have missed. — [Trustpilot AU](https://au.trustpilot.com/review/eklipse.gg)

**Medal.tv: the largest consumer clipping platform**
- A PC capture client that "uses AI to capture possible moments in the background". The CEO said in 2021 that the company had moved away from ML for capturing game video. — [GamesBeat, 14 Dec 2021, updated 18 Jun 2025](https://gamesbeat.com/medal-tv-raises-60m-as-creators-clip-2m-game-moments-a-day/)
- Scale (2021): nearly 1M DAU across PC, mobile and console, and more than 2M clips per day. — [GamesBeat](https://gamesbeat.com/medal-tv-raises-60m-as-creators-clip-2m-game-moments-a-day/)
- Funding: US$60M in 2021 (a US$45M round led by OMERS Ventures plus an earlier US$15M round), US$70M raised to that date. Then US$13M at a US$333M post-money valuation on 11 Jul 2024 (Horizons Ventures, OMERS, peak6, Arcadia), alongside the launch of "Highlight", a general Windows/Mac AI-assistant platform. Medal then reported over 1M DAU and 4M+ monthly users. — [PR Newswire, 11 Jul 2024](https://www.prnewswire.com/news-releases/medal-unveils-highlight---a-revolutionary-ai-assistant-platform-raises-13m-at-333m-valuation-302194826.html)
- Estimated revenue about US$18.2M ARR in 2025. This is a third-party estimate, not reported. — [GetLatka](https://getlatka.com/companies/medal.tv)
- Total funding is estimated at about US$89.3M over 8 rounds. PitchBook lists a Series E dated 11 Sep 2025 with no amount disclosed. — [Tracxn](https://tracxn.com/d/companies/medal/__oATa7VF_pJEfa3bm1kfKx8lEcDUBnnihrOHjNoYRMXg); [PitchBook](https://pitchbook.com/profiles/company/265525-39)
- Mobile: Medal reaches mobile through its acquisition of Megacool (a mobile SDK). I found no evidence of BGMI or PUBG Mobile auto-highlight detection. — [Medal funding summary (via search)](https://startupintros.com/orgs/medal)

**Outplayed (Overwolf)**
- A desktop app with capture modes Highlights (auto-detects game events and creates clips), Full Match, Full Session and Manual. — [Overwolf Support: How to use Outplayed](https://support.overwolf.com/support/solutions/articles/9000284659-how-to-use-outplayed)
- Claims to support 5,000+ games; an older listing says 600+. Unlisted games can be enabled manually or screen-recorded. — [Outplayed on Overwolf](https://game.overwolf.com/outplayed-2025/); [Overwolf quick set-up](https://support.overwolf.com/support/solutions/articles/9000284663-outplayed-quick-set-up-guide)
- "This app is made for Desktop gaming only." No mobile support. — [Overwolf app listing](https://www.overwolf.com/app/overwolf-outplayed)
- Competitors attack it for needing Overwolf and for showing ads (competitor claim). — [Medal vs Outplayed](https://medal.tv/compare/medal-vs-outplayed); [Insights.gg vs Outplayed](https://insights.gg/blog/insights-vs-outplayed)

**Streamlabs AI Game Highlighter (Logitech)**
- Announced Sep 2024 by Logitech G and Streamlabs. It launched with Fortnite only and was described as a beta: enable it from the Highlighter tab or at Go Live with Fortnite selected, and it records the stream and compiles clips. — [Business Wire, 17 Sep 2024](https://www.businesswire.com/news/home/20240917543459/en); [Streamlabs support](https://support.streamlabs.com/hc/en-us/articles/39938192759451-Introducing-Streamlabs-AI-Game-Highlighter-An-Easy-Way-to-Capture-Your-Best-Gaming-Moments)
- The current Highlighter page lists free ML-powered highlighting for Fortnite, Apex Legends, League of Legends, VALORANT and others, "continuing to expand". No mobile titles appear. — [streamlabs.com/highlighter (via search summary)](https://streamlabs.com/highlighter)

**NVIDIA Highlights (ShadowPlay / NVIDIA App)**
- Game-integrated: the developer implements the Highlights SDK, which fires events such as multi-kills, and clips are saved automatically. Launch titles were PUBG (PC) and LawBreakers. — [NVIDIA dev blog: UE4 Highlights plugin](https://developer.nvidia.com/blog/implementing-nvidia-highlights-plugin-unreal-engine-4); [TechRadar](https://www.techradar.com/news/nvidia-shadowplay-highlights-shares-your-badass-gaming-moments)
- Still listed as a feature of the NVIDIA App ("automatically captures key moments, clutch kills"). I found no discontinuation notice. PC and GeForce only. — [Tech Advisor guide](https://www.techadvisor.com/article/730541/how-to-use-nvidia-shadowplay-highlights.html); [NVIDIA supported games FAQ](https://nvidia.custhelp.com/app/answers/detail/a_id/3324/~/what-games-does-shadowplay-support)

**SteelSeries Moments**
- Windows 10 (RS5+) capture app with AI auto-clipping on supported titles (recent additions are Street Fighter 6 and CoD: Black Ops 7), or clipping by hotkey. Shares to YouTube, Discord, Reddit and X. PC only; pricing was not shown. — [SteelSeries Moments](https://steelseries.com/gg/moments)

**Twitch native: Clips, "Clip That" voice command, and Auto Clips (alpha)**
- Auto Clips and Stream Summaries were announced at TwitchCon Rotterdam 2026. They build highlights from "chat activity, voice tone, and on-screen events". The alpha is "English-only, apply to join". — [streamer.guide](https://streamer.guide/blog/twitchcon-rotterdam-2026-new-features-1440p-clips-guilds)
- A creator reported alpha access in March 2026: the tool "identifies the best part of a stream then automatically creates and publishes clips with captions". — [Threads @zachbussey](https://www.threads.com/@zachbussey/post/DV41DSEFiCF)
- Conflict: a June 2026 blog says the features are "live on the platform now". Rollout status is unclear. — [StreamChat AI blog](https://streamchatai.com/blog/twitchs-new-ai-stream-summaries-and-auto-clips-what-they-actually-mean-for-your-channel)
- Limitation: auto clips stay on Twitch, so a YouTube audience gets nothing from Twitch-originated sessions. — [StreamChat AI blog](https://streamchatai.com/blog/twitchs-new-ai-stream-summaries-and-auto-clips-what-they-actually-mean-for-your-channel)

**YouTube Live**
- I found no evidence of a native feature that auto-generates highlight Shorts from live streams. Search results returned only third-party tools. See Gaps.

**Sizzle.gg**
- Creates highlights from Twitch/YouTube streams or uploaded gameplay. Users can filter by kills, knockdowns, headshots and victories. Offers vertical download, mashups and boundary editing. A "Universal AI" covers non-supported games (a testimonial mentions Farlight 84 and Among Us). No published game list, detection details or pricing; the site is undated. — [sizzle.gg](https://www.sizzle.gg/home)
- Earlier reports: a US$5M seed and exit from beta (undated article). The free tier carries a watermark and a paid "Starter" plan removes it (per Eklipse, a competitor). — [nordot.app](https://nordot.app/897773219007397888); [Eklipse blog](https://blog.eklipse.gg/tools/best-ai-game-highlight-tools-tsai.html)

**StreamLadder**
- A clip converter that turns an existing Twitch clip into a vertical video with facecam/gameplay templates. It does not detect highlights itself (description per a competitor blog). I found no current pricing. — [Eklipse blog (via search summary)](https://blog.eklipse.gg/tools/best-video-game-highlight-recorder.html)

**Newer or niche entrants found**
- **BGMI Clipper (bgmiclipper.com)**: a Windows desktop tool built for BGMI. Uses a custom ONNX model that recognises kill-feed icons frame by frame, plus gunshot/audio-spike detection, in Auto, Audio Only or AI Only modes. Batch folder processing, merging into one reel with fades, direct YouTube upload, offline processing. Accepts OBS captures, screen-recorder output and mobile clips. Pricing is one-time: Free ₹0 (2 video processes), Basic ₹499, Pro ₹699 (lifetime updates, 2 PCs), paid through Razorpay. Windows 10/11 only, with about 2 GB of dependencies downloaded on first run. The page says nothing about captions, vertical output, ranking or funny moments. No user counts, testimonials, accuracy figures or company details ("© 2025"). — [bgmiclipper.com](https://bgmiclipper.com/)
- **FragCut**: browser-based post-stream clipper for FPS Twitch VODs that outputs 9:16. Valorant is its most tuned model; it claims to "work with any game". US$19.99/mo. No mobile mention. — [FragCut](https://fragcut.io/alternatives/powder-gg)
- **StreamClipping AI**: turns Twitch, YouTube and Kick streams and VODs into 9:16 clips, auto-posted. — [streamclipping.ai](https://streamclipping.ai/)
- Generic clippers market gaming pages but are not game-aware: Choppity, Wayin, Short.ai. — [Choppity](https://www.choppity.com/tools/free-ai-clip-maker/ai-clip-maker-for-gaming/); [Wayin](https://wayin.ai/tools/ai-gaming-clip-generator/); [Short.ai](https://www.short.ai/ai-clip-maker/game-highlight)
- Powder.gg successors positioning themselves: AssistantGG, AutoStreamPro, GameClipper Advanced (local). — [AssistantGG](https://www.assistant.gg/en/assistantgg-the-natural-successor-to-powder-gg/); [AutoStreamPro](https://www.autostreampro.com/blog/autostreampro-vs-powder); [GameClipper Advanced](https://gameclipperadvanced.com/blog/powder-gg-alternatives/)

### Inferences
- Detection quality depends on game-specific models. Every tool falls back to audio, chat and transcript heuristics for unsupported games, and that fallback is exactly what users complain about ("tracks volume spikes, grabs banter"). A BGMI-specific visual model (kill feed, knock, squad-wipe, circle state, chicken dinner) is the defensible piece.
- PC capture clients (Medal, Outplayed, NVIDIA, SteelSeries) cannot run on a phone, so they only reach BGMI players who stream through an emulator or a PC capture card. Mobile creators mostly upload recordings or stream to YouTube. That favours a cloud or VOD approach like Eklipse's, and Eklipse is the nearest threat.
- Twitch Auto Clips is English-only alpha and Twitch-locked. BGMI streaming in India happens mainly on YouTube (and formerly Loco/Rooter). This was not verified in this research; see Gaps.

### Gaps
- Could not read eklipse.gg pages directly (403), so the exact game list, a PUBG Mobile/BGMI entry and the help-centre text on how highlights are chosen were not retrieved.
- No current pricing found for StreamLadder, Sizzle, Clipify or SteelSeries Moments. Clipify was not covered by any result.
- Medal, Outplayed and Overwolf pricing and Premium tiers were not retrieved. Medal user numbers after 2024 were not found.
- No source confirmed a native YouTube Live auto-clip or auto-Shorts feature in 2026.
- No r/BGMI or r/PUBGMobile threads about AI clipping tools were retrieved.

## Q2. Which tools support BGMI / PUBG Mobile today? Does Eklipse?

### Takeaway
Only one tool found is purpose-built for BGMI: BGMI Clipper, a small Windows/offline tool sold for a one-time ₹499–699. It detects kill-feed icons and audio, with no captions, ranking or vertical output advertised and no evidence of quality. Eklipse names PUBG and has a "PUBG Clip Maker" page and a mobile app, but no source unambiguously confirms that its game-specific detection works on PUBG Mobile/BGMI footage. No major player advertises BGMI.

### Cited Findings
- BGMI Clipper: purpose-built, kill-feed ONNX model plus audio, accepts "mobile clips" and screen-recorder output, ₹0/₹499/₹699 one-time. No accuracy figures or testimonials. — [bgmiclipper.com](https://bgmiclipper.com/)
- Eklipse has a "PUBG Clip Maker" use-case page, but search summaries do not say whether it covers the mobile version. The fetcher was blocked (403). — [Eklipse PUBG clips](https://eklipse.gg/use-case/pubg-clips/)
- Eklipse's AI Edit page reportedly lists "Mobile Legends, Free Fire, and PUBG" as mobile game clips. This suggests it accepts mobile footage for editing but does not confirm PUBG Mobile-specific highlight detection. — [Eklipse AI Edit (via search summary)](https://eklipse.gg/features/ai-edit/)
- An older Eklipse "gaming assistant" page (about 446 days old) names PUBG among supported titles in a Steam/PC context. — [Eklipse Gaming Assistant (via search summary)](https://eklipse.gg/use-case/eklipse-game-highlights/)
- Outplayed is desktop only; NVIDIA Highlights requires PC game SDK integration (PUBG PC was a launch title); SteelSeries Moments runs on Windows. None supports mobile titles natively. — [Overwolf listing](https://www.overwolf.com/app/overwolf-outplayed); [TechRadar](https://www.techradar.com/news/nvidia-shadowplay-highlights-shares-your-badass-gaming-moments); [SteelSeries](https://steelseries.com/gg/moments)
- Streamlabs' ML highlighter list (Fortnite, Apex, LoL, VALORANT …) has no mobile titles. — [Streamlabs Highlighter](https://streamlabs.com/highlighter)
- Sizzle, Choppity and FragCut pages make no mention of BGMI or PUBG Mobile. — [Sizzle](https://www.sizzle.gg/home); [FragCut](https://fragcut.io/alternatives/powder-gg)

### Inferences
- In practice, BGMI creators today get either generic audio/chat-spike clipping (Eklipse fallback, OpusClip-style tools) or a hobby-grade kill-feed detector (BGMI Clipper). A BGMI-trained model with ranking, good boundaries, Hinglish captions and facecam-aware vertical output does not appear to exist commercially.
- BGMI Clipper shows that kill-feed icon detection on BGMI is technically achievable and that the price point Indian creators accept is low (₹499–699 one-time). That puts pressure on any subscription priced in USD.

### Gaps
- No independent test of Eklipse on PUBG Mobile/BGMI footage was found.
- BGMI Clipper's user base, quality and maker are unknown.
- I did not search Indian streaming platforms (Loco, Rooter) or Indian creator tools for built-in auto-clipping. This should be a follow-up.

## Q3. Which tools shut down, pivoted or struggled, and why?

### Takeaway
Powder.gg, the best-known local AI game clipper, has shut down; most sources give financial difficulties as the reason. Athenascope (probably the "Athenian" in the brief) shut down in April 2022 after a US$2.5M seed. Medal's main 2024 raise went to a general AI-assistant product, Highlight, a partial pivot away from pure clipping. Pure-play gaming clippers have struggled to sustain themselves.

### Cited Findings
- Powder.gg was a Windows app that used local AI to find highlights in recordings and finished Twitch/YouTube/Kick streams. For unsupported games it used audio emotion, chat spikes, transcription and keyword search. The team said it "could no longer sustain the service". The app "will no longer be updated or maintained" and active subscriptions were cancelled. — [The Rundown AI tool archive, last checked 29 Aug 2026](https://www.therundown.ai/tools/powder)
- Shutdown date conflict. FragCut says "late 2024 … due to financial difficulties". An Eklipse comparison page reportedly says July 2026, and GameClipper Advanced says 2026. All three are competitors. — [FragCut](https://fragcut.io/alternatives/powder-gg); [Eklipse vs Powder (via search summary)](https://eklipse.gg/compare/eklipse-vs-powder/); [GameClipper Advanced](https://gameclipperadvanced.com/blog/powder-gg-alternatives/)
- Powder Trustpilot reviews exist (page 5 of reviews indicates a sizeable review base); the content was not retrieved. — [Trustpilot powder.gg](https://uk.trustpilot.com/review/powder.gg?page=5)
- Athenascope (founded by Xfire co-creator Chris Kirmse) analysed Fortnite, Rocket League and PUBG streams to auto-create highlight videos and was free at launch. It raised a US$2.5M seed led by First Round in Feb 2019. — [TechCrunch, 8 Feb 2019](https://techcrunch.com/2019/02/08/athenascope-nabs-2-5m-seed-led-by-first-round-to-bring-gamers-ai-edited-highlight-reels); [PC Gamer](https://www.pcgamer.com/uk/this-tech-uses-ai-to-automatically-create-highlight-clips-for-you-in-fortnite-and-pubg)
- Athenascope "shut down way back in April of 2022" (from Eklipse, a competitor). — [Eklipse blog: Athenascope alternatives](https://blog.eklipse.gg/tools/athenascope-alternatives-you-need-to-try.html); [Framedrop, Feb 2024](https://framedrop.ai/blog/athenascope-alternative)
- Medal launched "Highlight", a general AI-assistant runtime for Windows/Mac, with its July 2024 US$13M raise. — [PR Newswire](https://www.prnewswire.com/news-releases/medal-unveils-highlight---a-revolutionary-ai-assistant-platform-raises-13m-at-333m-valuation-302194826.html)
- Eklipse moved from freemium to fully paid in June 2026 (vendor). This may signal pressure on free-tier compute costs. — [Eklipse (via search summary)](https://eklipse.gg/)
- Streamlabs' highlighter is free and bundled. Twitch is building Auto Clips natively. Platform bundling squeezes standalone tools. — [Streamlabs Highlighter](https://streamlabs.com/highlighter); [streamer.guide](https://streamer.guide/blog/twitchcon-rotterdam-2026-new-features-1440p-clips-guilds)

### Inferences
- Two well-funded or well-known pure-play AI game clippers (Athenascope, Powder) died. Survivors either have a broad capture or social platform (Medal, Overwolf), a hardware or streaming parent (NVIDIA, SteelSeries, Logitech/Streamlabs), or charge subscriptions (Eklipse). Unit economics (video compute, low willingness to pay) are the recurring risk.
- Powder's shutdown left its users looking for replacements, which is why several "Powder alternative" pages appeared in 2026.

### Gaps
- Powder's funding, user counts and an exact, primary-sourced shutdown date (its own farewell post) were not retrieved.
- "Athenian" was not found as a separate product. I assume it means Athenascope; confirm with the requester.
- "Clipify" was not found in any result. Its status is unknown.

## Q4. What the market says is still unsolved

### Takeaway
Users and vendors point to the same unsolved problems: low precision, with audio spikes producing banter clips and quiet skill plays missed; failure on games with little on-screen information or no game-specific model; slow or failed processing; quality loss on export; English-only native features; and platform lock-in. I found no tool that advertises funny-moment detection, non-English (Hindi/Hinglish) commentary understanding, or mobile-game-specific models with ranking and captions.

### Cited Findings
- About 4 in 10 clips good. The tool "tracks volume spikes", grabs banter and misses quiet gameplay. — [Trustpilot AU: Eklipse](https://au.trustpilot.com/review/eklipse.gg)
- AI could not detect kills or objectives in a game with little on-screen information. — [Trustpilot UK p3: Eklipse](https://uk.trustpilot.com/review/eklipse.gg?page=3)
- Poor or random clips that need manual fixes; processing failures and slowness; export quality below the source. — [Trustpilot UK p3](https://uk.trustpilot.com/review/eklipse.gg?page=3); [Trustpilot NZ p3](https://nz.trustpilot.com/review/eklipse.gg?page=3)
- Most recommended clips poor; free-tier and processing limits. — [Product Hunt: Eklipse.gg](https://www.producthunt.com/products/eklipse-gg)
- Twitch Auto Clips alpha is English-only. — [streamer.guide](https://streamer.guide/blog/twitchcon-rotterdam-2026-new-features-1440p-clips-guilds)
- Cross-platform gap: Twitch auto clips do not reach a creator's YouTube audience. — [StreamChat AI](https://streamchatai.com/blog/twitchs-new-ai-stream-summaries-and-auto-clips-what-they-actually-mean-for-your-channel)
- Generic fallbacks (audio emotion, chat spikes, transcription, keywords) are what tools use when no game model exists. — [The Rundown AI: Powder](https://www.therundown.ai/tools/powder)
- Sizzle advertises "edit clip start and end times", an implicit admission that auto boundaries need correction. — [sizzle.gg](https://www.sizzle.gg/home)
- BGMI Clipper's own docs recommend "AI Only" mode when audio is unreliable, implicitly acknowledging that audio-spike detection misfires on noisy mobile or commentary audio. — [bgmiclipper.com](https://bgmiclipper.com/)

### Inferences
- Openings AI-GCM could target:
  - a BGMI-trained visual event model (kill feed, knocks, squad wipes, clutch 1vN, final circle, chicken dinner);
  - Hindi/Hinglish speech plus emotion for funny and hype moments;
  - boundary logic built on fight onset and resolution rather than fixed pre/post windows;
  - vertical reframing that handles the landscape mobile HUD plus facecam;
  - a creator review UI;
  - INR pricing that competes with ₹499 one-time tools.
- The lesson from Powder's death and the volume of competitor clippers: a standalone product needs either very low compute cost per hour of VOD or a distribution wedge (Indian YouTube BGMI creators, esports orgs, agencies).

### Gaps
- No Reddit threads (r/Twitch, r/NewTubers, r/BGMI, r/PUBGMobile) were retrieved directly, so community sentiment rests on Trustpilot and Product Hunt summaries.
- No published accuracy benchmarks exist for any tool. Every quality claim is a vendor claim or an anecdote.
- No vendor was found offering facecam-aware vertical reframing designed specifically for mobile-game HUD layouts. Absence is not proof; it needs hands-on testing.
