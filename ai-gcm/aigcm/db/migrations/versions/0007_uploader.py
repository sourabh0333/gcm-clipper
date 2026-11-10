"""uploader bookkeeping and quota days

Revision ID: 0007
Revises: 0006
Create Date: 2026-11-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '0007'
down_revision: Union[str, Sequence[str], None] = '0006'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('quota_days',
    sa.Column('day', sa.String(length=10), nullable=False),
    sa.Column('uploads', sa.Integer(), nullable=False),
    sa.Column('units', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('day')
    )
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('upload_url', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('attempts', sa.Integer(), nullable=False, server_default='0'))
        batch_op.add_column(sa.Column('next_try_at', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('thumbnail', sa.String(length=200), nullable=True))
        batch_op.add_column(sa.Column('posted_at', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('checked_at', sa.DateTime(), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('posts', schema=None) as batch_op:
        for name in ('checked_at', 'posted_at', 'thumbnail', 'next_try_at', 'attempts', 'upload_url'):
            batch_op.drop_column(name)
    op.drop_table('quota_days')
