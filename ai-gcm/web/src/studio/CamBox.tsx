import { useEffect, useRef, useState } from "react";
import type { Box } from "../api";

type Props = { video: HTMLVideoElement; box: Box; onDone: (box: Box) => void; onCancel: () => void };

const MIN = 0.05;
const clamp = (x: number, lo: number, hi: number) => Math.min(hi, Math.max(lo, x));

// The whole source frame with the camera box on it: drag inside the box to move it, drag a corner to
// resize it. Used when the camera wasn't found automatically (a handcam, a face turned away) or is off.
export default function CamBox({ video, box: start, onDone, onCancel }: Props) {
  const [box, setBox] = useState<Box>(start);
  const frame = useRef<HTMLDivElement>(null);
  const canvas = useRef<HTMLCanvasElement>(null);
  const card = useRef<HTMLDivElement>(null);

  useEffect(() => { card.current?.scrollIntoView?.({ behavior: "smooth", block: "center" }); }, []);

  useEffect(() => {
    const c = canvas.current;
    const ctx = c?.getContext("2d");
    if (!c || !ctx || !video.videoWidth) return;
    c.width = 640;
    c.height = Math.round((640 * video.videoHeight) / video.videoWidth);
    ctx.drawImage(video, 0, 0, c.width, c.height);
  }, [video]);

  function drag(mode: "move" | "tl" | "br") {
    return (event: React.PointerEvent) => {
      event.stopPropagation();
      (event.target as HTMLElement).setPointerCapture(event.pointerId);
      const rect = frame.current!.getBoundingClientRect();
      const [x0, y0] = [event.clientX, event.clientY];
      const before = box;
      const move = (e: PointerEvent) => {
        const dx = (e.clientX - x0) / rect.width;
        const dy = (e.clientY - y0) / rect.height;
        const [x, y, w, h] = before;
        if (mode === "move") setBox([clamp(x + dx, 0, 1 - w), clamp(y + dy, 0, 1 - h), w, h]);
        if (mode === "br") setBox([x, y, clamp(w + dx, MIN, 1 - x), clamp(h + dy, MIN, 1 - y)]);
        if (mode === "tl") {
          const nx = clamp(x + dx, 0, x + w - MIN);
          const ny = clamp(y + dy, 0, y + h - MIN);
          setBox([nx, ny, x + w - nx, y + h - ny]);
        }
      };
      const up = () => {
        window.removeEventListener("pointermove", move);
        window.removeEventListener("pointerup", up);
        window.removeEventListener("pointercancel", up);
      };
      window.addEventListener("pointermove", move);
      window.addEventListener("pointerup", up);
      window.addEventListener("pointercancel", up);
    };
  }

  const pct = (v: number) => `${(v * 100).toFixed(2)}%`;
  return (
    <div className="card cambox" ref={card}>
      <div className="title">Camera box</div>
      <p className="small muted">Drag the box onto your camera; drag a corner to resize it. It's remembered for this stream's other clips.</p>
      <div className="camframe" ref={frame}>
        <canvas ref={canvas} />
        <div className="camrect" style={{ left: pct(box[0]), top: pct(box[1]), width: pct(box[2]), height: pct(box[3]) }}
             onPointerDown={drag("move")} aria-label="Camera box">
          <div className="camcorner tl" onPointerDown={drag("tl")} aria-label="Resize from the top left" />
          <div className="camcorner br" onPointerDown={drag("br")} aria-label="Resize from the bottom right" />
        </div>
      </div>
      <div className="row" style={{ marginTop: 10 }}>
        <button className="primary" onClick={() => onDone(box.map((v) => Math.round(v * 10000) / 10000) as Box)}>Use this box</button>
        <button onClick={onCancel}>Cancel</button>
      </div>
    </div>
  );
}
