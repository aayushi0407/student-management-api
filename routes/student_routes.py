

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from schemas import StudentCreate,  StudentUpdate, StudentResponse
from services import student_service

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.post(
    "",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_student(
    data: StudentCreate,
    db: Session = Depends(get_db)
):
    return student_service.create_student(
        db, data.model_dump()
    )


@router.get("", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return student_service.get_all_students(db)


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    return student_service.get_student_by_id(db, student_id)


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    data: StudentUpdate,
    db: Session = Depends(get_db)
):
    return student_service.update_student(
        db,
        student_id,
        data.model_dump()
    )


@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    return student_service.delete_student(db, student_id)
