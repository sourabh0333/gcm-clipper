# GCM Clipper master plan

The single plan for building the complete, ready-to-sell app. Written 5 November 2026 and revised the same day after the competitor audit. It folds in all four research reports ([market validation](../reports/BGMI%20AI%20clipper%20market%20validation.md), [auto-posting and more games](../reports/AI%20clipper%20autoposting%20and%20multigame%20gaps.md), [what gaming YouTubers need](../reports/Gaming%20YouTuber%20content%20workflow%20needs.md), [competitor feature audit and creator gaps](../reports/Competitor%20feature%20audit%20and%20creator%20gaps.md)) and the [architecture](../docs/ARCHITECTURE.md). Progress is tracked in [ai-gcm/BUILD_NOTES.md](../ai-gcm/BUILD_NOTES.md).

"GCM Clipper" was the working name; the product is **Kaatclip** (decision D0, 6 Nov 2026; see `reports/Product name research.md`). Folder and plan names keep "gcm-clipper" until renamed.

---

## 1. What we are building

**One sentence:** a gaming content management app for Indian YouTubers that turns every livestream into ranked clips, lets the creator edit them on a phone into the format top Indian gaming Shorts use, plans the week on a calendar, posts approved clips to their own YouTube channel on schedule, and learns from that channel's results.

**The loop it runs:**

```
 stream (creator marks moments live)
   → engine finds the best moments (BGMI screen events + Hinglish talk + markers)
   → studio turns them into Shorts in the top Indian format, and a weekly compilation with commentary
   → creator approves on the phone
   → posted to YouTube on the calendar, with the stream link
   → results feed the next ranking
```

**What is ours and what is not.** Each step of the loop exists in some rival: Eklipse approves and auto-posts, StreamLadder has editor seats and rupee prices, Medal has voice markers. The 25-tool audit found eight things nobody has: event detection for **any mobile game**, **Hinglish** captions inside a game-aware clipper, **zoom triggered by a game event**, **phone-screencast streams as a proper input**, a **Shorts-share gauge**, **re-ranking from the channel's own results**, a **stream link in a gaming clipper's post**, and **UPI billing**. The pitch order is therefore: the engine, then the studio, then the loop.

**Principles**

