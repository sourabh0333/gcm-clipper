import { useEffect, useState } from "react";
import { api, type Me } from "../api";

export default function Settings({ me }: { me: Me }) {
  const [invites, setInvites] = useState<{ email: string }[]>([]);
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");

  useEffect(() => {
    if (me.admin) api<{ email: string }[]>("/api/admin/invites").then(setInvites).catch(() => {});
  }, [me.admin]);

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
      <h2>Notifications</h2>
      <p className="muted small">Telegram messages when clips are ready come next.</p>
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
