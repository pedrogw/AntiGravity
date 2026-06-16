"""Add current_lat and current_lng to delivery

Revision ID: 2a7f3c9e1d5d
Revises: 17589825805b
Create Date: 2026-06-16 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "2a7f3c9e1d5d"
down_revision: Union[str, None] = "17589825805b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("delivery", sa.Column("current_lat", sa.Float(), nullable=True))
    op.add_column("delivery", sa.Column("current_lng", sa.Float(), nullable=True))


def downgrade() -> None:
    op.drop_column("delivery", "current_lng")
    op.drop_column("delivery", "current_lat")
