from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.models.course import Course
from app.models.student import Student
from app.routers import courses, students

# Ensure SQLAlchemy metadata is fully registered before creating tables.
_ = [Student, Course]

TEST_DATABASE_URL = "sqlite://"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_test_app() -> FastAPI:
    app = FastAPI(title="Student Management API Test")
    app.include_router(students.router)
    app.include_router(courses.router)

    @app.get("/", tags=["Root"])
    def read_root():
        return {"message": "Welcome to the Student Management API!"}

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    return app


@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    app = create_test_app()
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)


def test_root_endpoint(client: TestClient):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Student Management API!"}


def test_student_crud_flow(client: TestClient):
    create_payload = {
        "name": "Alice Johnson",
        "age": 21,
        "email": "alice@example.com",
        "major": "Computer Science",
    }

    create_response = client.post("/students/", json=create_payload)
    assert create_response.status_code == 200
    created_student = create_response.json()
    assert created_student["name"] == create_payload["name"]
    assert created_student["email"] == create_payload["email"]

    student_id = created_student["id"]

    list_response = client.get("/students/")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    get_response = client.get(f"/students/{student_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == student_id

    update_response = client.put(
        f"/students/{student_id}",
        json={"major": "Software Engineering", "age": 22},
    )
    assert update_response.status_code == 200
    assert update_response.json()["major"] == "Software Engineering"
    assert update_response.json()["age"] == 22

    delete_response = client.delete(f"/students/{student_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {
        "message": "Student 'Alice Johnson' successfully deleted"
    }


def test_student_duplicate_email_returns_400(client: TestClient):
    payload = {
        "name": "Alice Johnson",
        "age": 21,
        "email": "alice@example.com",
        "major": "Computer Science",
    }

    first_response = client.post("/students/", json=payload)
    duplicate_response = client.post("/students/", json=payload)

    assert first_response.status_code == 200
    assert duplicate_response.status_code == 400
    assert duplicate_response.json() == {"detail": "Email already registered"}


def test_student_not_found_endpoints_return_404(client: TestClient):
    get_response = client.get("/students/9999")
    delete_response = client.delete("/students/9999")
    update_response = client.put("/students/9999", json={"major": "Physics"})

    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Student not found"}
    assert delete_response.status_code == 404
    assert delete_response.json() == {"detail": "Student not found"}
    assert update_response.status_code == 404
    assert update_response.json() == {"detail": "Student not found"}


def test_course_crud_flow(client: TestClient):
    create_payload = {
        "title": "Algorithms",
        "description": "Core algorithms and analysis",
        "credits": 3,
    }

    create_response = client.post("/courses/", json=create_payload)
    assert create_response.status_code == 200
    created_course = create_response.json()
    assert created_course["title"] == create_payload["title"]
    assert created_course["credits"] == create_payload["credits"]

    course_id = created_course["id"]

    list_response = client.get("/courses/")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    get_response = client.get(f"/courses/{course_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == course_id

    update_response = client.put(
        f"/courses/{course_id}",
        json={"description": "Updated description", "credits": 4},
    )
    assert update_response.status_code == 200
    assert update_response.json()["description"] == "Updated description"
    assert update_response.json()["credits"] == 4

    delete_response = client.delete(f"/courses/{course_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {
        "message": "Course 'Algorithms' successfully deleted"
    }


def test_course_not_found_endpoints_return_404(client: TestClient):
    get_response = client.get("/courses/9999")
    delete_response = client.delete("/courses/9999")
    update_response = client.put("/courses/9999", json={"credits": 5})

    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Course not found"}
    assert delete_response.status_code == 404
    assert delete_response.json() == {"detail": "Course not found"}
    assert update_response.status_code == 404
    assert update_response.json() == {"detail": "Course not found"}
