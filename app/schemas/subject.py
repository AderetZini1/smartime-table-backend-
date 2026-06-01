from pydantic import BaseModel
from typing import Optional

# בסיס - שדות משותפים
class SubjectBase(BaseModel):
    subject_name: str
    required_room_id: Optional[int] = None  # חדר ייעודי, לא חובה

# ליצירת מקצוע חדש
class SubjectCreate(SubjectBase):
    pass

# לעדכון מקצוע
class SubjectUpdate(BaseModel):
    subject_name: Optional[str] = None
    required_room_id: Optional[int] = None

# מה שחוזר מהשרת
class SubjectResponse(SubjectBase):
    id: int

    class Config:
        from_attributes = True