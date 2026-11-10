"""posts and stream links

Revision ID: 0006
Revises: 0005
Create Date: 2026-11-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '0006'
down_revision: Union[str, Sequence[str], None] = '0005'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',
    sa.Column('id', sa.String(length=32), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('clip_id', sa.Integer(), nullable=True),
    sa.Column('render_id', sa.String(length=32), nullable=True),
    sa.Column('channel_id', sa.String(length=32), nullable=True),
    sa.Column('kind', sa.String(length=8), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('tags', sa.JSON(), nullable=False),
    sa.Column('mode', sa.String(length=8), nullable=False),
    sa.Column('publish_at', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(length=12), nullable=False),
    sa.Column('approval', sa.JSON(), nullable=True),
    sa.Column('approved_at', sa.DateTime(), nullable=True),
    sa.Column('video_id', sa.String(length=32), nullable=True),
    sa.Column('error', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['channel_id'], ['youtube_channels.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['clip_id'], ['clips.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['render_id'], ['renders.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_posts_user_id'), ['user_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_posts_clip_id'), ['clip_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_posts_status'), ['status'], unique=False)
    with op.batch_alter_table('streams', schema=None) as batch_op:
        batch_op.add_column(sa.Column('link', sa.String(length=200), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('streams', schema=None) as batch_op:
        batch_op.drop_column('link')
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_posts_status'))
        batch_op.drop_index(batch_op.f('ix_posts_clip_id'))
        batch_op.drop_index(batch_op.f('ix_posts_user_id'))
    op.drop_table('posts')
