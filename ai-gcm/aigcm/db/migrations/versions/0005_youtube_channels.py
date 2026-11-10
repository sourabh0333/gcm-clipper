"""youtube channels

Revision ID: 0005
Revises: 0004
Create Date: 2026-11-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '0005'
down_revision: Union[str, Sequence[str], None] = '0004'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('youtube_channels',
    sa.Column('id', sa.String(length=32), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('channel_id', sa.String(length=64), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('thumbnail', sa.String(length=500), nullable=True),
    sa.Column('scopes', sa.Text(), nullable=False),
    sa.Column('refresh_token', sa.Text(), nullable=False),
    sa.Column('status', sa.String(length=12), nullable=False),
    sa.Column('settings', sa.JSON(), nullable=False),
    sa.Column('connected_at', sa.DateTime(), nullable=False),
    sa.Column('checked_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'channel_id')
    )
    with op.batch_alter_table('youtube_channels', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_youtube_channels_user_id'), ['user_id'], unique=False)


def downgrade() -> None:
    with op.batch_alter_table('youtube_channels', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_youtube_channels_user_id'))
    op.drop_table('youtube_channels')
