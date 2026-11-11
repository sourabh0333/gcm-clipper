import { useCallback, useEffect, useState } from "react";
import { Link, useNavigate } from "react-router";
import { api, type Post } from "../api";
import { POST_LABEL } from "../format";

export type CalendarPost = Post & { day: string; at: string };
export type Gauge = {
  channel: string; shorts: number; uploads: number; planned: number; share: number; warn: boolean; limit: number;
  days: number; ahead: number; as_of: string | null;
};
export type Live = { id: string; title: string; start: string; channel: string; day: string; teased: boolean; can_tease: boolean };
type CalendarData = { start: string; days: number; posts: CalendarPost[]; unscheduled: Post[]; gauge: Gauge | null; lives?: Live[] };
type FillResult = { placed: Post[]; free_left: number; exports_left: number; drafts_left: number };
type BatchResult = { approved: Post[]; problems: { id: string; error: string }[] };

export const TZ = Intl.DateTimeFormat().resolvedOptions().timeZone || "Asia/Kolkata";

// Calendar days are the phone's own dates, as YYYY-MM-DD.
export function ymd(d: Date): string {
  const pad = (n: number) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
}
export function parseDay(day: string): Date {
  const [y, m, d] = day.split("-").map(Number);
  return new Date(y, m - 1, d);
}
export function addDays(day: string, n: number): string {
  const d = parseDay(day);
  d.setDate(d.getDate() + n);
  return ymd(d);
}
export function mondayOf(day: string): string {
  const d = parseDay(day);
  return addDays(day, -((d.getDay() + 6) % 7));
}
const dayName = (day: string) => parseDay(day).toLocaleDateString("en-IN", { weekday: "short", day: "numeric", month: "short" });
const clockOf = (iso: string) => new Date(iso).toLocaleTimeString("en-IN", { hour: "numeric", minute: "2-digit" });

export function GaugeCard({ gauge }: { gauge: Gauge | null }) {
  if (!gauge) return null;
  const pct = Math.round(gauge.share * 100);
  return (
    <div className="card" aria-label="Shorts share">
      <div className="spread">
        <span className="title">Shorts share: {pct}%</span>
        <span className={`chip ${gauge.warn ? "failed" : "done"}`}>{gauge.warn ? `above ${Math.round(gauge.limit * 100)}%` : "fine"}</span>
      </div>
      <div className="bar" style={{ marginTop: 8 }}>
        <div style={{ width: `${Math.min(100, pct)}%`, background: gauge.warn ? "var(--reject)" : undefined }} />
      </div>
      <div className="small muted" style={{ marginTop: 6 }}>
        {gauge.shorts} Shorts of {gauge.uploads} uploads on {gauge.channel}: the last {gauge.days} days
        {gauge.planned ? ` and ${gauge.planned} planned for the next ${gauge.ahead}` : ""}.
        {gauge.warn && " Channels that post mostly Shorts can grow slower; space them out, or add a weekly compilation."}
      </div>
    </div>
  );
}

function PostCard({ post, moving, onMove }: { post: CalendarPost; moving: boolean; onMove?: () => void }) {
  return (
    <div className="card row" style={{ flexWrap: "nowrap", margin: "6px 0", outline: moving ? "2px solid var(--accent)" : undefined }}>
      <span className="small" style={{ width: 58, flex: "none" }}>{clockOf(post.at)}</span>
      <Link to={`/posts/${post.id}`} style={{ flex: 1, minWidth: 0, color: "inherit", textDecoration: "none" }}>
        <div className="title">{post.title || "Untitled"}</div>
        <div className="small muted">{post.channel?.title ?? "No channel"}</div>
      </Link>
      {onMove && <button className="chip" onClick={onMove}>{moving ? "Cancel" : "Move"}</button>}
      <span className={`chip ${post.status}`}>{POST_LABEL[post.status]}</span>
    </div>
  );
}

export function useCalendar(start: string, days: number) {
  const [data, setData] = useState<CalendarData | null>(null);
  const [error, setError] = useState("");
  const load = useCallback(() => api<CalendarData>(`/api/calendar?start=${start}&days=${days}&tz=${encodeURIComponent(TZ)}`)
    .then(setData, (err) => setError((err as Error).message)), [start, days]);
  useEffect(() => { load(); }, [load]);
  return { data, error, load, setError };
}

