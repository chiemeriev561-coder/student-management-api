from fastapi import FastAPI
from app.routers import students

from app.routers import courses

from app.database import engine, Base
# Import models to register them with SQLAlchemy for table creation
from app.models.student import Student
from app.models.course import Course

# Ensure models are registered (this line serves to silence unused import warnings)
_ = [Student, Course]

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Management API")

# Include the routers
app.include_router(students.router)
app.include_router(courses.router)


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Student Management API!"}
