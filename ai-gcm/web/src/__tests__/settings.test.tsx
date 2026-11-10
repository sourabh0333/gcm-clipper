import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import Settings from "../pages/Settings";

const me = { email: "c@example.com", name: "Creator", picture: null, admin: false };
const channel = { id: "yt_1", channel_id: "UC1", title: "Test Gaming", thumbnail: null, status: "ok",
                  connected_at: "2026-11-10T00:00:00Z", settings: { made_for_kids: false, synthetic: false } };
let calls: { url: string; method: string; body: unknown }[] = [];
let channels: typeof channel[] = [];

beforeEach(() => {
  calls = [];
  channels = [channel];
  vi.stubGlobal("confirm", () => true);
  vi.stubGlobal("fetch", vi.fn(async (url: string, init: RequestInit = {}) => {
    const method = init.method ?? "GET";
    const body = init.body ? JSON.parse(String(init.body)) : null;
    calls.push({ url, method, body });
    if (url === "/api/youtube") return new Response(JSON.stringify({ available: true, channels }));
    if (url.endsWith("/settings")) return new Response(JSON.stringify({ ...channel, settings: body }));
    if (url.endsWith("/check")) return new Response(JSON.stringify({ ...channel, status: "expired" }));
    if (method === "DELETE") return new Response(JSON.stringify({ ok: true, revoked: true }));
    return new Response(JSON.stringify({ available: false, linked: false }));
  }));
});

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

const page = (path = "/settings") => render(<MemoryRouter initialEntries={[path]}><Settings me={me} /></MemoryRouter>);

describe("settings: YouTube", () => {
  it("says what came back from Google and offers to connect", async () => {
    channels = [];
    page("/settings?youtube=scopes");
    expect(await screen.findByText("Connect YouTube")).toBeTruthy();
    expect(screen.getByRole("status").textContent).toContain("all three permissions");
    expect(screen.getByText(/can't edit or delete your videos/)).toBeTruthy();
  });

  it("saves the channel's answers, shows an expired connection and disconnects", async () => {
    page();
    expect(await screen.findByText("Test Gaming")).toBeTruthy();
    fireEvent.click(screen.getByLabelText(/realistic altered or AI-made/));
    await waitFor(() => expect(calls.some((c) => c.method === "PUT")).toBe(true));
    expect(calls.find((c) => c.method === "PUT")!.body).toEqual({ made_for_kids: false, synthetic: true });

    fireEvent.click(screen.getByText("Check"));
    expect(await screen.findByText("Reconnect")).toBeTruthy();
    expect(screen.getByText(/Connection expired/)).toBeTruthy();

    fireEvent.click(screen.getByText("Disconnect"));
    await waitFor(() => expect(screen.queryByText("Test Gaming")).toBeNull());
    expect(calls.some((c) => c.method === "DELETE" && c.url === "/api/youtube/yt_1")).toBe(true);
    expect(screen.getByText("Connect YouTube")).toBeTruthy();
  });
});
