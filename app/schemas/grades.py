from pydantic import BaseModel


class GradeBase(BaseModel):
    student_id: int
    course_id: int
    grade: str


class GradeCreate(GradeBase):
    pass


class GradeUpdate(BaseModel):
    grade: str


class Grade(GradeBase):
    pass


class GradeListResponse(BaseModel):
    items: list[Grade]
    total: int
    skip: int
    limit: int
