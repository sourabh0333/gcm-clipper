# AI-GCM 6-week validation plan

Runs Monday 2 November to Sunday 13 December 2026. Budget: about ₹80,000–1,00,000 after pilot payments. No product code is written.

This plan turns the validation steps in [the market report](../reports/BGMI%20AI%20clipper%20market%20validation.md) into week-by-week work. It answers two questions:

1. **Quality gap:** On real BGMI streams, can creators see a clear difference between good highlights and what YouTube's free recap, OpusClip, Vizard, Eklipse and BGMI Clipper produce today?
2. **Payment:** Will creators or organisations pay for that difference within a month?

If both answers are yes, build. If only organisations pay, build the B2B version. If neither, stop.

---

## 1. Decision rules (fix these before week 1 starts)

Write these down and do not change them once results start coming in. They are the report's suggested thresholds, not industry benchmarks.

| Gate | When | Continue if | Stop or reshape if |
|---|---|---|---|
| G1 · YouTube recap | End of week 1 | Recap highlights are missing in India, English-only, or mostly pick chat spikes and banter over fights | Recap reliably finds BGMI kills and clutches in a Hinglish stream → drop the consumer plan; continue only B2B discovery (section 6) |
| G2 · Blind clip test | End of week 3 | Best existing tool's usable-clip rate is under 50%, it finds under 60% of the editor's top moments, and it misses quiet clutches or funny moments | Any tool reaches 75–80%+ usable clips with acceptable cut points → the quality gap is too small to sell |
| G3 · Interviews | End of week 3 | At least a third of streamers already pay an editor or spend 5+ hours a week finding highlights, and most post Shorts or Reels weekly | Most don't post short-form, or say YouTube recap and VN are enough, or say the creative edit (not finding moments) is the bottleneck |
| G4 · Paid pilot | End of week 6 | At least half the pilot creators pay for month 2, and the median creator posts at least half of the clips delivered | Creators take clips but won't pay, or post few of them |
| G5 · Organisations | End of week 6 | Two or more letters of intent or paid pilots at a monthly or per-event price well above the consumer price | Organisations' in-house editors are cheap enough, or they need broadcast-grade output |

Final decision at the end of week 6:

- **Build for creators:** G1, G2, G3 and G4 pass.
- **Build for organisations first:** G2 and G5 pass, whatever happened to G1 or G4.
- **Stop or rethink:** G2 fails, or both G4 and G5 fail.

---

## 2. Week by week

| Week | Dates | Work | Done when |
|---|---|---|---|
| 0 | 26 Oct – 1 Nov | Fix the decision rules. Set up the tracker sheet (section 9). Hire one experienced BGMI editor for the clip test. Buy tool subscriptions on monthly plans. Draft outreach messages. | Rules written down, editor booked, sheet ready |
| 1 | 2 – 8 Nov | **YouTube recap check:** stream 2–3 hours of your own BGMI with Hinglish commentary to a test channel and check YouTube Studio's live recap. **Read the BGMI terms** on Krafton's site and in the app. Send 150+ streamer outreach messages. Start interviews (target 8). Collect 6 VODs for the clip test with written permission. | G1 decided. 8 interviews done. 6 VODs in hand |
| 2 | 9 – 15 Nov | Editor cuts the reference set from the 6 VODs. Run every tool on the same VODs. Keep interviewing (target 10 more). Invite pilot creators from interviews. Start organisation outreach. | All clips exported. 18 interviews done. 8 pilot creators agreed |
| 3 | 16 – 22 Nov | Blind rating by 5 creators. Score results. Last interviews (target 25–30 total). **Pilot starts:** collect month-1 payment by UPI, deliver the free sample stream first. | G2 and G3 decided. Pilot live and paid |
| 4 | 23 – 29 Nov | Pilot week 2. Organisation calls (target 6). Optional Gemini and Sarvam probe (section 8). | Pilot clip log filling daily. 6 organisation calls |
| 5 | 30 Nov – 6 Dec | Pilot week 3. Organisation calls (target 10–15 total). Send letter-of-intent drafts to interested organisations. | Letters of intent out |
| 6 | 7 – 13 Dec | Pilot week 4 ends. Ask every pilot creator to pay for month 2. Close letters of intent. Write the decision memo (section 11). | G4 and G5 decided. Decision memo written |

