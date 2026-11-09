// The one way the app talks to the API. Every state-changing call carries the X-Kaatclip header the
// server's cross-site guard asks for; cookies carry the session.

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

export async function api<T>(path: string, init: { method?: string; body?: unknown } = {}): Promise<T> {
  const method = init.method ?? (init.body === undefined ? "GET" : "POST");
  const headers: Record<string, string> = {};
  if (method !== "GET") headers["X-Kaatclip"] = "1";
  if (init.body !== undefined) headers["Content-Type"] = "application/json";
  const res = await fetch(path, {
    method,
    headers,
    credentials: "same-origin",
    body: init.body === undefined ? undefined : JSON.stringify(init.body),
  });
  if (res.status === 204) return undefined as T;
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new ApiError(res.status, (data as { detail?: string }).detail ?? `Request failed (${res.status})`);
  return data as T;
}

export type Me = { email: string; name: string | null; picture: string | null; admin: boolean };

export type Stage = { name: string; status: string; seconds: number | null };

export type StreamSummary = {
  id: string;
  title: string;
  game: string;
  status: "uploading" | "queued" | "running" | "stopped" | "done" | "failed";
  recorded_on: string | null;
  duration_s: number | null;
  size_bytes: number | null;
  error: string | null;
  stopping: boolean;
  created_at: string;
  clips: number;
  kept: number;
  reviewed: number;
  upload?: { id: string; offset: number; length: number };
  progress?: { stages: Stage[]; fraction: number; last_log: string | null };
};

export type Clip = {
  id: number;
  stream_id: string;
  rank: number;
  start_s: number;
  end_s: number;
  length_s: number;
  type: string;
  score: number | null;
  title: string | null;
  why: string | null;
  titles: string[];
  hashtags: string[];
  description: string | null;
  labels: Record<string, unknown>;
  flags: { kind?: string; text?: string }[] | string[];
  decision: "keep" | "reject" | null;
  reason: string | null;
  video: string;
  safe_video: string | null;
  stream_title?: string;
};

export type LibraryClip = Clip & { stream_title: string; poster: string | null; edited: boolean; exported: boolean };
export type LibraryPage = {
  items: LibraryClip[];
  total: number;
  offset: number;
  limit: number;
  facets: { streams: { id: string; title: string; count: number }[]; types: { type: string; count: number }[] };
};

export type LiveSession = { id: string; title: string | null; started_at: string; ended_at: string | null; markers: number[] };

export type WorkerStatus = { online: boolean; busy: boolean; queue_waiting: boolean };

// Studio (M3): a clip's edit list, the footage saved for editing it, and its exports.
export type Segment = { start: number; end: number; speed: number };
export type Panel = { role: "game" | "cam"; src: [number, number, number, number]; dst: [number, number, number, number] };
export type EditData = {
  v: 1;
  segments: Segment[];
  layout: { template: "native" | "blur" | "band" | "split"; background: "blur" | "black"; panels: Panel[] };
  zooms: { t: number; dur: number; scale: number }[];
  hook: { text: string; color: "white" | "yellow"; on: boolean };
  captions: { on: boolean };
  cover_t: number | null;
  sponsor_safe: boolean;
};
export type StudioWindow = {
  status: "ready" | "preparing" | "failed" | "none" | "missing";
  error?: string | null;
  start?: number;
  end?: number;
  duration?: number;
  width?: number;
  height?: number;
  has_audio?: boolean;
  preview?: string;
  wave?: string;
  strip?: { url: string; every_s: number; cols: number; rows: number; frames: number; tile_w: number; tile_h: number };
};
export type RenderJob = {
  id: string;
  kind: "prepare" | "export";
  status: "queued" | "running" | "done" | "failed";
  error: string | null;
  version: number | null;
  sponsor_safe: boolean;
  created_at: string | null;
  finished_at: string | null;
  video: string | null;
};
export type Studio = {
  clip: Clip;
  window: StudioWindow;
  edit: { version: number; data: EditData; length_s: number };
  exports: RenderJob[];
};
