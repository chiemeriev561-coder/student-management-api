from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.crud import student as crud_student
from app.schemas import students as schemas_student

router = APIRouter(prefix="/students", tags=["Students"])


@router.get("/", response_model=List[schemas_student.Student])
def get_all_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = crud_student.get_students(db, skip=skip, limit=limit)
    return students


@router.get("/{student_id}", response_model=schemas_student.Student)
def get_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud_student.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


@router.post("/", response_model=schemas_student.Student)
def create_student(
    student: schemas_student.StudentCreate, db: Session = Depends(get_db)
):
    db_student = crud_student.get_student_by_email(db, email=student.email)
    if db_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_student.create_student(db=db, student=student)


@router.put("/{student_id}", response_model=schemas_student.Student)
def update_student(
    student_id: int,
    student_update: schemas_student.StudentUpdate,
    db: Session = Depends(get_db),
):
    db_student = crud_student.get_student(db, student_id=student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return crud_student.update_student(
        db, db_student=db_student, student_update=student_update
    )


@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud_student.get_student(db, student_id=student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    crud_student.delete_student(db, db_student=db_student)
    return {"message": f"Student '{db_student.name}' successfully deleted"}
