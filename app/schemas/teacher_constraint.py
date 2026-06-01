from pydantic import BaseModel
from typing import Optional

# בסיס - שדות משותפים
class TeacherConstraintBase(BaseModel):
    teacher_id: int
    timeslot_id: int
    weight: int  # 100=אילוץ קשיח, 1-10=העדפה רכה

# ליצירת אילוץ חדש
class TeacherConstraintCreate(TeacherConstraintBase):
    pass

# לעדכון אילוץ
class TeacherConstraintUpdate(BaseModel):
    weight: Optional[int] = None

# מה שחוזר מהשרת
class TeacherConstraintResponse(TeacherConstraintBase):
    id: int

    class Config:
        from_attributes = True