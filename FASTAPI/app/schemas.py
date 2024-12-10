# app/schemas.py
from pydantic import BaseModel
from typing import List, Optional

class StudentBase(BaseModel):
    name: str

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    group_id: Optional[int]

    class Config:
        orm_mode = True

class GroupBase(BaseModel):
    name: str

class GroupCreate(GroupBase):
    pass

class Group(GroupBase):
    id: int
    students: List[Student] = []

    class Config:
        orm_mode = True
