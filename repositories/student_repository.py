

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, selectinload

from models import Student


def create_student(db: Session, student_data: dict):
    student = Student(**student_data)
    db.add(student)
    db.commit()
    db.refresh(student)

    return student


def get_student_by_id(db: Session, student_id: int):
    statement = (
        select(Student)
        .options(selectinload(Student.course))
        .where(Student.id == student_id)
    )
    return db.scalar(statement)


def get_student_by_email(db: Session, email: str):
    statement = select(Student).where(Student.email == email)
    return db.scalar(statement)


def get_all_students(db: Session, skip=0, limit=10, search=None):
    statement = select(Student).options(selectinload(Student.course))

    if search and search.strip():
        search_term = f"%{search.strip()}%"
        statement = (
            statement.join(Student.course)
            .where(
                or_(
                    Student.name.ilike(search_term),
                    Student.course.has(name=search.strip()),
                    Student.email.ilike(search_term),
                )
            )
        )

    count_statement = select(func.count()).select_from(
        statement.order_by(None).subquery()
    )
    total = db.scalar(count_statement) or 0

    statement = statement.order_by(Student.id).offset(skip).limit(limit)
    students = db.scalars(statement).unique().all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "students": students,
    }


def update_student(db: Session, student, update_data: dict):
    for key, value in update_data.items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)

    return student


def delete_student(db: Session, student):
    db.delete(student)
    db.commit()