If G1 fails at the end of week 1, stop recruiting pilot creators and put that time into organisation discovery. Still run the clip test, because organisations will ask how good the clips are.

---

## 3. Finding streamers (interviews and pilot)

**Who to target**

- BGMI is their main game, and they stream on YouTube Live at least twice a week.
- 10,000 to 1,000,000 subscribers. Aim for a mix: about a third under 50,000, a third 50,000–250,000, and a third over 250,000.
- Mostly Hindi or Hinglish commentary, with a few English and a few no-commentary streamers.
- At least 5 people who already pay an editor.

**Where to find them**

- YouTube search for "BGMI live" and "BGMI Hindi live", sorted by upload date, and the channels of BGMI tournament casters.
- Instagram Reels under BGMI hashtags. Many streamers list a business email in their bio.
- BGMI Discord servers, and the editors who advertise BGMI edits on Instagram and Fiverr. Editors are a useful second group to interview.

**Screener (3 questions, before booking a call)**

1. How many times a week do you stream, and roughly for how long?
2. How many Shorts or Reels did you post last week?
3. Who edits your Shorts: you, a paid editor, a friend, or nobody?

Book calls only with people who stream at least twice a week. Treat "nobody makes Shorts" as a data point and book a few of these too.

**Outreach message (send in English or Hinglish, as the channel speaks)**

> Hi [name], I'm [your name], and I'm researching how BGMI streamers turn long streams into Shorts and Reels. I'm not selling anything. Could I ask you about your editing setup on a 30-minute call? As thanks, I'll send a ₹300 Amazon or Google Play voucher, and I'll share what I learn from 30 BGMI streamers.

Expect about 1 reply for every 6–10 messages. Send in batches of 50 and follow up once after 3 days.

---

## 4. Interview script (30–35 minutes)

Ask about what they actually did recently, not what they might do. Don't describe the product until the last 5 minutes; ideas pitched early get polite yeses that mean nothing. Run the call in whatever language the creator is comfortable in, and record it with permission.

**A. Warm-up (3 min)**

1. How long have you been streaming BGMI, and how big is the channel now?
2. Is streaming your main income, a side income, or not income yet?

**B. Their last stream (8 min)**

3. Tell me about your last stream. How long was it, and what happened after you went offline?
4. Did any Shorts or Reels come out of it? How many, and when did they go up?
5. Who found the moments? How did they find them: rewatching, chat timestamps, memory, viewer clips?
6. Roughly how long did finding the moments take? And editing them?
7. Were there good moments that never became clips? Why not?

**C. Current setup and spending (7 min)**

8. Which apps or tools do you use to edit? (Listen for VN, InShot, Edits, Premiere, OpusClip, Eklipse, BGMI Clipper.)
9. Have you tried an AI clipping tool? What happened? Why did you stop, if you did?
10. Do you pay anyone to edit? How much, and how: per clip, per month, or a share of earnings?
11. Have you seen YouTube's automatic highlights from your livestream? Did you use any of them?

**D. Why clips matter to them (5 min)**

12. Where do new viewers find you: Shorts, Reels, live recommendations, collaborations?
13. Can you point to a clip that brought you a lot of new subscribers? What was in it?
14. What makes a BGMI clip work? What makes one flop?

**E. Priorities (4 min)**

15. If finding moments took zero time, what would you do with the time saved?
16. Which part of making Shorts do you most want gone: finding moments, cutting, captions, layout, or titles?

**F. Offer and close (5 min)**

17. Describe the pilot in one sentence (section 7). Would you try it at ₹[the price for their group] a month?
18. If yes: book the pilot start date and send the UPI link. If no: what would need to change?
19. Can I use one of your recent VODs in a blind clip test? Here is what I'd do with it.
20. Who else should I talk to?

**After each call, fill one tracker row (5 minutes):** hours streamed per week, Shorts per week, minutes spent finding moments per stream, editor spend per month in ₹, tools tried, whether they use YouTube recap, main pain (finding, editing, captions or ideas), their reaction to the pilot (paid, interested, or declined), and one quote worth remembering.

