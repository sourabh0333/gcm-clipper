"""The copy of each channel's YouTube data that Kaatclip keeps (M4.4-M4.6): recent uploads with their views,
scheduled lives, and 28 days of Analytics by content type. Refreshed while the creator uses the calendar or the
streams page, and never kept past 30 days: the worker's daily job deletes anything older and re-checks every 30
days that the creator's permission still works (Developer Policies III.E.4, M4 review P-R6)."""

from datetime import timedelta

from . import youtube as yt
from .db.models import YouTubeChannel, utcnow
from .jobs import log

RECENT_DAYS = 28
RECENT_EVERY = timedelta(hours=6)
STATS_EVERY = timedelta(hours=12)
KEEP = timedelta(days=30)


def _spend(db, units):
    from .uploader import spend

    spend(db, units=units)


def token_for(settings, http, channel):
    return yt.access_token(http, settings, yt.unseal(settings.token_key, channel.refresh_token))


def forget(channel):
    """Delete the cached YouTube data (the channel's name and picture stay: they are shown to the creator)."""
    channel.recent = channel.recent_at = channel.upcoming = channel.stats = channel.stats_at = None


def refresh(db, settings, http, channel, now=None, stats=False):
    """Re-read what is stale: uploads and lives every 6 hours, Analytics every 12 (only when `stats`). Problems
    leave the old copy; an expired connection marks the channel and deletes the copy. Commits."""
    now = now or utcnow()
    due_recent = channel.recent_at is None or now - channel.recent_at >= RECENT_EVERY
    due_stats = stats and (channel.stats_at is None or now - channel.stats_at >= STATS_EVERY)
    if channel.status != "ok" or not (due_recent or due_stats):
        return False
    try:
        token = token_for(settings, http, channel)
        if due_recent:
            items, units = yt.recent_uploads(http, token, now - timedelta(days=RECENT_DAYS))
            try:
                upcoming = yt.upcoming_streams(http, token)
                units += 1
            except yt.YouTubeError:
                upcoming = channel.upcoming
            _spend(db, units)
            channel.recent, channel.recent_at, channel.upcoming = items, now, upcoming
        if due_stats:
            end = now.date()
            channel.stats = yt.channel_report(http, token, end - timedelta(days=RECENT_DAYS), end)
            channel.stats_at = now
        channel.checked_at = now
    except yt.Expired:
        channel.status = "expired"
        forget(channel)
    except Exception as exc:   # nice-to-have numbers: never break the page over them
        log(f"channel data: {channel.id}: {exc}")
    db.commit()
    return True


def retention(db, settings, http, now=None):
    """The daily 30-day job: delete cached data older than 30 days; every 30 days make sure the creator's
    permission still works, and if not, mark the channel expired and delete its cached data."""
    now = now or utcnow()
    forgotten = checked = expired = 0
    from sqlalchemy import select

    for channel in db.scalars(select(YouTubeChannel)).all():
        if channel.recent_at and now - channel.recent_at > KEEP:
            channel.recent = channel.recent_at = channel.upcoming = None
            forgotten += 1
        if channel.stats_at and now - channel.stats_at > KEEP:
            channel.stats = channel.stats_at = None
            forgotten += 1
        if channel.status == "ok" and settings.token_key and now - channel.checked_at > KEEP:
            try:
                token_for(settings, http, channel)
                channel.checked_at = now
                checked += 1
            except yt.Expired:
                channel.status = "expired"
                forget(channel)
                expired += 1
            except Exception as exc:
                log(f"channel data: can't check {channel.id}: {exc}")
    db.commit()
    return {"forgotten": forgotten, "checked": checked, "expired": expired}
