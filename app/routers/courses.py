from fastapi import APIRouter, Depends, HTTPException, Query, Response

from app.cache import cache
from app.database import get_db
from app.dependencies import get_current_user
from app.crud import course as crud_course
from app.schemas import courses as schemas_course
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/courses",
    tags=["Courses"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=schemas_course.CourseListResponse)
def get_all_courses(
    response: Response,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    cache_key = f"courses:list:{skip}:{limit}"
    cached_response = cache.get(cache_key)
    if cached_response is not None:
        response.headers["X-Cache"] = "HIT"
        return cached_response

    courses = crud_course.get_courses(db, skip=skip, limit=limit)
    payload = {
        "items": [
            schemas_course.Course.model_validate(course).model_dump(mode="json")
            for course in courses
        ],
        "total": crud_course.count_courses(db),
        "skip": skip,
        "limit": limit,
    }
    cache.set(cache_key, payload)
    response.headers["X-Cache"] = "MISS"
    return payload


@router.get("/{course_id}", response_model=schemas_course.Course)
def get_course(course_id: int, response: Response, db: Session = Depends(get_db)):
    cache_key = f"courses:detail:{course_id}"
    cached_response = cache.get(cache_key)
    if cached_response is not None:
        response.headers["X-Cache"] = "HIT"
        return cached_response

    db_course = crud_course.get_course(db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    payload = schemas_course.Course.model_validate(db_course).model_dump(mode="json")
    cache.set(cache_key, payload)
    response.headers["X-Cache"] = "MISS"
    return payload


@router.post("/", response_model=schemas_course.Course)
def create_course(course: schemas_course.CourseCreate, db: Session = Depends(get_db)):
    created_course = crud_course.create_course(db=db, course=course)
    cache.invalidate_prefix("courses:")
    return created_course


@router.put("/{course_id}", response_model=schemas_course.Course)
def update_course(
    course_id: int,
    course_update: schemas_course.CourseUpdate,
    db: Session = Depends(get_db),
):
    db_course = crud_course.get_course(db, course_id=course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    updated_course = crud_course.update_course(
        db, db_course=db_course, course_update=course_update
    )
    cache.invalidate_prefix("courses:")
    return updated_course


@router.delete("/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    db_course = crud_course.get_course(db, course_id=course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    crud_course.delete_course(db, db_course=db_course)
    cache.invalidate_prefix("courses:")
    return {"message": f"Course '{db_course.title}' successfully deleted"}
