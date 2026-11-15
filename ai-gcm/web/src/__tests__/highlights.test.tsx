import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router";
import { afterEach, describe, expect, it, vi } from "vitest";
import Highlights, { type StreamHighlights } from "../studio/Highlights";

const map = {
  duration: 3000, best: 2, session: [1, 2],
  parts: [{ start: 0, end: 300, kind: "not_bgmi", why: "chat" }, { start: 300, end: 1200, kind: "match", match: 1 },
          { start: 1200, end: 1400, kind: "between" }, { start: 1400, end: 3000, kind: "match", match: 2 }],
  matches: [{ n: 1, start: 300, end: 1200, ended: "death", placement: 6, kills: 7, score: 30, fights: 5, map: "erangel", mode: "classic" },
            { n: 2, start: 1400, end: 3000, ended: "dinner", placement: 1, kills: 12, score: 60, fights: 9, map: null, mode: null }],
} as StreamHighlights["map"];

const done = {
  id: "r1", status: "done", error: null, stream_id: "s1", matches: [2], session: false, auto: true, created_at: null,
  length_s: 540, kept: 0.31, kills: 12, label: "second", titles: ["CHICKEN DINNER + 12 FINISHES | BGMI"], description: "",
  pieces: [{ i: 0, kind: "teaser", start: 10, end: 30, length: 20 }, { i: 1, kind: "fight", start: 40, end: 90, length: 50, kills: 3, punch: 1 },
           { i: 2, kind: "card", text: "A FEW MINUTES LATER" }, { i: 3, kind: "ending", start: 2990, end: 3000, length: 10 }],
  video: "/media/highlights/r1/video", play: "/media/highlights/r1/video?view=1", thumbnails: ["/media/highlights/r1/thumb_1"],
  shorts: [{ clip_id: 5, title: "CHICKEN DINNER 🏆", role: "teaser", length_s: 30, poster: "/media/posters/5", decision: null }],
  posts: [],
} as StreamHighlights["highlights"][number];

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

function serve(state: StreamHighlights, calls: { url: string; body: unknown }[]) {
  vi.stubGlobal("fetch", vi.fn(async (url: string, init: RequestInit = {}) => {
    calls.push({ url, body: init.body ? JSON.parse(String(init.body)) : null });
    if (url.endsWith("/plan-posts")) return new Response(JSON.stringify({ posts: [{ id: "p1", publish_at: null }], waiting: [5] }));
    if (init.method === "POST") return new Response(JSON.stringify({ status: "queued" }));
    return new Response(JSON.stringify(state));
  }));
}

describe("highlights on the stream page", () => {
  it("shows the map and makes a highlight of a match or the session", async () => {
    const calls: { url: string; body: unknown }[] = [];
    serve({ map, map_status: "done", has_source: true, highlights: [] }, calls);
    render(<MemoryRouter><Highlights streamId="s1" /></MemoryRouter>);
    expect(await screen.findByText("Match 2")).toBeTruthy();
    expect(screen.getByText(/12 kills · 🏆 Chicken Dinner/)).toBeTruthy();
    expect(screen.getByText(/7 kills · #6/)).toBeTruthy();
    expect(screen.getByLabelText("Stream map").children.length).toBe(4);
    fireEvent.click(screen.getAllByText("Make highlight")[1]);
    await waitFor(() => expect(calls.some((c) => c.url === "/api/streams/s1/highlights" && JSON.stringify(c.body) === '{"matches":[2]}')).toBe(true));
    fireEvent.click(screen.getByText(/Make a session video/));
    await waitFor(() => expect(calls.some((c) => JSON.stringify(c.body) === '{"session":true}')).toBe(true));
    fireEvent.click(screen.getByText(/Make a comedy cut/));
    await waitFor(() => expect(calls.some((c) => JSON.stringify(c.body) === '{"style":"comedy"}')).toBe(true));
  });

  it("shows a comedy cut's funny bits and makes it again without one", async () => {
    const calls: { url: string; body: unknown }[] = [];
    const comedy = { ...done, id: "r2", style: "comedy", kills: 0, titles: ["GTX & LOLO KALESH 😂 | FUNNY BGMI HIGHLIGHT"],
      pieces: [{ i: 0, kind: "intro", start: 5, end: 9, length: 4 }, { i: 1, kind: "unit", start: 40, end: 60, length: 20, title: "Kara do meri shaadi", funny: 9, punch: 1 },
               { i: 2, kind: "unit", start: 90, end: 100, length: 10, funny: 8 }],
      shorts: [{ clip_id: 6, title: "Kara do meri shaadi 😂", role: "funny", length_s: 25, poster: "/media/posters/6", decision: null }],
    } as StreamHighlights["highlights"][number];
    serve({ map, map_status: "done", has_source: true, highlights: [comedy] }, calls);
    render(<MemoryRouter><Highlights streamId="s1" /></MemoryRouter>);
    expect(await screen.findByText((_, el) => el?.className === "title" && el.textContent === "Comedy cut · 9 min")).toBeTruthy();
    expect(screen.getByText(/2 funny bits in stream order/)).toBeTruthy();
    expect(screen.getByText(/Funny bit · Kara do meri shaadi 😂/)).toBeTruthy();
    fireEvent.click(screen.getByText(/What's in it/));
    fireEvent.click(screen.getAllByRole("checkbox")[2]);
    fireEvent.click(screen.getByText("Make again"));
    await waitFor(() => expect(calls.some((c) => JSON.stringify(c.body) === '{"style":"comedy","drop":[2]}')).toBe(true));
  });

  it("plays a finished highlight, leaves out an unticked part and plans the posts", async () => {
    const calls: { url: string; body: unknown }[] = [];
    serve({ map, map_status: "done", has_source: true, highlights: [done] }, calls);
    render(<MemoryRouter><Highlights streamId="s1" /></MemoryRouter>);
    expect(await screen.findByText(/second channel/)).toBeTruthy();
    expect(screen.getByText("CHICKEN DINNER + 12 FINISHES | BGMI")).toBeTruthy();
    expect(screen.getByText(/Teaser · CHICKEN DINNER/).closest("a")?.getAttribute("href")).toBe("/clips/5/studio");
    fireEvent.click(screen.getByText(/What's in it/));
    fireEvent.click(screen.getAllByRole("checkbox")[1]);
    fireEvent.click(screen.getByText("Make again"));
    await waitFor(() => expect(calls.some((c) => JSON.stringify(c.body) === '{"matches":[2],"session":false,"drop":[1]}')).toBe(true));
    fireEvent.click(screen.getByText("Plan the posts"));
    expect(await screen.findByText(/1 draft in Posts, not approved yet. 1 Short is still being made/)).toBeTruthy();
  });

  it("offers to find the matches when there is no map", async () => {
    const calls: { url: string; body: unknown }[] = [];
    serve({ map: null, map_status: null, has_source: true, highlights: [] }, calls);
    render(<MemoryRouter><Highlights streamId="s1" /></MemoryRouter>);
    fireEvent.click(await screen.findByText("Find the matches"));
    await waitFor(() => expect(calls.some((c) => c.url === "/api/streams/s1/map")).toBe(true));
  });
});
