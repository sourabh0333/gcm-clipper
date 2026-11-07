import { useEffect, useState } from "react";
import { Link } from "react-router";
import { api, type StreamSummary, type WorkerStatus } from "../api";
import { bytes, duration, STATUS_LABEL } from "../format";

export function StreamCard({ stream }: { stream: StreamSummary }) {
  const fraction =
    stream.status === "uploading" && stream.upload
      ? stream.upload.offset / stream.upload.length
      : stream.progress?.fraction ?? 0;
  return (
    <Link to={`/streams/${stream.id}`} className="card">
      <div className="spread">
        <span className="title">{stream.title}</span>
        <span className={`chip ${stream.status}`}>{STATUS_LABEL[stream.status] ?? stream.status}</span>
      </div>
      <div className="muted small">
        {[stream.recorded_on, duration(stream.duration_s), stream.status === "uploading" && stream.upload
          ? `${bytes(stream.upload.offset)} of ${bytes(stream.upload.length)}` : ""]
          .filter(Boolean).join(" · ")}
      </div>
      {(stream.status === "running" || stream.status === "uploading") && (
        <div className="bar"><div style={{ width: `${Math.round(fraction * 100)}%` }} /></div>
      )}
      {stream.status === "done" && (
        <div className="small" style={{ marginTop: 6 }}>
          {stream.clips} clips · {stream.reviewed === stream.clips ? `${stream.kept} kept` : `${stream.clips - stream.reviewed} to review`}
        </div>
      )}
      {stream.status === "failed" && stream.error && <div className="small error">{stream.error}</div>}
    </Link>
  );
}

export default function Streams() {
  const [streams, setStreams] = useState<StreamSummary[] | null>(null);
  const [worker, setWorker] = useState<WorkerStatus | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let alive = true;
    let timer: number | undefined;
    async function load() {
      try {
        const [list, status] = await Promise.all([
          api<StreamSummary[]>("/api/streams"),
          api<WorkerStatus>("/api/worker"),
        ]);
        if (!alive) return;
        setStreams(list);
        setWorker(status);
        setError("");
        const busy = list.some((s) => ["uploading", "queued", "running"].includes(s.status));
        timer = window.setTimeout(load, busy ? 4000 : 20000);
      } catch (err) {
        if (alive) setError((err as Error).message);
        timer = window.setTimeout(load, 10000);
      }
    }
    load();
    return () => {
      alive = false;
      window.clearTimeout(timer);
    };
  }, []);

  return (
    <>
      <h1>Your streams</h1>
      {worker && !worker.online && worker.queue_waiting && (
        <div className="banner">The laptop's worker isn't running, so waiting streams won't start yet.</div>
      )}
      {error && <p className="error">{error}</p>}
      {streams === null && !error && <p className="muted">Loading…</p>}
      {streams?.length === 0 && (
        <div className="card">
          <p>No streams yet. Upload a recording of a stream (MP4, MKV or MOV) and Kaatclip finds the moments worth posting.</p>
          <Link to="/new" className="button primary">Upload a recording</Link>
        </div>
      )}
      {streams?.map((s) => <StreamCard key={s.id} stream={s} />)}
    </>
  );
}
