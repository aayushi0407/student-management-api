

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from repositories import student_repository as repo


def create_student(db: Session, data: dict):
    # Friendly check before inserting
    existing = repo.get_student_by_email(db, data["email"])

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Email is already registered"
        )

    try:
        return repo.create_student(db, data)
    except IntegrityError:
        # Undo the failed transaction
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email is already registered"
        )



def get_all_students(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: str | None = None
):
    return repo.get_all_students(
        db,
        skip=skip,
        limit=limit,
        search=search
    )


def get_student_by_id(db: Session, student_id: int):
    student = repo.get_student_by_id(db, student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


def update_student(db: Session, student_id: int, data: dict):
    student = get_student_by_id(db, student_id)

    existing = repo.get_student_by_email(db, data["email"])

    if existing is not None and existing.id != student_id:
        raise HTTPException(
            status_code=409,
            detail="Email is already registered"
        )

    try:
        return repo.update_student(db, student, data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email is already registered"
        )


def delete_student(db: Session, student_id: int):
    student = get_student_by_id(db, student_id)
    repo.delete_student(db, student)

    return {"message": "Student deleted successfully"}
