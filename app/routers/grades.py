from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.crud import course as crud_course
from app.crud import grade as crud_grade
from app.crud import student as crud_student
from app.database import get_db
from app.dependencies import get_current_user
from app.schemas import grades as schemas_grade

router = APIRouter(
    prefix="/grades",
    tags=["Grades"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=schemas_grade.GradeListResponse)
def get_all_grades(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return {
        "items": crud_grade.get_grades(db, skip=skip, limit=limit),
        "total": crud_grade.count_grades(db),
        "skip": skip,
        "limit": limit,
    }


@router.get("/{student_id}/{course_id}", response_model=schemas_grade.Grade)
def get_grade(student_id: int, course_id: int, db: Session = Depends(get_db)):
    grade_record = crud_grade.get_grade(db, student_id=student_id, course_id=course_id)
    if grade_record is None:
        raise HTTPException(status_code=404, detail="Grade record not found")
    return grade_record


@router.post("/", response_model=schemas_grade.Grade)
def create_grade(grade: schemas_grade.GradeCreate, db: Session = Depends(get_db)):
    db_student = crud_student.get_student(db, student_id=grade.student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    db_course = crud_course.get_course(db, course_id=grade.course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    existing_grade = crud_grade.get_grade(
        db, student_id=grade.student_id, course_id=grade.course_id
    )
    if existing_grade is not None:
        raise HTTPException(status_code=400, detail="Grade record already exists")

    return crud_grade.create_grade(
        db,
        student_id=grade.student_id,
        course_id=grade.course_id,
        grade=grade.grade,
    )


@router.put("/{student_id}/{course_id}", response_model=schemas_grade.Grade)
def update_grade(
    student_id: int,
    course_id: int,
    grade_update: schemas_grade.GradeUpdate,
    db: Session = Depends(get_db),
):
    grade_record = crud_grade.get_grade(db, student_id=student_id, course_id=course_id)
    if grade_record is None:
        raise HTTPException(status_code=404, detail="Grade record not found")

    return crud_grade.update_grade(
        db, student_id=student_id, course_id=course_id, grade=grade_update.grade
    )


@router.delete("/{student_id}/{course_id}")
def delete_grade(student_id: int, course_id: int, db: Session = Depends(get_db)):
    deleted_grade = crud_grade.delete_grade(
        db, student_id=student_id, course_id=course_id
    )
    if deleted_grade is None:
        raise HTTPException(status_code=404, detail="Grade record not found")
    return {"message": "Grade record successfully deleted"}
