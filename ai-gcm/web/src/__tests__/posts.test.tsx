import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import PostPage, { nextEvening } from "../pages/PostPage";
import Posts from "../pages/Posts";

const channel = { id: "yt_1", channel_id: "UC1", title: "Test Gaming", thumbnail: null, status: "ok",
                  connected_at: "2026-11-10T00:00:00Z", settings: { made_for_kids: false, synthetic: false } };
const base = { id: "po_1", status: "draft", kind: "short", clip_id: 1, clip_title: "c", stream_id: "st_1", render_id: "rn_1",
               video: "/media/renders/rn_1", cover: null, channel: { id: "yt_1", title: "Test Gaming", thumbnail: null, status: "ok" },
               title: "1v4 clutch", description: "Full stream: https://youtu.be/abcdefghijk", tags: ["bgmi"], mode: "schedule",
               publish_at: "2026-11-20T13:30:00Z", approved_at: null, video_id: null, error: null,
               updated_at: "2026-11-10T10:00:00.000001Z", created_at: "2026-11-10T10:00:00Z" };
let calls: { url: string; method: string; body: Record<string, unknown> | null }[] = [];
let posts: Record<string, unknown>[] = [];

beforeEach(() => {
  calls = [];
  posts = [base, { ...base, id: "po_2", title: "Second", updated_at: "2026-11-10T10:05:00Z" },
           { ...base, id: "po_3", title: "Old one", status: "posted", video_id: "abc" }];
  vi.stubGlobal("fetch", vi.fn(async (url: string, init: RequestInit = {}) => {
    const method = init.method ?? "GET";
    const body = init.body ? JSON.parse(String(init.body)) : null;
    calls.push({ url, method, body });
    if (url === "/api/youtube") return new Response(JSON.stringify({ available: true, channels: [channel] }));
    if (url === "/api/posts") return new Response(JSON.stringify(posts));
    if (url === "/api/posts/approve") {
      return new Response(JSON.stringify({ approved: [{ ...base, status: "approved" }],
                                           problems: [{ id: "po_2", error: "Add a title." }] }));
    }
    if (url.endsWith("/approve")) return new Response(JSON.stringify({ ...base, status: "approved", approved_at: "2026-11-10T10:01:00Z" }));
    if (method === "PUT") return new Response(JSON.stringify({ ...base, ...body, updated_at: "2026-11-10T10:00:30Z" }));
    return new Response(JSON.stringify(base));
  }));
});

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

describe("post this?", () => {
  it("saves, shows exactly what will be approved, and approves that version", async () => {
    render(<MemoryRouter initialEntries={["/posts/po_1"]}><Routes><Route path="/posts/:id" element={<PostPage />} /></Routes></MemoryRouter>);
    fireEvent.change(await screen.findByLabelText("Title"), { target: { value: "1v4 clutch in Pochinki" } });
    expect(screen.getByText("22/100")).toBeTruthy();
    fireEvent.click(screen.getByText("Review and approve"));
    const dialog = await screen.findByRole("dialog");
    expect(dialog.textContent).toContain("1v4 clutch in Pochinki");
    expect(dialog.textContent).toContain("Test Gaming");
    const put = calls.find((c) => c.method === "PUT")!;
    expect(put.body).toMatchObject({ title: "1v4 clutch in Pochinki", channel_id: "yt_1", mode: "schedule", tags: ["bgmi"] });
    expect(new Date(put.body!.publish_at as string).toISOString()).toBe("2026-11-20T13:30:00.000Z");

    fireEvent.click(screen.getByText("Approve"));
    await waitFor(() => expect(screen.getByText("approved")).toBeTruthy());
    expect(calls.find((c) => c.url === "/api/posts/po_1/approve")!.body).toEqual({ seen: "2026-11-10T10:00:30Z" });
  });

  it("suggests the next evening at least an hour away", () => {
    const at = new Date(nextEvening(new Date(2026, 10, 10, 18, 30)));
    expect([at.getDate(), at.getHours()]).toEqual([11, 19]);
    expect(new Date(nextEvening(new Date(2026, 10, 10, 9, 0))).getDate()).toBe(10);
  });
});

describe("posts list", () => {
  it("approves an explicit list after showing each one, and keeps the ones with problems", async () => {
    render(<MemoryRouter initialEntries={["/posts?view=list"]}><Posts /></MemoryRouter>);
    expect(await screen.findByText("Drafts (2)")).toBeTruthy();
    expect(screen.getByText("Posted (1)")).toBeTruthy();
    fireEvent.click(screen.getByLabelText("Pick 1v4 clutch"));
    fireEvent.click(screen.getByLabelText("Pick Second"));
    fireEvent.click(screen.getByText("Approve 2 posts"));
    const dialog = await screen.findByRole("dialog");
    expect(dialog.querySelectorAll("li")).toHaveLength(2);
    fireEvent.click(screen.getByText("Approve 2"));
    await waitFor(() => expect(screen.getByText("Second: Add a title.")).toBeTruthy());
    expect(calls.find((c) => c.url === "/api/posts/approve")!.body).toEqual({ posts: [
      { id: "po_1", seen: "2026-11-10T10:00:00.000001Z" }, { id: "po_2", seen: "2026-11-10T10:05:00Z" }] });
  });
});
