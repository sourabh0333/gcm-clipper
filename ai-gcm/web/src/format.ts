export function clock(seconds: number): string {
  const s = Math.max(0, Math.floor(seconds));
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const rest = String(s % 60).padStart(2, "0");
  return h ? `${h}:${String(m).padStart(2, "0")}:${rest}` : `${m}:${rest}`;
}

export function duration(seconds: number | null | undefined): string {
  if (!seconds) return "";
  const minutes = Math.round(seconds / 60);
  return minutes >= 60 ? `${Math.floor(minutes / 60)} h ${minutes % 60} min` : `${minutes} min`;
}

export function bytes(n: number | null | undefined): string {
  if (!n) return "0 MB";
  return n >= 1024 ** 3 ? `${(n / 1024 ** 3).toFixed(1)} GB` : `${Math.round(n / 1024 ** 2)} MB`;
}

// A post's time in the creator's own clock: "Tue 11 Nov, 7:00 pm".
export function when(iso: string | null | undefined): string {
  if (!iso) return "";
  return new Date(iso).toLocaleString("en-IN", { weekday: "short", day: "numeric", month: "short", hour: "numeric",
                                                 minute: "2-digit" });
}

export const POST_LABEL: Record<string, string> = {
  draft: "draft", approved: "approved", uploading: "uploading", scheduled: "scheduled", posted: "posted",
  failed: "failed", cancelled: "cancelled",
};

export const STATUS_LABEL: Record<string, string> = {
  uploading: "Uploading",
  queued: "Waiting",
  running: "Working",
  stopped: "Stopped",
  done: "Ready",
  failed: "Failed",
};

export const TYPE_LABEL: Record<string, string> = {
  multi_kill: "Multi-kill",
  fight: "Fight",
  win: "Chicken dinner",
  funny: "Funny",
  rage: "Rage",
  banter: "Banter",
  hype: "Hype",
  talk: "Talk",
  reaction: "Reaction",
  marked: "You marked this",
};

export const STAGE_LABEL: Record<string, string> = {
  ingest: "Reading the video",
  vision: "Watching the game",
  audio: "Listening",
  sounds: "Finding laughs and shouts",
  transcript: "Writing down the talk",
  moments: "Picking moments",
  judge: "Ranking",
  captions: "Captions",
  render: "Cutting the clips",
  review: "Finishing",
};
