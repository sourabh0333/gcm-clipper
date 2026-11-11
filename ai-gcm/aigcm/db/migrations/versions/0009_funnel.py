"""stream funnel: upcoming lives, studio checklist, teasers

Revision ID: 0009
Revises: 0008
Create Date: 2026-11-11

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '0009'
down_revision: Union[str, Sequence[str], None] = '0008'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('youtube_channels', schema=None) as batch_op:
        batch_op.add_column(sa.Column('upcoming', sa.JSON(), nullable=True))
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('studio_done', sa.Boolean(), nullable=False, server_default=sa.false()))
        batch_op.add_column(sa.Column('teaser_for', sa.String(length=32), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_column('teaser_for')
        batch_op.drop_column('studio_done')
    with op.batch_alter_table('youtube_channels', schema=None) as batch_op:
        batch_op.drop_column('upcoming')
