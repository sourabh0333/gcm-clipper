from aigcm.vision import Counter, counter_events, is_spectating, parse_number


def feed(counter, reads, fresh_match=True):
    changes = []
    for t, value in enumerate(reads):
        change = counter.update(float(t), value, fresh_match)
        if change:
            changes.append(change)
    return changes


def test_parse_number_fixes_letter_confusions():
    assert parse_number("4") == 4
    assert parse_number("D") == 0
    assert parse_number(" 1 2 ") == 12
    assert parse_number("Elim") is None
    assert parse_number("1234") is None


def test_kill_needs_two_agreeing_reads_and_keeps_first_time():
    changes = feed(Counter("elims"), [3, 3, None, 4, 4, 4])
    assert changes == [(0.0, None, 3), (3.0, 3, 4)]
    assert len(counter_events(changes[1])) == 1


def test_single_misread_makes_no_kill():
    changes = feed(Counter("elims"), [3, 3, 8, 3, 9, 3])
    assert changes == [(0.0, None, 3)]


def test_two_misreads_of_a_lower_number_make_no_fake_kills():
    changes = feed(Counter("elims"), [4, 4, 1, 1, 4, 4])
    assert changes == [(0.0, None, 4)]


def test_reset_to_zero_starts_a_new_match_in_a_fresh_lobby():
    changes = feed(Counter("elims"), [5, 5, 0, 0, 1, 1])
    kinds = [e["kind"] for c in changes for e in counter_events(c)]
    assert kinds == ["match_start", "self_kill"]


def test_reset_is_timed_when_the_new_lobby_confirms_it():
    counter = Counter("elims")
    feed(counter, [4, 4])
    for t in range(2, 10):
        assert counter.update(float(t), 0, fresh_match=False) is None
    assert counter.update(10.0, 0, fresh_match=True) == (10.0, 4, 0)


def test_without_lobby_signal_a_flicker_is_ignored_but_a_long_reset_counts():
    # ANJI's vertical layout hides the Remaining counter; a 2 s flicker to 0 double-counted a kill.
    flicker = feed(Counter("elims"), [1, 1, 0, 0, 0, 0, 1, 1], fresh_match=None)
    assert flicker == [(0.0, None, 1)]
    reset = feed(Counter("elims"), [3, 3] + [0] * 20, fresh_match=None)
    assert reset[-1][1:] == (3, 0)


def test_reset_hold_is_measured_in_seconds_not_reads():
    # At one read a second the 10 s hold is 10 reads; at two a second it is 20.
    assert Counter("elims", 1.0).reset_reads == 10 and Counter("elims", 2.0).reset_reads == 20
    reset = feed(Counter("elims", 1.0), [3, 3] + [0] * 10, fresh_match=None)
    assert reset[-1][1:] == (3, 0)


def test_brief_zero_mid_match_is_ignored():
    # A teammate's counter flashing up while the streamer spectates must not reset kills.
    changes = feed(Counter("elims"), [3, 3, 0, 0, 0, 3, 3], fresh_match=False)
    assert changes == [(0.0, None, 3)]


def test_long_teammate_counter_while_spectating_never_resets_kills():
    changes = feed(Counter("elims"), [3, 3] + [0] * 60 + [3, 3], fresh_match=False)
    assert changes == [(0.0, None, 3)]


def test_spectating_text_matches_ocr_misspellings():
    for text in ["Spectating:Teammate", "Spectting:Teammate", "Spectsting", "Spectaing Tuamnata"]:
        assert is_spectating(text)
    assert not is_spectating("Request Recall")


def test_remaining_accepts_normal_drops_and_new_lobbies():
    changes = feed(Counter("remaining"), [97, 97, 80, 80, 60, 60, 98, 98])
    assert [c[2] for c in changes] == [97, 80, 60, 98]


def test_remaining_ignores_dropped_digits():
    # "60" misread as "6" and "10" as "0" in the real test stream.
    changes = feed(Counter("remaining"), [60, 60, 6, 6, 60, 0, 0, 59, 59])
    assert [c[2] for c in changes] == [60, 59]
    # "41" read as "141" on a stream that enlarged the HUD.
    assert feed(Counter("remaining"), [41, 41, 141, 141, 141, 141, 141, 141]) == [(0.0, None, 41)]


def test_icon_hud_row_gives_remaining_and_elims_boxes():
    from aigcm.vision import icon_row
    # OCR reads the compact HUD's row as one line, icons included: person 36, crosshair 20, wings 2 across
    # three 58 px cells on a 1280x720 frame (crop pixels of the top-left search area).
    lines = [("236202", 0.85, (72, 1, 246, 29)), ("BGMI", 0.9, (301, 6, 339, 27)), ("TAGLoLzZz", 0.84, (87, 32, 141, 51))]
    boxes = icon_row(lines, 1280, 720)
    assert set(boxes) == {"remaining", "elims"}
    rx, ry, rw, rh = boxes["remaining"]
    ex = boxes["elims"][0]
    # The players number ends just inside the first cell (about x=125) and the box holds two digits.
    assert abs((rx + rw) * 1280 - 125) < 4 and 34 < rw * 1280 < 52 and rx < ex and 0 <= ry < 0.05
    assert icon_row([("36", 0.9, (60, 10, 95, 36))], 1280, 720) == {}
    # The compass strip is a long row of three-digit headings; it must not be taken for the HUD.
    compass = [(str(v), 0.9, (300 + i * 40, 8, 330 + i * 40, 30)) for i, v in enumerate((105, 120, 135, 150, 165))]
    assert icon_row(compass, 1280, 720) == {}
