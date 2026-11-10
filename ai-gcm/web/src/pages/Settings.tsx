import { useEffect, useState } from "react";
import { Link } from "react-router";
import { api, type Me } from "../api";

export default function Settings({ me }: { me: Me }) {
  const [invites, setInvites] = useState<{ email: string }[]>([]);
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [telegram, setTelegram] = useState<{ available: boolean; linked: boolean } | null>(null);
  const [tgNote, setTgNote] = useState("");

  useEffect(() => {
    if (me.admin) api<{ email: string }[]>("/api/admin/invites").then(setInvites).catch(() => {});
    api<{ available: boolean; linked: boolean }>("/api/telegram").then(setTelegram).catch(() => {});
  }, [me.admin]);

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
    </>
  );
}
