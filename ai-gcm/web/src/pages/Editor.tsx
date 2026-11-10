import { useCallback, useEffect, useRef, useState } from "react";
import { Link, useParams } from "react-router";
import { api, type Box, type EditData, type RenderJob, type Studio, type Template } from "../api";
import { clock } from "../format";
import {
  addPart, applyPreset, cameraBox, captionChunks, type Chunk, CLAIM_LIMIT_S, fitTo, fixWord, hookBox, musicSeconds,
  MUSIC_WARN_S, outputLength, partAt, problems, removePart, SAFE_LENGTH_S, zoomSounds,
  setSpeed, setZoomStrength, SPEEDS, split, templateLayout, toggleZoom, toOutput, trim, wordsInParts, ZOOM_STRENGTHS,
  zoomStrength,
} from "../studio/model";
import CamBox from "../studio/CamBox";
import { CAPTION_FONT, drawFrame, PREVIEW_H, PREVIEW_W } from "../studio/preview";
import Timeline, { TIMELINE_PAD } from "../studio/Timeline";

const POLL_MS = 2000;
const HOOK_DELAY_MS = 450;   // draw the hook once typing pauses
// The emoji bundled in assets/emoji (the hook draws only these, in colour).
const EMOJI = [0x1f525, 0x1f631, 0x1f602, 0x1f923, 0x1f62d, 0x1f621, 0x1f92f, 0x1f480, 0x1f451, 0x1f3af, 0x1f3c6, 0x26a1,
  0x1f4a5, 0x1f680, 0x1f60e, 0x1f921, 0x1f440, 0x1f608, 0x1f64f, 0x2764, 0x1f4af, 0x2705, 0x274c, 0x26a0, 0x1f3ae, 0x1f52b,
  0x1f4a3, 0x1fa78, 0x1f624, 0x1f975, 0x1f976, 0x1f633, 0x1f914, 0x1f44f, 0x1f91d, 0x1f4aa, 0x1fae1, 0x1f410, 0x1f981,
  0x1f40d, 0x1f357, 0x1f414, 0x1f947, 0x1f389, 0x1f4c8, 0x23f1, 0x1f9e0, 0x1f64c, 0x1f605, 0x1f62c, 0x1f60f, 0x1f92b,
  0x1f5ff, 0x1f47b, 0x2620, 0x1f62e, 0x1f972, 0x1f606, 0x1fae3, 0x1f534, 0x1f381, 0x1f447, 0x1f446].map((c) => String.fromCodePoint(c));
const TOOLS = [["cut", "Cut"], ["layout", "Layout"], ["zoom", "Zoom"], ["text", "Text"], ["captions", "Captions"]] as const;
type Tool = (typeof TOOLS)[number][0];
const TEMPLATES: [Template, string][] = [["native", "As streamed"], ["blur", "Blur fill"], ["band", "Hook band"], ["split", "Camera on top"]];
const DEFAULT_CAMERA: Box = [0.02, 0.6, 0.3, 0.38];
const ZOOMS = [4, 6, 10, 16, 24];   // timeline pixels per second

function fileName(title: string | null, id: number) {
  return `${(title ?? `clip-${id}`).replace(/[^\w\- ]+/g, "").trim() || "clip"}.mp4`;
}

