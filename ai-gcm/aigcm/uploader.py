"""The uploader (M4.3): sends approved posts to YouTube from the worker's posting lane.

Only what the creator approved goes up: `post.approval` (title, description, tags, privacy, publish time, the two
answers), and only after `posting.approved()` passes and the video file still has the approved SHA-256. A
scheduled post is uploaded private with `publishAt`, so YouTube itself makes it public at the planned minute
(the laptop can be off by then). The upload is YouTube's resumable protocol in 8 MB pieces; the session address
is kept on the post, so a dropped connection or a restart carries on from the last piece. Afterwards the
uploader reads the video back (privacy must be what was approved, P-R2), sets the cover as thumbnail once
YouTube has processed it (P-R7), and confirms the scheduled post went public. Quota is counted per Pacific-time
day: the uploads bucket (100 a day) and the 10,000 shared units (P-R1). See plans/M4 Plan and post plan.md.

Each step reads and writes the database in short transactions and talks to YouTube with none open."""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import httpx
from sqlalchemy import select, update

from . import posting
from . import youtube as yt
from .db.models import AuditEntry, Post, QuotaDay, Render, YouTubeChannel, utcnow
from .jobs import log

UPLOAD_URL = "https://www.googleapis.com/upload/youtube/v3/videos"
THUMB_URL = "https://www.googleapis.com/upload/youtube/v3/thumbnails/set"
CHUNK = 8 * 1024 * 1024            # a multiple of 256 KiB, as YouTube asks
UPLOADS_PER_DAY = 100
UNITS_PER_DAY = 10_000
UNITS = {"list": 1, "thumbnail": 50}
NEEDS_VERIFY = "not set: verify the channel"   # the post page explains: youtube.com/verify, then Set cover again
MISSED = timedelta(minutes=2)       # a scheduled time this close when a new upload starts has been missed
BACKOFF_S = [60, 120, 300, 600, 1800]
CHECK_EVERY = timedelta(minutes=1)
PROCESSING_LIMIT = timedelta(hours=2)
LATE_LIMIT = timedelta(hours=2)
PACIFIC = ZoneInfo("America/Los_Angeles")
INDIA = ZoneInfo("Asia/Kolkata")


class Retry(Exception):
    """Try again later: the network, or YouTube busy."""


class Wait(Exception):
    """Try again after `until` (UTC): YouTube's daily limit."""

    def __init__(self, message, until):
        super().__init__(message)
        self.until = until


class Fail(Exception):
    """Give up and tell the creator, in plain words."""


# --- quota ---------------------------------------------------------------------------------------------------

def quota_day(now=None):
    moment = (now or utcnow()).replace(tzinfo=ZoneInfo("UTC"))
    return moment.astimezone(PACIFIC).date().isoformat()


def next_quota_day(now=None):
    """The next Pacific midnight (when Google resets the quota), plus 5 minutes, as naive UTC."""
    moment = (now or utcnow()).replace(tzinfo=ZoneInfo("UTC")).astimezone(PACIFIC)
    midnight = datetime.combine(moment.date() + timedelta(days=1), datetime.min.time(), PACIFIC)
    return (midnight + timedelta(minutes=5)).astimezone(ZoneInfo("UTC")).replace(tzinfo=None)


def spend(db, uploads=0, units=0, now=None):
    day = quota_day(now)
    row = db.get(QuotaDay, day)
    if row is None:
        row = QuotaDay(day=day, uploads=0, units=0)
        db.add(row)
    row.uploads += uploads
    row.units += units
    return row


def usage(db, now=None):
    row = db.get(QuotaDay, quota_day(now))
    return {"uploads": row.uploads if row else 0, "uploads_limit": UPLOADS_PER_DAY,
            "units": row.units if row else 0, "units_limit": UNITS_PER_DAY}


# --- talking to YouTube --------------------------------------------------------------------------------------

