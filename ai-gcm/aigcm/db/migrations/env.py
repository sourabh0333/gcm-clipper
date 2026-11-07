"""Alembic environment. The connection comes from aigcm.db.migrate(); batch mode lets later migrations
alter SQLite tables (SQLite can't drop or change columns in place)."""

from alembic import context

from aigcm.db.models import Base

connection = context.config.attributes.get("connection")
if connection is None:
    raise RuntimeError("Run migrations through aigcm.db.migrate(engine).")

context.configure(connection=connection, target_metadata=Base.metadata, render_as_batch=True,
                  compare_type=True)
with context.begin_transaction():
    context.run_migrations()
