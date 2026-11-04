# GCM Clipper: plan to a ready-to-sell app

Written 4 November 2026, updated the same day with approval-based posting, learning from past posts, more games, and the full content-management workflow. The research behind the update is [AI clipper autoposting and multigame gaps](../reports/AI%20clipper%20autoposting%20and%20multigame%20gaps.md).

**What the product is:** a **gaming content management app** for YouTubers. One place for the whole workflow, from a finished stream to posted videos:

| Stage | What the app does |
|---|---|
| **1. Clip** | Finds the best moments in each stream (kills, clutches, funny talk, rage) and cuts ranked 9:16 clips |
| **2. Edit** | A phone-friendly editor built for gaming clips: trim, layout, zoom on the action, caption styles, hook text, brand kit, thumbnails; plus compilations from many clips |
| **3. Plan** | A library of every clip across all streams, and a content calendar to plan what goes out when |
| **4. Post** | Asks "Post this?", then schedules and posts to the creator's YouTube channel, with status and failure alerts |
| **5. Learn** | Shows what worked on the channel and pushes similar clips up next time |

**YouTube is the main platform** (owner's decision, 4 Nov); Instagram is optional, after launch, if creators ask. After launch, contact streamers.

**Estimate: about 11 weeks of building to launch**, then Free Fire and other games in the month after. This assumes you can do the account sign-ups and decisions in the "You" column within a day or two each time. Claude writes the code, tests and docs.

---

## What the research changed

- **Posting after approval is needed, but it won't win sales on its own.** OpusClip, Vizard, Klap, Reap and Eklipse already post to Shorts and Reels on their $15–39 a month plans. Creators complain about bad clips, not about uploading. So posting is part of the base product, and clip quality stays the main job.
- **YouTube posting became cheap two days ago** (2 Nov 2026): uploads from new, unreviewed apps no longer stay private, and an upload costs 1 unit from a separate allowance of 100 uploads a day for the whole app (about 33 creators at 3 Shorts a day). This is two days old, so it gets tested with one real upload first.
- **Instagram needs paperwork:** Meta App Review plus Business Verification, which needs proof of a business (for a sole proprietor, documents such as Udyam or GST registration). Since YouTube is the main platform, Instagram moves after launch (step 37) and only if creators ask.
- **Access to a creator's channel is always through "Sign in with Google"**, never their password. Shared passwords break with 2-step verification, can get the account flagged, and make you responsible for anything that goes wrong. For a manual beta before the app's sign-in is ready, a creator can add you in YouTube Studio → Settings → Permissions, which needs no password. Clips are always posted on the creator's own channel, never re-uploaded to yours.
- **Learning from past posts is the real gap, but only one kind:** re-rank today's clips by what worked for this creator before (kills, clutches, funny talk, rage; which game). Nobody does this with game-event labels. It needs 10+ posted clips per creator first, so it comes after launch. "Best time to post" has weak evidence for Shorts; generic virality scores are mistrusted.
- **Free Fire comes next:** about 77.4M monthly users in India against BGMI's 20.8M, relaunched as Free Fire India on 28 Oct 2026, and its kill and win banners work like BGMI's. A "talk mode" then covers GTA V roleplay, Minecraft and horror games using the funny-moment pipeline that already exists.
- **Skip:** TikTok (banned in India), Moj/Josh/ShareChat posting (no public API; download and share only), fully automatic posting without approval (YouTube's "inauthentic content" and Instagram's originality rules), generic virality scores, a "best time" engine, built-in A/B tests (Instagram's Trial Reels does it free).

---

## What "ready to sell" means

A creator can:

1. Sign up with Google or a phone OTP on the website or the installed app.
2. Start a free trial stream: paste a YouTube link or upload a recording, and pick the game.
3. Get ranked 9:16 clips with Hinglish captions, clean titles and hashtags within a few hours, with a notification.
4. Swipe to keep or reject.
5. Edit any clip on the phone or laptop: trim and split, facecam and gameplay layout, zoom on the kill, caption style, hook text at the start, their own logo and outro, pick a thumbnail frame. Or make a compilation ("Top 10 kills this week") from several clips.
6. Find any clip later in the **library** (filter by stream, game, type, status), and see the week on a **content calendar**.
7. Connect their YouTube channel once with "Sign in with Google". Each finished clip asks **"Post this?"**. Approved clips go onto the calendar and post at the planned times, with a clear status and an alert if a post fails.
8. See a "your results" page: which kinds of clips did best as Shorts.
9. Pay monthly by UPI AutoPay, see stream hours left, cancel any time.

And you can:

10. See every user, job, post, failure and payment on an admin page.
11. Leave it running for a week without touching it.

---

## Decisions needed from you first

| # | Decision | Options | Suggestion |
|---|---|---|---|
| D1 | Brand and seller | A separate product with its own name. The seller behind it can be **you as a sole proprietor**, or a **new company** later | **Its own brand, not Cevrynt** (owner's decision, 4 Nov). Start as a sole proprietor (PAN, bank account, free Udyam registration) for Razorpay; register a company only if the product takes off |
| D2 | Price | The validation plan offers ₹499 and ₹999 per 4 weeks | **Starter ₹499** (about 8 stream hours a month, YouTube posting) and **Pro ₹999** (about 20 hours, YouTube posting, results page), first stream free. Rivals with posting charge about ₹1,300–3,500 a month |
| D3 | Where processing runs at launch | **Laptop** (free, roughly 30–40 creators, must stay on) or **cloud server** (always on, costs monthly from day one) | Laptop first, cloud once revenue covers it (step 32) |
| D4 | Video source | YouTube link only, or also file upload | Both. Downloading from YouTube is against YouTube's terms, even for the creator's own videos; upload is the safe path |
| D5 | Platforms | YouTube only at launch, or YouTube and Instagram | **YouTube only at launch** (owner's decision, 4 Nov). Instagram after launch if creators ask (step 37) |

---

## Phase 1: Make the engine product-grade (weeks 1–2, ₹0)

| Step | What | Who | Done when |
|---|---|---|---|
| 1 | **Full-length streams:** 3–5 hour streams end to end, in chunks, resume after a crash or power cut, delete the source after clips are made. | Claude | Three full real streams processed with no manual fixes |
| 2 | **Speed:** run vision, audio and transcript at the same time, read the HUD less often in quiet stretches. Target a 3-hour stream in about 1 hour on the laptop (now 1–3 hours). | Claude | Measured on a 3-hour stream |
| 3 | **Accuracy:** test on 10 more streams. Knock detection, the bigger speech model when a transcript looks broken, tune talk vs fight ranking from your swipes. | Claude, you review clips | Each stream checked; misses written down |
| 4 | **File upload** from phone or PC, in parts if large, as well as pasting a link. | Claude | A 2 GB file uploads from a phone |
| 5 | **Edit data model:** store every clip as a list of edits on top of the source (cuts, layout, zoom, captions, overlays), so edits are fast, undoable and re-rendered only on export. The editor itself is Phase 1b. | Claude | Old clips open as editable projects |
| 6 | **Post-ready output:** clean Hinglish title (no swear words in titles, which limits ads), 3–5 hashtags, the "not endorsed by Krafton" line for BGMI descriptions, no GCM watermark, no added music. | Claude | Every clip has a ready title, hashtags and description |
| 7 | **Clip labels for learning later:** save each clip's type (kill, multi-kill, clutch, funny, rage, banter), game, length and score, and later its posting results. | Claude | Stored for every clip |
| 8 | **Delivery:** download one clip or all as a zip, share from the phone (also covers Moj, Josh and ShareChat by hand). | Claude | Works on Android Chrome |

## Phase 1b: Content studio, the management part (weeks 3–5, ₹0)

Indian gaming creators edit Shorts today in phone apps like VN and InShot (CapCut is banned in India) or pay an editor. The studio doesn't try to copy those general editors. It does the edits gaming clips need, fast, on a phone, with the AI doing the first pass.

| Step | What | Who | Done when |
|---|---|---|---|
| S1 | **Clip library:** every clip from every stream in one place; filter by stream, game, type (kill, clutch, funny…), status (new, kept, edited, scheduled, posted, rejected), date; search by what was said | Claude | 100+ clips browse smoothly on a phone |
| S2 | **Editor basics:** trim, split and join, change start and end on a timeline, speed up dead parts, preview instantly | Claude | A clip is re-cut in under a minute on a phone |
| S3 | **Gaming layouts:** facecam on top and gameplay below (auto-detect the facecam box, adjustable), full gameplay, blur fill; **zoom on the kill** using the kill time the AI already knows; keep the kill feed visible | Claude | Each layout renders correctly on all 3 test streams |
| S4 | **Captions and text:** caption style presets (font, colour, size, position, word highlight), Hinglish or Devanagari, edit words; a **hook line** in the first 2 seconds ("1v4 clutch 😱"), AI-suggested | Claude | Styles look right on vertical and landscape sources |
| S5 | **Brand kit:** creator's logo, colours, caption style, intro and outro clips, standard description, hashtags and game disclaimer, applied to every clip automatically | Claude | Set once, used on every export |
| S6 | **Thumbnails and titles:** pick a frame, add big text; AI title options in Hinglish (clean, no swear words) | Claude | Every clip has a thumbnail and 3 title options |
| S7 | **Compilations:** pick several clips (or "best 10 of this week") and make one longer video, 16:9 for a normal YouTube upload or 9:16 for a long Short, with transitions and chapter titles | Claude | A 5-minute "best of the week" renders from 10 clips |
| S8 | **Content calendar:** week and month view of scheduled and posted videos; drag to move; empty-day warnings; "fill this week" places approved clips one a day | Claude | Plan a week in a few taps |
| S9 | **Sound safety:** no added music by default; optional sound effects only from a royalty-free set; warn when game or background music might trigger copyright claims | Claude | No added track can cause a claim |

Kept out at launch (add if creators ask): music library, stickers and effects packs, voice-over recording, team accounts for creator plus editor, multi-channel management.

## Phase 2: Turn it into a service (weeks 6–7, first small costs)

| Step | What | Who | Cost |
|---|---|---|---|
| 9 | **Domain**, a new `.com` or `.in` for the product's own name | You buy or confirm, Claude sets it up | About ₹800–1,000 a year |
| 10 | **Website and app hosting** on Cloudflare Pages: HTTPS, installable app, sharing works | You make a free Cloudflare account, Claude deploys | ₹0 |
| 11 | **Laptop connected safely** through Cloudflare Tunnel | Claude | ₹0 |
| 12 | **Accounts:** Google login and phone OTP; each creator sees only their own streams (Supabase free tier) | You make a free Supabase account, Claude builds | ₹0 up to 50,000 users |
| 13 | **Job queue:** many creators submit; streams run in order, with "your stream is 3rd in line" | Claude | ₹0 |
| 14 | **Clip storage** on Cloudflare R2, auto-deleted after 30 days (posted clips stay on the platforms) | Claude | ₹0 up to 10 GB |
| 15 | **Payments:** Razorpay subscriptions with UPI AutoPay, plans from D2, free first stream | **You do Razorpay KYC**, Claude builds | About 2% of each payment |
| 16 | **Usage limits** per plan | Claude | ₹0 |
| 17 | **Notifications:** email when clips are ready, a post went live, or something failed | You make the account (Brevo or Resend free tier), Claude builds | ₹0 |

## Phase 3: Posting to YouTube after approval (week 8)

| Step | What | Who | Cost |
|---|---|---|---|
| 18 | **Test YouTube's new rule first:** upload one test Short from a test Google project and confirm it goes public; check the quota page | Claude, with your test YouTube channel | ₹0 |
| 19 | **Connect YouTube with "Sign in with Google"** (no passwords): creator signs in once and can disconnect any time. Google's free "sensitive scope" check (about 3–5 business days, needs the domain, privacy policy and a demo video); until it passes, sign-in shows a warning and works only for listed test users, which is fine for the beta. Follow Google's user data rules: use the access only for approved uploads and scheduling, store it encrypted, delete it on disconnect | You submit with Claude's prepared answers, Claude builds | ₹0 |
| 20 | **"Post this?" approvals:** every kept clip asks; approve one by one or a batch; edit title and description before approving | Claude | ₹0 |
| 21 | **Calendar posting:** approved clips and compilations go onto the content calendar (S8) and are uploaded with YouTube's own scheduled publish time; "1 Short a day at 6 pm" style defaults, no best-time engine; thumbnail, title, description and hashtags from the studio | Claude | ₹0 |
| 22 | **Post status and safety:** posted, scheduled, failed with retry; alert on failure; daily-limit counter; never repost the same clip to the same channel | Claude | ₹0 |
| 23 | **"Your channel" basics:** show the creator's recent Shorts and their views next to the clips, so they see what's already working (read-only, from YouTube Analytics) | Claude | ₹0 |
| 24 | **Manual beta path:** until step 19's check passes, a beta creator can add you in YouTube Studio → Permissions instead | You, with the creator | ₹0 |

## Phase 4: Trust and launch (weeks 9–10)

| Step | What | Who | Cost |
|---|---|---|---|
| 25 | **Paid Gemini for customer streams** (free tier lets Google use the data), with a spending cap | You add a card in Google AI Studio, Claude sets the cap | Estimate: a few rupees per stream |
| 26 | **Legal pages:** privacy policy, terms (creator must own the stream; posting only after their approval), refund policy, AI processing consent, and the disclosures Google requires for YouTube data | Claude drafts, **you approve** | ₹0 to draft |
| 27 | **Game and platform terms:** Krafton, Garena, Rockstar, Mojang and YouTube rules on clips and auto-posting | Claude researches, you decide | ₹0 |
| 28 | **Admin page:** users, jobs, posts, failures, payments, retry, refund link | Claude | ₹0 |
| 29 | **Monitoring:** phone alert when a job or post fails or the laptop goes offline | Claude | ₹0 |
| 30 | **Landing page:** demo clips (with permission), pricing, sign-up | Claude builds, you approve | ₹0 |
| 31 | **Closed beta:** 5 streamers for 2 weeks, free; fix what they hit; 2–3 testimonials; compare their own picks with the app's ranking | You invite, Claude fixes | ₹0 |

## Phase 5: After launch (month 1–3)

| Step | What | When |
|---|---|---|
| 32 | **Cloud worker with a GPU**, so it doesn't depend on the laptop | When the queue often waits hours, or revenue covers roughly ₹3,000–8,000 a month (estimate) |
| 33 | **Free Fire MAX / Free Fire India** as the second game: kill, squad-wipe and Booyah detection, trained on a few hundred labelled frames from real streams | Month 1 after launch |
| 34 | **Talk mode for any game** (GTA V roleplay, Minecraft, horror, party games): speech, laughter, loudness and the AI judge, no game detector | Month 1 after launch |
| 35 | **"Your results" page:** from YouTube Analytics, which clip types got the best watch-through and views as Shorts | Once creators have 10+ posted clips each |
| 36 | **Personal ranking:** push up the kinds of clips that worked for this creator, combined with their keep/reject swipes | After step 35, checked against beta creators' own picks |
| 37 | **Instagram Reels (optional):** first through a posting service Meta has already approved (Zernio: free for 2 accounts, then about ₹530 per account a month, vendor price not checked), then direct after Meta Business Verification and App Review as a sole proprietor | Only if creators ask |
| 38 | **Valorant** (very standard HUD, open tools exist) | When PC creators ask |
| 39 | **Play Store app** (the installed web app wrapped for Android) | Optional; about ₹2,100 one-time Google fee |
| 40 | **Organisations plan** (esports teams, agencies): several channels under one account | If organisations show interest |

---

## Costs before the first sale

| Item | Cost |
|---|---|
| Hosting, login, database, storage, email, tunnel (free tiers) | ₹0 |
| Domain | About ₹800–1,000 a year |
| YouTube posting and Google's scope check | ₹0 |
| Razorpay | ₹0 upfront, about 2% per payment |
| Paid Gemini for customer streams | A few rupees per stream, from the first paying customer |
| Play Store (optional) | About ₹2,100 one time |

So the app can still be built and launched for **about ₹1,000** (the domain). Real costs start once creators pay: paid Gemini, later the cloud worker, and Instagram posting only if it's added.

---

## Check before building on it

These come from thin or very new sources; each has a cheap check, built into the steps above.

| Claim | Check |
|---|---|
| YouTube uploads from unreviewed apps can be public (2 Nov 2026) | Step 18: one real test upload |
| Upload quota of 100 a day for the app | Step 18: read the quota page in Google Cloud Console |
| Instagram limits, Meta verification time, posting-service prices | Only if Instagram is added (step 37) |
| Free Fire screen signals and effort | Run 2–3 Free Fire streams through the current pipeline before step 33 |
| Personal ranking improves views | Compare with beta creators' own picks (step 31) before selling it as a feature |

## Limits to know

- **The laptop is the server at first.** If it's off or offline, processing stops (already scheduled YouTube posts still go out, since YouTube publishes them). About 30–40 creators maximum until step 32.
- **YouTube's 100 uploads a day is for the whole app,** about 33 creators at 3 Shorts a day. Beyond that, Google's quota-extension form.
- **Posting doesn't sell the product on its own.** The research is clear that creators judge clip quality first. Steps 1–3 matter more than steps 18–24.
- **Accounts only you can create:** domain, Cloudflare, Supabase, Razorpay (KYC), Google Cloud project for YouTube sign-in, Google AI Studio billing, email service, Play Store. Claude can't sign up or enter payment or ID details for you. Start Razorpay KYC in week 1, since it can take days.

## Risk of building before asking streamers

Eleven weeks of building happens before any streamer says what they want. A free way to reduce this: during Phase 1, send your own clips to 3–5 streamers you know and ask "would you post these?" and "would you let an app post them for you after you approve?".

---

## Week-by-week summary

| Week | Dates | Build | You |
|---|---|---|---|
| 1 | 4–10 Nov | Steps 1–2 (full streams, speed) | Decide D1–D4. Start Razorpay KYC (Udyam registration first if needed). Create Cloudflare and Supabase accounts |
| 2 | 11–17 Nov | Steps 3–8 (accuracy, upload, edit data model, post-ready output, labels, delivery) | Review test clips strictly |
| 3 | 18–24 Nov | Studio S1–S3 (library, editor basics, gaming layouts and zoom) | Try the editor on your phone, say what feels slow |
| 4 | 25 Nov – 1 Dec | Studio S4–S6 (caption styles and hook text, brand kit, thumbnails and titles) | Send a logo and outro for testing |
| 5 | 2–8 Dec | Studio S7–S9 (compilations, content calendar, sound safety) | Plan a test week on the calendar |
| 6 | 9–15 Dec | Steps 9–13 (domain, hosting, tunnel, login, queue) | Domain, email account |
| 7 | 16–22 Dec | Steps 14–17 (storage, payments, limits, notifications) | Razorpay live keys once KYC is approved |
| 8 | 23–29 Dec | Steps 18–24 (YouTube test, sign-in, approvals, calendar posting, post status, channel basics) | Test YouTube channel; submit Google's scope check |
| 9 | 30 Dec – 5 Jan | Steps 25–30 (paid AI, legal, admin, alerts, landing page) | Approve legal pages, add card for paid Gemini |
| 10 | 6–12 Jan | Fixes; closed beta starts (step 31) | Invite 5 streamers |
| 11 | 13–19 Jan | Beta fixes | Testimonials, then open sales |
| +1 month | February | Steps 33–34 (Free Fire, talk mode for other games) | Find 2–3 Free Fire streamers for testing |
