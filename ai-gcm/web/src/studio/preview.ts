// Draws one frame of the export on a canvas, from the preview copy, with the same layout numbers the
// renderer uses (aigcm/studio/render.py): background (blurred cover or black), then each panel's crop
// in its canvas rectangle, the game panel zoomed at kills. The canvas is half size (540x960) to stay
// smooth on phones; every coordinate is scaled by the same factor.
import type { EditData } from "../api";
import { CAPTION_MARGIN, type Chunk, H, hookBox, HUD_STRIP, panelSource, toOutput, W, zoomAt } from "./model";

export type Overlays = { hook?: HTMLImageElement | null; chunks?: Chunk[]; strip?: HTMLImageElement | null };
const STRIP_Y = H - 140 - 30;   // brand.STRIP_Y
const CAPTION_COLOURS = { white: "#fff", yellow: "#ffe600" };
const CAPTION_SIZES = { normal: 78, large: 92 };
export const CAPTION_FONT = "Mukta ExtraBold";

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

export function drawFrame(ctx: CanvasRenderingContext2D, video: HTMLVideoElement, edit: EditData, sourceT: number,
                          overlays: Overlays = {}) {
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
  if (edit.layout.band_h) {
    ctx.fillStyle = "#000";
    ctx.fillRect(0, 0, PREVIEW_W, edit.layout.band_h * K);
  }
  for (const panel of edit.layout.panels) {
    const zoomed = panel.role === "game" ? zoom : 1;
    const [sx, sy, sw, sh] = panelSource(panel, vw, vh, zoomed);
    const [dx, dy, dw, dh] = panel.dst;
    ctx.drawImage(video, sx, sy, sw, sh, dx * K, dy * K, dw * K, dh * K);
    if (zoomed > 1 && edit.keep_hud !== false) {
      // The renderer lays the unzoomed top strip (the kill counters) back over a zoomed game panel.
      const [ux, uy, uw, uh] = panelSource(panel, vw, vh, 1);
      ctx.drawImage(video, ux, uy, uw, uh * HUD_STRIP, dx * K, dy * K, dw * K, dh * HUD_STRIP * K);
    }
  }
  if (edit.hook.on && overlays.hook?.complete && overlays.hook.naturalWidth) {
    // The hook is the same image the export lays over the video, drawn by the server.
    const [y, h] = hookBox(edit.layout);
    ctx.drawImage(overlays.hook, 0, y * K, PREVIEW_W, h * K);
  }
  if (edit.lower_third && overlays.strip?.complete && overlays.strip.naturalWidth) {
    ctx.drawImage(overlays.strip, 0, STRIP_Y * K, PREVIEW_W, overlays.strip.naturalHeight * K);
  }
  if (edit.captions.on && out !== null) {
    const chunk = overlays.chunks?.find((c) => out >= c.start && out < c.end);
    if (chunk) {
      // As the export's captions: bold, white, black outline, centred, CAPTION_MARGIN up from the bottom.
      const size = CAPTION_SIZES[edit.captions.size ?? "normal"] * K;
      ctx.font = `${size}px "${CAPTION_FONT}", sans-serif`;
      ctx.textAlign = "center";
      ctx.textBaseline = "bottom";
      ctx.lineJoin = "round";
      const x = PREVIEW_W / 2;
      const y = PREVIEW_H - (CAPTION_MARGIN[edit.layout.template] ?? 380) * K;
      const text = chunk.text.toUpperCase();
      ctx.lineWidth = 12 * K;
      ctx.strokeStyle = "#000";
      ctx.strokeText(text, x, y, PREVIEW_W - 120 * K);
      ctx.fillStyle = CAPTION_COLOURS[edit.captions.color ?? "white"];
      ctx.fillText(text, x, y, PREVIEW_W - 120 * K);
    }
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
