# Finding Kaatclip's first beta streamers

Written 12 November 2026. The goal: 2-3 Hindi/Hinglish BGMI streamers using Kaatclip for 1-2 weeks and telling us honestly
what works, so the next features are chosen from real use (see [reports/Kaatclip feature gaps 2026.md](../reports/Kaatclip%20feature%20gaps%202026.md)).

## Who to ask

- BGMI streamers who stream **from a PC with OBS** (on YouTube) and speak Hindi or Hinglish.
- About **5,000-100,000 subscribers**: big enough to care about Shorts, small enough not to have an editor.
- They stream **at least 3 times a week**, and post few or irregular Shorts today (look at their Shorts tab).
- Avoid anyone whose streams are mostly other people's content.

Where to find them: YouTube search "BGMI live Hindi", sorted by upload date; the "Live" tab of BGMI; channels in the
creators' own recommendations; Instagram gaming pages; Discord gaming servers.

## How to ask

Send a direct message on **Instagram** (most creators read DMs) or their **Discord**, not in their live chat (that looks
like spam). Keep it personal: mention one of their streams. Send each message yourself; don't send the same text to
dozens of people at once.

### Message (Hinglish)

> Hi {name} bhai! Maine aapka {stream / moment} wala stream dekha, mast tha 🔥
>
> Main Kaatclip bana raha hoon: ek app jo aapke BGMI stream ki recording se khud best moments dhundhta hai (kills,
> clutch, funny baatein), unhe Hinglish captions ke saath vertical Shorts banata hai, aur aapke approve karne par
> aapke YouTube pe schedule kar deta hai. Kuch bhi aapke approval ke bina post nahi hota.
>
> Abhi beta hai, bilkul free. 2 hafte use karke honest feedback de doge? Setup 10 minute ka hai (OBS se record karte
> ho na?). Agar interested ho to apna Gmail bhej do, main access de dunga.

### Message (English)

> Hi {name}! I watched your {stream / moment} stream, loved it 🔥
>
> I'm building Kaatclip: an app that finds the best moments in your BGMI stream recordings by itself (kills,
> clutches, funny talk), turns them into vertical Shorts with Hinglish captions, and schedules them on your YouTube
> once you approve. Nothing posts without your approval.
>
> It's in beta and completely free. Would you try it for 2 weeks and give honest feedback? Setup takes 10 minutes
> (you record with OBS, right?). If you're interested, send me your Gmail and I'll give you access.

## When someone says yes

1. **Google Cloud** (project `kaatclip`) → Google Auth Platform → **Audience** → **Test users** → **Add users** → their
   Gmail → Save. (Up to 100 testers while the app is in Testing.)
2. **Kaatclip** → Settings → **Beta invites** → their Gmail → Invite.
3. Send them the guide link: `{your Kaatclip address}/guide` (today: https://greenbornit.tailfc640f.ts.net/guide).
4. Keep the laptop on and online during their streams and uploads.

## What to ask them after a week

- Which clips did you keep, and why did you skip the others?
- Did you post the Shorts? Did they get views or subscribers?
- What took too long or confused you?
- Did you use Reels, "Make another version", the calendar?
- Would you pay for it? How much a month would feel fair?
- Do you have sponsors? Would a sponsor report help you?

Write their answers in `ai-gcm/BUILD_NOTES.md` so the next sessions can use them.
