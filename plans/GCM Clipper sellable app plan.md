# GCM Clipper: plan to a ready-to-sell app

Written 4 November 2026. Goal: an app a BGMI streamer can sign up to, pay for by UPI, and use every week without you doing anything by hand. After that, contact streamers.

**Estimate: about 6–7 weeks of building**, if you can do the account sign-ups and decisions in the "You do" column within a day or two each time. Claude writes the code, tests and docs.

---

## What "ready to sell" means

A creator can:

1. Sign up with Google or a phone OTP on the website or the installed app.
2. Start a free trial stream: paste a YouTube link or upload a recording.
3. Get 10 ranked 9:16 clips with Hinglish captions and titles within a few hours, with an email or WhatsApp-style notification.
4. Swipe to keep or reject, trim a clip, fix a caption, then download or share.
5. Pay monthly by UPI AutoPay, see how many stream hours are left, cancel any time.

And you can:

6. See every user, job, failure and payment on an admin page, and fix things without opening the code.
7. Leave it running for a week without touching it.

---

## Decisions needed from you first

| # | Decision | Options | Suggestion |
|---|---|---|---|
| D1 | Brand and seller | Sell as **Cevrynt** (your company) or as a new name like **GCM Clipper** | Under Cevrynt: the payment account, policies and domain then belong to the company |
| D2 | Price | The validation plan offers ₹499 and ₹999 per 4 weeks | Two plans: **Starter ₹499** (about 8 stream hours a month) and **Pro ₹999** (about 20 hours), first stream free |
| D3 | Where processing runs at launch | **Laptop** (free, but must stay on, and handles roughly 10–20 creators) or **cloud server** (always on and faster, but costs money every month from day one) | Laptop for the first customers, cloud once revenue covers it (step 23) |
| D4 | Video source | YouTube link only, or also file upload | Both. Downloading from YouTube is against YouTube's terms, even for the creator's own videos; upload is the safe path |

---

## Phase 1: Make the engine product-grade (weeks 1–2, ₹0)

| Step | What | Who | Done when |
|---|---|---|---|
| 1 | **Full-length streams:** 3–5 hour streams run end to end. Process in chunks, resume after a crash or power cut, delete the source video after clips are made so the disk doesn't fill up. | Claude | Three full real streams processed with no manual fixes |
| 2 | **Speed:** run vision, audio and transcript at the same time, read the HUD at a lower rate during quiet stretches, download only what's needed. Target: a 3-hour stream in about 1 hour on the laptop (now 1–3 hours). | Claude | Measured on a 3-hour stream |
| 3 | **Accuracy:** test on 10 more streams. Add knock detection, use the bigger speech model when a transcript looks broken (ANJI case), tune talk vs fight ranking from your swipes. | Claude, you review clips | Each stream checked; misses written down |
| 4 | **File upload:** upload a recording from phone or PC, in parts if large, as well as pasting a link. | Claude | A 2 GB file uploads from a phone and processes |
| 5 | **Clip editing:** trim start and end, edit caption text, change the title, choose the layout (facecam on top or blur). | Claude | Done from a phone |
| 6 | **Delivery:** download one clip or all as a zip, share to Instagram or YouTube from the phone, copy the suggested title and hashtags. | Claude | Works on Android Chrome |

## Phase 2: Turn it into a service (weeks 3–4, first small costs)

| Step | What | Who | Cost |
|---|---|---|---|
| 7 | **Domain**, e.g. `clipper.cevrynt.com` (free if you own cevrynt.com) or a new `.in` | You buy or confirm, Claude sets it up | ₹0, or about ₹800 a year for a new domain |
| 8 | **Website and app hosting** on Cloudflare Pages: secure HTTPS, so the app installs on phones and sharing works | You make a free Cloudflare account, Claude deploys | ₹0 |
| 9 | **Laptop connected to the internet safely** through Cloudflare Tunnel: no open ports, and it works from anywhere | Claude | ₹0 |
| 10 | **Accounts:** Google login and phone OTP, each creator sees only their own streams (Supabase free tier: login and database) | You make a free Supabase account, Claude builds | ₹0 up to 50,000 users |
| 11 | **Job queue:** many creators can submit; streams run one at a time in order, with a "your stream is 3rd in line" message | Claude | ₹0 |
| 12 | **Clip storage** on Cloudflare R2, auto-deleted after 30 days | Claude | ₹0 up to 10 GB, then about ₹1.3 per GB a month |
| 13 | **Payments:** Razorpay subscriptions with UPI AutoPay, plans from D2, free first stream, upgrade, cancel, invoices | **You do Razorpay KYC** (PAN, bank account, and company documents if you sell as Cevrynt), Claude builds | No fixed fee, about 2% of each payment |
| 14 | **Usage limits:** stream hours per plan, a clear message when the limit is reached | Claude | ₹0 |
| 15 | **Notifications:** email when clips are ready or a stream fails (Brevo or Resend free tier) | You make the account, Claude builds | ₹0 for the first few hundred emails a day |

