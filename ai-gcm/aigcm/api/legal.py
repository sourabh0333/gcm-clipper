"""Kaatclip's public pages (M4.8): the home page, the privacy policy and the terms, readable without signing in
(Google's verification and YouTube's Developer Policies III.A.1, III.A.2). Plain HTML from the server, so they load
fast and any crawler can read them. A creator accepts the current version once before using the app
(`/api/me/accept`); changing the policy means a new TERMS_VERSION, and everyone is asked again.

These texts describe what the code does today. Change them in the same commit as anything that changes what
Kaatclip collects, keeps or shares. They are a careful first version, not legal advice: the owner should have them
read before the public launch (M6)."""

import html

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()
TERMS_VERSION = "2026-11-11"
UPDATED = "11 November 2026"

YOUTUBE_TERMS = "https://www.youtube.com/t/terms"
GOOGLE_PRIVACY = "https://policies.google.com/privacy"
GOOGLE_PERMISSIONS = "https://security.google.com/settings/security/permissions"
USER_DATA_POLICY = "https://developers.google.com/terms/api-services-user-data-policy"

STYLE = """body{margin:0;background:#0e0f13;color:#e9eaee;font:16px/1.6 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
main{max-width:720px;margin:0 auto;padding:24px 16px 64px}a{color:#ffb020}h1{font-size:1.8rem;margin:.4em 0}
h2{font-size:1.2rem;margin-top:1.8em}.brand{font-weight:800;font-size:1.3rem;text-decoration:none;color:#e9eaee}
.brand span{color:#ffb020}.muted{color:#9aa0b0}nav a{margin-right:16px}li{margin:.3em 0}
.button{display:inline-block;background:#ffb020;color:#1a1200;font-weight:700;padding:10px 18px;border-radius:10px;
text-decoration:none;margin-top:12px}"""


def contact(settings):
    return settings.contact_email or (sorted(settings.admins)[0] if settings.admins else "")


def page(title, body):
    return HTMLResponse(f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} · Kaatclip</title>
<style>{STYLE}</style></head><body><main>
<a class="brand" href="/">Kaat<span>clip</span></a>
<nav class="muted" style="margin-top:8px"><a href="/about">About</a><a href="/guide">Guide</a><a href="/privacy">Privacy</a><a href="/terms">Terms</a></nav>
{body}</main></body></html>""")


@router.get("/about", include_in_schema=False)
def about(request: Request):
    return page("About", """
