// The editor's arithmetic, kept apart from the screen so it can be tested. It mirrors the server:
// aigcm/studio/edit.py (time mapping, limits) and aigcm/studio/render.py (zoom, panel crops), so the
// preview shows what the export will be.
import type { Box, EditData, Panel, Segment, Template } from "../api";

export const W = 1080;
export const H = 1920;
export const MIN_PART_S = 0.3;
export const MAX_LENGTH_S = 180;
export const SPEEDS = [1, 1.5, 2, 3];
const ZOOM_IN_S = 0.25;
const ZOOM_OUT_S = 0.35;
const ZOOM_LEAD_S = 0.4;
const ZOOM_MERGE_S = 2;
export const FACECAM_H = 760;
export const BAND_H = 420;
export const HUD_STRIP = 0.13;
export const ZOOM_STRENGTHS: [string, number][] = [["Off", 0], ["Light", 1.15], ["Strong", 1.3]];

export const round = (x: number) => Math.round(x * 1000) / 1000;

export function outputLength(segs: Segment[]): number {
  return segs.reduce((sum, s) => sum + (s.end - s.start) / s.speed, 0);
}

/** Where source time t lands in the export, or null if it was cut out. */
export function toOutput(segs: Segment[], t: number): number | null {
  let offset = 0;
  for (const s of segs) {
    if (t >= s.start && t <= s.end) return offset + (t - s.start) / s.speed;
    offset += (s.end - s.start) / s.speed;
  }
  return null;
}

/** The source time shown at output time `out`, and the part it is in. */
export function toSource(segs: Segment[], out: number): { t: number; index: number } {
  let offset = 0;
  for (let i = 0; i < segs.length; i++) {
    const s = segs[i];
    const len = (s.end - s.start) / s.speed;
    if (out < offset + len || i === segs.length - 1) {
      return { t: Math.min(s.end, s.start + Math.max(0, out - offset) * s.speed), index: i };
    }
    offset += len;
  }
  return { t: 0, index: 0 };
}

export function partAt(segs: Segment[], t: number): number {
  return segs.findIndex((s) => t >= s.start && t <= s.end);
}

/** Split the part under source time t in two; unchanged if t is too close to an edge. */
export function split(segs: Segment[], t: number): Segment[] {
  const i = partAt(segs, t);
  if (i < 0) return segs;
  const s = segs[i];
  if (t - s.start < MIN_PART_S || s.end - t < MIN_PART_S) return segs;
  return [...segs.slice(0, i), { ...s, end: round(t) }, { ...s, start: round(t) }, ...segs.slice(i + 1)];
}

export function removePart(segs: Segment[], i: number): Segment[] {
  return segs.length > 1 ? segs.filter((_, j) => j !== i) : segs;
}

export function setSpeed(segs: Segment[], i: number, speed: number): Segment[] {
  return segs.map((s, j) => (j === i ? { ...s, speed } : s));
}

/** Move one edge of part i to source time t, kept inside the footage, off its neighbours, and at least
 *  MIN_PART_S long. */
export function trim(segs: Segment[], i: number, edge: "start" | "end", t: number, lo: number, hi: number): Segment[] {
  const s = segs[i];
  let value: number;
  if (edge === "start") {
    const floor = i > 0 ? segs[i - 1].end : lo;
    value = Math.min(Math.max(t, floor), s.end - MIN_PART_S);
  } else {
    const ceil = i < segs.length - 1 ? segs[i + 1].start : hi;
    value = Math.max(Math.min(t, ceil), s.start + MIN_PART_S);
  }
  return segs.map((p, j) => (j === i ? { ...p, [edge]: round(value) } : p));
}

/** Bring back a few seconds of cut footage at source time t (a new part, between its neighbours). */
export function addPart(segs: Segment[], t: number, lo: number, hi: number, length = 5): Segment[] {
  if (partAt(segs, t) >= 0) return segs;
  const next = segs.find((s) => s.start > t);
  const end = Math.min(t + length, next ? next.start : hi);
  if (end - t < MIN_PART_S || t < lo) return segs;
  return [...segs, { start: round(t), end: round(end), speed: 1 }].sort((a, b) => a.start - b.start);
}

/** Zooms on each kill inside [a, b], kills close together sharing one (as the server's default edit). */
export function killZooms(events: { t: number; kind: string }[], a: number, b: number, scale = 1.25) {
  const zooms: EditData["zooms"] = [];
  for (const t of events.filter((e) => e.kind === "self_kill" && e.t >= a && e.t <= b).map((e) => e.t).sort((x, y) => x - y)) {
    if (zooms.length && t - zooms[zooms.length - 1].t < ZOOM_MERGE_S) continue;
    zooms.push({ t, dur: 1.2, scale });
  }
  return zooms;
}

/** Zoom on every kill inside the edit's parts at this strength (0 = no zooms). */
export function setZoomStrength(edit: EditData, events: { t: number; kind: string }[], scale: number): EditData {
  if (!scale) return { ...edit, zooms: [] };
  const zooms = edit.segments.flatMap((s) => killZooms(events, s.start, s.end, scale));
  return { ...edit, zooms };
}

