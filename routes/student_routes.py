
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from database import get_db
from schemas import StudentCreate, StudentUpdate, StudentResponse, StudentListResponse
from services import student_service

router = APIRouter(prefix="/students", tags=["Students"])


@router.post(
    "/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db)
):
    return student_service.create_student(
        db, student_data.model_dump()
    )


@router.get("/", response_model=StudentListResponse)
def get_all_students(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    search: str | None = None,
    db: Session = Depends(get_db)
):
    return student_service.get_all_students(
        db, skip=skip, limit=limit, search=search
    )


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    return student_service.get_student(db, student_id)


@router.patch("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    update_data: StudentUpdate,
    db: Session = Depends(get_db)
):
    return student_service.update_student(
        db,
        student_id,
        update_data.model_dump(exclude_unset=True)
    )


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student_service.delete_student(db, student_id)


