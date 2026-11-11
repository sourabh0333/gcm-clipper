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

export type Me = { email: string; name: string | null; picture: string | null; admin: boolean; accepted?: boolean; terms_version?: string };

export type Stage = { name: string; status: string; seconds: number | null };

export type YouTubeChannel = {
  id: string;
  channel_id: string;
  title: string;
  thumbnail: string | null;
  status: "ok" | "expired";
  connected_at: string;
  settings: { made_for_kids: boolean; synthetic: boolean };
};
export type YouTubeState = { available: boolean; channels: YouTubeChannel[] };

export type PostStatus = "draft" | "approved" | "uploading" | "scheduled" | "posted" | "failed" | "cancelled";
export type Post = {
  id: string;
  status: PostStatus;
  kind: string;
  clip_id: number | null;
  clip_title: string | null;
  stream_id: string | null;
  render_id: string | null;
  video: string | null;
  play?: string | null;      // the light copy for playing in the app
  cover: string | null;
  channel: { id: string; title: string; thumbnail: string | null; status: string } | null;
  title: string;
  description: string;
  tags: string[];
  mode: "schedule" | "now";
  publish_at: string | null;
  approved_at: string | null;
  video_id: string | null;
  error: string | null;
  updated_at: string;
  created_at: string;
  posted_at: string | null;
  thumbnail: string | null;
  next_try_at: string | null;
  stream_link: string | null;
  stream_title: string | null;
  has_link: boolean;
  teaser_for: string | null;
  studio: { url: string; comment: string | null; related: string | null; done: boolean } | null;
};
export type Quota = { uploads: number; uploads_limit: number; units: number; units_limit: number };

export type StreamSummary = {
  id: string;
  title: string;
  game: string;
  status: "uploading" | "queued" | "running" | "stopped" | "done" | "failed";
  recorded_on: string | null;
  link: string | null;
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
  play?: string;             // the light copy for playing in the app; video is the full file
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

export type LiveMark = { t: number; source: string; by: string | null };
export type LiveSession = {
  id: string; title: string | null; started_at: string; ended_at: string | null; markers: number[];
  marks?: LiveMark[]; chat?: string | null;
};

export type WorkerStatus = { online: boolean; busy: boolean; queue_waiting: boolean };

// Studio (M3): a clip's edit list, the footage saved for editing it, and its exports.
export type Segment = { start: number; end: number; speed: number };
export type Panel = { role: "game" | "cam"; src: [number, number, number, number]; dst: [number, number, number, number] };
export type EditData = {
  v: 1;
  segments: Segment[];
  layout: { template: Template; background: "blur" | "black"; band_h?: number; panels: Panel[] };
  zooms: { t: number; dur: number; scale: number }[];
  hook: { text: string; color: "white" | "yellow"; on: boolean };
  captions: { on: boolean; script?: "auto" | "latin" | "devanagari"; words?: WordFix[]; color?: "white" | "yellow";
              size?: "normal" | "large" };
  cover_t: number | null;
  sponsor_safe: boolean;
  keep_hud?: boolean;
  lower_third?: boolean;
  sfx?: { t: number; name: "whoosh" | "boom" | "ding" | "pop"; gain: number }[];
  intro?: boolean;
  outro?: boolean;
};

export type BrandKit = {
  hook_color: "yellow" | "white";
  caption_color: "white" | "yellow";
  caption_size: "normal" | "large";
  lower_third: boolean;
  name: string;
  upi: string;
  instagram: string;
  use_intro: boolean;
  use_outro: boolean;
  description: string;
  hashtags: string[];
  disclaimer: string | null;
};
export type BrandView = {
  kit: BrandKit;
  files: { logo: string | null; intro: string | null; outro: string | null };
  lengths: { intro: number; outro: number };
  music?: { intro: number; outro: number };
  strip: string | null;
};
export type PostText = { title: string; description: string; hashtags: string[]; text: string };
export type Template = "native" | "blur" | "band" | "split";
export type WordFix = { t: number; w: string };
export type Word = { t: number; end: number; w: string };
export type Box = [number, number, number, number];
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
  play?: string | null;
  cover?: string | null;
};
export type Studio = {
  clip: Clip;
  window: StudioWindow;
  edit: { version: number; data: EditData; length_s: number };
  editor: {
    events: { t: number; kind: string }[];
    anchor: number | null;
    facecam: Box | null;
    facecam_source: "auto" | "manual" | null;
    words: Word[];
    brand: { strip: string | null; intro_s: number; outro_s: number };
    music: [number, number][];
    presets: { moment: [number, number]; full_fight: [number, number]; suggested: "moment" | "full_fight" };
  } | null;
  exports: RenderJob[];
};