1. **The creator approves everything that goes public.** This is also YouTube's rule (Developer Policies III.E.3.d and III.I.2): every post, scheduled post, comment and chat message needs the creator's prior express consent, per clip or by a clearly worded standing consent they can revoke.
2. **Game-aware first.** Kills, clutches and wins are read from the screen; talk is read from Hinglish speech. Speech-only tools miss silent kills; we don't. Every clip shows **why it was picked** (the event and its time).
3. **Phone first.** Every creator action works on an Android phone over home Wi-Fi, and the important ones over mobile data.
4. **Shorts are trailers for the stream.** The product's success measure is stream viewers and subscribers, not Shorts views. Top creators leave Short descriptions empty today, so the stream link and the teaser Short are an experiment the beta measures.
5. **Don't rebuild what YouTube gives free:** title and thumbnail tests, dubbing, idea tools, and now Studio's AI clip suggestions (live in India and Hindi; transcript-based, 1:1 trims, no 9:16, no ranking). Prepare inputs for them instead.
6. **₹0 until it earns.** Free tiers, the laptop as the first server, paid services only behind a cap.
7. **No creator passwords, ever.** Google sign-in only. **No downloading from YouTube, ever** (Developer Policies III.E.1), even the creator's own streams.
8. **Resumable and bounded.** Every long job survives a crash or power cut; disk use is capped; cached YouTube data is refreshed or deleted every 30 days.
9. **One flat price.** No per-game or per-feature locks (Eklipse's per-game paywall is its most common complaint).

**Who it is for**

| Segment | Fit | Note |
|---|---|---|
| Hindi/Hinglish BGMI streamers, 10k–500k subscribers, streaming from PC/OBS or phone screencast, paying an intern or editor or doing it themselves | **Primary** | Pain is highest; YouTube's free highlights exclude screencast and encoder streams |
| Free Fire streamers | Second game, month 1 after launch | About 4× BGMI's Indian user base |
| GTA RP, Minecraft, horror streamers | "Talk mode", month 1–2 | Speech-driven; our Hinglish edge applies |
| Tamil and Telugu gaming creators | Month 1–3 | Channels of 2.9M–4.1M exist; regional captions are nearly free |
| Freelance gaming editors and clip channels | Editor tier, month 1 | Buyers and the cheapest sales channel |
| Agencies | Later | Trinity Gaming, Sky Route, 8Bit manage 200+ creators each |
| Creators under ~5k subscribers, vertical-only phone-app streamers, very large creators with teams, esports orgs | Not targeted | Won't pay, already served free, already staffed, or no buying evidence |

---

## 2. Decisions

| # | Decision | Status |
|---|---|---|
| D0 | **Product name** (needed for the domain, the Google sign-in consent screen and legal pages; must not contain "YouTube") | **Kaatclip** (6 Nov 2026). kaatclip.com / .in / .app unregistered and @kaatclip free on YouTube when checked; owner registers them before M4. Instagram handle to confirm by hand. |
| D1 | Own brand, not under Cevrynt; seller is the owner as a sole proprietor (PAN, bank account, free Udyam registration); a company only if it takes off | Decided 4 Nov |
| D2 | Plans, all GST-inclusive and with **no per-game or per-feature locks**: **₹99 first month**, then **Starter ₹499** (8 stream hours a month) or **Pro ₹999** (20 hours, results page); **₹49–99 per stream** by UPI payment link for creators who won't subscribe; **Editor ₹2,499** (several channels, seats, client approval) after launch; first stream free. Ceiling set by StreamLadder (₹1,455–3,783 in India) and Eklipse (about $24.99) | Revised 5 Nov |
| D3 | Laptop is the first server; cloud GPU worker once revenue covers it | Decided 4 Nov |
| D4 | **Video in: upload only.** Marker-window upload from the phone (about 2 minutes around each marker) on mobile data; the full file over Wi-Fi or from a PC. No YouTube link import in any form | **Revised 5 Nov** (YouTube Developer Policies III.E.1 forbid downloading or storing stream video) |
| D5 | YouTube only at launch; Instagram optional later if creators ask | Decided 4 Nov |
| D6 | Build the full app before contacting streamers; revenue may come slowly | Decided 4 Nov |
| D7 | Google sign-in only at launch (phone OTP needs a paid SMS service) | Decided 4 Nov |
| D8 | Notifications: web push plus a free **Telegram bot** at launch; WhatsApp only after paying users (per-message fees and Meta approval) | Added 5 Nov |

---

## 3. User journeys

**Creator, first week**

1. Opens the site on the phone, taps "Continue with Google". Sees the plan page: first stream free, then ₹99 for the first month.
2. Adds their channel: "Connect YouTube" (Google asks for upload and analytics permission). Sets game = BGMI, caption style, logo, and which channel Shorts go to (main or a separate Shorts channel).
3. Before the next stream, installs the app to the home screen and opens the **Live** screen: a big "Mark moment" button. Also turns on the `!clip` chat command for mods; the app listens to the live chat and replies "Clip saved".
4. After the stream, on mobile data, uploads just the minutes around the markers (about an hour of footage for 15 markers); on Wi-Fi, the whole recording.
5. Gets a notification 1–3 hours later: "14 clips ready". Swipes: keep or reject. Each clip says why it was picked ("2 kills at 1:12:40, you marked this"). Marked moments are always in the list.
6. Opens one clip in the studio: it already has the black-band hook ("1v4 LAST ZONE 😱"), the facecam-top layout and the zoom on the kill. Drags the start earlier, approves.
7. Taps "Post this?" on 5 clips. They land on the calendar, one every evening at 7 pm, each with the stream link in the description and a one-tap "finish in Studio" button for the related-video link and pinned comment. The weekly compilation, with their own commentary clips and chapters, is suggested for Sunday.
8. During the week, gets "Posted" and, once, "Post failed, retrying" messages. Sees "Your channel" showing which clip types did best, marked "data through Tuesday" because YouTube's numbers lag 2–3 days.

**Editor (month 1 after launch)**

1. Has an Editor plan with 3 client channels. Each client connected their own YouTube and can revoke it.
2. Edits clips for client A; sends an approval link by push, Telegram or email. Client A approves from the phone; the clip posts to A's channel.

**Owner (you), daily**

1. Opens the admin page: jobs in queue, failures, payments, disk space, quota used. Retries one failed job. Everything else runs itself.

---

## 4. Feature specification

Each module lists what it does and when it is "done". Numbers in brackets are the plan steps the build notes track. "Gap" marks a feature the audit found in no rival; "table stakes" marks one rivals already have.

### 4.1 Capture

| Feature | Behaviour | Done when |
|---|---|---|
| **Moment markers** (3a) | Live screen with a large button; `!clip` chat command read live through `liveChatMessages.streamList` (one 5-unit connection per stream, resumable), with a capped "Clip saved" reply; spoken phrase ("clip that") found in the transcript. There is no chat-replay API, so chat markers are caught live or not at all. Each marker is a strong ranking signal and always produces a clip; markers are shown on the clips they made. Table stakes, but the only input that makes phone-only creators possible | A marker tapped during a real stream appears as a clip with "you marked this"; a `!clip` typed by a mod does the same |
| **Marker-window upload** (4) | The browser (PC, or a phone that has the recording) cuts about 2 minutes around each marker and uploads only those pieces, resumable. **Gap.** Most phone streaming apps keep no local recording (M2 review R4), so full upload from the PC is the main path and this step comes last, behind a spike | A 15-marker stream uploads about 1 hour of footage instead of the whole file |
| **Full upload** (4) | Resumable chunked upload from phone or PC, up to 8 GB; progress and time left; survives a dropped connection; optional "shrink to 720p first" helper for PC | A 2 GB file uploads over Wi-Fi and resumes after airplane mode |
| **Stream details** | Game, title, date, markers attached to the job | Shown on the job page |

### 4.2 Engine

| Feature | Behaviour | Done when |
|---|---|---|
| **Full-length streams** (1) | 3–5 hour streams run end to end; vision and transcript resume from checkpoints; sources deleted 14 days after clips are made | Three real 3+ hour streams processed with no manual fixes; a killed job resumes |
| **Speed** (2) | Vision, sounds and transcript run in parallel; HUD read less often in quiet stretches | A 3-hour stream in about 1 hour on the laptop |
| **Accuracy** (3) | Tested on 10 more streams; knock detection; bigger speech model when a transcript looks broken; talk-vs-fight weights tuned from swipes; every miss written down | 80%+ of hand-picked top moments found on 5 labelled streams |
| **BGMI events** | Eliminations and Remaining counters, Spectating handling, chicken dinner, accolades, knocks. **Gap:** every rival's game list is PC-only | Existing, kept under test |
| **Talk moments** | Laughter, screams, loudness, banter and roast words, Gemini reading the transcript | Existing; Gemini on with a spending cap |
| **"Why this clip"** | Every clip carries its reason: event, timestamp, marker, talk type | Shown in review, library and the editor |
| **Clip labels** (7) | Type (kill, multi-kill, clutch, win, funny, rage, banter, marked), game, length, score, players left, and later post results | Stored for every clip |
| **Post-ready output** (6) | Titles from the three evidenced families (stat or record, Hinglish punchline, suspense), under about 45 characters, one emoji from a fixed set, a per-channel series counter ("1v4 #7"); hashtags sized to the channel; description with the stream link and the Krafton line; no watermark, no added music | Every clip ships with all of these |
| **Brand-safe check and Hinglish bleep** (6) | Flags swearing in titles, slurs, betting or real-money-gaming mentions, other games' logos, and a title that promises what the first seconds don't show. A "sponsor-safe" export bleeps Hinglish gaali from the word-level transcript (Latin and Devanagari lists) | Flags shown on the clip; sponsor-safe export plays clean |
| **Match recap** (M8) | Result-screen detector plus local OCR → a kills-and-placement card image for community posts, and per-match chapter times for compilations and VOD descriptions | A recap card for each match in a test stream |

### 4.3 Review

| Feature | Behaviour | Done when |
|---|---|---|
| **Swipe queue** | One clip at a time, keep or reject, undo, sound toggle, the reason shown; batch keep | Existing; decisions saved per clip |
| **Reject reasons** | Optional one-tap reason (bad cut, not interesting, wrong moment) | Fed back into tuning |

### 4.4 Studio

The studio outputs the format top Indian gaming Shorts already use (sampled from about 45 channels): 30–60 seconds most of the time, up to 3 minutes for full fights, a black top band with a bold 1–2 line hook and one emoji, the HUD and kill feed kept in frame, facecam on top for personality channels.

| Feature | Behaviour | Done when |
|---|---|---|
| **Edit model** (5) | A clip is an edit list (cuts, layout, zoom, captions, text, brand kit) on top of the source; preview in the browser; render only on export; undo | An old clip reopens as an editable project |
| **Library** (S1) | All clips from all streams; filter by stream, game, type, status, flag; search by what was said | 100+ clips browse smoothly on a phone |
| **Editor basics** (S2) | Trim, split, join, timeline, speed up dead parts, instant preview. **Two length presets** chosen by detected fight length: 20–45 s moment, 60–120 s full fight; up to 180 s allowed | A clip re-cut in under a minute on a phone |
| **Gaming layouts** (S3) | HUD-kept 9:16 crop; facecam top 35–45% + gameplay (auto-detected facecam box, adjustable); blur fill; **zoom on the kill** at the known kill time (**gap**: rivals only zoom on speech); HUD, kill feed and minimap always in frame | Correct on all 3 test streams and 3 new ones |
| **Captions and hook** (S4) | Default: black top band, 1–2 line hook in heavy condensed caps (white or yellow, dark outline), one emoji; AI-suggested from the clip's event and talk. Word-level Hinglish captions only on talk clips; Hinglish or Devanagari; word editing. **Burned in only** (a caption track upload costs 400 quota units). **Gap:** Hinglish in a game-aware tool | Looks right on vertical and landscape sources |
| **Brand kit** (S5) | Logo, colours, caption style, intro and outro, standard description, hashtags, game disclaimer, optional lower-third (name, UPI, Instagram) as mid-size channels use; applied automatically | Set once, used on every export |
| **Thumbnails and titles** (S6) | Shorts cover-frame picker; compilation thumbnail = face cut-out (free background removal) + 2–3 words of stat text, or the best kill frame with no text when there is no cam; 3 titles + 3 thumbnails for long videos, ready for YouTube's Test & Compare (which does not cover Shorts) | Every long video has 3 and 3; every Short has a cover frame |
| **Weekly compilation** (S7) | "Best of this week", 8–13 minutes, 16:9, titled in the "[N] FINISHES \| context \| BGMI" pattern, **with the creator's own commentary clips, hook captions and chapters, never a silent kill montage** (YouTube's inauthentic-content rule); manual pick too; 9:16 long-Short option | A compilation renders from 10 clips with chapters and commentary |
| **Sound safety** (S9) | No added music; royalty-free SFX only; warning when background music may trigger a claim | No added track can cause a claim |
| **Style pass** (M8) | Meme and overlay pack, a voice-over slot, and a Hinglish-script UI toggle: the Hindi scene's definition of a "viral" Short | Month 1–3 after launch |
| **Export** (8) | Download one or all (zip), share from phone, copy title and description | Works on Android Chrome |

