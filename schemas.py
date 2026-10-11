

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class StudentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    course: str = Field(min_length=2, max_length=100)

    @field_validator("name", "course", mode="before")
    @classmethod
    def clean_text(cls, value):
        if isinstance(value, str):
            value = value.strip()

        if not isinstance(value, str) or not value:
            raise ValueError("This field cannot be empty")

        return value


class StudentUpdate(StudentCreate):
    pass


class StudentResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    course: str

    model_config = ConfigDict(from_attributes=True)
