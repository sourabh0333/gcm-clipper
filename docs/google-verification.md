# Google's check for Kaatclip (M4.8)

Everything needed to submit Kaatclip for Google's OAuth verification ("scope check"), so the app can leave
**Testing** mode: no more 100-tester cap, no 7-day YouTube reconnects, and no "Google hasn't verified this app"
warning. Prepared 11 November 2026 from the current app; see [plans/M4 Plan and post plan.md](../plans/M4%20Plan%20and%20post%20plan.md)
(P-R9, P-R11).

**What blocks the submission:** a domain of our own. Google needs the home page, privacy policy, terms and the
sign-in redirect on a domain verified in Google Search Console, and `ts.net` (Tailscale Funnel) can't be verified.
Cost: about ₹800-1,000 a year (the owner's decision). Everything else below is free.

---

## 1. What is ready in the app

| Google asks for | Kaatclip |
|---|---|
| Home page, public, describes the app, links the privacy policy | `/about` |
| Privacy policy, public, linked in the app at all times | `/privacy` (linked on the sign-in screen, the accept screen and Settings) |
| Terms of service | `/terms` (says users agree to the YouTube Terms of Service: YouTube Developer Policies III.A.1) |
| Users accept the privacy policy before using the app | The **Before you start** screen after the first sign-in (and again when the policy's version changes) |
| A way to revoke access | Settings → YouTube → **Disconnect** (revokes at Google at once and deletes the token and data); the privacy policy also points to Google's permissions page |
| A way to delete data | Settings → **Delete my account and data** (at once) |
| Data from a grant revoked on Google's side deleted within 30 days | The worker re-checks every channel's permission every 7 days and deletes the cached data at once, and the channel row 7 days later |
| YouTube data refreshed or deleted every 30 days (III.E.4) | Daily job in the worker |
| Limited Use statement | In the privacy policy |

The pages are plain HTML from the server (`ai-gcm/aigcm/api/legal.py`); their text must change with any change
to what Kaatclip collects or shares. They are a careful first version, not legal advice: have them read before the
public launch (M6).

---

## 2. Putting Kaatclip on the domain (once it is bought)

Example below uses `kaatclip.in`; use whatever is bought.

1. **Buy the domain** (any registrar). Point its nameservers to **Cloudflare** (free plan).
2. **Cloudflare Tunnel** (free) from the laptop: install `cloudflared`, `cloudflared tunnel login`, create a tunnel,
   route `kaatclip.in` (and `www`) to `http://localhost:8770`. Claude sets this up in a session on the laptop; the
   owner only clicks Cloudflare's login link.
3. In `ai-gcm/.env`: `AIGCM_PUBLIC_URL=https://kaatclip.in`, and restart Kaatclip.
4. **Google Search Console**: add the domain property `kaatclip.in`, verify with the DNS TXT record (in Cloudflare).
   Use the same Google account that owns the Cloud project.
5. **Google Cloud → Google Auth Platform:**
   - **Branding:** app name `Kaatclip`; support email; app logo (optional; a logo needs its own brand review, so
     leave it out the first time); home page `https://kaatclip.in/about`; privacy policy
     `https://kaatclip.in/privacy`; terms `https://kaatclip.in/terms`; authorised domain `kaatclip.in`; developer
     contact email.
   - **Clients → Kaatclip web:** add the redirect URI `https://kaatclip.in/auth/google/callback` (keep the `ts.net`
     one until the switch is done).
6. Sign in once through the new address to check it, then remove the old `ts.net` redirect URI.

---

## 3. The scopes and why (paste into "How will the scopes be used?")

Kaatclip asks for three sensitive scopes, all in a separate "Connect YouTube" step after sign-in. None is restricted,
so no security assessment (CASA) is needed. Kaatclip never asks for `youtube`, `youtube.force-ssl` or
`youtubepartner`: it never edits, deletes or comments.

| Scope | What Kaatclip does with it | Where in the demo |
|---|---|---|
| `https://www.googleapis.com/auth/youtube.upload` | Uploads Shorts the creator approved, one by one, with the exact title, description and tags they approved, as private with a publish time (so YouTube publishes them on schedule) or public at once; sets the creator's chosen cover frame as the thumbnail. Calls: `videos.insert` (resumable), `thumbnails.set`. | Approving a post, then the video in YouTube Studio as Scheduled |
| `https://www.googleapis.com/auth/youtube.readonly` | Shows which channel is connected; checks an upload's privacy and processing after upload; reads the last 28 days of the channel's uploads (lengths, views) for the Shorts-share gauge and the "Your channel" view; reads scheduled lives to suggest a teaser Short; finds the active live and reads its chat while the creator has a Live session open, to save a marker when the owner or a moderator types `!clip`. Calls: `channels.list`, `videos.list`, `playlistItems.list`, `liveBroadcasts.list`, `liveChatMessages.list`. | Settings → YouTube; Posts → Week (gauge, upcoming live); Live screen |
| `https://www.googleapis.com/auth/yt-analytics.readonly` | Shows the creator the last 28 days of views, watch time and subscribers split into Shorts, live and videos (`creatorContentType`), so they can see whether clips grow their stream. Call: `reports.query` on their own channel. | Streams → Your channel |

**Why not fewer:** `youtube.upload` can't read anything; `youtube.readonly` can't upload; Analytics by content
type needs `yt-analytics.readonly`.

**Data handling, in one paragraph (for the form):** Tokens are encrypted on the server. YouTube data is used only
to show the creator their own channel and to post what they approve; it is never sold, shared or used for ads, is
refreshed or deleted within 30 days, and is deleted at once when the creator disconnects or deletes their
account. Live chat messages are read only to find `!clip` from the owner or moderators; only the time and the
name are kept.

---

## 4. The demo video (about 3-4 minutes, uploaded to YouTube as Unlisted)

Google's reviewers want to see the consent screen (with the app name, and the browser's address bar showing the
`client_id`) and each scope in use. Record on the laptop's browser (bigger and the address bar is visible), in
English, with short spoken or on-screen notes. Use the test channel.

1. **Home page** (0:00-0:15): open `https://kaatclip.in/about`; scroll; click **Privacy** and **Terms**.
2. **Sign in** (0:15-0:40): **Continue with Google**; show the Google screen; then the **Before you start** screen;
   tick and **Continue**.
3. **Connect YouTube** (0:40-1:20): Settings → **Connect YouTube**. On Google's consent screen, **pause**: point at
   the app name and the address bar (`client_id=...`), and read out the three permissions; pick the channel; allow.
   Back in Settings: the channel shows as connected (`channels.list`, `youtube.readonly`).
4. **Upload (`youtube.upload`)** (1:20-2:20): Library → a clip → **Export** → **Post to YouTube**; show the title,
   description with the stream link, time; **Review and approve** → **Approve**. Wait for **scheduled**; open YouTube
   Studio and show the video as Scheduled with the same title and description.
5. **Read (`youtube.readonly`)** (2:20-2:50): Posts → **Week**: the Shorts-share gauge (from the channel's uploads) and
   an upcoming live with **Make a teaser** (schedule a test live in YouTube Studio beforehand). Live screen: **I'm
   live** shows "Listening to the chat" during a test live; type `!clip` and show the marker.
6. **Analytics (`yt-analytics.readonly`)** (2:50-3:20): Streams → **Your channel**: Shorts / Live / Videos, "data through".
7. **Revoke and delete** (3:20-3:50): Settings → YouTube → **Disconnect**; then Google's permissions page shows
   Kaatclip gone; mention **Delete my account and data**.

---

## 5. Submitting

1. Google Auth Platform → **Audience**: publishing status **In production** (Google then asks for verification).
2. **Verification centre** → **Prepare for verification**: confirm branding, paste the scope justifications from
   section 3, the demo video link from section 4, and the data handling paragraph.
3. Google replies by email (usually 3-5 working days, sometimes with questions). Answer from this file.
4. After approval: creators reconnect YouTube once so their tokens are no longer Testing-mode tokens.

**Until then (now):** the project stays in **Testing**. Every beta creator must be added under Audience → Test users
(up to 100), and their YouTube connection must be renewed every 7 days (Settings shows **Reconnect**).
