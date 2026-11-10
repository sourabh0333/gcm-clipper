import { useEffect, useState } from "react";
import { Link } from "react-router";
import { api, ApiError, type BrandKit, type BrandView } from "../api";

const KRAFTON = "BGMI is a trademark of KRAFTON, Inc. This video is not endorsed by or affiliated with KRAFTON.";

async function upload(kind: "logo" | "intro" | "outro", file: File): Promise<BrandView> {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`/api/brand/${kind}`, { method: "POST", body: form, credentials: "same-origin",
                                                   headers: { "X-Kaatclip": "1" } });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new ApiError(res.status, (data as { detail?: string }).detail ?? `Upload failed (${res.status})`);
  return data as BrandView;
}

function Choice<T extends string>({ value, options, onChange }: { value: T; options: [T, string][]; onChange: (v: T) => void }) {
  return (
    <div className="row">
      {options.map(([v, label]) => (
        <button key={v} type="button" className={value === v ? "chip on" : "chip"} onClick={() => onChange(v)}>{label}</button>
      ))}
    </div>
  );
}

// M3.6: the brand kit, set once and used on every export and on the clips of every new stream.
export default function Brand() {
  const [view, setView] = useState<BrandView | null>(null);
  const [kit, setKit] = useState<BrandKit | null>(null);
  const [tags, setTags] = useState("");
  const [note, setNote] = useState("");
  const [busy, setBusy] = useState("");
  const [stamp, setStamp] = useState(Date.now());   // reloads the strip preview after a change

  function show(next: BrandView) {
    setView(next);
    setKit(next.kit);
    setTags(next.kit.hashtags.join(" "));
    setStamp(Date.now());
  }

  useEffect(() => {
    api<BrandView>("/api/brand").then(show).catch((err) => setNote((err as Error).message));
  }, []);

  if (!kit || !view) return note ? <p className="error">{note}</p> : <p className="muted">Loading…</p>;
  const set = (patch: Partial<BrandKit>) => setKit({ ...kit, ...patch });

  async function save() {
    setBusy("save");
    try {
      show(await api<BrandView>("/api/brand", { method: "PUT", body: { ...kit, hashtags: tags.split(/[\s,]+/).filter(Boolean) } }));
      setNote("Saved. New edits and new streams' clips use it.");
    } catch (err) {
      setNote((err as Error).message);
    } finally {
      setBusy("");
    }
  }

  async function send(kind: "logo" | "intro" | "outro", file: File | undefined) {
    if (!file) return;
    setBusy(kind);
    setNote(kind === "logo" ? "Uploading the logo…" : `Uploading and preparing the ${kind} (a few seconds)…`);
    try {
      show(await upload(kind, file));
      setNote(kind === "logo" ? "Logo saved." : `The ${kind} is ready.`);
    } catch (err) {
      setNote((err as Error).message);
    } finally {
      setBusy("");
    }
  }

  async function drop(kind: "logo" | "intro" | "outro") {
    show(await api<BrandView>(`/api/brand/${kind}`, { method: "DELETE" }));
  }

  return (
    <>
      <p className="small"><Link to="/settings">← Settings</Link></p>
      <h1>Brand kit</h1>
      <p className="muted small">Set it once: every new edit and every new stream's clips use it. Edits you've already saved keep theirs.</p>

      <h2>Look</h2>
      <div className="card brandform">
        <label>Hook colour</label>
        <Choice value={kit.hook_color} options={[["yellow", "Yellow"], ["white", "White"]]} onChange={(v) => set({ hook_color: v })} />
        <label>Caption colour</label>
        <Choice value={kit.caption_color} options={[["white", "White"], ["yellow", "Yellow"]]} onChange={(v) => set({ caption_color: v })} />
        <label>Caption size</label>
        <Choice value={kit.caption_size} options={[["normal", "Normal"], ["large", "Large"]]} onChange={(v) => set({ caption_size: v })} />
      </div>

      <h2>Lower-third</h2>
      <div className="card brandform">
        <p className="small muted">A strip along the bottom with your logo, name, UPI ID and Instagram, as many Indian gaming channels use.</p>
        <Choice value={kit.lower_third ? "on" : "off"} options={[["on", "Show it"], ["off", "Don't show"]]}
                onChange={(v) => set({ lower_third: v === "on" })} />
        <label htmlFor="b-name">Name</label>
        <input id="b-name" value={kit.name} maxLength={40} onChange={(e) => set({ name: e.target.value })} placeholder="Your channel name" />
        <label htmlFor="b-upi">UPI ID</label>
        <input id="b-upi" value={kit.upi} maxLength={60} onChange={(e) => set({ upi: e.target.value })} placeholder="name@okaxis" />
        <label htmlFor="b-ig">Instagram</label>
        <input id="b-ig" value={kit.instagram} maxLength={40} onChange={(e) => set({ instagram: e.target.value })} placeholder="@yourhandle" />
        <label>Logo</label>
        <div className="row">
          {view.files.logo && <img src={`${view.files.logo}?v=${stamp}`} alt="Your logo" className="brandlogo" />}
          <label className="button filebutton">{view.files.logo ? "Change logo" : "Add logo"}
            <input type="file" accept="image/png,image/jpeg,image/webp" disabled={busy !== ""}
                   onChange={(e) => send("logo", e.target.files?.[0])} />
          </label>
          {view.files.logo && <button type="button" className="danger" onClick={() => drop("logo")}>Remove</button>}
        </div>
        {view.strip && <img className="brandstrip" src={`${view.strip}?v=${stamp}`} alt="How the strip looks" />}
        {view.strip && <p className="small muted">The strip as saved; save again to see changes.</p>}
      </div>

      <h2>Intro and outro</h2>
      <div className="card brandform">
        <p className="small muted">Up to 6 seconds each. Most Shorts work better without an intro (viewers swipe away), so it's off unless you switch it on.</p>
        {(["intro", "outro"] as const).map((kind) => (
          <div key={kind} className="brandclip">
            <div className="spread">
              <span className="title">{kind === "intro" ? "Intro" : "Outro"}{view.files[kind] ? ` · ${view.lengths[kind].toFixed(1)} s` : ""}</span>
              {view.files[kind] && (
                <Choice value={(kind === "intro" ? kit.use_intro : kit.use_outro) ? "on" : "off"}
                        options={[["on", "Use"], ["off", "Don't use"]]}
                        onChange={(v) => set(kind === "intro" ? { use_intro: v === "on" } : { use_outro: v === "on" })} />
              )}
            </div>
            {view.files[kind] && <video src={`${view.files[kind]}?v=${stamp}`} controls playsInline preload="metadata" />}
            <div className="row">
              <label className="button filebutton">{view.files[kind] ? "Replace" : `Add ${kind}`}
                <input type="file" accept="video/*" disabled={busy !== ""} onChange={(e) => send(kind, e.target.files?.[0])} />
              </label>
              {view.files[kind] && <button type="button" className="danger" onClick={() => drop(kind)}>Remove</button>}
            </div>
          </div>
        ))}
      </div>

      <h2>Post text</h2>
      <div className="card brandform">
        <label htmlFor="b-desc">Standard description</label>
        <textarea id="b-desc" rows={4} maxLength={1500} value={kit.description} onChange={(e) => set({ description: e.target.value })}
                  placeholder="Live every day at 8 PM. Join the squad!" />
        <label htmlFor="b-tags">Hashtags</label>
        <input id="b-tags" value={tags} onChange={(e) => setTags(e.target.value)} placeholder="#bgmi #bgmishorts" />
        <label htmlFor="b-game">Game line</label>
        <textarea id="b-game" rows={3} maxLength={300} value={kit.disclaimer ?? KRAFTON}
                  onChange={(e) => set({ disclaimer: e.target.value === KRAFTON ? null : e.target.value })} />
        <p className="small muted">Added to every description with the stream link. Clear the game line to leave it out.</p>
      </div>

      <div className="row" style={{ margin: "14px 0 24px" }}>
        <button className="primary" disabled={busy !== ""} onClick={save}>{busy === "save" ? "Saving…" : "Save brand kit"}</button>
      </div>
      {note && <div className="toast" onClick={() => setNote("")}>{note}</div>}
    </>
  );
}
