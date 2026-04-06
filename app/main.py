from fastapi import FastAPI
from app.routers import students
from app.routers import courses

app = FastAPI(title="Student Management API")

# Include the routers
app.include_router(students.router)
app.include_router(courses.router)


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Student Management API!"}
