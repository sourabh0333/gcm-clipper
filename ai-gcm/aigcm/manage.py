"""Owner commands for the platform database.

    python -m aigcm.manage import-jobs --owner you@gmail.com
    python -m aigcm.manage prepare-kept
    python -m aigcm.manage backfill-library

import-jobs: brings job folders made before the platform existed (the old app and the command line) into
the database under one account, with their clips and the keep or reject decisions in decisions.json.
Folders already in the database are skipped, so it can be run again safely.

prepare-kept: queues the studio's working window for every kept clip that doesn't have one yet (clips kept
before the studio existed), while their streams' recordings are still on the laptop. The worker makes
them. Safe to run again.

backfill-library: fills in what was said in each clip (for the library's search) from the job's transcript,
flags clips with background music (M3.9), and queues posters for every finished stream; the worker makes
the posters. Safe to run again."""

import argparse
import sys

from sqlalchemy import select

from . import db as database
from .db.models import AuditEntry, Clip, Stream, User, new_id, utcnow
from .jobs import STAGES, read_json
from .jobview import failure, finished_clips, spoken_between


def folder_status(manifest):
    stages = manifest.get("stages", {})
    if all(stages.get(s, {}).get("status") == "done" for s in STAGES):
        return "done"
    if any(e.get("status") == "failed" for e in stages.values()):
        return "failed"
    return "stopped"


def import_jobs(session, settings, owner_email):
    """Returns the folder names imported."""
    owner_email = owner_email.strip().lower()
    user = session.scalar(select(User).where(User.email == owner_email))
    if user is None:
        user = User(email=owner_email, is_admin=owner_email in settings.admins)
        session.add(user)
        session.flush()
    known = set(session.scalars(select(Stream.job_dir)))
    imported = []
    for folder in sorted(p for p in settings.jobs_dir.iterdir() if p.is_dir()):
        if folder.name in known or not (folder / "manifest.json").exists():
            continue
        info, saved = read_json(folder / "info.json", {}), read_json(folder / "settings.json", {})
        status = folder_status(read_json(folder / "manifest.json", {}))
        title = info.get("title") or saved.get("source") or folder.name
        stream = Stream(id=new_id("st"), job_dir=folder.name, user_id=user.id, title=str(title)[:300],
                        status=status, duration_s=info.get("duration"), source_name=saved.get("source"),
                        error=failure(folder) if status == "failed" else None, finished_at=utcnow())
        session.add(stream)
        session.flush()
        if status == "done":
            decisions = read_json(folder / "decisions.json", {})
            for item in finished_clips(folder):
                clip = Clip(stream_id=stream.id, **item)
                verdict = decisions.get(item["clip_key"], {})
                if verdict.get("verdict") in ("keep", "reject"):
                    clip.decision, clip.decided_at = verdict["verdict"], utcnow()
                    clip.decision_reason = (verdict.get("reason") or None) and verdict["reason"][:300]
                session.add(clip)
            from .studio.project import queue_posters

            queue_posters(session, stream)
        imported.append(folder.name)
    session.add(AuditEntry(user_id=user.id, action="import_jobs", detail={"folders": imported}))
    session.commit()
    return imported


def backfill_library(session, settings):
    """Spoken text for clips that have none, and posters queued for every finished stream. Returns
    (clips updated, streams queued)."""
    from .studio.project import queue_posters

    updated = queued = 0
    for stream in session.scalars(select(Stream).where(Stream.status == "done")).all():
        transcript = read_json(settings.jobs_dir / stream.job_dir / "transcript.json")
        from .studio import sound

        sounds = sound.job_sounds(settings.jobs_dir / stream.job_dir)
        for clip in stream.clips:
            if clip.spoken is None and transcript:
                clip.spoken = spoken_between(transcript, clip.start_s, clip.end_s)
                updated += clip.spoken is not None
            if sounds:
                music = sound.clip_music(None, clip.start_s, clip.end_s, sounds)
                flags = [f for f in ((clip.details or {}).get("flags") or []) if f.get("kind") != "music"]
                if music >= sound.MUSIC_FLAG_S:
                    flags.append(sound.music_flag(music))
                clip.details = dict(clip.details or {}, flags=flags)
        if stream.clips:
            queue_posters(session, stream)
            queued += 1
    session.commit()
    return updated, queued


def prepare_kept(session, settings):
    """Queue a working window for each kept clip that has none; returns how many were queued."""
    from .studio.project import queue_prepare

    queued = 0
    for clip in session.scalars(select(Clip).where(Clip.decision == "keep")).all():
        if queue_prepare(session, settings, clip) is not None:
            queued += 1
    session.commit()
    return queued


def token_key(env_file):
    """Make the key that encrypts creators' YouTube tokens and add it to .env, once. Never printed: losing it only
    means creators reconnect; changing it does the same, so an existing key is never replaced."""
    from .youtube import new_key

    text = env_file.read_text(encoding="utf-8") if env_file.exists() else ""
    if any(line.strip().startswith("KAATCLIP_TOKEN_KEY=") and line.split("=", 1)[1].strip()
           for line in text.splitlines()):
        return False
    with env_file.open("a", encoding="utf-8", newline="\n") as f:
        f.write(("" if not text or text.endswith("\n") else "\n")
                + "# Encrypts creators' YouTube tokens (M4). Keep it; never share it.\n"
                + f"KAATCLIP_TOKEN_KEY={new_key()}\n")
    return True


def main(argv=None):
    from .api.settings import ApiSettings

    parser = argparse.ArgumentParser(prog="aigcm.manage", description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("import-jobs", help="bring existing job folders into the database under one account")
    p.add_argument("--owner", required=True, help="the Google email of the account that will own them")
    sub.add_parser("prepare-kept", help="queue studio footage for kept clips that have none yet")
    sub.add_parser("backfill-library", help="spoken text and posters for the library, for existing streams")
    sub.add_parser("token-key", help="add the YouTube token key to .env if it has none (never printed)")
    args = parser.parse_args(argv)
    if args.command == "token-key":
        from .config import ROOT
        made = token_key(ROOT / ".env")
        print("token key added to .env" if made else ".env already has a token key; left as it is")
        return 0

    settings = ApiSettings.from_env()
    engine = database.make_engine(settings.db_url)
    database.migrate(engine)
    with database.session_factory(engine)() as session:
        if args.command == "backfill-library":
            updated, queued = backfill_library(session, settings)
            print(f"spoken text for {updated} clips; posters queued for {queued} streams (the worker makes them)")
            return 0
        if args.command == "prepare-kept":
            print(f"queued {prepare_kept(session, settings)} kept clips for the studio; the worker prepares them")
            return 0
        names = import_jobs(session, settings, args.owner)
    print(f"imported {len(names)} job folders" + (": " + ", ".join(names) if names else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
