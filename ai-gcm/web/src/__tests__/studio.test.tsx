import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import StudioPage from "../pages/StudioPage";

const clip = { id: 7, stream_id: "st_1", rank: 1, start_s: 100, end_s: 130, length_s: 30, type: "fight", score: 1,
               title: "3 FINISHES", why: "3 kills at 0:01:50", titles: [], hashtags: [], description: null,
               labels: {}, flags: [], decision: "keep", reason: null, video: "/media/clips/7", safe_video: null };
const edit = {
  version: 0, length_s: 30,
  data: { v: 1, segments: [{ start: 100, end: 130, speed: 1 }],
          layout: { template: "blur", background: "blur", panels: [{ role: "game", src: [0, 0, 1, 1], dst: [0, 656, 1080, 608] }] },
          zooms: [{ t: 110, dur: 1.2, scale: 1.25 }], hook: { text: "3 FINISHES", color: "yellow", on: false },
          captions: { on: false }, cover_t: null, sponsor_safe: false },
};
const ready = { status: "ready", start: 40, end: 190, duration: 150, width: 1920, height: 1080, has_audio: true,
                preview: "/media/studio/7/preview.mp4", wave: "/media/studio/7/wave.json",
                strip: { url: "/media/studio/7/strip.jpg", every_s: 2, cols: 10, rows: 8, frames: 75, tile_w: 96, tile_h: 54 } };

let calls: { url: string; method: string; body?: unknown }[] = [];
let state: { window: object; exports: object[] };

beforeEach(() => {
  calls = [];
  state = { window: { status: "none" }, exports: [] };
  vi.stubGlobal("fetch", vi.fn(async (url: string, init: RequestInit = {}) => {
    const method = init.method ?? "GET";
    calls.push({ url, method, body: init.body ? JSON.parse(String(init.body)) : undefined });
    if (url.endsWith("/prepare")) {
      state.window = ready;
      return new Response(JSON.stringify(ready));
    }
    if (url.endsWith("/export")) {
      const job = { id: "rn_1", kind: "export", status: "done", error: null, version: 0, sponsor_safe: false,
                    created_at: null, finished_at: null, video: "/media/renders/rn_1" };
      state.exports = [job];
      return new Response(JSON.stringify(job));
    }
    return new Response(JSON.stringify({ clip, window: state.window, edit, exports: state.exports }));
  }));
});

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

describe("studio page", () => {
  it("asks for the footage once, then exports the automatic edit", async () => {
    render(
      <MemoryRouter initialEntries={["/clips/7/studio"]}>
        <Routes><Route path="/clips/:id/studio" element={<StudioPage />} /></Routes>
      </MemoryRouter>,
    );
    expect(await screen.findByText("3 FINISHES")).toBeTruthy();
    expect(await screen.findByText(/Automatic edit · 30.0 s · 1 part · layout blur · 1 zoom on kills/)).toBeTruthy();
    expect(calls.filter((c) => c.url.endsWith("/prepare"))).toHaveLength(1);

    fireEvent.click(screen.getByText("Export"));
    expect(await screen.findByText("Download")).toBeTruthy();
    await waitFor(() => expect(calls.find((c) => c.url.endsWith("/export"))?.body).toEqual({ sponsor_safe: false }));
    expect(screen.getByText("Download").getAttribute("href")).toBe("/media/renders/rn_1?download=1");
  });

  it("explains when the recording is gone", async () => {
    state.window = { status: "missing" };
    render(
      <MemoryRouter initialEntries={["/clips/7/studio"]}>
        <Routes><Route path="/clips/:id/studio" element={<StudioPage />} /></Routes>
      </MemoryRouter>,
    );
    expect(await screen.findByText(/no longer on the laptop/)).toBeTruthy();
    expect(screen.queryByText("Export")).toBeNull();
  });
});
