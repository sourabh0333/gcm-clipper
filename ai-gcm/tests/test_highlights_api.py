"""Highlights Stage 1 in the app (S1.5-S1.8): the stream map on the stream page, asking for a highlight, the
finished highlight's view, posting it as a long video, and one stream's batch of drafts at suggested times."""

from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import select

from aigcm.api import highlights
from aigcm.db.models import Clip, Post, Render, Stream, User
from aigcm.jobs import write_json
from aigcm.studio import lane

from test_posts import app, client_for, setup_export  # noqa: F401  (the fixture)

IST = ZoneInfo("Asia/Kolkata")
MAP = {"version": 1, "duration": 3000.0, "best": 2, "session": [],
       "parts": [{"start": 0, "end": 100, "kind": "not_bgmi", "why": "chat"}, {"start": 100, "end": 1000, "kind": "match", "match": 1},
                 {"start": 1000, "end": 1200, "kind": "between"}, {"start": 1200, "end": 2900, "kind": "match", "match": 2},
                 {"start": 2900, "end": 3000, "kind": "between"}],
       "matches": [{"n": 1, "start": 100, "end": 1000, "ended": "death", "placement": 30, "kills": 2, "kill_times": [300, 400],
                    "score": 8, "fights": [], "mode": None},
                   {"n": 2, "start": 1200, "end": 2900, "ended": "dinner", "placement": 1, "kills": 9, "score": 50,
                    "kill_times": [1500], "fights": [{"start": 1490, "end": 1510}], "mode": {"map": "erangel", "mode": "classic"}}]}


def _stream(app):
    with app.state.sessions() as s:
        stream = s.scalars(select(Stream).where(Stream.status == "done")).first()
        return stream.id, app.state.settings.jobs_dir / stream.job_dir


def test_the_map_and_asking_for_a_highlight(app):
    client = client_for(app, "owner@example.com")
    stream_id, folder = _stream(app)
    first = client.get(f"/api/streams/{stream_id}/highlights").json()
    assert first["map"] is None and first["highlights"] == []
    assert client.post(f"/api/streams/{stream_id}/highlights", json={}).status_code == 409    # no map yet
    assert client.post(f"/api/streams/{stream_id}/map").json()["status"] == "queued"

    write_json(folder / "map.json", MAP)
    (folder / "source.mp4").write_bytes(b"x")
    got = client.get(f"/api/streams/{stream_id}/highlights").json()
    assert [m["kills"] for m in got["map"]["matches"]] == [2, 9] and got["map"]["best"] == 2
    assert got["map"]["matches"][1]["map"] == "erangel" and got["map"]["parts"][0]["why"] == "chat"
    assert client.post(f"/api/streams/{stream_id}/highlights", json={"matches": [7]}).status_code == 422
    made = client.post(f"/api/streams/{stream_id}/highlights", json={"matches": [2], "drop": [3, 3]}).json()
    assert made["status"] == "queued" and made["matches"] == [2]
    with app.state.sessions() as s:
        assert s.get(Render, made["id"]).params["drop"] == [3]
    other = client_for(app, "b@example.com")
    assert other.get(f"/api/streams/{stream_id}/highlights").status_code == 404
    assert other.get(f"/api/highlights/{made['id']}").status_code == 404


def _done_highlight(app):
    stream_id, folder = _stream(app)
    write_json(folder / "map.json", MAP)
    (folder / "source.mp4").write_bytes(b"x")
    with app.state.sessions() as s:
        user = s.scalar(select(User).where(User.email == "owner@example.com"))
        render = Render(user_id=user.id, kind="highlight", status="done", output="video.mp4",
                        params={"stream_id": stream_id, "matches": [2]})
        s.add(render)
        s.flush()
        out = lane.highlight_folder(app.state.settings, s.get(Stream, stream_id), render.id)
        out.mkdir(parents=True)
        (out / "video.mp4").write_bytes(b"highlight video")
        (out / "thumb_1.jpg").write_bytes(b"jpg")
        write_json(out / "plan.json", {"pieces": [{"kind": "teaser", "start": 1490, "end": 1510, "label": "IN THIS VIDEO"},
                                                  {"kind": "fight", "start": 1480, "end": 1520, "kills": 1, "match": 2},
                                                  {"kind": "card", "text": "", "length": 2}]})
        write_json(out / "titles.json", {"titles": ["CHICKEN DINNER + 9 FINISHES | ERANGEL | BGMI"], "words": []})
        write_json(out / "post.json", {"title": "CHICKEN DINNER + 9 FINISHES | ERANGEL | BGMI",
                                       "description": "BGMI is a trademark of KRAFTON", "hashtags": ["#bgmi"]})
        write_json(out / "result.json", {"matches": [2], "length": 540.0, "kept": 0.32, "kills": 9, "label": "second",
                                         "shorts": []})
        stream = s.get(Stream, stream_id)
        stream.clips.append(Clip(clip_key=f"hl{render.id[:8]}1", rank=99, start_s=1480, end_s=1520, type="win",
                                 file_name="hl.mp4", title="CHICKEN DINNER 🏆",
                                 details={"from_highlight": render.id, "role": "teaser", "labels": {}}))
        s.commit()
        return render.id, stream_id