<h1>Your streams in, ready-to-post Shorts out</h1>
<p>Kaatclip is an app for Indian gaming creators who stream BGMI on YouTube. Upload a recording of your stream and
Kaatclip finds the moments worth posting (fights, clutches, funny talk), cuts them into vertical clips with captions,
and lets you edit them on your phone.</p>
<p>When you connect your YouTube channel, Kaatclip can post the clips you approve as Shorts at the time you choose,
show your posts on a calendar, show how your Shorts, lives and videos are doing, and save a moment when you or
your moderators type <code>!clip</code> in your live chat.</p>
<p>Nothing is ever posted without your approval of that exact post. Kaatclip cannot edit or delete your videos.</p>
<p>Kaatclip is invite-only during the beta.</p>
<a class="button" href="/">Open Kaatclip</a>
<p class="muted" style="margin-top:32px">Read the <a href="/privacy">privacy policy</a> and the
<a href="/terms">terms</a>. Kaatclip uses YouTube API Services.</p>""")


@router.get("/guide", include_in_schema=False)
def guide(request: Request):
    """The beta streamer's setup guide: one link the owner sends with the invite (docs/beta-outreach.md)."""
    app = html.escape(request.app.state.settings.public_url or "")
    mail = html.escape(contact(request.app.state.settings))
    ask = f'<a href="mailto:{mail}">{mail}</a>' if mail else "the person who invited you"
    return page("Guide", f"""
<h1>Getting started with Kaatclip</h1>
<p>About 10 minutes, once. Kaatclip finds the best moments of your BGMI streams, turns them into Shorts with Hinglish
captions, and posts the ones you approve to your YouTube. Nothing is posted without your approval.</p>

<h2>1. Sign in</h2>
<ol>
<li>Send your Gmail to the person who invited you. You can sign in after they add you.</li>
<li>Open <a href="{app}">{app}</a> on your phone and on your streaming PC, and tap <b>Continue with Google</b>.</li>
<li>During the beta Google may show "Google hasn't verified this app". Tap <b>Advanced</b> and <b>Go to Kaatclip</b>.</li>
<li>Read <b>Before you start</b>, tick the box and tap <b>Continue</b>.</li>
</ol>

<h2>2. Connect your YouTube channel</h2>
<ol>
<li>Settings → <b>Connect YouTube</b> → pick your channel → leave all three boxes ticked → <b>Continue</b>.</li>
<li>Leave "made for kids" and "altered or AI-made content" unticked unless they are true for your channel.</li>
<li>Verify your channel once at <a href="https://www.youtube.com/verify">youtube.com/verify</a> (free), so Kaatclip
can set your Shorts covers.</li>
<li>During the beta the connection lasts 7 days: when Settings shows <b>Reconnect</b>, tap it.</li>
</ol>

<h2>3. Set OBS to record when you stream</h2>
<ol>
<li>OBS → Settings → Advanced → tick <b>Automatically record when streaming</b>.</li>
<li>OBS → Settings → Output → Recording: keep the format (Hybrid MP4 or MKV) and note the recording folder
(usually <b>Videos</b>).</li>
</ol>

<h2>4. Every stream</h2>
<ol>
<li>Go live as usual. OBS starts recording.</li>
<li>On the streaming PC, open Kaatclip in <b>Chrome or Edge</b> → <b>+ Upload</b> → <b>Upload while I stream</b>.</li>
<li>Drag the newest recording from your Videos folder onto the page (or tap <b>Pick the OBS recording</b>). Keep that
tab open; it can stay in the background.</li>
<li>Optional: on your phone, tap <b>Live → I'm live</b>, and ask your moderators to type <code>!clip</code> in chat at
great moments.</li>
<li>When you stop streaming, the upload finishes by itself and Kaatclip starts making clips.</li>
</ol>
<p class="muted">Not streaming live? <b>+ Upload → Upload a recording</b> works for any finished recording.</p>

<h2>5. After the stream</h2>
<ol>
<li>When the clips are ready, open the stream and tap <b>Review</b>: swipe right to keep, left to skip.</li>
<li>Library → a kept clip → <b>Export</b>. Use the editor for layout, zoom, captions and the title text, or
<b>Make another version</b> for a different title and length.</li>
<li><b>Post to YouTube</b> → check the title and description → pick a time → <b>Review and approve</b> →
<b>Approve</b>. Or Posts → <b>Fill empty evenings</b> → <b>Approve the week</b>.</li>
<li>For Instagram: <b>Copy Reels caption</b>, then <b>Share</b> the video to Instagram and paste it.</li>
<li>Paste the stream's YouTube link on the stream page, so every Short sends viewers to your full stream.</li>
</ol>

<h2>Good to know</h2>
<ul>
<li>Use only your own streams. Kaatclip can't edit or delete your YouTube videos.</li>
<li>Telegram (Settings → Connect Telegram) tells you when clips are ready and when Shorts go live.</li>
<li>Questions or problems: {ask}. Honest feedback is the whole point of the beta.</li>
</ul>""")


