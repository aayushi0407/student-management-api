
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import get_db
from models import Course
from schemas import CourseCreate, CourseResponse

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.post(
    "/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED
)
def create_course(
    course_data: CourseCreate,
    db: Session = Depends(get_db)
):
    course_name = course_data.name.strip()

    existing_course = db.scalar(
        select(Course).where(Course.name.ilike(course_name))
    )

    if existing_course:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Course already exists"
        )

    course = Course(name=course_name)
    db.add(course)

    try:
        db.commit()
        db.refresh(course)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Course already exists"
        )

    return course


@router.get("/", response_model=list[CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    statement = select(Course).order_by(Course.id)
    return db.scalars(statement).all()


@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.get(Course, course_id)

    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    return course
