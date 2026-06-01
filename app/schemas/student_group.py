from pydantic import BaseModel
from typing import Optional

# בסיס - שדות משותפים
class StudentGroupBase(BaseModel):
    group_name: str
    student_count: int
    home_room_id: int  # חדר הבית של הקבוצה

# ליצירת קבוצה חדשה
class StudentGroupCreate(StudentGroupBase):
    pass

# לעדכון קבוצה
class StudentGroupUpdate(BaseModel):
    group_name: Optional[str] = None
    student_count: Optional[int] = None
    home_room_id: Optional[int] = None

# מה שחוזר מהשרת
class StudentGroupResponse(StudentGroupBase):
    id: int

    class Config:
        from_attributes = True