### 4.5 Plan

| Feature | Behaviour | Done when |
|---|---|---|
| **Content calendar** (S8) | Week and month views; scheduled, posted, failed; drag to move; "fill this week" with approved clips | Plan a week in a few taps |
| **Shorts-share gauge** (S8) | Shows Shorts as a share of uploads, warns above about 20%. **Gap:** no rival calendar has it | Visible on the calendar |
| **Stream schedule** (43) | Upcoming streams from `liveBroadcasts.list` (1 unit) on the calendar; teaser Short suggested before each | Month 1–2 after launch |

### 4.6 Post

| Feature | Behaviour | Done when |
|---|---|---|
| **Connect YouTube** (19) | Google OAuth with `youtube.upload`, `youtube.force-ssl`, `youtube.readonly`, `yt-analytics.readonly` (never `youtubepartner`); refresh token encrypted; disconnect deletes it. While in testing: up to 100 listed testers, re-consent every 7 days. Verification needs the homepage and privacy policy on the app's own domain plus a demo video | A creator connects and disconnects; Google's check passed |
| **"Post this?" approvals** (20) | Every kept clip asks; edit title and description first; batch approve; optional standing consent for scheduled posting, clearly worded, revocable, logged | Nothing posts without a recorded approval |
| **Calendar posting** (21) | Approved clips upload with `privacyStatus=private` always set (the default became public on 2 Nov 2026) and YouTube's `publishAt`; reschedule by updating the still-private video; thumbnail via `thumbnails.set` after processing succeeds (YouTube's auto frame as the fallback on non-YPP channels); post target per clip (main or Shorts channel). Cost per clip about 1 upload + 50 update + 50 thumbnail units | A scheduled Short goes public at the planned minute |
| **Stream funnel** (21) | Stream link in the description; a one-tap "finish in Studio" deep link with pre-filled text for the related-video link and pinned comment (the API cannot set either); a "live at 8 PM" teaser Short before each stream. **Gap:** no gaming clipper links back to the stream | Every posted Short has the link and the Studio button; beta compares Shorts with and without the teaser |
| **Status and safety** (22) | Posted, scheduled, failed with retry; alert on failure; counters for both quota buckets (100 uploads a day, 10,000 units a day: about 100 posted clips with thumbnails); never the same clip twice to one channel; cached YouTube data refreshed or deleted every 30 days | A forced failure shows up and retries |
| **Your channel** (23) | Recent uploads and their views next to the new clips, split by `creatorContentType` (Shorts, live, VOD), marked "data through <date>" (48–72 hour lag) | Shown on the job page |

