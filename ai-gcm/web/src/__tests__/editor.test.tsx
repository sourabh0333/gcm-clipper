import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import Editor from "../pages/Editor";

const data = {
  v: 1, segments: [{ start: 100, end: 130, speed: 1 }],
  layout: { template: "blur", background: "blur", panels: [{ role: "game", src: [0, 0, 1, 1], dst: [0, 656, 1080, 608] }] },
  zooms: [], hook: { text: "", color: "yellow", on: false }, captions: { on: false }, cover_t: null, sponsor_safe: false,
};
const studio = {
  clip: { id: 7, title: "3 FINISHES", rank: 1 },
  window: { status: "ready", start: 40, end: 190, duration: 150, width: 1920, height: 1080, has_audio: true,
            preview: "/media/studio/7/preview.mp4", wave: "/media/studio/7/wave.json",
            strip: { url: "/media/studio/7/strip.jpg", every_s: 2, cols: 10, rows: 8, frames: 75, tile_w: 96, tile_h: 54 } },
  edit: { version: 0, data, length_s: 30 },
  editor: { events: [{ t: 95, kind: "self_kill" }, { t: 150, kind: "self_kill" }], anchor: 110,
            presets: { moment: [95, 140], full_fight: [80, 160], suggested: "full_fight" } },
  exports: [],
};

let calls: { url: string; method: string; body?: { base_version?: number; data?: typeof data; version?: number } }[] = [];

beforeEach(() => {
  calls = [];
  vi.stubGlobal("fetch", vi.fn(async (url: string, init: RequestInit = {}) => {
    const method = init.method ?? "GET";
    const body = init.body ? JSON.parse(String(init.body)) : undefined;
    calls.push({ url, method, body });
    if (url.endsWith("/wave.json")) return new Response(JSON.stringify({ step_s: 0.1, peaks: [10, 50, 90] }));
    if (url.endsWith("/edit")) return new Response(JSON.stringify({ version: 1, data: body.data, length_s: 45 }));
    if (url.endsWith("/export")) return new Response(JSON.stringify({ id: "rn_1", kind: "export", status: "queued", error: null,
      version: 1, sponsor_safe: false, created_at: null, finished_at: null, video: null }));
    return new Response(JSON.stringify(studio));
  }));
});

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

describe("editor", () => {
  it("applies a length preset with zooms, undoes it, and saves before exporting", async () => {
    render(
      <MemoryRouter initialEntries={["/clips/7/edit"]}>
        <Routes><Route path="/clips/:id/edit" element={<Editor />} /></Routes>
      </MemoryRouter>,
    );
    expect(await screen.findByText(/Full fight 80s ★/)).toBeTruthy();
    expect(screen.getByText("Saved")).toBeTruthy();
    expect(document.querySelectorAll(".tlevent")).toHaveLength(2);

    fireEvent.click(screen.getByText(/Moment 45s/));
    expect(await screen.findByText("45.0 s")).toBeTruthy();
    fireEvent.click(screen.getByLabelText("Undo"));
    expect(await screen.findByText("30.0 s")).toBeTruthy();
    fireEvent.click(screen.getByLabelText("Redo"));
    expect(await screen.findByText("45.0 s")).toBeTruthy();

    fireEvent.click(screen.getByText("Export (saves first)"));
    await waitFor(() => expect(calls.some((c) => c.url.endsWith("/export"))).toBe(true));
    const saved = calls.find((c) => c.url.endsWith("/edit"))!;
    expect(saved.method).toBe("PUT");
    expect(saved.body!.base_version).toBe(0);
    expect(saved.body!.data!.segments).toEqual([{ start: 95, end: 140, speed: 1 }]);
    expect(calls.find((c) => c.url.endsWith("/export"))!.body).toEqual({ version: 1 });
    expect(await screen.findByText(/Rendering on the laptop/)).toBeTruthy();
  });
});
