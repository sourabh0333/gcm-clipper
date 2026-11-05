# GCM Clipper master plan

The single plan for building the complete, ready-to-sell app. Written 5 November 2026. It replaces the earlier step list and folds in all three research reports ([market validation](../reports/BGMI%20AI%20clipper%20market%20validation.md), [auto-posting and more games](../reports/AI%20clipper%20autoposting%20and%20multigame%20gaps.md), [what gaming YouTubers need](../reports/Gaming%20YouTuber%20content%20workflow%20needs.md)) and the [architecture](../docs/ARCHITECTURE.md). Progress is tracked in [ai-gcm/BUILD_NOTES.md](../ai-gcm/BUILD_NOTES.md).

"GCM Clipper" is the working name until the product name is chosen (decision D0).

---

## 1. What we are building

**One sentence:** a gaming content management app for Indian YouTubers that turns every livestream into ranked clips, lets the creator edit them on a phone, plans the week on a calendar, posts approved clips to their own YouTube channel on schedule, and learns from that channel's results.

**The loop it runs** (no competitor runs all of it for Hinglish gaming streamers):

```
 stream (creator marks moments live)
   → engine finds the best moments (game events + Hinglish talk + markers)
   → studio turns them into Shorts and a weekly compilation that point back to the stream
   → creator approves on the phone
   → posted to YouTube on the calendar
   → results feed the next ranking
```

**Principles**

1. **The creator approves everything that goes public.** Nothing posts on its own.
2. **Game-aware first.** Kills, clutches and wins are read from the screen; talk is read from Hinglish speech. Speech-only tools miss silent kills; we don't.
3. **Phone first.** Every creator action works on an Android phone over home Wi-Fi.
4. **Shorts are trailers for the stream.** The product's success measure is stream viewers and subscribers, not Shorts views.
5. **Don't rebuild what YouTube gives free** (title and thumbnail tests, dubbing, idea tools). Prepare inputs for them instead.
6. **₹0 until it earns.** Free tiers, the laptop as the first server, paid services only behind a cap.
7. **No creator passwords, ever.** Google sign-in only.
8. **Resumable and bounded.** Every long job survives a crash or power cut; disk use is capped.

**Who it is for**

| Segment | Fit | Note |
|---|---|---|
| Hindi/Hinglish BGMI streamers, 10k–500k subscribers, streaming horizontally (PC/OBS or phone screencast), paying an intern or editor or doing it themselves | **Primary** | Pain is highest; YouTube's free highlights don't cover their setup |
| Free Fire streamers | Second game, month 1 after launch | About 4× BGMI's Indian user base |
| GTA RP, Minecraft, horror streamers | "Talk mode", month 1–2 | Speech-driven; our Hinglish edge applies |
| Freelance gaming editors | Editor tier, month 1 | Buyers and the cheapest sales channel |
| Agencies and esports orgs | Later | Trinity Gaming, Sky Route, 8Bit and similar manage 200+ creators each |
| Creators under ~5k subscribers, vertical-only phone-app streamers, very large creators with teams | Not targeted | Won't pay, already served free, or already staffed |

---

## 2. Decisions

