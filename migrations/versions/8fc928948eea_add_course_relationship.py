
"""add course relationship

Revision ID: 8fc928948eea
Revises:
Create Date: 2026-10-13 16:29:12.353718
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "8fc928948eea"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Remove the old student table because its schema is changing.
    op.drop_table("students")

    # Create the courses table.
    op.create_table(
        "courses",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.UniqueConstraint("name"),
    )

    # Recreate students with a foreign key to courses.
    op.create_table(
        "students",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=150), nullable=False),
        sa.Column("course_id", sa.Integer(), nullable=False),
        sa.CheckConstraint(
            "length(trim(name)) >= 2",
            name="check_student_name_length",
        ),
        sa.ForeignKeyConstraint(["course_id"], ["courses.id"]),
        sa.UniqueConstraint("email"),
    )


def downgrade() -> None:
    op.drop_table("students")
    op.drop_table("courses")

    # Restore the old student table structure.
    op.create_table(
        "students",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=150), nullable=False),
        sa.Column("course", sa.String(length=100), nullable=False),
        sa.CheckConstraint(
            "length(trim(name)) >= 2",
            name="check_student_name_length",
        ),
        sa.CheckConstraint(
            "length(trim(course)) >= 2",
            name="check_student_course_length",
        ),
        sa.UniqueConstraint("email"),
    )
