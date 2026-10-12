
from sqlalchemy import select,func
from sqlalchemy.orm import Session
from models import Student


def create_student(db: Session, data: dict):
    student = Student(**data)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student




def get_all_students(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: str | None = None
):
    statement = select(Student)

    # Apply search filter
    if search and search.strip():
        search_term = f"%{search.strip()}%"
        statement = statement.where(
            Student.name.ilike(search_term)
            | Student.course.ilike(search_term)
        )

    # 1. Calculate total matching students
    count_statement = select(func.count()).select_from(
        statement.subquery()
    )
    total = db.scalar(count_statement)

    # 2. Fetch the requested page
    statement = (
        statement
        .order_by(Student.id)
        .offset(skip)
        .limit(limit)
    )
    students = db.scalars(statement).all()

    # 3. Return all response fields
    return {
        "total": total or 0,
        "skip": skip,
        "limit": limit,
        "students": students
    }




def get_student_by_id(db: Session, student_id: int):
    return db.get(Student, student_id)


def get_student_by_email(db: Session, email: str):
    statement = select(Student).where(Student.email == email)
    return db.scalar(statement)


def update_student(db: Session, student: Student, data: dict):
    for key, value in data.items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)
    return student


def delete_student(db: Session, student: Student):
    db.delete(student)
    db.commit()
