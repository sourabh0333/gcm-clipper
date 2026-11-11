"""The platform's tables. The engine stays file-based (job folders); the database owns accounts, who owns
what, the job queue, clips and the creator's decisions. See plans/M2 platform core plan.md (R11)."""

import secrets
from datetime import UTC, datetime

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def utcnow():
    """Naive UTC time: SQLite keeps no time zone, so every stored time is UTC by convention."""
    return datetime.now(UTC).replace(tzinfo=None)


def new_id(prefix):
    """A short random id that is also safe as a folder name."""
    return f"{prefix}_{secrets.token_hex(6)}"


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(320), unique=True)
    name: Mapped[str | None] = mapped_column(String(200))
    picture: Mapped[str | None] = mapped_column(String(500))
    google_sub: Mapped[str | None] = mapped_column(String(64), unique=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime)
    # The privacy policy and terms version this person accepted, and when (M4.8; aigcm.api.legal.TERMS_VERSION).
    terms_version: Mapped[str | None] = mapped_column(String(20))
    terms_accepted_at: Mapped[datetime | None] = mapped_column(DateTime)

    # Deleting an account deletes its streams (and through them clips and uploads): the database's ON DELETE
    # CASCADE does it, so the ORM must not try to blank the owner first.
    streams: Mapped[list["Stream"]] = relationship(back_populates="user", cascade="all, delete-orphan",
                                                   passive_deletes=True)


class Session(Base):
    """A signed-in browser. Only a hash of the cookie's token is stored, so a copy of the database can't be
    used to sign in."""
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)  # sha256 of the cookie token
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    last_used_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    expires_at: Mapped[datetime] = mapped_column(DateTime)
    user_agent: Mapped[str | None] = mapped_column(String(300))

    user: Mapped[User] = relationship()


class Invite(Base):
    """Who may sign in during the beta, besides the addresses in AIGCM_INVITES."""
    __tablename__ = "invites"

    email: Mapped[str] = mapped_column(String(320), primary_key=True)
    invited_by: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)


class LiveSession(Base):
    """A stream as it happens on the Live screen: its start time places the markers tapped during it."""
    __tablename__ = "live_sessions"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=lambda: new_id("live"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    title: Mapped[str | None] = mapped_column(String(300))
    started_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime)
    # The chat listener (M4.7): the YouTube live found for this session, where reading its chat got to, when to
    # read next, and a line for the Live screen.
    channel_id: Mapped[str | None] = mapped_column(String(32))
    broadcast_id: Mapped[str | None] = mapped_column(String(32))
    chat_id: Mapped[str | None] = mapped_column(String(200))
    chat_token: Mapped[str | None] = mapped_column(String(300))
    chat_at: Mapped[datetime | None] = mapped_column(DateTime)
    chat_note: Mapped[str | None] = mapped_column(String(200))


class Stream(Base):
    """One uploaded recording and the engine job made from it."""
    __tablename__ = "streams"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=lambda: new_id("st"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(300))
    game: Mapped[str] = mapped_column(String(32), default="bgmi")
    recorded_on: Mapped[str | None] = mapped_column(String(10))  # YYYY-MM-DD, as the creator gives it
    # uploading, queued, running, stopped, done, failed
    status: Mapped[str] = mapped_column(String(16), default="uploading", index=True)
    job_dir: Mapped[str] = mapped_column(String(80), unique=True)  # folder name under the jobs folder
    source_name: Mapped[str | None] = mapped_column(String(300))
    size_bytes: Mapped[int | None] = mapped_column(Integer)
    duration_s: Mapped[float | None] = mapped_column(Float)
    error: Mapped[str | None] = mapped_column(Text)
    stop_requested: Mapped[bool] = mapped_column(Boolean, default=False)
    live_session_id: Mapped[str | None] = mapped_column(ForeignKey("live_sessions.id", ondelete="SET NULL"))
    link: Mapped[str | None] = mapped_column(String(200))   # the stream on YouTube, for "Full stream:" in posts
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    queued_at: Mapped[datetime | None] = mapped_column(DateTime)
    started_at: Mapped[datetime | None] = mapped_column(DateTime)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime)

    user: Mapped[User] = relationship(back_populates="streams")
    clips: Mapped[list["Clip"]] = relationship(back_populates="stream", cascade="all, delete-orphan",
                                               passive_deletes=True, order_by="Clip.rank")


class Upload(Base):
    """A resumable upload (tus semantics): bytes arrive in order; `offset` is how many have been written."""
    __tablename__ = "uploads"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=lambda: new_id("up"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    stream_id: Mapped[str] = mapped_column(ForeignKey("streams.id", ondelete="CASCADE"), index=True)
    filename: Mapped[str] = mapped_column(String(300))
    length: Mapped[int] = mapped_column(Integer)
    offset: Mapped[int] = mapped_column(Integer, default=0)
    # For marker-window pieces (M2.8): where this piece starts in the stream, in seconds.
    stream_offset_s: Mapped[float | None] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime)
    # Uploading while streaming: the recording is still growing, so `length` is 0 (unknown) until the
    # browser sends the final size (tus creation-defer-length).
    growing: Mapped[bool] = mapped_column(Boolean, default=False)


