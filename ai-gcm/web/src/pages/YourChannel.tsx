import { useEffect, useState } from "react";
import { Link } from "react-router";
import { api } from "../api";

type Totals = { views: number; minutes: number; subscribers: number };
type Stats = { start: string; end: string; through: string | null; by_type: Record<"shorts" | "live" | "videos" | "other", Totals> };
type Upload = { id: string; title: string; at: string | null; kind: "shorts" | "live" | "videos"; views: number | null; kaatclip: boolean; url: string };
export type ChannelView = {
  id: string; title: string; thumbnail: string | null; status: string; stats: Stats | null; stats_at: string | null;
  recent_at: string | null; uploads: Upload[];
};

const KINDS: [keyof Stats["by_type"], string][] = [["shorts", "Shorts"], ["live", "Live"], ["videos", "Videos"]];

export function compact(n: number | null | undefined): string {
  if (n === null || n === undefined) return "–";
  if (n >= 10_000_000) return `${Math.round(n / 1_000_000)}M`;
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 10_000) return `${Math.round(n / 1000)}K`;
  if (n >= 1000) return `${(n / 1000).toFixed(1)}K`;
  return String(n);
}

const shortDate = (day: string) => new Date(day.length === 10 ? `${day}T12:00:00` : day)
  .toLocaleDateString("en-IN", { weekday: "short", day: "numeric", month: "short" });

function ChannelCard({ channel }: { channel: ChannelView }) {
  const [open, setOpen] = useState(false);
  const stats = channel.stats;
  const total = stats ? KINDS.reduce((sum, [k]) => sum + stats.by_type[k].views, 0) + stats.by_type.other.views : 0;
  return (
    <div className="card" aria-label={`Your channel ${channel.title}`}>
      <div className="spread">
        <span className="title">{channel.title}</span>
        {stats?.through && <span className="small muted">data through {shortDate(stats.through)}</span>}
      </div>
      {channel.status !== "ok" && (
        <p className="small">The connection has expired. <Link to="/settings">Reconnect in Settings</Link> to see your numbers.</p>
      )}
      {stats && (
        <>
          <div className="small muted" style={{ marginTop: 4 }}>Last 28 days: {compact(total)} views</div>
          <div className="kinds">
            {KINDS.map(([kind, label]) => {
              const t = stats.by_type[kind];
              const share = total ? Math.round((t.views / total) * 100) : 0;
              return (
                <div key={kind} className="kind">
                  <div className="small muted">{label}</div>
                  <div className="title">{compact(t.views)}</div>
                  <div className="small muted">{share}% · {t.subscribers >= 0 ? "+" : ""}{compact(t.subscribers)} subs</div>
                  <div className="bar"><div style={{ width: `${share}%` }} /></div>
                </div>
              );
            })}
          </div>
        </>
      )}
      {!stats && channel.status === "ok" && <p className="small muted">YouTube's numbers aren't in yet. Look again in a while.</p>}
      {channel.uploads.length > 0 && (
        <>
          <button className="chip" style={{ marginTop: 8 }} onClick={() => setOpen(!open)}>
            {open ? "Hide recent uploads" : `Recent uploads (${channel.uploads.length})`}
          </button>
          {open && channel.uploads.map((u) => (
            <a key={u.id} href={u.url} target="_blank" rel="noreferrer" className="row small"
               style={{ flexWrap: "nowrap", margin: "8px 0", color: "inherit", textDecoration: "none" }}>
              <span className={`chip ${u.kind === "live" ? "failed" : u.kind === "shorts" ? "running" : ""}`}>
                {u.kind === "shorts" ? "Short" : u.kind === "live" ? "Live" : "Video"}
              </span>
              <span style={{ flex: 1, minWidth: 0, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                {u.title || "Untitled"}{u.kaatclip ? " · Kaatclip" : ""}
              </span>
              <span className="muted">{compact(u.views)}</span>
            </a>
          ))}
        </>
      )}
    </div>
  );
}

// "Your channel" on the streams page: each connected channel's last 28 days by Shorts, live and videos, and its
// recent uploads. YouTube's numbers lag 2-3 days, hence "data through".
export default function YourChannel() {
  const [channels, setChannels] = useState<ChannelView[] | null>(null);
  useEffect(() => {
    api<{ channels: ChannelView[] }>("/api/channel").then((r) => setChannels(r.channels), () => setChannels([]));
  }, []);
  if (channels === null) return null;
  if (channels.length === 0) {
    return (
      <p className="small muted">
        <Link to="/settings">Connect YouTube</Link> to see your channel's Shorts, live and video numbers here.
      </p>
    );
  }
  return (
    <>
      <h2>Your channel</h2>
      {channels.map((c) => <ChannelCard key={c.id} channel={c} />)}
    </>
  );
}
