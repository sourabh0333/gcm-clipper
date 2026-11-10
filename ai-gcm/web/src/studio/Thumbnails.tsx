import { useCallback, useEffect, useState } from "react";
import { api } from "../api";

type Thumbs = { status: "none" | "queued" | "running" | "done" | "failed"; error?: string | null; images?: string[]; titles?: string[] };

// M3.7: three thumbnails and three titles for a long video of this stream (highlights, or the weekly
// compilation), ready for YouTube's Test & Compare.
export default function Thumbnails({ streamId }: { streamId: string }) {
  const [thumbs, setThumbs] = useState<Thumbs | null>(null);
  const [note, setNote] = useState("");

  const load = useCallback(() => {
    api<Thumbs>(`/api/streams/${streamId}/thumbnails`).then(setThumbs).catch((err) => setNote((err as Error).message));
  }, [streamId]);
  useEffect(load, [load]);

  const waiting = thumbs?.status === "queued" || thumbs?.status === "running";
  useEffect(() => {
    if (!waiting) return;
    const timer = window.setInterval(load, 3000);
    return () => window.clearInterval(timer);
  }, [waiting, load]);

  async function make() {
    setNote("");
    try {
      setThumbs(await api<Thumbs>(`/api/streams/${streamId}/thumbnails`, { method: "POST" }));
    } catch (err) {
      setNote((err as Error).message);
    }
  }

  async function copy(text: string) {
    try {
      await navigator.clipboard.writeText(text);
      setNote("Title copied");
    } catch {
      setNote("Couldn't copy here");
    }
  }

  if (!thumbs) return null;
  return (
    <div className="card thumbsbox">
      <div className="spread">
        <div className="title">Thumbnails and titles</div>
        {!waiting && <button onClick={make}>{thumbs.status === "done" ? "Make new ones" : "Make them"}</button>}
      </div>
      <p className="small muted">For a long video of this stream: 3 thumbnails and 3 titles to try in YouTube's Test & Compare.</p>
      {waiting && <p className="small">Making them on the laptop (about half a minute)…</p>}
      {thumbs.status === "failed" && <p className="small error">{thumbs.error}</p>}
      {thumbs.images && thumbs.images.length > 0 && (
        <div className="thumbgrid">
          {thumbs.images.map((src, i) => (
            <a key={src} href={`${src}?download=1`} aria-label={`Download thumbnail ${i + 1}`}>
              <img src={src} alt={`Thumbnail ${i + 1}`} loading="lazy" />
            </a>
          ))}
        </div>
      )}
      {thumbs.titles?.map((t) => (
        <div key={t} className="spread titlerow">
          <span className="small">{t}</span>
          <button onClick={() => copy(t)}>Copy</button>
        </div>
      ))}
      {note && <p className="small">{note}</p>}
    </div>
  );
}
