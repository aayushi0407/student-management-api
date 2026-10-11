
import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, DATABASE_URL, get_db
from main import app
import models  # Ensure model tables are registered


TEST_DATABASE_URL = os.getenv("STUDENT_TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    raise RuntimeError(
        "Set STUDENT_TEST_DATABASE_URL in your .env file"
    )

if TEST_DATABASE_URL == DATABASE_URL:
    raise RuntimeError(
        "The test database must differ from the development database"
    )

test_engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False
)


@pytest.fixture
def client():
    # Reset only the dedicated test database before each test
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    # Do not start the app lifespan, which creates tables
    # using the development engine in this project.
    test_client = TestClient(app)
    yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)
