import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { clearLive, liveCurrent, PIECE, startLive, streamEnded } from "../liveUpload";

const MB = 1024 * 1024;

// The recording OBS is writing: grows, then its start changes when recording stops (like an MKV's header).
let recording: Uint8Array<ArrayBuffer> = new Uint8Array(0);
function grow(to: number) {
  const next = new Uint8Array(to);
  next.set(recording);
  for (let i = recording.length; i < to; i++) next[i] = (i * 7) % 251;
  recording = next;
}

// The laptop: a tus upload of unknown length, piece hashes and rewrites.
let server: Uint8Array<ArrayBuffer> = new Uint8Array(0);
let finalLength = 0;
let calls: string[] = [];

async function hex(bytes: Uint8Array<ArrayBuffer>) {
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return Array.from(new Uint8Array(digest), (b) => b.toString(16).padStart(2, "0")).join("");
}

beforeEach(() => {
  vi.useFakeTimers({ shouldAdvanceTime: true });
  recording = new Uint8Array(0);
  server = new Uint8Array(0);
  finalLength = 0;
  calls = [];
  localStorage.clear();
  grow(20 * MB);
  window.showOpenFilePicker = async () => [{
    name: "2026-11-11 20-00-00.mkv",
    getFile: async () => new File([recording.slice()], "2026-11-11 20-00-00.mkv"),
  }];
  vi.stubGlobal("fetch", vi.fn(async (url: string, init: RequestInit = {}) => {
    const method = init.method ?? "GET";
    const headers = (init.headers ?? {}) as Record<string, string>;
    calls.push(`${method} ${url}`);
    if (method === "POST") {
      expect(headers["Upload-Defer-Length"]).toBe("1");
      return new Response(null, { status: 201, headers: { Location: "/api/uploads/up_1", "X-Stream-Id": "st_1" } });
    }
    if (method === "HEAD") return new Response(null, { headers: { "Upload-Offset": String(server.length) } });
    if (method === "GET") {
      const hashes = [];
      for (let at = 0; at < server.length; at += PIECE) hashes.push(await hex(server.slice(at, at + PIECE)));
      return new Response(JSON.stringify({ piece: PIECE, offset: server.length, hashes }));
    }
    const body = new Uint8Array(await new Response(init.body as BodyInit).arrayBuffer());
    if (method === "PUT") {
      const at = Number(new URL(url, "http://x").searchParams.get("at"));
      server.set(body, at);
      return new Response(null, { status: 204 });
    }
    // PATCH
    expect(Number(headers["Upload-Offset"])).toBe(server.length);
    if (headers["Upload-Length"]) finalLength = Number(headers["Upload-Length"]);
    const next = new Uint8Array(server.length + body.length);
    next.set(server);
    next.set(body, server.length);
    server = next;
    return new Response(null, { status: 204, headers: { "Upload-Offset": String(server.length) } });
  }));
});

afterEach(() => {
  vi.useRealTimers();
  vi.restoreAllMocks();
  clearLive();
});

describe("upload while streaming", () => {
  it("sends the recording as it grows, keeps the end back, fixes the rewritten start and finishes", async () => {
    await startLive({ title: "Sunday", game: "bgmi" });
    await vi.waitFor(() => expect(server.length).toBe(2 * PIECE), { timeout: 5000 });     // 20 MB minus the margin
    expect(finalLength).toBe(0);

    grow(30 * MB);
    await vi.advanceTimersByTimeAsync(5000);
    await vi.waitFor(() => expect(server.length).toBe(3 * PIECE), { timeout: 5000 });

    // OBS stops: the file grows a little more and its header is rewritten.
    grow(31 * MB + 12345);
    recording.set(new Uint8Array(65536).fill(9), 0);
    streamEnded();
    for (let i = 0; i < 5 && liveCurrent()?.status !== "done"; i++) await vi.advanceTimersByTimeAsync(5000);
    await vi.waitFor(() => expect(liveCurrent()?.status).toBe("done"), { timeout: 10000 });

    expect(finalLength).toBe(recording.length);
    expect(server.length).toBe(recording.length);
    expect(await hex(server)).toBe(await hex(recording));
    expect(calls.filter((c) => c.startsWith("PUT"))).toEqual(["PUT /api/uploads/up_1/rewrite?at=0"]);   // only the start
    expect(localStorage.getItem("kc_live_upload")).toBeNull();
  });
});