def test_a_finished_highlight_posts_as_a_long_video(app):
    setup_export(app)          # connects a channel
    render_id, stream_id = _done_highlight(app)
    client = client_for(app, "owner@example.com")
    link = "https://www.youtube.com/live/abcdefghijk"
    client.put(f"/api/streams/{stream_id}/link", json={"link": link})
    view = client.get(f"/api/highlights/{render_id}").json()
    assert view["kills"] == 9 and view["label"] == "second" and view["titles"][0].startswith("CHICKEN DINNER")
    assert [p["kind"] for p in view["pieces"]] == ["teaser", "fight", "card"]
    assert view["shorts"][0]["role"] == "teaser" and view["thumbnails"] == [f"/media/highlights/{render_id}/thumb_1"]
    assert client.get(view["video"]).content == b"highlight video"

    post = client.post("/api/posts", json={"render_id": render_id}).json()
    assert post["kind"] == "video" and post["title"].startswith("CHICKEN DINNER") and post["stream_id"] == stream_id
    assert post["description"].startswith(f"Full stream: {link}") and post["stream_link"] == link
    assert client.post("/api/posts", json={"render_id": render_id}).json()["id"] == post["id"]   # the open draft


def test_one_stream_one_batch_at_suggested_times(app):
    setup_export(app)
    render_id, _ = _done_highlight(app)
    client = client_for(app, "owner@example.com")
    planned = client.post(f"/api/highlights/{render_id}/plan-posts").json()
    assert len(planned["posts"]) == 1 and len(planned["waiting"]) == 1     # the Short needs an export first
    long_post = planned["posts"][0]
    at = datetime.fromisoformat(long_post["publish_at"].replace("Z", "+00:00")).astimezone(IST)
    assert (at.hour, at.minute) == (12, 0) and long_post["status"] == "draft"
    with app.state.sessions() as s:
        kinds = [r.kind for r in s.scalars(select(Render).where(Render.clip_id.is_not(None))).all()]
        assert "prepare" in kinds and kinds.count("export") >= 2             # the Short's window and export queued
        assert all(p.status == "draft" for p in s.scalars(select(Post)).all())   # nothing approved
    assert client.delete(f"/api/highlights/{render_id}").status_code == 204
    with app.state.sessions() as s:
        assert s.scalar(select(Post).where(Post.render_id == render_id)) is None


def test_suggested_times_in_india():
    shorts = [{"clip_id": 1, "role": "teaser"}, {"clip_id": 2, "role": "best"}, {"clip_id": 3, "role": "best"}]
    morning = datetime(2026, 11, 12, 4, 0)          # 09:30 in India
    times = {k: v.replace(tzinfo=ZoneInfo("UTC")).astimezone(IST) for k, v in
             highlights.suggested_times(morning, shorts).items()}
    assert (times[1].day, times[1].hour, times[1].minute) == (12, 21, 30)      # the teaser tonight
    assert (times["video"].day, times["video"].hour) == (13, 12)               # the highlight tomorrow noon
    assert [(times[k].day, times[k].hour) for k in (2, 3)] == [(14, 21), (15, 21)]
    late = datetime(2026, 11, 12, 15, 0)            # 20:30 in India: too late for tonight
    assert highlights.suggested_times(late, shorts)[1].replace(tzinfo=ZoneInfo("UTC")).astimezone(IST).day == 13
