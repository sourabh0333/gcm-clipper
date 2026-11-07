# Google sign-in setup (owner, about 10 minutes, free)

Kaatclip signs creators in with Google. Google needs to know the app first. This is done once, in your own Google account. Claude can't do it for you, but can walk through it with you in the browser if you say so.

**Easiest:** double-click `ai-gcm/Setup Kaatclip.cmd`. It does Telegram and the phone address first, then prints the exact redirect URIs for step 5 and asks for the values from step 6, so nothing has to be typed into `.env` by hand.

Sign-in asks only for name, email and profile picture. With only those, Google needs no tester list and no review (M2 plan, finding R2). YouTube permissions come later, in M4, with their own steps.

## Steps

1. Open <https://console.cloud.google.com/> with the Google account you want to own Kaatclip. Accept the terms if asked.
2. **Create a project:** project picker at the top → New project → name `Kaatclip` → Create. Select it.
3. **Open "Google Auth Platform"** (search "OAuth consent" or "Google Auth Platform" in the top bar) → Get started.
   - App name: `Kaatclip`
   - User support email: your email
   - Audience: **External**
   - Contact email: your email
   - Agree and Create.
4. **Data access** (left menu): Add or remove scopes → tick only `.../auth/userinfo.email`, `.../auth/userinfo.profile` and `openid` → Update → Save. Add nothing else.
5. **Clients** (left menu) → Create client:
   - Application type: **Web application**
   - Name: `Kaatclip web`
   - Authorised redirect URIs → Add URI: `http://localhost:8770/auth/google/callback`
   - Add a second one for the phone: `https://<laptop>.<tailnet>.ts.net/auth/google/callback` (the setup script prints the exact address).
   - Create. A box shows the **Client ID** and **Client secret**.
6. Paste the Client ID, Client secret and your Google email into the setup window when it asks. (Or by hand: open `ai-gcm/.env` in Notepad and add these lines with your own values.)

   ```
   GOOGLE_CLIENT_ID=...apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=...
   AIGCM_ADMINS=your.google.email@gmail.com
   AIGCM_PUBLIC_URL=http://localhost:8770
   ```

   Never paste the secret into a chat. `.env` is never committed.
7. Tell Claude "Google is set up". Claude starts the API and you sign in once on the laptop to confirm.

## Notes

- Publishing status can stay **Testing**: with only these scopes, anyone you invite can sign in, with no 7-day expiry.
- To let a beta creator in, add their email to `AIGCM_INVITES` in `.env` (comma-separated) or use the invite list in the app as the owner.
- If Google shows "redirect_uri_mismatch", the address in step 5 doesn't exactly match `AIGCM_PUBLIC_URL` + `/auth/google/callback`.
