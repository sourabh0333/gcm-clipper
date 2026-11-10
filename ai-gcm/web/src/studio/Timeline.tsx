import { useEffect, useRef } from "react";
import type { Segment, StudioWindow } from "../api";

type Props = {
  win: Required<Pick<StudioWindow, "start" | "end" | "duration" | "strip" | "wave">>;
  segments: Segment[];
  selected: number;
  events: { t: number; kind: string }[];
  zooms: number[];                   // kill times that have a zoom
  music?: [number, number][];        // where the stream plays music (sound safety)
  pps: number;                       // pixels per second of footage
  playhead: React.RefObject<HTMLDivElement | null>;
  scroller: React.RefObject<HTMLDivElement | null>;
  onSeek: (t: number) => void;
  onSelect: (i: number) => void;
  onEventTap: (t: number) => void;
  onTrimStart: () => void;
  onTrim: (i: number, edge: "start" | "end", t: number) => void;
  onTrimEnd: () => void;
};

const STRIP_H = 46;
const WAVE_H = 22;
const PAD = 16;   // room at both ends so the first and last handles can be grabbed

// The whole saved footage on one scrollable strip: frames, sound, kills, and the parts kept for the
// export. Dragging a part's handle trims it; tapping elsewhere moves the playhead there.
export default function Timeline(p: Props) {
  const inner = useRef<HTMLDivElement>(null);
  const wave = useRef<HTMLCanvasElement>(null);
  const peaks = useRef<number[] | null>(null);
  const width = Math.ceil(p.win.duration * p.pps);
  const x = (t: number) => PAD + (t - p.win.start) * p.pps;

  function timeAt(clientX: number) {
    const rect = inner.current!.getBoundingClientRect();
    return p.win.start + (clientX - rect.left - PAD) / p.pps;
  }

  useEffect(() => {
    let live = true;
    fetch(p.win.wave, { credentials: "same-origin" }).then((r) => r.json()).then((data: { peaks: number[]; step_s: number }) => {
      if (!live) return;
      peaks.current = data.peaks;
      draw(data.step_s);
    }).catch(() => {});
    return () => { live = false; };
  }, [p.win.wave]);

  useEffect(() => { draw(); });

  function draw(step = 0.1) {
    const canvas = wave.current;
    const values = peaks.current;
    if (!canvas || !values) return;
    canvas.width = Math.min(width, 16000);
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    ctx.clearRect(0, 0, canvas.width, WAVE_H);
    ctx.fillStyle = "#6b7184";
    const k = canvas.width / width;
    values.forEach((v, i) => {
      const h = Math.max(1, (v / 100) * WAVE_H);
      ctx.fillRect(i * step * p.pps * k, (WAVE_H - h) / 2, Math.max(1, step * p.pps * k - 0.5), h);
    });
  }

  function drag(i: number, edge: "start" | "end") {
    return (event: React.PointerEvent) => {
      event.stopPropagation();
      (event.target as HTMLElement).setPointerCapture(event.pointerId);
      p.onSelect(i);
      p.onTrimStart();
      const move = (e: PointerEvent) => p.onTrim(i, edge, timeAt(e.clientX));
      const up = () => {
        window.removeEventListener("pointermove", move);
        window.removeEventListener("pointerup", up);
        window.removeEventListener("pointercancel", up);
        p.onTrimEnd();
      };
      window.addEventListener("pointermove", move);
      window.addEventListener("pointerup", up);
      window.addEventListener("pointercancel", up);
    };
  }

  const strip = p.win.strip;
  const scale = STRIP_H / strip.tile_h;
  const tileW = strip.tile_w * scale;
  const gaps: [number, number][] = [];
  let from = p.win.start;
  for (const s of p.segments) {
    if (s.start > from) gaps.push([from, s.start]);
    from = Math.max(from, s.end);
  }
  if (from < p.win.end) gaps.push([from, p.win.end]);

  return (
    <div className="timeline" ref={p.scroller}>
      <div className="tlinner" ref={inner} style={{ width: width + 2 * PAD }}
           onPointerDown={(e) => p.onSeek(timeAt(e.clientX))}>
        <div className="tlstrip" style={{ left: PAD, width, height: STRIP_H }}>
          {Array.from({ length: strip.frames }, (_, i) => (
            <div key={i} style={{
              left: i * strip.every_s * p.pps, width: strip.every_s * p.pps + 1,
              backgroundImage: `url(${strip.url})`,
              backgroundSize: `${strip.cols * tileW}px auto`,
              backgroundPosition: `${-(i % strip.cols) * tileW}px ${-Math.floor(i / strip.cols) * STRIP_H}px`,
            }} />
          ))}
        </div>
        <canvas ref={wave} className="tlwave" height={WAVE_H} style={{ left: PAD, width, top: STRIP_H + 4 }} />
        {gaps.map(([a, b]) => <div key={a} className="tlgap" style={{ left: x(a), width: (b - a) * p.pps }} />)}
        {p.events.map((e) => {
          const zoomed = e.kind === "self_kill" && p.zooms.some((z) => Math.abs(z - e.t) < 0.75);
          return (
            <div key={`${e.kind}${e.t}`} className={`tlevent ${e.kind}${zoomed ? " zoomed" : ""}`} style={{ left: x(e.t) }}
                 title={e.kind === "self_kill" ? (zoomed ? "Kill, zoomed: tap to remove the zoom" : "Kill: tap to zoom")
                   : e.kind.replace("_", " ")}
                 onPointerDown={(ev) => {
                   if (e.kind !== "self_kill") return;
                   ev.stopPropagation();
                   p.onEventTap(e.t);
                 }} />
          );
        })}
        {p.segments.map((s, i) => (
          // Keyed by position: a key from the start time would remount the part mid-drag and drop the finger.
          <div key={i} className={i === p.selected ? "tlpart on" : "tlpart"}
               style={{ left: x(s.start), width: (s.end - s.start) * p.pps }}
               onPointerDown={(e) => { e.stopPropagation(); p.onSelect(i); p.onSeek(timeAt(e.clientX)); }}>
            {s.speed !== 1 && <span className="tlspeed">{s.speed}×</span>}
            <div className="tlhandle start" onPointerDown={drag(i, "start")} aria-label="Trim start" />
            <div className="tlhandle end" onPointerDown={drag(i, "end")} aria-label="Trim end" />
          </div>
        ))}
        {(p.music ?? []).map(([a, b]) => (
          <div key={`m${a}`} className="tlmusic" style={{ left: x(Math.max(a, p.win.start)), width: Math.max(2, (Math.min(b, p.win.end) - Math.max(a, p.win.start)) * p.pps) }}
               title="Music" />
        ))}
        <div className="tlplayhead" ref={p.playhead} style={{ left: PAD }} />
      </div>
    </div>
  );
}

export const TIMELINE_PAD = PAD;
