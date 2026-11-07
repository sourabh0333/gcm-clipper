import { useEffect, useState } from "react";
import { Link } from "react-router";
import { api, type LiveSession } from "../api";
import { bytes, duration } from "../format";
import {
  clearUpload, current, pauseUpload, resumeUpload, startUpload, subscribe, uploadMetadata, type UploadState,
} from "../uploader";

export default function NewStream() {
  const [file, setFile] = useState<File | null>(null);
  const [title, setTitle] = useState("");
  const [recordedOn, setRecordedOn] = useState(new Date().toISOString().slice(0, 10));
  const [liveId, setLiveId] = useState("");
  const [sessions, setSessions] = useState<LiveSession[]>([]);
  const [up, setUp] = useState<UploadState | null>(current());
  const [message, setMessage] = useState("");

  useEffect(() => subscribe(setUp), []);

  useEffect(() => {
    api<{ open: LiveSession | null; recent: LiveSession[] }>("/api/live")
      .then((live) => setSessions([...(live.open ? [live.open] : []), ...live.recent]))
      .catch(() => {});
  }, []);

  function pick(f: File | null) {
    setFile(f);
    if (f && !title) setTitle(f.name.replace(/\.[^.]+$/, ""));
  }

  async function start() {
    if (!file) return;
    setMessage("");
    try {
      await startUpload(file, uploadMetadata(file, title, recordedOn, liveId));
    } catch (err) {
      setMessage((err as Error).message);
    }
  }

  if (up) {
    const fraction = up.total ? up.sent / up.total : 0;
    const left = up.speed > 0 ? (up.total - up.sent) / up.speed : null;
    return (
      <>
        <h1>{up.status === "done" ? "Uploaded" : "Uploading"}</h1>
        <p className="muted small">{up.fileName}</p>
        <div className="bar"><div style={{ width: `${Math.round(fraction * 100)}%` }} /></div>
        <div className="spread small muted">
          <span>{Math.round(fraction * 100)}% · {bytes(up.sent)} of {bytes(up.total)}</span>
          <span>
            {up.status === "sending" && up.speed > 0 ? `${(up.speed / 1024 ** 2).toFixed(1)} MB/s` : ""}
            {up.status === "sending" && left ? ` · ${duration(left) || "under a minute"} left` : ""}
          </span>
        </div>
        {up.status === "sending" && <p className="small muted">You can use the rest of the app meanwhile; keep this tab open.</p>}
        {up.error && <p className="error">{up.error}</p>}
        <div className="row" style={{ marginTop: 16 }}>
          {up.status === "sending" && <button onClick={pauseUpload}>Pause</button>}
          {(up.status === "paused" || up.status === "error") && <button className="primary" onClick={resumeUpload}>Resume</button>}
          {up.status === "done" && up.streamId && (
            <Link className="button primary" to={`/streams/${up.streamId}`} onClick={clearUpload}>See the stream</Link>
          )}
          {up.status !== "sending" && <button onClick={clearUpload}>{up.status === "done" ? "Upload another" : "Start over"}</button>}
        </div>
      </>
    );
  }

  return (
    <>
      <h1>Upload a stream</h1>
      <p className="muted small">
        The recording from OBS or your streaming app (MP4, MKV or MOV). Use Wi-Fi for big files. If the upload stops,
        open this page again and pick the same file: it carries on from where it stopped.
      </p>
      <label htmlFor="file">Recording</label>
      <input id="file" type="file" accept="video/mp4,video/x-matroska,video/quicktime,.mp4,.mkv,.mov"
        onChange={(e) => pick(e.target.files?.[0] ?? null)} />
      {file && <p className="muted small">{file.name} · {bytes(file.size)}</p>}
      <label htmlFor="title">Title</label>
      <input id="title" value={title} maxLength={300} onChange={(e) => setTitle(e.target.value)} />
      <label htmlFor="date">Streamed on</label>
      <input id="date" type="date" value={recordedOn} onChange={(e) => setRecordedOn(e.target.value)} />
      {sessions.length > 0 && (
        <>
          <label htmlFor="live">Moments you marked on the Live screen</label>
          <select id="live" value={liveId} onChange={(e) => setLiveId(e.target.value)}>
            <option value="">None</option>
            {sessions.map((s) => (
              <option key={s.id} value={s.id}>
                {new Date(s.started_at).toLocaleString()} · {s.markers.length} marks{s.title ? ` · ${s.title}` : ""}
              </option>
            ))}
          </select>
        </>
      )}
      {message && <p className="error">{message}</p>}
      <div className="row" style={{ marginTop: 18 }}>
        <button className="primary" disabled={!file} onClick={start}>Start upload</button>
      </div>
    </>
  );
}
