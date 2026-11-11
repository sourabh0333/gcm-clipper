import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { addDays, mondayOf, WeekView, ymd } from "../pages/Calendar";

const start = mondayOf(ymd(new Date()));
const day3 = addDays(start, 2);
function at(day: string, hour: number) {
  const [y, m, d] = day.split("-").map(Number);
  return new Date(y, m - 1, d, hour, 0).toISOString();
}
const post = (id: string, day: string, status = "draft") => ({
  id, status, title: `Clip ${id}`, day, at: at(day, 19), publish_at: at(day, 19), mode: "schedule",
  channel: { id: "yt_1", title: "Test Gaming", thumbnail: null, status: "ok" }, updated_at: `u-${id}`, tags: [],
});
let calls: { url: string; method: string; body: Record<string, unknown> | null }[] = [];
let posts: ReturnType<typeof post>[] = [];

beforeEach(() => {
  calls = [];
  posts = [post("a", day3), post("b", addDays(start, 4), "scheduled")];
  vi.stubGlobal("fetch", vi.fn(async (url: string, init: RequestInit = {}) => {
    const method = init.method ?? "GET";
    const body = init.body ? JSON.parse(String(init.body)) : null;
    calls.push({ url, method, body });
    if (url.startsWith("/api/calendar/fill")) {
      posts = [...posts, post("c", addDays(start, 5))];
      return new Response(JSON.stringify({ placed: [post("c", addDays(start, 5))], free_left: 3, exports_left: 0, drafts_left: 0 }));
    }
    if (url.startsWith("/api/calendar")) {
      return new Response(JSON.stringify({ start, days: 7, posts, unscheduled: [],
        gauge: { channel: "Test Gaming", shorts: 9, uploads: 30, planned: 2, share: 0.3, warn: true, limit: 0.2, days: 28, ahead: 7, as_of: null } }));
    }
    if (url === "/api/posts/approve") return new Response(JSON.stringify({ approved: [post("a", day3, "approved")], problems: [] }));
    return new Response(JSON.stringify({ ...posts[0], ...body }));
  }));
});

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

describe("week view", () => {
  it("shows the week, the gauge, moves a draft and fills the free evenings", async () => {
    render(<MemoryRouter><WeekView start={start} setStart={() => {}} /></MemoryRouter>);
    expect(await screen.findByText("Clip a")).toBeTruthy();
    expect(screen.getByText("Shorts share: 30%")).toBeTruthy();
    expect(screen.getAllByText("Move")).toHaveLength(1);            // only the draft can move
    fireEvent.click(screen.getByText("Move"));
    fireEvent.click(screen.getAllByRole("button", { name: "Move here" })[0]);
    await waitFor(() => expect(calls.some((c) => c.method === "PUT")).toBe(true));
    const put = calls.find((c) => c.method === "PUT")!;
    expect(put.url).toBe("/api/posts/a/time");
    const moved = new Date(put.body!.publish_at as string);
    expect(ymd(moved) !== day3 && ymd(moved) >= ymd(new Date()) && moved.getHours() === 19).toBe(true);

    fireEvent.click(screen.getByText("Fill empty evenings"));
    expect(await screen.findByText(/Planned 1 draft at 7 pm/)).toBeTruthy();
    expect(calls.find((c) => c.url === "/api/calendar/fill")!.body).toMatchObject({ days: 7 });
  });

  it("approves the week's drafts as one listed batch", async () => {
    render(<MemoryRouter><WeekView start={start} setStart={() => {}} /></MemoryRouter>);
    fireEvent.click(await screen.findByText("Approve the week (1)"));
    const dialog = await screen.findByRole("dialog");
    expect(dialog.querySelectorAll("li")).toHaveLength(1);
    fireEvent.click(screen.getByText("Approve 1"));
    await waitFor(() => expect(screen.getByText("1 approved.")).toBeTruthy());
    expect(calls.find((c) => c.url === "/api/posts/approve")!.body).toEqual({ posts: [{ id: "a", seen: "u-a" }] });
  });

  it("finds Mondays", () => {
    expect(mondayOf("2026-11-11")).toBe("2026-11-09");
    expect(mondayOf("2026-11-09")).toBe("2026-11-09");
    expect(mondayOf("2026-11-15")).toBe("2026-11-09");
    expect(addDays("2026-11-30", 1)).toBe("2026-12-01");
  });
});
