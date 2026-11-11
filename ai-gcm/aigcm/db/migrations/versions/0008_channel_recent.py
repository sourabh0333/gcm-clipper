"""recent uploads per channel, for the Shorts-share gauge

Revision ID: 0008
Revises: 0007
Create Date: 2026-11-11

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '0008'
down_revision: Union[str, Sequence[str], None] = '0007'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('youtube_channels', schema=None) as batch_op:
        batch_op.add_column(sa.Column('recent', sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column('recent_at', sa.DateTime(), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('youtube_channels', schema=None) as batch_op:
        batch_op.drop_column('recent_at')
        batch_op.drop_column('recent')
