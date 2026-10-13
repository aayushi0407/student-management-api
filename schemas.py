


from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class CourseCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Course name must contain at least 2 characters")
        return value


class CourseResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class StudentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    course_id: int = Field(gt=0)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Student name must contain at least 2 characters")
        return value


class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    email: EmailStr | None = None
    course_id: int | None = Field(default=None, gt=0)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str | None) -> str | None:
        if value is not None:
            value = value.strip()
            if len(value) < 2:
                raise ValueError("Student name must contain at least 2 characters")
        return value


class StudentResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    course_id: int
    course: CourseResponse

    model_config = ConfigDict(from_attributes=True)


class StudentListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    students: list[StudentResponse]
