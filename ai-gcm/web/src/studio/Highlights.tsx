import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router";
import { api } from "../api";
import { duration } from "../format";

// Highlights Stage 1 (plans/Highlights Stage 1 plan.md): the stream map and the kill-match highlights made
// from it, with the Shorts cut from each, and one stream's batch of posts at suggested times.

export type MapPart = { start: number; end: number; kind: "match" | "between" | "not_bgmi"; match?: number; why?: string };
export type MapMatch = {
  n: number; start: number; end: number; ended: string; placement: number | null; kills: number; score: number;
  fights: number; map: string | null; mode: string | null;
};
export type StreamMap = { duration: number; parts: MapPart[]; matches: MapMatch[]; best: number | null; session: number[] };
export type HighlightPiece = {
  i: number; kind: string; text?: string; start?: number; end?: number; length?: number; kills?: number;
  title?: string | null; match?: number; punch?: number;
};
export type Highlight = {
  id: string; status: "queued" | "running" | "done" | "failed"; error: string | null; stream_id: string;
  matches: number[] | null; session: boolean; auto: boolean; created_at: string | null;
  length_s?: number; kept?: number; kills?: number; label?: "main" | "second"; titles?: string[]; description?: string;
  pieces?: HighlightPiece[]; dropped?: number[]; video?: string; play?: string; thumbnails?: string[];
  shorts?: { clip_id: number; title: string | null; role: string; length_s: number; poster: string; decision: string | null }[];
  posts?: { id: string; status: string; publish_at: string | null }[];
};
export type StreamHighlights = {
  map: StreamMap | null; map_status: string | null; has_source: boolean; highlights: Highlight[];
  leftovers?: { count: number; until: string | null };
};

const PIECE_LABEL: Record<string, string> = {
  intro: "Opening (IN THIS VIDEO)", teaser: "Opening (IN THIS VIDEO)", drop: "The drop", fight: "Fight", talk: "Talk",
  marked: "You marked this", ending: "Ending",
};

function ending(m: MapMatch) {
  if (m.ended === "dinner" || m.placement === 1) return "🏆 Chicken Dinner";
  if (m.placement) return `#${m.placement}`;
  if (m.ended === "death") return "died";
  if (m.ended === "cut_off") return "recording ends";
  return "";
}

function when(iso: string | null) {
  if (!iso) return "";
  return new Date(iso).toLocaleString("en-IN", { weekday: "short", day: "numeric", month: "short", hour: "numeric", minute: "2-digit" });
}

export function MapBar({ map }: { map: StreamMap }) {
  const total = map.duration || 1;
  return (
    <div className="mapbar" aria-label="Stream map">
      {map.parts.map((p) => (
        <div key={`${p.start}-${p.kind}`} className={`mapbar-part ${p.kind}${p.match === map.best ? " best" : ""}`}
             style={{ width: `${((p.end - p.start) / total) * 100}%` }}
             title={p.kind === "match" ? `Match ${p.match}` : p.kind === "between" ? "Lobby and menus" : (p.why ?? "Not BGMI")}>
          {p.kind === "match" && (p.end - p.start) / total > 0.04 ? p.match : ""}
        </div>
      ))}
    </div>
  );
}

