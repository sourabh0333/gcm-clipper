# Competitor feature audit: every tool a gaming YouTuber could use instead of GCM Clipper (as of 5 Nov 2026)

Scope note: this goes deeper on the tools already summarised in `research_notes/AI clipper autoposting and multigame gaps/competitors_posting_analytics.md` and `research_notes/Gaming YouTuber content workflow needs/creator_suite_landscape.md`. Everything below was read on 2026-11-05 unless a date is given. Cell codes: **Y** = documented by the vendor, **P** = partial or only on some tiers, **N** = vendor says no or the feature is absent from every official page read, **U** = could not be established. Each cell carries a source number from the key under its table. Prices are as shown on the page on the date given; no currency conversion is applied. Several official sites could not be read at all (eklipse.gg and blog.eklipse.gg are Cloudflare-blocked for both WebFetch and the browser pane; G2, Capterra and Product Hunt's Spikes page block bots; reddit.com and old.reddit.com are not allowed in the browser and no mirror resolved). Where a cell rests on a search-engine summary of a blocked page, a third party, or a competitor's comparison page, the note says so.

## Key question 1: Feature matrix, feature by feature, tool by tool

### Takeaway
Across 20+ tools, game-event detection exists only for PC titles (Eklipse's unnamed "1,000+", Medal's 14-game list, Streamlabs Replay's 52-game list, Powder's 40+, ZoneClip's 30); no tool names BGMI, Free Fire MAX or any mobile title. Approve-then-post, voice "clip it" markers, content calendars, failure alerts, editor seats and even INR pricing (StreamLadder) already exist somewhere, so they are not gaps. Hinglish (romanised) captions exist in exactly one tool (Reap), which has no game awareness. Nobody documents zoom triggered by a game event, a Shorts-share gauge, mobile-game screencast as an input, or re-ranking clips from the channel's own YouTube results.

### Cited Findings

#### Table A: gaming-native clippers (Eklipse, Powder, Spikes Studio, Clipbot.tv, Sizzle, StreamLadder, Medal)

| Feature | Eklipse | Powder | Spikes Studio | Clipbot.tv | Sizzle | StreamLadder | Medal |
|---|---|---|---|---|---|---|---|
| Game-event detection (which games) | **Y** PC/console: "game-specific detection across 1,000+ titles. FPS, MOBA, Battle Royale"; names COD, Fortnite, Valorant, Apex, Minecraft, LoL, GTA V/FiveM, OW2, CS2, Marvel Rivals [A1][A2]. About page claims 3,000+ (search summary) [A3]. "Gameplay Intelligence" engine default on Premium from 1 Jun 2026; not on Kick; unsupported games "fall back to general action detection" (search summary of blocked blog) [A4]. No mobile title named anywhere. Per-game paywalls reported: "every game says 'premium game'" [A5]; ARC Raiders needed "another 20$" [A2] | **Y** "40+ of the world's most popular games, including Fortnite, Valorant, Counter-Strike 2, League of Legends, Rocket League, Call of Duty, Helldivers 2"; other games via "Universal Game Support" (audio emotion) [A6] | **P** "AI-powered clip detection" generic; homepage now pitches a "Micro-Drama Engine"; no game list [A7]. Competitor says detection "tuned for general repurposing" [A8] | **N** No detection: "Your viewers make the clips, or a !clip chat command does it"; filters by Twitch view count [A9] | **P** Filters for "kills, knockdowns, headshots, victories"; "natively supports the most popular games" but no list; "Universal AI" for any stream incl. Just Chatting [A10][A11] | **P** ClipGPT looks for "funny reactions, chat interactions, and intense highlights"; no game events, no game list [A12][A13] | **Y** In-game events per title, list updated 26 Oct 2026: CS2, Dota 2, EA FC Online, Fortnite, GTA V FiveM (server-defined), LoL, Minecraft (server-defined), PUBG (PC), R.E.P.O., Rocket League, RuneScape Dragonwilds, Valorant, War Thunder, YAPYAP [A14] |
| Live-stream moment markers | **Y** Voice: "say 'clip it' mid-stream" [A1]; "Live Clipping & Auto-Post" added 30 Oct 2026 [A1][A2]. No chat command or hotkey documented | **N** "Powder provides post-processing software... the stream must be completed" [A6] | **P** Competitor says Spikes' "spike" is "a keyword your mods punch in by hand" (chat command) [A15]; not on Spikes' own pages | **Y** "!clip chat command" and viewer clips [A9] | **N** Not mentioned [A10] | **N** Not mentioned; ClipGPT runs on finished VODs [A12] | **Y** F8 hotkey (15 s to 10 min) and voice "Medal Clip That" in every game [A14][A16] |
| Works on mobile-game screencast / OBS recordings | **P** Reads stream VODs from Twitch, YouTube, Facebook, Kick [A1]; local VOD upload on web is a credit-based premium feature, and the mobile app "does not support uploading local video files" (search summaries of blocked help pages, which conflict with an AI Edit upload page) [A17]. No screencast/mobile-game claim | **P** Local files and Twitch/YouTube/Kick links [A6]; Windows app, so a phone screencast must be moved to PC | **P** "UPLOAD FILE" on homepage; web editor only up to 5 min [A7] | **N** Twitch clips only; "does not record gameplay or scan VODs" [A9] | **P** "File Uploads" and "local gameplay videos" [A10] | **P** "Import from Upload (max 10 GB)" in AI clipping; ClipGPT itself "supports Twitch & Kick" [A18] | **P** PC capture only; "Medal can video capture any PC game" [A16]; mobile app reviews/posts clips [A16] |
| Upload of local files | **P** see above [A17] | **Y** [A6] | **Y** [A7] | **N** [A9] | **Y** [A10] | **Y** 10 GB [A18] (free tier 200 MB, paid 2 GB in the editor table) [A18] | **Y** "import console captures" [A16] |
| Link import | **Y** Twitch/YouTube/Facebook/Kick accounts [A1] | **Y** Twitch, YouTube, Kick stream links [A6] | **U** Twitch integration "clips as soon as a broadcast ends" per third party [A19] | **Y** Twitch [A9] | **Y** Twitch and YouTube accounts [A10] | **Y** Twitch, Kick, Trovo, YouTube clips; Twitch and Kick VODs [A18] | **N** capture client |
| Hinglish or Hindi captions | **U/N** AI Edit "works best with English videos", more languages "soon" (undated blog via search) [A20]; a competitor says Eklipse states "99+ caption languages" [A15]. No Hindi or Hinglish named on any page read | **U** "AI-generated subtitles"; languages not listed [A6]; English is the only Steam language [A21] | **U** "over 99 languages" [A7]; Hindi not named | **U** "Automated captions" on Pro; languages not listed [A9] | **N** captions not mentioned [A10][A11] | **U** "over 90 languages", auto-detect; Hindi not named [A22] | **U** Premium "Auto-generated subtitles" in editor; languages not listed [A23] |
| Caption editing on phone | **P** "adjust a caption if you want" in the app's swipe stack [A1] | **N** no mobile app [A6] | **N** no mobile app [A8] | **N** no app [A9] | **N** | **P** iOS and Android apps; click-a-word caption editing documented for web [A12][A22] | **N** mobile app is for review/share [A16] |
| Facecam detection and vertical layouts | **P** "formats for vertical", "multiple pre-edited versions" [A1]; facecam detection not stated | **P** "vertical templates" [A6] | **P** "AI face tracking and auto-reframe on the paid tier" (competitor) [A8] | **P** Manual: "Crop your camera and gameplay area" [A9] | **P** "Vertical Download" only [A10] | **Y** "Auto detect and frame facecams" in AI clipping; default and custom layouts in editor [A18] | **N** not mentioned [A16] |
| Zoom on action | **U** AI Edit adds "memes, visual effects" [A20]; zoom not stated | **N** | **P** "Automatic transitions and zooming" (generic) [A7] | **N** | **N** | **P** "Add Zoom & Effects" (manual editor) [A18] | **N** |
| Hook text | **U** | **N** | **P** title, description, hashtags generated [A7] | **N** | **N** | **Y** "AI - Hook intro title"; "Auto Captions, Hashtags and Hooks" on Creator [A18] | **N** |
| Brand kit or templates | **P** "meme templates, overlays"; a Play review mentions "saved templates" [A1] | **P** vertical templates [A6] | **P** "Customizable video templates"; "Custom templates" on Enterprise [A7][A24] | **N** | **N** | **P** "Customise layouts"; "Save hashtags" [A18] | **N** |
| Thumbnails | **U** | **N** | **N** | **N** | **N** | **N** | **N** |
| Titles and descriptions | **P** Manual title/description at posting (help via search) [A25] | **N** | **Y** "title, description, and suggested hashtags" [A7] | **N** | **N** | **Y** hashtags and hooks [A18] | **N** |
| Compilations / long-form output | **Y** montage-maker feature page exists (search listing) [A26] | **Y** "AI Automontages" [A6] | **N** not on pricing page | **N** | **P** "Mashup Your Clips" [A10] | **Y** MontageMaker; "Auto convert all clips into YouTube video"; "Create a YouTube video from your stream" [A18] | **P** editor montages [A23] |
| Clip library across streams | **Y** "clip stack"; storage 14 days monthly / 90 days annual (earlier research) [A1] | **Y** "Content Management" [A6] | **P** storage 7 days free / 90 days PRO+ / unlimited Enterprise [A24] | **P** | **P** 30-day storage [A11] | **U** | **Y** library with "Auto Clips" filter [A14] |
| Content calendar | **Y** Content Planner; scheduling on paid plan (search summary) [A27] | **N** | **Y** "Social Media Scheduler" (annual PRO+) [A24] | **P** "Upload scheduling" (Pro) [A9] | **N** | **Y** "Post and schedule" from Starter [A18] | **N** |
| Approval before posting | **Y** "Eklipse does 90% of the work. You review and approve." [A1]; Content Agent "is not a fully automated publishing tool" (search summary) [A28]. But Live Clipping "automatically shares" (opt-in) [A1] | **N** no posting | **U** | **P** "Pick your favorite clips and only upload those"; default is automatic [A9] | **N** | **P** manual post/schedule; "Auto Pilot: post clips right after your stream" marked "Soon" [A18] | **N** |
| Scheduled posting to YouTube | **Y** Shorts; a reviewer: "schedule posting works great. Not so much for youtube though" (13 Mar 2026) [A29] | **N** | **Y** YouTube among scheduler targets [A24] | **Y** Shorts [A9] | **N** "1-Click Sharing" only [A10] | **Y** "Post & Schedule to YouTube" [A18] | **N** share link; one-click cross-post per earlier research (page timed out today) |
| Link back to stream / related-video | **N** not found [A25] | **N** | **N** | **N** | **N** | **N** | **N** |
| Post status and failure alerts | **Y** "Publishing Failed" notification toggle; red "Failed" status with platform reason; requeue (search summary of help) [A30] | **N** | **U** | **P** "performance insights" (Pro) [A9] | **N** | **U** | **N** |
| Per-channel analytics or learning | **P** planner "track your performance" (blog, no detail); AI-clip feedback page exists [A30][A31] | **N** | **P** "Analytics" dashboard claimed [A7] | **P** "performance insights" [A9] | **N** | **U** | **N** |
| Team / editor seats with client approval | **N** not found | **N** | **P** Enterprise "account manager"; seats not stated [A24] | **N** | **N** | **Y** Pro: "Invite editors to your workspace", "Control what each editor can view or edit" [A18] | **N** |
| Phone app or PWA | **Y** iOS 3.8 (1.2K ratings), v2.7.39 [A2]; Android 2.3 (1.42K reviews, 100K+ downloads), updated 30 Oct 2026 [A1] | **N** "does not have a mobile app" [A6] | **N** (earlier research) | **N** | **N** "NO SOFTWARE OR DOWNLOAD REQUIRED" web [A11] | **Y** iOS and Android [A12] | **Y** iOS/Android [A16] |
| INR pricing or UPI | **N** USD; mobile $27.99/mo (search summary) [A32] | **N** | **N** USD | **N** USD | **N** USD | **Y (INR)** app shows ₹0 Free / ₹1,455 Starter / ₹2,619 Creator / ₹3,783 Pro per month in India, 5 Nov 2026 [A18]. UPI not stated | **N** |
| Free tier limits | **Ended** "fully paid since June 2026"; old free tier was 720p, 1 stream/day, 15 clips/stream, 14-day storage, watermark (search summary) [A33]. Premium $24.99/mo, $112.99/6 mo, $179.99/yr (help via search) [A32] | **Free** "Powder is free for gamers"; paid sub for organisations by contacting sales [A6] | **Free** "Access demo clips", 30 min, 720p, watermark, 7-day storage; PRO+ $32.99/mo (300 min) or $14.09/mo annual (3,600 min/yr); Enterprise $115.99/mo or $56.34/mo annual [A24] | **7-day trial** then Pro $9/mo billed $108/yr ($15 monthly per FAQ) [A9] | **Trial** then $4.99/mo Starter [A11] | **Free** ₹0: 720p/30fps, 200 MB uploads, no ClipGPT [A18] | **Free**; Premium 14-day trial, price not shown [A23] |
| Watermark | **Y** on non-Premium: "Premium: removes watermark" [A1] | **U** third party says free exports watermarked (unverified) [A34] | **Y** free: "our free plan includes a watermark" [A7] | **N** "no watermarks... no matter your plan" [A9] | **N** "no Sizzle.gg watermark" [A11] | **P** "Basic editing never adds a watermark"; Starter-only editor features on Free get one [A12] | **Y** Premium "Removable watermarks" [A23] |

Sources for Table A:
- [A1] Google Play listing, updated 30 Oct 2026 — https://play.google.com/store/apps/details?id=com.eklip.se&hl=en_US
- [A2] App Store listing, v2.7.39 — https://apps.apple.com/us/app/eklipse-gg/id1638105930
- [A3] Search summary of https://eklipse.gg/about (page blocked)
- [A4] Search summary of https://blog.eklipse.gg/streaming-tips/gameplay-intelligence.html and https://eklipse.gg/help/upgrade-eklipse-premium-before-gameplay-intelligence/ (both blocked)
- [A5] Trustpilot review 21 Jun 2026 — https://www.trustpilot.com/review/eklipse.gg?stars=1&stars=2&stars=3
- [A6] Powder site, FAQ — https://www.powder.gg/
- [A7] Spikes Studio homepage — https://www.spikes.studio/
- [A8] AutoClip vs Spikes (competitor) — https://autoclip.dev/compare/autoclip-vs-spikes
- [A9] Clipbot.tv homepage — https://clipbot.tv/
- [A10] Sizzle homepage — https://www.sizzle.gg/
- [A11] Sizzle Universal AI page — https://www.sizzle.gg/universal
- [A12] StreamLadder homepage — https://streamladder.com/
- [A13] StreamLadder ClipGPT page — https://www.streamladder.com/features/clipgpt
- [A14] Medal auto clipping, updated 26 Oct 2026 — https://medal.tv/auto-clipping
- [A15] ClipMe gaming roundup (competitor) — https://clipme.com/best-ai-clipper-for-gaming
- [A16] Medal homepage — https://medal.tv/
- [A17] Search summaries of https://eklipse.gg/help/why-cant-i-upload-my-own-videos/ and https://eklipse.gg/help/how-to-upload-a-video-to-ai-edit/ (blocked)
- [A18] StreamLadder plans page, India, 5 Nov 2026 — https://app.streamladder.com/upgrade
- [A19] SendShort review of Spikes, 11 Jan 2026 (competitor) — https://sendshort.ai/?p=3011
- [A20] Search summary of https://blog.eklipse.gg/eklipse-news-and-guide/how-to-edit-video-using-ai-edit-feature.html (blocked)
- [A21] Powder on Steam — https://store.steampowered.com/app/1794970
- [A22] StreamLadder captions page — https://streamladder.com/features/captions
- [A23] Medal Premium — https://medal.tv/premium
- [A24] Spikes pricing — https://spikes.studio/pricing
- [A25] Search summary of https://eklipse.gg/help/how-to-make-stream-highlights-with-eklipse/ (blocked)
- [A26] Search listing of https://eklipse.gg/features/the-best-ai-gaming-montage-maker (blocked)
- [A27] Search summary of https://eklipse.gg/content-planner/ (blocked)
- [A28] Search summary of https://blog.eklipse.gg/streaming-tips/turn-stream-into-30-days-of-content.html (blocked)
- [A29] Trustpilot Eklipse — https://www.trustpilot.com/review/eklipse.gg
- [A30] Search summaries of https://eklipse.gg/help/will-i-get-a-notification-when-a-post-publishes-or-fails/ and https://eklipse.gg/help/how-do-i-reschedule-a-post-that-failed-to-publish/ (blocked)
- [A31] Search listing of https://eklipse.gg/help/how-to-give-feedback-on-ai-clips (blocked)
- [A32] Search summary of https://eklipse.gg/help/how-much-does-eklipse-premium-cost/ (blocked)
- [A33] Search summary of https://blog.eklipse.gg/eklipse-news-and-guide/is-eklipse-free-pricing-and-features-explained.html (blocked)
- [A34] Search summary of third-party listings (toolbit, G2 AI) for Powder

#### Table B: general AI clippers (Vizard, OpusClip, Klap, Reap, Submagic, Ssemble)

| Feature | Vizard | OpusClip | Klap | Reap | Submagic | Ssemble |
|---|---|---|---|---|---|---|
| Game-event detection | **N** speech-first; "Spark" multimodal beta (earlier research) [B1] | **P** Pro: "visual objects, sound, emotion, genre-specific"; ClipAnything demo prompt "Give me the scene where the player kills the enemy with a stone"; no game list [B2][B3] | **N** [B4] | **N** "less optimized for frame-heavy visual-scene workflows" (earlier research) | **N** gaming page: "Magic Clips finds the strongest moments in a long VOD"; no game events [B5] | **P** "Intelligent selection of gaming highlights and reactions" but works best on speech [B6] |
| Live moment markers | **N** | **N** | **N** | **N** | **N** | **N** |
| Mobile screencast / OBS recordings | **P** uploads up to 60 min free / 600 min paid, 1 GB / 30 GB [B1] | **P** uploads; Twitch and Medal import on Pro [B2] | **P** | **P** | **P** max video length 2 / 5 / 30 min by plan [B7] | **P** "Up to a 20-minute segment per input video" [B8] |
| Upload / link import | **Y/Y** [B1] | **Y/Y** Drive, Vimeo, Zoom, Rumble, StreamYard (Starter); Dropbox, Twitch, FB, IG, TikTok, LinkedIn, X, Loom, Riverside, Frame.io (Pro) [B2] | **Y/Y** | **Y/Y** | **Y/Y** | **Y/Y** |
| Hinglish or Hindi captions | **P** Hindi subtitles page claims "over 97% accuracy", translate to 28 languages [B9]; no Hinglish | **N** help centre: "OpusClip does not support Hindi at this time" [B10]; API blog (13 May 2026) lists Hindi for the API only [B11] | **P** 52 languages (earlier); the Google Play "Klap Ai" app with Hindi is published by "ABD Apps LLC", not Klap's company ZIGG SAS, so it may be unrelated [B12][B4] | **Y** romanised "Hinglish, Arabizi, Romanized Urdu, and more" [B13] | **P** Hindi subtitle page; no Hinglish [B5][B14] | **U** "over 30 languages", Hindi not named [B8] |
| Caption editing on phone | **N** no app | **N** | **U** | **P** mobile browser; native apps "launching in Q3 2026" (not confirmed shipped) [B13] | **N** | **N** |
| Facecam / vertical layouts | **Y** AI reframe [B1] | **Y** reframing options all plans; a competitor says it "locks onto the wrong pane once a facecam sits over gameplay" [B2][B15] | **Y** | **Y** | **Y** | **Y** |
| Zoom on action | **N** | **N** | **N** | **N** | **Y** "Auto-zoom" (Pro) [B7] | **N** |
| Hook text | **P** AI post suggestions [B1] | **Y** Auto Headlines, saved to Brand Template (21 Oct 2026) [B16] | **U** | **U** | **Y** AI hook titles [B7] | **U** |
| Brand kit / templates | **P** custom/brand templates, brand kit on Business [B1] | **Y** 1 / 1 / up to 4 brand templates [B2] | **U** | **Y** 3 / 6 / unlimited brand caption templates [B13] | **Y** Brand Kit (Pro) [B7] | **P** "viral templates" [B8] |
| Thumbnails | **P** AI thumbnail at publish (earlier research) | **N** | **N** | **N** | **N** | **N** |
| Titles and descriptions | **Y** AI caption/hashtags [B1] | **Y** | **U** | **U** | **Y** | **U** |
| Compilations / long-form | **N** | **N** | **N** | **N** | **N** | **N** |
| Content calendar | **Y** "Schedule social posts" (Creator+) [B1] | **Y** scheduler (Pro+) [B2] | **U** | **Y** content calendar, bulk scheduler [B13] | **P** "Publishing" page; 1 / 3 profiles [B7] | **Y** "Calendar Feature... at best performing times" [B6] |
| Approval before posting | **P** user clicks Publish per clip (earlier research) | **P** manual | **U** | **U** | **U** | **U** |
| Scheduled posting to YouTube | **Y** | **Y** Shorts (Starter posts; Pro schedules) [B2] | **Y** "Unlimited social accounts" [B4] | **Y** Shorts (Creator) [B13] | **Y** (Pro+) [B7] | **Y** [B8] |
| Link back to stream / related video | **N** | **P** 4 Sep 2026: "add a link to the full video in YouTube post captions" (caption link, not the related-video field) [B16] | **N** | **N** | **N** | **N** |
| Post status / failure alerts | **U** | **U** | **U** | **U** | **U** | **U** |
| Per-channel analytics / learning | **N** | **P** "Clip analytics" Coming soon on Pro, live on Business [B2] | **P** "Analytics" in all plans, undefined [B4] | **P** AI Virality Score trained on Reap's user base [B13] | **P** "Publish & analytics for social" [B7] | **P** claims "tracks which clips perform best and automatically adjusts future selections" (unverified) [B6] |
| Team / editor seats | **Y** Business shared workspace, seats [B1] | **Y** Pro "2 users / pack, up to 4" [B2] | **P** Pro+ "For teams" [B4] | **Y** Studio up to 3 [B13] | **Y** 1 / 3 / unlimited [B7] | **U** |
| Phone app / PWA | **N** | **N** not mentioned [B2] | **U** (see Hindi row) | **P** coming [B13] | **N** | **N** |
| INR / UPI | **N** | **N** | **N** | **N** | **N** USD/EUR/BRL shown [B7] | **N** |
| Free tier | 60 credits/mo, 720p, 10-min export, 3-day storage, 1 account [B1] | Free: watermark, 3-day storage; Starter $15/mo; Pro $29/mo; Business custom [B2] | No free plan shown; Basic $14.50/mo ($174/yr), Pro $39.50/mo ($474/yr), Pro+ $94.50/mo ($1,134/yr), yearly prices [B4] | Free 1 h clipping + 1 h captions watermarked; Creator $9.99/mo ($119.88/yr); Studio $29/mo ($348/yr) [B13] | No free plan; "15 free videos"; Starter $19/mo ($12 annual), Pro $39 ($23), Business $69 ($41) [B7][B5] | Pro $6/mo ($72/yr, 360 credits), Expert $12, Business $24, Custom $40; no free tier shown [B8] |
| Watermark | free yes [B1] | free yes [B2] | **U** | free yes [B13] | none [B7] | **U** |

Sources for Table B:
- [B1] Vizard pricing — https://vizard.ai/pricing
- [B2] OpusClip pricing — https://www.opus.pro/pricing
- [B3] ClipAnything — https://www.opus.pro/clipanything
- [B4] Klap pricing — https://klap.app/pricing
- [B5] Submagic gaming page — https://www.submagic.co/solutions/gaming
- [B6] Ssemble smart clipping — https://www.ssemble.com/tools/smart-clipping
- [B7] Submagic pricing — https://www.submagic.co/pricing
- [B8] Ssemble pricing — https://www.ssemble.com/pricing
- [B9] Vizard Hindi subtitles — https://vizard.ai/tools/auto-subtitle-generator-online/hindi-subtitles
- [B10] OpusClip help — https://help.opus.pro/docs/article/does-opusclip-support-hindi
- [B11] OpusClip API blog, 13 May 2026 — https://www.opus.pro/blog/multi-language-captions-api
- [B12] "Klap Ai" on Google Play (ABD Apps LLC) — https://play.google.com/store/apps/details?id=com.dos.ai.video.clipping&hl=en_US
- [B13] Reap pricing — https://reap.video/pricing
- [B14] Submagic Hindi page — https://www.submagic.co/hi/auto-subtitle-generator/hindi
- [B15] ClipMe (competitor) — https://clipme.com/best-ai-clipper-for-gaming
- [B16] OpusClip changelog (Canny) — https://opusclip.canny.io/changelog

#### Table C: platform and suite tools (Restream Clips, Streamlabs, StreamElements, vidIQ Clipping, YouTube Studio, YouTube Create)

| Feature | Restream Clips | Streamlabs (Cross Clip / Replay / Sidekick) | StreamElements | vidIQ Clipping | YouTube Studio (Video Clips & Shorts; live highlights) | YouTube Create |
|---|---|---|---|---|---|---|
| Game-event detection | **N** "uses spoken content" [C1] | **Y** Replay (free, Windows): "kills, death events and victories" in 52 listed games incl. PUBG: BATTLEGROUNDS, Minecraft, Fortnite, Valorant, CS2, Warzone, BF6, Marvel Rivals; no mobile title; "Stream Highlights" toggle on imports pulls "funny reactions" [C2][C3]. Sidekick "detects in-game events" for automations; games not listed [C4] | **N** no clipping product; platform nearly shut down May 2026, acquired by Razer 31 Jul 2026 "to keep it operating in its current form" [C5] | **N** "not optimized for gameplay"; "cannot process videos without spoken audio" [C6] | **N** live highlights are generic; Studio AI suggestions are transcript-based [C7][C8] | **N** |
| Live moment markers | **N** | **N** (Replay hotkey 15 s manual clip) [C3] | **N** | **N** | **N** | **N** |
| Mobile screencast / OBS recordings | **P** Studio/encoder recordings over 10 min auto-clipped; uploads and public links [C1] | **P** Replay imports "past streams and gaming clips" [C2]; Cross Clip uploads 100 MB free / 1 GB Pro [C9] | n/a | **P** uploads only (.mp4, 30 GB, 10 h); no YouTube URL [C6] | **N** live highlights: "The stream cannot be a screencast"; must be vertical from the YouTube mobile app [C7]. Studio clips work on uploaded/archived videos [C8][C10] | **Y** phone footage |
| Hindi / Hinglish captions | **P** Hindi in translation list [C1] | **U** Cross Clip captions (v2.5.1), languages not listed [C11] | n/a | **P** Hindi among 11 caption languages [C6] | **P** autocaptions from transcript; AI suggestions available in India and Hindi [C8] | **P** language menu; "cannot generate captions for clips longer than 60 seconds" [C12]; Hindi at launch (earlier research) |
| Caption editing on phone | **N** | **P** Cross Clip iOS app [C11] | n/a | **N** | **P** Studio mobile unverified | **Y** tap word to correct; style tabs [C12] |
| Facecam / vertical layouts | **P** AI "framing" [C1] | **P** Cross Clip layouts; reviews: "Having to manually adjust the box on my face camera is extremely tedious" (7 Jun 2024), "set the camera view, every single time" (19 Feb 2025) [C11] | n/a | **Y** crops to vertical [C6] | **P** Shorts cut from long video; reframing not described [C8] | **Y** |
| Zoom on action | **N** | **N** | n/a | **N** | **N** | **N** |
| Hook text / titles | **Y** captions, titles [C1] | **N** | n/a | **P** title at publish [C6] | **Y** suggested title if Short unchanged [C8] | **N** |
| Brand kit / templates | **N** | **P** Cross Clip layers; "Need to be able to save templates" (review) [C11] | n/a | **P** caption style presets [C6] | **N** | **N** |
| Thumbnails | **N** | **N** | n/a | **N** | **N** | **N** |
| Compilations / long-form | **N** | **Y** Replay "highlight reel" with intros/outros/music [C2] | n/a | **N** | **P** video clips with intro/outro [C8] | **P** editor |
| Content calendar | **N** "no built-in way to schedule an exported clip" [C1] | **N** | n/a | **P** "Publish Now" or "Schedule" per clip [C6] | **Y** scheduled publish (native) | **N** |
| Approval before posting | **N** | **N** | n/a | **P** manual publish | **Y** drafts; live highlights saved "by default as a private video" [C7][C8] | n/a |
| Scheduled posting to YouTube | **P** direct post to Shorts, no schedule [C1] | **P** Replay "Direct uploads to YouTube, Discord and your phone"; TikTok "on the horizon" [C2] | n/a | **Y** Shorts, schedule date/time [C6] | **Y** | **Y** |
| Link back to stream / related video | **N** | **N** | n/a | **N** | **Y** "The source video is added as a related video unless the Short is private, unlisted, or Made for Kids"; clip description link recommended [C8] | **N** |
| Post status / failure alerts | **U** | **N** | n/a | **U** | **Y** native | n/a |
| Per-channel analytics / learning | **N** | **N** | n/a | **P** vidIQ channel analytics (separate) | **Y** YouTube Analytics (not used to rank clips) | **N** |
| Team / editor seats | **N** | **N** | n/a | **P** Enterprise roles (earlier research) | **Y** channel permissions | **N** |
| Phone app | **N** | **Y** Cross Clip iOS 4.6 (563 ratings), last version 25 Sep 2024 [C11] | n/a | **N** web | **Y** Studio app | **Y** Android/iOS |
| INR / UPI | **N** USD | **N** USD | n/a | **N** "local pricing may vary" (earlier research) | free | free |
| Free tier / price | Clips add-on $19 / $29 / $59 per mo on Standard $19 / Professional $49 / Business $239; 50 / 100 / 250 clips; Free plan has "Restream branding" [C13] | Cross Clip Free (100 MB, watermark, outro) / Pro $4.99/mo or $49.99/yr; Ultra $18.99/mo; Ultra "from $15.75/mo" [C9][C11][C4]; Replay free [C3] | n/a | Free 150 credits; Boost $16.58/mo ($199/yr); MAX $39/mo ($468/yr) "Up to 11 hours of short clipping"; paid clips no watermark [C14][C6] | free | free |

Sources for Table C:
- [C1] Restream Clips FAQ — https://support.restream.io/en/articles/10559224-clips-general-faqs
- [C2] Replay announcement, updated 22 Sep 2026 — https://streamlabs.com/content-hub/post/streamlabs-AI-game-highlighter-replay
- [C3] How to use Replay (full game list), updated 22 Sep 2026 — https://streamlabs.com/content-hub/post/how-to-use-replay
- [C4] Streamlabs Ultra — https://streamlabs.com/ultra
- [C5] Tubefilter, 31 Jul 2026 — https://www.tubefilter.com/2026/07/31/gamer-lifestyle-brand-razer-acquires-streamer-platform-streamelements/
- [C6] vidIQ help, 21 Aug 2026 — https://support.vidiq.com/en/articles/11519169-clipping
- [C7] YouTube Help, promote your live stream (highlight eligibility) — https://support.google.com/youtube/answer/2524542?hl=en
- [C8] YouTube Help, Video Clips & Shorts in Studio — https://support.google.com/youtube/answer/15824265?hl=en
- [C9] Cross Clip plans — https://streamlabs.com/cross-clip/plans
- [C10] Tubefilter, 17 Apr 2026 (archived streams, auto-suggestions "later this year") — https://www.tubefilter.com/2026/04/17/youtube-clipping-tool-viewer-clips-shorts/
- [C11] Cross Clip App Store — https://apps.apple.com/us/app/id1568560633
- [C12] YouTube Create captions help — https://support.google.com/youtube/answer/13818789?hl=en
- [C13] Restream pricing — https://restream.io/pricing
- [C14] vidIQ pricing — https://vidiq.com/pricing/

#### Table D: 2026 entrants found by search (ZoneClip, ClipMe, StreamGen, Choppity, AutoClip, Twitch Auto Clips)

| Feature | ZoneClip | ClipMe | StreamGen | Choppity | AutoClip | Twitch Auto Clips (native) |
|---|---|---|---|---|---|---|
| Game-event detection | **Y** "gameplay events, visuals, speech, audio, and reactions together"; 30 games: Apex, Warzone, Counter-Strike, Dota 2, Tarkov, Fortnite, LoL, Overwatch, R6, Valorant, Deadlock...; local AI; v1.1.3 Windows/macOS [D1] | **P** "multi-signal model that includes chat velocity"; admits Eklipse "beats ClipMe" on kills [D2] | **P** "gameplay, audio, and chat signals" on Twitch VODs 8 h+ [D3][D4] | **N** "vocal energy, speech speed, and emotional intensity" [D5] | **P** multimodal; "Silent gameplay with no commentary is the weakest case" [D6] | **P** "chat activity, vocal inflection, and on-screen events" [D7] |
| Live moment markers | **N** | **Y** clips "while you're still live" (automatic, not creator-marked) [D2] | **N** | **N** | **N** | **Y** "Twitch Clip That" voice phrase [D7] |
| Mobile screencast / OBS recordings | **Y** local file or YouTube/Twitch/MP4/M3U8 link [D1] | **N** stream links only [D2] | **P** Twitch VOD, clips, or video files [D4] | **Y** uploads to 10 GB; YouTube/Vimeo/Twitch URL [D5] | **N** channels it watches | **N** |
| Hindi / Hinglish captions | **U** editable captions, player-name corrections [D1] | **N** Starter "English only"; paid auto-translated [D8] | **U** "90+ languages" [D4] | **P** Hindi among 97; "code-switching... means more manual editing" [D9] | **U** site has Hindi interface; captioning unconfirmed [D6] | **U** English rollout first (third party) |
| Facecam / vertical layouts | **Y** "keep the action, HUD, and creator reaction visible" [D1] | **Y** facecam-plus-gameplay layouts [D2] | **Y** "facecam and gameplay in frame" [D4] | **Y** [D5] | **Y** "facecam split layouts" [D6] | **P** "exploring... auto-cropping and trimming" [D7] |
| Zoom on action | **N** | **N** | **N** | **N** | **N** | **N** |
| Hook / titles | **U** | **U** | **Y** captions, brand presets [D3] | **Y** | **Y** virality score with "5-criterion breakdown" [D6] | **N** |
| Brand kit | **P** reusable layouts [D1] | **N** | **Y** brand presets [D3] | **U** | **U** | **N** |
| Compilations | **N** | **P** "Highlight reels" (Pro) [D8] | **P** VOD Editor beta exports to Resolve/Premiere [D3] | **N** | **N** | **N** |
| Content calendar | **Y** "Plan and schedule finished clips across multiple platforms" [D1] | **N** (only $500/mo done-for-you) [D8] | **Y** "Smart schedule", Autopilot queue [D3][D4] | **P** post direct [D5] | **Y** "anti-shadowban pacing" [D6] | **N** |
| Approval before posting | **U** | **N** | **U** | **P** | **Y** team workspaces "route clips through approval before anything publishes" [D6] | **N** |
| Scheduled posting to YouTube | **Y** [D1] | **N** | **Y** Shorts [D4] | **Y** Shorts [D5] | **Y** [D6] | **N** |
| Link back to stream | **N** | **N** | **N** | **N** | **N** | **N** |
| Per-channel learning | **P** "bring performance data back into your workflow" (no detail) [D1] | **N** | **N** | **N** | **N** | **N** |
| Team seats | **N** | **P** Studio 3 seats [D8] | **N** | **N** | **Y** [D6] | n/a |
| Phone app | **N** desktop | **N** web | **N** | **N** | **N** | n/a |
| INR / UPI | **N** USD | **N** USD | **N** EUR | **N** | **N** USD | free |
| Free tier / price | Free: local AI, no watermark, 4K60; Plus $15/mo (10 h cloud), Pro $29/mo (30 h) [D1] | Starter free: 1 stream/mo, 5 h, watermark, 7-day storage; Pro $29/mo (5 streams, 13 h); Studio $99/mo [D8] | free with lower limits; paid "from €8/month" (home) or "€5.49" (blog) [D4][D3] | free tool; paid for no-watermark [D5] | free start; Starter $19.99 (200 credits), Pro $39.99, Scale $79.99; paid watermark-free [D6] | free; "moving to beta in the coming months" after 30 May 2026, waitlist [D7] |

Sources for Table D:
- [D1] ZoneClip — https://zoneclip.ai/
- [D2] ClipMe roundup, updated 7 Oct 2026 — https://clipme.com/best-ai-clipper-for-gaming
- [D3] StreamGen blog, 17 Sep 2026 — https://streamgen.cc/blog/best-clipping-software-for-games/
- [D4] StreamGen homepage — https://streamgen.cc/
- [D5] Choppity gaming tool — https://www.choppity.com/tools/free-ai-clip-maker/ai-clip-maker-for-gaming/
- [D6] AutoClip — https://autoclip.dev/ and https://autoclip.dev/use-cases/gaming
- [D7] Twitch blog, 30 May 2026 — https://blog.twitch.com/en/2026/05/30/everything-we-announced-at-twitchcon-rotterdam-2026/
- [D8] ClipMe pricing — https://clipme.com/pricing
- [D9] Choppity help, languages — https://help.choppity.com/articles/6828649-supported-languages-and-accuracy-expectations

**Other dated facts behind the tables**
- Powder's bare domain `powder.gg` now 301-redirects to a Google Doc titled "To the Powder community" (body not readable: JS-rendered, export blocked) — https://powder.gg/ ; the `www` site still says "Powder is free for gamers!" and lists 40+ games — https://www.powder.gg/ . A Trustpilot reviewer (17 Oct 2025) wrote "i am sad to see them shutting down"; another (16 Nov 2025) "Program doesn't work anymore on my PC. Stopped connecting to my YouTube and Twitch" — https://www.trustpilot.com/review/powder.gg . Insights.gg (24 Aug 2026) says "the service may be winding down soon, so reliability can vary" — https://insights.gg/blog/10-best-clipping-software-that-doesnt-affect-fps . No official shutdown notice was readable.
- BGMI Clipper (bgmiclipper.com), the only BGMI-named tool, did not resolve (DNS ENOTFOUND) on 5 Nov 2026.
- Eklipse's Play Store "What's new" (30 Oct 2026): "Live Clipping & Auto-Post: Eklipse now captures your best moments while you stream and automatically shares them to your social channels. Configure everything directly from your mobile app" — https://play.google.com/store/apps/details?id=com.eklip.se&hl=en_US
- Eklipse App Store: "Mobile app lets you review and post from anywhere"; "Console and mobile: works for PS5 and Xbox streamers" (here "mobile" means the phone app, not mobile games) — https://apps.apple.com/us/app/eklipse-gg/id1638105930
- StreamLadder's Creator plan: "Unlimited use of ClipGPT AI Clipping", "Up to 30 clips from each stream", "ClipGPT supports Twitch & Kick"; Pro: "Auto Pilot: find & edit your best clips — Soon", "Auto Pilot: post clips right after your stream — Soon" — https://app.streamladder.com/upgrade
- YouTube Studio AI clip suggestions: "currently available for creators in select countries" (Brazil, Canada, France, Germany, India, Mexico, South Korea, Spain, UK, US) and languages (English, French, German, Hindi, Korean, Portuguese, Spanish) — https://support.google.com/youtube/answer/15824265?hl=en
- YouTube live highlights: "The stream must be in a vertical format and streamed using the YouTube mobile app", "The stream cannot be a screencast", 10 min–12 h, chat on, saved private — https://support.google.com/youtube/answer/2524542?hl=en
- Twitch Auto Clips: "only 50% of streamers have a clip to share after any given stream... for streamers using Auto Clips, that number is up to 85%"; automatic captions on community clips rolling out; "We'll be moving to beta in the coming months" — https://blog.twitch.com/en/2026/05/30/everything-we-announced-at-twitchcon-rotterdam-2026/

### Inferences
- The gaming-native segment splits into event readers (Eklipse, Medal, Replay, Powder, ZoneClip) and reaction/chat readers (ClipMe, StreamGen, Choppity, Clipbot). Both camps are PC-first; the event readers hook game APIs, replay systems or PC kill feeds, which is why no mobile title appears in any list.
- StreamLadder is the most complete "creator suite" among the gaming tools (facecam auto-detect, hooks, scheduling to five networks, editor seats with permissions, INR prices, phone apps), but its AI picker is speech/chat-based and its auto-post is "Soon".
- Eklipse is the only tool combining game events + approve-then-post + calendar + failure alerts + phone app; its weaknesses are per-game paywalls, no documented Hindi, a dead free tier and poor store ratings (2.3 Android).

### Gaps
- Eklipse's own site, pricing, help centre and blog could not be read (Cloudflare 403 in both WebFetch and the browser pane). Rows marked "search summary" rely on search-engine extracts of those pages and should be re-checked from a different network.
- Spikes' per-plan feature icons, Vizard's per-plan icons and StreamLadder's per-plan comparison icons did not come through as text, so tier placement for some features (e.g. which StreamLadder tier gets facecam auto-detect) is unknown.
- Medal's "Does Medal automatically upload or post my clips?" and "Does auto clipping work on mobile or Mac?" FAQ answers were collapsed; medal.tv/learn pages timed out (522).
- Whether the Google Play "Klap Ai" app is Klap's (publisher mismatch) is unresolved.

## Key question 2: Which features does NO tool have, provably, and which supposed gaps are not gaps

### Takeaway
Provable "nobody has it" items, from the matrix: (1) HUD/event detection for BGMI, Free Fire MAX or any mobile game; (2) Hinglish (romanised) captions inside a game-aware clipper; (3) zoom triggered by a game event; (4) mobile-game screencast as a supported input; (5) a content calendar with a Shorts-share (mix) gauge; (6) documented re-ranking of clips from the channel's own YouTube results; (7) a stream link-back in a gaming clipper's YouTube post; (8) UPI billing. Not gaps: approve-then-post (Eklipse), voice "clip it" markers (Eklipse, Medal, Twitch), INR pricing (StreamLadder), editor seats with permissions (StreamLadder, OpusClip, AutoClip), failure alerts (Eklipse), compilations (StreamLadder, Eklipse, Powder, Replay), phone apps (Eklipse, StreamLadder, Cross Clip, Medal).

### Cited Findings
**Proven gaps**
- Mobile-game detection: Medal's full list (CS2, Dota 2, EA FC Online, Fortnite, GTA V FiveM, LoL, Minecraft, PUBG, R.E.P.O., Rocket League, RuneScape Dragonwilds, Valorant, War Thunder, YAPYAP) has no mobile title — https://medal.tv/auto-clipping . Replay's 52-game list has none — https://streamlabs.com/content-hub/post/how-to-use-replay . ZoneClip's 30 and Powder's named games have none — https://zoneclip.ai/ ; https://www.powder.gg/ . Eklipse's store listings name only PC/console titles and say "FPS, MOBA, Battle Royale" — https://play.google.com/store/apps/details?id=com.eklip.se&hl=en_US . Search found no Eklipse page naming PUBG Mobile or Free Fire; older posts list "PUBG" and say it "felt a bit neglected" (search summary of blog.eklipse.gg). vidIQ: "not optimized for gameplay" — https://support.vidiq.com/en/articles/11519169-clipping . YouTube live highlights exclude screencasts — https://support.google.com/youtube/answer/2524542?hl=en
- Hinglish: the only romanised-Hinglish claim is Reap's ("Hinglish, Arabizi, Romanized Urdu, and more") — https://reap.video/pricing ; Reap has no game detection (earlier research). OpusClip: "does not support Hindi at this time" — https://help.opus.pro/docs/article/does-opusclip-support-hindi . Eklipse AI Edit "works best with English" (search summary). Choppity warns code-switching "means more manual editing" — https://help.choppity.com/articles/6828649-supported-languages-and-accuracy-expectations
- Event-triggered zoom: the only auto-zoom features are generic (Submagic Pro "Auto-zoom" — https://www.submagic.co/pricing ; Spikes "Automatic transitions and zooming" — https://www.spikes.studio/ ; StreamLadder manual "Add Zoom & Effects" — https://app.streamladder.com/upgrade). None ties zoom to a kill/knock event.
- Shorts-share gauge: calendars exist (Eklipse Content Planner, StreamLadder, Reap, Spikes, Ssemble, ZoneClip, AutoClip) but no page describes a long-form vs Shorts mix target or gauge (all pricing/feature pages above).
- Per-channel learning: Ssemble's "tracks which clips perform best and automatically adjusts future selections" is the only claim and names no data source — https://www.ssemble.com/tools/smart-clipping ; ZoneClip says "bring performance data back into your workflow" without detail — https://zoneclip.ai/ ; OpusClip clip analytics "Coming soon" on Pro — https://www.opus.pro/pricing ; Eklipse has an AI-clip feedback form (search listing) but no documented analytics loop.
- Link back to stream: only YouTube Studio's own tool adds the source as a related video — https://support.google.com/youtube/answer/15824265?hl=en ; OpusClip adds "a link to the full video in YouTube post captions" (4 Sep 2026) — https://opusclip.canny.io/changelog . No gaming clipper documents either.
- UPI: no vendor page mentions UPI. Only Sizzle lists payment methods ("debit or credit card, Cash App, and Link") — https://www.sizzle.gg/universal

**Not gaps (competitors already have them)**
- Approve-then-post: Eklipse "You review and approve. That's it." — https://apps.apple.com/us/app/eklipse-gg/id1638105930 ; AutoClip team approval — https://autoclip.dev/
- Creator moment markers: Eklipse voice "clip it"; Medal F8 and "Medal Clip That"; Twitch "Clip That"; Clipbot "!clip" chat command — sources in Tables A and D.
- INR pricing: StreamLadder ₹1,455 / ₹2,619 / ₹3,783 per month — https://app.streamladder.com/upgrade
- Editor seats with permissions: StreamLadder Pro — same page; OpusClip "2 users / pack, up to 4" — https://www.opus.pro/pricing
- Failure alerts: Eklipse "Publishing Failed" toggle (search summary of help).
- Weekly compilation: StreamLadder "Auto convert all clips into YouTube video" and MontageMaker — https://app.streamladder.com/upgrade ; Powder "AI Automontages" — https://www.powder.gg/ ; Replay highlight reels — https://streamlabs.com/content-hub/post/streamlabs-AI-game-highlighter-replay
- Facecam auto-detect: StreamLadder "Auto detect and frame facecams"; ZoneClip and StreamGen keep facecam + gameplay — Tables A and D.

### Inferences
- GCM's defensible combination is (mobile-game HUD + Hinglish speech) for detection, event-triggered zoom and layouts in a phone editor, and a calendar that learns from the channel's own Shorts results. Each of approval, scheduling, calendar, markers, seats and compilations must still be built, but as table stakes, not as the pitch.
- Eklipse's per-game paywall and "Premium game" locks suggest per-title detection is costly for them; a BGMI-first tool with a single price avoids that complaint.
- StreamLadder already prices in rupees, so "INR pricing" alone will not differentiate; UPI and an hours-based plan might.

### Gaps
- "None has it" is proven only against pages that could be read. Eklipse's 1,000+/3,000+ list is unpublished; it is possible (not evidenced) that a mobile title is inside it.
- No independent test of any tool on BGMI or Free Fire footage exists in any source found.

## Key question 3: User complaints from first-hand review pages (gaming use)

### Takeaway
Eklipse draws the most volume and the sharpest gaming-specific complaints: audio-spike clipping that misses quiet gameplay, cuts "right after the best part", wrong captions, games locked behind extra passes, 1–5 h processing, no refunds, and YouTube posting going to long-form instead of Shorts. Spikes' 18 Trustpilot reviews are mostly about billing and silence from support. Powder's recent reviews report the app stopping and "shutting down". StreamLadder and Clipbot have too few reviews to judge. Reddit could not be reached from this environment.

### Cited Findings
**Eklipse** (Trustpilot 4.1 from 971 reviews; 71% 5-star, 7% 1-star; "Hasn't replied to negative reviews") — https://www.trustpilot.com/review/eklipse.gg?stars=1&stars=2&stars=3
- "Low Accuracy (4/10 hit rate) Most clips pulled are just random banter from audio spikes. It tracks volume changes rather than actual clip worthy moments, missing quiet gameplay while clipping useless noise... exporting your clips are locked behind a $23/month subscription" (19 Aug 2026)
- "every game says 'premium game' so cannot make clips, also it doesn't auto clip during streams... if your stream is over 2 hours also states you need premium" (21 Jun 2026)
- "I play FPS mainly and it just clips your character running or doing nothing at all. The processing takes 1+ hours... if you don't buy the 1 year sub... you don't get the VIP passes" (22 Apr 2026)
- "frustrating habit of clipping right after the best part or just as the moment is wrapping up. The Captions are Wrong, every single time" (23 Apr 2026)
- "stuck in 'processing' at 33% forever... Posting to Instagram was painful... never able to post to Facebook" (31 Mar 2026)
- "stream processing for 5+ hours" (15 May 2026); "wouldnt refund me few days later of autorenew for a whole year" (25 Aug 2026); "charged another €23 despite not using the platform" (24 Jun 2026)
- "The automatic clip making and schedule posting works great. Not so much for youtube though." (13 Mar 2026) — https://www.trustpilot.com/review/eklipse.gg
- App Store (3.8, 1.2K ratings): "it doesn't always capture the correct moments rather it collect the badges when you get them. I play Call of Duty so if I get a fury badge it only shows the kill when I received the badge, not all the kills" (31 Mar); "after paying... 28$ an then... another 20$ to clip arc raiders specifically" (4 Jan); "games that I've been playing, are now locked behind a pay wall" (21 Dec 2024) — https://apps.apple.com/us/app/eklipse-gg/id1638105930
- Google Play (2.3, 1.42K reviews): "every clip is muted for 2-3 seconds at the beginning and then it completely de-syncs audio and video... THERE ARE NO REFUNDS" (22 Aug 2026); positive: "30-50ish clips per session... can take up to a 12 hour stream" (11 Sep 2026) — https://play.google.com/store/apps/details?id=com.eklip.se&hl=en_US
- A search-surfaced Trustpilot review says live clipping "put the clip on long-form YouTube when they wanted Shorts" (single report, page not read directly).

**Spikes Studio** (Trustpilot 2.3 from 18; 50% 1-star; unclaimed profile) — https://www.trustpilot.com/review/spikes.studio
- "I paid $20 for a subscription, but I have no idea where my money went... absolutely zero response" (22 May 2026)
- "Error Uploading a Video... after clicking 'Generate'... no one in tech support" (5 Jul 2025)
- "You can't really edit the clips, lots of features are only 'available in the future' and it has a lot of bugs" (3 Jan 2024); several cancellation/refund complaints (2024–2025)
- SendShort (11 Jan 2026) lists "Occasional inaccuracies in AI clipping" — https://sendshort.ai/?p=3011

**Powder** (Trustpilot 4.3 from 105; 1 review in last 12 months) — https://www.trustpilot.com/review/powder.gg
- "sad to see them shutting down" (17 Oct 2025); "Stopped connecting to my YouTube and Twitch... won't let me access" (16 Nov 2025); "slowly becoming subscription, why make youtube and twitch connect a payed feature" (1 Aug 2025); "rendering the final video is limited to fullhd. Also AMD adrenalin recordings won't import" (26 Feb 2025); "would like more supported games" (6 Feb 2025)
- Steam: "Mostly Positive", 73% of 100 reviews — https://store.steampowered.com/app/1794970

**StreamLadder** (Trustpilot 3.7 from 2) — https://www.trustpilot.com/review/streamladder.com
- "even after canceling, they continue to withdraw money" (19 Jan 2024; company replied). G2 "not enough reviews" (search). Vidpros (9 Feb 2026): "Generated clips might not always cut exactly where you want"; ClipGPT needs the top tier — https://vidpros.com/streamladder-review-2026/

**Clipbot.tv** (Product Hunt 5.0 from 3) — https://www.producthunt.com/products/clipbot-tv/reviews — praise only; no critical reviews found.

**Cross Clip** (App Store 4.6 from 563): manual facecam box every time; Pro benefits not unlocking (22 Aug 2025) — https://apps.apple.com/us/app/id1568560633

### Inferences
- Complaints cluster on three things GCM can design against: detection that reads loudness not game state (so quiet clutches are missed and lobby banter is clipped), clips cut late/early around the event, and opaque per-game or per-feature paywalls. A visible "why this clip" (HUD event + timestamp) and a single plan would answer all three.
- Store ratings (Eklipse Android 2.3) show phone-first users are the least satisfied segment of the market leader.

### Gaps
- Reddit (r/Twitch, r/NewTubers, r/youtubers, r/IndianGaming): old.reddit.com is "not allowed due to safety restrictions" in the browser pane, redlib.ssps.io did not resolve, and web search returned no Reddit threads for any query tried. No Reddit evidence is included.
- G2 and Capterra returned 403; Product Hunt's Spikes page was behind a bot check. Only Trustpilot, App Store, Google Play and Product Hunt (Clipbot) were read first-hand.
- No Indian-creator review of any tool on BGMI footage was found.

## Key question 4: What could not be read, and source quality

### Takeaway
Primary pages were read for StreamLadder, Medal, Powder, Spikes (pricing/home), Clipbot, Sizzle, Vizard, OpusClip, Klap, Reap, Submagic, Ssemble, Restream, Streamlabs, vidIQ, YouTube Help, Twitch, ZoneClip, ClipMe, StreamGen, Choppity and AutoClip. Eklipse is the big exception: every eklipse.gg and blog.eklipse.gg URL was blocked, so its rows come from its store listings, Trustpilot and search-engine extracts.

### Cited Findings
- Blocked or unreadable: eklipse.gg/* and blog.eklipse.gg/* (Cloudflare "Sorry, you have been blocked"); g2.com (403); capterra.com (403); producthunt.com Spikes (bot check); old.reddit.com (browser policy); redlib.ssps.io (DNS); bgmiclipper.com (DNS); powder.gg community Google Doc (JS-only, export 400); medal.tv/learn/* (522); kompozy.io, nexusclips.com, clypse.ai (domain checks failed); sizzle.gg/pricing (ECONNRESET); opus.pro/changelog (404; Canny changelog used instead).
- Vendor-vs-vendor pages used (biased, flagged in cells): AutoClip comparisons, ClipMe roundup, Eklipse compare pages (via search), SendShort, Vidpros, StreamGen blog, Subclip, StreamYard blog.

### Inferences
- The Eklipse rows are the least certain and the most important; a re-read from a different IP (phone session) should be the first follow-up.

### Gaps
- Eklipse's current supported-game list, caption languages, analytics and Content Agent tier placement remain unverified first-hand.
- Medal's posting-to-Shorts behaviour and mobile auto-clipping answer were not read today.
