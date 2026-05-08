from fastapi import APIRouter, Depends, HTTPException, Query, Response

from app.cache import cache
from app.database import get_db
from app.dependencies import get_current_user
from app.crud import student as crud_student
from app.schemas import students as schemas_student
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/students",
    tags=["Students"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=schemas_student.StudentListResponse)
def get_all_students(
    response: Response,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    cache_key = f"students:list:{skip}:{limit}"
    cached_response = cache.get(cache_key)
    if cached_response is not None:
        response.headers["X-Cache"] = "HIT"
        return cached_response

    students = crud_student.get_students(db, skip=skip, limit=limit)
    payload = {
        "items": [
            schemas_student.Student.model_validate(student).model_dump(mode="json")
            for student in students
        ],
        "total": crud_student.count_students(db),
        "skip": skip,
        "limit": limit,
    }
    cache.set(cache_key, payload)
    response.headers["X-Cache"] = "MISS"
    return payload


@router.get("/{student_id}", response_model=schemas_student.Student)
def get_student(student_id: int, response: Response, db: Session = Depends(get_db)):
    cache_key = f"students:detail:{student_id}"
    cached_response = cache.get(cache_key)
    if cached_response is not None:
        response.headers["X-Cache"] = "HIT"
        return cached_response

    db_student = crud_student.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    payload = schemas_student.Student.model_validate(db_student).model_dump(mode="json")
    cache.set(cache_key, payload)
    response.headers["X-Cache"] = "MISS"
    return payload


@router.post("/", response_model=schemas_student.Student)
def create_student(
    student: schemas_student.StudentCreate, db: Session = Depends(get_db)
):
    db_student = crud_student.get_student_by_email(db, email=student.email)
    if db_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    created_student = crud_student.create_student(db=db, student=student)
    cache.invalidate_prefix("students:")
    return created_student


@router.put("/{student_id}", response_model=schemas_student.Student)
def update_student(
    student_id: int,
    student_update: schemas_student.StudentUpdate,
    db: Session = Depends(get_db),
):
    db_student = crud_student.get_student(db, student_id=student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    updated_student = crud_student.update_student(
        db, db_student=db_student, student_update=student_update
    )
    cache.invalidate_prefix("students:")
    return updated_student


@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud_student.get_student(db, student_id=student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    crud_student.delete_student(db, db_student=db_student)
    cache.invalidate_prefix("students:")
    return {"message": f"Student '{db_student.name}' successfully deleted"}
