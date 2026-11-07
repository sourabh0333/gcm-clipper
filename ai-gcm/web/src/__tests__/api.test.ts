import { afterEach, describe, expect, it, vi } from "vitest";
import { api, ApiError } from "../api";
import { uploadMetadata } from "../uploader";

afterEach(() => vi.restoreAllMocks());

describe("api", () => {
  it("adds the app header to changes but not to reads, and surfaces the server's message", async () => {
    const calls: RequestInit[] = [];
    vi.stubGlobal("fetch", vi.fn(async (_url: string, init: RequestInit) => {
      calls.push(init);
      return new Response(JSON.stringify(init.method === "GET" ? { ok: 1 } : { detail: "Not invited." }), {
        status: init.method === "GET" ? 200 : 403,
      });
    }));
    await api("/api/me");
    await expect(api("/auth/dev-login", { body: { email: "x" } })).rejects.toEqual(new ApiError(403, "Not invited."));
    expect((calls[0].headers as Record<string, string>)["X-Kaatclip"]).toBeUndefined();
    expect((calls[1].headers as Record<string, string>)["X-Kaatclip"]).toBe("1");
    expect(calls[1].method).toBe("POST");
  });
});

describe("upload metadata", () => {
  it("carries the title, date and live session the server reads", () => {
    const file = new File(["x"], "obs 2026-11-05.mkv");
    expect(uploadMetadata(file, "Rank push", "2026-11-05", "live_1")).toEqual({
      filename: "obs 2026-11-05.mkv", title: "Rank push", game: "bgmi", recorded_on: "2026-11-05", live_session: "live_1",
    });
    expect(uploadMetadata(file, "", "", "")).toEqual({ filename: "obs 2026-11-05.mkv", title: "obs 2026-11-05.mkv", game: "bgmi" });
  });
});