@router.get("/privacy", include_in_schema=False)
def privacy(request: Request):
    mail = html.escape(contact(request.app.state.settings))
    write = f'<a href="mailto:{mail}">{mail}</a>' if mail else "the address on Google's sign-in screen for Kaatclip"
    return page("Privacy policy", f"""
<h1>Privacy policy</h1>
<p class="muted">Last updated {UPDATED}. Version {TERMS_VERSION}.</p>
<p>This policy explains what Kaatclip collects, why, where it is kept, who it is shared with, and how to remove it.
You accept it before using Kaatclip, and it is linked from the app at all times.</p>

<h2>Kaatclip uses YouTube API Services</h2>
<p>Kaatclip uses YouTube API Services to post your approved clips and to read your channel's information. By using
those features you also agree to the <a href="{YOUTUBE_TERMS}">YouTube Terms of Service</a>, and Google's handling of
data is covered by the <a href="{GOOGLE_PRIVACY}">Google Privacy Policy</a>.</p>

<h2>What Kaatclip collects and why</h2>
<ul>
<li><b>Your Google account:</b> your email address, name, profile picture and Google account ID, when you sign in
with Google. Used to sign you in and to check that you are invited.</li>
<li><b>Your YouTube channel (only if you connect it):</b> the channel's ID, name and picture, and a permission token
from Google, kept encrypted. Used to post the clips you approve, and for the features below.</li>
<li><b>Your channel's recent activity:</b> your uploads from the last 28 days (titles, dates, lengths, view counts),
your scheduled lives, and YouTube Analytics totals for the last 28 days split into Shorts, lives and videos. Used for
the calendar, the Shorts-share gauge, teaser suggestions and the "Your channel" view.</li>
<li><b>Your live chat (only while a Live session is open in Kaatclip):</b> chat messages are read to find
<code>!clip</code> typed by you or your moderators. Kaatclip keeps only the time of each <code>!clip</code> and the
name of the person who typed it; other messages are not stored.</li>
<li><b>What you upload and make:</b> stream recordings, the clips found in them, your edits, exported videos, cover
images, your brand kit (logo, intro, outro, text), post titles and descriptions, and your approvals of posts, with the
exact text you approved.</li>
<li><b>Telegram (only if you link it):</b> your Telegram chat ID, to send you messages when clips are ready or posts
go live.</li>
<li><b>A record of important actions</b> (signing in, approving, posting, connecting and disconnecting YouTube), to
show what happened and to protect your account.</li>
</ul>
<p>Kaatclip does not sell your information, does not show advertisements, and does not let any third party serve
content in the app.</p>

<h2>How it is used and shared</h2>
<ul>
<li><b>Google / YouTube:</b> your approved clips, with their title, description, tags and your answers to YouTube's
questions (made for kids, altered content), are sent to YouTube when they are posted.</li>
<li><b>Google Gemini:</b> to rank moments and write titles, short low-resolution previews of candidate moments and
parts of the automatic transcript are sent to Google's Gemini API. During the beta Kaatclip uses Gemini's free
tier, under which Google may use what is sent to improve its products.</li>
<li><b>Telegram:</b> if you link it, short messages about your clips and posts are sent through Telegram.</li>
<li>Nothing else is shared with anyone, except where the law requires it.</li>
</ul>
<p>Kaatclip's use and transfer of information received from Google APIs follows the
<a href="{USER_DATA_POLICY}">Google API Services User Data Policy</a>, including its Limited Use requirements.</p>

<h2>Where it is kept, and for how long</h2>
<p>During the beta, Kaatclip runs on its owner's computer in India, and your data is kept there. Your YouTube
permission token is encrypted. Copies of your channel's activity are refreshed while you use the app and are
deleted when they are 30 days old. Every 7 days Kaatclip checks that your YouTube permission still works; if you
have removed it, Kaatclip deletes everything it kept from YouTube about that channel within 7 days. Your recordings,
clips and posts stay until you delete them or your account.</p>

<h2>Cookies</h2>
<p>Kaatclip stores one cookie on your device to keep you signed in, and a short-lived one during Google sign-in. It
does not use advertising or tracking cookies.</p>

<h2>Your choices</h2>
<ul>
<li><b>Disconnect YouTube</b> in Settings: Kaatclip asks Google to remove its access straight away and deletes the
channel's token and data it kept.</li>
<li>You can also remove Kaatclip's access in your Google account at
<a href="{GOOGLE_PERMISSIONS}">{GOOGLE_PERMISSIONS}</a>.</li>
<li><b>Delete a stream</b> to remove its recording, clips and exports.</li>
<li><b>Delete my account and data</b> in Settings removes your account, recordings, clips, edits, posts records, brand
kit and YouTube connection, and removes Kaatclip's access to YouTube, at once (and always within 7 days).
Videos already posted to YouTube stay on YouTube: delete them there.</li>
</ul>

<h2>Questions or complaints</h2>
<p>Write to {write}.</p>""")


@router.get("/terms", include_in_schema=False)
def terms(request: Request):
    mail = html.escape(contact(request.app.state.settings))
    return page("Terms", f"""
<h1>Terms of use</h1>
<p class="muted">Last updated {UPDATED}. Version {TERMS_VERSION}.</p>
<ol>
<li><b>YouTube's terms.</b> Kaatclip uses YouTube API Services. By using Kaatclip, you are agreeing to be bound by the
<a href="{YOUTUBE_TERMS}">YouTube Terms of Service</a>.</li>
<li><b>Privacy.</b> The <a href="/privacy">privacy policy</a> explains what Kaatclip collects and how it is used. You
accept it before using Kaatclip.</li>
<li><b>Your content.</b> You upload only recordings you have the right to use. They stay yours: Kaatclip uses them only
to make your clips and posts for you.</li>
<li><b>Posting.</b> Kaatclip posts to YouTube only the posts you approve, exactly as approved, on the channel and at the
time you choose. You are responsible for what you post, including music and other people's content, and for the
answers you give YouTube (made for kids, altered content).</li>
<li><b>The beta.</b> Kaatclip is invite-only and free during the beta. It may change, pause or stop, and it may make
mistakes: check your clips before you approve them.</li>
<li><b>Fair use of the app.</b> Don't use Kaatclip to break the law or anyone's rights, or to get around YouTube's
rules.</li>
<li><b>Leaving.</b> You can disconnect YouTube or delete your account in Settings at any time.</li>
<li><b>Contact.</b> {f'<a href="mailto:{mail}">{mail}</a>' if mail else "the address on Google's sign-in screen for Kaatclip"}.</li>
</ol>""")