## Phase 3: Trust, safety and launch (weeks 5–6)

| Step | What | Who | Cost |
|---|---|---|---|
| 16 | **Paid Gemini for customer streams.** On the free tier Google can use what's sent to improve its products. That's fine for testing on public streams, not for paying customers' videos. | You add a payment card to the Google AI Studio account, Claude adds a spending cap | Estimate: a few rupees per stream for text and clip checks; measured in step 3 before launch |
| 17 | **Legal pages:** privacy policy, terms of service, refund policy (Razorpay requires all three), and consent for AI processing. Terms say the creator must own the stream. | Claude drafts, **you approve**; a lawyer review is worth it once revenue starts | ₹0 to draft |
| 18 | **Game and platform terms:** check Krafton's BGMI and YouTube terms on clips and on tools that process streams | Claude researches, you decide | ₹0 |
| 19 | **Admin page:** users, jobs, failures, payments, retry button, refund link | Claude | ₹0 |
| 20 | **Monitoring:** alert to your phone when a job fails or the laptop goes offline | Claude | ₹0 |
| 21 | **Landing page:** what it does, demo clips (with permission), pricing, sign-up | Claude builds, you approve | ₹0 |
| 22 | **Closed beta:** 5 friendly streamers use it free for 2 weeks; fix what they hit; collect 2–3 testimonials | You invite, Claude fixes | ₹0 |

## Phase 4: After launch, when revenue allows

| Step | What | When |
|---|---|---|
| 23 | **Cloud worker with a GPU**, so it doesn't depend on the laptop and runs faster | When the queue often waits more than a few hours, or revenue covers roughly ₹3,000–8,000 a month (estimate, depends on hours used) |
| 24 | **Play Store app** (the installed web app wrapped for Android) | Optional; Google charges a one-time fee of about ₹2,100 |
| 25 | **Learn from swipes:** ranking adapts to each creator's keeps and rejects | Once there are a few hundred decisions |
| 26 | **Organisations plan** (esports teams, agencies): several channels under one account | If organisations show interest |

---

## Costs before the first sale

| Item | Cost |
|---|---|
| Hosting, login, database, storage, email, tunnel (free tiers) | ₹0 |
| Domain | ₹0 with cevrynt.com, or about ₹800 a year |
| Razorpay | ₹0 upfront, about 2% per payment |
| Paid Gemini for customer streams | A few rupees per stream, from the first paying customer |
| Play Store (optional) | About ₹2,100 one time |

So the app can be built and launched for **under ₹1,000**, with real costs starting only once creators pay.

---

## Limits to know

- **The laptop is the server at first.** If it's off, asleep, or loses power or internet, processing stops (clips already made stay available). At about 1 hour per 3-hour stream it can handle around 15–20 streams a day, which is roughly 30–40 creators streaming three times a week. Step 23 removes this limit.
- **YouTube downloading** breaks YouTube's terms, even for a creator's own video. Competitors accept links anyway, but the safe path is upload (step 4), and the terms (step 17) make the creator responsible for owning the content.
- **Accounts only you can create:** domain, Cloudflare, Supabase, Razorpay (KYC), Google AI Studio billing, email service, Play Store. Claude can't sign up or enter payment or ID details for you. Each takes 5–30 minutes; Razorpay KYC can take a few days to approve, so start it in week 1.

## Risk of building before asking streamers

Six weeks of building happens before any streamer says what they want, so there's a chance of building things they don't need, or missing the one thing they care about. A cheap way to reduce this without changing the plan: during Phase 1, send your own clips to 3–5 streamers you know and ask one question, "would you post these?". It takes a few hours and costs nothing.

---

## Week-by-week summary

| Week | Dates | Build | You |
|---|---|---|---|
| 1 | 4–10 Nov | Steps 1–2 (full streams, speed) | Decide D1–D4. Start Razorpay KYC. Create Cloudflare and Supabase accounts |
| 2 | 11–17 Nov | Steps 3–6 (accuracy, upload, editing, delivery) | Review test clips strictly |
| 3 | 18–24 Nov | Steps 7–11 (domain, hosting, tunnel, login, queue) | Domain, email account |
| 4 | 25 Nov – 1 Dec | Steps 12–15 (storage, payments, limits, emails) | Razorpay live keys once KYC is approved |
| 5 | 2–8 Dec | Steps 16–21 (paid AI, legal, admin, alerts, landing page) | Approve legal pages, add card for paid Gemini |
| 6 | 9–15 Dec | Fixes; start the closed beta (step 22) | Invite 5 streamers |
| 7 | 16–22 Dec | Beta fixes | Collect testimonials, then open sales |
