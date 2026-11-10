import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import Brand from "../pages/Brand";

const kit = { hook_color: "yellow", caption_color: "white", caption_size: "normal", lower_third: false, name: "", upi: "",
              instagram: "", use_intro: false, use_outro: false, description: "", hashtags: [], disclaimer: null };
let puts: Record<string, unknown>[] = [];

beforeEach(() => {
  puts = [];
  vi.stubGlobal("fetch", vi.fn(async (_url: string, init: RequestInit = {}) => {
    const body = init.body ? JSON.parse(String(init.body)) : kit;
    if (init.method === "PUT") puts.push(body);
    return new Response(JSON.stringify({ kit: { ...kit, ...body }, files: { logo: null, intro: null, outro: null },
                                         lengths: { intro: 0, outro: 0 }, strip: body.name ? "/media/brand/strip" : null }));
  }));
});

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

describe("brand kit page", () => {
  it("saves the look, lower-third and post text", async () => {
    render(<MemoryRouter><Brand /></MemoryRouter>);
    fireEvent.change(await screen.findByLabelText("Name"), { target: { value: "Kaatclip" } });
    fireEvent.change(screen.getByLabelText("UPI ID"), { target: { value: "k@okaxis" } });
    fireEvent.click(screen.getByText("Show it"));
    fireEvent.click(screen.getAllByText("White")[0]);          // hook colour
    fireEvent.change(screen.getByLabelText("Hashtags"), { target: { value: "#bgmi, #kaatclip  shorts" } });
    fireEvent.click(screen.getByText("Save brand kit"));
    await waitFor(() => expect(puts).toHaveLength(1));
    expect(puts[0]).toMatchObject({ name: "Kaatclip", upi: "k@okaxis", lower_third: true, hook_color: "white",
                                    hashtags: ["#bgmi", "#kaatclip", "shorts"], disclaimer: null });
    expect(await screen.findByAltText("How the strip looks")).toBeTruthy();
  });
});
