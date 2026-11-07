import { useEffect, useState } from "react";
import { api } from "../api";

type AuthConfig = { google: boolean; dev: boolean };

export default function SignIn() {
  const [config, setConfig] = useState<AuthConfig | null>(null);
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const next = encodeURIComponent(location.pathname + location.search);

  useEffect(() => {
    api<AuthConfig>("/api/auth-config").then(setConfig).catch(() => setConfig({ google: false, dev: false }));
  }, []);

  async function devSignIn(event: React.FormEvent) {
    event.preventDefault();
    try {
      await api("/auth/dev-login", { body: { email } });
      location.reload();
    } catch (err) {
      setError((err as Error).message);
    }
  }

  return (
    <div className="shell">
      <h1 style={{ marginTop: "18vh", fontSize: "2rem" }}>Kaat<span style={{ color: "var(--accent)" }}>clip</span></h1>
      <p className="muted">Your streams in, ready-to-post Shorts out. Invite-only during the beta.</p>
      {config?.google && (
        <a className="button primary" href={`/auth/google/start?next=${next}`} style={{ width: "100%", marginTop: 16 }}>
          Continue with Google
        </a>
      )}
      {config && !config.google && !config.dev && (
        <p className="banner">Google sign-in isn't set up on this laptop yet.</p>
      )}
      {config?.dev && (
        <form onSubmit={devSignIn} style={{ marginTop: 24 }}>
          <label htmlFor="dev-email">Laptop sign-in (development only)</label>
          <input id="dev-email" type="email" required value={email} onChange={(e) => setEmail(e.target.value)} />
          <button type="submit" style={{ marginTop: 10 }}>Sign in on this laptop</button>
          {error && <p className="error">{error}</p>}
        </form>
      )}
    </div>
  );
}
