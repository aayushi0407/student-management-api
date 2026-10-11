
def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Student Management API is running"
    }


def test_create_student(client):
    response = client.post(
        "/students",
        json={
            "name": "Rahul Sharma",
            "email": "rahul@example.com",
            "course": "Computer Science"
        }
    )

    assert response.status_code == 201

    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "Rahul Sharma"
    assert data["email"] == "rahul@example.com"
    assert data["course"] == "Computer Science"


def test_invalid_email(client):
    response = client.post(
        "/students",
        json={
            "name": "Rahul Sharma",
            "email": "not-an-email",
            "course": "Computer Science"
        }
    )

    assert response.status_code == 422


def test_duplicate_email(client):
    student = {
        "name": "Rahul Sharma",
        "email": "rahul@example.com",
        "course": "Computer Science"
    }

    first = client.post("/students", json=student)
    second = client.post("/students", json=student)

    assert first.status_code == 201
    assert second.status_code == 409


def test_get_student(client):
    created = client.post(
        "/students",
        json={
            "name": "Priya Sharma",
            "email": "priya@example.com",
            "course": "Information Technology"
        }
    )

    student_id = created.json()["id"]

    response = client.get(f"/students/{student_id}")

    assert response.status_code == 200
    assert response.json()["id"] == student_id


def test_student_not_found(client):
    response = client.get("/students/999999")

    assert response.status_code == 404


def test_update_student(client):
    created = client.post(
        "/students",
        json={
            "name": "Aman Sharma",
            "email": "aman@example.com",
            "course": "Computer Science"
        }
    )

    student_id = created.json()["id"]

    response = client.put(
        f"/students/{student_id}",
        json={
            "name": "Aman Verma",
            "email": "aman@example.com",
            "course": "Data Science"
        }
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Aman Verma"
    assert response.json()["course"] == "Data Science"


def test_delete_student(client):
    created = client.post(
        "/students",
        json={
            "name": "Neha Sharma",
            "email": "neha@example.com",
            "course": "Computer Science"
        }
    )

    student_id = created.json()["id"]

    deleted = client.delete(f"/students/{student_id}")
    fetched = client.get(f"/students/{student_id}")

    assert deleted.status_code == 200
    assert fetched.status_code == 404
