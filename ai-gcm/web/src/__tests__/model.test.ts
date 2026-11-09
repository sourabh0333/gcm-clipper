import { describe, expect, it } from "vitest";
import type { EditData } from "../api";
import {
  addPart, applyPreset, outputLength, panelSource, problems, removePart, setSpeed, split, toOutput, toSource, trim,
  zoomAt,
} from "../studio/model";

const segs = [{ start: 10, end: 20, speed: 1 }, { start: 30, end: 40, speed: 2 }];
const blur: EditData["layout"] = { template: "blur", background: "blur",
  panels: [{ role: "game", src: [0, 0, 1, 1], dst: [0, 656, 1080, 608] }] };
const edit: EditData = { v: 1, segments: segs, layout: blur, zooms: [{ t: 15, dur: 1.2, scale: 1.25 }],
  hook: { text: "", color: "yellow", on: false }, captions: { on: false }, cover_t: null, sponsor_safe: false };

describe("time mapping (same numbers as the server's edit.py)", () => {
  it("maps source to output and back through cuts and speed", () => {
    expect(outputLength(segs)).toBe(15);
    expect(toOutput(segs, 15)).toBe(5);
    expect(toOutput(segs, 25)).toBeNull();
    expect(toOutput(segs, 34)).toBe(12);
    expect(toSource(segs, 12)).toEqual({ t: 34, index: 1 });
    expect(toSource(segs, 99)).toEqual({ t: 40, index: 1 });
  });
});

describe("part operations", () => {
  it("splits, trims within neighbours, deletes, speeds up and brings footage back", () => {
    expect(split(segs, 15)).toEqual([{ start: 10, end: 15, speed: 1 }, { start: 15, end: 20, speed: 1 }, segs[1]]);
    expect(split(segs, 10.1)).toBe(segs);                 // too close to the edge
    expect(split(segs, 25)).toBe(segs);                   // nothing there
    expect(trim(segs, 0, "end", 35, 0, 100)[0].end).toBe(30);       // stops at the next part
    expect(trim(segs, 1, "start", 5, 0, 100)[1].start).toBe(20);    // stops at the previous part
    expect(trim(segs, 0, "start", -9, 2, 100)[0].start).toBe(2);    // stops at the footage's start
    expect(trim(segs, 0, "start", 25, 0, 100)[0].start).toBe(19.7); // keeps the part 0.3 s long
    expect(removePart(segs, 0)).toEqual([segs[1]]);
    expect(removePart([segs[0]], 0)).toEqual([segs[0]]);   // the last part stays
    expect(setSpeed(segs, 0, 2)[0].speed).toBe(2);
    expect(addPart(segs, 22, 0, 100)).toEqual([segs[0], { start: 22, end: 27, speed: 1 }, segs[1]]);
    expect(addPart(segs, 28, 0, 100)[1]).toEqual({ start: 28, end: 30, speed: 1 });
    expect(addPart(segs, 15, 0, 100)).toBe(segs);
  });

  it("applies a length preset with zooms on its kills", () => {
    const events = [{ t: 50, kind: "self_kill" }, { t: 51, kind: "self_kill" }, { t: 70, kind: "self_kill" },
                    { t: 60, kind: "accolade" }, { t: 200, kind: "self_kill" }];
    const cut = applyPreset(edit, 45, 90, events);
    expect(cut.segments).toEqual([{ start: 45, end: 90, speed: 1 }]);
    expect(cut.zooms.map((z) => z.t)).toEqual([50, 70]);
    const native = applyPreset({ ...edit, layout: { ...blur, template: "native" }, zooms: [] }, 45, 90, events);
    expect(native.zooms).toEqual([]);
  });

  it("names what would stop a save", () => {
    expect(problems(edit, 0, 100)).toEqual([]);
    expect(problems(edit, 12, 100)).toHaveLength(1);
    expect(problems({ ...edit, segments: [{ start: 0, end: 200, speed: 1 }] }, 0, 300)[0]).toMatch(/3 minutes/);
  });
});

describe("what the preview draws (the renderer's numbers)", () => {
  it("zooms around the kill and crops panels like ffmpeg", () => {
    expect(zoomAt(edit, 0)).toBe(1);
    expect(zoomAt(edit, 5)).toBeCloseTo(1.25);             // the kill at 15 s plays at 5 s
    expect(zoomAt(edit, 5 + 1.2 + 0.5)).toBe(1);
    const full = panelSource(blur.panels[0], 1920, 1080);    // 1080x608 is a hair narrower than 16:9
    expect(full[2] / full[3]).toBeCloseTo(1080 / 608);
    expect(full[3]).toBe(1080);
    expect(full[0]).toBeCloseTo((1920 - full[2]) / 2);
    const [x, y, w, h] = panelSource(blur.panels[0], 1920, 1080, 2);
    expect(w).toBeCloseTo(full[2] / 2);
    expect(x + w / 2).toBeCloseTo(960);
    expect(y + h / 2).toBeCloseTo(540, 0);
    const tall = panelSource({ role: "game", src: [0, 0, 1, 1], dst: [0, 0, 1080, 1920] }, 1920, 1080);
    expect(tall[2] / tall[3]).toBeCloseTo(1080 / 1920);     // a wide source cropped to the tall panel
  });
});

describe("layouts and zoom controls (M3.4)", () => {
  it("builds the same templates as the server's edit.py", async () => {
    const { templateLayout } = await import("../studio/model");
    const cam: [number, number, number, number] = [0, 0.56, 0.33, 0.44];
    expect(templateLayout("split", 1280, 720, cam).panels.map((p) => p.dst)).toEqual([[0, 0, 1080, 760], [0, 760, 1080, 608]]);
    const band = templateLayout("band", 1280, 720, cam);
    expect(band.band_h).toBe(420);
    expect(band.panels.map((p) => p.dst)).toEqual([[0, 420, 1080, 608], [0, 1028, 1080, 892]]);
    expect(templateLayout("split", 1280, 720, null).template).toBe("blur");
    expect(templateLayout("native", 720, 1280, null).panels[0].dst).toEqual([0, 0, 1080, 1920]);
    expect(templateLayout("blur", 1280, 618, null).panels[0].dst).toEqual([0, 699, 1080, 522]);
  });

  it("sets the zoom strength for every kill in the parts, and toggles one", async () => {
    const { setZoomStrength, toggleZoom, zoomStrength } = await import("../studio/model");
    const events = [{ t: 12, kind: "self_kill" }, { t: 35, kind: "self_kill" }, { t: 25, kind: "self_kill" }];
    const strong = setZoomStrength(edit, events, 1.3);
    expect(strong.zooms.map((z) => [z.t, z.scale])).toEqual([[12, 1.3], [35, 1.3]]);   // 25 s is cut out
    expect(zoomStrength(strong)).toBe(1.3);
    expect(setZoomStrength(edit, events, 0).zooms).toEqual([]);
    const fewer = toggleZoom(strong, 12.3);
    expect(fewer.zooms.map((z) => z.t)).toEqual([35]);
    expect(toggleZoom(fewer, 12).zooms.map((z) => [z.t, z.scale])).toEqual([[12, 1.3], [35, 1.3]]);
  });
});