def reason_of(response):
    try:
        error = response.json().get("error") or {}
    except ValueError:
        return None, response.text[:200]
    errors = error.get("errors") or [{}]
    return errors[0].get("reason"), error.get("message") or ""


def refuse(response, what):
    """Turn a YouTube error answer into Retry, Wait or Fail."""
    if response.status_code >= 500 or response.status_code == 429:
        raise Retry(f"YouTube was busy ({response.status_code})")
    reason, message = reason_of(response)
    if response.status_code == 401:
        raise yt.Expired("The YouTube connection has expired. Reconnect the channel.")
    if reason in ("rateLimitExceeded", "userRateLimitExceeded", "backendError"):
        raise Retry(f"YouTube asked to slow down ({reason})")
    if reason in ("quotaExceeded", "uploadLimitExceeded", "dailyLimitExceeded"):
        raise Wait("YouTube's daily upload limit is used up; it uploads after the limit resets.", next_quota_day())
    raise Fail(f"YouTube refused the {what}: {message or reason or response.status_code}")


def metadata(approval):
    status = {"privacyStatus": approval["privacy"], "selfDeclaredMadeForKids": bool(approval["made_for_kids"]),
              "containsSyntheticMedia": bool(approval["synthetic"]), "embeddable": True}
    if approval.get("publish_at"):
        status["publishAt"] = approval["publish_at"]
    snippet = {"title": approval["title"], "description": approval["description"], "tags": approval["tags"],
               "categoryId": approval.get("category") or "20"}
    return {"snippet": snippet, "status": status}


def start_session(http, token, approval, size):
    response = http.post(UPLOAD_URL, params={"uploadType": "resumable", "part": "snippet,status"},
                         headers={"Authorization": f"Bearer {token}", "X-Upload-Content-Length": str(size),
                                  "X-Upload-Content-Type": "video/mp4"},
                         json=metadata(approval))
    if response.status_code == 200 and response.headers.get("location"):
        return response.headers["location"]
    refuse(response, "upload")


def _next_offset(response):
    got = response.headers.get("range")      # "bytes=0-1048575": what YouTube has so far
    return int(got.rsplit("-", 1)[1]) + 1 if got else 0


def resume_point(http, url, size):
    """("at", offset) to carry on, ("done", video) if YouTube already has it all, or None if the session is gone."""
    response = http.put(url, headers={"Content-Range": f"bytes */{size}", "Content-Length": "0"})
    if response.status_code == 308:
        return "at", _next_offset(response)
    if response.status_code in (200, 201):
        return "done", response.json()
    if response.status_code in (404, 410):
        return None
    refuse(response, "upload")


def send(http, url, path, size, offset, chunk=CHUNK):
    """Send the file from `offset` in pieces. Returns YouTube's video resource."""
    with open(path, "rb") as f:
        while True:
            f.seek(offset)
            data = f.read(chunk)
            end = offset + len(data) - 1
            response = http.put(url, content=data, headers={"Content-Range": f"bytes {offset}-{end}/{size}",
                                                            "Content-Type": "video/mp4"}, timeout=180)
            if response.status_code in (200, 201):
                return response.json()
            if response.status_code != 308:
                if response.status_code in (404, 410):
                    raise Retry("YouTube's upload session ended; starting it again")
                refuse(response, "upload")
            offset = _next_offset(response)


def read_back(http, token, video_id):
    response = http.get(f"{yt.API}/videos", params={"part": "status,processingDetails", "id": video_id},
                        headers={"Authorization": f"Bearer {token}"})
    if response.status_code != 200:
        refuse(response, "check")
    items = response.json().get("items") or []
    return items[0] if items else None


def set_thumbnail(http, token, video_id, jpeg_path):
    response = http.post(THUMB_URL, params={"videoId": video_id}, content=jpeg_path.read_bytes(),
                         headers={"Authorization": f"Bearer {token}", "Content-Type": "image/jpeg"})
    if response.status_code == 200:
        return "set"
    reason, message = reason_of(response)
    if response.status_code == 403 and "permission" in (message or "").lower():
        # YouTube allows custom covers only on verified channels (phone verification, free).
        return NEEDS_VERIFY
    return f"not set: {message or reason or response.status_code}"[:200]


