from fastapi import FastAPI
from app.database import SessionLocal
from app.routers import auth
from app.routers import students
from app.routers import courses
from app.routers import grades
from app.routers import reports
from app.rate_limiter import (
    DEFAULT_RATE_LIMIT_MAX_REQUESTS,
    DEFAULT_RATE_LIMIT_WINDOW_SECONDS,
    RateLimitMiddleware,
)


def create_app(
    rate_limit_max_requests: int = DEFAULT_RATE_LIMIT_MAX_REQUESTS,
    rate_limit_window_seconds: int = DEFAULT_RATE_LIMIT_WINDOW_SECONDS,
):
    app = FastAPI(title="Student Management API")
    app.state.session_factory = SessionLocal
    app.add_middleware(
        RateLimitMiddleware,
        max_requests=rate_limit_max_requests,
        window_seconds=rate_limit_window_seconds,
    )

    app.include_router(auth.router)
    app.include_router(students.router)
    app.include_router(courses.router)
    app.include_router(grades.router)
    app.include_router(reports.router)

    @app.get("/", tags=["Root"])
    def read_root():
        return {"message": "Welcome to the Student Management API!"}

    return app


app = create_app()
