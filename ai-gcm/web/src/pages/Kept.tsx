import { useEffect, useState } from "react";
import { Link } from "react-router";
import { api, type Clip } from "../api";

async function share(clip: Clip) {
  const blob = await (await fetch(clip.video, { credentials: "same-origin" })).blob();
  const file = new File([blob], `${(clip.title ?? `clip-${clip.id}`).replace(/[^\w\- ]+/g, "").trim() || "clip"}.mp4`, { type: "video/mp4" });
  if (!navigator.canShare?.({ files: [file] })) throw new Error("This browser can't share videos. Use Download instead.");
  await navigator.share({ files: [file], title: clip.title ?? undefined });
}

export default function Kept() {
  const [clips, setClips] = useState<Clip[] | null>(null);
  const [toast, setToast] = useState("");

  useEffect(() => {
    api<Clip[]>("/api/clips?decision=keep").then(setClips).catch((err) => setToast((err as Error).message));
  }, []);

  function say(text: string) {
    setToast(text);
    window.setTimeout(() => setToast(""), 3000);
  }

  async function copy(clip: Clip) {
    const text = [clip.title, clip.description, clip.hashtags.join(" ")].filter(Boolean).join("\n\n");
    try {
      await navigator.clipboard.writeText(text);
      say("Title, description and hashtags copied");
    } catch {
      say("Couldn't copy here");
    }
  }

  return (
    <>
      <h1>Kept clips</h1>
      {clips?.length === 0 && <p className="muted">Keep clips while reviewing a stream and they collect here.</p>}
      {clips === null && !toast && <p className="muted">Loading…</p>}
      {clips?.map((clip) => (
        <div key={clip.id} className="card kept">
          <video src={clip.video} controls playsInline preload="metadata" />
          <div className="title" style={{ marginTop: 8 }}>{clip.title ?? `Clip ${clip.rank}`}</div>
          <div className="small muted">
            {clip.why} · <Link to={`/streams/${clip.stream_id}`}>{clip.stream_title}</Link>
          </div>
          {clip.hashtags.length > 0 && <div className="small muted">{clip.hashtags.join(" ")}</div>}
          <div className="row" style={{ marginTop: 10 }}>
            <Link className="button primary" to={`/clips/${clip.id}/studio`}>Edit</Link>
            <a className="button" href={`${clip.video}?download=1`}>Download</a>
            {clip.safe_video && <a className="button" href={`${clip.safe_video}&download=1`}>Sponsor-safe copy</a>}
            <button onClick={() => share(clip).catch((err) => say((err as Error).message))}>Share</button>
            <button onClick={() => copy(clip)}>Copy text</button>
          </div>
        </div>
      ))}
      {toast && <div className="toast">{toast}</div>}
    </>
  );
}
