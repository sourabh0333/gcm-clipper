"""Posts and approvals (M4.2): a draft from an export, its limits, approving exactly what was seen, batch
approval of an explicit list, one post per clip per channel, and nothing reaching the uploader unapproved."""

import shutil
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select

from aigcm import db, posting
from aigcm.api import create_app
from aigcm.api.settings import ApiSettings
from aigcm.db.models import AuditEntry, Clip, Post, Render, User, YouTubeChannel
from aigcm.manage import import_jobs
from aigcm.studio import project

DEMO = Path(__file__).resolve().parent.parent / "demo"
APP = {"x-kaatclip": "1"}


@pytest.fixture
def app(tmp_path):
    jobs = tmp_path / "jobs"
    shutil.copytree(DEMO, jobs, ignore=shutil.ignore_patterns("decisions.json", "run.log"))
    settings = ApiSettings(db_url=db.sqlite_url(tmp_path / "t.db"), jobs_dir=jobs, dev_login=True,
                           invites=frozenset({"owner@example.com", "b@example.com"}), min_free_bytes=0)
    app = create_app(settings)
    with app.state.sessions() as s:
        import_jobs(s, settings, "owner@example.com")
        s.query(Render).delete()
        s.commit()
    return app


def client_for(app, email):
    client = TestClient(app, base_url="http://localhost", headers=APP)
    client.post("/auth/dev-login", json={"email": email})
    return client


def setup_export(app, email="owner@example.com", channel_status="ok", clip_n=0):
    """An export on disk for one of the user's clips, and a connected channel."""
    settings = app.state.settings
    with app.state.sessions() as s:
        user = s.scalar(select(User).where(User.email == email))
        clips = s.scalars(select(Clip).order_by(Clip.id)).all()
        clip = clips[clip_n]
        render = Render(user_id=user.id, clip_id=clip.id, kind="export", status="done", output=f"e{clip.id}.mp4",
                        params={"version": 0})
        s.add(render)
        folder = project.job_folder(settings, clip) / "exports"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / f"e{clip.id}.mp4").write_bytes(b"fake video " + str(clip.id).encode())
        channel = s.scalar(select(YouTubeChannel).where(YouTubeChannel.user_id == user.id))
        if channel is None:
            channel = YouTubeChannel(user_id=user.id, channel_id="UC1", title="Test Gaming", refresh_token="sealed",
                                     status=channel_status, settings={"made_for_kids": False, "synthetic": False})
            s.add(channel)
        s.commit()
        return render.id, clip.id, channel.id


def later(minutes=120):
    return (datetime.now(UTC) + timedelta(minutes=minutes)).isoformat()


def draft(client, render_id, **changes):
    """The open draft for an export, set to good values plus `changes`."""
    post = client.post("/api/posts", json={"render_id": render_id}).json()
    if changes:
        channels = client.get("/api/youtube").json()["channels"]
        body = {"title": "A good clip", "description": "Full stream soon", "tags": ["bgmi"], "mode": "schedule",
                "channel_id": channels[0]["id"] if channels else None, "publish_at": later()}
        body.update(changes)
        post = client.put(f"/api/posts/{post['id']}", json=body).json()
    return post


def test_a_draft_comes_from_the_export_with_the_stream_link(app):
    render_id, clip_id, channel_id = setup_export(app)
    client = client_for(app, "owner@example.com")
    clip = client.get("/api/library").json()
    stream_id = client.get(f"/api/clips/{clip_id}/studio").json()["clip"]["stream_id"]
    assert client.put(f"/api/streams/{stream_id}/link", json={"link": "https://evil.com/x"}).status_code == 422
    link = "https://www.youtube.com/live/abcdefghijk"
    assert client.put(f"/api/streams/{stream_id}/link", json={"link": link}).json() == {"link": link, "drafts_updated": 0}
    assert client.get(f"/api/streams/{stream_id}").json()["link"] == link

    post = client.post("/api/posts", json={"render_id": render_id}).json()
    assert post["status"] == "draft" and post["channel"]["id"] == channel_id and post["clip_id"] == clip_id
    assert post["description"].startswith(f"Full stream: {link}")
    assert post["title"] and len(post["title"]) <= 100 and not any(t.startswith("#") for t in post["tags"])
    # Asking again for the same export gives the same open draft.
    assert client.post("/api/posts", json={"render_id": render_id}).json()["id"] == post["id"]
    assert clip is not None