// A week, Monday to Sunday: each evening's posts, moving a draft to another day in two taps, filling the free
// evenings with drafts, and approving the week's drafts as one listed batch.
export function WeekView({ start, setStart }: { start: string; setStart: (day: string) => void }) {
  const { data, error, load, setError } = useCalendar(start, 7);
  const [moving, setMoving] = useState<CalendarPost | null>(null);
  const [note, setNote] = useState("");
  const [confirming, setConfirming] = useState(false);
  const [problems, setProblems] = useState<{ id: string; error: string }[]>([]);
  const navigate = useNavigate();
  const today = ymd(new Date());

  if (!data) return error ? <p className="error">{error}</p> : <p className="muted">Loading…</p>;
  const days = Array.from({ length: 7 }, (_, i) => addDays(start, i));
  const drafts = data.posts.filter((p) => p.status === "draft");

  async function moveTo(day: string) {
    if (!moving) return;
    const old = new Date(moving.at);
    const target = parseDay(day);
    target.setHours(old.getHours(), old.getMinutes(), 0, 0);
    try {
      await api(`/api/posts/${moving.id}/time`, { method: "PUT", body: { publish_at: target.toISOString() } });
      setMoving(null);
      setNote(`Moved to ${dayName(day)}.`);
      await load();
    } catch (err) {
      setError((err as Error).message);
    }
  }

  async function makeTeaser(live: Live) {
    try {
      const post = await api<Post>("/api/calendar/teaser", { body: { live_id: live.id, tz: TZ } });
      navigate(`/posts/${post.id}`);     // check the teaser's title and text, then approve it
    } catch (err) {
      setError((err as Error).message);
    }
  }

  async function fillWeek() {
    try {
      const result = await api<FillResult>("/api/calendar/fill", { body: { tz: TZ, start: start < today ? today : start, days: 7 } });
      setNote(result.placed.length
        ? `Planned ${result.placed.length} draft${result.placed.length > 1 ? "s" : ""} at 7 pm. Check them, then approve the week.`
        : result.free_left
          ? "No finished exports left to plan. Export more kept clips in the Library."
          : "Every evening this week already has a post.");
      await load();
    } catch (err) {
      setError((err as Error).message);
    }
  }

  async function approveWeek() {
    try {
      const result = await api<BatchResult>("/api/posts/approve",
        { body: { posts: drafts.map((p) => ({ id: p.id, seen: p.updated_at })) } });
      setProblems(result.problems);
      setConfirming(false);
      setNote(`${result.approved.length} approved.`);
      await load();
    } catch (err) {
      setError((err as Error).message);
    }
  }

  return (
    <>
      <div className="spread" style={{ margin: "8px 0" }}>
        <button className="chip" aria-label="Previous week" onClick={() => setStart(addDays(start, -7))}>‹</button>
        <button className="chip" onClick={() => setStart(mondayOf(today))}>{dayName(start)} – {dayName(addDays(start, 6))}</button>
        <button className="chip" aria-label="Next week" onClick={() => setStart(addDays(start, 7))}>›</button>
      </div>
      <GaugeCard gauge={data.gauge} />
      <div className="row" style={{ margin: "10px 0" }}>
        <button className="primary" onClick={fillWeek}>Fill empty evenings</button>
        {drafts.length > 0 && !confirming && (
          <button onClick={() => setConfirming(true)}>Approve the week ({drafts.length})</button>
        )}
      </div>
      {confirming && (
        <div className="card" role="dialog" aria-label="Approve the week">
          <div className="title">Approve these {drafts.length} exactly as they are?</div>
          <ol className="small">
            {drafts.map((p) => <li key={p.id}><b>{p.title || "Untitled"}</b> to {p.channel?.title ?? "no channel"}, public {dayName(p.day)} {clockOf(p.at)}</li>)}
          </ol>
          <p className="small muted">Each uploads with the title, description and tags on its own page. Tap one to check it first.</p>
          <div className="row">
            <button className="primary" onClick={approveWeek}>Approve {drafts.length}</button>
            <button onClick={() => setConfirming(false)}>Not yet</button>
          </div>
        </div>
      )}
      {note && <p className="small" role="status">{note}</p>}
      {problems.map((p) => <p key={p.id} className="small error">{data.posts.find((x) => x.id === p.id)?.title ?? "A post"}: {p.error}</p>)}
      {moving && <p className="small banner">Tap <b>Move here</b> on the day for “{moving.title || "Untitled"}”.</p>}
      {days.map((day) => {
        const rows = data.posts.filter((p) => p.day === day);
        const past = day < today;
        return (
          <section key={day} aria-label={dayName(day)}>
            <div className="spread" style={{ marginTop: 12 }}>
              <h3 style={{ margin: 0, opacity: past ? 0.6 : 1 }}>{dayName(day)}{day === today ? " · today" : ""}</h3>
              {moving && !past && moving.day !== day && <button className="chip" onClick={() => moveTo(day)}>Move here</button>}
            </div>
            {(data.lives ?? []).filter((l) => l.day === day).map((live) => (
              <div key={live.id} className="row small" style={{ margin: "6px 0", flexWrap: "nowrap" }}>
                <span style={{ flex: 1, minWidth: 0 }}>🔴 Live {clockOf(live.start)}: <b>{live.title || "your stream"}</b></span>
                {live.teased ? <span className="chip done">teaser planned</span>
                  : live.can_tease && <button className="chip" onClick={() => makeTeaser(live)}>Make a teaser</button>}
              </div>
            ))}
            {rows.length === 0 && <p className="small muted" style={{ margin: "4px 0" }}>{past ? "Nothing posted" : "Free evening"}</p>}
            {rows.map((p) => (
              <PostCard key={p.id} post={p} moving={moving?.id === p.id}
                        onMove={p.status === "draft" ? () => setMoving(moving?.id === p.id ? null : p) : undefined} />
            ))}
          </section>
        );
      })}
      {data.unscheduled.length > 0 && (
        <>
          <h2>Drafts without a time ({data.unscheduled.length})</h2>
          <p className="small muted">Fill empty evenings gives them a day, or open one to pick its time.</p>
          {data.unscheduled.map((p) => (
            <Link key={p.id} to={`/posts/${p.id}`} className="card" style={{ display: "block" }}>
              <div className="title">{p.title || "Untitled"}</div>
            </Link>
          ))}
        </>
      )}
      {error && <p className="error">{error}</p>}
    </>
  );
}

