"""live chat listener for !clip markers

Revision ID: 0011
Revises: 0010
Create Date: 2026-11-11

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '0011'
down_revision: Union[str, Sequence[str], None] = '0010'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

COLUMNS = (('channel_id', sa.String(length=32)), ('broadcast_id', sa.String(length=32)),
           ('chat_id', sa.String(length=200)), ('chat_token', sa.String(length=300)),
           ('chat_at', sa.DateTime()), ('chat_note', sa.String(length=200)))


def upgrade() -> None:
    with op.batch_alter_table('live_sessions', schema=None) as batch_op:
        for name, kind in COLUMNS:
            batch_op.add_column(sa.Column(name, kind, nullable=True))
    with op.batch_alter_table('markers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('by', sa.String(length=100), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('markers', schema=None) as batch_op:
        batch_op.drop_column('by')
    with op.batch_alter_table('live_sessions', schema=None) as batch_op:
        for name, _ in reversed(COLUMNS):
            batch_op.drop_column(name)
