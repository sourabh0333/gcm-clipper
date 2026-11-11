"""uploads of recordings that are still growing

Revision ID: 0013
Revises: 0012
Create Date: 2026-11-11

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '0013'
down_revision: Union[str, Sequence[str], None] = '0012'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('uploads', schema=None) as batch_op:
        batch_op.add_column(sa.Column('growing', sa.Boolean(), nullable=False, server_default=sa.false()))


def downgrade() -> None:
    with op.batch_alter_table('uploads', schema=None) as batch_op:
        batch_op.drop_column('growing')