function HighlightCard({ h, onChange }: { h: Highlight; onChange: () => void }) {
  const [off, setOff] = useState<Set<number>>(new Set());
  const [note, setNote] = useState("");
  const [busy, setBusy] = useState(false);

  async function again() {
    setBusy(true);
    try {
      await api(`/api/streams/${h.stream_id}/highlights`, {
        method: "POST", body: { matches: h.matches, session: h.session, drop: [...off] },
      });
      setOff(new Set());
      onChange();
    } catch (err) {
      setNote((err as Error).message);
    } finally {
      setBusy(false);
    }
  }

  async function planPosts() {
    setBusy(true);
    try {
      const got = await api<{ posts: { id: string; publish_at: string | null }[]; waiting: number[] }>(
        `/api/highlights/${h.id}/plan-posts`, { method: "POST" });
      setNote(`${got.posts.length} draft${got.posts.length === 1 ? "" : "s"} in Posts, not approved yet.` +
        (got.waiting.length ? ` ${got.waiting.length} Short${got.waiting.length === 1 ? " is" : "s are"} still being made; tap Plan again in a few minutes.` : ""));
      onChange();
    } catch (err) {
      setNote((err as Error).message);
    } finally {
      setBusy(false);
    }
  }

  async function remove() {
    if (!confirm("Delete this highlight video? Its Shorts stay with the stream's clips.")) return;
    try {
      await api(`/api/highlights/${h.id}`, { method: "DELETE" });
      onChange();
    } catch (err) {
      setNote((err as Error).message);
    }
  }

  async function copy(text: string) {
    try {
      await navigator.clipboard.writeText(text);
      setNote("Copied");
    } catch {
      setNote("Couldn't copy here");
    }
  }

  const what = h.session ? "Session" : `Match ${(h.matches ?? []).join(", ") || "best"}`;
  if (h.status !== "done") {
    return (
      <div className="card">
        <div className="spread"><div className="title">{what}</div><span className={`chip ${h.status}`}>{h.status === "failed" ? "Failed" : "Making…"}</span></div>
        {h.status === "failed" ? <p className="error small">{h.error}</p>
          : <p className="small muted">Cutting the highlight and its Shorts. A 10-minute video takes about 15 minutes.</p>}
        {h.status === "failed" && <button className="danger" onClick={remove}>Delete</button>}
      </div>
    );
  }
  const pieces = h.pieces ?? [];
  return (
    <div className="card">
      <div className="spread">
        <div className="title">{what} · {h.kills} kills · {duration(h.length_s ?? 0)}</div>
        <span className="chip done">Ready</span>
      </div>
      <video className="highlight-video" src={h.play} controls preload="metadata" playsInline />
      <p className="small muted">
        Keeps {Math.round((h.kept ?? 0) * 100)}% of the match. Suggested for your{" "}
        <b>{h.label === "main" ? "main channel (a record match)" : "second channel (a match cut)"}</b>.
      </p>
      {h.thumbnails && h.thumbnails.length > 0 && (
        <div className="row thumbs">{h.thumbnails.map((t) => <img key={t} src={t} alt="Thumbnail" />)}</div>
      )}
      <h3>Titles</h3>
      {(h.titles ?? []).map((t) => (
        <div key={t} className="row small" style={{ flexWrap: "nowrap" }}>
          <span style={{ flex: 1, minWidth: 0, overflowWrap: "anywhere" }}>{t}</span>
          <button className="chip" onClick={() => copy(t)}>Copy</button>
        </div>
      ))}
      {h.shorts && h.shorts.length > 0 && (
        <>
          <h3>Shorts from it</h3>
          {h.shorts.map((s) => (
            <Link key={s.clip_id} className="row short-row" to={`/clips/${s.clip_id}/studio`}>
              <img src={s.poster} alt="" />
              <span>{s.role === "teaser" ? "Teaser" : "Best fight"} · {s.title} · {Math.round(s.length_s)} s</span>
            </Link>
          ))}
        </>
      )}
      <details>
        <summary>What's in it ({pieces.filter((p) => p.kind !== "card").length} parts)</summary>
        <p className="small muted">Untick a part and tap Make again to leave it out.</p>
        {pieces.map((p) => p.kind === "card" ? (
          p.text ? <div key={p.i} className="small muted piece-card">— {p.text} —</div> : null
        ) : (
          <label key={p.i} className="row small piece">
            <input type="checkbox" checked={!off.has(p.i)}
                   onChange={(e) => setOff((was) => { const next = new Set(was); if (e.target.checked) next.delete(p.i); else next.add(p.i); return next; })} />
            <span>{PIECE_LABEL[p.kind] ?? p.kind}{p.title ? `: ${p.title}` : ""}{p.kills ? ` · ${p.kills} kill${p.kills > 1 ? "s" : ""}` : ""}
              {" · "}{Math.round(p.length ?? 0)} s{p.punch ? " · face zoom" : ""}</span>
          </label>
        ))}
        <button disabled={busy || off.size === 0} onClick={again}>Make again</button>
      </details>
      {h.posts && h.posts.length > 0 && (
        <p className="small">Planned: {h.posts.map((p) => `${p.status} ${when(p.publish_at)}`).join(", ")} · <Link to="/posts">Open Posts</Link></p>
      )}
      <div className="row" style={{ marginTop: 8 }}>
        <button className="primary" disabled={busy} onClick={planPosts}>Plan the posts</button>
        <a className="button" href={`${h.video}?download=1`}>Download</a>
        <button className="danger" onClick={remove}>Delete</button>
      </div>
      <p className="small muted">Plan the posts puts the highlight (tomorrow noon) and its Shorts (teaser tonight, the others on the next evenings) in Posts as drafts. Nothing posts until you approve it.</p>
      {note && <p className="small">{note}</p>}
    </div>
  );
}

