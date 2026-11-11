import { useEffect, useState } from "react";
import { api, type LiveSession } from "../api";
import { clock } from "../format";

export default function Live() {
  const [live, setLive] = useState<LiveSession | null | undefined>(undefined);
  const [now, setNow] = useState(Date.now());
  const [error, setError] = useState("");
  const [flash, setFlash] = useState(false);

  useEffect(() => {
    api<{ open: LiveSession | null }>("/api/live").then((r) => setLive(r.open)).catch((e) => setError((e as Error).message));
    const timer = window.setInterval(() => setNow(Date.now()), 1000);
    return () => window.clearInterval(timer);
  }, []);

  // While live, look again every 20 seconds: !clip marks typed in YouTube chat arrive from the laptop.
  const liveId = live?.id;
  useEffect(() => {
    if (!liveId) return;
    const timer = window.setInterval(() => {
      api<{ open: LiveSession | null }>("/api/live").then((r) => { if (r.open?.id === liveId) setLive(r.open); }, () => {});
    }, 20000);
    return () => window.clearInterval(timer);
  }, [liveId]);

  async function run(fn: () => Promise<LiveSession>) {
    setError("");
    try {
      setLive(await fn());
    } catch (err) {
      setError((err as Error).message);
    }
  }

  async function mark() {
    if (!live) return;
    navigator.vibrate?.(60);
    setFlash(true);
    window.setTimeout(() => setFlash(false), 600);
    await run(() => api<LiveSession>(`/api/live/${live.id}/markers`, { method: "POST" }));
  }

  if (live === undefined) return <p className="muted">{error || "Loading…"}</p>;

  if (live === null)
    return (
      <>
        <h1>Live</h1>
        <p className="muted">
          Tap "I'm live" when your stream starts. Then tap the big button whenever something happens that should be a
          clip. When you upload the recording, pick this session and every mark becomes a clip.
        </p>
        <p className="muted small">
          With YouTube connected, you or a moderator can also type <b>!clip</b> in your live chat: Kaatclip saves the
          moment quietly, without replying in chat.
        </p>
        <button className="primary" style={{ width: "100%" }} onClick={() => run(() => api<LiveSession>("/api/live", { body: {} }))}>
          I'm live
        </button>
        {error && <p className="error">{error}</p>}
      </>
    );

  const elapsed = (now - Date.parse(live.started_at)) / 1000;
  return (
    <>
      <div className="spread" style={{ marginTop: 16 }}>
        <span className="chip running">● LIVE {clock(elapsed)}</span>
        <span className="muted small">{live.markers.length} marked</span>
      </div>
      <button className="markbtn" onClick={mark} style={flash ? { background: "var(--keep)" } : undefined}>
        {flash ? "Saved ✓" : "Mark moment"}
      </button>
      {error && <p className="error">{error}</p>}
      {live.markers.length > 0 && (
        <p className="muted small">Last mark at {clock(live.markers[live.markers.length - 1])}</p>
      )}
      {live.chat && <p className="small" role="status">💬 {live.chat}</p>}
      {(live.marks ?? []).filter((m) => m.source === "chat").length > 0 && (
        <p className="muted small">
          From chat: {(live.marks ?? []).filter((m) => m.source === "chat").map((m) => `${clock(m.t)}${m.by ? ` (${m.by})` : ""}`).join(", ")}
        </p>
      )}
      <div className="row">
        <button disabled={!live.markers.length}
          onClick={() => run(() => api<LiveSession>(`/api/live/${live.id}/markers/last`, { method: "DELETE" }))}>
          Undo last mark
        </button>
        <button className="danger" onClick={() => run(() => api<LiveSession>(`/api/live/${live.id}/end`, { method: "POST" }))
          .then(() => setLive(null))}>
          Stream ended
        </button>
      </div>
    </>
  );
}
