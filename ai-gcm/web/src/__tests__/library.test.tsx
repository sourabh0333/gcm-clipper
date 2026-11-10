import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import Library from "../pages/Library";

function clip(id: number) {
  return { id, stream_id: "st_1", rank: id, start_s: 0, end_s: 30, length_s: 30, type: "fight", score: 1,
           title: `Clip ${id}`, why: null, titles: [], hashtags: [], description: null, labels: {}, flags: [],
           decision: "keep", reason: null, video: `/media/clips/${id}`, safe_video: null, stream_title: "Stream",
           poster: id % 2 ? `/media/posters/${id}` : null, edited: id === 1, exported: false };
}

let urls: string[] = [];
const clipLinks = () => screen.getAllByRole("link").filter((a) => a.getAttribute("href")?.startsWith("/clips/"));

beforeEach(() => {
  urls = [];
  vi.stubGlobal("IntersectionObserver", class { observe() {} disconnect() {} });
  vi.stubGlobal("fetch", vi.fn(async (url: string) => {
    urls.push(url);
    const offset = Number(new URL(url, "http://x").searchParams.get("offset"));
    const q = new URL(url, "http://x").searchParams.get("q");
    const all = q ? [clip(3)] : Array.from({ length: 45 }, (_, i) => clip(i + 1));
    return new Response(JSON.stringify({
      items: all.slice(offset, offset + 40), total: all.length, offset, limit: 40,
      facets: { streams: [{ id: "st_1", title: "Stream", count: 45 }], types: [{ type: "fight", count: 45 }] },
    }));
  }));
});

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

describe("library", () => {
  it("shows kept clips by default, pages, filters and searches", async () => {
    render(
      <MemoryRouter initialEntries={["/library"]}>
        <Routes><Route path="/library" element={<Library />} /></Routes>
      </MemoryRouter>,
    );
    expect(await screen.findByText("45 clips")).toBeTruthy();
    expect(urls[0]).toContain("decision=keep");
    expect(clipLinks()).toHaveLength(40);
    expect(clipLinks()[0].getAttribute("href")).toBe("/clips/1/studio");

    fireEvent.click(screen.getByText("Load more"));
    await waitFor(() => expect(clipLinks()).toHaveLength(45));
    expect(urls.at(-1)).toContain("offset=40");

    fireEvent.click(screen.getByText("Edited"));
    await waitFor(() => expect(urls.at(-1)).toContain("edited=1"));

    fireEvent.change(screen.getByLabelText("Search clips"), { target: { value: "zone" } });
    await waitFor(() => expect(screen.getByText("1 clip")).toBeTruthy(), { timeout: 2000 });
    expect(urls.at(-1)).toContain("q=zone");
  }, 15000);   // 45 tiles and a typing pause: slow when every test file runs at once
});
