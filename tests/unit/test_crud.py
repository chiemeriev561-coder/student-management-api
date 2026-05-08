from app.crud import course as crud_course
from app.crud import student as crud_student
from app.crud import user as crud_user
from app.schemas.courses import CourseCreate, CourseUpdate
from app.schemas.students import StudentCreate, StudentUpdate


def test_student_crud_functions(db_session):
    student = crud_student.create_student(
        db_session,
        StudentCreate(
            name="Alice Johnson",
            age=21,
            email="alice@example.com",
            major="Computer Science",
        ),
    )

    assert student.id is not None
    assert crud_student.get_student(db_session, student.id).email == "alice@example.com"
    assert crud_student.get_student_by_email(db_session, "alice@example.com").id == student.id
    assert crud_student.get_students(db_session) == [student]

    updated_student = crud_student.update_student(
        db_session,
        student,
        StudentUpdate(age=22, major="Software Engineering"),
    )
    assert updated_student.age == 22
    assert updated_student.major == "Software Engineering"

    deleted_student = crud_student.delete_student(db_session, updated_student)
    assert deleted_student.id == student.id
    assert crud_student.get_student(db_session, student.id) is None


def test_course_crud_functions(db_session):
    course = crud_course.create_course(
        db_session,
        CourseCreate(
            title="Algorithms",
            description="Core algorithms and analysis",
            credits=3,
        ),
    )

    assert course.id is not None
    assert crud_course.get_course(db_session, course.id).title == "Algorithms"
    assert crud_course.get_courses(db_session) == [course]

    updated_course = crud_course.update_course(
        db_session,
        course,
        CourseUpdate(description="Updated description", credits=4),
    )
    assert updated_course.description == "Updated description"
    assert updated_course.credits == 4

    deleted_course = crud_course.delete_course(db_session, updated_course)
    assert deleted_course.id == course.id
    assert crud_course.get_course(db_session, course.id) is None


def test_user_crud_functions(db_session):
    user = crud_user.create_user(
        db_session,
        username="admin",
        email="admin@example.com",
        password_hash="hashed-password",
    )

    assert user.id is not None
    assert crud_user.get_user_by_id(db_session, user.id).username == "admin"
    assert crud_user.get_user_by_username(db_session, "admin").email == "admin@example.com"
    assert crud_user.get_user_by_email(db_session, "admin@example.com").id == user.id
