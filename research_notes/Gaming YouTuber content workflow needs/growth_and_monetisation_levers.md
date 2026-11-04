# Growth and monetisation levers for gaming YouTubers (India focus), and features they suggest

Researched 4 Nov 2026. Posting-time evidence is deliberately left out (covered in `reports/AI clipper autoposting and multigame gaps.md`). Evidence grades used below: **Official** (YouTube/Google), **Dataset** (a named sample with a stated method, usually correlational), **Vendor/blog** (numbers without a checkable method), **Folklore** (widely repeated, source not traceable).

## 1. Shorts vs long-form vs live: do Shorts grow gaming channels, live viewership and subscribers?

### Takeaway
YouTube says Shorts do not hurt long-form, but the best independent dataset found (AIR Media-Tech, 18,000 channels, Mar 2025–Mar 2026) shows gaming channels that post mostly long-form have far more subscribers than mixed ones, and there is no hard data at all on Shorts turning into live viewers. The evidence supports Shorts as tight highlight clips that point viewers to the stream or long video (Related Video link), at a modest share of uploads. It does not support "post more Shorts and your channel grows" for gaming.

### Cited Findings
- **Official:** YouTube's blog post "Debunking common myths about YouTube Shorts" (6 May 2025) says Shorts and long-form are recommended by separate systems that still consider cross-format viewing. Shorts product lead Todd Sherman reportedly said on Creator Insider that YouTube has not seen Shorts hurt long-form performance. Only secondary coverage was read, not the post itself — [Net Influencer](https://www.netinfluencer.com/youtube-debunks-common-myths-about-shorts-as-format-gains-traction/); [RouteNote](https://routenote.com/blog/youtube-debunks-the-myths-why-youtube-shorts-is-powerful-for-artists-and-creators/)
- **Folklore warning:** A widely repeated Rene Ritchie quote that "Shorts don't hurt long-form" (often dated "early 2026") appears in different wordings on different sites and could not be traced to a primary source — [CreatiCalc](https://creaticalc.com/blog/do-youtube-shorts-hurt-long-form)
- **Counter-evidence (2023):** The Financial Times reported in Sept 2023 that several YouTube executives worried Shorts were cannibalising long-form viewing — [Tubefilter, 5 Sep 2023](https://tubefilter.com/2023/09/05/youtube-shorts-cannibalizing-long-form-views/); [9to5Google](https://9to5google.com/2023/09/04/youtube-shorts-cannibalize-long-videos/)
- **Counter-evidence (2024, academic):** An arXiv paper on 250 large creators reports "a significant decrease in both view counts and engagement in long-form videos" after short-form launched. The abstract gives no effect sizes, and it is not gaming-specific — [arXiv 2402.18208, Feb 2024](https://arxiv.org/abs/2402.18208v2)
- **Dataset (strongest gaming evidence):** AIR Media-Tech studied 18,000 English-language channels (40+ videos, 10+ long-form each) from March 2025 to March 2026. Gaming channels that are "Long-Only" (under 10% Shorts) had **85% more subscribers** (median) than "Long+Short Mix" (10–70% Shorts), the largest gap of any niche. Medians by tier: 100K–1M monthly views 70,100 vs 37,850; 1M–10M 270,500 vs 163,500; 10M–50M 1.71M vs 1.055M. Only the 50M–100M tier flips (3.03M vs 4.43M), and that rests on 35 channels. Channels that switched strategy mid-year at 100K–1M had a median of 34,700. The authors call it correlational and did not measure live streams. They recommend gaming channels keep Shorts under 20% of uploads, set the Related Video field and add a spoken call to action, and they suggest 25–40% Shorts is the sweet spot across all niches, with a drop above 55% — [AIR Media-Tech, updated 28 May 2026](https://air.io/en/audience-growth/do-youtube-shorts-help-your-long-form-videos-grow-data-from-18000-channels)
- **Dataset (revenue side):** AIR's 274-channel RPM study (within-channel comparison of 149 channels across months with and without Shorts) found gaming long-form RPM of $3.42 without Shorts vs $3.29 with, a 4% gap it calls noise, and named gaming the most stable niche. Its dose-response table is messier: $3.31 at 0 Shorts a month, $1.25 at 6–20, $2.11 at 21+; the biggest drop was at 1–5 Shorts a month, which the authors call counterintuitive and possibly a cohort effect — [AIR Media-Tech, updated 17 Sep 2026](https://air.io/en/air-data-findings/what-is-youtube-shorts-rpm-in-your-niche-in-2026)
- **Vendor/blog (unverified):** Eklipse claims Shorts grow subscribers 3–5x faster for new gaming channels under 10K, and that 15–25% of Shorts-acquired subscribers watch long-form; no method given — [Eklipse blog](https://blog.eklipse.gg/basic-knowledge/youtube-shorts-vs-long-form-gaming-which-grows-faster.html). Eklipse sells a Shorts clipper, so it has an interest.
- **Official feature – Related Video link:** Since 2023 a creator can attach one "related video" link to a Short, pointing to any video on the same channel, **including a live stream**. It shows as clickable text under the channel handle and is set in YouTube Studio (desktop) on new or old Shorts — [Tubefilter, 1 Sep 2023](https://tubefilter.com/2023/09/01/youtube-related-links-multi-format-creators-shorts-live-long-form/); [vidIQ](https://vidiq.com/blog/post/youtube-related-links-connect-shorts-long-videos). YouTube's own guide suggests visual cues (pointing at the link, flashing the target's thumbnail) — [YouTube blog, related videos traffic guide](https://blog.youtube/creator-and-artist-stories/youtube-related-videos-traffic-guide/)
- No official conversion analytics for the Related Video link was found; creators were asking for it at launch — [Tubefilter, 2023](https://tubefilter.com/2023/09/01/youtube-related-links-multi-format-creators-shorts-live-long-form/)
- **Official feature – vertical live:** Since Feb 2024, live streams can appear in the Shorts feed; a creator can stream horizontal and vertical at once (vertical is a centre crop), Super Chat and memberships work there, and non-subscribers can find the stream. Scheduled streams and Premieres do not show in the Shorts feed until live — [Music Ally, 12 Feb 2024](https://musically.com/2024/02/12/youtube-adds-vertical-live-to-promote-livestreams-in-shorts/); [YouTube Creators – Live](https://www.youtube.com/creators/create/live/); [Tubefilter, 8 Feb 2024](https://www.tubefilter.com/2024/02/08/youtube-vertical-live-streams-shorts-feed-multi-format/). No data on viewer or subscriber outcomes from vertical live was found; vidIQ notes vertical streams are hard to find outside the feed — [vidIQ](https://vidiq.com/blog/post/youtube-vertical-live-update/)

### Inferences
- For gaming, Shorts are best treated as **trailers for the stream and the long video**, not as a growth engine of their own. The pitch for GCM Clipper should be "bring viewers to your next stream", in line with the earlier report's conclusion that Shorts income is tiny.
- **Feature: auto-fill the Related Video link** on every posted Short, pointing at the source stream VOD or the next scheduled/live stream. Check whether the YouTube Data API exposes this field; if not, show a one-tap "copy and set in Studio" reminder. (API support not verified — see Gaps.)
- **Feature: spoken/visual CTA end-card** option in the editor ("full match live at 8 PM"), since AIR and YouTube both recommend a call to action.
- **Feature: Shorts-share gauge** on the results page: show what share of the channel's uploads are Shorts and warn above ~20% for gaming (AIR's suggestion). Treat the threshold as a soft default, since the data is correlational.
- **Feature: "Shorts → long/live" tracker** on the results page using the creator's own analytics (subscribers gained per Short, traffic from Shorts feed to the stream), because no official conversion number exists and per-channel evidence is the only kind that is reliable.
- **Feature: vertical-live prompt**: remind creators who stream from phones (most BGMI streamers) that dual horizontal/vertical streaming puts the live stream into the Shorts feed. Low effort, unproven upside.

### Gaps
- No study (official or independent) measuring Shorts → live-stream conversion for gaming. AIR explicitly excluded live.
- No India-specific or Hindi-language version of the Shorts vs long-form study; AIR's sample is English-language channels.
- Whether the YouTube Data API can set the Shorts Related Video field was not checked.
- The original YouTube May 2025 myths post was not read directly; wording comes from secondary coverage.
- No outcome data for vertical live streams.

## 2. Thumbnails and titles (packaging)

### Takeaway
YouTube's own A/B tool (Test & Compare) now tests up to three titles, three thumbnails or combinations, and it picks winners by **watch time share, not click-through rate**. Packaging guidance from MrBeast's leaked document and analyst tools stresses CTR plus matching the promise in the first minute, but no gaming-specific or Hinglish-title study was found.

### Cited Findings
- **Official:** Test & Compare optimises for overall watch time rather than CTR; YouTube says judging the winner by watch time "will best support creators' growth". Results show each option's share of watch time and a label (Winner, Performed Same, Inconclusive). YouTube notes third-party tools often optimise for CTR and may pick a different winner — [YouTube Help: A/B test titles & thumbnails](https://support.google.com/youtube/answer/16391400?hl=en-GB)
- Title testing rolled out globally, allowing up to three titles, three thumbnails or combinations per video — [Search Engine Journal](https://www.searchenginejournal.com/youtube-title-a-b-testing-rolls-out-globally-to-creators/562571/). Some 2026 guides still describe the tool as thumbnail-only, so availability may vary by account — [TubeBuddy](https://www.tubebuddy.com/blog/leaked-youtube-ab-testing-title-thumbnail/)
- Tests run up to about two weeks; a visible 60/40 split is not automatically a winner — [Descript](https://www.descript.com/blog/article/how-to-ab-test-on-youtube-for-better-video-performance); [ThumbnailPeak](https://thumbnailpeak.com/blog/youtube-thumbnail-ab-testing)
- No published 2025–2026 data was found on how often watch-time winners differ from CTR winners — search result summary across the sources above.
- **Leaked MrBeast production document (Sept 2024, authenticity unconfirmed):** the three numbers that matter are CTR, average view duration and average view percentage; a thumbnail/title that does not match the content kills retention; the first minute gets most attention (the team says it lost 21M viewers in the first minute of one video) — [Simon Willison, 15 Sep 2024](https://simonwillison.net/2024/Sep/15/how-to-succeed-in-mrbeast-production/); [Sherwood News](https://www.sherwood.news/culture/mrbeast-youtube-leaked-internal-success-document); [Creator Handbook](https://www.creatorhandbook.net/leaked-document-allegedly-reveals-mrbeasts-secrets-to-youtube-success-the-key-takeaways/)
- **Vendor:** 1of10 scores videos against the channel's own normal ("outlier score") and tracks how title/thumbnail swaps changed views; it claims 300,000+ outlier videos in its database. These are self-reported marketing figures with no independent validation — [1of10 features](https://1of10.com/features); [1of10 Chrome extension](https://chromewebstore.google.com/detail/1of10com-optimization-too/gkfdnmclhbgbidnpmimfdobgjpeblckn?hl=en-US)
- Shorts custom thumbnails became settable via the API on 3 Nov 2026 (from the earlier report) — [YouTube API revision history](https://developers.google.com/youtube/v3/revision_history)
- Swearing in titles or thumbnails still limits ads even though July 2025 rules relaxed profanity in the first 7 seconds (from the earlier report) — [Social Media Today](https://www.socialmediatoday.com/news/youtube-eases-monetization-restrictions-content-profanity/756398/)

### Inferences
- **Feature: generate 3 title + 3 thumbnail variants per long video or stream VOD** (Hinglish and English), so the creator can load them straight into Test & Compare. The app should not build its own A/B testing; YouTube's tool is free and judges by watch time.
- **Feature: thumbnail frame picker** from the clip's peak moment (kill banner, reaction face), since the clip detector already knows where the peak is.
- **Feature: "promise check"**: warn when the title/thumbnail claims something the clip's first seconds do not show (e.g. "1v4 clutch" title on a clip that opens on looting), following the MrBeast mismatch rule.
- **Feature: outlier view on the results page**: rank the creator's own videos by views relative to their channel median, the 1of10 idea applied to the creator's own data.
- Keep auto-titles clean of swearing (ad limits).

### Gaps
- No data-backed study on gaming thumbnails specifically (faces vs gameplay, text vs no text) from vidIQ, TubeBuddy or Paddy Galloway was found in this round.
- No evidence on Hinglish vs Hindi (Devanagari) vs English titles for Indian gaming audiences. This is a real gap; a creator-level test via Test & Compare is the only cheap way to learn it.
- Whether Test & Compare is available through the API (so the app could start tests) was not checked; likely Studio-only.

## 3. Live stream growth levers

### Takeaway
Hard evidence on live growth levers is thin. The academic Twitch work links frequent streaming (5+ times a week) with top channels, and a 2026 minute-level study shows viewers split when a group's creators stream at the same time. Schedule-consistency and stream-length "rules" in blogs mostly lack data. Vertical live and the Related Video link are the official YouTube tools that connect Shorts to live.

### Cited Findings
- **Dataset (academic, Twitch, correlational):** the most-followed outlier channels streamed more than five times a week, mostly under two hours per stream; the authors propose streaming at least 5 times a week, mixing gaming and non-gaming content, and 40+ hours a week. Most streams in the data last up to 6 hours — [arXiv 2111.05939, 2021](https://arxiv.org/pdf/2111.05939)
- **Dataset (academic, 2026):** a minute-level study of 18 Hololive channels found a creator streaming alone averaged 14,377 viewers vs 6,057 when 8 others from the same group streamed at once; viewers transfer between overlapping streams — [arXiv 2603.23773, Mar 2026](https://arxiv.org/html/2603.23773v1)
- **Analyst guidance:** Streams Charts says growth should be judged month over month on average viewers (not peak), because stream length, timing, raids and competition distort daily numbers — [Streams Charts](https://streamscharts.com/news/average-viewers-vs-peak-viewers-what-actually-shows-stream-growth)
- **Folklore/blog (no traceable data):** "consistent schedules for 6+ months outgrow variable schedules even controlling for hours" (attributed to TwitchTracker) and "60-minute streams have the highest retention at 35%" — [StreamLint](https://streamlint.com/blog/twitch-stream-schedule-frequency-guide); [Awisee](https://awisee.com/blog/live-stream-growth-strategies/). No underlying data found.
- **Official:** Scheduled streams and Premieres do not appear in the Shorts feed until live; vertical live streams do appear there and support Super Chat and memberships — [YouTube Creators – Live](https://www.youtube.com/creators/create/live/); [Music Ally](https://musically.com/2024/02/12/youtube-adds-vertical-live-to-promote-livestreams-in-shorts/)
- India context: Twitch has under 2% of streaming hours in India; Rooter (Indian platform) reached ₹82 crore FY25 revenue, 85M+ users, with creators getting 90% of gift revenue — [Outlook Respawn, Sep/Oct 2025](https://respawn.outlookindia.com/pop-culture/pop-culture-originals/in-indias-gaming-boom-creators-navigate-a-pay-to-play-paradox)

### Inferences
- **Feature: stream schedule in the content calendar** with a weekly "streams done vs planned" streak and month-over-month average-viewer trend (Streams Charts' advice), rather than daily peaks.
- **Feature: pre-stream promo Short**: a "going live at 8 PM" Short cut from the last stream's best moment, posted a few hours before the stream with the Related Video link set to the scheduled stream.
- **Feature: collab-clash warning** (later): if the creator's usual collab partners or squad stream at the same slot, flag it, based on the Hololive overlap finding. Weak evidence for India; nice-to-have only.
- Avoid selling stream-length or "best schedule" rules as proven.

### Gaps
- No YouTube-specific data on schedule consistency, stream length, live notifications, Premieres, collabs, chat engagement or raids/Live Redirect was found. YouTube's live redirect feature exists but no outcome data was found this round.
- No India-specific live stream growth data (YouTube Live dominates Indian game streaming, but numbers were not found).
- The 2021 Twitch study is old and Twitch-only.

## 4. Retention for Shorts and highlights

### Takeaway
YouTube publishes no target numbers; the official advice is to compare against the creator's own Shorts of similar length. The two Studio metrics that matter are "viewed vs swiped away" (hook) and average percentage viewed. Shorts can be up to 3 minutes since 15 Oct 2024, but no data shows longer Shorts perform better or worse for gaming.

### Cited Findings
- **Official:** Since 15 Oct 2024, square or vertical uploads up to 3 minutes count as Shorts (previous cap 60 s); YouTube called it "a top requested feature" — [PetaPixel, 4 Oct 2024](https://petapixel.com/2024/10/04/youtube-shorts-expands-video-length-to-three-minutes/); [Tubefilter](https://www.tubefilter.com/?p=182474)
- "Viewed vs swiped away" in Studio is the share of feed impressions where the viewer stayed rather than scrolled past — [Creator Essentials](https://www.creatoressentials.com/glossary/viewed-vs-swiped-away/)
- Benchmarks are best read against the creator's own similar Shorts (format, length, topic, traffic source), not global numbers — [Bytecap](https://www.bytecap.io/research/youtube-shorts-retention-benchmarks)
- **Vendor/blog thresholds (conflicting, unverified):** viewed rate 50–60% average, 70–80% good — [Shortimize](https://www.shortimize.com/blog/youtube-shorts-retention-rate); "70%+ viral, 50/50 average" — [GrowCreator](https://growcreator.pro/blog/youtube-shorts-retention-rate-benchmark); a secondhand vendor claim that Shorts with swipe-away under 30% got 4x the sustained distribution of those over 50% could not be verified — search summary.
- MrBeast document: losing viewers in the first minute is the main loss point even for top videos — [Simon Willison](https://simonwillison.net/2024/Sep/15/how-to-succeed-in-mrbeast-production/)
- Clip compilations/highlights earn a lower long-form RPM (₹2–5) than gameplay with commentary (₹15–35) in India, per one guide (unverified) — [Fluxnote](https://fluxnote.io/guides/youtube-rpm-india-gaming-niche-2026)
- YouTube Analytics API gives a 100-point retention curve per video and separates Shorts-feed traffic (from the earlier report) — [Analytics dimensions](https://developers.google.com/youtube/analytics/dimensions)

### Inferences
- **Feature: hook check at clip-cut time**: start every clip within ~1 s of the action (kill feed, shout), never on a lull. This is the clipper's core job and matches the top user complaint about rivals (late cuts).
- **Feature: loop-friendly endings** option (end on a frame that flows into the start) — folklore-level evidence, cheap to offer as a toggle.
- **Feature: per-creator retention panel**: pull each posted Short's viewed rate and average percentage viewed, compare with the creator's own median for that clip type and length bucket (under 30 s, 30–60 s, 60–180 s). Do not show global "good/bad" thresholds as fact.
- **Feature: length suggestion** learned from the creator's own results, defaulting to short (15–45 s) highlight cuts until data exists; offer 1–3 min "story" cuts for funny/banter moments.

### Gaps
- No data on 1–3 minute Shorts vs under-60 s for gaming.
- No published retention benchmarks specific to gaming Shorts or Indian audiences.
- Whether the Analytics API exposes "viewed vs swiped away" was not confirmed (Studio shows it).

## 5. Monetisation in India

### Takeaway
Ad revenue is small for Indian gaming creators (long-form roughly ₹5–40 per 1,000 views by different sources; Shorts far less), and brand deals make up most income (EY: over 70% for gaming/esports creators). The August 2025 ban on real-money gaming removed the biggest sponsor category, so creators now need non-gaming brands, which raises the value of brand-safe content and professional media kits. Live fan funding (Super Chat, memberships) is significant for top Indian gaming streamers.

### Cited Findings
- **Ad RPM (India):** Indian YouTube creators typically earn ₹20–40 per 1,000 views — [Outlook Respawn](https://respawn.outlookindia.com/pop-culture/pop-culture-originals/in-indias-gaming-boom-creators-navigate-a-pay-to-play-paradox). Guides give gaming long-form ₹15–35 (BGMI at the low end, PC titles higher) and Shorts ₹2–8 — [Fluxnote RPM guide](https://fluxnote.io/guides/youtube-rpm-india-gaming-niche-2026); another gives ₹5–20 overall, BGMI ₹8–15 — [Fluxnote India gaming guide](https://fluxnote.io/guides/youtube-gaming-channel-india-2026). Both Fluxnote figures are unverified and conflict with each other.
- **Shorts RPM (global):** across niches $0.02–$1.48 (AIR, 274 channels); the gaming figure is only in an image not readable here — [AIR Media-Tech](https://air.io/en/air-data-findings/what-is-youtube-shorts-rpm-in-your-niche-in-2026). Gaming Shorts roughly $0.02–0.05 per 1,000 views (from earlier report) — [Klap](https://embed.klap.app/blog/how-much-youtube-shorts-pay-per-1000-views). Licensed music in a Short shrinks the revenue pool — [NBC News](https://www.nbcnews.com/tech/youtube-shorts-revenue-sharing-partner-program-music-license-rcna48635)
- **Brand deals dominate:** EY says over 70% of gaming/esports creator revenue comes from brand partnerships; affiliate and merchandise are under 10% — [Outlook Respawn](https://respawn.outlookindia.com/pop-culture/pop-culture-originals/in-indias-gaming-boom-creators-navigate-a-pay-to-play-paradox)
- **RMG ban:** the Online Gaming Regulation Bill (assented Aug 2025) banned real-money gaming, which had been the main sponsor of gaming creators; RMG was 55–60% of the gaming market before the law. The article expects banking, auto and lifestyle brands to enter as esports gains recognition (speculative) — [Outlook Respawn](https://respawn.outlookindia.com/pop-culture/pop-culture-originals/in-indias-gaming-boom-creators-navigate-a-pay-to-play-paradox)
- **Device brands:** iQOO brings gaming creators into product development — same source.
- **Sponsorship rate cards (vendor/blog, unverified):** Indian 10K–50K subs ₹5,000–25,000 per video; 50K–100K ₹30,000–80,000; 100K+ ₹1–3 lakh+ — [Boss Wallah](https://bosswallah.com/blog/creator-hub/youtube-sponsorship-rates-explained-what-influencers-really-earn-in-2025/). Another guide: ₹50K–2L per video, and publisher deals ₹1–5L a month — [Fluxnote](https://fluxnote.io/guides/youtube-gaming-channel-india-2026). Global gaming dedicated-video benchmarks: 10K–100K $150–625; 100K–500K $900–3.6K; 1M+ $13K–50K — [VidScored](https://vidscored.com/tools/sponsorship-rates/gaming). No primary Indian survey (Kofluence, Chtrbox, EY-FICCI) with tiered gaming rates was found.
- **Fan funding:** PlayBoard's all-time India Super Chat ranking has gaming channels throughout the top 20 (e.g. GtxPreet, Gyan Gaming), with the top channel around $647K — [PlayBoard](https://playboard.co/en/youtube-ranking/most-superchatted-all-channels-in-india-total). Super Chat creator share reported as 70% — [Unity Films](https://unityfilms.net/youtube-super-chat/). Indian ranges: Super Chat ₹1–500 per message, membership tiers ₹49–999 a month (guide estimate) — [Ytverse](https://ytverse.in/monetize-youtube-gaming-channel-in-india-2026); [Kudozz](https://www.kudozz.in/blog/youtube-gifts-memberships-super-thanks)
- **Alternative platforms:** Rooter (90% gift share to creators), STAN Club Passes (25M downloads, $8.5M raised) — [Outlook Respawn](https://respawn.outlookindia.com/pop-culture/pop-culture-originals/in-indias-gaming-boom-creators-navigate-a-pay-to-play-paradox)
- **Market:** Indian esports estimated at $151M in 2025 including a sponsorship correction — [Ken Research](https://www.kenresearch.com/industry-reports/india-esports-market); FICCI-EY 2026 puts the gamer base at 520M — [AnimationXpress](https://www.animationxpress.com/?p=1636098); Lumikai says 590M — [Game Industry Library](https://gameindustrylibrary.com/documents/state-of-india-interactive-media-gaming-2024/read)
- YouTube's inauthentic-content rule (July 2025) can demonetise mass-produced repetitive uploads (from earlier report) — [YouTube monetization policies](https://www.youtube.com/intl/en_be/howyoutubeworks/policies/monetization-policies)

### Inferences
- Since brand money is the main income and the old sponsors (RMG) are gone, software that helps a mid-size creator **win and deliver brand deals** is closer to money than anything about Shorts RPM.
- **Feature: auto media kit** (one-page PDF/link): subscribers, average views per long video and Short (last 30/90 days), live average viewers, audience country/age/gender from YouTube Analytics, top clips, past sponsors. Low effort, data already pulled for the results page.
- **Feature: sponsor-slot tracker** in the calendar: which stream/video carries which brand, deliverables (mention at X min, pinned comment link, Short), due dates, payment status, plus proof-of-delivery clips with timestamps and view counts for the brand report.
- **Feature: brand-safe filter**: flag clips with slurs/abuse, gambling or betting references (illegal RMG promotion after Aug 2025), and other games' branding (Krafton rule), before a clip goes into a sponsor package or gets posted.
- **Feature: Super Chat / member highlights**: detect Super Chat and member shout-out moments in the stream chat log and offer "thank you" clips or a community post, which rewards payers in public. (Effect on revenue unproven.)
- **Feature: affiliate link block** in descriptions (phone, trigger, earphones) — modest value given affiliates are under 10% of income.
- Do not market Shorts income; market "more stream viewers and brand-ready numbers".

### Gaps
- No primary Indian report (Kofluence, Chtrbox, EY-FICCI, Redseer, Google India) with gaming sponsorship rates by subscriber tier was found; all tiered numbers are from blogs.
- No reliable source on YouTube "Hype" availability in India or Super Thanks economics.
- Gaming Shorts RPM in India specifically is unverified.
- Tournament/esports prize income for creators not researched in this round.

## 6. Community: posts, polls, Discord/WhatsApp, comment replies

### Takeaway
Evidence here is mostly vendor anecdote. Polls reliably get more interaction than other post types, but no source shows community posts or comment replies causing channel growth or more views.

### Cited Findings
- AIR Media-Tech reports a case where regular posts got 1,000–1,500 likes and ~40 comments, while polls reached 7.7K votes and 215 comments; it also claims weekly polls got 1.5–6x more engagement than average video comment sections, from internal data across "hundreds of channels" (self-reported) — [AIR Media-Tech](https://air.io/en/how-to-use-polls-to-boost-engagement-from-the-youtube-community)
- A roundup claims polls get 12–25% engagement vs 1–4% for link posts, without naming data — [mean.ceo](https://blog.mean.ceo/?p=11655)
- Some sources say community engagement does not directly boost individual video recommendations; others claim it does; no primary evidence either way — [Gyre](https://gyre.pro/blog/how-can-the-youtube-community-tab-help-you-grow-in)
- AIR suggests weekly posts; too frequent and viewers ignore them (no sample size) — [AIR Media-Tech](https://air.io/en/youtube-hacks/how-to-talk-to-your-youtube-community-10-tips-to-make-your-community-alive)
- STAN's Club Passes (voice rooms, private tournaments) show Indian gaming fans pay for access and interaction — [Outlook Respawn](https://respawn.outlookindia.com/pop-culture/pop-culture-originals/in-indias-gaming-boom-creators-navigate-a-pay-to-play-paradox)

### Inferences
- **Feature: auto-drafted community posts** after each stream: a poll ("Kal kaunsa map? Erangel / Miramar") and a "stream recap" post with the top clip. Cheap to build, low risk; value is engagement, not proven growth. Requires checking whether the API supports community posts (likely not; may need copy-to-Studio).
- **Feature: WhatsApp Channel / Discord share text** for each new clip or stream announcement, as a share button (no API needed).
- **Feature: comment triage** (later): surface comments asking questions or naming sponsors for reply. No evidence on growth effect.

### Gaps
- No independent study on the growth effect of community posts, comment replies, Discord or WhatsApp Channels for gaming or Indian creators.
- Whether the YouTube Data API supports creating community posts was not checked.
