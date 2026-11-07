// The upload in progress lives here, outside any screen, so moving around the app doesn't stop it. Only
// closing the tab does; picking the same file again then resumes from the server's offset.
import * as tus from "tus-js-client";

export const CHUNK = 8 * 1024 * 1024; // keeps each request inside Cloudflare's limits later (M2 review R5)

export type UploadState = {
  fileName: string;
  sent: number;
  total: number;
  speed: number; // bytes per second, smoothed
  status: "sending" | "paused" | "error" | "done";
  error: string;
  streamId: string | null;
};

let upload: tus.Upload | null = null;
let state: UploadState | null = null;
const listeners = new Set<(s: UploadState | null) => void>();

function set(patch: Partial<UploadState>) {
  state = state ? { ...state, ...patch } : null;
  listeners.forEach((fn) => fn(state));
}

export function current() {
  return state;
}

export function subscribe(fn: (s: UploadState | null) => void) {
  listeners.add(fn);
  return () => {
    listeners.delete(fn);
  };
}

export function uploadMetadata(file: File, title: string, recordedOn: string, liveId: string) {
  const meta: Record<string, string> = { filename: file.name, title: title || file.name, game: "bgmi" };
  if (recordedOn) meta.recorded_on = recordedOn;
  if (liveId) meta.live_session = liveId;
  return meta;
}

function readableError(err: Error) {
  const text = String(err.message || err);
  const detail = text.match(/response text: (\{.*\})/);
  if (detail) {
    try {
      return (JSON.parse(detail[1]) as { detail?: string }).detail ?? text;
    } catch {
      /* fall through */
    }
  }
  return text.slice(0, 200);
}

export async function startUpload(file: File, metadata: Record<string, string>) {
  if (state && (state.status === "sending" || state.status === "paused")) throw new Error("An upload is already going.");
  let mark = { at: Date.now(), sent: 0 };
  state = { fileName: file.name, sent: 0, total: file.size, speed: 0, status: "sending", error: "", streamId: null };
  listeners.forEach((fn) => fn(state));
  upload = new tus.Upload(file, {
    endpoint: `${location.origin}/api/uploads`,
    chunkSize: CHUNK,
    retryDelays: [0, 1000, 3000, 5000, 10000, 20000, 30000],
    headers: { "X-Kaatclip": "1" },
    metadata,
    removeFingerprintOnSuccess: true,
    onAfterResponse(_req, res) {
      const id = res.getHeader("X-Stream-Id");
      if (id && state) state.streamId = id;
    },
    onProgress(sent, total) {
      const now = Date.now();
      const seconds = (now - mark.at) / 1000;
      if (seconds >= 2) {
        const speed = (sent - mark.sent) / seconds;
        mark = { at: now, sent };
        set({ sent, total, speed: state?.speed ? state.speed * 0.6 + speed * 0.4 : speed });
      } else set({ sent, total });
    },
    onError(err) {
      set({ status: "error", error: readableError(err) });
    },
    onSuccess() {
      set({ status: "done", sent: file.size });
    },
  });
  const previous = await upload.findPreviousUploads();
  if (previous.length) upload.resumeFromPreviousUpload(previous[0]);
  upload.start();
}

export function pauseUpload() {
  void upload?.abort();
  set({ status: "paused", speed: 0 });
}

export function resumeUpload() {
  set({ status: "sending", error: "" });
  upload?.start();
}

export function clearUpload() {
  if (state?.status === "sending") return;
  upload = null;
  state = null;
  listeners.forEach((fn) => fn(state));
}
