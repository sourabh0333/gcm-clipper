"""studio edits and renders

Revision ID: 0002
Revises: 0001
Create Date: 2026-11-09

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '0002'
down_revision: Union[str, Sequence[str], None] = '0001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('edits',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('clip_id', sa.Integer(), nullable=False),
    sa.Column('version', sa.Integer(), nullable=False),
    sa.Column('data', sa.JSON(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['clip_id'], ['clips.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('clip_id', 'version')
    )
    with op.batch_alter_table('edits', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_edits_clip_id'), ['clip_id'], unique=False)

    op.create_table('renders',
    sa.Column('id', sa.String(length=32), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('clip_id', sa.Integer(), nullable=True),
    sa.Column('kind', sa.String(length=16), nullable=False),
    sa.Column('status', sa.String(length=12), nullable=False),
    sa.Column('params', sa.JSON(), nullable=False),
    sa.Column('output', sa.String(length=200), nullable=True),
    sa.Column('error', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('started_at', sa.DateTime(), nullable=True),
    sa.Column('finished_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['clip_id'], ['clips.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('renders', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_renders_clip_id'), ['clip_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_renders_status'), ['status'], unique=False)
        batch_op.create_index(batch_op.f('ix_renders_user_id'), ['user_id'], unique=False)


def downgrade() -> None:
    with op.batch_alter_table('renders', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_renders_user_id'))
        batch_op.drop_index(batch_op.f('ix_renders_status'))
        batch_op.drop_index(batch_op.f('ix_renders_clip_id'))
    op.drop_table('renders')
    with op.batch_alter_table('edits', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_edits_clip_id'))
    op.drop_table('edits')
