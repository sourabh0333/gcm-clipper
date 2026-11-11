import { useEffect, useRef, useState } from "react";
import { Link, useParams } from "react-router";
import { api, type Clip } from "../api";
import { clock, TYPE_LABEL } from "../format";

const REASONS: [string, string][] = [
  ["bad_cut", "Bad cut"],
  ["not_interesting", "Not interesting"],
  ["wrong_moment", "Wrong moment"],
  ["duplicate", "Duplicate"],
];
const SWIPE_PX = 90;

function readMuted() {
  try {
    return localStorage.getItem("kc-muted") !== "0";
  } catch {
    return true;
  }
}

export default function Review() {
  const { id } = useParams();
  const [clips, setClips] = useState<Clip[] | null>(null);
  const [index, setIndex] = useState(0);
  const [history, setHistory] = useState<number[]>([]);
  const [muted, setMuted] = useState(readMuted);
  // The next clip loads only once this one can play through, so the two don't share a slow link.
  const [buffered, setBuffered] = useState<number | null>(null);
  const [askReason, setAskReason] = useState<Clip | null>(null);
  const [error, setError] = useState("");
  const [drag, setDrag] = useState(0);
  const start = useRef<number | null>(null);
  const video = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    api<Clip[]>(`/api/streams/${id}/clips`)
      .then((all) => {
        setClips(all);
        const first = all.findIndex((c) => c.decision === null);
        setIndex(first === -1 ? 0 : first);
      })
      .catch((err) => setError((err as Error).message));
  }, [id]);

  const clip = clips?.[index];
  const next = clips?.[index + 1];

  async function decide(verdict: "keep" | "reject" | null, target: Clip, reason?: string) {
    const updated = await api<Clip>(`/api/clips/${target.id}/decision`, { body: { verdict, reason: reason ?? null } });
    setClips((all) => all?.map((c) => (c.id === updated.id ? updated : c)) ?? null);
    return updated;
  }

  async function choose(verdict: "keep" | "reject") {
    if (!clip) return;
    setError("");
    try {
      await decide(verdict, clip);
      setHistory((h) => [...h, index]);
      setAskReason(verdict === "reject" ? clip : null);
      setIndex((i) => i + 1);
    } catch (err) {
      setError((err as Error).message);
    }
    setDrag(0);
  }

  async function undo() {
    const previous = history[history.length - 1];
    if (previous === undefined || !clips) return;
    try {
      await decide(null, clips[previous]);
      setHistory((h) => h.slice(0, -1));
      setAskReason(null);
      setIndex(previous);
    } catch (err) {
      setError((err as Error).message);
    }
  }

  async function giveReason(reason: string) {
    if (!askReason) return;
    try {
      await decide("reject", askReason, reason);
    } finally {
      setAskReason(null);
    }
  }

  function toggleSound() {
    setMuted((m) => {
      try {
        localStorage.setItem("kc-muted", m ? "0" : "1");
      } catch {
        /* private mode: the choice just isn't remembered */
      }
      return !m;
    });
  }

  useEffect(() => {
    function onKey(event: KeyboardEvent) {
      if (event.key === "ArrowRight") choose("keep");
      else if (event.key === "ArrowLeft") choose("reject");
      else if (event.key === "Backspace" || event.key.toLowerCase() === "z") undo();
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  });

  const reasonBar = askReason && (
    <div className="reasons" aria-label="Why not?">
      <span className="muted small">Why not? (optional)</span>
      {REASONS.map(([key, label]) => <button key={key} onClick={() => giveReason(key)}>{label}</button>)}
    </div>
  );

  if (error && !clips) return <p className="error">{error}</p>;
  if (!clips) return <p className="muted">Loading…</p>;

  if (!clip) {
    const kept = clips.filter((c) => c.decision === "keep").length;
    return (
      <>
        <h1>All done</h1>
        <p>You kept {kept} of {clips.length} clips.</p>
        {reasonBar}
        <div className="row">
          <Link className="button primary" to="/library?decision=keep">See kept clips</Link>
          {history.length > 0 && <button onClick={undo}>Undo last</button>}
          <Link className="button" to={`/streams/${id}`}>Back to the stream</Link>
        </div>
      </>
    );
  }

  const flags = (clip.flags as unknown[]).map((f) => (typeof f === "string" ? f : (f as { text?: string; kind?: string }).text ?? (f as { kind?: string }).kind ?? ""));

  return (
    <>
      <div className="spread" style={{ marginTop: 12 }}>
        <span className="muted small">{index + 1} of {clips.length}</span>
        <button onClick={toggleSound} aria-label={muted ? "Sound on" : "Sound off"}>{muted ? "🔇 Sound off" : "🔊 Sound on"}</button>
      </div>
      <div className="review">
        <div
          className="clipcard"
          key={clip.id}
          style={{ transform: `translateX(${drag}px) rotate(${drag / 30}deg)` }}
          onPointerDown={(e) => { start.current = e.clientX; }}
          onPointerMove={(e) => { if (start.current !== null) setDrag(e.clientX - start.current); }}
          onPointerUp={() => {
            start.current = null;
            if (drag > SWIPE_PX) choose("keep");
            else if (drag < -SWIPE_PX) choose("reject");
            else {
              if (Math.abs(drag) < 8 && video.current) video.current.paused ? video.current.play() : video.current.pause();
              setDrag(0);
            }
          }}
          onPointerCancel={() => { start.current = null; setDrag(0); }}
        >
          <video ref={video} src={clip.play ?? clip.video} autoPlay loop playsInline muted={muted} preload="auto"
                 onCanPlayThrough={() => setBuffered(clip.id)} />
          <div className="stamp keep" style={{ opacity: Math.max(0, drag / SWIPE_PX) }}>KEEP</div>
          <div className="stamp reject" style={{ opacity: Math.max(0, -drag / SWIPE_PX) }}>NOPE</div>
          <div className="clipinfo">
            <div className="spread">
              <span className="title">{clip.title ?? `Clip ${clip.rank}`}</span>
              <span className="chip">{TYPE_LABEL[clip.type] ?? clip.type}</span>
            </div>
            <div className="small muted">{clip.why} · {clock(clip.length_s)} long</div>
            {flags.length > 0 && <div className="small error">⚠ {flags.join(", ")}</div>}
          </div>
        </div>
        {next && buffered === clip.id && <link rel="preload" as="video" href={next.play ?? next.video} />}
      </div>
      {reasonBar}
      {error && <p className="error">{error}</p>}
      <div className="actions">
        <button className="reject" onClick={() => choose("reject")}>✗ Reject</button>
        <button onClick={undo} disabled={!history.length} aria-label="Undo">↶</button>
        <span />
        <button className="keep primary" onClick={() => choose("keep")}>✓ Keep</button>
      </div>
    </>
  );
}
