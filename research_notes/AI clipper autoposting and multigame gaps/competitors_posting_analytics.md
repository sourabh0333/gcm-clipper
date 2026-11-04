# Competitors: AI clipping + auto-posting, scheduling and performance analytics (as of 4 Nov 2026)

Scope note: the earlier internal report (`reports/BGMI AI clipper market validation.md`) already covers basic clipping quality, Eklipse/OpusClip/Vizard gaming accuracy, BGMI Clipper, THUNDER, Powder/Athenascope shutdowns and YouTube Live AI highlights. These notes focus on posting, scheduling, approval and analytics features, plus what changed. All pages were read on 2026-11-04 unless a different date is given. Prices are USD as shown on the page (no INR prices were published by any vendor checked). Where an INR figure is given, it uses an **assumed ₹88 = $1**. That rate is not sourced; it is the same assumption as the earlier report. Several official pages (eklipse.gg, StreamLadder pricing) returned 403 errors or sit behind a login, so some rows rely on search summaries and third parties. Each such row says so.

## For each tool: clipping, gaming awareness, auto-post/schedule, approval, performance analytics, Hindi/Hinglish, price

### Takeaway
Auto-posting and scheduling are now table stakes among AI clippers, usually locked to the mid tier ($15–39/mo): OpusClip, Vizard, Klap, Submagic, Reap, Eklipse, Spikes Studio and Ssemble all post to YouTube Shorts, TikTok and Instagram, and most also post to Facebook. None of them combines (a) game-event detection for mobile titles, (b) Hinglish captions and (c) ranking clips by the creator's own past post performance. Analytics are thin: "clip analytics" is "coming soon" even on OpusClip Pro.

### Cited Findings

**Comparison table (official page read 2026-11-04 unless marked)**