# --- the lane ------------------------------------------------------------------------------------------------

def claim(db, now=None):
    """The next approved post due for upload, marked uploading. A post whose approval no longer matches it is
    failed here, never uploaded."""
    now = now or utcnow()
    for post in db.scalars(select(Post).where(Post.status == "approved")
                           .where((Post.next_try_at.is_(None)) | (Post.next_try_at <= now))
                           .order_by(Post.approved_at).limit(5)).all():
        if not posting.approved(post):
            post.status, post.error = "failed", "The approval doesn't match the post any more. Approve it again."
            db.commit()
            continue
        taken = db.execute(update(Post).where(Post.id == post.id, Post.status == "approved")
                           .values(status="uploading", updated_at=now)).rowcount
        db.commit()
        if taken:
            return post.id
    return None


def requeue(db):
    """Posts left uploading by a crash or restart go back to approved; their session is kept, so they resume."""
    count = db.execute(update(Post).where(Post.status == "uploading").values(status="approved")).rowcount
    db.commit()
    return count


def _parse(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).replace(tzinfo=None) if iso else None


def _token(http, settings, sessions, channel_id):
    with sessions() as db:
        channel = db.get(YouTubeChannel, channel_id)
        if channel is None:
            raise Fail("The channel was disconnected. Connect it again and make a new post.")
        if channel.status != "ok":
            raise Fail(f"Reconnect {channel.title} in Settings, then make the post again.")
        sealed = channel.refresh_token
    try:
        return yt.access_token(http, settings, yt.unseal(settings.token_key, sealed))
    except yt.Expired:
        with sessions() as db:
            channel = db.get(YouTubeChannel, channel_id)
            if channel is not None:
                channel.status, channel.checked_at = "expired", utcnow()
                db.commit()
        raise


