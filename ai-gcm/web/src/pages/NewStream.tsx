import { useEffect, useState } from "react";
import { Link } from "react-router";
import { api, type LiveSession } from "../api";
import { bytes, duration } from "../format";
import {
  carryOn, clearLive, liveCurrent, liveSubscribe, liveSupported, savedLive, startLive, stopLive, streamEnded,
  type LiveState,
} from "../liveUpload";
import {
  clearUpload, current, pauseUpload, resumeUpload, startUpload, subscribe, uploadMetadata, type UploadState,
} from "../uploader";

// While uploading during a stream: what's sent, what OBS has written, and the way to finish.
function LiveProgress({ live }: { live: LiveState }) {
  const still = Math.round((Date.now() - live.grewAt) / 1000);
  const busy = live.status === "uploading" || live.status === "finishing";
  return (
    <>
      <h1>{live.status === "done" ? "Uploaded" : live.status === "stopped" ? "Stopped" : "Uploading while you stream"}</h1>
      <p className="muted small">{live.fileName}</p>
      <div className="bar"><div style={{ width: `${live.size ? Math.round((live.sent / live.size) * 100) : 0}%` }} /></div>
      <div className="small muted">
        {bytes(live.sent)} sent · the recording is {bytes(live.size)}
        {live.status === "uploading" && (still < 15 ? " and growing" : ` · no new video for ${still} s`)}
      </div>
      {live.status === "uploading" && (
        <p className="small muted">
          Keep this tab open while you stream (it can stay in the background). When you stop recording in OBS, the
          last part goes up by itself within about 2 minutes, or tap Stream ended.
        </p>
      )}
      {live.note && <p className="small">{live.note}</p>}
      <div className="row" style={{ marginTop: 16 }}>
        {live.status === "uploading" && <button className="primary" onClick={streamEnded}>Stream ended</button>}
        {busy && <button className="danger" onClick={() => { if (confirm("Stop and throw away this upload?")) void stopLive(); }}>Stop</button>}
        {live.status === "done" && live.streamId && (
          <Link className="button primary" to={`/streams/${live.streamId}`} onClick={clearLive}>See the stream</Link>
        )}
        {!busy && <button onClick={clearLive}>Upload another</button>}
      </div>
    </>
  );
}

export default function NewStream() {
  const [file, setFile] = useState<File | null>(null);
  const [title, setTitle] = useState("");
  const [recordedOn, setRecordedOn] = useState(new Date().toISOString().slice(0, 10));
  const [liveId, setLiveId] = useState("");
  const [sessions, setSessions] = useState<LiveSession[]>([]);
  const [up, setUp] = useState<UploadState | null>(current());
  const [live, setLive] = useState<LiveState | null>(liveCurrent());
  const [mode, setMode] = useState<"file" | "live">(liveSupported() ? "live" : "file");
  const [, tick] = useState(0);
  const [message, setMessage] = useState("");
  const saved = savedLive();

  useEffect(() => subscribe(setUp), []);
  useEffect(() => liveSubscribe(setLive), []);
  useEffect(() => {          // the "no new video for N s" counter
    if (!live || live.status !== "uploading") return;
    const timer = window.setInterval(() => tick((n) => n + 1), 1000);
    return () => window.clearInterval(timer);
  }, [live]);

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

  async function startWhileStreaming() {
    setMessage("");
    try {
      const meta: Record<string, string> = { title: title || "Stream", game: "bgmi" };
      if (recordedOn) meta.recorded_on = recordedOn;
      if (liveId) meta.live_session = liveId;
      await startLive(meta);
    } catch (err) {
      if ((err as Error).name !== "AbortError") setMessage((err as Error).message);
    }
  }

  if (live) return <LiveProgress live={live} />;

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
      {saved && (
        <div className="banner small">
          An upload of <b>{saved.name}</b> didn't finish.{" "}
          <button className="chip" onClick={() => carryOn().catch((err) => setMessage((err as Error).message))}>Carry on</button>{" "}
          (pick the same recording)
        </div>
      )}
      {liveSupported() && (
        <div className="chips" role="tablist">
          <button role="tab" aria-selected={mode === "live"} className={`chip${mode === "live" ? " on" : ""}`} onClick={() => setMode("live")}>
            Upload while I stream
          </button>
          <button role="tab" aria-selected={mode === "file"} className={`chip${mode === "file" ? " on" : ""}`} onClick={() => setMode("file")}>
            Upload a recording
          </button>
        </div>
      )}
      {mode === "live" ? (
        <p className="muted small">
          On the PC you stream from: start recording in OBS when you go live (OBS Settings → Advanced → Automatically
          record when streaming), then pick the recording here. Kaatclip uploads it while you stream, so the clips
          start a few minutes after you stop.
        </p>
      ) : (
        <>
          <p className="muted small">
            The recording from OBS (MP4, MKV or MOV). Use Wi-Fi for big files. If the upload stops, open this page again
            and pick the same file: it carries on from where it stopped.
          </p>
          <label htmlFor="file">Recording</label>
          <input id="file" type="file" accept="video/mp4,video/x-matroska,video/quicktime,.mp4,.mkv,.mov"
            onChange={(e) => pick(e.target.files?.[0] ?? null)} />
          {file && <p className="muted small">{file.name} · {bytes(file.size)}</p>}
        </>
      )}
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
        {mode === "live"
          ? <button className="primary" onClick={startWhileStreaming}>Pick the OBS recording and start</button>
          : <button className="primary" disabled={!file} onClick={start}>Start upload</button>}
      </div>
    </>
  );
}
