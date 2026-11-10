import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router";
import { api, type Post, type YouTubeChannel, type YouTubeState } from "../api";
import { POST_LABEL, when } from "../format";

const TITLE_MAX = 100;

// datetime-local works in the phone's own clock; the server keeps UTC.
function toLocalInput(iso: string | null): string {
  if (!iso) return "";
  const d = new Date(iso);
  const pad = (n: number) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

// The next 7 pm at least an hour away: a sensible first time for a Short.
export function nextEvening(now = new Date()): string {
  const d = new Date(now);
  d.setHours(19, 0, 0, 0);
  if (d.getTime() < now.getTime() + 3600_000) d.setDate(d.getDate() + 1);
  return d.toISOString();
}

type Form = { title: string; description: string; tags: string; channel_id: string; mode: "schedule" | "now"; at: string };

function formFor(post: Post, channels: YouTubeChannel[]): Form {
  const ok = channels.filter((c) => c.status === "ok");
  return {
    title: post.title, description: post.description, tags: post.tags.join(", "),
    channel_id: post.channel?.id ?? ok[0]?.id ?? "", mode: post.mode,
    at: toLocalInput(post.publish_at ?? nextEvening()),
  };
}

// "Post this?": a post's exact title, description, channel and time, edited as a draft and then approved.
// Approving sends the version the creator was shown (its updated_at); the server refuses a stale one.
export default function PostPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [post, setPost] = useState<Post | null>(null);
  const [channels, setChannels] = useState<YouTubeChannel[]>([]);
  const [form, setForm] = useState<Form | null>(null);
  const [review, setReview] = useState<Post | null>(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    Promise.all([api<Post>(`/api/posts/${id}`), api<YouTubeState>("/api/youtube")]).then(([p, yt]) => {
      setPost(p);
      setChannels(yt.channels);
      setForm(formFor(p, yt.channels));
    }, (err) => setError((err as Error).message));
  }, [id]);

  if (!post || !form) return error ? <p className="error">{error}</p> : <p className="muted">Loading…</p>;
  const set = (change: Partial<Form>) => { setForm({ ...form, ...change }); setReview(null); };
  const draft = post.status === "draft";
  const channel = channels.find((c) => c.id === form.channel_id);

  async function save(): Promise<Post> {
    const body = {
      title: form!.title, description: form!.description, channel_id: form!.channel_id || null, mode: form!.mode,
      tags: form!.tags.split(/[,\n]/).map((t) => t.trim()).filter(Boolean),
      publish_at: form!.mode === "schedule" && form!.at ? new Date(form!.at).toISOString() : null,
    };
    const saved = await api<Post>(`/api/posts/${id}`, { method: "PUT", body });
    setPost(saved);
    return saved;
  }

  async function run(work: () => Promise<void>) {
    setBusy(true);
    setError("");
    try {
      await work();
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(false);
    }
  }

  const approve = () => run(async () => {
    const done = await api<Post>(`/api/posts/${id}/approve`, { body: { seen: review!.updated_at } });
    setPost(done);
    setReview(null);
  });

  const cancel = () => run(async () => {
    if (!confirm("Cancel this post? It won't be uploaded.")) return;
    setPost(await api<Post>(`/api/posts/${id}/cancel`, { method: "POST" }));
  });

  const remove = () => run(async () => {
    await api(`/api/posts/${id}`, { method: "DELETE" });
    navigate("/posts");
  });

  return (
    <>
      <p className="small"><Link to="/posts">← Posts</Link></p>
      <div className="spread">
        <h1 style={{ margin: 0 }}>{draft ? "Post this?" : post.title}</h1>
        <span className={`chip ${post.status}`}>{POST_LABEL[post.status]}</span>
      </div>
      {post.video && (
        <div className="card studio" style={{ marginTop: 12 }}>
          <video src={post.video} poster={post.cover ?? undefined} controls playsInline preload="metadata" />
        </div>
      )}

      {draft && (
        <div className="card brandform">
          <label htmlFor="p-channel">Channel</label>
          {channels.length === 0
            ? <p className="small">No YouTube channel connected. <Link to="/settings">Connect one in Settings</Link>.</p>
            : (
              <select id="p-channel" value={form.channel_id} onChange={(e) => set({ channel_id: e.target.value })}>
                <option value="">Pick a channel</option>
                {channels.map((c) => (
                  <option key={c.id} value={c.id} disabled={c.status !== "ok"}>
                    {c.title}{c.status !== "ok" ? " (reconnect in Settings)" : ""}
                  </option>
                ))}
              </select>
            )}

          <label htmlFor="p-title">Title</label>
          <input id="p-title" value={form.title} onChange={(e) => set({ title: e.target.value })} />
          <div className={`small ${form.title.length > TITLE_MAX ? "error" : "muted"}`}>{form.title.length}/{TITLE_MAX}</div>

          <label htmlFor="p-desc">Description</label>
          <textarea id="p-desc" rows={8} value={form.description} onChange={(e) => set({ description: e.target.value })} />

          <label htmlFor="p-tags">Tags</label>
          <input id="p-tags" value={form.tags} onChange={(e) => set({ tags: e.target.value })} placeholder="bgmi, clutch" />

          <label>When</label>
          <label className="tick">
            <input type="radio" name="mode" checked={form.mode === "schedule"} onChange={() => set({ mode: "schedule" })} />
            Schedule: YouTube makes it public at
          </label>
          {form.mode === "schedule" && (
            <input type="datetime-local" aria-label="Goes public at" value={form.at} onChange={(e) => set({ at: e.target.value })}
                   style={{ marginTop: 8 }} />
          )}
          <label className="tick">
            <input type="radio" name="mode" checked={form.mode === "now"} onChange={() => set({ mode: "now" })} />
            Post now: public as soon as it uploads
          </label>

          <div className="row" style={{ marginTop: 14 }}>
            <button className="primary" disabled={busy} onClick={() => run(async () => setReview(await save()))}>
              Review and approve
            </button>
            <button disabled={busy} onClick={() => run(async () => { await save(); })}>Save draft</button>
            <button className="danger" disabled={busy} onClick={remove}>Delete</button>
          </div>
        </div>
      )}

      {draft && review && (
        <div className="card" role="dialog" aria-label="Approve this post">
          <div className="title">Approve exactly this?</div>
          <dl className="small approval">
            <dt>Channel</dt><dd>{review.channel?.title ?? "none picked"}</dd>
            <dt>Goes public</dt><dd>{review.mode === "now" ? "As soon as it uploads" : when(review.publish_at)}</dd>
            <dt>Title</dt><dd>{review.title}</dd>
            <dt>Description</dt><dd style={{ whiteSpace: "pre-wrap" }}>{review.description || "(empty)"}</dd>
            <dt>Tags</dt><dd>{review.tags.join(", ") || "(none)"}</dd>
            <dt>Made for kids</dt><dd>{channel?.settings.made_for_kids ? "Yes" : "No"}</dd>
            <dt>Altered or AI-made</dt><dd>{channel?.settings.synthetic ? "Yes" : "No"}</dd>
          </dl>
          <p className="small muted">
            Approving uploads this video to {review.channel?.title ?? "the channel"}
            {review.mode === "now" ? " as public." : " as private, and YouTube makes it public at that time."} After
            it uploads, changes are made in YouTube Studio.
          </p>
          <div className="row">
            <button className="primary" disabled={busy} onClick={approve}>Approve</button>
            <button disabled={busy} onClick={() => setReview(null)}>Not yet</button>
          </div>
        </div>
      )}

      {!draft && (
        <div className="card">
          <dl className="small approval">
            <dt>Channel</dt><dd>{post.channel?.title ?? "disconnected"}</dd>
            <dt>Goes public</dt><dd>{post.mode === "now" ? "As soon as it uploads" : when(post.publish_at)}</dd>
            {post.approved_at && <><dt>Approved</dt><dd>{when(post.approved_at)}</dd></>}
            <dt>Description</dt><dd style={{ whiteSpace: "pre-wrap" }}>{post.description || "(empty)"}</dd>
            <dt>Tags</dt><dd>{post.tags.join(", ") || "(none)"}</dd>
          </dl>
          {post.status === "approved" && (
            <p className="small muted">Approved. The laptop uploads it to YouTube; you can cancel until the upload starts.</p>
          )}
          {post.error && <p className="small error">{post.error}</p>}
          {post.video_id && (
            <a className="button" href={`https://studio.youtube.com/video/${post.video_id}/edit`} target="_blank" rel="noreferrer">
              Change in YouTube Studio
            </a>
          )}
          <div className="row" style={{ marginTop: 10 }}>
            {(post.status === "approved" || post.status === "failed") && <button disabled={busy} onClick={cancel}>Cancel post</button>}
            {(post.status === "cancelled" || post.status === "failed") && (
              <button className="danger" disabled={busy} onClick={remove}>Delete</button>
            )}
          </div>
        </div>
      )}
      {error && <p className="error" role="alert">{error}</p>}
    </>
  );
}
