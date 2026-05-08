from fastapi.testclient import TestClient

from app.database import get_db
from app.main import create_app


def test_root_endpoint(client: TestClient):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Student Management API!"}


def test_register_and_login_returns_access_token(client: TestClient):
    register_response = client.post(
        "/auth/register",
        json={
            "username": "admin",
            "email": "admin@example.com",
            "password": "strong-password",
        },
    )

    assert register_response.status_code == 201
    register_body = register_response.json()
    assert register_body["token_type"] == "bearer"
    assert register_body["user"]["username"] == "admin"
    assert "access_token" in register_body

    login_response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "strong-password"},
    )

    assert login_response.status_code == 200
    login_body = login_response.json()
    assert login_body["token_type"] == "bearer"
    assert login_body["user"]["email"] == "admin@example.com"


def test_login_rejects_invalid_credentials(client: TestClient):
    response = client.post(
        "/auth/login",
        json={"username": "missing", "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid username or password"}


def test_protected_endpoints_require_authentication(client: TestClient):
    response = client.get("/students/")

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Authentication credentials were not provided"
    }


def test_student_crud_flow(client: TestClient, auth_headers):
    create_payload = {
        "name": "Alice Johnson",
        "age": 21,
        "email": "alice@example.com",
        "major": "Computer Science",
    }

    create_response = client.post("/students/", json=create_payload, headers=auth_headers)
    assert create_response.status_code == 200
    created_student = create_response.json()
    assert created_student["name"] == create_payload["name"]
    assert created_student["email"] == create_payload["email"]

    student_id = created_student["id"]

    list_response = client.get("/students/", headers=auth_headers)
    assert list_response.status_code == 200
    assert list_response.json()["total"] == 1
    assert len(list_response.json()["items"]) == 1
    assert list_response.headers["X-Cache"] == "MISS"

    cached_list_response = client.get("/students/", headers=auth_headers)
    assert cached_list_response.status_code == 200
    assert cached_list_response.headers["X-Cache"] == "HIT"

    get_response = client.get(f"/students/{student_id}", headers=auth_headers)
    assert get_response.status_code == 200
    assert get_response.json()["id"] == student_id
    assert get_response.headers["X-Cache"] == "MISS"

    cached_get_response = client.get(f"/students/{student_id}", headers=auth_headers)
    assert cached_get_response.status_code == 200
    assert cached_get_response.headers["X-Cache"] == "HIT"

    update_response = client.put(
        f"/students/{student_id}",
        json={"major": "Software Engineering", "age": 22},
        headers=auth_headers,
    )
    assert update_response.status_code == 200
    assert update_response.json()["major"] == "Software Engineering"
    assert update_response.json()["age"] == 22

    delete_response = client.delete(f"/students/{student_id}", headers=auth_headers)
    assert delete_response.status_code == 200
    assert delete_response.json() == {
        "message": "Student 'Alice Johnson' successfully deleted"
    }


def test_student_duplicate_email_returns_400(client: TestClient, auth_headers):
    payload = {
        "name": "Alice Johnson",
        "age": 21,
        "email": "alice@example.com",
        "major": "Computer Science",
    }

    first_response = client.post("/students/", json=payload, headers=auth_headers)
    duplicate_response = client.post("/students/", json=payload, headers=auth_headers)

    assert first_response.status_code == 200
    assert duplicate_response.status_code == 400
    assert duplicate_response.json() == {"detail": "Email already registered"}


def test_student_not_found_endpoints_return_404(client: TestClient, auth_headers):
    get_response = client.get("/students/9999", headers=auth_headers)
    delete_response = client.delete("/students/9999", headers=auth_headers)
    update_response = client.put(
        "/students/9999", json={"major": "Physics"}, headers=auth_headers
    )

    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Student not found"}
    assert delete_response.status_code == 404
    assert delete_response.json() == {"detail": "Student not found"}
    assert update_response.status_code == 404
    assert update_response.json() == {"detail": "Student not found"}


def test_course_crud_flow(client: TestClient, auth_headers):
    create_payload = {
        "title": "Algorithms",
        "description": "Core algorithms and analysis",
        "credits": 3,
    }

    create_response = client.post("/courses/", json=create_payload, headers=auth_headers)
    assert create_response.status_code == 200
    created_course = create_response.json()
    assert created_course["title"] == create_payload["title"]
    assert created_course["credits"] == create_payload["credits"]

    course_id = created_course["id"]

    list_response = client.get("/courses/", headers=auth_headers)
    assert list_response.status_code == 200
    assert list_response.json()["total"] == 1
    assert len(list_response.json()["items"]) == 1
    assert list_response.headers["X-Cache"] == "MISS"

    cached_list_response = client.get("/courses/", headers=auth_headers)
    assert cached_list_response.status_code == 200
    assert cached_list_response.headers["X-Cache"] == "HIT"

    get_response = client.get(f"/courses/{course_id}", headers=auth_headers)
    assert get_response.status_code == 200
    assert get_response.json()["id"] == course_id
    assert get_response.headers["X-Cache"] == "MISS"

    cached_get_response = client.get(f"/courses/{course_id}", headers=auth_headers)
    assert cached_get_response.status_code == 200
    assert cached_get_response.headers["X-Cache"] == "HIT"

    update_response = client.put(
        f"/courses/{course_id}",
        json={"description": "Updated description", "credits": 4},
        headers=auth_headers,
    )
    assert update_response.status_code == 200
    assert update_response.json()["description"] == "Updated description"
    assert update_response.json()["credits"] == 4

    delete_response = client.delete(f"/courses/{course_id}", headers=auth_headers)
    assert delete_response.status_code == 200
    assert delete_response.json() == {
        "message": "Course 'Algorithms' successfully deleted"
    }