### 4.7 Learn

| Feature | Behaviour | Done when |
|---|---|---|
| **Your results** (35) | Better or worse than the channel's usual by clip type and length; outliers; subscribers per Short; Shorts share; average and peak live viewers by month. **Gap:** no rival re-ranks from the channel's own results | Once creators have 10+ posted clips |
| **Personal ranking** (36) | Push up clip types that worked for this creator, combined with swipes; checked against beta creators' own picks | After the results page |

### 4.8 Accounts and billing

| Feature | Behaviour | Done when |
|---|---|---|
| **Sign-in** (12) | Google only; secure cookie session; each creator sees only their own data | Two accounts cannot see each other's jobs |
| **Plans and usage** (15, 16) | Stream hours per plan; clear message at the limit; first stream free; ₹99 first month; per-stream UPI payment links next to AutoPay subscriptions; prices shown GST-inclusive | Limits enforced |
| **Payments** (15) | Razorpay Subscriptions with UPI AutoPay (about 2.36% with GST) and payment links; webhook updates the plan; invoices; cancel any time | A test subscription activates, renews and cancels; a per-stream link pays |
| **Editor tier** (41) | Seats, several channels, client approval link. Table stakes, still the cheapest sales channel | Month 1 after launch |

### 4.9 Admin, operations, trust