/** Add a zoom at kill time t, or take away the one already there. */
export function toggleZoom(edit: EditData, t: number): EditData {
  const near = edit.zooms.findIndex((z) => Math.abs(z.t - t) < 0.75);
  if (near >= 0) return { ...edit, zooms: edit.zooms.filter((_, i) => i !== near) };
  const scale = edit.zooms.length ? Math.max(...edit.zooms.map((z) => z.scale)) : 1.25;
  return { ...edit, zooms: [...edit.zooms, { t, dur: 1.2, scale }].sort((a, b) => a.t - b.t) };
}

export function zoomStrength(edit: EditData): number {
  return edit.zooms.length ? Math.max(...edit.zooms.map((z) => z.scale)) : 0;
}

const even = (x: number) => Math.round(x / 2) * 2;

/** The starting panels of a layout template: the same numbers as edit.py's template_layout. "split"
 *  needs the camera box (frame fractions); without one it falls back to "blur". */
export function templateLayout(template: Template, width: number, height: number, facecam: Box | null): EditData["layout"] {
  const aspect = width / height;
  const full: Box = [0, 0, 1, 1];
  if (template === "native") {
    let w = W;
    let h = even(W / aspect);
    if (h > H) [w, h] = [even(H * aspect), H];
    return { template: "native", background: "black", band_h: 0,
             panels: [{ role: "game", src: full, dst: [Math.floor((W - w) / 2), Math.floor((H - h) / 2), w, h] }] };
  }
  const gameH = Math.min(even(W / aspect), H);
  if (template === "split" && facecam) {
    return { template: "split", background: "blur", band_h: 0, panels: [
      { role: "cam", src: facecam, dst: [0, 0, W, FACECAM_H] },
      { role: "game", src: full, dst: [0, FACECAM_H, W, Math.min(gameH, H - FACECAM_H)] }] };
  }
  if (template === "band") {
    const game: Panel = { role: "game", src: full, dst: [0, BAND_H, W, Math.min(gameH, H - BAND_H)] };
    const below = BAND_H + game.dst[3];
    const panels = [game];
    if (facecam && H - below >= 200) panels.push({ role: "cam", src: facecam, dst: [0, below, W, H - below] });
    return { template: "band", background: "blur", band_h: BAND_H, panels };
  }
  return { template: "blur", background: "blur", band_h: 0,
           panels: [{ role: "game", src: full, dst: [0, Math.floor((H - gameH) / 2), W, gameH] }] };
}

export function cameraBox(edit: EditData): Box | null {
  return edit.layout.panels.find((p) => p.role === "cam")?.src ?? null;
}

/** A length preset: one part [a, b]; landscape layouts get a zoom on each kill inside it. */
export function applyPreset(edit: EditData, a: number, b: number, events: { t: number; kind: string }[]): EditData {
  return {
    ...edit,
    segments: [{ start: round(a), end: round(b), speed: 1 }],
    zooms: edit.layout.template === "native" ? edit.zooms : killZooms(events, a, b),
  };
}

const clip01 = (x: number) => Math.min(1, Math.max(0, x));

/** The game panel's zoom at output time t: the renderer's zoom_expr, evaluated. */
export function zoomAt(edit: EditData, t: number): number {
  let z = 1;
  for (const zoom of edit.zooms) {
    const at = toOutput(edit.segments, zoom.t);
    if (at === null || zoom.scale <= 1) continue;
    const a = Math.max(0, at - ZOOM_LEAD_S);
    const b = at + zoom.dur;
    z += (zoom.scale - 1) * clip01((t - a) / ZOOM_IN_S) * clip01((b - t) / ZOOM_OUT_S);
  }
  return z;
}

/** The source rectangle (video pixels) a panel shows: its crop, trimmed to the panel's shape from the
 *  centre (ffmpeg's scale "increase" + crop), then narrowed by the zoom around the centre. */
export function panelSource(panel: Panel, vw: number, vh: number, zoom = 1): [number, number, number, number] {
  const [fx, fy, fw, fh] = panel.src;
  let [x, y, w, h] = [fx * vw, fy * vh, fw * vw, fh * vh];
  const want = panel.dst[2] / panel.dst[3];
  if (w / h > want) {
    const nw = h * want;
    x += (w - nw) / 2;
    w = nw;
  } else {
    const nh = w / want;
    y += (h - nh) / 2;
    h = nh;
  }
  if (zoom > 1) {
    const nw = w / zoom;
    const nh = h / zoom;
    x += (w - nw) / 2;
    y += (h - nh) / 2;
    w = nw;
    h = nh;
  }
  return [x, y, w, h];
}

/** Problems that would stop the server saving the edit, in plain words; empty when it can be saved. */
export function problems(edit: EditData, lo: number, hi: number): string[] {
  const out: string[] = [];
  const total = outputLength(edit.segments);
  if (total > MAX_LENGTH_S + 0.01) out.push(`The clip is ${Math.round(total)} s; Shorts can be at most 3 minutes.`);
  if (edit.segments.some((s) => s.start < lo - 0.05 || s.end > hi + 0.05)) out.push("A part reaches outside the saved footage.");
  if (edit.segments.some((s) => s.end - s.start < MIN_PART_S)) out.push("A part is too short.");
  return out;
}
