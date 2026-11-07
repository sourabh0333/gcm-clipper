import subprocess
import sys

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import inspect, text

from aigcm import db
from aigcm.api import create_app
from aigcm.api.settings import ApiSettings
from aigcm.db.models import Stream, User


@pytest.fixture
def settings(tmp_path):
    return ApiSettings(db_url=db.sqlite_url(tmp_path / "test.db"), jobs_dir=tmp_path / "jobs")


def test_the_migration_creates_every_table(settings):
    app = create_app(settings)
    tables = set(inspect(app.state.engine).get_table_names())
    assert {"users", "sessions", "invites", "streams", "uploads", "clips", "live_sessions", "markers",
            "telegram_links", "worker_state", "audit_log", "alembic_version"} <= tables
    # Running it again on the same file is a no-op.
    create_app(settings)


def test_sqlite_runs_in_wal_mode_with_foreign_keys(settings):
    app = create_app(settings)
    with app.state.engine.connect() as connection:
        assert connection.execute(text("PRAGMA journal_mode")).scalar() == "wal"
        assert connection.execute(text("PRAGMA foreign_keys")).scalar() == 1


def test_health_answers(settings):
    client = TestClient(create_app(settings))
    response = client.get("/api/health")
    assert response.status_code == 200 and response.json()["ok"] is True


def test_rows_round_trip_and_deleting_a_user_removes_their_streams(settings):
    app = create_app(settings)
    with app.state.sessions() as s:
        user = User(email="a@example.com")
        s.add(user)
        s.flush()
        s.add(Stream(user_id=user.id, title="Rank push", job_dir="st_test"))
        s.commit()
        stream = s.query(Stream).one()
        assert stream.id.startswith("st_") and stream.status == "uploading" and stream.game == "bgmi"
        s.delete(user)
        s.commit()
        assert s.query(Stream).count() == 0


def test_two_connections_can_write_one_after_the_other(settings):
    # The API and the worker are separate processes; BEGIN IMMEDIATE makes the second writer wait instead
    # of failing.
    app = create_app(settings)
    other = db.make_engine(settings.db_url)
    with app.state.sessions() as a, db.session_factory(other)() as b:
        a.add(User(email="one@example.com"))
        a.commit()
        b.add(User(email="two@example.com"))
        b.commit()
        assert a.query(User).count() == 2


def test_the_api_package_imports_no_engine_code():
    # The phone session has no engine models; the API must start without them (plan R13).
    code = ("import sys, aigcm.api, aigcm.db; "
            "heavy = [m for m in ('numpy', 'aigcm.vision', 'aigcm.transcript', 'rapidocr_onnxruntime', "
            "'faster_whisper', 'mediapipe') if m in sys.modules]; print(heavy)")
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True).stdout
    assert out.strip() == "[]"


def test_a_long_read_never_blocks_a_writer(settings):
    # A GET that streams a video keeps its read transaction open; writes must still go through at once
    # (found in the M2.6 browser check: a playing clip blocked every keep and reject for 15 s).
    import time
    app = create_app(settings)
    reader = app.state.sessions()
    reader.connection(execution_options={"readonly": True})
    reader.query(User).count()            # holds a read transaction open
    started = time.time()
    with app.state.sessions() as writer:
        writer.add(User(email="w@example.com"))
        writer.commit()
    assert time.time() - started < 2
    reader.close()


def test_a_write_waits_for_another_write_instead_of_failing(settings):
    import threading
    import time
    app = create_app(settings)
    first = app.state.sessions()
    first.add(User(email="first@example.com"))
    first.flush()                          # holds the write lock
    done = []

    def second():
        with app.state.sessions() as s:
            s.add(User(email="second@example.com"))
            s.commit()
            done.append(time.time())

    thread = threading.Thread(target=second)
    thread.start()
    time.sleep(0.5)
    released = time.time()
    first.commit()
    thread.join(timeout=10)
    assert done and done[0] >= released