def upload(settings, sessions, http, post_id, notify=None, chunk=CHUNK, now=None):
    """Upload one claimed post. Returns the event: scheduled, posted, waiting, retrying or failed."""
    from .studio import lane

    now = now or utcnow()
    with sessions() as db:
        post = db.get(Post, post_id)
        approval, url = dict(post.approval), post.upload_url
        clip, render = post.clip, db.get(Render, post.render_id) if post.render_id else None
        video = lane.render_file(settings, db, render, clip)
        limit = usage(db, now)
    try:
        if video is None:
            raise Fail("The exported video is gone. Export the clip again and make a new post.")
        if posting.file_hash(video) != approval["video_sha256"]:
            raise Fail("The video changed after it was approved. Make a new post from the export.")
        if url is None:
            publish_at = _parse(approval.get("publish_at"))
            if publish_at is not None and publish_at <= now + MISSED:
                raise Fail("It missed its time (the laptop wasn't uploading then). Make a new post with a new time.")
            if limit["uploads"] >= UPLOADS_PER_DAY:
                raise Wait("YouTube's daily upload limit is used up; it uploads after the limit resets.",
                           next_quota_day(now))
        token = _token(http, settings, sessions, approval["channel"]["id"])
        size = video.stat().st_size
        result = None
        if url:
            point = resume_point(http, url, size)
            if point is None:
                url = None
            elif point[0] == "done":
                result = point[1]
            else:
                result = send(http, url, video, size, point[1], chunk)
        if result is None and url is None:
            url = start_session(http, token, approval, size)
            with sessions() as db:
                db.get(Post, post_id).upload_url = url
                spend(db, uploads=1, now=now)
                db.commit()
            result = send(http, url, video, size, 0, chunk)
        video_id = result["id"]
        with sessions() as db:
            post = db.get(Post, post_id)
            post.video_id, post.upload_url = video_id, None
            db.commit()
        item = read_back(http, token, video_id)
        with sessions() as db:
            spend(db, units=UNITS["list"], now=now)
            db.commit()
        status = (item or {}).get("status") or {}
        if status.get("uploadStatus") in ("rejected", "failed"):
            raise Fail(f"YouTube {status['uploadStatus']} the video "
                       f"({status.get('rejectionReason') or status.get('failureReason') or 'no reason given'}).")
        if status.get("privacyStatus") != approval["privacy"] or (approval.get("publish_at") and not status.get("publishAt")):
            raise Fail(f"YouTube set it to {status.get('privacyStatus', 'unknown')} instead of {approval['privacy']}"
                       f"{' with a publish time' if approval.get('publish_at') else ''}. Check it in YouTube Studio.")
        event = "scheduled" if approval["privacy"] == "private" else "posted"
        with sessions() as db:
            post = db.get(Post, post_id)
            post.status, post.error, post.checked_at, post.updated_at = event, None, now, now
            if event == "posted":
                post.posted_at = now
            db.add(AuditEntry(user_id=post.user_id, action="post_uploaded",
                              detail={"post": post.id, "video": video_id, "privacy": approval["privacy"],
                                      "publish_at": approval.get("publish_at")}))
            db.commit()
        log(f"uploader: {post_id} uploaded as {video_id} ({event})")
    except Wait as exc:
        return _later(sessions, post_id, str(exc), exc.until, notify, count=False)
    except (Retry, httpx.TransportError) as exc:
        return _later(sessions, post_id, f"Upload interrupted ({exc}); trying again.", None, notify)
    except (Fail, yt.YouTubeError) as exc:
        return _fail(sessions, post_id, str(exc), notify)
    except Exception as exc:  # anything unexpected: keep the post, try again later
        log(f"uploader: {post_id} hit {exc!r}")
        return _later(sessions, post_id, "Something went wrong on the laptop; trying again.", None, notify)
    if notify:
        notify(post_id, event)
    return event


def _later(sessions, post_id, message, until, notify, count=True):
    with sessions() as db:
        post = db.get(Post, post_id)
        if count:
            post.attempts += 1
            if post.attempts > len(BACKOFF_S):
                db.commit()
                return _fail(sessions, post_id, f"The upload kept failing. {message}", notify)
            until = utcnow() + timedelta(seconds=BACKOFF_S[post.attempts - 1])
        post.status, post.next_try_at, post.error = "approved", until, message
        db.commit()
    log(f"uploader: {post_id} waits until {until:%Y-%m-%d %H:%M} UTC: {message}")
    return "waiting" if not count else "retrying"


def _fail(sessions, post_id, message, notify):
    with sessions() as db:
        post = db.get(Post, post_id)
        post.status, post.error, post.upload_url, post.updated_at = "failed", message, None, utcnow()
        db.add(AuditEntry(user_id=post.user_id, action="post_failed", detail={"post": post.id, "error": message}))
        db.commit()
    log(f"uploader: {post_id} failed: {message}")
    if notify:
        notify(post_id, "failed")
    return "failed"


def due_check(db, now=None):
    """A post on YouTube that needs a look: its thumbnail once processed, or a scheduled one past its time."""
    now = now or utcnow()
    rows = db.scalars(select(Post).where(Post.video_id.is_not(None), Post.status.in_(("scheduled", "posted")))
                      .where((Post.checked_at.is_(None)) | (Post.checked_at <= now - CHECK_EVERY))
                      .order_by(Post.checked_at)).all()
    for post in rows:
        if post.thumbnail is None or (post.status == "scheduled" and post.publish_at and post.publish_at <= now):
            return post.id
    return None


