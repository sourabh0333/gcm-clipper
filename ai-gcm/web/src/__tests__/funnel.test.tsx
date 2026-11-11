import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { Post } from "../api";
import { FinishInStudio } from "../pages/PostPage";

const studio = { url: "https://studio.youtube.com/video/vid12345678/edit", comment: "Full stream 👉 https://youtu.be/abcdefghijk",
                 related: "Sunday rank push", done: false };
const post = { id: "po_1", video_id: "vid12345678", studio } as unknown as Post;

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

describe("finish in Studio", () => {
  it("shows the related stream and the comment to copy, and ticks off", async () => {
    const writeText = vi.fn(async () => {});
    vi.stubGlobal("navigator", { ...navigator, clipboard: { writeText } });
    const calls: unknown[] = [];
    vi.stubGlobal("fetch", vi.fn(async (_url: string, init: RequestInit = {}) => {
      calls.push(JSON.parse(String(init.body)));
      return new Response(JSON.stringify({ ...post, studio: { ...studio, done: true } }));
    }));
    const onChange = vi.fn();
    render(<FinishInStudio post={post} onChange={onChange} />);
    expect(screen.getByText("Sunday rank push")).toBeTruthy();
    expect(screen.getByText("Open in Studio").getAttribute("href")).toBe(studio.url);
    fireEvent.click(screen.getByText("Copy"));
    await waitFor(() => expect(writeText).toHaveBeenCalledWith(studio.comment));
    fireEvent.click(screen.getByText("Done"));
    await waitFor(() => expect(onChange).toHaveBeenCalled());
    expect(calls).toEqual([{ done: true }]);
  });
});
