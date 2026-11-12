"""Hook variety, Reels captions and the cover retry (12 Nov 2026)."""

from types import SimpleNamespace

import pytest
from sqlalchemy import select

from aigcm.db.models import Clip, Post, User
from aigcm.studio import brand, variety
from aigcm.studio import edit as E
from aigcm.titles import KRAFTON_LINE

from test_studio import APP, client_for, ffmpeg, first_clip, make_source, studio_app  # noqa: F401
from aigcm.worker import Worker

TITLES = ["DOUBLE FINISH 💀", "Bhai ye kya scene tha 🤣", "Last second tak dekho 😱"]


def clip(rank, titles=TITLES):
    return SimpleNamespace(rank=rank, title=titles[0] if titles else "Fight", details={"titles": titles})


def test_families_and_turns():
    assert [variety.family_of(t) for t in TITLES] == ["stat", "punchline", "suspense"]
    assert variety.base_of("3 FINISHES 1 FIGHT LAST ZONE #2 🔥") == "3 FINISHES 1 FIGHT LAST ZONE"
    # Clips of a stream take turns, so the stream's Shorts don't all open the same way.
    assert [variety.rotated_title(clip(r)) for r in (1, 2, 3, 4)] == TITLES + [TITLES[0]]
    assert variety.rotated_title(clip(2, [])) == "Fight"
    assert variety.next_title(clip(1), TITLES[0]) == TITLES[1]
    assert variety.next_title(clip(1), TITLES[2]) == TITLES[0]
    assert variety.next_title(clip(1), "typed by the creator") == TITLES[0]


def test_a_stat_title_counts_its_series_on_the_channel(studio_app):  # noqa: F811
    with studio_app.state.sessions() as s:
        user = s.scalar(select(User).where(User.email == "owner@example.com"))
        assert variety.with_series(s, user.id, "DOUBLE FINISH 💀") == "DOUBLE FINISH 💀"     # first time: no number
        s.add_all([Post(user_id=user.id, title="DOUBLE FINISH 💀", status="posted"),
                   Post(user_id=user.id, title="DOUBLE FINISH #2 💀", status="scheduled"),
                   Post(user_id=user.id, title="DOUBLE FINISH #9 💀", status="cancelled")])
        s.commit()
        assert variety.with_series(s, user.id, "DOUBLE FINISH 💀") == "DOUBLE FINISH #3 💀"
        assert variety.with_series(s, user.id, "Bhai ye kya scene tha 🤣") == "Bhai ye kya scene tha 🤣"


def test_another_version_swaps_the_length_and_keeps_only_whats_inside():
    edit = E.EditData(segments=[E.Segment(start=270, end=310)], layout=E.template_layout("native", 1080, 1920),
                      zooms=[E.Zoom(t=275), E.Zoom(t=300)], sfx=[E.SoundFx(t=300, name="boom")], cover_t=275,
                      hook=E.Hook(text=TITLES[0], on=True))
    presets = {"moment": [290, 310], "full_fight": [270, 310]}
    other, (a, b) = variety.alternate(edit, clip(1), presets, TITLES[1])
    assert (a, b) == (290, 310) and [z.t for z in other.zooms] == [300] and other.cover_t is None
    assert other.hook.text == TITLES[1] and other.hook.on and [s.t for s in other.sfx] == [300]
    back, _ = variety.alternate(other, clip(1), presets, TITLES[2])
    assert [(s.start, s.end) for s in back.segments] == [(270, 310)]


@pytest.mark.skipif(ffmpeg() is None, reason="ffmpeg is not installed")
def test_make_another_version_in_the_studio(studio_app):  # noqa: F811
    settings = studio_app.state.settings
    make_source(settings.jobs_dir / "demo-finished" / "source.mp4")
    owner = client_for(studio_app, "owner@example.com")
    c = first_clip(owner)
    url = f"/api/clips/{c['id']}"
    with studio_app.state.sessions() as s:                                        # titles, as real clips have
        row = s.get(Clip, c["id"])
        row.details = {**(row.details or {}), "titles": TITLES}
        row.rank = 1
        s.commit()
    assert owner.post(f"{url}/variant", headers=APP).status_code == 409          # footage not ready yet
    owner.post(f"{url}/decision", json={"verdict": "keep"}, headers=APP)
    assert Worker(settings).render_step()
    before = owner.get(f"{url}/studio").json()["edit"]
    made = owner.post(f"{url}/variant", headers=APP).json()
    assert made["version"] == 1 and made["hook"] != before["data"]["hook"]["text"]
    assert owner.get(f"{url}/studio").json()["edit"]["version"] == 1
    assert client_for(studio_app, "b@example.com").post(f"{url}/variant", headers=APP).status_code == 404


def test_reels_caption():
    post = brand.post_text("1v4 LAST ZONE 😎", f"Full stream: https://youtu.be/abcdefghijk\n\n{KRAFTON_LINE}\n\n#bgmi",
                           ["#bgmi", "#bgmishorts", "#shorts", "#ytshorts", "#gaming"], None)
    reels = brand.reels_text(post, None)
    assert reels["hashtags"] == ["#bgmi", "#bgmireels", "#reels", "#gaming"]
    assert "youtu.be" not in reels["caption"] and "link in bio" in reels["caption"]
    assert reels["caption"].startswith("1v4 LAST ZONE") and KRAFTON_LINE in reels["caption"]
    kit = brand.BrandKit(description="Live daily 8 PM!", disclaimer="")
    with_kit = brand.reels_text(brand.post_text("Clutch", "", ["#bgmi"], kit), kit)
    assert "Live daily 8 PM!" in with_kit["caption"] and KRAFTON_LINE not in with_kit["caption"]
    assert len(with_kit["caption"]) <= 2200


def test_cover_again_only_for_a_post_on_youtube(studio_app):  # noqa: F811
    owner = client_for(studio_app, "owner@example.com")
    with studio_app.state.sessions() as s:
        user = s.scalar(select(User).where(User.email == "owner@example.com"))
        c = s.scalars(select(Clip)).first()
        done = Post(user_id=user.id, clip_id=c.id, title="x", status="posted", video_id="vid12345678",
                    thumbnail="not set: verify the channel")
        draft = Post(user_id=user.id, clip_id=c.id, title="y", status="draft")
        s.add_all([done, draft])
        s.commit()
        done_id, draft_id = done.id, draft.id
    again = owner.post(f"/api/posts/{done_id}/cover", headers=APP)
    assert again.status_code == 200 and again.json()["thumbnail"] is None
    assert owner.post(f"/api/posts/{draft_id}/cover", headers=APP).status_code == 409
    assert client_for(studio_app, "b@example.com").post(f"/api/posts/{done_id}/cover", headers=APP).status_code == 404


def test_a_cover_refused_for_an_unverified_channel_says_so(tmp_path):
    import httpx

    from aigcm import uploader

    cover = tmp_path / "c.jpg"
    cover.write_bytes(b"\xff\xd8 jpeg")
    refuse = httpx.Response(403, json={"error": {"message": "The authenticated user doesn't have permissions to upload "
                                                            "and set custom video thumbnails.",
                                                 "errors": [{"reason": "forbidden"}]}})
    http = httpx.Client(transport=httpx.MockTransport(lambda r: refuse))
    assert uploader.set_thumbnail(http, "t", "vid", cover) == uploader.NEEDS_VERIFY
    other = httpx.Client(transport=httpx.MockTransport(lambda r: httpx.Response(400, json={"error": {"message": "bad image"}})))
    assert uploader.set_thumbnail(other, "t", "vid", cover) == "not set: bad image"
