"""Add grade to student_course

Revision ID: 0c2a7f4ad3bc
Revises: 5f2c9d0db9aa
Create Date: 2026-05-09 12:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0c2a7f4ad3bc"
down_revision: Union[str, Sequence[str], None] = "5f2c9d0db9aa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("student_course", sa.Column("grade", sa.String(length=5), nullable=True))


def downgrade() -> None:
    op.drop_column("student_course", "grade")