class Clip(Base):
    """A clip the engine made, copied from the job's ranked.json once the job is done, plus the creator's
    keep or reject decision."""
    __tablename__ = "clips"
    __table_args__ = (UniqueConstraint("stream_id", "clip_key"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stream_id: Mapped[str] = mapped_column(ForeignKey("streams.id", ondelete="CASCADE"), index=True)
    clip_key: Mapped[str] = mapped_column(String(40))  # the engine's clip id
    rank: Mapped[int] = mapped_column(Integer)
    start_s: Mapped[float] = mapped_column(Float)
    end_s: Mapped[float] = mapped_column(Float)
    type: Mapped[str] = mapped_column(String(24))
    score: Mapped[float | None] = mapped_column(Float)
    file_name: Mapped[str] = mapped_column(String(120))
    safe_file_name: Mapped[str | None] = mapped_column(String(120))
    title: Mapped[str | None] = mapped_column(String(200))
    why: Mapped[str | None] = mapped_column(Text)
    details: Mapped[dict] = mapped_column(JSON, default=dict)  # titles, hashtags, description, labels, flags...
    spoken: Mapped[str | None] = mapped_column(Text)   # what was said in the clip, for the library's search
    decision: Mapped[str | None] = mapped_column(String(8))  # keep, reject or none yet
    decision_reason: Mapped[str | None] = mapped_column(String(300))
    decided_at: Mapped[datetime | None] = mapped_column(DateTime)

    stream: Mapped[Stream] = relationship(back_populates="clips")
    edits: Mapped[list["Edit"]] = relationship(back_populates="clip", cascade="all, delete-orphan",
                                               passive_deletes=True, order_by="Edit.version")


class Edit(Base):
    """One saved version of a clip's edit list (M3 Studio). The newest version is the clip's edit; the last
    20 are kept for going back. See plans/M3 Studio plan.md, decision 1."""
    __tablename__ = "edits"
    __table_args__ = (UniqueConstraint("clip_id", "version"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    clip_id: Mapped[int] = mapped_column(ForeignKey("clips.id", ondelete="CASCADE"), index=True)
    version: Mapped[int] = mapped_column(Integer)
    data: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)

    clip: Mapped[Clip] = relationship(back_populates="edits")


class Render(Base):
    """Studio work for the worker's render lane: "prepare" saves a kept clip's working window and preview
    copy; "export" renders an edit into the final video. Runs beside stream jobs (M3 review S-R7)."""
    __tablename__ = "renders"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=lambda: new_id("rn"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    clip_id: Mapped[int | None] = mapped_column(ForeignKey("clips.id", ondelete="CASCADE"), index=True)
    kind: Mapped[str] = mapped_column(String(16))
    status: Mapped[str] = mapped_column(String(12), default="queued", index=True)  # queued running done failed
    params: Mapped[dict] = mapped_column(JSON, default=dict)
    output: Mapped[str | None] = mapped_column(String(200))   # file name, for exports
    error: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    started_at: Mapped[datetime | None] = mapped_column(DateTime)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime)


class YouTubeChannel(Base):
    """A creator's connected YouTube channel (M4.1). The refresh token is encrypted (aigcm.youtube.seal) and
    deleted on disconnect; nothing else from YouTube is kept here beyond the channel's name and picture."""
    __tablename__ = "youtube_channels"
    __table_args__ = (UniqueConstraint("user_id", "channel_id"),)

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=lambda: new_id("yt"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    channel_id: Mapped[str] = mapped_column(String(64))
    title: Mapped[str] = mapped_column(String(200))
    thumbnail: Mapped[str | None] = mapped_column(String(500))
    scopes: Mapped[str] = mapped_column(Text, default="")
    refresh_token: Mapped[str] = mapped_column(Text)            # encrypted
    status: Mapped[str] = mapped_column(String(12), default="ok")   # ok, expired
    settings: Mapped[dict] = mapped_column(JSON, default=dict)  # made_for_kids, synthetic: the creator's answers
    connected_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    checked_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    # The last 28 days of uploads (ids, dates, lengths, live or not) for the Shorts-share gauge (M4.4); refreshed
    # every few hours while the calendar is used, deleted with the channel, never older than 30 days (III.E.4).
    recent: Mapped[list | None] = mapped_column(JSON)
    recent_at: Mapped[datetime | None] = mapped_column(DateTime)
    upcoming: Mapped[list | None] = mapped_column(JSON)    # scheduled lives (id, title, start), for teasers (M4.5)
    # The last 28 days of YouTube Analytics by content type (M4.6). Like `recent`, refreshed while used and
    # deleted when older than 30 days or when the connection no longer works (Developer Policies III.E.4).
    stats: Mapped[dict | None] = mapped_column(JSON)
    stats_at: Mapped[datetime | None] = mapped_column(DateTime)


class Post(Base):
    """A post to YouTube (M4.2). Editable while a draft; Approve freezes it and stores exactly what was approved
    in `approval` (the uploader posts that and nothing else). Status: draft, approved, uploading, scheduled,
    posted, failed, cancelled."""
    __tablename__ = "posts"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=lambda: new_id("po"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    clip_id: Mapped[int | None] = mapped_column(ForeignKey("clips.id", ondelete="CASCADE"), index=True)
    render_id: Mapped[str | None] = mapped_column(ForeignKey("renders.id", ondelete="SET NULL"))
    channel_id: Mapped[str | None] = mapped_column(ForeignKey("youtube_channels.id", ondelete="SET NULL"))
    kind: Mapped[str] = mapped_column(String(8), default="short")
    title: Mapped[str] = mapped_column(String(100), default="")
    description: Mapped[str] = mapped_column(Text, default="")
    tags: Mapped[list] = mapped_column(JSON, default=list)
    mode: Mapped[str] = mapped_column(String(8), default="schedule")    # schedule (private + publishAt) or now
    publish_at: Mapped[datetime | None] = mapped_column(DateTime)        # UTC
    status: Mapped[str] = mapped_column(String(12), default="draft", index=True)
    approval: Mapped[dict | None] = mapped_column(JSON)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime)
    video_id: Mapped[str | None] = mapped_column(String(32))
    error: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    # The uploader's bookkeeping (M4.3): YouTube's resumable session (valid about a week), tries, when to try
    # again, the thumbnail's result, when it went public, and when YouTube was last asked about it.
    upload_url: Mapped[str | None] = mapped_column(Text)
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    next_try_at: Mapped[datetime | None] = mapped_column(DateTime)
    thumbnail: Mapped[str | None] = mapped_column(String(200))
    posted_at: Mapped[datetime | None] = mapped_column(DateTime)
    checked_at: Mapped[datetime | None] = mapped_column(DateTime)
    # The stream funnel (M4.5): the creator ticked "finished in Studio" (related video and pinned comment), and
    # the upcoming live this post is a teaser for.
    studio_done: Mapped[bool] = mapped_column(Boolean, default=False)
    teaser_for: Mapped[str | None] = mapped_column(String(32))

    clip: Mapped["Clip | None"] = relationship()
    channel: Mapped["YouTubeChannel | None"] = relationship()


class QuotaDay(Base):
    """YouTube API use for one Pacific-time day (Google's quota day), for the whole app: the uploads bucket
    (100 videos.insert a day) and the shared 10,000 units."""
    __tablename__ = "quota_days"

    day: Mapped[str] = mapped_column(String(10), primary_key=True)   # YYYY-MM-DD in America/Los_Angeles
    uploads: Mapped[int] = mapped_column(Integer, default=0)
    units: Mapped[int] = mapped_column(Integer, default=0)


class BrandKitRow(Base):
    """A creator's brand kit (M3.6): settings as JSON (aigcm.studio.brand.BrandKit); files in the jobs folder."""
    __tablename__ = "brand_kits"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    data: Mapped[dict] = mapped_column(JSON, default=dict)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)


class Marker(Base):
    """A moment the creator marked: on the Live screen (wall-clock time), by chat or by voice."""
    __tablename__ = "markers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    live_session_id: Mapped[str | None] = mapped_column(ForeignKey("live_sessions.id", ondelete="CASCADE"))
    stream_id: Mapped[str | None] = mapped_column(ForeignKey("streams.id", ondelete="CASCADE"))
    at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    source: Mapped[str] = mapped_column(String(12), default="button")
    by: Mapped[str | None] = mapped_column(String(100))       # who typed !clip in chat


class TelegramLink(Base):
    __tablename__ = "telegram_links"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    chat_id: Mapped[int | None] = mapped_column(Integer)
    link_token: Mapped[str | None] = mapped_column(String(64), unique=True)
    token_expires_at: Mapped[datetime | None] = mapped_column(DateTime)
    linked_at: Mapped[datetime | None] = mapped_column(DateTime)


class WorkerState(Base):
    """One row the worker keeps fresh, so the app can say when the laptop's worker is not running."""
    __tablename__ = "worker_state"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    heartbeat_at: Mapped[datetime | None] = mapped_column(DateTime)
    stream_id: Mapped[str | None] = mapped_column(String(32))
    pid: Mapped[int | None] = mapped_column(Integer)


class AuditEntry(Base):
    """Who did what, for anything that matters later (sign-ins, uploads, decisions, and in M4 approvals)."""
    __tablename__ = "audit_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True)
    action: Mapped[str] = mapped_column(String(48))
    detail: Mapped[dict] = mapped_column(JSON, default=dict)
    at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
