"""Add enrollment indexes

Revision ID: 5f2c9d0db9aa
Revises: 7c5a27863f8e
Create Date: 2026-05-09 10:00:00.000000

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "5f2c9d0db9aa"
down_revision: Union[str, Sequence[str], None] = "7c5a27863f8e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        "ix_student_course_course_id", "student_course", ["course_id"], unique=False
    )
    op.create_index(
        "ix_student_course_student_id", "student_course", ["student_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index("ix_student_course_student_id", table_name="student_course")
    op.drop_index("ix_student_course_course_id", table_name="student_course")
