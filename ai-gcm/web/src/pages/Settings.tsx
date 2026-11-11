import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router";
import { api, type Me, type YouTubeChannel, type YouTubeState } from "../api";

// What came back from Google's consent screen (the server sends ?youtube=<result> to this page).
const YT_RESULTS: Record<string, string> = {
  connected: "YouTube connected.",
  cancelled: "Connecting YouTube was cancelled.",
  scopes: "Kaatclip needs all three permissions (upload, see your channel, see its stats). Connect again and leave every box ticked.",
  "no-channel": "That Google account has no YouTube channel. Make one on YouTube first, or pick another account.",
  refused: "Google didn't accept the connection. Try again.",
  "signed-out": "You were signed out while connecting. Sign in, then connect again.",
  "not-ready": "YouTube isn't set up on the laptop yet.",
};

export default function Settings({ me }: { me: Me }) {
  const [invites, setInvites] = useState<{ email: string }[]>([]);
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [telegram, setTelegram] = useState<{ available: boolean; linked: boolean } | null>(null);
  const [tgNote, setTgNote] = useState("");
  const [youtube, setYoutube] = useState<YouTubeState | null>(null);
  const [params, setParams] = useSearchParams();
  const [ytNote, setYtNote] = useState(YT_RESULTS[params.get("youtube") ?? ""] ?? "");

  useEffect(() => {
    if (me.admin) api<{ email: string }[]>("/api/admin/invites").then(setInvites).catch(() => {});
    api<{ available: boolean; linked: boolean }>("/api/telegram").then(setTelegram).catch(() => {});
    api<YouTubeState>("/api/youtube").then(setYoutube).catch(() => {});
    if (params.get("youtube")) setParams({}, { replace: true });
  }, [me.admin]);

  function connectYouTube() {
    // A plain navigation to Google's consent screen; Google sends the browser back to this page.
    location.href = "/auth/youtube/start";
  }

  function replaceChannel(row: YouTubeChannel) {
    setYoutube((y) => y && { ...y, channels: y.channels.map((c) => (c.id === row.id ? row : c)) });
  }

  async function checkChannel(c: YouTubeChannel) {
    try {
      const row = await api<YouTubeChannel>(`/api/youtube/${c.id}/check`, { method: "POST" });
      replaceChannel(row);
      setYtNote(row.status === "ok" ? `${row.title} is connected.` : `${row.title} needs reconnecting.`);
    } catch (err) {
      setYtNote((err as Error).message);
    }
  }

  async function disconnectChannel(c: YouTubeChannel) {
    if (!confirm(`Disconnect ${c.title}? Kaatclip's access is removed at Google and its saved connection deleted.`)) return;
    try {
      await api(`/api/youtube/${c.id}`, { method: "DELETE" });
      setYoutube((y) => y && { ...y, channels: y.channels.filter((x) => x.id !== c.id) });
      setYtNote(`${c.title} disconnected.`);
    } catch (err) {
      setYtNote((err as Error).message);
    }
  }

  async function setAnswer(c: YouTubeChannel, key: "made_for_kids" | "synthetic", value: boolean) {
    try {
      replaceChannel(await api<YouTubeChannel>(`/api/youtube/${c.id}/settings`,
        { method: "PUT", body: { ...c.settings, [key]: value } }));
    } catch (err) {
      setYtNote((err as Error).message);
    }
  }

  async function connectTelegram() {
    try {
      const { url } = await api<{ url: string }>("/api/telegram/link", { method: "POST" });
      // A plain navigation: phones block a new window opened after waiting for the server. t.me opens the
      // Telegram app; tapping Start there links the chat, and coming back shows it connected.
      setTgNote("Opening Telegram: tap Start there, then come back here.");
      location.href = url;
    } catch (err) {
      setTgNote((err as Error).message);
    }
  }

  async function disconnectTelegram() {
    setTelegram(await api<{ available: boolean; linked: boolean }>("/api/telegram", { method: "DELETE" }).then(
      (r) => ({ available: true, linked: r.linked })));
  }

  const [deleting, setDeleting] = useState(false);
  const [confirmEmail, setConfirmEmail] = useState("");
  const [deleteNote, setDeleteNote] = useState("");

  async function deleteAccount(event: React.FormEvent) {
    event.preventDefault();
    try {
      await api("/api/me", { method: "DELETE", body: { email: confirmEmail } });
      location.href = "/about";
    } catch (err) {
      setDeleteNote((err as Error).message);
    }
  }

  async function signOut() {
    await api("/auth/logout", { method: "POST" }).catch(() => {});
    location.href = "/";
  }

  async function invite(event: React.FormEvent) {
    event.preventDefault();
    try {
      await api("/api/admin/invites", { body: { email } });
      setInvites(await api<{ email: string }[]>("/api/admin/invites"));
      setEmail("");
      setMessage("Invited. They can sign in with that Google account now.");
    } catch (err) {
      setMessage((err as Error).message);
    }
  }

  async function uninvite(address: string) {
    await api(`/api/admin/invites/${encodeURIComponent(address)}`, { method: "DELETE" });
    setInvites(await api<{ email: string }[]>("/api/admin/invites"));
  }

  return (
    <>
      <h1>Settings</h1>
      <div className="card">
        <div className="title">{me.name ?? me.email}</div>
        <div className="small muted">{me.email}{me.admin ? " · owner" : ""}</div>
        <button style={{ marginTop: 12 }} onClick={signOut}>Sign out</button>
      </div>
      <h2>YouTube</h2>
      {youtube && !youtube.available && <p className="muted small">YouTube posting isn't set up on this laptop yet.</p>}
      {youtube?.available && (
        <>
          {youtube.channels.map((c) => (
            <div key={c.id} className="card">
              <div className="row" style={{ alignItems: "center", gap: 10 }}>
                {c.thumbnail && <img src={c.thumbnail} alt="" width={40} height={40} style={{ borderRadius: "50%" }} referrerPolicy="no-referrer" />}
                <div style={{ flex: 1 }}>
                  <div className="title">{c.title}</div>
                  <div className="small muted">{c.status === "ok" ? "Connected" : "Connection expired: reconnect to keep posting"}</div>
                </div>
              </div>
              {c.status === "ok" && (
                <div className="small" style={{ marginTop: 4 }}>
                  <label className="tick">
                    <input type="checkbox" checked={c.settings.made_for_kids}
                      onChange={(e) => setAnswer(c, "made_for_kids", e.target.checked)} />
                    My videos on this channel are made for kids
                  </label>
                  <label className="tick">
                    <input type="checkbox" checked={c.settings.synthetic}
                      onChange={(e) => setAnswer(c, "synthetic", e.target.checked)} />
                    My clips include realistic altered or AI-made content
                  </label>
                </div>
              )}
              <div className="row" style={{ marginTop: 10 }}>
                {c.status === "expired"
                  ? <button className="primary" onClick={connectYouTube}>Reconnect</button>
                  : <button onClick={() => checkChannel(c)}>Check</button>}
                <button className="danger" onClick={() => disconnectChannel(c)}>Disconnect</button>
              </div>
            </div>
          ))}
          <div className="card">
            <div className="small muted">
              {youtube.channels.length
                ? "Post to another channel too (a Shorts channel, say): pick it on Google's screen."
                : "Connect your channel to post approved clips to YouTube. Kaatclip can upload and see your channel and its stats; it can't edit or delete your videos, and nothing is posted without your approval."}
            </div>
            <button className="primary" style={{ marginTop: 10 }} onClick={connectYouTube}>
              {youtube.channels.length ? "Connect another channel" : "Connect YouTube"}
            </button>
          </div>
        </>
      )}
      {ytNote && <p className="small" role="status">{ytNote}</p>}
      <h2>Brand kit</h2>
      <Link to="/brand" className="card">
        <div className="title">Your look, lower-third, intro and post text</div>
        <div className="small muted">Set once; used on every export and on new streams' clips.</div>
      </Link>
      <h2>Notifications</h2>
      {telegram && !telegram.available && <p className="muted small">Telegram messages aren't set up on this laptop yet.</p>}
      {telegram?.available && (
        <div className="card">
          <div className="title">Telegram</div>
          <div className="small muted">
            {telegram.linked ? "Connected: you get a message when clips are ready or a stream fails." : "Get a message when your clips are ready."}
          </div>
          <div className="row" style={{ marginTop: 10 }}>
            {telegram.linked
              ? <button onClick={disconnectTelegram}>Disconnect</button>
              : <button className="primary" onClick={connectTelegram}>Connect Telegram</button>}
          </div>
          {tgNote && <p className="small">{tgNote}</p>}
        </div>
      )}
      {me.admin && (
        <>
          <h2>Beta invites</h2>
          <form onSubmit={invite} className="row">
            <input type="email" required placeholder="creator@gmail.com" value={email} onChange={(e) => setEmail(e.target.value)}
              style={{ flex: 1, minWidth: 200 }} aria-label="Email to invite" />
            <button type="submit" className="primary">Invite</button>
          </form>
          {message && <p className="small">{message}</p>}
          {invites.map((i) => (
            <div key={i.email} className="spread card">
              <span>{i.email}</span>
              <button className="danger" onClick={() => uninvite(i.email)}>Remove</button>
            </div>
          ))}
        </>
      )}
      <h2>Your account</h2>
      <div className="card">
        <div className="small muted">
          <a href="/privacy" target="_blank" rel="noreferrer">Privacy policy</a> ·{" "}
          <a href="/terms" target="_blank" rel="noreferrer">Terms</a> · You can also remove Kaatclip's YouTube access at{" "}
          <a href="https://security.google.com/settings/security/permissions" target="_blank" rel="noreferrer">your Google account</a>.
        </div>
        {!deleting
          ? <button className="danger" style={{ marginTop: 10 }} onClick={() => setDeleting(true)}>Delete my account and data</button>
          : (
            <form onSubmit={deleteAccount} style={{ marginTop: 10 }}>
              <p className="small">
                This removes your recordings, clips, edits, exports, post records, brand kit and YouTube connection, and
                removes Kaatclip's access to YouTube. Videos already on YouTube stay there. It can't be undone.
              </p>
              <label htmlFor="del-email">Type your email address to confirm</label>
              <input id="del-email" type="email" required value={confirmEmail} onChange={(e) => setConfirmEmail(e.target.value)} />
              <div className="row" style={{ marginTop: 10 }}>
                <button type="submit" className="danger" disabled={confirmEmail.trim().toLowerCase() !== me.email.toLowerCase()}>
                  Delete everything
                </button>
                <button type="button" onClick={() => { setDeleting(false); setConfirmEmail(""); }}>Keep my account</button>
              </div>
              {deleteNote && <p className="small error">{deleteNote}</p>}
            </form>
          )}
      </div>
    </>
  );
}
