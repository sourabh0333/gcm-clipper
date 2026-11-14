"""A clip's edit list: what the creator changed, kept apart from the source video, so preview is instant and
rendering happens only on export. See plans/M3 Studio plan.md (decisions 1–4).

Times are **source seconds**: seconds into the job's source file, the same clock as the clip's start and
end and the engine's events. The output is a 1080x1920 canvas; layout panels each draw a crop of the
source frame (fractions of its width and height) into a rectangle of the canvas (pixels). The browser
preview and the ffmpeg renderer read the same numbers, so they show the same picture."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

W, H = 1080, 1920
MAX_LENGTH_S = 180.0      # YouTube Shorts allow up to 3 minutes
MIN_SEGMENT_S = 0.3
MAX_SEGMENTS = 40
KILL_KINDS = ("self_kill",)
ZOOM_MERGE_S = 2.0        # kills closer than this share one zoom
FACECAM_H = 760           # the split layout's camera band, as the engine's render.py had it
# Clip types that are about what was said: they get word captions by default (plan section 4.4).
TALK_TYPES = {"funny", "banter", "rage", "hype", "wholesome", "story", "talk", "reaction"}
BAND_H = 420              # the band layout's black hook band


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Segment(Strict):
    start: float = Field(ge=0)
    end: float = Field(gt=0)
    speed: float = Field(1.0, ge=1.0, le=4.0)


class Panel(Strict):
    role: Literal["game", "cam"]
    src: tuple[float, float, float, float]   # x, y, w, h as fractions of the source frame
    dst: tuple[int, int, int, int]           # x, y, w, h in canvas pixels

    @field_validator("src")
    @classmethod
    def _src_inside(cls, v):
        x, y, w, h = v
        if not (0 <= x < 1 and 0 <= y < 1 and 0.02 <= w <= 1 and 0.02 <= h <= 1 and x + w <= 1.0001
                and y + h <= 1.0001):
            raise ValueError("panel crop must lie inside the frame")
        return v

    @field_validator("dst")
    @classmethod
    def _dst_inside(cls, v):
        x, y, w, h = v
        if not (0 <= x and 0 <= y and 16 <= w and 16 <= h and x + w <= W and y + h <= H):
            raise ValueError("panel must lie inside the 1080x1920 canvas")
        return v


class Layout(Strict):
    template: Literal["native", "blur", "band", "split"]
    background: Literal["blur", "black"] = "blur"
    band_h: int = Field(0, ge=0, le=900)     # a black band across the top, for the hook (M3.5)
    panels: list[Panel] = Field(min_length=1, max_length=3)


class Zoom(Strict):
    t: float = Field(ge=0)                       # the kill, in source seconds
    dur: float = Field(1.2, ge=0.3, le=6.0)      # how long the zoom holds after it
    scale: float = Field(1.25, ge=1.0, le=2.5)


class SoundFx(Strict):
    t: float = Field(ge=0)                                    # source seconds
    name: Literal["whoosh", "boom", "ding", "pop"]            # synthesised in assets/sfx (make_sfx.py)
    gain: float = Field(0.7, ge=0.05, le=1.0)


class Hook(Strict):
    text: str = Field("", max_length=80)
    color: Literal["white", "yellow"] = "yellow"
    on: bool = False


class WordFix(Strict):
    t: float                                  # the word's start in the transcript (source seconds)
    w: str = Field("", max_length=40)         # what to show instead; empty hides the word


class Captions(Strict):
    on: bool = False
    script: Literal["auto", "latin", "devanagari"] = "auto"
    color: Literal["white", "yellow"] = "white"
    size: Literal["normal", "large"] = "normal"
    words: list[WordFix] = Field(default_factory=list, max_length=800)


class FaceSpan(Strict):
    """A stretch (source seconds) when the Short shows the face alone, big, over a blurred copy of it: the
    streamer talking or reacting with no shooting."""
    start: float = Field(ge=0)
    end: float = Field(ge=0)


class EditData(Strict):
    v: Literal[1] = 1
    segments: list[Segment] = Field(min_length=1, max_length=MAX_SEGMENTS)
    layout: Layout
    zooms: list[Zoom] = Field(default_factory=list, max_length=30)
    hook: Hook = Field(default_factory=Hook)
    captions: Captions = Field(default_factory=Captions)
    cover_t: float | None = None
    sponsor_safe: bool = False
    keep_hud: bool = True      # the game panel's top strip (kill counters) stays unzoomed during zooms
    sfx: list[SoundFx] = Field(default_factory=list, max_length=40)
    lower_third: bool = False  # the brand kit's strip (logo, name, UPI, Instagram) at the bottom
    intro: bool = False        # the brand kit's intro before the clip
    outro: bool = False        # and its outro after
    face: list[FaceSpan] = Field(default_factory=list, max_length=20)   # face-only moments (needs a camera)

    @model_validator(mode="after")
    def _segments_in_order(self):
        last_end = -1.0
        for seg in self.segments:
            if seg.end - seg.start < MIN_SEGMENT_S:
                raise ValueError(f"each part must be at least {MIN_SEGMENT_S} s long")
            if seg.start < last_end - 1e-6:
                raise ValueError("parts must be in time order and must not overlap")
            last_end = seg.end
        if output_length(self.segments) > MAX_LENGTH_S + 0.01:
            raise ValueError(f"a clip can be at most {MAX_LENGTH_S:.0f} s long")
        return self


def check_window(edit, start, end):
    """Every part must lie inside the clip's working window (the only footage kept for editing)."""
    for seg in edit.segments:
        if seg.start < start - 0.05 or seg.end > end + 0.05:
            raise ValueError("a part reaches outside the footage saved for this clip")


