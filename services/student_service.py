

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import Course
from repositories import student_repository


def create_student(db: Session, student_data: dict):
    course_id = student_data.get("course_id")

    if db.get(Course, course_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    existing_student = student_repository.get_student_by_email(
        db, student_data["email"]
    )

    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    try:
        return student_repository.create_student(db, student_data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Student could not be created because of a data conflict"
        )


def get_student(db: Session, student_id: int):
    student = student_repository.get_student_by_id(db, student_id)

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return student


def get_all_students(db: Session, skip=0, limit=10, search=None):
    return student_repository.get_all_students(
        db, skip=skip, limit=limit, search=search
    )


def update_student(db: Session, student_id: int, update_data: dict):
    student = student_repository.get_student_by_id(db, student_id)

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update"
        )

    if "course_id" in update_data:
        if db.get(Course, update_data["course_id"]) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )

    if "email" in update_data:
        existing_student = student_repository.get_student_by_email(
            db, update_data["email"]
        )
        if existing_student and existing_student.id != student_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

    try:
        return student_repository.update_student(
            db, student, update_data
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Student could not be updated because of a data conflict"
        )


def delete_student(db: Session, student_id: int):
    student = student_repository.get_student_by_id(db, student_id)

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    student_repository.delete_student(db, student)
