"""Stacked Shorts from vertical streams (owner, 14 Nov): finding the game and camera bands in a streamer's own
vertical layout, and the default Short edit that stacks them (16:9 highlights keep the stream as streamed)."""

import numpy as np

from aigcm.studio import gamebox
from aigcm.studio.edit import FACECAM_H, W, default_edit


def _rows(bands, n=160):
    rows = np.full(n, 1.5)                       # overlays: hardly change
    for (a, b), level in bands:
        rows[int(a * n):int(b * n)] = level
    return rows


def test_game_and_camera_bands_like_anji():
    # Camera 10-36% (people move a little), game 37-69% (always changing), overlay below.
    found = gamebox.layout_from_rows(_rows([((0.10, 0.36), 8.0), ((0.37, 0.69), 50.0)]), counter_y=0.36)
    assert abs(found["game"][1] - 0.37) < 0.02 and abs(found["game"][3] - 0.32) < 0.02
    assert found["cam"][1] < 0.1 and found["cam"][1] + found["cam"][3] <= found["game"][1] + 1e-6   # never into the game


def test_animated_art_under_the_game_is_not_the_game():
    # T-REX: the game (7-55%), a quiet overlay strip, then animated art that changes as much as the game.
    rows = _rows([((0.07, 0.545), 44.0), ((0.59, 0.96), 58.0)])
    found = gamebox.layout_from_rows(rows, counter_y=0.56, aspect=1280 / 720)
    assert abs(found["game"][1] - 0.07) < 0.02 and found["game"][1] + found["game"][3] < 0.56


def test_no_clear_game_band():
    assert gamebox.layout_from_rows(np.zeros(160)) is None


def test_the_default_short_stacks_camera_over_the_cut_out_game():
    game, cam = [0.0, 0.3625, 1.0, 0.325], [0.0, 0.1, 1.0, 0.2625]
    edit = default_edit(10.0, 40.0, 720, 1280, "CLUTCH", [{"t": 20.0, "kind": "self_kill"}], facecam=cam, game=game)
    panels = {p.role: p for p in edit.layout.panels}
    assert edit.layout.template == "split" and panels["cam"].dst == (0, 0, W, FACECAM_H)
    assert panels["game"].src == tuple(game) and panels["game"].dst[1] == FACECAM_H
    assert abs(panels["game"].dst[3] - W / ((1.0 * 720) / (0.325 * 1280))) <= 2       # the band keeps its shape
    assert edit.zooms                                                                   # kills zoom, as landscape
    # No camera found: the cut-out game over a blur; nothing found: the stream as it was streamed.
    assert default_edit(10.0, 40.0, 720, 1280, game=game).layout.panels[0].src == tuple(game)
    assert default_edit(10.0, 40.0, 720, 1280).layout.template == "native"
