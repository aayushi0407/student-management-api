
from sqlalchemy import select
from sqlalchemy.orm import Session
from models import Student


def create_student(db: Session, data: dict):
    student = Student(**data)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def get_all_students(db: Session):
    statement = select(Student).order_by(Student.id)
    return db.scalars(statement).all()


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
