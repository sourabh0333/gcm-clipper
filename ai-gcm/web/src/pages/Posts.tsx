import { useEffect, useState } from "react";
import { Link } from "react-router";
import { api, type Post, type Quota } from "../api";
import { POST_LABEL, when } from "../format";

type BatchResult = { approved: Post[]; problems: { id: string; error: string }[] };

const SECTIONS: { title: string; statuses: Post["status"][] }[] = [
  { title: "Approved and scheduled", statuses: ["approved", "uploading", "scheduled"] },
  { title: "Posted", statuses: ["posted"] },
  { title: "Failed or cancelled", statuses: ["failed", "cancelled"] },
];

function Row({ post, pick }: { post: Post; pick?: { on: boolean; toggle: () => void } }) {
  return (
    <div className="card row" style={{ flexWrap: "nowrap" }}>
      {pick && <input type="checkbox" checked={pick.on} onChange={pick.toggle} aria-label={`Pick ${post.title || "untitled"}`} />}
      {post.cover && <img src={post.cover} alt="" width={45} height={80} style={{ objectFit: "cover", borderRadius: 6 }} />}
      <Link to={`/posts/${post.id}`} style={{ flex: 1, minWidth: 0, color: "inherit", textDecoration: "none" }}>
        <div className="title">{post.title || "Untitled"}</div>
        <div className="small muted">
          {post.channel?.title ?? "No channel"} · {post.mode === "now" ? "post now" : when(post.publish_at) || "no time yet"}
        </div>
      </Link>
      <span className={`chip ${post.status}`}>{POST_LABEL[post.status]}</span>
    </div>
  );
}

// Every post: drafts to approve (one by one, or an explicit list at once), then what's on its way and done.
// The calendar views come in M4.4.
export default function Posts() {
  const [posts, setPosts] = useState<Post[] | null>(null);
  const [picked, setPicked] = useState<string[]>([]);
  const [confirming, setConfirming] = useState(false);
  const [problems, setProblems] = useState<{ id: string; error: string }[]>([]);
  const [error, setError] = useState("");
  const [quota, setQuota] = useState<Quota | null>(null);

  const load = () => api<Post[]>("/api/posts").then(setPosts, (err) => setError((err as Error).message));
  useEffect(() => {
    load();
    api<Quota>("/api/posts/quota").then(setQuota, () => {});   // the owner only
  }, []);
  // While something is uploading or waiting to go public, look again every 15 seconds.
  const active = posts?.some((p) => p.status === "approved" || p.status === "uploading");
  useEffect(() => {
    if (!active) return;
    const timer = window.setInterval(load, 15000);
    return () => window.clearInterval(timer);
  }, [active]);

  if (!posts) return error ? <p className="error">{error}</p> : <p className="muted">Loading…</p>;
  const drafts = posts.filter((p) => p.status === "draft");
  const chosen = drafts.filter((p) => picked.includes(p.id));
  const toggle = (id: string) => { setPicked((ids) => (ids.includes(id) ? ids.filter((x) => x !== id) : [...ids, id])); setConfirming(false); };

  async function approveChosen() {
    try {
      const result = await api<BatchResult>("/api/posts/approve",
        { body: { posts: chosen.map((p) => ({ id: p.id, seen: p.updated_at })) } });
      setProblems(result.problems);
      setPicked(result.problems.map((p) => p.id));
      setConfirming(false);
      await load();
    } catch (err) {
      setError((err as Error).message);
    }
  }

  const titleOf = (id: string) => posts.find((p) => p.id === id)?.title || "Untitled";

  return (
    <>
      <h1>Posts</h1>
      {posts.length === 0 && (
        <p className="muted">No posts yet. Open a clip in the Library, export it, and tap <b>Post to YouTube</b>.</p>
      )}

      {drafts.length > 0 && (
        <>
          <h2>Drafts ({drafts.length})</h2>
          {drafts.map((p) => <Row key={p.id} post={p} pick={{ on: picked.includes(p.id), toggle: () => toggle(p.id) }} />)}
          {chosen.length > 0 && !confirming && (
            <button className="primary" onClick={() => setConfirming(true)}>
              Approve {chosen.length} post{chosen.length > 1 ? "s" : ""}
            </button>
          )}
          {confirming && (
            <div className="card" role="dialog" aria-label="Approve these posts">
              <div className="title">
                {chosen.length === 1 ? "Approve this post exactly as it is?" : `Approve these ${chosen.length} posts exactly as they are?`}
              </div>
              <ol className="small">
                {chosen.map((p) => (
                  <li key={p.id}>
                    <b>{p.title || "Untitled"}</b> to {p.channel?.title ?? "no channel"},{" "}
                    {p.mode === "now" ? "public as soon as it uploads" : `public ${when(p.publish_at)}`}
                  </li>
                ))}
              </ol>
              <p className="small muted">Each uploads with the title, description and tags on its own page. Open one to check it first.</p>
              <div className="row">
                <button className="primary" onClick={approveChosen}>Approve {chosen.length}</button>
                <button onClick={() => setConfirming(false)}>Not yet</button>
              </div>
            </div>
          )}
          {problems.map((p) => (
            <p key={p.id} className="small error">{titleOf(p.id)}: {p.error}</p>
          ))}
        </>
      )}

      {SECTIONS.map(({ title, statuses }) => {
        const rows = posts.filter((p) => statuses.includes(p.status));
        return rows.length > 0 && (
          <div key={title}>
            <h2>{title} ({rows.length})</h2>
            {rows.map((p) => <Row key={p.id} post={p} />)}
          </div>
        );
      })}
      {quota && (
        <p className="small muted">
          YouTube today (whole app): {quota.uploads} of {quota.uploads_limit} uploads · {quota.units} of {quota.units_limit} units
        </p>
      )}
      {error && <p className="error">{error}</p>}
    </>
  );
}
