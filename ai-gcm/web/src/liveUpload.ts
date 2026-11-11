// Upload while streaming: the creator picks OBS's recording once, at the start of the stream, and this sends it
// to the laptop as it grows. Chrome and Edge can re-read a picked file (File System Access API), so each look
// gets the bytes OBS has written since. The last few MB stay back while recording, because OBS may still touch
// them. When the file stops growing (or the creator taps "Stream ended"), the laptop's copy is compared piece by
// piece with the finished file, pieces OBS rewrote (the start of an MKV or MP4) are re-sent, and the rest goes
// with the final size, which queues the stream like any upload. Like the normal upload, it lives outside any
// screen, so moving around the app doesn't stop it; closing the tab does, and "Carry on" picks it up again.

export const PIECE = 8 * 1024 * 1024;     // matches the server's HASH_PIECE
const MARGIN = 4 * 1024 * 1024;           // not sent while OBS is still writing
const LOOK_MS = 5000;
export const STILL_MS = 90_000;           // no growth this long: the recording has stopped
const SAVED = "kc_live_upload";

type Handle = { getFile(): Promise<File>; name: string };
declare global {
  interface Window {
    showOpenFilePicker?: (options?: unknown) => Promise<Handle[]>;
  }
}

export type LiveState = {
  fileName: string;
  sent: number;            // bytes the laptop has
  size: number;            // the recording's size on this PC
  status: "uploading" | "finishing" | "done" | "error" | "stopped";
  note: string;
  streamId: string | null;
  grewAt: number;          // when the recording last grew (ms)
};

let state: LiveState | null = null;
let handle: Handle | null = null;
let url = "";
let timer: number | undefined;
let busy = false;
let finishAsked = false;
const listeners = new Set<(s: LiveState | null) => void>();

function set(patch: Partial<LiveState>) {
  state = state ? { ...state, ...patch } : null;
  listeners.forEach((fn) => fn(state));
}

export const liveSupported = () => typeof window !== "undefined" && typeof window.showOpenFilePicker === "function";
export const liveCurrent = () => state;
export function liveSubscribe(fn: (s: LiveState | null) => void) {
  listeners.add(fn);
  return () => { listeners.delete(fn); };
}

// An upload left unfinished when the tab closed: picking the same recording again carries on.
export function savedLive(): { url: string; name: string; streamId: string } | null {
  try {
    return JSON.parse(localStorage.getItem(SAVED) ?? "null");
  } catch {
    return null;
  }
}

function encodeMeta(meta: Record<string, string>) {
  const b64 = (text: string) => btoa(String.fromCharCode(...new TextEncoder().encode(text)));
  return Object.entries(meta).map(([k, v]) => `${k} ${b64(v)}`).join(",");
}

const TUS = { "Tus-Resumable": "1.0.0", "X-Kaatclip": "1" };

async function detail(res: Response) {
  try {
    return ((await res.json()) as { detail?: string }).detail ?? `The laptop answered ${res.status}.`;
  } catch {
    return `The laptop answered ${res.status}.`;
  }
}

// OBS writes all the time, and Chrome refuses to read a picked file that changed since it was looked at, so
// each read takes a fresh look and tries again a few times.
async function readPiece(at: number, length: number): Promise<ArrayBuffer> {
  let last: unknown;
  for (let attempt = 0; attempt < 8; attempt++) {
    try {
      const file = await handle!.getFile();
      return await file.slice(at, at + length).arrayBuffer();
    } catch (err) {
      last = err;
      await new Promise((r) => setTimeout(r, 150 * (attempt + 1)));
    }
  }
  throw last instanceof Error ? last : new Error("Couldn't read the recording.");
}

async function sendPiece(body: ArrayBuffer, final?: number) {
  const headers: Record<string, string> = { ...TUS, "Upload-Offset": String(state!.sent), "Content-Type": "application/offset+octet-stream" };
  if (final !== undefined) headers["Upload-Length"] = String(final);
  const res = await fetch(url, { method: "PATCH", headers, body, credentials: "same-origin" });
  if (res.status === 409) {        // the laptop has a different count (a lost answer): ask and carry on
    await syncOffset();
    return;
  }
  if (!res.ok) throw new Error(await detail(res));
  set({ sent: Number(res.headers.get("Upload-Offset") ?? state!.sent + body.byteLength) });
}

async function syncOffset() {
  const res = await fetch(url, { method: "HEAD", headers: TUS, credentials: "same-origin" });
  if (!res.ok) throw new Error("This upload is gone from the laptop. Start again.");
  set({ sent: Number(res.headers.get("Upload-Offset") ?? 0), streamId: res.headers.get("X-Stream-Id") ?? state?.streamId ?? null });
}

async function sha256(buffer: ArrayBuffer) {
  const digest = await crypto.subtle.digest("SHA-256", buffer);
  return Array.from(new Uint8Array(digest), (b) => b.toString(16).padStart(2, "0")).join("");
}

