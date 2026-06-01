from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# בסיס - שדות משותפים
class ScheduleRunBase(BaseModel):
    algorithm: str  # CSP / HILL_CLIMBING / GENETIC
    score: Optional[float] = None  # ציון פונקציית המטרה
    is_selected: bool = False  # המערכת הנבחרת

# ליצירת הרצה חדשה
class ScheduleRunCreate(BaseModel):
    algorithm: str  # רק האלגוריתם נשלח - השאר ממולא אוטומטית

# מה שחוזר מהשרת
class ScheduleRunResponse(ScheduleRunBase):
    id: int
    run_at: datetime  # זמן ההרצה

    class Config:
        from_attributes = True