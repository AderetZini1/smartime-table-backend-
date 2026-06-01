from pydantic import BaseModel
from typing import Optional

# בסיס - שדות משותפים
class ScheduleBase(BaseModel):
    timeslot_id: int
    tea_assignment_id: int  # המורה והמקצוע
    room_id: int
    run_id: Optional[int] = None  # הרצת האלגוריתם שייצרה את השיעור

# ליצירת שיעור חדש
class ScheduleCreate(ScheduleBase):
    pass

# מה שחוזר מהשרת
class ScheduleResponse(ScheduleBase):
    id: int

    class Config:
        from_attributes = True