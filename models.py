


from sqlalchemy import ForeignKey, Integer, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    students: Mapped[list["Student"]] = relationship(
        back_populates="course"
    )


class Student(Base):
    __tablename__ = "students"

    __table_args__ = (
        CheckConstraint(
            "length(trim(name)) >= 2",
            name="check_student_name_length"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False
    )

    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id"),
        nullable=False
    )

    course: Mapped["Course"] = relationship(
        back_populates="students"
    )
