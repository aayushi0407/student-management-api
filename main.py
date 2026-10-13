

from fastapi import FastAPI

from routes.student_routes import router as student_router
from routes.course_routes import router as course_router


app = FastAPI(title="Student Management API")


@app.get("/")
def home():
    return {"message": "Student Management API is running"}


app.include_router(student_router)
app.include_router(course_router)