| Feature | Behaviour | Done when |
|---|---|---|
| **Admin page** (28) | Users, jobs, posts, failures, payments, disk, quota; retry; refund link | Everything above visible |
| **Monitoring and messages** (29) | Telegram bot for "clips ready", post status and alerts; phone alert when a job or post fails or the laptop goes offline; daily summary | Alerts arrive within 5 minutes |
| **Backups** | Database and brand kits backed up daily to free cloud storage; restore tested | A restore from backup works |
| **Security** | HTTPS only, encrypted tokens, rate limits, secrets in `.env`, dependency updates | A review checklist passed before beta |
| **Legal** (26, 27) | Privacy policy, terms (creator owns the stream; posting only after approval; consent wording for scheduled posting), refund policy, AI processing consent, Google data-use disclosures, 30-day data retention, YouTube branding rules (no "YouTube" in the name, logos link back); game publishers' rules documented | Live on the site; Razorpay accepts them |
| **Paid Gemini** (25) | Paid tier with a spending cap for customer data | Cap set; cost per stream measured |
| **Landing page** (30) | What it does, demo clips (with permission), pricing, sign-up | Live |

---

## 5. Technical plan

Summary; details in [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md).

| Layer | Choice |
|---|---|
| Engine | The existing `aigcm` Python pipeline, extended |
| API | FastAPI |
| Worker | Separate Python process pulling jobs from the database queue; a cloud GPU worker can join later |
| Database | SQLAlchemy models, SQLite first, Postgres later; Alembic migrations |
| Web app | React + TypeScript + Vite, installable PWA, mobile-first |
| Editing | Edit lists in the database; browser preview; ffmpeg render on export |
| Upload | Resumable chunked upload; marker-window trims cut on the phone (browser-side ffmpeg or recorder slices) before upload |
| Live chat | One `streamList` connection per live stream for `!clip`, resumable, with a capped reply |
| Storage | Per-job folders on the laptop; sources 14 days, clips 30 days; Cloudflare R2 later |
| Access | Cloudflare Tunnel to the laptop; static files on Cloudflare Pages |
| Sign-in | Google OpenID Connect; YouTube scopes requested separately |
| Payments | Razorpay Subscriptions and payment links |
| Messages | Web push and a Telegram bot |
| AI | Gemini (paid, capped) for judging and talk; local models for speech, sounds, OCR; IndicTrans2 (free) for regional languages |

