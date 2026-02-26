from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.crud import course as crud_course
from app.schemas import courses as schemas_course

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("/", response_model=List[schemas_course.Course])
def get_all_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    courses = crud_course.get_courses(db, skip=skip, limit=limit)
    return courses


@router.get("/{course_id}", response_model=schemas_course.Course)
def get_course(course_id: int, db: Session = Depends(get_db)):
    db_course = crud_course.get_course(db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course


@router.post("/", response_model=schemas_course.Course)
def create_course(course: schemas_course.CourseCreate, db: Session = Depends(get_db)):
    return crud_course.create_course(db=db, course=course)


@router.put("/{course_id}", response_model=schemas_course.Course)
def update_course(
    course_id: int,
    course_update: schemas_course.CourseUpdate,
    db: Session = Depends(get_db),
):
    db_course = crud_course.get_course(db, course_id=course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    return crud_course.update_course(
        db, db_course=db_course, course_update=course_update
    )


@router.delete("/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    db_course = crud_course.get_course(db, course_id=course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    crud_course.delete_course(db, db_course=db_course)
    return {"message": f"Course '{db_course.title}' successfully deleted"}
