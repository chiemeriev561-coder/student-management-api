from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.course import student_course


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    email = Column(String, unique=True, index=True)
    major = Column(String, index=True)

    # Establish the Many-to-Many relationship using the association table from course.py
    courses = relationship(
        "Course", secondary=student_course, back_populates="students"
    )