def test_limits_are_checked_on_approve(app):
    render_id, _, _ = setup_export(app)
    client = client_for(app, "owner@example.com")
    cases = [
        ({"title": ""}, "Add a title"),
        ({"title": "x" * 101}, "101 characters"),
        ({"title": "Clutch <3"}, "< or >"),
        ({"description": "é" * 2600}, "5,000 bytes"),
        ({"publish_at": None}, "Pick when"),
        ({"publish_at": later(5)}, "15 minutes"),
        ({"publish_at": later(60 * 24 * 400)}, "within the next year"),
        ({"channel_id": None, "publish_at": later()}, "Pick the channel"),
    ]
    for changes, words in cases:
        post = draft(client, render_id, **changes)
        refused = client.post(f"/api/posts/{post['id']}/approve", json={"seen": post["updated_at"]})
        assert refused.status_code == 409 and words in refused.json()["detail"], (changes, refused.json())
        assert client.get(f"/api/posts/{post['id']}").json()["status"] == "draft"
    # A title of exactly 100 characters is fine (Developer Policies III.C.1).
    post = draft(client, render_id, title="y" * 100, publish_at=later())
    assert client.post(f"/api/posts/{post['id']}/approve", json={"seen": post["updated_at"]}).status_code == 200


def test_approval_records_exactly_what_was_seen(app):
    render_id, _, channel_id = setup_export(app)
    client = client_for(app, "owner@example.com")
    when = later(180)
    post = draft(client, render_id, title="1v4 clutch in Pochinki", tags=["#bgmi", "bgmi", "clutch"], publish_at=when)
    assert post["tags"] == ["bgmi", "clutch"]

    stale = post["updated_at"]
    edited = draft(client, render_id, title="1v4 clutch in Pochinki!", publish_at=when)
    refused = client.post(f"/api/posts/{post['id']}/approve", json={"seen": "2020-01-01T00:00:00Z"})
    assert refused.status_code == 409 and "changed since you looked" in refused.json()["detail"]
    assert stale is not None

    done = client.post(f"/api/posts/{post['id']}/approve", json={"seen": edited["updated_at"]}).json()
    assert done["status"] == "approved" and done["approved_at"]
    # Approved posts are frozen.
    body = {"title": "changed", "description": "", "tags": [], "mode": "now", "channel_id": channel_id}
    assert client.put(f"/api/posts/{post['id']}", json=body).status_code == 409

    with app.state.sessions() as s:
        row = s.get(Post, post["id"])
        a = row.approval
        assert a["title"] == "1v4 clutch in Pochinki!" and a["privacy"] == "private" and a["category"] == "20"
        assert a["publish_at"].startswith(when[:16]) and a["channel"]["youtube_id"] == "UC1"
        assert a["made_for_kids"] is False and a["synthetic"] is False and len(a["video_sha256"]) == 64
        assert posting.approved(row)
        audit = s.scalar(select(AuditEntry).where(AuditEntry.action == "post_approved"))
        assert audit.detail["post"] == row.id and audit.detail["title"] == a["title"]

        # Anything changed behind the approval's back stops the uploader.
        row.title = "sneaky"
        assert not posting.approved(row)
        s.rollback()


def test_post_now_is_public_and_cancel_takes_it_back(app):
    render_id, _, _ = setup_export(app)
    client = client_for(app, "owner@example.com")
    post = draft(client, render_id, mode="now", publish_at=None)
    done = client.post(f"/api/posts/{post['id']}/approve", json={"seen": post["updated_at"]}).json()
    with app.state.sessions() as s:
        assert s.get(Post, post["id"]).approval["privacy"] == "public"
    assert client.delete(f"/api/posts/{post['id']}").status_code == 409        # cancel first
    assert client.post(f"/api/posts/{post['id']}/cancel").json()["status"] == "cancelled"
    assert client.delete(f"/api/posts/{post['id']}").json() == {"ok": True}
    assert done["status"] == "approved"


def test_one_post_per_clip_per_channel(app):
    render_id, _, _ = setup_export(app)
    client = client_for(app, "owner@example.com")
    first = draft(client, render_id, publish_at=later())
    second = client.post("/api/posts", json={"render_id": render_id}).json()
    assert second["id"] == first["id"]
    assert client.post(f"/api/posts/{first['id']}/approve", json={"seen": first["updated_at"]}).status_code == 200
    again = draft(client, render_id, publish_at=later(300))
    assert again["id"] != first["id"]
    refused = client.post(f"/api/posts/{again['id']}/approve", json={"seen": again["updated_at"]})
    assert refused.status_code == 409 and "already going to Test Gaming" in refused.json()["detail"]
    client.post(f"/api/posts/{first['id']}/cancel")
    again = client.get(f"/api/posts/{again['id']}").json()
    assert client.post(f"/api/posts/{again['id']}/approve", json={"seen": again["updated_at"]}).status_code == 200


