import { useCallback, useEffect, useRef, useState } from "react";
import { Link, useSearchParams } from "react-router";
import { api, type LibraryPage } from "../api";

const PAGE = 40;
const DECISIONS: [string, string][] = [["keep", "Kept"], ["none", "Not reviewed"], ["reject", "Rejected"], ["all", "All"]];
const TOGGLES: [string, string][] = [["edited", "Edited"], ["exported", "Exported"], ["flag", "Flagged"]];
const TYPE_NAMES: Record<string, string> = {
  multi_kill: "Multi-kill", fight: "Fight", clutch: "Clutch", win: "Win", reaction: "Reaction", funny: "Funny",
  rage: "Rage", banter: "Banter", marked: "Marked", moment: "Moment",
};

function typeName(type: string) {
  return TYPE_NAMES[type] ?? type.replace(/_/g, " ");
}

// M3.2: every clip from every stream, two posters to a row, filtered and searched a page at a time.
// Filters live in the address, so going back from a clip returns to the same view.
export default function Library() {
  const [params, setParams] = useSearchParams();
  const decision = params.get("decision") ?? "keep";
  const [query, setQuery] = useState(params.get("q") ?? "");
  const [page, setPage] = useState<LibraryPage | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const sentinel = useRef<HTMLDivElement>(null);
  const request = useRef(0);

  const filters = new URLSearchParams();
  if (decision !== "all") filters.set("decision", decision);
  for (const key of ["q", "stream", "type", "edited", "exported", "flag", "sort"]) {
    const value = params.get(key);
    if (value) filters.set(key, value);
  }
  const filterKey = filters.toString();

  const fetchPage = useCallback(async (offset: number) => {
    const ticket = ++request.current;
    setLoading(true);
    try {
      const next = await api<LibraryPage>(`/api/library?${filterKey}&offset=${offset}&limit=${PAGE}`);
      if (ticket !== request.current) return;   // a newer search replaced this one
      setPage((before) => (offset === 0 || !before ? next : { ...next, items: [...before.items, ...next.items] }));
      setError("");
    } catch (err) {
      if (ticket === request.current) setError((err as Error).message);
    } finally {
      if (ticket === request.current) setLoading(false);
    }
  }, [filterKey]);

  useEffect(() => {
    fetchPage(0);
  }, [fetchPage]);

  // Typing searches after a short pause, not on every key.
  useEffect(() => {
    const timer = window.setTimeout(() => {
      if ((params.get("q") ?? "") !== query.trim()) update("q", query.trim() || null);
    }, 350);
    return () => window.clearTimeout(timer);
  });

  const more = page !== null && page.items.length < page.total;
  useEffect(() => {
    const el = sentinel.current;
    if (!el || !more) return;
    const watcher = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting && !loading) fetchPage(page!.items.length);
    }, { rootMargin: "600px" });
    watcher.observe(el);
    return () => watcher.disconnect();
  }, [more, loading, page, fetchPage]);

  function update(key: string, value: string | null) {
    const next = new URLSearchParams(params);
    if (value === null) next.delete(key);
    else next.set(key, value);
    setParams(next, { replace: true });
  }

  const facets = page?.facets;
  return (
    <>
      <h1>Library</h1>
      <input type="search" placeholder="Search what was said or the title" value={query}
             onChange={(e) => setQuery(e.target.value)} aria-label="Search clips" />
      <div className="chips" role="group" aria-label="Filters">
        {DECISIONS.map(([key, label]) => (
          <button key={key} className={decision === key ? "chip on" : "chip"} onClick={() => update("decision", key)}>
            {label}
          </button>
        ))}
        {TOGGLES.map(([key, label]) => (
          <button key={key} className={params.get(key) ? "chip on" : "chip"}
                  onClick={() => update(key, params.get(key) ? null : "1")}>{label}</button>
        ))}
      </div>
      <div className="row filters">
        <select value={params.get("stream") ?? ""} onChange={(e) => update("stream", e.target.value || null)}
                aria-label="Stream">
          <option value="">All streams</option>
          {facets?.streams.map((s) => <option key={s.id} value={s.id}>{s.title.slice(0, 60)} ({s.count})</option>)}
        </select>
        <select value={params.get("type") ?? ""} onChange={(e) => update("type", e.target.value || null)}
                aria-label="Clip type">
          <option value="">All types</option>
          {facets?.types.map((t) => <option key={t.type} value={t.type}>{typeName(t.type)} ({t.count})</option>)}
        </select>
        <select value={params.get("sort") ?? ""} onChange={(e) => update("sort", e.target.value || null)}
                aria-label="Order">
          <option value="">Newest streams</option>
          <option value="score">Best first</option>
        </select>
      </div>

      {page && <p className="small muted">{page.total} clip{page.total === 1 ? "" : "s"}</p>}
      {page?.total === 0 && (
        <p className="muted">{decision === "keep" && !filterKey.includes("q=")
          ? "Keep clips while reviewing a stream and they collect here."
          : "No clips match. Try fewer filters."}</p>
      )}
      <div className="grid">
        {page?.items.map((clip) => (
          <Link key={clip.id} to={`/clips/${clip.id}/studio`} className="tile">
            <div className="poster">
              {clip.poster
                ? <img src={clip.poster} alt="" loading="lazy" decoding="async" />
                : <div className="noposter">{typeName(clip.type)}</div>}
              <span className="length">{Math.round(clip.length_s)}s</span>
              <span className="badges">
                {clip.decision === "keep" && <span title="Kept">✓</span>}
                {clip.edited && <span title="Edited">✎</span>}
                {clip.exported && <span title="Exported">⬇</span>}
                {clip.flags.length > 0 && <span title="Flagged" className="flagged">!</span>}
              </span>
            </div>
            <div className="tiletitle">{clip.title ?? `Clip ${clip.rank}`}</div>
            <div className="small muted tilesub">{typeName(clip.type)} · {clip.stream_title}</div>
          </Link>
        ))}
      </div>
      <div ref={sentinel} />
      {more && <button style={{ width: "100%", marginTop: 12 }} disabled={loading}
                       onClick={() => fetchPage(page!.items.length)}>{loading ? "Loading…" : "Load more"}</button>}
      {page === null && !error && <p className="muted">Loading…</p>}
      {error && <p className="error">{error}</p>}
    </>
  );
}
