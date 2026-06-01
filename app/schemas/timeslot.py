from pydantic import BaseModel

# בסיס - שדות משותפים
class TimeslotBase(BaseModel):
    day_of_week: int  # 1-6 (ראשון עד שישי)
    hour_of_day: int  # 1-8 (מספר השיעור ביום)

# ליצירת timeslot חדש
class TimeslotCreate(TimeslotBase):
    pass

# מה שחוזר מהשרת
class TimeslotResponse(TimeslotBase):
    id: int

    class Config:
        from_attributes = True