async function look() {
  if (busy || !state || !handle) return;
  busy = true;
  try {
    const file = await handle.getFile();
    if (file.size !== state.size) set({ size: file.size, grewAt: Date.now() });
    const stopped = finishAsked || Date.now() - state.grewAt > STILL_MS;
    if (stopped) {
      await finish();
      return;
    }
    while (state.status === "uploading" && state.sent + PIECE <= state.size - MARGIN) {
      await sendPiece(await readPiece(state.sent, PIECE));
    }
    set({ note: "" });
  } catch (err) {
    // A failed look or finish is tried again on the next look; finishing starts over from the check.
    set({ status: state?.status === "finishing" ? "uploading" : state?.status, note: `${(err as Error).message} Trying again…` });
  } finally {
    busy = false;
  }
  if (state?.status === "uploading") timer = window.setTimeout(look, LOOK_MS);
}

// The recording has stopped: make the laptop's copy match the finished file, then send the rest.
async function finish() {
  set({ status: "finishing", note: "Checking the recording…" });
  // Make sure OBS really is done: the size must stay the same for a few seconds.
  let size = (await handle!.getFile()).size;
  for (;;) {
    await new Promise((r) => setTimeout(r, 4000));
    const now = (await handle!.getFile()).size;
    if (now === size) break;
    size = now;
  }
  set({ size });
  await syncOffset();
  const res = await fetch(`${url}/hashes`, { headers: TUS, credentials: "same-origin" });
  if (!res.ok) throw new Error(await detail(res));
  const server = (await res.json()) as { piece: number; offset: number; hashes: string[] };
  let fixed = 0;
  for (let i = 0; i < server.hashes.length; i++) {
    const at = i * server.piece;
    const length = Math.min(server.piece, server.offset - at);
    const local = await readPiece(at, length);
    if ((await sha256(local)) !== server.hashes[i]) {
      const put = await fetch(`${url}/rewrite?at=${at}`, { method: "PUT", headers: TUS, body: local, credentials: "same-origin" });
      if (!put.ok) throw new Error(await detail(put));
      fixed++;
    }
    if (i % 10 === 0) set({ note: `Checking the recording… ${Math.round(((i + 1) / server.hashes.length) * 100)}%` });
  }
  set({ note: fixed ? `Corrected ${fixed} piece${fixed > 1 ? "s" : ""}; sending the rest…` : "Sending the rest…" });
  if (state!.sent >= size) await sendPiece(new ArrayBuffer(0), size);
  while (state!.sent < size) {
    const length = Math.min(PIECE, size - state!.sent);
    await sendPiece(await readPiece(state!.sent, length), size);
  }
  localStorage.removeItem(SAVED);
  set({ status: "done", note: "" });
}

async function run() {
  finishAsked = false;
  window.clearTimeout(timer);
  timer = window.setTimeout(look, 500);
}

async function pick(): Promise<{ handle: Handle; file: File }> {
  const [picked] = await window.showOpenFilePicker!({
    types: [{ description: "Stream recording", accept: { "video/*": [".mkv", ".mp4", ".mov"] } }],
  });
  const file = await picked.getFile();
  if (!/\.(mkv|mp4|mov)$/i.test(file.name)) throw new Error("Pick the MKV, MP4 or MOV recording OBS is writing.");
  return { handle: picked, file };
}

export async function startLive(meta: Record<string, string>) {
  if (state && (state.status === "uploading" || state.status === "finishing")) throw new Error("An upload is already going.");
  const picked = await pick();
  const res = await fetch("/api/uploads", {
    method: "POST", credentials: "same-origin",
    headers: { ...TUS, "Upload-Defer-Length": "1", "Upload-Metadata": encodeMeta({ ...meta, filename: picked.file.name }) },
  });
  if (res.status !== 201) throw new Error(await detail(res));
  handle = picked.handle;
  url = res.headers.get("Location")!;
  const streamId = res.headers.get("X-Stream-Id");
  localStorage.setItem(SAVED, JSON.stringify({ url, name: picked.file.name, streamId }));
  state = { fileName: picked.file.name, sent: 0, size: picked.file.size, status: "uploading", note: "", streamId, grewAt: Date.now() };
  listeners.forEach((fn) => fn(state));
  await run();
}

// After the tab closed or the PC restarted: pick the same recording (still growing or finished) and carry on.
export async function carryOn() {
  const saved = savedLive();
  if (!saved) throw new Error("Nothing to carry on.");
  const picked = await pick();
  if (picked.file.name !== saved.name) throw new Error(`Pick the same recording: ${saved.name}.`);
  handle = picked.handle;
  url = saved.url;
  state = { fileName: saved.name, sent: 0, size: picked.file.size, status: "uploading", note: "", streamId: saved.streamId, grewAt: Date.now() };
  listeners.forEach((fn) => fn(state));
  await syncOffset();
  await run();
}

export function streamEnded() {
  finishAsked = true;
  window.clearTimeout(timer);
  void look();
}

export async function stopLive() {
  window.clearTimeout(timer);
  if (url) await fetch(url, { method: "DELETE", headers: TUS, credentials: "same-origin" }).catch(() => {});
  localStorage.removeItem(SAVED);
  set({ status: "stopped", note: "" });
}

export function clearLive() {
  if (state?.status === "uploading" || state?.status === "finishing") return;
  state = null;
  handle = null;
  url = "";
  listeners.forEach((fn) => fn(state));
}
