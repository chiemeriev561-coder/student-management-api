from pydantic import BaseModel, ConfigDict
from typing import Optional


# --------- Models / Schemas ---------
class CourseBase(BaseModel):
    title: str
    description: str
    credits: int


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    credits: Optional[int] = None


class Course(CourseBase):
    id: int

    # This tells Pydantic to read data even if it is not a dict, but an ORM model
    model_config = ConfigDict(from_attributes=True)
