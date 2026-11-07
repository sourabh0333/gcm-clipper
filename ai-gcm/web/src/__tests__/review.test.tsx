import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import Review from "../pages/Review";

function clip(id: number, decision: string | null = null) {
  return { id, stream_id: "st_1", rank: id, start_s: 0, end_s: 30, length_s: 30, type: "fight", score: 1,
           title: `Clip title ${id}`, why: `2 kills at 0:0${id}:00`, titles: [], hashtags: [], description: null,
           labels: {}, flags: [], decision, reason: null, video: `/media/clips/${id}`, safe_video: null };
}

let posts: { url: string; body: { verdict: string | null; reason: string | null } }[] = [];

beforeEach(() => {
  posts = [];
  vi.stubGlobal("fetch", vi.fn(async (url: string, init: RequestInit = {}) => {
    if (url.endsWith("/clips")) return new Response(JSON.stringify([clip(1), clip(2)]));
    const body = JSON.parse(String(init.body));
    posts.push({ url, body });
    const id = Number(url.split("/")[3]);
    return new Response(JSON.stringify({ ...clip(id), decision: body.verdict, reason: body.reason }));
  }));
});

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

function show() {
  render(
    <MemoryRouter initialEntries={["/streams/st_1/review"]}>
      <Routes><Route path="/streams/:id/review" element={<Review />} /></Routes>
    </MemoryRouter>,
  );
}

describe("review", () => {
  it("keeps, rejects with a reason, undoes, and finishes", async () => {
    show();
    expect(await screen.findByText("Clip title 1")).toBeTruthy();
    expect(screen.getByText(/2 kills at 0:01:00/)).toBeTruthy();

    fireEvent.click(screen.getByText("✓ Keep"));
    expect(await screen.findByText("Clip title 2")).toBeTruthy();
    expect(posts[0]).toEqual({ url: "/api/clips/1/decision", body: { verdict: "keep", reason: null } });

    fireEvent.click(screen.getByText("✗ Reject"));
    expect(await screen.findByText("All done")).toBeTruthy();
    expect(screen.getByText("You kept 1 of 2 clips.")).toBeTruthy();

    fireEvent.click(screen.getByText("Undo last"));
    expect(await screen.findByText("Clip title 2")).toBeTruthy();
    await waitFor(() => expect(posts.at(-1)?.body.verdict).toBeNull());

    fireEvent.click(screen.getByText("✗ Reject"));
    fireEvent.click(await screen.findByText("Bad cut"));
    await waitFor(() => expect(posts.at(-1)?.body).toEqual({ verdict: "reject", reason: "bad_cut" }));
  });

  it("works from the keyboard", async () => {
    show();
    await screen.findByText("Clip title 1");
    fireEvent.keyDown(window, { key: "ArrowLeft" });
    expect(await screen.findByText("Clip title 2")).toBeTruthy();
    expect(posts[0].body.verdict).toBe("reject");
  });
});