---

## 5. Blind clip test

**Goal:** Measure how good today's tools are on real BGMI footage, against an editor's choices, without raters knowing which tool made which clip.

### 5.1 VODs (6 total)

Pick these so the hard cases are included:

| # | Format | Commentary | Facecam | HUD | Length |
|---|---|---|---|---|---|
| 1 | Squad, YouTube Live VOD | Hinglish, loud | Yes, corner | Default | 3–4 h |
| 2 | Squad, YouTube Live VOD | Hindi | Yes, large | Custom | 3–4 h |
| 3 | Solo, YouTube Live VOD | Hinglish, calm | No | Default | 2–3 h |
| 4 | Squad, screen recording | None | No | Default | 1–2 h |
| 5 | Scrim or tournament POV | Hinglish | Yes | Custom | 2–3 h |
| 6 | Your own test stream from week 1 | Hinglish | Yes | Default | 2–3 h |

Get written permission (a WhatsApp message is enough) for every VOD that isn't yours. Use it only for this test and delete it afterwards unless the creator agrees otherwise.

### 5.2 Reference set from the editor

Brief for the BGMI editor (pay about ₹2,000 per VOD, ₹12,000 total):

- Watch each whole VOD and log **every moment worth a Short** in the sheet: start time, end time, moment type (fight, clutch, multi-kill, close escape, funny, win, other), and a 1–5 rating.
- Start a clip just before the fight starts and end it after the reaction, not on the last kill.
- Then cut the top 8 moments per VOD as 9:16 clips with facecam on top and gameplay below, plus Hinglish captions.

Have the editor also log, without cutting, how long finding the moments took per VOD. That figure is the time saving you would be selling.

For one VOD, have a second person log moments as well. If the two lists overlap by less than 60%, "a good moment" is too subjective to measure. Narrow the rating to fights and clutches, and note this in the decision memo.

### 5.3 Tools to run

| Tool | Setting | Notes |
|---|---|---|
| YouTube live recap | Default | Only works on live streams, so only VOD 6 (your test stream) can be tested |
| OpusClip Pro | ClipAnything (visual mode), 9:16, gaming layout | About $29 for one month |
| Vizard | Gaming clip maker, 9:16 | One month |
| Eklipse | Choose PUBG if BGMI isn't listed; note which game was selected | One month |
| BGMI Clipper | ₹699 version | Windows; produces horizontal clips, so crop them to 9:16 the same way as the others |

Use each tool's default or recommended setting, and record the setting. Take each tool's **top 8 clips per VOD** by its own ranking, or all of them if it makes fewer. Write down processing time and the cost per hour of footage.

### 5.4 Making the test blind

- Export every clip at 1080×1920. Remove watermarks and tool branding. Put the editor's clips through the same export.
- Rename each clip to a random ID. Keep the ID-to-tool key in a separate sheet the raters never see.
- Shuffle the clips. Clips from the same VOD must not appear in a run.
- About 6 VODs × 6 sources × 8 clips ≈ 288 clips. Every clip gets 3 raters, so each of 5 raters watches about 170 clips, about 3 hours of work. Pay each rater ₹2,000.

**Raters:** 5 BGMI creators from the interviews who are not in the pilot. Add 2 BGMI viewers if possible, because viewers judge what gets watched.

### 5.5 Rating form (one form per clip)

1. Would you post this clip? *As it is / with small edits / no*
2. How good is the moment itself? *1–5*
3. Start: *too early / right / too late / cuts into the action*
4. End: *too early / right / too late*
5. Captions: *usable / need fixing / wrong or missing*
6. What kind of moment is it? *fight, clutch, multi-kill, close escape, funny, win, nothing happens*

### 5.6 How to score