def test_course_not_found_endpoints_return_404(client: TestClient, auth_headers):
    get_response = client.get("/courses/9999", headers=auth_headers)
    delete_response = client.delete("/courses/9999", headers=auth_headers)
    update_response = client.put("/courses/9999", json={"credits": 5}, headers=auth_headers)

    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Course not found"}
    assert delete_response.status_code == 404
    assert delete_response.json() == {"detail": "Course not found"}
    assert update_response.status_code == 404
    assert update_response.json() == {"detail": "Course not found"}


def test_grade_crud_flow(client: TestClient, auth_headers):
    student_response = client.post(
        "/students/",
        json={
            "name": "Alice Johnson",
            "age": 21,
            "email": "alice@example.com",
            "major": "Computer Science",
        },
        headers=auth_headers,
    )
    course_response = client.post(
        "/courses/",
        json={
            "title": "Algorithms",
            "description": "Core algorithms and analysis",
            "credits": 3,
        },
        headers=auth_headers,
    )
    student_id = student_response.json()["id"]
    course_id = course_response.json()["id"]

    create_response = client.post(
        "/grades/",
        json={"student_id": student_id, "course_id": course_id, "grade": "A"},
        headers=auth_headers,
    )
    assert create_response.status_code == 200
    assert create_response.json() == {
        "student_id": student_id,
        "course_id": course_id,
        "grade": "A",
    }

    list_response = client.get("/grades/", headers=auth_headers)
    assert list_response.status_code == 200
    assert list_response.json()["total"] == 1
    assert list_response.json()["items"][0]["grade"] == "A"

    get_response = client.get(f"/grades/{student_id}/{course_id}", headers=auth_headers)
    assert get_response.status_code == 200
    assert get_response.json()["grade"] == "A"

    update_response = client.put(
        f"/grades/{student_id}/{course_id}",
        json={"grade": "A-"},
        headers=auth_headers,
    )
    assert update_response.status_code == 200
    assert update_response.json()["grade"] == "A-"

    delete_response = client.delete(
        f"/grades/{student_id}/{course_id}", headers=auth_headers
    )
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Grade record successfully deleted"}


def test_grade_requires_existing_student_and_course(client: TestClient, auth_headers):
    missing_student_response = client.post(
        "/grades/",
        json={"student_id": 9999, "course_id": 1, "grade": "B"},
        headers=auth_headers,
    )
    assert missing_student_response.status_code == 404
    assert missing_student_response.json() == {"detail": "Student not found"}

    student_response = client.post(
        "/students/",
        json={
            "name": "Alice Johnson",
            "age": 21,
            "email": "alice@example.com",
            "major": "Computer Science",
        },
        headers=auth_headers,
    )
    existing_student_id = student_response.json()["id"]

    missing_course_response = client.post(
        "/grades/",
        json={"student_id": existing_student_id, "course_id": 9999, "grade": "B"},
        headers=auth_headers,
    )
    assert missing_course_response.status_code == 404
    assert missing_course_response.json() == {"detail": "Course not found"}


def test_grade_not_found_endpoints_return_404(client: TestClient, auth_headers):
    get_response = client.get("/grades/1/1", headers=auth_headers)
    update_response = client.put("/grades/1/1", json={"grade": "B"}, headers=auth_headers)
    delete_response = client.delete("/grades/1/1", headers=auth_headers)

    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Grade record not found"}
    assert update_response.status_code == 404
    assert update_response.json() == {"detail": "Grade record not found"}
    assert delete_response.status_code == 404
    assert delete_response.json() == {"detail": "Grade record not found"}


def test_student_pagination_metadata(client: TestClient, auth_headers):
    for index in range(3):
        response = client.post(
            "/students/",
            json={
                "name": f"Student {index}",
                "age": 20 + index,
                "email": f"student{index}@example.com",
                "major": "Engineering",
            },
            headers=auth_headers,
        )
        assert response.status_code == 200

    response = client.get("/students/?skip=1&limit=2", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["skip"] == 1
    assert response.json()["limit"] == 2
    assert response.json()["total"] == 3
    assert len(response.json()["items"]) == 2


def test_summary_report_is_generated_in_background(client: TestClient, auth_headers):
    client.post(
        "/students/",
        json={
            "name": "Alice Johnson",
            "age": 21,
            "email": "alice@example.com",
            "major": "Computer Science",
        },
        headers=auth_headers,
    )
    client.post(
        "/courses/",
        json={
            "title": "Algorithms",
            "description": "Core algorithms and analysis",
            "credits": 3,
        },
        headers=auth_headers,
    )

    create_response = client.post("/reports/summary", headers=auth_headers)

    assert create_response.status_code == 202
    job_id = create_response.json()["job_id"]

    status_response = client.get(f"/reports/summary/{job_id}", headers=auth_headers)

    assert status_response.status_code == 200
    assert status_response.json()["status"] == "completed"
    assert status_response.json()["result"] == {
        "students": 1,
        "courses": 1,
        "enrollments": 0,
    }


def test_rate_limiting_rejects_excess_requests(db_session):
    app = create_app(rate_limit_max_requests=2, rate_limit_window_seconds=60)

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as limited_client:
        first = limited_client.get("/")
        second = limited_client.get("/")
        third = limited_client.get("/")

    assert first.status_code == 200
    assert second.status_code == 200
    assert third.status_code == 429
    assert third.json() == {"detail": "Rate limit exceeded"}
