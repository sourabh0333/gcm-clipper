"""Database access for the API and the worker: one SQLite file (Postgres later), created and upgraded by the
Alembic migrations in db/migrations, so nobody has to run a setup step.

Two processes write the same SQLite file (the API and the worker), so every connection uses WAL mode and
a 15 s busy timeout, and every transaction starts with BEGIN IMMEDIATE: it takes the write lock up front
instead of failing with "database is locked" when a read has to become a write half way through."""

from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

MIGRATIONS = Path(__file__).resolve().parent / "migrations"


def make_engine(url):
    if url.startswith("sqlite:///"):
        Path(url.removeprefix("sqlite:///")).parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(url, connect_args={"timeout": 15} if url.startswith("sqlite") else {})
    if url.startswith("sqlite"):
        @event.listens_for(engine, "connect")
        def _pragmas(dbapi_connection, _record):
            # Let SQLAlchemy's "begin" event issue BEGIN, instead of the sqlite3 module's own deferred BEGIN.
            dbapi_connection.isolation_level = None
            cursor = dbapi_connection.cursor()
            for pragma in ("journal_mode=WAL", "synchronous=NORMAL", "foreign_keys=ON", "busy_timeout=15000"):
                cursor.execute(f"PRAGMA {pragma}")
            cursor.close()

        @event.listens_for(engine, "begin")
        def _begin(connection):
            connection.exec_driver_sql("BEGIN IMMEDIATE")
    return engine


def migrate(engine):
    """Bring the database to the newest schema."""
    from alembic import command
    from alembic.config import Config

    config = Config()
    config.set_main_option("script_location", str(MIGRATIONS))
    with engine.begin() as connection:
        config.attributes["connection"] = connection
        command.upgrade(config, "head")


def session_factory(engine):
    return sessionmaker(engine, expire_on_commit=False)


def sqlite_url(path):
    return f"sqlite:///{Path(path).resolve().as_posix()}"
