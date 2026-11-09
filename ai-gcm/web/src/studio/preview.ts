// Draws one frame of the export on a canvas, from the preview copy, with the same layout numbers the
// renderer uses (aigcm/studio/render.py): background (blurred cover or black), then each panel's crop
// in its canvas rectangle, the game panel zoomed at kills. The canvas is half size (540x960) to stay
// smooth on phones; every coordinate is scaled by the same factor.
import type { EditData } from "../api";
import { H, panelSource, toOutput, W, zoomAt } from "./model";

export const PREVIEW_W = 540;
export const PREVIEW_H = 960;
const K = PREVIEW_W / W;

function cover(vw: number, vh: number): [number, number, number, number] {
  const want = W / H;
  if (vw / vh > want) {
    const w = vh * want;
    return [(vw - w) / 2, 0, w, vh];
  }
  const h = vw / want;
  return [0, (vh - h) / 2, vw, h];
}

export function drawFrame(ctx: CanvasRenderingContext2D, video: HTMLVideoElement, edit: EditData, sourceT: number) {
  const vw = video.videoWidth;
  const vh = video.videoHeight;
  if (!vw || !vh) return;
  const out = toOutput(edit.segments, sourceT);
  const zoom = out === null ? 1 : zoomAt(edit, out);
  ctx.save();
  ctx.fillStyle = "#000";
  ctx.fillRect(0, 0, PREVIEW_W, PREVIEW_H);
  if (edit.layout.background === "blur") {
    ctx.filter = "blur(12px)";
    const [sx, sy, sw, sh] = cover(vw, vh);
    ctx.drawImage(video, sx, sy, sw, sh, -20, -20, PREVIEW_W + 40, PREVIEW_H + 40);
    ctx.filter = "none";
  }
  for (const panel of edit.layout.panels) {
    const [sx, sy, sw, sh] = panelSource(panel, vw, vh, panel.role === "game" ? zoom : 1);
    const [dx, dy, dw, dh] = panel.dst;
    ctx.drawImage(video, sx, sy, sw, sh, dx * K, dy * K, dw * K, dh * K);
  }
  if (out === null) {
    // A moment that is cut out: shown dimmed while scrubbing, so it's clear it won't be in the export.
    ctx.fillStyle = "rgba(0, 0, 0, 0.55)";
    ctx.fillRect(0, 0, PREVIEW_W, PREVIEW_H);
    ctx.fillStyle = "#fff";
    ctx.font = "bold 28px system-ui, sans-serif";
    ctx.textAlign = "center";
    ctx.fillText("Cut out", PREVIEW_W / 2, PREVIEW_H / 2);
  }
  ctx.restore();
}
