# Student Management API

A RESTful API built with **FastAPI, PostgreSQL, and SQLAlchemy** to manage student records. The project implements CRUD operations, input validation, database constraints, and automated testing.

## Features

- Create a new student
- Retrieve all students or a student by ID
- Update existing student details
- Delete a student record
- Validate student names, email addresses, and course names
- Prevent duplicate email addresses
- Handle errors such as student not found and duplicate email
- Separate routes, services, and repository layers
- Automated API tests using Pytest

## Tech Stack

- **Language:** Python
- **API Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Validation:** Pydantic
- **Testing:** Pytest and HTTPX
- **Server:** Uvicorn

## Project Structure

```text
stu_management/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── requirements.txt
├── .env
├── .gitignore
├── routes/
│   ├── __init__.py
│   └── student_routes.py
├── services/
│   ├── __init__.py
│   └── student_service.py
├── repositories/
│   ├── __init__.py
│   └── student_repository.py
└── tests/
    ├── conftest.py
    └── test_students.py
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/aayushi0407/student-management-api.git
cd student-management-api
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/student_api_db
STUDENT_TEST_DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/student_api_test_db
```

Replace `YOUR_PASSWORD` with your PostgreSQL password.

Create the `student_api_db` and `student_api_test_db` databases in PostgreSQL before running the application and tests.

**Important:** Keep `.env` private. Never commit your database credentials to GitHub. Automated tests should use a separate test database.

### 5. Run the application

```bash
uvicorn main:app --reload
```

The API will run locally at:

`http://127.0.0.1:8000`

Open the interactive API documentation at:

`http://127.0.0.1:8000/docs`

## API Endpoints

Base URL: `http://127.0.0.1:8000`

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check API status |
| POST | `/students` | Create a student |
| GET | `/students` | Retrieve all students |
| GET | `/students/{student_id}` | Retrieve a student by ID |
| PUT | `/students/{student_id}` | Update a student |
| DELETE | `/students/{student_id}` | Delete a student |

### Example: Create a student

**Request**

```http
POST /students
Content-Type: application/json
```

```json
{
  "name": "Aarav Sharma",
  "email": "aarav@example.com",
  "course": "Computer Science"
}
```

**Example response**

```json
{
  "id": 1,
  "name": "Aarav Sharma",
  "email": "aarav@example.com",
  "course": "Computer Science"
}
```

The generated ID may differ depending on the database.

## Validation and Error Handling

The API validates input data and handles common errors, including:

- Invalid email addresses
- Names and course names that are too short or empty
- Duplicate email addresses
- Requests for students that do not exist

Common status codes include:

- `200 OK` — Request completed successfully
- `201 Created` — Student created successfully
- `404 Not Found` — Student does not exist
- `409 Conflict` — Email address already registered
- `422 Unprocessable Entity` — Request data failed validation

## Architecture

The project uses a layered architecture:

- **Routes:** Handle HTTP requests and responses.
- **Services:** Implement business logic and error handling.
- **Repositories:** Perform database operations.
- **Models:** Define database tables using SQLAlchemy.
- **Schemas:** Validate incoming data and structure API responses.
- **Database:** Configure PostgreSQL connectivity and database sessions.

This separation makes the code easier to maintain, test, and extend.

## Running Tests

Make sure PostgreSQL is running and the test database is configured separately from the development database.

Run:

```bash
python -m pytest -v
```

The test suite covers API functionality, input validation, duplicate emails, retrieving students, updating records, and deleting records.

## Future Improvements

- Add pagination and search filters
- Add database migrations with Alembic
- Implement authentication and authorization
- Add Docker support
- Deploy the API to a cloud platform

## Learning Outcomes

Through this project, I practised building REST APIs, integrating PostgreSQL with SQLAlchemy, validating request data, organizing backend code into layers, handling errors, writing automated tests, and using Git and GitHub for version control.