**Data model (main tables)**

`users`, `channels` (YouTube connection, encrypted token, target channel for Shorts), `brand_kits`, `streams` (job, source, game, markers, status), `moments`, `clips` (labels, reason, scores, flags, decision), `edits` (edit list per clip, versions), `compilations`, `calendar_entries`, `posts` (YouTube video id, schedule, status, attempts, quota used), `post_stats` (daily analytics snapshots, 30-day retention), `subscriptions`, `payments`, `editor_memberships`, `approvals` (per clip and standing consent), `audit_log`.

**Quality bar for every milestone**

- Unit tests for every module; the suite stays green (`python -m pytest`).
- A real-stream check for any pipeline change.
- Phone check in Chrome on Android for any screen change.
- Notes updated, committed and pushed.

---

## 6. Build order

Milestones are gated by their "done when", not by dates. Week numbers are estimates for a full-time build with Claude doing the code; a milestone that slips moves the rest.

| Milestone | Scope | Done when | Weeks |
|---|---|---|---|
| **M0 Foundation** | Architecture; resume from checkpoints; cleanup | Done 4–5 Nov | — |
| **M1 Engine product-grade** | Full streams, speed, accuracy on 10 streams, markers (file-based first), "why this clip", labels, title generator, brand-safe check and bleep | Three 3-hour streams end to end in about 1 hour each; 80%+ top-moment recall on 5 labelled streams | 1–3 |
| **M2 Platform core** | Database and models, API, worker queue, Google sign-in, resumable and marker-window upload, Telegram bot, new web app with jobs, progress, review (replaces the current server and PWA). **Reviewed 7 Nov; steps, decisions and owner tasks in [M2 platform core plan](M2%20platform%20core%20plan.md)** | Two creators can sign in, upload from a phone, and review their own streams; the old app is retired | 4–5 |
| **M3 Studio** | Edit model, library, editor with length presets, layouts and zoom, black-band hook and captions, brand kit, thumbnails and cover frames, compilation with commentary and chapters, sound safety, export | Every 4.4 "done when" met; phone-tested | 6–8 |
| **M4 Plan and post** | Calendar, Shorts-share gauge, YouTube connect, approvals and standing consent, scheduled posting, funnel (description link, Studio deep link, teaser Short), status and quota counters, your-channel view, live `!clip` listener | A clip approved on the phone posts to a test channel at the scheduled minute with the stream link; Google's scope check submitted | 9–10 |
| **M5 Service** | Domain, Cloudflare Pages and Tunnel, Razorpay plans, payment links and webhooks, usage limits, notifications, storage lifecycle | A test subscription activates and renews; a per-stream link pays; limits enforced; reachable from mobile data | 11 |
| **M6 Trust and ops** | Legal pages, admin page, monitoring, backups, security checklist, paid Gemini with cap, landing page | All 4.9 "done when" met | 12 |
| **M7 Beta and launch** | Closed beta: 5 streamers plus 1 editor for 2 weeks; fixes; testimonials; open sales | Beta creators post real Shorts through the app; no unresolved critical bug | 13–14 |
| **M8 After launch** | Free Fire; talk mode; Tamil and Telugu captions and titles; results page; personal ranking; editor tier; match recap cards; style pass (memes, overlays, voice-over, Hinglish UI); stream schedule; chat-spike signal; cloud worker when revenue allows | Rolling, month 1–3 | 15+ |

