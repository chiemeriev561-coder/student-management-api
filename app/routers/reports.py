from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.reports import build_summary_report, create_report_job, get_report_job

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
    dependencies=[Depends(get_current_user)],
)


def _run_summary_report(job_id: str, session_factory):
    db = session_factory()
    try:
        build_summary_report(job_id, db)
    finally:
        db.close()


@router.post("/summary", status_code=status.HTTP_202_ACCEPTED)
def create_summary_report(background_tasks: BackgroundTasks, request: Request):
    job_id = create_report_job()
    background_tasks.add_task(_run_summary_report, job_id, request.app.state.session_factory)
    return {"job_id": job_id, "status": "pending"}


@router.get("/summary/{job_id}")
def get_summary_report(job_id: str, db: Session = Depends(get_db)):
    _ = db
    report_job = get_report_job(job_id)
    if report_job is None:
        raise HTTPException(status_code=404, detail="Report job not found")
    return report_job
