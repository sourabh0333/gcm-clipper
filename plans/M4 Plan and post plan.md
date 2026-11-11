# M4 Plan and post: reviewed plan

Written 10 November 2026 before any M4 code, after reviewing the [master plan](GCM%20Clipper%20master%20plan.md) sections 4.5 and 4.6, the M4 row, section 9 (risks) and section 11 (things to check), against Google's current YouTube Data API reference pages, the YouTube API Services Developer Policies and Google's OAuth verification guides (all read 10 Nov 2026). Progress is tracked in [ai-gcm/BUILD_NOTES.md](../ai-gcm/BUILD_NOTES.md).

**M4 goal (from the master plan):** calendar, Shorts-share gauge, YouTube connect, approvals, scheduled posting, the stream funnel (description link, Studio deep link, teaser Short), status and quota counters, the your-channel view, and the live `!clip` listener. **Done when** a clip approved on the phone posts to a test channel at the scheduled minute with the stream link, and Google's scope check is submitted.

---

## 1. What the review found

| # | Finding | Effect on M4 |
|---|---|---|
| P-R1 | **Uploads now have their own quota bucket.** `videos.insert` costs 1 unit from a "Video Uploads" bucket of 100 calls a day (Google's reference; many 2026 guides still quote the old 1,600 units). Everything else shares 10,000 units a day: `thumbnails.set` 50, `videos.update` 50, `videos.list` 1, live chat 5 per connection. | The master plan's numbers hold: about 100 posted Shorts a day for the whole app, ample for the beta. Counters for both buckets; Google's audit form (free) before about 30 active creators. |
| P-R2 | **Uploads are no longer forced private.** The current `videos.insert` reference says uploads from unverified projects are *not* restricted to private, and a video without `privacyStatus` defaults to **public** (Google's older revision note still says the opposite). | Every upload sets `privacyStatus: private` with `publishAt` (or public only for an explicit "post now"), and the uploader reads the status back and fails loudly if YouTube changed it. |
| P-R3 | **Changing a video after upload needs the broad scope.** `videos.update` (reschedule, re-title) accepts only `youtube`, `youtube.force-ssl` or `youtubepartner`, whose consent screen says "see, edit and permanently delete your YouTube videos". `videos.insert` and `thumbnails.set` accept the narrow `youtube.upload` ("manage your YouTube videos"). A third-party guide reports that reviewers reject asking for `youtube.upload` together with `force-ssl`. | Ask only for **`youtube.upload`, `youtube.readonly`, `yt-analytics.readonly`**: a gentler consent screen for creators and a simpler review. Moving a post is free until it's approved; after approval it's on YouTube, and the app offers "change in Studio" (a deep link). |
| P-R4 | **Testing mode tokens last 7 days.** An external app in "Testing" with sensitive scopes gets refresh tokens that expire after 7 days; tokens issued then stay limited even after publishing. | **Approving uploads right away** (private, with `publishAt`): YouTube itself publishes at the planned minute, so a post scheduled 10 days out goes live even if the token expired or the laptop is off. A "reconnect YouTube" banner when the token fails. |
| P-R5 | **Consent rules.** Express consent before any upload or change (III.E.3, II.3); automated uploads need "prior specific and express consent" (III.I.2); no text added to a description without consent (III.C.3); the title field must allow 100 characters (III.C.1); never change a video's privacy without instruction (III.E.3). | Every post shows its exact final title, description, channel and time before **Approve**; the approved text is stored in the audit log. Batch approval lists each post explicitly. **The master plan's blanket "standing consent" is dropped**: "specific" consent for future, unseen clips is a risk to the whole app's API access. |
| P-R6 | **Revoking and data.** Disconnect must revoke programmatically and delete the creator's YouTube data within 7 days (III.D.2.3); stored YouTube data must be refreshed or deleted every 30 days, and stats need the authorization re-checked every 30 days (III.E.4). | Disconnect calls Google's revoke endpoint and deletes the token and cached data at once. A nightly job refreshes or deletes YouTube data older than 30 days. |
| P-R7 | **Thumbnails on Shorts are uncertain.** `thumbnails.set` accepts `youtube.upload` and must be called after processing succeeds; YouTube Help says Shorts thumbnails are set in Studio on a computer. | The uploader waits for processing (polling `videos.list`, 1 unit), tries the cover frame, records the result; on the test channel we learn whether Shorts take it. Long videos (compilations) get the chosen thumbnail. |
| P-R8 | **Live chat is readable with the narrow scopes**; replying in chat needs the broad scope. `liveChatMessages.streamList` streams messages for 5 units per connection and resumes from the last page token. | The `!clip` listener reads chat (owner and moderators only) and saves markers silently; no "Clip saved" reply. **Changed at M4.7 (11 Nov):** `streamList` turned out to be gRPC-only (not in the REST discovery document), which would need a new package, so the listener polls `liveChatMessages.list` (5 units) about once a minute instead; each message keeps the time it was typed, so markers stay exact. About 300 units an hour of live. |
| P-R9 | **Google's check needs a domain we own.** The homepage, privacy policy and redirect URIs must sit on domains verified in Search Console; subdomains of shared hosts (github.io, pages.dev, ts.net) can't be verified as domains. Plus a demo video, a justification per scope, and 3-5 working days. | M4 is built and tested in **Testing mode** (up to 100 listed testers, no domain, ₹0). The submission waits on the owner buying a domain (about ₹800-1,000 a year, already in the master plan's costs). Claude prepares the privacy policy, terms, justifications and demo-video script. |
| P-R10 | **Creators may run several channels** (main and Shorts channels as brand accounts); each Google consent picks one channel. | "Connect another channel"; a post target per post. |
| P-R11 | **The privacy policy has required content** (III.A.2): uses YouTube API Services, links to YouTube's Terms and Google's Privacy Policy, what is collected and why, revocation through Google's security settings page, a contact. | A first privacy policy and terms page in M4 (needed for the consent screen and the check), refined with the legal pages in M6. |

---

## 2. Decisions taken in this review

1. **Scopes:** `youtube.upload`, `youtube.readonly`, `yt-analytics.readonly`, requested in a separate "Connect YouTube" step after sign-in (incremental authorization, offline access). Never `youtube`, `force-ssl` or `youtubepartner`.
2. **Posting model:** Approve = upload now as private with `publishAt`; YouTube publishes. "Post now" = public at once. A post is editable (time, title, text, channel) until it's approved; after that, Studio.
3. **One post per clip per channel**, unless the creator deletes it on YouTube and posts again.
4. **No standing consent** in M4; batch approval of explicit lists instead.
5. **Tokens** encrypted with a key in `.env` (made by the setup script), never logged, deleted on disconnect.
6. **Upload code** uses YouTube's resumable upload over `httpx` (8 MB chunks, retries), with no new dependency.
7. **The stream link** comes from the live broadcast when YouTube knows it, else the creator pastes it on the stream page.

---

## 3. Steps

| Step | What | Done when |
|---|---|---|
| **M4.1 Connect YouTube** | Channels table (encrypted refresh token, channel id and title, scopes, connected and checked dates); connect flow with Google's channel chooser; disconnect with revoke and deletion; reconnect banner on failure | A creator connects and disconnects the test channel from the phone |
| **M4.2 Posts and approvals** | Posts table; "Post this?" from an export: title (100 characters), the exact description (post text with the stream link), tags, channel, time; Approve records the consent text; batch approve | Nothing can post without a recorded approval |
| **M4.3 The uploader** | A posting lane in the worker: resumable upload, private with `publishAt` or public now, Gaming category, made-for-kids and altered-content answers from the channel settings; status read back; thumbnail after processing; retries; Telegram on posted and failed; quota counters | A scheduled Short goes public at the planned minute |
| **M4.4 Calendar** | Week and month views; drafts, scheduled, posted, failed; drag to move drafts; "fill this week" proposes evening slots for the creator to approve; Shorts-share gauge | A week planned in a few taps |
| **M4.5 Stream funnel** | Stream link in every description; "Finish in Studio" deep link with text for the related video and pinned comment; teaser Short suggested before upcoming streams (`liveBroadcasts.list`) | Every posted Short has the link and the Studio button |
| **M4.6 Your channel** | Recent uploads and views split by Shorts, live and videos (Analytics `creatorContentType`), "data through <date>"; 30-day refresh and deletion job | Shown on the streams page |
| **M4.7 Live `!clip`** | During a Live session, read the active broadcast's chat; `!clip` from the owner or a moderator saves a marker | A `!clip` typed by a moderator becomes a marker |
| **M4.8 Privacy, terms and the check pack** | `/privacy` and `/terms` pages; scope justifications; demo-video script; the submission once the domain exists | Google's scope check submitted |
| **M4.9 Real test** | On the owner's phone with the test channel | A clip approved on the phone posts to the test channel at the scheduled minute with the stream link |

---

## 4. Versions and costs

No new packages. YouTube Data API v3 and YouTube Analytics API: free within quota. The domain for Google's check (about ₹800-1,000 a year) is the only cost, and only at M4.8.

---

## 5. What the owner does for M4 (all free until the domain)

1. **A test YouTube channel** (a brand account under your Google account; about 5 minutes). Real posts go there first.
2. **In Google Cloud (project `kaatclip`), about 10 minutes, with Claude guiding:** turn on the YouTube Data API v3 and the YouTube Analytics API; add the three scopes to the consent screen's Data access; add your Google account (and the test channel's) as test users.
3. **Later, at M4.8:** decide on buying the domain (kaatclip.com or .in) for Google's check; record the demo video from Claude's script.

---

## 6. Changes to the master plan from this review

- Section 4.6 "Connect YouTube": the three narrow scopes (P-R3); never `force-ssl`.
- Section 4.6 "'Post this?' approvals": no standing consent (P-R5).
- Section 4.6 "Calendar posting": upload at approval as private with `publishAt`; reschedule after approval in Studio (P-R3, P-R4).
- Section 4.1 "Moment markers": no "Clip saved" chat reply (P-R8).
- Section 11: the private-lock and quota checks are answered by Google's current reference (P-R1, P-R2); the Shorts thumbnail check stays for the test channel.