// A month at a glance: each day's posts as coloured marks; tap a day to open its week.
export function MonthView({ month, setMonth, openWeek }: { month: string; setMonth: (m: string) => void; openWeek: (day: string) => void }) {
  const first = `${month}-01`;
  const start = mondayOf(first);
  const { data, error } = useCalendar(start, 42);
  const today = ymd(new Date());
  const shift = (n: number) => {
    const d = parseDay(first);
    d.setMonth(d.getMonth() + n);
    setMonth(ymd(d).slice(0, 7));
  };
  if (!data) return error ? <p className="error">{error}</p> : <p className="muted">Loading…</p>;
  const label = parseDay(first).toLocaleDateString("en-IN", { month: "long", year: "numeric" });
  return (
    <>
      <div className="spread" style={{ margin: "8px 0" }}>
        <button className="chip" aria-label="Previous month" onClick={() => shift(-1)}>‹</button>
        <b>{label}</b>
        <button className="chip" aria-label="Next month" onClick={() => shift(1)}>›</button>
      </div>
      <GaugeCard gauge={data.gauge} />
      <div className="month">
        {["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"].map((d) => <div key={d} className="small muted">{d}</div>)}
        {Array.from({ length: 42 }, (_, i) => addDays(start, i)).map((day) => {
          const rows = data.posts.filter((p) => p.day === day);
          return (
            <button key={day} className={`monthday${day.slice(0, 7) !== month ? " other" : ""}${day === today ? " today" : ""}`}
                    onClick={() => openWeek(day)} aria-label={`${dayName(day)}: ${rows.length} post${rows.length === 1 ? "" : "s"}`}>
              <span>{parseDay(day).getDate()}</span>
              <span className="marks">{rows.slice(0, 3).map((p) => <i key={p.id} className={`mark ${p.status}`} />)}</span>
            </button>
          );
        })}
      </div>
      <p className="small muted">
        <i className="mark draft" /> draft <i className="mark scheduled" /> approved or scheduled <i className="mark posted" /> posted{" "}
        <i className="mark failed" /> failed
      </p>
    </>
  );
}