**Dependencies:** M2 needs D0 (name) for the sign-in consent screen. M4 needs the domain and privacy policy on it (pulled forward from M5/M6 for Google's check). M5 needs Razorpay KYC, which can take days, so it starts in week 1.

---

## 7. What only you can do

| When | Task | Why |
|---|---|---|
| Week 1 | ~~Choose the product name (D0)~~ Done: Kaatclip. Register kaatclip.com, kaatclip.in, kaatclip.app and @kaatclip on YouTube; check Instagram | Domain, consent screen, legal pages |
| Week 1 | Udyam registration (free), then start Razorpay KYC | Can take days to approve |
| Week 1 | Create a test YouTube channel and a Telegram account for the bot | Posting and message tests before any creator is involved |
| Week 1–2 | Review clips strictly; try the live marker button during a real session | Tunes ranking and markers |
| Week 4 | Buy the domain; create Cloudflare and Google Cloud accounts; set up the Google sign-in consent screen with the prepared text | Sign-in and hosting |
| Week 9 | Submit Google's sensitive-scope check with the prepared answers and demo video | YouTube posting for anyone outside the test list |
| Week 11 | Razorpay live keys | Payments |
| Week 12 | Approve the legal pages; add a card to Google AI Studio with the cap | Launch |
| Week 13 | Invite 5 streamers and 1 editor | Beta |

Claude prepares every form answer, policy text and demo video script. You only sign up, paste and approve.

---

## 8. Costs

| Before the first sale | Cost |
|---|---|
| Hosting, sign-in, database, storage, Telegram, tunnel (free tiers) | ₹0 |
| Domain | about ₹800–1,000 a year |
| Google scope check, YouTube posting | ₹0 |
| Razorpay | ₹0 upfront, about 2.36% per payment with GST |
| Total | **about ₹1,000** |

| After customers pay | Cost |
|---|---|
| Paid Gemini | a few rupees per stream (measured in M1) |
| Regional captions | IndicTrans2 free; Sarvam fallback about ₹30 per hour of speech |
| Cloud GPU worker | roughly ₹3,000–8,000 a month, only when the laptop can't keep up |
| Extra storage | about ₹1.3 per GB a month beyond the free 10 GB |
| WhatsApp (only if added) | per-message fees plus a provider's charges |

**Pricing anchors:** Indian editors charge ₹497–1,490 per Short on Fiverr, ₹300–1,000 for a basic cut, ₹800–5,000 with motion graphics, ₹5,000–25,000 a month for a Shorts pipeline, ₹20,000–45,000 a month full-time. ₹499–999 a month for unlimited edits of 8–20 stream hours sits well under all of these.

---

## 9. Risks and what we do about them

| Risk | Likelihood | What we do |
|---|---|---|
| **YouTube Studio's AI clip suggestions** are live in India and Hindi | Certain | They are transcript-based 1:1 trims with no 9:16, no ranking, no HUD reading. We win on screen events, markers, Hinglish, layouts, length presets and the phone studio. Watch Creator Insider monthly for the promised "clippable moments" on archived streams |
| **Eklipse fast-follow** (it has approve-then-post, voice markers, live auto-post, a phone app, and launched "Gameplay Intelligence" in 2026) | High | It lacks mobile-game detection and Hinglish, has a 2.3 Android rating, per-game paywalls and 1–5 hour processing complaints. Our answer: one flat price, a visible "why this clip", cuts that open on the action |
| **Streamlabs Ultra or vidIQ bundle clipping into bills streamers already pay** | Medium | Same answer; vidIQ says it is "not optimized for gameplay" |
| **Creators won't pay** | Medium–high | ₹99 first month; ₹49–99 per stream; first stream free; the pitch is stream growth, not Shorts income; editors as a second buyer |
| **Clips judged "plain" by the Hindi scene's meme-and-voiceover standard** | Medium | Ship the top-Shorts format by default (hook band, layouts, zoom); style pass in M8 |
| **Compilations flagged as inauthentic content** | Medium | Commentary clips, captions, chapters, varied hooks; never a silent montage |
| **Laptop offline, power cut, disk full** | High over months | Resumable jobs, cleanup, alerts, daily backups; cloud worker once revenue allows |
| **YouTube quota** (100 uploads a day and 10,000 units a day for the whole app) | Low at launch | Counters and alerts; compliance audit form before about 30 active creators |
| **Google's scope check or Razorpay KYC takes longer than expected** | Medium | Start both early; 100-tester list and YouTube Studio permissions as the manual fallback |
| **Game bans (BGMI and Free Fire have both been banned before)** | Low–medium | Free Fire and talk mode after launch, so the app isn't tied to one game |
| **Gemini free tier uses data** | Certain | Paid tier with a cap before any customer stream |
| **Too many Shorts hurting channels** | Unproven | Shorts-share gauge; weekly compilation; track Shorts share and subscribers per Short in beta |
| **Scope creep** | High | Anything not in section 4 goes to the later list, not into the build |

---

## 10. Launch checklist

- [ ] Three real 3-hour streams processed end to end in about 1 hour each
- [ ] 80%+ top-moment recall on 5 labelled streams; misses documented
- [ ] A marker-window upload from a phone on mobile data processes correctly
- [ ] A clip approved on a phone posts to a test channel at the scheduled minute, private-then-public, with the stream link
- [ ] Google sensitive-scope check passed
- [ ] Razorpay test subscription activates, renews and cancels; a per-stream link pays; live keys in place
- [ ] Legal pages live with the 30-day retention and consent wording; Razorpay accepts them
- [ ] Admin page, Telegram alerts and daily backups working; a restore tested
- [ ] Paid Gemini with a cap; cost per stream measured
- [ ] Beta creators posted real Shorts through the app; no critical bug open
- [ ] Landing page with demo clips (with permission) and testimonials
- [ ] Support path (email or Telegram) and a refund process written down

---

## 11. Things to check before relying on them

| Claim | Check |
|---|---|
| YouTube uploads from unreviewed apps can be public (2 Nov 2026 change) | One real test upload in M4; always set `privacyStatus` anyway |
| Two quota buckets (100 uploads a day; 10,000 units) | Quota page after the test upload |
| Shorts thumbnails via the API on a non-YPP channel | Try on the test channel; fall back to the auto frame |
| `streamList` works for a live `!clip` listener and shows Super Chat fields | Test on a live session in M4 |
| Studio's AI clip suggestions on a BGMI VOD: what they pick | Upload one test stream and compare with our picks, week 1 |
| Eklipse's exact feature list (its site blocked our reader) | A first-hand look from the phone session or a trial |
| Fewer Shorts help gaming channels (one correlational study) | Track Shorts share and subscribers per Short in beta |
| Zoom, speed ramps and music use in top Shorts (not visible from stills) | Watch 20 top clips by hand before S3 |
| Per-stream pricing uptake | Offer it in beta and count |
| Free Fire screen signals | Run 2–3 Free Fire streams through the pipeline before M8 |
| Personal ranking improves results | Compare with beta creators' own picks before selling it |

---

## 12. Later list (not in the build)

WhatsApp control surface (after paying users) · Instagram Reels · Valorant · Play Store wrapper · agency plan · sponsor deliverable tracker with GST invoices · community post drafts to copy into Studio · AI-edited thumbnails as a paid add-on · comment reply suggestions · phone OTP sign-in · music library · live overlays and multistreaming (never: Streamlabs owns live production) · our own A/B testing, dubbing, keyword research (never: YouTube and vidIQ give these) · YouTube link import, VOD download, chat-replay scraping (never: against YouTube's developer policies) · API-set related video, pinned comments, community posts (impossible: no API) · auto media kit (brand platforms pull YouTube data themselves) · Rooter and Loco (no APIs; Loco has left India as a priority) · esports-org sales motion and squad multi-POV (no buying evidence).
