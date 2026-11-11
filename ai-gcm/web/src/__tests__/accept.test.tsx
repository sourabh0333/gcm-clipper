import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import Accept from "../pages/Accept";

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

describe("before you start", () => {
  it("needs the tick, then accepts this version of the policy", async () => {
    const bodies: unknown[] = [];
    vi.stubGlobal("fetch", vi.fn(async (_url: string, init: RequestInit = {}) => {
      bodies.push(JSON.parse(String(init.body)));
      return new Response(JSON.stringify({ accepted: true }));
    }));
    const onAccepted = vi.fn();
    const me = { email: "c@example.com", name: "Creator", picture: null, admin: false, accepted: false, terms_version: "2026-11-11" };
    render(<Accept me={me} onAccepted={onAccepted} />);
    expect(screen.getByText("privacy policy").getAttribute("href")).toBe("/privacy");
    const go = screen.getByText("Continue") as HTMLButtonElement;
    expect(go.disabled).toBe(true);
    fireEvent.click(screen.getByLabelText(/accept the privacy policy and terms/));
    fireEvent.click(go);
    await waitFor(() => expect(onAccepted).toHaveBeenCalled());
    expect(bodies).toEqual([{ version: "2026-11-11" }]);
  });
});
