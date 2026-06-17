from pydantic import BaseModel
from typing import Optional

class TeacherConstraintBase(BaseModel):
    teacher_id: int
    timeslot_id: int
    weight: int

class TeacherConstraintCreate(TeacherConstraintBase):
    constraint_type: Optional[str] = 'unavailable'
    reason: Optional[str] = None

class TeacherConstraintUpdate(BaseModel):
    weight: Optional[int] = None
    constraint_type: Optional[str] = None
    reason: Optional[str] = None

class TeacherConstraintResponse(TeacherConstraintBase):
    id: int
    constraint_type: Optional[str] = 'unavailable'
    reason: Optional[str] = None

    class Config:
        from_attributes = True