from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import Optional
from app.database import get_db
from app.models.teacher import Teacher
from app.auth import get_current_teacher
from pydantic import BaseModel

class HomeroomPrefSchema(BaseModel):
    wants_homeroom: Optional[bool] = None
    preferred_group_id: Optional[int] = None
    wants_continue_with_previous: Optional[bool] = None

class HomeroomPrefResponse(BaseModel):
    id: int
    teacher_id: int
    wants_homeroom: Optional[bool]
    preferred_group_id: Optional[int]
    wants_continue_with_previous: Optional[bool]

    class Config:
        from_attributes = True

router = APIRouter(prefix="/teacher-homeroom-prefs", tags=["teacher-homeroom-prefs"])

@router.get("/me")
async def get_my_homeroom_pref(
    db: AsyncSession = Depends(get_db),
    current_teacher: Teacher = Depends(get_current_teacher)
):
    result = await db.execute(
        text("SELECT * FROM teacher_homeroom_preferences WHERE teacher_id = :tid"),
        {"tid": current_teacher.id}
    )
    row = result.mappings().one_or_none()
    return dict(row) if row else {}

@router.post("/me")
async def save_my_homeroom_pref(
    data: HomeroomPrefSchema,
    db: AsyncSession = Depends(get_db),
    current_teacher: Teacher = Depends(get_current_teacher)
):
    await db.execute(
        text("""
            INSERT INTO teacher_homeroom_preferences (teacher_id, wants_homeroom, preferred_group_id, wants_continue_with_previous)
            VALUES (:tid, :wh, :pgid, :wcp)
            ON CONFLICT (teacher_id) DO UPDATE SET
                wants_homeroom = :wh,
                preferred_group_id = :pgid,
                wants_continue_with_previous = :wcp
        """),
        {"tid": current_teacher.id, "wh": data.wants_homeroom, "pgid": data.preferred_group_id, "wcp": data.wants_continue_with_previous}
    )
    await db.commit()
    return {"message": "Saved"}