def check(settings, sessions, http, post_id, notify=None, now=None):
    """Look at one uploaded post: set the thumbnail once YouTube has processed the video, and confirm a scheduled
    post went public. Returns the event: posted, failed, thumbnail or None."""
    from .studio import lane

    now = now or utcnow()
    with sessions() as db:
        post = db.get(Post, post_id)
        video_id, channel_id = post.video_id, post.channel_id or (post.approval or {}).get("channel", {}).get("id")
        render = db.get(Render, post.render_id) if post.render_id else None
        video = lane.render_file(settings, db, render, post.clip)
        status, publish_at, approved_at, thumbnail = post.status, post.publish_at, post.approved_at, post.thumbnail
        post.checked_at = now
        db.commit()
    event = None
    try:
        token = _token(http, settings, sessions, channel_id)
        item = read_back(http, token, video_id)
        with sessions() as db:
            spend(db, units=UNITS["list"], now=now)
            db.commit()
        if item is None:
            return _fail(sessions, post_id, "The video is no longer on YouTube.", notify)
        state = item.get("status") or {}
        processing = (item.get("processingDetails") or {}).get("processingStatus")
        if state.get("uploadStatus") in ("rejected", "failed"):
            return _fail(sessions, post_id, f"YouTube {state['uploadStatus']} the video "
                                            f"({state.get('rejectionReason') or state.get('failureReason') or 'no reason given'}).",
                         notify)
        changes = {}
        if thumbnail is None:
            if state.get("uploadStatus") == "processed" or processing == "succeeded":
                cover = lane.cover_path(video) if video else None
                if cover is not None and cover.is_file():
                    changes["thumbnail"] = set_thumbnail(http, token, video_id, cover)
                    with sessions() as db:
                        spend(db, units=UNITS["thumbnail"], now=now)
                        db.commit()
                    event = "thumbnail"
                else:
                    changes["thumbnail"] = "no cover image"
            elif approved_at and now - approved_at > PROCESSING_LIMIT:
                changes["thumbnail"] = "not set: YouTube was still processing the video"
        if status == "scheduled" and publish_at and publish_at <= now:
            moved = _parse(state.get("publishAt"))
            if state.get("privacyStatus") == "public":
                # YouTube made it public at its time; the laptop may only be looking now (it was off).
                changes.update(status="posted", posted_at=min(now, moved or publish_at))
                event = "posted"
            elif moved is not None and moved > now:
                changes["publish_at"] = moved          # the creator moved it in YouTube Studio: follow YouTube
            elif state.get("privacyStatus") == "private" and moved is None:
                return _fail(sessions, post_id, "Its schedule was removed in YouTube Studio, so it stays private.",
                             notify)
            elif now - publish_at > LATE_LIMIT:
                return _fail(sessions, post_id, "YouTube didn't make it public at the planned time. Check it in "
                                                "YouTube Studio.", notify)
        with sessions() as db:
            post = db.get(Post, post_id)
            for key, value in changes.items():
                setattr(post, key, value)
            if changes:
                post.updated_at = now
            db.commit()
    except (Retry, Wait, httpx.TransportError) as exc:
        log(f"uploader: checking {post_id} later: {exc}")
        return None
    except (Fail, yt.YouTubeError) as exc:
        log(f"uploader: can't check {post_id}: {exc}")
        return None
    if event == "posted" and notify:
        notify(post_id, "live")
    return event


def step(settings, sessions, http, notify=None):
    """One unit of the posting lane's work. Returns what it did, or None when there was nothing to do."""
    with sessions() as db:
        post_id = claim(db)
    if post_id:
        return upload(settings, sessions, http, post_id, notify)
    with sessions() as db:
        post_id = due_check(db)
    if post_id:
        return check(settings, sessions, http, post_id, notify) or "checked"
    return None


def when_india(value):
    """'Tue 11 Nov, 7:00 pm' in India time, for messages."""
    if value is None:
        return ""
    local = value.replace(tzinfo=ZoneInfo("UTC")).astimezone(INDIA)
    return local.strftime("%a %d %b, %I:%M %p").replace(" 0", " ").replace("AM", "am").replace("PM", "pm")
