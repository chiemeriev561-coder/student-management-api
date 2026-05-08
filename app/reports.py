import threading
import uuid
from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.course import Course, student_course
from app.models.student import Student


_report_jobs: dict[str, dict] = {}
_lock = threading.Lock()


def create_report_job() -> str:
    job_id = str(uuid.uuid4())
    with _lock:
        _report_jobs[job_id] = {
            "job_id": job_id,
            "status": "pending",
            "created_at": datetime.now(timezone.utc),
            "completed_at": None,
            "result": None,
        }
    return job_id


def build_summary_report(job_id: str, db: Session):
    students_count = db.query(func.count(Student.id)).scalar() or 0
    courses_count = db.query(func.count(Course.id)).scalar() or 0
    enrollments_count = db.execute(
        select(func.count()).select_from(student_course)
    ).scalar_one()

    with _lock:
        _report_jobs[job_id] = {
            **_report_jobs[job_id],
            "status": "completed",
            "completed_at": datetime.now(timezone.utc),
            "result": {
                "students": students_count,
                "courses": courses_count,
                "enrollments": enrollments_count,
            },
        }


def get_report_job(job_id: str):
    with _lock:
        return _report_jobs.get(job_id)


def clear_report_jobs():
    with _lock:
        _report_jobs.clear()
