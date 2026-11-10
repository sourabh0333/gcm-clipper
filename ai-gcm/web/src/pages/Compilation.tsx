import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router";
import { api } from "../api";
import { duration } from "../format";

type Piece = { clip_id: number; title: string; stream_title: string; type: string; talk: boolean; length_s: number;
               kills: number; kept: boolean; chosen: boolean; poster: string };
type Suggestion = { format: "wide" | "short"; total_s: number; limit_s: number; target_s: [number, number]; pieces: Piece[] };
type Made = { id: string; status: string; error: string | null; format: string; pieces: number; created_at: string | null;
              video?: string; titles?: string[]; chapters?: string[]; description?: string; length_s?: number; thumbnails?: string[] };

// M3.8: the week's best as one long video (or a 9:16 one up to 3 minutes): fights with the creator's talk
// clips between them, title cards, chapters, and the thumbnails and titles to post it with.
export default function Compilation() {
  const [format, setFormat] = useState<"wide" | "short">("wide");
  const [suggestion, setSuggestion] = useState<Suggestion | null>(null);
  const [pieces, setPieces] = useState<Piece[]>([]);
  const [made, setMade] = useState<Made[]>([]);
  const [note, setNote] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    setSuggestion(null);
    api<Suggestion>(`/api/compilations/suggest?format=${format}`).then((s) => { setSuggestion(s); setPieces(s.pieces); })
      .catch((err) => setNote((err as Error).message));
  }, [format]);

  const loadMade = useCallback(() => { api<Made[]>("/api/compilations").then(setMade).catch(() => {}); }, []);
  useEffect(loadMade, [loadMade]);
  const waiting = made.some((m) => m.status === "queued" || m.status === "running");
  useEffect(() => {
    if (!waiting) return;
    const timer = window.setInterval(loadMade, 5000);
    return () => window.clearInterval(timer);
  }, [waiting, loadMade]);

  const chosen = pieces.filter((p) => p.chosen);
  const total = chosen.reduce((sum, p) => sum + p.length_s, 0);
  const over = suggestion ? total > (format === "short" ? suggestion.limit_s : 20 * 60) : false;

  function toggle(id: number) {
    setPieces((all) => all.map((p) => (p.clip_id === id ? { ...p, chosen: !p.chosen } : p)));
  }

  function move(id: number, by: number) {
    setPieces((all) => {
      const order = all.filter((p) => p.chosen);
      const i = order.findIndex((p) => p.clip_id === id);
      const j = i + by;
      if (i < 0 || j < 0 || j >= order.length) return all;
      [order[i], order[j]] = [order[j], order[i]];
      return [...order, ...all.filter((p) => !p.chosen)];
    });
  }

  async function makeIt() {
    setBusy(true);
    try {
      const job = await api<Made>("/api/compilations", { body: { clip_ids: chosen.map((p) => p.clip_id), format } });
      setMade((list) => [job, ...list]);
      setNote(format === "wide" ? "Making it on the laptop: about 1.5 minutes for every minute of video." : "Making it on the laptop.");
    } catch (err) {
      setNote((err as Error).message);
    } finally {
      setBusy(false);
    }
  }

  async function copy(text: string, what: string) {
    try {
      await navigator.clipboard.writeText(text);
      setNote(`${what} copied`);
    } catch {
      setNote("Couldn't copy here");
    }
  }

  async function remove(id: string) {
    await api(`/api/compilations/${id}`, { method: "DELETE" }).catch((err) => setNote((err as Error).message));
    loadMade();
  }

  return (
    <>
      <p className="small"><Link to="/library">← Library</Link></p>
      <h1>Weekly compilation</h1>
      <p className="muted small">The week's best fights with your own talk clips between them, a title card on each, and
        chapters in the description: never a silent kill montage.</p>
      <div className="chips">
        <button className={format === "wide" ? "chip on" : "chip"} onClick={() => setFormat("wide")}>Long video 16:9</button>
        <button className={format === "short" ? "chip on" : "chip"} onClick={() => setFormat("short")}>Short 9:16 (up to 3 min)</button>
      </div>

      {!suggestion && <p className="muted">Picking the week's best…</p>}
      {suggestion && (
        <>
          <p className={over ? "small error" : "small"}>
            {chosen.length} clips · {duration(total)}
            {format === "wide" && total < suggestion.target_s[0] && " · shorter than the usual 8–13 minutes"}
            {over && " · too long"}
          </p>
          <div className="compilelist">
            {pieces.map((p, i) => (
              <div key={p.clip_id} className={p.chosen ? "compilerow on" : "compilerow"}>
                <input type="checkbox" checked={p.chosen} onChange={() => toggle(p.clip_id)} aria-label={`Use ${p.title}`} />
                <img src={p.poster} alt="" loading="lazy" />
                <div className="compiletext">
                  <div className="small title">{p.title}</div>
                  <div className="small muted">{p.talk ? "Talk" : `${p.kills} kill${p.kills === 1 ? "" : "s"}`} · {Math.round(p.length_s)} s{p.kept ? " · kept" : ""}</div>
                </div>
                {p.chosen && (
                  <div className="compilemove">
                    <button aria-label="Earlier" disabled={i === 0} onClick={() => move(p.clip_id, -1)}>↑</button>
                    <button aria-label="Later" disabled={i === chosen.length - 1} onClick={() => move(p.clip_id, 1)}>↓</button>
                  </div>
                )}
              </div>
            ))}
            {pieces.length === 0 && <p className="muted small">No clips from the last week have footage left on the laptop.</p>}
          </div>
          <button className="primary" style={{ width: "100%", marginTop: 12 }} disabled={busy || chosen.length < 2 || over}
                  onClick={makeIt}>Make the compilation</button>
        </>
      )}

      {made.length > 0 && <h2>Made</h2>}
      {made.map((m) => (
        <div key={m.id} className="card compiled">
          <div className="spread">
            <span className="small">{m.format === "short" ? "Short 9:16" : "Long video"} · {m.pieces} clips
              {m.length_s ? ` · ${duration(m.length_s)}` : ""}</span>
            <span className={`chip ${m.status}`}>{m.status === "running" ? "making" : m.status}</span>
          </div>
          {m.status === "failed" && <p className="small error">{m.error}</p>}
          {m.video && <video src={m.video} controls playsInline preload="metadata" poster={m.thumbnails?.[0]} />}
          {m.thumbnails && m.thumbnails.length > 0 && (
            <div className="thumbgrid">
              {m.thumbnails.map((src, i) => (
                <a key={src} href={`${src}?download=1`} aria-label={`Download thumbnail ${i + 1}`}><img src={src} alt={`Thumbnail ${i + 1}`} /></a>
              ))}
            </div>
          )}
          {m.titles?.map((t) => (
            <div key={t} className="spread titlerow">
              <span className="small">{t}</span>
              <button onClick={() => copy(t, "Title")}>Copy</button>
            </div>
          ))}
          {m.description && (
            <details>
              <summary className="small">Description with chapters</summary>
              <pre className="small description">{m.description}</pre>
              <button onClick={() => copy(m.description!, "Description")}>Copy description</button>
            </details>
          )}
          <div className="row" style={{ marginTop: 8 }}>
            {m.video && <a className="button primary" href={`${m.video}?download=1`}>Download</a>}
            {m.status !== "queued" && m.status !== "running" && <button className="danger" onClick={() => remove(m.id)}>Delete</button>}
          </div>
        </div>
      ))}
      {note && <div className="toast" onClick={() => setNote("")}>{note}</div>}
    </>
  );
}
