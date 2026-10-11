

from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import Base, engine
from models import Student
from routes.student_routes import router as student_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Student Management API",
    lifespan=lifespan
)


@app.get("/")
def home():
    return {"message": "Student Management API is running"}


app.include_router(student_router)
