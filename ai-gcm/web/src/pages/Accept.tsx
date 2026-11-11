import { useState } from "react";
import { api, type Me } from "../api";

// Before using Kaatclip, a creator accepts the current privacy policy and terms (YouTube Developer Policies
// III.A.2). Shown once per version; the pages open in a new tab so this screen stays.
export default function Accept({ me, onAccepted }: { me: Me; onAccepted: () => void }) {
  const [ticked, setTicked] = useState(false);
  const [error, setError] = useState("");

  async function accept() {
    try {
      await api("/api/me/accept", { body: { version: me.terms_version } });
      onAccepted();
    } catch (err) {
      setError((err as Error).message);
    }
  }

  return (
    <div className="shell">
      <h1 style={{ marginTop: "10vh" }}>Before you start</h1>
      <p className="muted">Hi {me.name ?? me.email}. In short:</p>
      <ul className="small">
        <li>Your recordings, clips and posts are kept on the computer that runs Kaatclip, and stay yours.</li>
        <li>Kaatclip uses YouTube API Services. If you connect YouTube, it posts only what you approve, exactly as
          approved, and it can't edit or delete your videos.</li>
        <li>Short previews of moments and parts of the transcript go to Google's Gemini to rank clips and write
          titles.</li>
        <li>You can disconnect YouTube or delete your account and data in Settings at any time.</li>
      </ul>
      <p className="small">
        Read the full <a href="/privacy" target="_blank" rel="noreferrer">privacy policy</a> and{" "}
        <a href="/terms" target="_blank" rel="noreferrer">terms</a>. Using Kaatclip means you also agree to the{" "}
        <a href="https://www.youtube.com/t/terms" target="_blank" rel="noreferrer">YouTube Terms of Service</a>.
      </p>
      <label className="tick">
        <input type="checkbox" checked={ticked} onChange={(e) => setTicked(e.target.checked)} />
        I've read and accept the privacy policy and terms
      </label>
      <button className="primary" disabled={!ticked} onClick={accept} style={{ width: "100%", marginTop: 16 }}>
        Continue
      </button>
      {error && <p className="error">{error}</p>}
    </div>
  );
}