# --- time mapping ----------------------------------------------------------------------------------------

def output_length(segments):
    return sum((s.end - s.start) / s.speed for s in segments)


def to_output(segments, t):
    """Where source time `t` lands in the exported video, or None if it was cut out."""
    offset = 0.0
    for s in segments:
        if s.start <= t <= s.end:
            return offset + (t - s.start) / s.speed
        offset += (s.end - s.start) / s.speed
    return None


def span_to_output(segments, a, b):
    """The output spans that source span [a, b] becomes (one per part it touches)."""
    out, offset = [], 0.0
    for s in segments:
        lo, hi = max(a, s.start), min(b, s.end)
        if hi > lo:
            out.append((round(offset + (lo - s.start) / s.speed, 3), round(offset + (hi - s.start) / s.speed, 3)))
        offset += (s.end - s.start) / s.speed
    return out


# --- layouts ---------------------------------------------------------------------------------------------

def _even(x):
    return int(round(x / 2)) * 2


def template_layout(template, width, height, facecam=None, game=None):
    """The starting panels of a layout template for a source of this size. `facecam` is the camera box as
    frame fractions (x, y, w, h), needed by "split"; without one, "split" falls back to "blur". `game` is
    where the game sits inside a vertical stream's own layout (studio.gamebox); the game panel shows only
    that part."""
    full = (0.0, 0.0, 1.0, 1.0)
    if game and template != "native":
        full = tuple(float(v) for v in game)
        aspect = (game[2] * width) / (game[3] * height)
    else:
        aspect = width / height
    if template == "native":
        w, h = W, _even(W / aspect)
        if h > H:
            w, h = _even(H * aspect), H
        return Layout(template="native", background="black",
                      panels=[Panel(role="game", src=full, dst=((W - w) // 2, (H - h) // 2, w, h))])
    game_h = min(_even(W / aspect), H)
    if template == "split" and facecam:
        return Layout(template="split", background="blur", panels=[
            Panel(role="cam", src=tuple(facecam), dst=(0, 0, W, FACECAM_H)),
            Panel(role="game", src=full, dst=(0, FACECAM_H, W, min(game_h, H - FACECAM_H)))])
    if template == "band":
        # The hook band on top, the gameplay under it, and the camera filling the rest when there is one.
        game = Panel(role="game", src=full, dst=(0, BAND_H, W, min(game_h, H - BAND_H)))
        below = BAND_H + game.dst[3]
        panels = [game]
        if facecam and H - below >= 200:
            panels.append(Panel(role="cam", src=tuple(facecam), dst=(0, below, W, H - below)))
        return Layout(template="band", background="blur", band_h=BAND_H, panels=panels)
    return Layout(template="blur", background="blur",
                  panels=[Panel(role="game", src=full, dst=(0, (H - game_h) // 2, W, game_h))])


def hook_box(layout):
    """Where the hook sits on the canvas, (y, height): in the black band when there is one; at the foot
    of the camera band in "split" (so it covers neither the face nor the kill counters); above the
    gameplay in "blur"; near the top of a vertical stream's own layout."""
    if layout.band_h:
        return 0, layout.band_h
    if layout.template == "split":
        return FACECAM_H - 260, 260
    if layout.template == "blur":
        game_top = min((p.dst[1] for p in layout.panels if p.role == "game"), default=H // 3)
        height = min(420, max(160, game_top - 140))
        return max(0, game_top - height - 30), height
    return 110, 360


def cover_time(edit, intro_s=0.0):
    """Where the Short's cover frame is taken from, in seconds of the exported video: the frame the creator
    chose, else the first zoomed kill (a moment of action, hook and all), else 40% in. `intro_s` is the
    length of an intro joined before the clip."""
    at = to_output(edit.segments, edit.cover_t) if edit.cover_t is not None else None
    if at is None:
        kills = [t for t in (to_output(edit.segments, z.t) for z in edit.zooms) if t is not None]
        at = min(kills) + 0.3 if kills else output_length(edit.segments) * 0.4
    return round(intro_s + min(max(at, 0.0), max(0.0, output_length(edit.segments) - 0.1)), 3)


def is_talk(kind, labels=None):
    return kind in TALK_TYPES or bool((labels or {}).get("talk"))


def kill_zooms(events, start, end):
    """One zoom per kill (kills close together share one), for landscape sources."""
    times = sorted(e["t"] for e in events or () if e.get("kind") in KILL_KINDS and start <= e["t"] <= end)
    zooms = []
    for t in times:
        if zooms and t - zooms[-1].t < ZOOM_MERGE_S:
            continue
        zooms.append(Zoom(t=t))
    return zooms


def default_edit(start, end, width, height, title=None, events=(), captions=False, facecam=None,
                 window=None, brand=None, game=None):
    """The edit a clip starts with, made from what the engine knows (decision 2). Shorts are stacked, the
    camera on top and the game below (owner, 14 Nov; the stacked layout outperforms a game-only crop on the
    channels studied): a vertical stream's game band and camera are cut out of its own layout (`game`, from
    studio.gamebox); landscape streams go over a blurred fill with a zoom on each kill. A vertical stream
    whose game can't be found stays as it was streamed."""
    if window:
        start, end = max(start, window[0]), min(end, window[1])
    b = brand or {}   # what the creator's brand kit sets (studio.brand.defaults)
    vertical = height > width
    # Facecam on top for streams with a camera (the top Indian format); otherwise the blurred fill.
    if vertical and not game:
        layout = template_layout("native", width, height, facecam)
    else:
        layout = template_layout("split" if facecam else "blur", width, height, facecam, game if vertical else None)
    vertical = vertical and not game        # a cropped game band zooms on kills like a landscape stream
    return EditData(
        segments=[Segment(start=round(start, 3), end=round(end, 3))],
        layout=layout,
        zooms=[] if vertical else kill_zooms(events, start, end),
        hook=Hook(text=(title or "")[:80], on=bool((title or "").strip()), color=b.get("hook_color", "yellow")),
        captions=Captions(on=bool(captions), color=b.get("caption_color", "white"), size=b.get("caption_size", "normal")),
        lower_third=bool(b.get("lower_third")), intro=bool(b.get("intro")), outro=bool(b.get("outro")),
    )