// M3.3: the phone editor. A canvas shows the export as it will look, played from the small preview copy
// through the edit's parts (cuts and speed-ups); the timeline trims, splits and speeds them up; Save
// stores a new version; Export renders it on the laptop and the result can be shared straight away.
export default function Editor() {
  const { id } = useParams();
  const [studio, setStudio] = useState<Studio | null>(null);
  const [edit, setEdit] = useState<EditData | null>(null);
  const [saved, setSaved] = useState("");
  const [version, setVersion] = useState(0);
  const [past, setPast] = useState<EditData[]>([]);
  const [future, setFuture] = useState<EditData[]>([]);
  const [selected, setSelected] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [zoomIndex, setZoomIndex] = useState(2);
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);
  const [job, setJob] = useState<RenderJob | null>(null);
  const [shareFile, setShareFile] = useState<File | null>(null);
  const [cursor, setCursor] = useState(0);
  const [tool, setTool] = useState<Tool>("cut");
  const [placing, setPlacing] = useState<{ box: Box; template: Template } | null>(null);
  const [converting, setConverting] = useState(false);
  const hookImage = useRef<HTMLImageElement | null>(null);
  const stripImage = useRef<HTMLImageElement | null>(null);
  const chunks = useRef<Chunk[]>([]);
  const lastOut = useRef(0);   // where the playhead was last frame, to start sound effects as it passes them

  const video = useRef<HTMLVideoElement>(null);
  const canvas = useRef<HTMLCanvasElement>(null);
  const playhead = useRef<HTMLDivElement>(null);
  const scroller = useRef<HTMLDivElement>(null);
  const timeLabel = useRef<HTMLSpanElement>(null);
  const editRef = useRef<EditData | null>(null);
  const cursorRef = useRef(0);
  const partRef = useRef(0);
  const playingRef = useRef(false);
  const dragBase = useRef<EditData | null>(null);
  editRef.current = edit;

  const pps = ZOOMS[zoomIndex];
  const win = studio?.window;
  const lo = win?.start ?? 0;
  const hi = win?.end ?? 0;

  useEffect(() => {
    api<Studio>(`/api/clips/${id}/studio`).then((data) => {
      setStudio(data);
      setEdit(data.edit.data);
      setSaved(JSON.stringify(data.edit.data));
      setVersion(data.edit.version);
      cursorRef.current = data.edit.data.segments[0].start;
      setCursor(cursorRef.current);
    }).catch((err) => setMessage((err as Error).message));
  }, [id]);

  const dirty = edit !== null && JSON.stringify(edit) !== saved;
  useEffect(() => {
    if (!message) return;
    const timer = window.setTimeout(() => setMessage(""), 3500);
    return () => window.clearTimeout(timer);
  }, [message]);
  useEffect(() => {
    if (!dirty) return;
    const warn = (e: BeforeUnloadEvent) => e.preventDefault();
    window.addEventListener("beforeunload", warn);
    return () => window.removeEventListener("beforeunload", warn);
  }, [dirty]);

  // --- drawing and the playhead (updated directly, not through React, so playing stays smooth) -----------
  const paint = useCallback(() => {
    const v = video.current;
    const ctx = canvas.current?.getContext("2d");
    const current = editRef.current;
    if (!v || !ctx || !current) return;
    const t = cursorRef.current;
    drawFrame(ctx, v, current, t, { hook: hookImage.current, chunks: chunks.current, strip: stripImage.current });
    if (playhead.current) playhead.current.style.left = `${TIMELINE_PAD + (t - lo) * pps}px`;
    if (timeLabel.current) {
      const out = toOutput(current.segments, t);
      timeLabel.current.textContent = `${out === null ? "cut" : clock(out)} / ${clock(outputLength(current.segments))}`;
    }
  }, [lo, pps]);

  useEffect(() => { paint(); }, [edit, paint, cursor]);

  // Captions: the same chunks the export burns in, from the transcript's words and the creator's fixes.
  const words = studio?.editor?.words;
  useEffect(() => {
    chunks.current = edit && words ? captionChunks(edit, words) : [];
    paint();
  }, [edit, words, paint]);

  // The brand kit's lower-third strip, the same image the export lays on.
  const stripUrl = studio?.editor?.brand?.strip ?? null;
  useEffect(() => {
    if (!stripUrl) { stripImage.current = null; return; }
    const image = new Image();
    image.onload = () => { stripImage.current = image; paint(); };
    image.src = `${stripUrl}?v=${Date.now()}`;
  }, [stripUrl, paint]);

  // The bundled caption font, so the preview's captions look like the export's.
  useEffect(() => {
    if (typeof FontFace === "undefined" || !document.fonts) return;
    new FontFace(CAPTION_FONT, "url(/fonts/Mukta-ExtraBold.ttf)").load()
      .then((face) => { document.fonts.add(face); paint(); }).catch(() => {});
  }, [paint]);

  // The hook: drawn by the server (the same image the export uses), shortly after typing stops.
  const hookText = edit?.hook.text ?? "";
  const hookColor = edit?.hook.color ?? "yellow";
  const hookOn = edit?.hook.on ?? false;
  const hookHeight = edit ? hookBox(edit.layout)[1] : 0;
  const hookBacking = edit ? !edit.layout.band_h : false;
  useEffect(() => {
    if (!hookOn || !hookText.trim()) {
      hookImage.current = null;
      paint();
      return;
    }
    let live = true;
    const timer = window.setTimeout(() => {
      api<{ url: string | null }>(`/api/clips/${id}/hook`, { body: { text: hookText, color: hookColor, box_h: hookHeight, backing: hookBacking } })
        .then(({ url }) => {
          if (!live) return;
          if (!url) { hookImage.current = null; paint(); return; }
          const image = new Image();
          image.onload = () => { if (live) { hookImage.current = image; paint(); } };
          image.src = url;
        })
        .catch((err) => setMessage((err as Error).message));
    }, HOOK_DELAY_MS);
    return () => { live = false; window.clearTimeout(timer); };
  }, [id, hookText, hookColor, hookOn, hookHeight, hookBacking, paint]);

  // Open (and zoom) with the playhead in view: the saved footage starts a minute or more before the clip.
  const ready = studio?.window.status === "ready";
  useEffect(() => {
    const box = scroller.current;
    if (box && ready) box.scrollLeft = Math.max(0, TIMELINE_PAD + (cursorRef.current - lo) * pps - box.clientWidth * 0.25);
  }, [ready, lo, pps]);

  const showSource = useCallback((t: number) => {
    const v = video.current;
    cursorRef.current = Math.min(Math.max(t, lo), hi);
    if (v) v.currentTime = Math.max(0, cursorRef.current - lo);
    paint();
  }, [lo, hi, paint]);

  function pause() {
    playingRef.current = false;
    video.current?.pause();
    setPlaying(false);
    setCursor(cursorRef.current);
  }

  function tick() {
    const v = video.current;
    const current = editRef.current;
    if (!playingRef.current || !v || !current) return;
    const segs = current.segments;
    const t = v.currentTime + lo;
    let i = partRef.current;
    if (i >= segs.length || t >= segs[i].end - 0.02) {
      i += 1;
      if (i >= segs.length) {
        cursorRef.current = segs[segs.length - 1].end;
        paint();
        pause();
        return;
      }
      partRef.current = i;
      v.currentTime = segs[i].start - lo;
      v.playbackRate = segs[i].speed;
    }
    cursorRef.current = Math.max(t, segs[i].start);
    const now = toOutput(segs, cursorRef.current);
    if (now !== null) {
      for (const fx of current.sfx ?? []) {
        const at = toOutput(segs, fx.t);
        if (at !== null && at > lastOut.current && at <= now) {
          const sound = new Audio(`/sfx/${fx.name}.wav`);
          sound.volume = fx.gain;
          sound.play().catch(() => {});
        }
      }
      lastOut.current = now;
    }
    paint();
    const box = scroller.current;
    const x = TIMELINE_PAD + (cursorRef.current - lo) * pps;
    if (box && (x < box.scrollLeft || x > box.scrollLeft + box.clientWidth - 40)) box.scrollLeft = x - 40;
    requestAnimationFrame(tick);
  }

  function play() {
    const v = video.current;
    if (!v || !edit) return;
    const segs = edit.segments;
    let t = cursorRef.current;
    let i = partAt(segs, t);
    if (i < 0 || t >= segs[i].end - 0.05) {
      i = segs.findIndex((s) => s.start > t);
      if (i < 0) i = 0;   // at the end: from the top
      t = segs[i].start;
    }
    partRef.current = i;
    cursorRef.current = t;
    lastOut.current = toOutput(segs, t) ?? 0;
    v.currentTime = t - lo;
    v.playbackRate = segs[i].speed;
    playingRef.current = true;
    setPlaying(true);
    v.play().then(() => requestAnimationFrame(tick)).catch((err) => {
      setMessage(`Can't play here: ${(err as Error).message}`);
      pause();
    });
  }

  // --- changing the edit ----------------------------------------------------------------------------
  function commit(next: EditData) {
    if (!edit) return;
    setPast((p) => [...p.slice(-49), edit]);
    setFuture([]);
    setEdit(next);
    setShareFile(null);
    setJob(null);
  }

  function undo() {
    if (!edit || past.length === 0) return;
    setFuture((f) => [edit, ...f]);
    setEdit(past[past.length - 1]);
    setPast((p) => p.slice(0, -1));
  }

  function redo() {
    if (!edit || future.length === 0) return;
    setPast((p) => [...p, edit]);
    setEdit(future[0]);
    setFuture((f) => f.slice(1));
  }

  function seek(t: number) {
    if (playingRef.current) pause();
    showSource(t);
    setCursor(cursorRef.current);
    const i = edit ? partAt(edit.segments, cursorRef.current) : -1;
    if (i >= 0) setSelected(i);
  }

  // --- saving and exporting -------------------------------------------------------------------------
  async function save(): Promise<number | null> {
    if (!edit) return null;
    const issues = problems(edit, lo, hi);
    if (issues.length) {
      setMessage(issues[0]);
      return null;
    }
    if (!dirty) return version;
    setBusy(true);
    try {
      const result = await api<{ version: number; data: EditData }>(`/api/clips/${id}/edit`,
        { method: "PUT", body: { base_version: version, data: edit } });
      setVersion(result.version);
      setSaved(JSON.stringify(edit));
      setMessage(`Saved as version ${result.version}`);
      return result.version;
    } catch (err) {
      setMessage((err as Error).message);
      return null;
    } finally {
      setBusy(false);
    }
  }

  async function exportNow() {
    if (playingRef.current) pause();
    const v = await save();
    if (v === null) return;
    setBusy(true);
    setShareFile(null);
    try {
      setJob(await api<RenderJob>(`/api/clips/${id}/export`, { body: { version: v } }));
    } catch (err) {
      setMessage((err as Error).message);
    } finally {
      setBusy(false);
    }
  }

  useEffect(() => {
    if (!job || job.status === "failed") return;
    if (job.status === "done") {
      // Fetched now, so tapping Share opens the share sheet at once (phones only allow it right after a tap).
      if (job.video && !shareFile) {
        fetch(job.video, { credentials: "same-origin" }).then((r) => r.blob())
          .then((blob) => setShareFile(new File([blob], fileName(studio?.clip.title ?? null, Number(id)), { type: "video/mp4" })))
          .catch(() => {});
      }
      return;
    }
    const timer = window.setTimeout(() => {
      api<RenderJob>(`/api/renders/${job.id}`).then(setJob).catch((err) => setMessage((err as Error).message));
    }, POLL_MS);
    return () => window.clearTimeout(timer);
  }, [job, shareFile, studio, id]);

  async function share() {
    if (!shareFile) return;
    try {
      if (!navigator.canShare?.({ files: [shareFile] })) throw new Error("This browser can't share videos. Use Download.");
      await navigator.share({ files: [shareFile] });
    } catch (err) {
      if ((err as Error).name !== "AbortError") setMessage((err as Error).message);
    }
  }

  // --- screen ---------------------------------------------------------------------------------------
  if (!studio || !edit) return message ? <p className="error">{message}</p> : <p className="muted">Loading…</p>;
  if (studio.window.status !== "ready" || !win?.preview || !win.strip || !win.wave || !studio.editor) {
    return (
      <>
        <p>This clip's footage isn't ready for editing yet.</p>
        <Link className="button" to={`/clips/${id}/studio`}>Back to the clip</Link>
      </>
    );
  }
  const segs = edit.segments;
  const total = outputLength(segs);
  const music = musicSeconds(studio.editor.music ?? [], segs);
  const vertical = (win.height ?? 0) > (win.width ?? 0);
  const camera = cameraBox(edit) ?? studio.editor.facecam;
  const strength = zoomStrength(edit);

  function applyTemplate(template: Template, box: Box | null = camera) {
    if (!edit) return;
    if (template === "split" && !box) {
      setPlacing({ box: DEFAULT_CAMERA, template });   // no camera known yet: let the creator mark it
      return;
    }
    commit({ ...edit, layout: templateLayout(template, win!.width ?? 1920, win!.height ?? 1080, box) });
  }
  const part = segs[Math.min(selected, segs.length - 1)];
  const presets = studio.editor.presets;
  const inGap = partAt(segs, cursor) < 0;
  const timelineWin = { start: lo, end: hi, duration: win.duration ?? hi - lo, strip: win.strip, wave: win.wave };

  return (
    <div className="editor">
      <div className="spread edtop">
        <Link to={`/clips/${id}/studio`} className="button" aria-label="Close the editor">✕</Link>
        <span ref={timeLabel} className="small edtime" />
        <div className="row">
          <button onClick={undo} disabled={past.length === 0} aria-label="Undo">↶</button>
          <button onClick={redo} disabled={future.length === 0} aria-label="Redo">↷</button>
          <button onClick={save} disabled={!dirty || busy}>{dirty ? "Save" : "Saved"}</button>
        </div>
      </div>

      <div className="stage" onClick={() => (playing ? pause() : play())}>
        <canvas ref={canvas} width={PREVIEW_W} height={PREVIEW_H} />
        {!playing && <span className="playbtn">▶</span>}
      </div>
      <video ref={video} src={win.preview} playsInline preload="auto" className="offscreen"
             onLoadedData={paint} onSeeked={paint} />

      <div className="chips">
        <button className="chip" onClick={() => commit(applyPreset(edit, presets.moment[0], presets.moment[1], studio.editor!.events))}>
          Moment {Math.round(presets.moment[1] - presets.moment[0])}s{presets.suggested === "moment" ? " ★" : ""}
        </button>
        <button className="chip" onClick={() => commit(applyPreset(edit, presets.full_fight[0], presets.full_fight[1], studio.editor!.events))}>
          Full fight {Math.round(presets.full_fight[1] - presets.full_fight[0])}s{presets.suggested === "full_fight" ? " ★" : ""}
        </button>
        <span className="small muted edlen">{total.toFixed(1)} s{total > 60 ? " · over 1 min" : ""}</span>
      </div>

      <Timeline win={timelineWin} segments={segs} selected={selected} events={studio.editor.events} pps={pps}
                zooms={edit.zooms.map((z) => z.t)} onEventTap={(t) => commit(toggleZoom(edit, t))}
                music={studio.editor.music}
                playhead={playhead} scroller={scroller} onSeek={seek} onSelect={setSelected}
                onTrimStart={() => { if (playingRef.current) pause(); dragBase.current = edit; }}
                onTrim={(i, edge, t) => {
                  setEdit((current) => current && { ...current, segments: trim(current.segments, i, edge, t, lo, hi) });
                  showSource(Math.min(Math.max(t, lo), hi));
                }}
                onTrimEnd={() => {
                  const base = dragBase.current;
                  dragBase.current = null;
                  if (base && JSON.stringify(base.segments) !== JSON.stringify(editRef.current?.segments)) {
                    setPast((p) => [...p.slice(-49), base]);
                    setFuture([]);
                    setJob(null);
                  }
                  setCursor(cursorRef.current);
                }} />

      <div className="chips tooltabs" role="tablist">
        {TOOLS.map(([t, label]) => (
          <button key={t} role="tab" aria-selected={tool === t} className={tool === t ? "chip on" : "chip"}
                  onClick={() => setTool(t)}>{label}</button>
        ))}
      </div>

      {tool === "text" && (
        <div className="edpanel">
          <div className="row">
            <button className={edit.hook.on ? "chip on" : "chip"}
                    onClick={() => commit({ ...edit, hook: { ...edit.hook, on: !edit.hook.on } })}>
              Hook {edit.hook.on ? "on" : "off"}
            </button>
            {(["yellow", "white"] as const).map((c) => (
              <button key={c} className={edit.hook.color === c ? "chip on" : "chip"}
                      onClick={() => commit({ ...edit, hook: { ...edit.hook, color: c, on: true } })}>
                {c === "yellow" ? "Yellow" : "White"}
              </button>
            ))}
          </div>
          <input value={edit.hook.text} maxLength={80} aria-label="Hook text" placeholder="1V4 LAST ZONE 😱"
                 onChange={(e) => setEdit({ ...edit, hook: { ...edit.hook, text: e.target.value, on: true } })}
                 onFocus={() => { dragBase.current = edit; }}
                 onBlur={() => {
                   const base = dragBase.current;
                   dragBase.current = null;
                   if (base && base.hook.text !== editRef.current?.hook.text) {
                     setPast((p) => [...p.slice(-49), base]);
                     setFuture([]);
                   }
                 }} />
          {studio.clip.titles.length > 0 && (
            <div className="chips" aria-label="Suggested hooks">
              {studio.clip.titles.map((t) => (
                <button key={t} className="chip" onClick={() => commit({ ...edit, hook: { ...edit.hook, text: t, on: true } })}>{t}</button>
              ))}
            </div>
          )}
          {(studio.editor.brand.strip || studio.editor.brand.intro_s > 0 || studio.editor.brand.outro_s > 0) && (
            <div className="row" aria-label="Brand kit">
              {studio.editor.brand.strip && (
                <button className={edit.lower_third ? "chip on" : "chip"} onClick={() => commit({ ...edit, lower_third: !edit.lower_third })}>
                  Lower-third
                </button>
              )}
              {studio.editor.brand.intro_s > 0 && (
                <button className={edit.intro ? "chip on" : "chip"} onClick={() => commit({ ...edit, intro: !edit.intro })}>
                  Intro {studio.editor.brand.intro_s.toFixed(0)}s
                </button>
              )}
              {studio.editor.brand.outro_s > 0 && (
                <button className={edit.outro ? "chip on" : "chip"} onClick={() => commit({ ...edit, outro: !edit.outro })}>
                  Outro {studio.editor.brand.outro_s.toFixed(0)}s
                </button>
              )}
              <Link to="/brand" className="small">Brand kit</Link>
            </div>
          )}
          <div className="emojis" aria-label="Add an emoji">
            {EMOJI.map((e) => (
              <button key={e} onClick={() => commit({ ...edit, hook: { ...edit.hook, text: `${edit.hook.text.trimEnd()} ${e}`.slice(0, 80), on: true } })}>
                {e}
              </button>
            ))}
          </div>
        </div>
      )}

      {tool === "captions" && (
        <div className="edpanel">
          <div className="row">
            <button className={edit.captions.on ? "chip on" : "chip"}
                    onClick={() => commit({ ...edit, captions: { ...edit.captions, on: !edit.captions.on } })}>
              Captions {edit.captions.on ? "on" : "off"}
            </button>
            <button className="chip" disabled={converting || !(edit.captions.words ?? []).length}
                    onClick={() => commit({ ...edit, captions: { ...edit.captions, script: "auto", words: [] } })}>As spoken</button>
            {(["latin", "devanagari"] as const).map((script) => (
              <button key={script} className={edit.captions.script === script ? "chip on" : "chip"} disabled={converting}
                      onClick={async () => {
                        const listed = wordsInParts(edit, studio.editor!.words);
                        if (!listed.length) { setMessage("No words were heard in this clip."); return; }
                        setConverting(true);
                        try {
                          const result = await api<{ words: { t: number; w: string }[] }>(`/api/clips/${id}/captions/convert`,
                            { body: { script, words: listed.map((w) => ({ t: w.t, w: w.w })) } });
                          commit({ ...edit, captions: { on: true, script, words: result.words } });
                        } catch (err) {
                          setMessage((err as Error).message);
                        } finally {
                          setConverting(false);
                        }
                      }}>
                {script === "latin" ? "Hinglish" : "हिंदी"}
              </button>
            ))}
          </div>
          <div className="row">
            {(["white", "yellow"] as const).map((c) => (
              <button key={c} className={(edit.captions.color ?? "white") === c ? "chip on" : "chip"}
                      onClick={() => commit({ ...edit, captions: { ...edit.captions, color: c } })}>{c === "white" ? "White" : "Yellow"}</button>
            ))}
            {(["normal", "large"] as const).map((z) => (
              <button key={z} className={(edit.captions.size ?? "normal") === z ? "chip on" : "chip"}
                      onClick={() => commit({ ...edit, captions: { ...edit.captions, size: z } })}>{z === "normal" ? "Normal" : "Large"}</button>
            ))}
          </div>
          {converting && <p className="small muted">Converting with Gemini…</p>}
          <p className="small muted">Tap a word to fix it; clear it to hide it.</p>
          <div className="wordlist">
            {wordsInParts(edit, studio.editor.words).map((w) => (
              <button key={w.t} className={w.shown !== w.w ? "word fixed" : "word"} onClick={() => {
                const next = window.prompt(`Change "${w.shown}" to:`, w.shown);
                if (next !== null) commit(fixWord(edit, w, next.trim()));
              }}>{w.shown || "∅"}</button>
            ))}
            {wordsInParts(edit, studio.editor.words).length === 0 && <span className="small muted">No words were heard in this clip.</span>}
          </div>
        </div>
      )}

      {placing && video.current && (
        <CamBox video={video.current} box={placing.box} onCancel={() => setPlacing(null)}
                onDone={(box) => { applyTemplate(placing.template, box); setPlacing(null); }} />
      )}

      {tool === "layout" && !placing && (
        <div className="row edtools">
          {TEMPLATES.filter(([t]) => (vertical ? t === "native" || t === "blur" : t !== "native")).map(([t, label]) => (
            <button key={t} className={edit.layout.template === t ? "chip on" : "chip"} onClick={() => applyTemplate(t)}>{label}</button>
          ))}
          {!vertical && (
            <button onClick={() => setPlacing({ box: camera ?? DEFAULT_CAMERA,
                                                template: edit.layout.template === "band" ? "band" : "split" })}>
              {camera ? "Move camera box" : "Mark camera"}
            </button>
          )}
          {!vertical && !camera && <span className="small muted">No camera found in this stream.</span>}
        </div>
      )}

      {tool === "zoom" && (
        <div className="row edtools">
          <span className="small muted">Zoom on kills</span>
          {ZOOM_STRENGTHS.map(([label, scale]) => (
            <button key={label} className={(scale ? Math.abs(strength - scale) < 0.01 : strength === 0) ? "chip on" : "chip"}
                    onClick={() => commit(setZoomStrength(edit, studio.editor!.events, scale))}>{label}</button>
          ))}
          <button className={edit.keep_hud !== false ? "chip on" : "chip"}
                  onClick={() => commit({ ...edit, keep_hud: edit.keep_hud === false })}>Keep HUD</button>
          <button className={(edit.sfx ?? []).length ? "chip on" : "chip"} disabled={!edit.zooms.length}
                  onClick={() => commit(zoomSounds(edit, !(edit.sfx ?? []).length))}>Sound on zooms</button>
          <span className="small muted">Tap a red kill mark to add or take away its zoom.</span>
        </div>
      )}

      {tool === "cut" && <div className="row edtools">
        {inGap
          ? <button onClick={() => commit({ ...edit, segments: addPart(segs, cursor, lo, hi) })}>+ Bring back</button>
          : <button onClick={() => commit({ ...edit, segments: split(segs, cursor) })}>Split</button>}
        <button onClick={() => commit({ ...edit, segments: removePart(segs, selected) })} disabled={segs.length < 2}>
          Delete part
        </button>
        <button className={edit.cover_t !== null && Math.abs(edit.cover_t - cursor) < 0.05 ? "chip on" : "chip"}
                disabled={inGap} title="The Short's cover: this frame (otherwise the first kill)"
                onClick={() => commit({ ...edit, cover_t: Math.round(cursor * 1000) / 1000 })}>
          {edit.cover_t === null ? "Cover here" : "Cover ✓ here"}
        </button>
        {edit.cover_t !== null && (
          <button className="chip" onClick={() => commit({ ...edit, cover_t: null })}>Auto cover</button>
        )}
        <span className="small muted">Speed</span>
        {SPEEDS.map((s) => (
          <button key={s} className={part.speed === s ? "chip on" : "chip"}
                  onClick={() => commit({ ...edit, segments: setSpeed(segs, selected, s) })}>{s}×</button>
        ))}
        <span className="grow" />
        <button aria-label="Zoom the timeline out" onClick={() => setZoomIndex((z) => Math.max(0, z - 1))}>−</button>
        <button aria-label="Zoom the timeline in" onClick={() => setZoomIndex((z) => Math.min(ZOOMS.length - 1, z + 1))}>+</button>
      </div>}

      {music >= MUSIC_WARN_S && (
        <div className={total > CLAIM_LIMIT_S ? "banner musicwarn danger" : "banner musicwarn"}>
          {total > CLAIM_LIMIT_S
            ? <>Music plays under about {Math.round(music)} s of this clip. A Short over 1 minute with a music claim is blocked worldwide.</>
            : <>Music plays under about {Math.round(music)} s of this clip. Under a minute a claim won't block it, but it can take the money.</>}
          {total > CLAIM_LIMIT_S && (
            <button className="primary" onClick={() => {
              const focus = edit.zooms.length ? toOutput(segs, edit.zooms[0].t) : null;
              commit({ ...edit, segments: fitTo(segs, SAFE_LENGTH_S, focus ?? total / 2) });
            }}>Cut to {SAFE_LENGTH_S} s</button>
          )}
        </div>
      )}

      <div className="card edexport">
        {!job && <button className="primary" disabled={busy} onClick={exportNow}>Export{dirty ? " (saves first)" : ""}</button>}
        {job && (job.status === "queued" || job.status === "running") && (
          <div className="small">Rendering on the laptop… {job.status === "queued" ? "waiting for its turn" : "about as long as the clip"}</div>
        )}
        {job?.status === "failed" && <div className="small error">Export failed: {job.error}</div>}
        {job?.status === "done" && (
          <div className="row">
            <button className="primary" disabled={!shareFile} onClick={share}>{shareFile ? "Share" : "Getting it ready…"}</button>
            <a className="button" href={`${job.video}?download=1`}>Download</a>
            <button onClick={() => setJob(null)}>Export again</button>
          </div>
        )}
      </div>
      {message && <div className="toast" onClick={() => setMessage("")}>{message}</div>}
    </div>
  );
}