| Tool | AI clipping / gaming-aware? | Auto-post / schedule (platforms) | Approval step | Performance analytics / best time | Hindi / Hinglish | Price (USD, date seen) |
|---|---|---|---|---|---|---|
| OpusClip | Yes. Free/Starter clip only from spoken words. Pro/Business add five clipping types (spoken words, visual objects, sound, emotion, genre-specific). "Screenshare/gameplay layout" on all tiers; Twitch and Medal.tv import on Pro+ | Starter: post to YT Shorts, TikTok, Instagram (no scheduler). Pro/Business: post **and schedule** to YT Shorts, TikTok, Instagram, Facebook, LinkedIn, X, Pinterest, Threads, Bluesky; Snapchat "coming soon" | User posts or schedules each clip themselves (no auto-approval flow documented) | Virality score on Starter+. "Clip analytics" is "Coming soon" on Pro and live on Business; "real-time trend analysis" on Business only. No best-time feature listed | 25 transcription languages per Reap's check; Hindi not confirmed officially; no romanized (Hinglish) captions | Free $0 (watermark, 3-day storage, "post one clip every day for free"); Starter $15/mo; Pro $29/mo ($14.50 annual); Business custom |
| Vizard | Yes. "Spark" multimodal mode (beta); earlier report notes gaming claims for kill feeds and clutches | "Schedule social posts" on Creator+. Free has 1 social account, Creator 6, Business 20. Business auto-scheduling publishes up to 10 clips/day (Reap) | User clicks **Publish** on a clip and picks accounts and time; AI writes caption, hashtags and thumbnail | None found | 40 transcription languages; Hindi not named; no romanized captions (Reap) | Free: 60 credits/mo, 720p, 3-day storage. Creator $29/mo ($14.50 annual); Business $39/mo ($19.50 annual) per Reap (official page showed placeholder $0) |
| Klap | Yes, speech-first; no gaming features on the pricing page | "Unlimited social accounts" on all plans; posts to TikTok, YouTube, Instagram, LinkedIn, Facebook; no X (Reap) | Not documented | **"Analytics" included in all plans** (no detail given) | 52 languages; Hindi listed in Play Store app; no romanized captions | Now priced by clips/month: Basic 100 clips $14/mo annual ($29 monthly), Pro 300 clips $39/mo annual ($79 monthly), Pro+ 1,000 clips $94/mo annual. No free tier shown |
| Submagic | Yes, via "Magic Clips" add-on; caption-styling focus; no gaming coverage | Scheduler on Pro+, six platforms including Facebook (Reap). A competitor claims it has no auto-posting; conflicting | Not documented | Not documented | 49 transcription languages; "No romanized script support observed" | Starter $19/mo ($12 annual), Pro $39 ($23 annual), Business $69 ($41 annual); Magic Clips add-on about +$19/mo (aggregators, not official) |
| Eklipse | Yes, gaming-first: on-screen signals (kill feed, round results) plus audio and chat; PUBG page; BGMI unconfirmed | "Content Planner" schedules and posts to TikTok, YT Shorts, IG Reels, Facebook. "Content Agent" queues clips "for you to approve" (search summary of official site; page blocked) | **Yes, approve-before-post** (per search summary) | None found | Not documented | Premium $24.99/mo, Premium Pro $39.99/mo; about $14.99/mo annual; "fully paid since June 2026"; app billing $27.99/mo. Clips stored 14 days (monthly) or 90 days (annual). Third parties still list a free tier |
| StreamLadder | ClipGPT scans VODs up to about 6 h (third party) | "Content Publisher" posts/schedules to TikTok, Reels, Shorts per listings; one review says post-only, no scheduling | Unknown | None found | Unknown | Pricing page is login-gated; Silver about $8.28/mo vs "from €15" in other listings (unverified) |
| Spikes Studio | Yes | Direct publishing or scheduling to YouTube, TikTok, LinkedIn "and more" (vendor) | Unknown | None found | Unknown | Paid from about $19/mo; free tier 30 min/year with watermark (third party) |
| Sizzle | Gaming VOD clipper (kills/knocks, Valorant-first per earlier report) | **No auto-post**: download and upload manually (competitor's claim); email when highlights are ready | n/a | None | No | Starter tier exists; price not checked |
| Medal | PC capture client, in-game events | One-click cross-post to TikTok, YT Shorts, X per Medal help; a competitor says YT Shorts isn't in the docs | Manual one-click | None found | n/a | Free / premium |
| Clipbot (newer, Twitch) | Live monitoring of Twitch streams | **Fully automatic**: clips, crops, captions and uploads to TikTok and YT Shorts "overnight" (vendor) | **No approval** (vendor says fully automatic) | None found | Unknown | Not checked |
| Reap (newer) | Yes, speech-first; "less optimized for frame-heavy visual-scene workflows" | Creator: TikTok, Instagram, YT Shorts, Facebook, LinkedIn; X on Studio. Free: 1 account, 1 post/day | Not documented | AI virality score; model "fine-tuned... on clips labeled with real engagement outcomes from Reap's own user base" | **Only tool with romanized captions incl. Hinglish**; Hindi in top accuracy tier | Free; Creator $9.99/mo annual ($16.99 monthly); Studio $29/mo annual |
| Ssemble (newer) | "Stream Highlights... gaming highlights and reactions"; works best on speech | Schedules and posts to TikTok, YouTube, Instagram, X "at best performing times" | Not documented | Claims smart clipping "tracks which clips perform best and automatically adjusts future selections"; improvement "after 10+ videos" | Caption translation to 30+ languages; Hindi dubbed-track selection | Yearly $6/mo Pro, $12 Expert, $24 Business; headline says "from $7.50/mo" (inconsistent) |
| Repurpose.io | **No AI clipping**: cross-post automation | Instagram, TikTok, YouTube, Facebook named or shown as icons | Not shown | Not shown | n/a | Starter $35/mo (3 accounts/network, 5,000 videos/mo), Pro $79, Agency $179; yearly $349/$790/$1,790; 14-day trial, "Publish 10 videos for FREE" |
| Buffer | No clipping | Automatic publishing to YouTube (Shorts), TikTok (business), Instagram (business/creator), Facebook pages, X; personal IG and FB groups get reminders only | Drafts/reminders | Insights (30-day history on Free, unlimited on paid); "Takeaways: AI-powered observations about performance" on all plans; best-time suggestions from your own history (secondary source) | n/a | Free: 3 channels, 10 scheduled posts/channel; Essentials $5/channel/mo ($60/yr); Team $10/channel/mo |
| Metricool | No clipping | Schedules Reels, TikTok, YouTube (Shorts), Threads, LinkedIn, Pinterest, X (X is an add-on), Bluesky; also **connects Twitch** | Drafts | "Best Times" in the Planner; analytics 30 days on Free, unlimited on paid; competitor analysis (5 profiles on Free) | n/a | Free: 1 brand, 20 posts/mo; Starter $20/mo annual ($25 monthly) for 5 brands; Advanced $53/mo annual ($67 monthly). EUR/USD only |
| Later | No clipping | Visual calendar, auto-publish Reels | — | Best-time tied to its analytics (secondary) | n/a | About $18–25/mo (secondary, unverified) |
| Hootsuite | No clipping | Bulk scheduling | — | OwlyAI best-time suggestions (secondary) | n/a | Entry about $99/mo, per seat (secondary) |

Sources for the table:
- OpusClip plans, posting platforms, virality score, clip analytics "Coming soon" on Pro, Snapchat coming soon, free daily post — [OpusClip pricing](https://www.opus.pro/pricing)
- OpusClip posting caps (TikTok 15/day per account, Instagram 40/day, YouTube about 15/day, X 150/day), language counts, no romanized captions — [Reap report, re-checked 27 Oct 2026](https://reap.video/reports/state-of-top-ai-video-clipping-tools-2026)
- Vizard free tier, account counts, "Schedule social posts" — [Vizard pricing](https://vizard.ai/pricing). Publish flow (pick accounts and time, AI writes caption, hashtags, thumbnail) — [Vizard content calendar](https://vizard.ai/tools/content-calendar). Prices and the 10-clips/day auto-schedule — [Reap report](https://reap.video/reports/state-of-top-ai-video-clipping-tools-2026)
- Klap clips/month tiers, "Unlimited social accounts", "Analytics" in all plans — [Klap pricing](https://klap.app/pricing). Platforms, monthly prices, 52 languages — [Reap report](https://reap.video/reports/state-of-top-ai-video-clipping-tools-2026). Hindi in app — [Google Play](https://play.google.com/store/apps/details?id=com.dos.ai.video.clipping&hl=en)
- Submagic prices — [Reap report](https://reap.video/reports/state-of-top-ai-video-clipping-tools-2026); [Costbench](https://www.costbench.com/software/ai-video-editing-saas/submagic/). Scheduler page — [Submagic Shorts scheduler](https://www.submagic.co/hi/youtube-shorts-scheduler). Conflicting "no auto-posting" claim — [AutoClip comparison](https://autoclip.dev/compare/autoclip-vs-submagic)
- Eklipse Content Planner, Content Agent approve queue, prices, storage — search summary of [eklipse.gg](https://eklipse.gg/) and [Eklipse AI highlights](https://eklipse.gg/features/ai-highlights/) (direct fetch blocked by HTTP 403); [agent-finder](https://agent-finder.co/reviews/eklipse); [Capterra](https://www.capterra.com/p/10015243/Eklipse/) (lists Free and $19.99, which looks outdated)
- StreamLadder — [Vidpros review 2026](https://vidpros.com/streamladder-review-2026/); [ClipSpeedAI comparison](https://www.clipspeed.ai/compare/clipspeedai-vs-streamladder.html); [ShortSync](https://www.shortsync.app/alternative/streamladder) (all third party)
- Spikes Studio — [Draqee](https://draqee.com/spikes-studio/) (third party)
- Sizzle no auto-post — [Clipbot comparison](https://clipbot.tv/blog/clipbot-vs-sizzle-comparison) (competitor); [Sizzle](https://www.sizzle.gg/universal)
- Medal cross-post — [Medal learn](https://medal.tv/learn/share-gaming-clips); dispute — [Clipbot vs Medal](https://clipbot.tv/blog/clipbot-vs-medal-tv-comparison-twitch-highlights)
- Clipbot fully automatic overnight upload — [Clipbot](https://clipbot.tv/blog/clipbot-vs-sizzle-comparison) (vendor)
- Reap — [Reap report](https://reap.video/reports/state-of-top-ai-video-clipping-tools-2026) (vendor-published; ranks itself first)
- Ssemble — [Ssemble Smart Clipping](https://www.ssemble.com/tools/smart-clipping)
- Repurpose.io — [Repurpose.io pricing](https://repurpose.io/pricing/)
- Buffer — [Buffer pricing](https://buffer.com/pricing); best-time from own history — [fs-poster comparison](https://www.fs-poster.com/blog/buffer-vs-hootsuite-vs-later) (secondary)
- Metricool — [Metricool pricing](https://metricool.com/pricing/); Reels and Shorts scheduling — [Metricool Reels guide](https://metricool.com/schedule-reels-with-metricool)
- Later and Hootsuite — [fs-poster](https://www.fs-poster.com/blog/buffer-vs-hootsuite-vs-later); [Vizard/Dupple roundup](https://dupple.com/blog/best-social-media-schedule) (secondary blogs with inconsistent numbers)

**Other findings**
- Dupple reports that Buffer, Later, Hootsuite and Sprout made AI auto-scheduling the default in 2025–26. One 2026 roundup says Reels, TikTok videos and Shorts auto-publish, while Stories still need manual confirmation because of API limits — [Dupple](https://dupple.com/blog/best-social-media-schedule) (secondary).
- Munch's standalone clipper was discontinued. Scheduling now exists only inside Munch Studio ($38–60/mo yearly) — [Reap report](https://reap.video/reports/state-of-top-ai-video-clipping-tools-2026).
- Descript, Veed and CapCut have no scheduler, only manual upload or share-on-export — [Reap report](https://reap.video/reports/state-of-top-ai-video-clipping-tools-2026). (CapCut is banned in India; see the earlier report.)
- Approximate INR at the assumed ₹88/$: OpusClip Pro $29 ≈ ₹2,550/mo; Vizard Creator $29 ≈ ₹2,550; Eklipse Premium $24.99 ≈ ₹2,200; Reap Creator annual $9.99 ≈ ₹880; Buffer Essentials $5/channel ≈ ₹440 per channel; Metricool Starter annual $20 ≈ ₹1,760.

### Inferences
- The cheapest way to get "clip + schedule" today is Reap Creator (about $10/mo annual, and it has Hinglish), or OpusClip Starter ($15/mo) for posting without scheduling. Scheduling at OpusClip needs Pro ($29). GCM Clipper's posting features are therefore table stakes, not a differentiator. The differentiators are approval-first posting tuned to Indian platforms (YT Shorts + IG Reels), game-event ranking and personalised ranking.
- Eklipse's "Content Agent → approve" queue is the closest analogue to GCM's planned approval-based auto-posting, and it is gaming-first. It is the most direct competitor for this feature set.
- No clipper documents Snapchat posting as live (OpusClip lists it as "coming soon"). Snapchat matters in India, so this is a small gap.

### Gaps
- The official Eklipse pricing and Content Planner pages returned 403. The approval flow and per-tier inclusion are from a search summary, not a page read directly.
- Official current pricing for Later, Hootsuite, Sizzle, Medal premium, StreamLadder and Spikes Studio was not verified. Only secondary or third-party figures are available.
- Powder: still treated as shut down per the earlier report. Its status was not re-checked.
- Whether Repurpose.io has an approval step or analytics could not be read from the truncated page.
- India-focused clipping tools: no Inc42, YourStory or Entrackr coverage of an Indian AI clipping startup was found. Only Magicroll (self-described "India built", Hindi and Hinglish support, marketing copy) and Eloelo's Dolphin AI (a production tool, not a clipper) surfaced — [Magicroll](https://magicroll.ai/blogs/best-ai-video-tools-for-indian-creators-in-2026-a-comprehensive-guide); [Digit](https://www.digit.in/features/general/this-indian-ai-startup-wants-to-disrupt-video-production-workflows-heres-how.html). Neither is confirmed as a clipper with auto-posting.
- No vendor publishes INR pricing or UPI billing (not found for any tool checked).

## Which tools understand game events (kills, wins) versus generic speech/virality scoring, and which games they support

### Takeaway
Only the gaming-native tools (Eklipse, Sizzle, Medal, Streamlabs, BGMI Clipper and Clipbot for Twitch) use game or HUD events. The horizontal tools (OpusClip, Vizard, Klap, Submagic, Reap, Ssemble) score clips mostly from transcripts. OpusClip and Vizard have visual modes, but their gaming quality is disputed. None of the clippers with posting and scheduling documents BGMI, Free Fire MAX or COD Mobile detection.

### Cited Findings
- OpusClip "listens. It doesn't watch". A cited creator (an OpusClip brand partner) says it "waits for speech pauses and cuts late, skipping the action" and is "NOT Great at Gaming Clips" — [Two Average Gamers, Apr 2026](https://www.twoaveragegamers.com/opusclip-review-2026-great-tool-wrong-hype-for-gamers/). Contradicted in part by Reap's benchmark, which calls OpusClip ClipAnything "the strongest frame-aware selection workflow in the set" (it typically takes 20–40 min) — [Reap report](https://reap.video/reports/state-of-top-ai-video-clipping-tools-2026). This applies only to the Pro tier and visual mode; Free and Starter clip from spoken words only — [OpusClip pricing](https://www.opus.pro/pricing).
- Reap's test corpus included a 45-minute gaming stream, but it published no gaming results. It describes itself as "less optimized for frame-heavy visual-scene workflows" — [Reap report](https://reap.video/reports/state-of-top-ai-video-clipping-tools-2026).
- Ssemble's FAQ says smart clipping works best on speech-based content, despite its "Stream Highlights" feature — [Ssemble](https://www.ssemble.com/tools/smart-clipping).
- Eklipse markets on-screen kill and round signals and claims to be better for games (vendor comparison) — [Eklipse vs Vizard](https://eklipse.gg/compare/eklipse-vs-vizard/); [Eklipse gaming blog](https://blog.eklipse.gg/tools/ai-clip-maker-gaming.html). The earlier internal report notes HUD detection fails when overlays cover the HUD, and BGMI support is unconfirmed.
- Vizard is described as transcript-driven and struggles with silent gameplay — search summary of [Eklipse vs Vizard](https://eklipse.gg/compare/eklipse-vs-vizard/) (vendor-written, biased). Vizard's own Spark multimodal mode is in beta with no gaming results published — [Reap report](https://reap.video/reports/state-of-top-ai-video-clipping-tools-2026).
- Medal compares 8 gaming clipping tools in its 2026 guide (PC capture-centric) — [Medal](https://medal.tv/learn/best-clipping-software).

### Inferences
- For GTA V RP, Minecraft and "just chatting" style streams, where moments are driven by talk and banter, speech-first tools (OpusClip, Reap, Klap) are reasonable competitors. For BGMI, Free Fire MAX, COD Mobile and Valorant, where moments are silent clutches and kill feeds, only Eklipse-style HUD detection competes, and none of these tools documents mobile HUDs. A multi-game GCM should combine both signals: speech/Hinglish for RP and Minecraft, HUD/audio for shooters.

### Gaps
- No source lists Eklipse's current supported-game list (the page was blocked). Support for Free Fire MAX, COD Mobile, GTA V RP and Minecraft by any clipper with posting is unverified.
- No independent accuracy benchmark on mobile battle royale footage exists for any of these tools.

## Known weaknesses and complaints

### Takeaway
The recurring complaints are clips that are cut late or are speech-driven on gaming footage, silent auto-post failures (especially TikTok), features locked to higher tiers, per-minute credit metering, and watermarks or 3-day storage on free tiers. Hinglish handling is the clearest gap: only Reap documents romanized captions.

### Cited Findings
- OpusClip reviews say TikTok auto-posting has "reliability issues including dropped connections and posts that fail to publish silently", and that auto-posting sits on higher paid tiers — search summary of OpusClip reviews ([Unkoa](https://www.unkoa.com/opus-clip-in-2025-the-smartest-way-to-turn-long-videos-into-viral-shorts/); [aitoolsatlas](https://aitoolsatlas.ai/tools/opusclip/pros-cons)). Anecdotal.
- An Eklipse Trustpilot reviewer reports failed posts to Facebook and Instagram. Others say the AI "occasionally misses crucial action moments or selects completely irrelevant video clips" (178 reviews, mostly positive) — [Trustpilot Eklipse](https://www.trustpilot.com/review/eklipse.gg).
- OpusClip Free: watermark, 3-day storage, 1 credit = 1 min, Free 60 credits; Starter 150; Pro 300 — [Two Average Gamers](https://www.twoaveragegamers.com/opusclip-review-2026-great-tool-wrong-hype-for-gamers/); [OpusClip pricing](https://www.opus.pro/pricing). Vizard Free: 720p, 10-minute export length, 3-day storage — [Vizard pricing](https://vizard.ai/pricing).
- Platform-imposed posting caps (OpusClip: TikTok 15/day, YouTube about 15/day, Instagram 40/day per account) — [Reap report](https://reap.video/reports/state-of-top-ai-video-clipping-tools-2026).
- Hinglish: Reap says it is the only tool tested with romanized captions ("Hinglish, Arabizi, Romanized Urdu..."). Submagic and Klap: "No romanized script support observed" — [Reap report](https://reap.video/reports/state-of-top-ai-video-clipping-tools-2026) (vendor-run test).
- OpusClip Hindi support is unconfirmed. One third party lists Hindi; OpusClip's own pages name about 5 languages "and 20 more" — [aitoolsatlas](https://aitoolsatlas.ai/tools/opusclip/free-vs-paid); [OpusClip alternative page](https://www.opus.pro/alternative/munch).
- StreamLadder's pricing page is login-gated, so the price is not transparent — [ClipSpeedAI](https://www.clipspeed.ai/compare/clipspeedai-vs-streamladder.html).
- Eklipse pricing is inconsistent across sources (Capterra lists Free + $19.99; agent-finder $9.99; official $24.99/$39.99) — [Capterra](https://www.capterra.com/p/10015243/Eklipse/); [agent-finder](https://agent-finder.co/reviews/eklipse).

### Inferences
- Reliability of posting (retries, clear failure notices, re-auth prompts) and a visible daily-cap tracker are cheap ways for GCM to look better than incumbents. An approval-first flow also protects against the "silent failure" complaint.
- Per-minute metering on 3–6 hour streams remains a pain point. OpusClip Pro's 300 credits cover about 5 hours, and Klap's switch to clips-per-month pricing is one response to it.

### Gaps
- No Reddit threads (r/NewTubers, r/Twitch, r/BGMI, r/IndianGaming) were surfaced by search. Community complaints are therefore drawn from review sites and blogs, not Reddit. G2 and Product Hunt were not read.
- No source tested Hinglish quality on gaming squad audio for any tool.

## Is anyone learning from the creator's own past performance to rank clips or choose posting time?

### Takeaway
Partly, and nobody combines it per creator. Clip ranking today uses either a generic virality model (OpusClip, quso, AutoClip) or a model trained on a vendor's whole user base (Reap). Only Ssemble claims to adapt selection to an account's own clip performance, and that is unverified marketing. Best-time-to-post from the creator's own history is standard in schedulers (Buffer, Metricool, Hootsuite, Vista Social) but missing from clippers. "Rank today's clips using this creator's past Shorts and Reels results, and suggest when to post" is an open slot.

### Cited Findings
- OpusClip's virality score is a generic prediction. No formula is published; third parties describe hook, emotion and trend signals and "analysis of 1000s of viral videos" — [toolsforhumans](https://toolsforhumans.ai/ai-tools/opus-clip); [aitoolsatlas](https://aitoolsatlas.ai/tools/opusclip/tutorial). Per-clip analytics are "Coming soon" on Pro and live on Business, plus Business-only "real-time trend analysis" — [OpusClip pricing](https://www.opus.pro/pricing). Reap found no learning model, only a tips article on avoiding low view counts — [Reap report](https://reap.video/reports/state-of-top-ai-video-clipping-tools-2026).
- Reap's scorer is "fine-tuned specifically on clips labeled with real engagement outcomes from Reap's own user base". Reap claims about 1 in 5 generated clips meets an engagement threshold (internal, unverified). This is cross-user, not per-creator — [Reap report](https://reap.video/reports/state-of-top-ai-video-clipping-tools-2026).
- Ssemble: "Smart clipping tracks which clips perform best and automatically adjusts future selections". It claims improvement "after 10+ videos" and posting "at best performing times", without naming its data sources (YouTube/TikTok analytics not mentioned) — [Ssemble](https://www.ssemble.com/tools/smart-clipping).
- quso.ai scores moments on retention and virality signals and cites its own benchmark of 508,000 posts. AutoClip scores hook, retention, shareability, trend fit and emotion, and lists "smart scheduling with optimal posting times" — [quso.ai](https://quso.ai/products/ai-clips-generator); [AutoClip](https://autoclip.dev/) (vendor claims).
- Klap includes "Analytics" in all plans (scope undocumented) — [Klap pricing](https://klap.app/pricing). Vizard has no documented analytics or best-time feature; the user picks the time — [Vizard content calendar](https://vizard.ai/tools/content-calendar).
- Schedulers: Buffer offers AI "Takeaways" observations about performance on all plans and insights history (30 days free, unlimited paid) — [Buffer pricing](https://buffer.com/pricing). Its best-time suggestions are based on the account's own engagement history (secondary) — [fs-poster](https://www.fs-poster.com/blog/buffer-vs-hootsuite-vs-later). Metricool has "Best Times" in its Planner and unlimited metric history on paid plans — [Metricool pricing](https://metricool.com/pricing/). Vista Social refreshes optimal times from new post data — [Vista Social help](https://support.vistasocial.com/hc/en-us/articles/6140669938971-Optimal-time-find-the-best-time-to-publish-on-social).
- Best-time models generally need 2–4 weeks of consistent posting data before they are reliable (explainer, not a study) — [Picmim](https://blog.picmim.com/blog/ai-optimal-post-timing-social-media). SocialKit suggests checking published windows against your own analytics after 4–6 weeks — [SocialKit](https://socialk.it/en/how-to/how-to-schedule-at-the-best-time-to-post).
- Clipspeed describes a feedback loop in which post-publication tracking improves selection, but says most clippers still combine AI with human judgement — [Clipspeed](https://www.clipspeed.ai/blog/how-to-pick-best-clips-from-stream.html).

### Inferences
- A defensible GCM feature: pull the creator's own YouTube Analytics and Instagram Insights for past Shorts and Reels. Learn which clip types (kill/clutch, funny banter, rage, specific game) and which hours performed. Use that to re-rank the day's candidates and suggest a slot, then post only after approval. No competitor found does all of this, and none does it with game-event labels.
- Expect a cold start: published guidance suggests 2–4+ weeks or 10+ posts before personal signals are meaningful. Blend a generic prior (game-event and energy score) with per-creator learning.

### Gaps
- No independent evaluation of any "learning" claim (Ssemble, Reap, quso, AutoClip) was found.
- It is not confirmed whether any clipper reads YouTube Analytics or Instagram Insights APIs for per-creator ranking. Vendors don't name their data sources.
- YouTube Studio's own audience-active-times and recommendation features were not researched in this pass.