| # | Decision | Status |
|---|---|---|
| D0 | **Product name** (needed for the domain, the Google sign-in consent screen and legal pages) | **Open. Needed before milestone M2.** |
| D1 | Own brand, not under Cevrynt; seller is the owner as a sole proprietor (PAN, bank account, free Udyam registration); a company only if it takes off | Decided 4 Nov |
| D2 | Plans: **Starter ₹499** (8 stream hours a month), **Pro ₹999** (20 hours, results page), **Editor ₹2,499** (several channels, editor seats, client approval) after launch; **₹99 first month** instead of a free trial; first stream free | Decided 4 Nov |
| D3 | Laptop is the first server; cloud GPU worker once revenue covers it | Decided 4 Nov |
| D4 | Video in: resumable upload (main path) and YouTube link (creator's own streams, their responsibility under the terms) | Decided 4 Nov |
| D5 | YouTube only at launch; Instagram optional later if creators ask | Decided 4 Nov |
| D6 | Build the full app before contacting streamers; revenue may come slowly | Decided 4 Nov |
| D7 | Google sign-in only at launch (phone OTP needs a paid SMS service) | Decided 4 Nov (architecture) |

---

## 3. User journeys

**Creator, first week**

1. Opens the site on the phone, taps "Continue with Google". Sees the plan page: first stream free, then ₹99 for the first month.
2. Adds their channel: "Connect YouTube" (Google asks for upload and analytics permission). Sets game = BGMI, caption style, logo.
3. Before the next stream, installs the app to the home screen and opens the **Live** screen: a big "Mark moment" button. Also sets a chat command `!clip` for mods.
4. After the stream, uploads the recording (resumable, can continue after a dropped connection) or pastes the stream link.
5. Gets a notification 1–3 hours later: "14 clips ready". Swipes: keep or reject. Marked moments are always in the list.
6. Opens one clip in the studio, drags the start earlier, picks the "facecam top" layout, approves the hook text.
7. Taps "Post this?" on 5 clips. They land on the calendar, one every evening at 7 pm, each linked to the stream. The weekly compilation is suggested for Sunday.
8. During the week, gets "Posted" and, once, "Post failed, retrying" messages. Sees "Your channel" showing which clip types did best.

**Editor (month 1 after launch)**

1. Has an Editor plan with 3 client channels. Each client connected their own YouTube and can revoke it.
2. Edits clips for client A; sends an approval link. Client A approves from WhatsApp on their phone; the clip posts to A's channel.

**Owner (you), daily**

1. Opens the admin page: jobs in queue, failures, payments, disk space. Retries one failed job. Everything else runs itself.

---

## 4. Feature specification

Each module lists what it does and when it is "done". Numbers in brackets are the plan steps the build notes track.

### 4.1 Capture

| Feature | Behaviour | Done when |
|---|---|---|
| **Moment markers** (3a) | Live screen with a large button; chat command (`!clip`, configurable) read from the stream's chat; spoken phrase ("clip that") found in the transcript. Each marker is a strong ranking signal and always produces a clip; markers are shown on the clips they made | A marker tapped during a real stream appears as a clip with "you marked this" |
| **Upload** (4) | Resumable chunked upload from phone or PC, up to 8 GB; shows progress and time left; survives a dropped connection; optional "shrink to 720p before upload" helper for PC | A 2 GB file uploads from a phone over Wi-Fi and resumes after airplane mode |
| **Link import** (4) | Paste a YouTube link to the creator's own stream; the terms make the creator responsible; a section can be chosen | Works for public and unlisted streams |
| **Stream details** | Game, title, date, markers, chat replay (if available) attached to the job | Shown on the job page |

### 4.2 Engine

| Feature | Behaviour | Done when |
|---|---|---|
| **Full-length streams** (1) | 3–5 hour streams run end to end; vision and transcript resume from checkpoints; sources deleted 14 days after clips are made | Three real 3+ hour streams processed with no manual fixes; a killed job resumes |
| **Speed** (2) | Vision, sounds and transcript run in parallel; HUD read less often in quiet stretches; download only the needed section | A 3-hour stream in about 1 hour on the laptop |
| **Accuracy** (3) | Tested on 10 more streams; knock detection; bigger speech model when a transcript looks broken; talk-vs-fight weights tuned from swipes; every miss written down | A labelled check on 5 streams: 80%+ of hand-picked top moments found |
| **BGMI events** | Eliminations and Remaining counters, Spectating handling, chicken dinner, accolades, knocks | Existing, kept under test |
| **Talk moments** | Laughter, screams, loudness, banter and roast words, Gemini reading the transcript | Existing; Gemini on with a spending cap |
| **Clip labels** (7) | Type (kill, multi-kill, clutch, win, funny, rage, banter, marked), game, length, score, players left, and later post results | Stored for every clip |
| **Post-ready output** (6) | Clean Hinglish title options, 3–5 hashtags, description with stream link and Krafton line, no watermark, no added music | Every clip ships with all of these |
| **Brand-safe and promise check** (6) | Flags swearing in titles, slurs, betting or real-money-gaming mentions, other games' logos, and a title that promises what the first seconds don't show | Flags shown on the clip; sponsor-safe filter in the library |

### 4.3 Review

| Feature | Behaviour | Done when |
|---|---|---|
| **Swipe queue** | One clip at a time, keep or reject, undo, sound toggle, reasons shown; batch keep | Existing; decisions saved per clip |
| **Reject reasons** | Optional one-tap reason (bad cut, not interesting, wrong moment) | Fed back into tuning |

### 4.4 Studio

| Feature | Behaviour | Done when |
|---|---|---|
| **Edit model** (5) | A clip is an edit list (cuts, layout, zoom, captions, text, brand kit) on top of the source; preview in the browser; render only on export; undo | An old clip reopens as an editable project |
| **Library** (S1) | All clips from all streams; filter by stream, game, type, status, flag; search by what was said | 100+ clips browse smoothly on a phone |
| **Editor basics** (S2) | Trim, split, join, timeline, speed up dead parts, instant preview | A clip re-cut in under a minute on a phone |
| **Gaming layouts** (S3) | Facecam top + gameplay (auto-detected facecam box, adjustable), full gameplay, blur fill; **zoom on the kill** at the known kill time; kill feed kept visible | Correct on all 3 test streams and 3 new ones |
| **Captions and hook** (S4) | Style presets (font, colour, size, position, word highlight), Hinglish or Devanagari, word editing; AI-suggested hook line in the first 2 seconds | Looks right on vertical and landscape sources |
| **Brand kit** (S5) | Logo, colours, caption style, intro and outro, standard description, hashtags, game disclaimer, applied automatically | Set once, used on every export |
| **Thumbnails and titles** (S6) | Frame pick, facecam cut-out (free background removal), big text; 3 titles + 3 thumbnails for long videos, ready for YouTube's Test & Compare | Every long video has 3 and 3 |
| **Weekly compilation** (S7) | "Best of this week" 16:9 with chapters, auto-suggested each week; manual pick too; 9:16 long Short option | A 5-minute compilation renders from 10 clips |
| **Sound safety** (S9) | No added music; royalty-free SFX only; warning when background music may trigger a claim | No added track can cause a claim |
| **Export** (8) | Download one or all (zip), share from phone, copy title and description | Works on Android Chrome |

### 4.5 Plan

| Feature | Behaviour | Done when |
|---|---|---|
| **Content calendar** (S8) | Week and month views; scheduled, posted, failed; drag to move; "fill this week" with approved clips | Plan a week in a few taps |
| **Shorts-share gauge** (S8) | Shows Shorts as a share of uploads, warns above about 20% | Visible on the calendar |
| **Stream schedule** (43) | Planned streams on the calendar; teaser Short suggested before each | Month 1–2 after launch |

### 4.6 Post

| Feature | Behaviour | Done when |
|---|---|---|
| **Connect YouTube** (19) | Google OAuth with upload and analytics scopes; refresh token encrypted; disconnect deletes it; Google's sensitive-scope check passed | A creator connects and disconnects; check passed |
| **"Post this?" approvals** (20) | Every kept clip asks; edit title and description first; batch approve | Nothing posts without a recorded approval |
| **Calendar posting** (21) | Approved clips upload as private with YouTube's scheduled publish time; thumbnail, title, description, hashtags from the studio; defaults like "one at 7 pm" | A scheduled Short goes public at the planned minute |
| **Stream funnel pack** (21) | Related Video link to the stream recording or next live stream (if the API allows), stream link in description and pinned comment, "live at 8 PM" teaser Short, "join the stream" end card | Every Short links back to the stream |
| **Status and safety** (22) | Posted, scheduled, failed with retry, alert on failure, daily-cap counter, never the same clip twice to one channel | A forced failure shows up and retries |
| **Your channel** (23) | Recent Shorts and their views next to the new clips (YouTube Analytics, read-only) | Shown on the job page |

### 4.7 Learn

| Feature | Behaviour | Done when |
|---|---|---|
| **Your results** (35) | Better or worse than the channel's usual by clip type and length; outliers; subscribers per Short; Shorts share; average live viewers by month | Once creators have 10+ posted clips |
| **Personal ranking** (36) | Push up clip types that worked for this creator, combined with swipes; checked against beta creators' own picks | After the results page |

### 4.8 Accounts and billing

| Feature | Behaviour | Done when |
|---|---|---|
| **Sign-in** (12) | Google only; secure cookie session; each creator sees only their own data | Two accounts cannot see each other's jobs |
| **Plans and usage** (15, 16) | Stream hours per plan; clear message at the limit; first stream free; ₹99 first month | Limits enforced |
| **Payments** (15) | Razorpay Subscriptions with UPI AutoPay; webhook updates the plan; invoices; cancel any time | A test subscription activates, renews and cancels |
| **Editor tier** (41) | Seats, several channels, client approval link | Month 1 after launch |

### 4.9 Admin, operations, trust

| Feature | Behaviour | Done when |
|---|---|---|
| **Admin page** (28) | Users, jobs, posts, failures, payments, disk; retry; refund link | Everything above visible |
| **Monitoring** (29) | Phone alert when a job or post fails or the laptop goes offline; daily summary | Alerts arrive within 5 minutes |
| **Backups** | Database and brand kits backed up daily to free cloud storage; restore tested | A restore from backup works |
| **Security** | HTTPS only, encrypted tokens, rate limits, secrets in `.env`, dependency updates | A review checklist passed before beta |
| **Legal** (26, 27) | Privacy policy, terms, refund policy, AI processing consent, Google data-use disclosures; game publishers' rules documented | Live on the site; Razorpay accepts them |
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
| Storage | Per-job folders on the laptop; sources 14 days, clips 30 days; Cloudflare R2 later |
| Access | Cloudflare Tunnel to the laptop; static files on Cloudflare Pages |
| Sign-in | Google OpenID Connect; YouTube scopes requested separately |
| Payments | Razorpay Subscriptions |
| AI | Gemini (paid, capped) for judging and talk; local models for speech, sounds, OCR |

**Data model (main tables)**

`users`, `channels` (YouTube connection, encrypted token), `brand_kits`, `streams` (job, source, game, markers, status), `moments`, `clips` (labels, scores, flags, decision), `edits` (edit list per clip, versions), `compilations`, `calendar_entries`, `posts` (YouTube video id, schedule, status, attempts), `post_stats` (daily analytics snapshots), `subscriptions`, `payments`, `editor_memberships`, `approvals`, `audit_log`.

**Quality bar for every milestone**

- Unit tests for every module; the suite stays green (`python -m pytest`).
- A real-stream check for any pipeline change.
- Phone check in Chrome on Android for any screen change.
- Notes updated, committed and pushed.

---

## 6. Build order

Milestones are gated by their "done when", not by dates. The week numbers are estimates for a full-time build with Claude doing the code; a milestone that slips moves the rest.

| Milestone | Scope | Done when | Weeks |
|---|---|---|---|
| **M0 Foundation** | Architecture; resume from checkpoints; cleanup | Done 4–5 Nov | — |
| **M1 Engine product-grade** | Full streams, speed, accuracy on 10 streams, markers (file-based first), labels, post-ready output, brand-safe check | Three 3-hour streams end to end in about 1 hour each; 80%+ top-moment recall on 5 labelled streams | 1–3 |
| **M2 Platform core** | Database and models, API, worker queue, Google sign-in, resumable upload, new web app with jobs, progress, review (replaces the current server and PWA) | Two creators can sign in, upload, and review their own streams; the old app is retired | 4–5 |
| **M3 Studio** | Edit model, library, editor, layouts and zoom, captions and hook, brand kit, thumbnails and titles, compilation, sound safety, export | Every 4.4 "done when" met; phone-tested | 6–8 |
| **M4 Plan and post** | Calendar, Shorts-share gauge, YouTube connect, approvals, scheduled posting, funnel pack, status and alerts, your-channel view | A clip approved on the phone posts to a test channel at the scheduled minute with the stream link; Google's scope check submitted | 9–10 |
| **M5 Service** | Domain, Cloudflare Pages and Tunnel, Razorpay plans and webhooks, usage limits, email notifications, storage lifecycle | A test subscription activates and renews; limits enforced; the app reachable from mobile data | 11 |
| **M6 Trust and ops** | Legal pages, admin page, monitoring, backups, security checklist, paid Gemini with cap, landing page | All 4.9 "done when" met | 12 |
| **M7 Beta and launch** | Closed beta: 5 streamers plus 1 editor for 2 weeks; fixes; testimonials; open sales | Beta creators post real Shorts through the app; no unresolved critical bug | 13–14 |
| **M8 After launch** | Free Fire; talk mode; results page; personal ranking; editor tier; media kit; stream schedule; chat spikes; cloud worker when revenue allows | Rolling, month 1–3 | 15+ |

**Dependencies:** M2 needs D0 (name) for the sign-in consent screen. M4 needs the domain and privacy policy (M5/M6 items are pulled forward for the Google check). M5 needs Razorpay KYC, which can take days, so it starts in week 1.

---

## 7. What only you can do

| When | Task | Why |
|---|---|---|
| Week 1 | Choose the product name (D0) | Domain, consent screen, legal pages |
| Week 1 | Udyam registration (free), then start Razorpay KYC | Can take days to approve |
| Week 1 | Create a test YouTube channel | For posting tests before any creator is involved |
| Week 1–2 | Review clips strictly; try the live marker button during a real session | Tunes ranking and markers |
| Week 4 | Buy the domain; create Cloudflare and Google Cloud accounts; set up the Google sign-in consent screen with the prepared text | Sign-in and hosting |
| Week 9 | Submit Google's sensitive-scope check with the prepared answers and demo video | YouTube posting for anyone outside the test list |
| Week 11 | Razorpay live keys; email service account | Payments and notifications |
| Week 12 | Approve the legal pages; add a card to Google AI Studio with the cap | Launch |
| Week 13 | Invite 5 streamers and 1 editor | Beta |

Claude prepares every form answer, policy text and demo video script. You only sign up, paste and approve.

---

## 8. Costs

| Before the first sale | Cost |
|---|---|
| Hosting, sign-in, database, storage, email, tunnel (free tiers) | ₹0 |
| Domain | about ₹800–1,000 a year |
| Google scope check, YouTube posting | ₹0 |
| Razorpay | ₹0 upfront, about 2% per payment |
| Total | **about ₹1,000** |

| After customers pay | Cost |
|---|---|
| Paid Gemini | a few rupees per stream (measured in M1) |
| Cloud GPU worker | roughly ₹3,000–8,000 a month, only when the laptop can't keep up |
| Extra storage | about ₹1.3 per GB a month beyond the free 10 GB |
| Instagram posting service (only if added) | free for 2 accounts, then about ₹530 per account a month |

---

## 9. Risks and what we do about them

| Risk | Likelihood | What we do |
|---|---|---|
| **YouTube ships free "clippable moment" suggestions for archived streams** (promised for late 2026) | High | Win on what YouTube doesn't do: game events, markers, Hinglish, gaming layouts, funnel, approvals, per-channel learning. Watch Creator Insider monthly |
| **Streamlabs Ultra or vidIQ bundle clipping into bills streamers already pay** | Medium | Same answer; plus the editor tier and compilations they don't offer |
| **Creators won't pay** | Medium–high | ₹99 first month; first stream free; the pitch is stream growth and sponsor readiness, not Shorts income; editors as a second buyer |
| **Clip quality disappoints in the first session** | Medium | M1's accuracy gate before any creator sees it; markers guarantee the moments they care about |
| **Laptop offline, power cut, disk full** | High over months | Resumable jobs, cleanup, alerts, daily backups; cloud worker once revenue allows |
| **YouTube terms on downloading links** | Medium | Upload is the main path; link import is the creator's own stream and their responsibility under the terms |
| **YouTube upload quota (100 a day for the app)** | Low at launch | Counter and alert; quota-extension form before 30 creators |
| **Google's scope check or Razorpay KYC takes longer than expected** | Medium | Start both early; test-user list and YouTube Studio permissions as the manual fallback |
| **Game bans (BGMI, Free Fire have both been banned before)** | Low–medium | Free Fire and talk mode after launch, so the app isn't tied to one game |
| **Gemini free tier uses data** | Certain | Paid tier with a cap before any customer stream |
| **Too many Shorts hurting channels** | Unproven | Shorts-share gauge; weekly compilation; track Shorts share and subscribers per Short in beta |
| **Scope creep** | High | Anything not in section 4 goes to the "later" list, not into the build |

---

## 10. Launch checklist

- [ ] Three real 3-hour streams processed end to end in about 1 hour each
- [ ] 80%+ top-moment recall on 5 labelled streams; misses documented
- [ ] A clip approved on a phone posts to a test channel at the scheduled minute with the stream link
- [ ] Google sensitive-scope check passed
- [ ] Razorpay test subscription activates, renews and cancels; live keys in place
- [ ] Legal pages live; Razorpay accepts them
- [ ] Admin page, alerts and daily backups working; a restore tested
- [ ] Paid Gemini with a cap; cost per stream measured
- [ ] Beta creators posted real Shorts through the app; no critical bug open
- [ ] Landing page with demo clips (with permission) and testimonials
- [ ] Support path (email or WhatsApp) and a refund process written down

---

## 11. Things to check before relying on them

| Claim | Check |
|---|---|
| YouTube uploads from unreviewed apps can be public (2 Nov 2026 change) | One real test upload, M4 |
| 100 uploads a day for the whole app | Quota page after the test upload |
| YouTube's free live highlights: who gets them, screencast or OBS in India | Stream a test BGMI session both ways, week 1 |
| The API can set a Short's Related Video link | Try on the test channel before M4 |
| Fewer Shorts help gaming channels (one correlational study) | Track Shorts share and subscribers per Short in beta |
| Free Fire screen signals | Run 2–3 Free Fire streams through the pipeline before M8 |
| Personal ranking improves results | Compare with beta creators' own picks before selling it |

---

## 12. Later list (not in the build)

Instagram Reels (posting service, then direct after Meta review) · Valorant · Play Store wrapper · organisations plan · sponsor deliverable tracker with GST invoices · Tamil and Telugu captions · community post drafts · AI-edited thumbnails as a paid add-on · comment reply suggestions · phone OTP sign-in · music library · voice-over · live overlays and multistreaming (never: Streamlabs owns live production) · our own A/B testing, dubbing, keyword research (never: YouTube and vidIQ give these).
