import { useCallback, useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router";
import { api, type Clip, type StreamSummary } from "../api";
import { duration, STAGE_LABEL, STATUS_LABEL } from "../format";
import Highlights from "../studio/Highlights";
import Thumbnails from "../studio/Thumbnails";

export default function StreamPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [stream, setStream] = useState<StreamSummary | null>(null);
  const [clips, setClips] = useState<Clip[]>([]);
  const [error, setError] = useState("");
  const [link, setLink] = useState<string | null>(null);
  const [linkNote, setLinkNote] = useState("");

  const load = useCallback(async () => {
    const s = await api<StreamSummary>(`/api/streams/${id}`);
    setStream(s);
    if (s.status === "done") setClips(await api<Clip[]>(`/api/streams/${id}/clips`));
    return s;
  }, [id]);

  useEffect(() => {
    let alive = true;
    let timer: number | undefined;
    async function tick() {
      try {
        const s = await load();
        if (alive && ["uploading", "queued", "running"].includes(s.status)) timer = window.setTimeout(tick, 3000);
      } catch (err) {
        if (alive) setError((err as Error).message);
      }
    }
    tick();
    return () => {
      alive = false;
      window.clearTimeout(timer);
    };
  }, [load]);

  async function act(action: "stop" | "resume") {
    try {
      setStream(await api<StreamSummary>(`/api/streams/${id}/${action}`, { method: "POST" }));
      if (action === "resume") window.setTimeout(load, 1500);
    } catch (err) {
      setError((err as Error).message);
    }
  }

  async function saveLink(value = link ?? "") {
    try {
      const saved = await api<{ link: string | null; drafts_updated: number }>(`/api/streams/${id}/link`,
        { method: "PUT", body: { link: value } });
      setStream((s) => s && { ...s, link: saved.link });
      setLink(null);
      setLinkNote(saved.link
        ? `Saved. New posts from this stream start with it${saved.drafts_updated ? `; added to ${saved.drafts_updated} draft${saved.drafts_updated > 1 ? "s" : ""}` : ""}.`
        : "Link removed.");
    } catch (err) {
      setLinkNote((err as Error).message);
    }
  }

  // Lives on the creator's channel that look like this stream (same day or about as long).
  const [suggestions, setSuggestions] = useState<{ url: string; title: string; at: string; seconds: number | null }[]>([]);
  useEffect(() => {
    if (stream?.status === "done" && !stream.link) {
      api<typeof suggestions>(`/api/streams/${id}/link-suggestions`).then(setSuggestions, () => {});
    }
  }, [id, stream?.status, stream?.link]);

  async function remove() {
    if (!confirm("Delete this stream, its recording and all its clips? This can't be undone.")) return;
    try {
      await api(`/api/streams/${id}`, { method: "DELETE" });
      navigate("/");
    } catch (err) {
      setError((err as Error).message);
    }
  }

  if (error && !stream) return <p className="error">{error}</p>;
  if (!stream) return <p className="muted">Loading…</p>;
  const toReview = clips.filter((c) => c.decision === null).length;
  const kept = clips.filter((c) => c.decision === "keep");

  return (
    <>
      <div className="spread" style={{ marginTop: 16 }}>
        <h1 style={{ margin: 0 }}>{stream.title}</h1>
        <span className={`chip ${stream.status}`}>{STATUS_LABEL[stream.status]}</span>
      </div>
      <p className="muted small">{[stream.recorded_on, duration(stream.duration_s)].filter(Boolean).join(" · ")}</p>

      {stream.status === "uploading" && (
        <div className="banner">
          This recording hasn't finished uploading. Open <Link to="/new">Upload</Link> and pick the same file to carry on.
        </div>
      )}
      {stream.status === "queued" && <p>Waiting for the laptop to start on it.</p>}

      {stream.progress && stream.status !== "done" && (
        <>
          {stream.status === "running" && (
            <>
              <div className="bar"><div style={{ width: `${Math.round(stream.progress.fraction * 100)}%` }} /></div>
              <p className="small muted">{Math.round(stream.progress.fraction * 100)}% · a 3-hour stream takes about an hour</p>
            </>
          )}
          <ul className="stages">
            {stream.progress.stages.map((s) => (
              <li key={s.name} className={s.status}>
                <span>{STAGE_LABEL[s.name] ?? s.name}</span>
                <span>{s.status === "done" ? "✓" : s.status === "running" ? "…" : s.status === "failed" ? "✗" : ""}</span>
              </li>
            ))}
          </ul>
          {stream.progress.last_log && <p className="small muted" style={{ overflowWrap: "anywhere" }}>{stream.progress.last_log}</p>}
        </>
      )}
      {stream.error && <p className="error">{stream.error}</p>}
      {error && <p className="error">{error}</p>}

      <div className="row" style={{ marginTop: 12 }}>
        {(stream.status === "running" || stream.status === "queued") && (
          <button onClick={() => act("stop")} disabled={stream.stopping}>{stream.stopping ? "Stopping…" : "Stop"}</button>
        )}
        {(stream.status === "stopped" || stream.status === "failed") && (
          <button className="primary" onClick={() => act("resume")}>Resume</button>
        )}
        {stream.status === "done" && clips.length > 0 && (
          <Link className="button primary" to={`/streams/${id}/review`}>
            {toReview ? `Review ${toReview} clip${toReview === 1 ? "" : "s"}` : "Review again"}
          </Link>
        )}
        {stream.status !== "running" && <button className="danger" onClick={remove}>Delete</button>}
      </div>

      {stream.status === "done" && (
        <>
          <h2>Stream link</h2>
          <div className="card">
            <div className="small muted">The stream on YouTube. Posts from its clips start with "Full stream: link".</div>
            <div className="row" style={{ marginTop: 8, flexWrap: "nowrap" }}>
              <input aria-label="Stream link" placeholder="https://youtube.com/live/…" value={link ?? stream.link ?? ""}
                     onChange={(e) => setLink(e.target.value)} />
              <button disabled={link === null} onClick={() => saveLink()}>Save</button>
            </div>
            {!stream.link && suggestions.map((s) => (
              <div key={s.url} className="row small" style={{ marginTop: 8, flexWrap: "nowrap" }}>
                <span style={{ flex: 1, minWidth: 0 }}>
                  Is it <b>{s.title || "this live"}</b>? {new Date(s.at).toLocaleDateString("en-IN", { day: "numeric", month: "short" })}
                  {s.seconds ? ` · ${duration(s.seconds)}` : ""}
                </span>
                <button className="chip" onClick={() => saveLink(s.url)}>Use it</button>
              </div>
            ))}
            {linkNote && <p className="small">{linkNote}</p>}
          </div>
          {id && <Highlights streamId={id} />}
          {clips.length > 0 && id && <Thumbnails streamId={id} />}
          <h2>Kept ({kept.length})</h2>
          {kept.length === 0 && <p className="muted small">Clips you keep show up here.</p>}
          {kept.map((c) => (
            <div key={c.id} className="card">
              <div className="title">{c.title ?? `Clip ${c.rank}`}</div>
              <div className="small muted">{c.why}</div>
            </div>
          ))}
        </>
      )}
    </>
  );
}
