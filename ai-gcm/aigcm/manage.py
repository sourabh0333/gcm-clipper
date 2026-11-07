"""Owner commands for the platform database.

    python -m aigcm.manage import-jobs --owner you@gmail.com

import-jobs: brings job folders made before the platform existed (the old app and the command line) into
the database under one account, with their clips and the keep or reject decisions in decisions.json.
Folders already in the database are skipped, so it can be run again safely."""

import argparse
import sys

from sqlalchemy import select

from . import db as database
from .db.models import AuditEntry, Clip, Stream, User, new_id, utcnow
from .jobs import STAGES, read_json
from .jobview import failure, finished_clips


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
        imported.append(folder.name)
    session.add(AuditEntry(user_id=user.id, action="import_jobs", detail={"folders": imported}))
    session.commit()
    return imported


def main(argv=None):
    from .api.settings import ApiSettings

    parser = argparse.ArgumentParser(prog="aigcm.manage", description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("import-jobs", help="bring existing job folders into the database under one account")
    p.add_argument("--owner", required=True, help="the Google email of the account that will own them")
    args = parser.parse_args(argv)

    settings = ApiSettings.from_env()
    engine = database.make_engine(settings.db_url)
    database.migrate(engine)
    with database.session_factory(engine)() as session:
        names = import_jobs(session, settings, args.owner)
    print(f"imported {len(names)} job folders" + (": " + ", ".join(names) if names else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