export default function Highlights({ streamId }: { streamId: string }) {
  const [data, setData] = useState<StreamHighlights | null>(null);
  const [note, setNote] = useState("");

  const load = useCallback(() => {
    api<StreamHighlights>(`/api/streams/${streamId}/highlights`).then(setData).catch((err) => setNote((err as Error).message));
  }, [streamId]);
  useEffect(load, [load]);

  const waiting = !!data && (data.map_status === "queued" || data.map_status === "running" ||
    data.highlights.some((h) => h.status === "queued" || h.status === "running"));
  useEffect(() => {
    if (!waiting) return;
    const timer = window.setInterval(load, 4000);
    return () => window.clearInterval(timer);
  }, [waiting, load]);

  async function make(body: { matches?: number[]; session?: boolean }) {
    setNote("");
    try {
      await api(`/api/streams/${streamId}/highlights`, { method: "POST", body });
      load();
    } catch (err) {
      setNote((err as Error).message);
    }
  }

  async function makeMap() {
    try {
      await api(`/api/streams/${streamId}/map`, { method: "POST" });
      load();
    } catch (err) {
      setNote((err as Error).message);
    }
  }

  if (!data) return note ? <p className="error small">{note}</p> : null;
  const map = data.map;
  return (
    <>
      <h2>Highlights</h2>
      {!map && (
        <div className="card">
          {data.map_status === "queued" || data.map_status === "running"
            ? <p className="small muted">Finding the matches in this stream…</p>
            : <>
                <p className="small muted">Find the matches in this stream, then make a highlight of the best one.</p>
                <button className="primary" onClick={makeMap}>Find the matches</button>
              </>}
        </div>
      )}
      {map && (
        <div className="card">
          <MapBar map={map} />
          <p className="small muted">Matches in colour, lobby in grey{map.parts.some((p) => p.kind === "not_bgmi") ? ", not BGMI dotted (not used)" : ""}.</p>
          {map.matches.length === 0 && <p className="small">No BGMI match found in this stream.</p>}
          {map.matches.map((m) => (
            <div key={m.n} className="row small match-row">
              <span style={{ flex: 1, minWidth: 0 }}>
                <b>Match {m.n}</b>{m.n === map.best ? " ⭐" : ""} · {m.kills} kill{m.kills === 1 ? "" : "s"}
                {ending(m) ? ` · ${ending(m)}` : ""} · {duration(m.end - m.start)}{m.map ? ` · ${m.map[0].toUpperCase()}${m.map.slice(1)}` : ""}
              </span>
              {data.has_source && m.kills > 0 && <button className="chip" onClick={() => make({ matches: [m.n] })}>Make highlight</button>}
            </div>
          ))}
          {data.has_source && map.session.length >= 2 && (
            <button onClick={() => make({ session: true })}>Make a session video (matches {map.session.join(", ")})</button>
          )}
          {!data.has_source && <p className="small muted">The recording is no longer on the laptop, so no new highlights can be cut.</p>}
          {data.leftovers && data.leftovers.count > 0 && data.highlights.length > 0 && (
            <p className="small muted">
              {data.leftovers.count} fight{data.leftovers.count === 1 ? "" : "s"} with kills not in any highlight yet
              {data.leftovers.until ? `, kept until ${new Date(data.leftovers.until).toLocaleDateString("en-IN", { day: "numeric", month: "short" })}` : ""} for a part 2.
            </p>
          )}
          <button className="chip" onClick={makeMap}>Find the matches again</button>
        </div>
      )}
      {data.highlights.map((h) => <HighlightCard key={h.id} h={h} onChange={load} />)}
      {note && <p className="error small">{note}</p>}
    </>
  );
}