| Measure | How it's calculated |
|---|---|
| **Usable-clip rate** | Share of clips where at least 2 of 3 raters said "as it is" or "with small edits" |
| **Coverage of top moments** | Share of the editor's 4–5-rated moments that a tool also clipped, overlapping by at least half the moment's length |
| **Cut accuracy** | Share of clips where the start and the end were both rated "right" |
| **Quiet clutch hits** | Of the editor's clutches with little talking, how many each tool found |
| **Funny moment hits** | Of the editor's funny moments, how many each tool found |
| **Captions** | Share of clips with usable captions, and a 10-clip spot check of Hinglish caption errors |
| **Cost and speed** | ₹ per hour of footage and minutes to process |

The editor's clips are your target quality. G2 passes if the best tool's usable-clip rate is clearly below the editor's, and below 50%.

---

## 6. Organisation interviews (10–15 calls, weeks 2–6)

**Targets:** content houses and talent managers that run several BGMI creators (for example S8UL, GodLike, Team Soul, Orangutan), tournament organisers and production companies (Krafton's BGIS operations, NODWIN Gaming, Upthrust, Skyesports), and Indian clipping or Shorts agencies. Reach the content or production lead through LinkedIn or the business email on their website.

**Script (25 minutes)**

1. Who produces Shorts and Reels for your creators or events today, and how many go out each week?
2. Walk me through the last event or week: from stream end to first clip published, how long did it take?
3. What does that cost per month or per event: editors, freelancers, agencies?
4. What goes wrong: speed, missed moments, cost, sponsor deliverables?
5. How fast do highlights need to be out for sponsors (for example iQOO or Realme)?
6. If clips were ranked and ready for your editors within 1 hour of a match, what would that be worth per event or per month?
7. Would you try it on one event or one month of streams?

**Letter of intent (one paragraph)**

> [Organisation] intends to run a paid pilot of AI-GCM highlight clipping for [one event / one month of streams], at ₹[price] per [event / month], if the first sample meets the quality we agree on. This letter is not binding.

Before pitching organisations, note Krafton's BGMI terms (read in October 2026): creators may earn from free-to-view videos, but may not "sell, or license" BGMI content, and commercial use needs Krafton's written permission. Every video must also carry the "not endorsed or sponsored by KRAFTON INC." line. Selling clip packages of a tournament to a third party may need Krafton's approval; selling editing software or a service to the rights holder does not obviously fall under this. Check with Krafton before any organisation pilot that involves selling footage.

Price to test with organisations: ₹2,999–4,999 a month for a team of streamers, or ₹5,000–15,000 per tournament day. These are starting points to test, not validated prices.

---

## 7. The paid pilot (weeks 3–6)

### 7.1 Offer

> **AI-GCM Highlight Desk, founding pilot**
>
> Send us your BGMI stream link. Within 24 hours you get your best moments as ranked, ready-to-post Shorts and Reels:
>
> - Up to **2 streams a week**, each up to 5 hours
> - **10 ranked clips per stream**, best first, each with a one-line reason ("1v3 clutch in final circle")
> - 9:16 layout with your facecam on top and gameplay below, keeping the kill feed visible
> - **Hinglish captions** burned in, plus a separate caption file
> - Suggested title and hashtags for every clip
> - Delivered to a Google Drive folder, with a WhatsApp message when it's ready
>
> You choose what to post. We never post for you.
>
> **Price:** ₹[499 or 999] for 4 weeks, paid upfront by UPI. Your first stream is free, so you can see a sample before paying.
> **Guarantee:** If fewer than 5 clips a week are worth posting, tell us and we refund the month.

Give half the pilot creators ₹499 and half ₹999, alternating as they sign up. With only 8 creators this is a rough signal, not a proper price test.

### 7.2 Terms (send in writing before payment)

- You keep all rights to your footage and clips.
- We use your VODs and clips only to make your clips and to improve our clip detection. We never publish them or share them with anyone else.
- You can stop at any time and get a refund for the weeks not used.
- At the end of the pilot we delete your footage unless you agree that we may keep it.

### 7.3 How clips are actually made

People make the clips during the pilot, using existing tools. This tests demand before building anything.

- 8 creators × 2 streams × about 4.5 hours per stream (finding moments with tools at 2× speed, then cutting 10 clips) comes to about 72 hours of editing a week. That needs two freelance editors at about 36 hours each. With one editor, cap the pilot at 4 creators.
- Editors may use OpusClip, Eklipse or BGMI Clipper to find candidates, then fix the ranking and cuts by hand. Log how much of each tool's output they kept. This shows how far the tools are from the target.
- Editor cost: about ₹43,000–58,000 for four weeks (about 290 hours at ₹150–200 an hour). Pilot payments recover about ₹6,000 of that.

### 7.4 What to measure

| Measure | How |
|---|---|
| Clips posted | Check each creator's Shorts and Reels twice a week and match them to delivered clips |
| Clips kept or rejected, and why | The creator reacts to each clip in WhatsApp (👍 / 👎) and gives a reason in a word or two for rejects |
| Delivery time | Stream end to delivery, in hours |
| Views on posted clips | Compare against the creator's average for Shorts in the 4 weeks before the pilot |
| Time saved | Ask in a 10-minute check-in at the end of weeks 1 and 4 |
| **Renewal** | At the end of week 4, send the month-2 payment link. Count only people who actually pay |

Every kept or rejected clip, with its timestamps, moment type and reason, also becomes the first labelled BGMI training data. Store it in the pilot clip log (section 9).

---

## 8. Optional technical probe (week 4, about ₹2,000)

This is not product code; it checks whether off-the-shelf models can do the basics.

1. In Google AI Studio, give Gemini 2.5 Flash-Lite three 20-minute BGMI segments and ask for every kill, knock and squad wipe with timestamps. Compare its list with the editor's log.
2. Run 10 minutes of squad Hinglish audio through Sarvam speech-to-text and Whisper large-v3. Count errors on 50 words of each.

**Encouraging:** most kill events come back within ±3 seconds, and Sarvam's captions are usable with light fixes.
**Warning:** the model can't find even clear kill-feed events. Plan for months of labelling before any MVP.

Note that Google's announced Flash price increase takes effect on 1 January 2027. Re-check prices when estimating cost per user.

---

## 9. Tracker sheet

One Google Sheet with these tabs:

| Tab | Columns |
|---|---|
| Outreach | Name, channel link, subscribers, language, contact, date sent, follow-up date, reply, call booked |
| Interviews | Name, date, hours streamed per week, Shorts per week, minutes finding moments per stream, editor spend ₹/month, tools tried, uses YouTube recap?, main pain, pilot reaction, quote |
| Clip test key | Clip ID, VOD, source tool, tool's rank, start, end (raters never see this tab) |
| Clip ratings | Clip ID, rater, post?, moment 1–5, start, end, captions, type |
| Pilot clip log | Creator, stream date, clip #, start, end, moment type, delivered at, kept/rejected, reason, posted?, views after 7 days |
| Organisations | Organisation, contact, type, current clip cost, required speed, interest, LOI sent, LOI signed, price |
| Budget | Item, planned ₹, spent ₹ |

---

## 10. Budget

| Item | Estimate |
|---|---|
| Interview vouchers (30 × ₹300) | ₹9,000 |
| Tool subscriptions, one month each (OpusClip Pro, Vizard, Eklipse, BGMI Clipper) | ₹8,000–9,000 |
| Reference editor (6 VODs) and second logger | ₹14,000 |
| Raters (5–7 × ₹2,000) | ₹10,000–14,000 |
| Pilot editors (4 weeks) | ₹43,000–58,000 |
| Model probe | ₹2,000 |
| **Total spend** | **₹86,000–1,06,000** |
| Pilot payments received (4 × ₹499 + 4 × ₹999) | −₹6,000 |
| **Net** | **about ₹80,000–1,00,000** |

USD prices are converted at about ₹88 to the dollar.

---

## 11. Decision memo (end of week 6, one page)

1. **Decision:** build for creators / build for organisations first / stop.
2. **Gate results:** G1–G5, each passed or failed, with the number behind it.
3. **Quality gap:** the editor's usable-clip rate against the best tool's, and which moment types the tools missed.
4. **Who paid:** pilot renewals at each price, letters of intent signed and their prices.
5. **Surprises:** anything that contradicts the report.
6. **If building:** what the first version must do, based on the moment types and reject reasons from the pilot log, and which labelled data already exists.