def test_batch_approves_each_listed_post_on_its_own(app):
    r1, _, _ = setup_export(app, clip_n=0)
    r2, _, _ = setup_export(app, clip_n=1)
    r3, _, _ = setup_export(app, clip_n=2)
    client = client_for(app, "owner@example.com")
    good1 = draft(client, r1, publish_at=later(60))
    good2 = draft(client, r2, publish_at=later(120))
    bad = draft(client, r3, title="")
    result = client.post("/api/posts/approve", json={"posts": [
        {"id": good1["id"], "seen": good1["updated_at"]}, {"id": bad["id"], "seen": bad["updated_at"]},
        {"id": good2["id"], "seen": good2["updated_at"]}, {"id": "po_nope", "seen": "x"}]}).json()
    assert [p["id"] for p in result["approved"]] == [good1["id"], good2["id"]]
    assert [p["id"] for p in result["problems"]] == [bad["id"], "po_nope"]
    assert "Add a title" in result["problems"][0]["error"]
    assert client.post("/api/posts/approve", json={"posts": []}).status_code == 422
    listed = client.get("/api/posts", params={"status": "approved"}).json()
    assert [p["id"] for p in listed] == [good1["id"], good2["id"]]        # soonest first


def test_an_expired_channel_or_missing_video_blocks_approval(app):
    render_id, clip_id, _ = setup_export(app, channel_status="expired")
    client = client_for(app, "owner@example.com")
    post = draft(client, render_id, publish_at=later())
    refused = client.post(f"/api/posts/{post['id']}/approve", json={"seen": post["updated_at"]})
    assert "Reconnect Test Gaming" in refused.json()["detail"]
    with app.state.sessions() as s:
        s.scalar(select(YouTubeChannel)).status = "ok"
        clip = s.get(Clip, clip_id)
        (project.job_folder(app.state.settings, clip) / "exports" / f"e{clip_id}.mp4").unlink()
        s.commit()
    refused = client.post(f"/api/posts/{post['id']}/approve", json={"seen": post["updated_at"]})
    assert "Export the clip again" in refused.json()["detail"]


def test_drafts_never_reach_the_uploader():
    post = Post(status="draft", title="t", description="d", channel_id="yt_1", render_id="rn_1",
                approval={"title": "t", "description": "d", "channel": {"id": "yt_1"}, "render": "rn_1",
                          "video_sha256": "a" * 64})
    assert not posting.approved(post)          # an approval record alone is not enough
    post.status, post.approved_at = "approved", datetime(2026, 11, 10)
    assert posting.approved(post)
    post.approval = None
    assert not posting.approved(post)


def test_another_creator_cannot_see_or_approve(app):
    render_id, _, _ = setup_export(app)
    owner = client_for(app, "owner@example.com")
    post = draft(owner, render_id, publish_at=later())
    other = client_for(app, "b@example.com")
    assert other.post("/api/posts", json={"render_id": render_id}).status_code == 404
    assert other.get(f"/api/posts/{post['id']}").status_code == 404
    assert other.post(f"/api/posts/{post['id']}/approve", json={"seen": post["updated_at"]}).status_code == 404
    assert other.post("/api/posts/approve", json={"posts": [{"id": post["id"], "seen": post["updated_at"]}]}).json() \
        == {"approved": [], "problems": [{"id": post["id"], "error": "Not found."}]}
    assert other.get("/api/posts").json() == []
    body = {"title": "x", "description": "", "tags": [], "mode": "now", "channel_id": None}
    assert other.put(f"/api/posts/{post['id']}", json=body).status_code == 404
    assert owner.get(f"/api/posts/{post['id']}").json()["status"] == "draft"


def test_text_rules():
    assert posting.clean_tags(["#BGMI", "bgmi", " clutch ", "", "<x>"]) == ["BGMI", "clutch"]
    long = [f"tag number {i}" for i in range(60)]
    assert posting.tags_length(posting.clean_tags(long)) <= posting.TAGS_MAX
    for ok in ("https://www.youtube.com/watch?v=abcdefghijk", "https://youtu.be/abcdefghijk?t=30",
               "https://youtube.com/live/abcdefghijk?feature=share"):
        assert posting.clean_link(ok) == ok
    for bad in ("http://youtube.com/watch?v=abcdefghijk", "https://youtube.com.evil.com/watch?v=abcdefghijk",
                "javascript:alert(1)", "https://youtu.be/short"):
        with pytest.raises(posting.PostError):
            posting.clean_link(bad)
    assert posting.clean_link("  ") is None
