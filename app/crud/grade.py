from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.orm import Session

from app.models.course import student_course


def get_grade(db: Session, student_id: int, course_id: int):
    statement = select(
        student_course.c.student_id,
        student_course.c.course_id,
        student_course.c.grade,
    ).where(
        student_course.c.student_id == student_id,
        student_course.c.course_id == course_id,
    )
    row = db.execute(statement).mappings().first()
    return dict(row) if row else None


def get_grades(db: Session, skip: int = 0, limit: int = 100):
    statement = (
        select(
            student_course.c.student_id,
            student_course.c.course_id,
            student_course.c.grade,
        )
        .offset(skip)
        .limit(limit)
    )
    return [dict(row) for row in db.execute(statement).mappings().all()]


def count_grades(db: Session):
    statement = select(func.count()).select_from(student_course)
    return db.execute(statement).scalar_one()


def create_grade(db: Session, student_id: int, course_id: int, grade: str):
    statement = insert(student_course).values(
        student_id=student_id, course_id=course_id, grade=grade
    )
    db.execute(statement)
    db.commit()
    return get_grade(db, student_id=student_id, course_id=course_id)


def update_grade(db: Session, student_id: int, course_id: int, grade: str):
    statement = (
        update(student_course)
        .where(
            student_course.c.student_id == student_id,
            student_course.c.course_id == course_id,
        )
        .values(grade=grade)
    )
    db.execute(statement)
    db.commit()
    return get_grade(db, student_id=student_id, course_id=course_id)


def delete_grade(db: Session, student_id: int, course_id: int):
    grade_record = get_grade(db, student_id=student_id, course_id=course_id)
    if grade_record is None:
        return None

    statement = delete(student_course).where(
        student_course.c.student_id == student_id,
        student_course.c.course_id == course_id,
    )
    db.execute(statement)
    db.commit()
    return grade_record
