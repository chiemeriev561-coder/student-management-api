from pydantic import BaseModel, ConfigDict
from typing import Optional


# --------- Models / Schemas ---------
class StudentBase(BaseModel):
    name: str
    age: int
    email: str
    major: str


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None
    major: Optional[str] = None


class Student(StudentBase):
    id: int

    # This tells Pydantic to read data even if it is not a dict, but an ORM model
    model_config = ConfigDict(from_attributes=True)
