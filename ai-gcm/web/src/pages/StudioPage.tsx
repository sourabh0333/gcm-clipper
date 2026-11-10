import { useCallback, useEffect, useRef, useState } from "react";
import { Link, useNavigate, useParams } from "react-router";
import { api, type Post, type PostText, type RenderJob, type Studio } from "../api";
import { clock } from "../format";

const POLL_MS = 3000;

async function copyText(text: string) {
  await navigator.clipboard.writeText(text);
}

async function shareVideo(url: string, name: string) {
  const blob = await (await fetch(url, { credentials: "same-origin" })).blob();
  const file = new File([blob], name, { type: "video/mp4" });
  if (!navigator.canShare?.({ files: [file] })) throw new Error("This browser can't share videos. Use Download instead.");
  await navigator.share({ files: [file] });
}

// M3.1: a clip opened as a studio project. Its footage is saved for editing, the preview copy plays,
// and the current edit exports to a finished Short. The full editor (timeline, trim, layouts) is M3.3.
export default function StudioPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [studio, setStudio] = useState<Studio | null>(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [note, setNote] = useState("");
  const [exportNote, setExportNote] = useState("");
  const asked = useRef(false);

  const load = useCallback(() => {
    api<Studio>(`/api/clips/${id}/studio`).then(setStudio).catch((err) => setError((err as Error).message));
  }, [id]);

  useEffect(load, [load]);

  // Clips kept before the studio existed have no saved footage yet: ask for it once.
  useEffect(() => {
    if (studio?.window.status === "none" && !asked.current) {
      asked.current = true;
      api(`/api/clips/${id}/prepare`, { method: "POST" }).then(load).catch((err) => setError((err as Error).message));
    }
  }, [studio, id, load]);

  const waiting = studio !== null && (studio.window.status === "preparing" ||
    studio.exports.some((e) => e.status === "queued" || e.status === "running"));
  useEffect(() => {
    if (!waiting) return;
    const timer = window.setInterval(load, POLL_MS);
    return () => window.clearInterval(timer);
  }, [waiting, load]);

  async function exportNow(sponsorSafe = false) {
    setBusy(true);
    try {
      await api<RenderJob>(`/api/clips/${id}/export`, { body: { sponsor_safe: sponsorSafe } });
      setExportNote("Making the finished video on the laptop (about a minute). It appears below under Exports, "
        + "with Post to YouTube and Download.");
      load();
      window.setTimeout(() => document.getElementById("exports")?.scrollIntoView({ behavior: "smooth" }), 400);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(false);
    }
  }

  async function retry() {
    setError("");
    await api(`/api/clips/${id}/prepare`, { method: "POST" }).catch((err) => setError((err as Error).message));
    load();
  }

  if (!studio) return error ? <p className="error">{error}</p> : <p className="muted">Loading…</p>;
  const { clip, window: win, edit } = studio;
  const name = `${(clip.title ?? `clip-${clip.id}`).replace(/[^\w\- ]+/g, "").trim() || "clip"}.mp4`;
  return (
    <>
      <p className="small"><Link to="/library">← Library</Link></p>
      <h1>{clip.title ?? `Clip ${clip.rank}`}</h1>
      <p className="small muted">{clip.why}</p>

      {win.status === "missing" && (
        <div className="banner">The stream's recording is no longer on the laptop, so this clip can't be edited.
          The original clip can still be downloaded below.</div>
      )}
      {(win.status === "preparing" || win.status === "none") && (
        <div className="card">
          <div className="title">Getting the footage ready…</div>
          <p className="small muted">The laptop is saving a few minutes around this clip for editing. This takes
            about half a minute, longer while a stream is being processed.</p>
        </div>
      )}
      {win.status === "failed" && (
        <div className="banner">
          <div className="error">Couldn't get the footage ready: {win.error}</div>
          <button style={{ marginTop: 8 }} onClick={retry}>Try again</button>
        </div>
      )}

      {win.status === "ready" && (
        <>
          <div className="card studio">
            <video src={win.preview} controls playsInline preload="metadata" />
            <p className="small muted">
              Footage saved for editing: {clock(win.start ?? 0)}–{clock(win.end ?? 0)} of the stream. This is a
              small preview copy; exports use the full quality.
            </p>
          </div>
          <h2>Current edit</h2>
          <div className="card">
            <div className="small">
              {edit.version === 0 ? "Automatic edit" : `Your edit, version ${edit.version}`} · {edit.length_s.toFixed(1)} s ·{" "}
              {edit.data.segments.length} part{edit.data.segments.length > 1 ? "s" : ""} · layout {edit.data.layout.template}
              {edit.data.zooms.length > 0 && ` · ${edit.data.zooms.length} zoom${edit.data.zooms.length > 1 ? "s" : ""} on kills`}
              {edit.data.captions.on && " · captions"}
            </div>
            <div className="row" style={{ marginTop: 10 }}>
              <Link className="button primary" to={`/clips/${id}/edit`}>Open editor</Link>
              <button disabled={busy} onClick={() => exportNow()}>Export</button>
              {clip.safe_video && <button disabled={busy} onClick={() => exportNow(true)}>Export sponsor-safe</button>}
            </div>
            <p className="small muted">
              {exportNote || "Export makes the finished video on the laptop. Nothing downloads to your phone unless you tap Download."}
            </p>
          </div>
        </>
      )}

      <h2>Original clip</h2>
      <div className="card">
        <div className="small muted">The clip as the engine cut it, before any studio changes.</div>
        <div className="row" style={{ marginTop: 10 }}>
          <a className="button" href={`${clip.video}?download=1`}>Download</a>
          {clip.safe_video && <a className="button" href={`${clip.safe_video}&download=1`}>Sponsor-safe copy</a>}
          <button onClick={() => shareVideo(clip.video, name).catch((err) => setError((err as Error).message))}>Share</button>
          <button onClick={() => api<PostText>(`/api/clips/${id}/post-text`).then((post) => copyText(post.text))
            .then(() => setNote("Title, description and hashtags copied"), () => setNote("Couldn't copy here"))}>
            Copy text
          </button>
        </div>
        {note && <p className="small">{note}</p>}
      </div>

      {studio.exports.length > 0 && <h2 id="exports">Exports</h2>}
      {studio.exports.map((job) => (
        <div key={job.id} className="card studio">
          <div className="spread">
            <span className="small">
              {job.version ? `Version ${job.version}` : "Automatic edit"}{job.sponsor_safe ? " · sponsor-safe" : ""}
            </span>
            <span className={`chip ${job.status}`}>{job.status === "running" ? "rendering" : job.status}</span>
          </div>
          {job.status === "failed" && <p className="small error">{job.error}</p>}
          {job.video && (
            <>
              <video src={job.video} controls playsInline preload="metadata" style={{ marginTop: 8 }}
                     poster={job.cover ?? undefined} />
              <div className="row" style={{ marginTop: 8 }}>
                <button className="primary" onClick={() => api<Post>("/api/posts", { body: { render_id: job.id } })
                  .then((post) => navigate(`/posts/${post.id}`), (err) => setError((err as Error).message))}>
                  Post to YouTube
                </button>
                <a className="button" href={`${job.video}?download=1`}>Download</a>
                {job.cover && <a className="button" href={`${job.cover}?download=1`}>Cover image</a>}
                <button onClick={() => shareVideo(job.video!, name).catch((err) => setError((err as Error).message))}>
                  Share
                </button>
              </div>
            </>
          )}
        </div>
      ))}
      {error && <div className="toast">{error}</div>}
    </>
  );
}
