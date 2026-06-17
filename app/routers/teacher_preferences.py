from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from datetime import datetime
from app.database import get_db
from app.models.teacher_preference import TeacherPreference
from app.models.teacher import Teacher
from app.auth import get_current_teacher
from pydantic import BaseModel

class TeacherPreferenceSchema(BaseModel):
    min_hours: Optional[int] = 18
    max_hours: Optional[int] = 26
    preferred_consecutive: Optional[bool] = False
    priority_early_finish: Optional[int] = 3
    priority_no_gaps: Optional[int] = 3
    priority_free_day: Optional[int] = 3
    priority_consecutive: Optional[int] = 3

class TeacherPreferenceResponse(BaseModel):
    id: int
    teacher_id: int
    min_hours: int
    max_hours: int
    preferred_consecutive: bool
    priority_early_finish: int
    priority_no_gaps: int
    priority_free_day: int
    priority_consecutive: int

    class Config:
        from_attributes = True

router = APIRouter(prefix="/teacher-preferences", tags=["teacher-preferences"])

@router.get("/me", response_model=Optional[TeacherPreferenceResponse])
async def get_my_preferences(
    db: AsyncSession = Depends(get_db),
    current_teacher: Teacher = Depends(get_current_teacher)
):
    result = await db.execute(
        select(TeacherPreference).where(TeacherPreference.teacher_id == current_teacher.id)
    )
    return result.scalar_one_or_none()

@router.post("/me", response_model=TeacherPreferenceResponse)
async def save_my_preferences(
    data: TeacherPreferenceSchema,
    db: AsyncSession = Depends(get_db),
    current_teacher: Teacher = Depends(get_current_teacher)
):
    result = await db.execute(
        select(TeacherPreference).where(TeacherPreference.teacher_id == current_teacher.id)
    )
    pref = result.scalar_one_or_none()
    
    if pref:
        for key, value in data.model_dump().items():
            setattr(pref, key, value)
    else:
        pref = TeacherPreference(teacher_id=current_teacher.id, **data.model_dump())
        db.add(pref)
    
    await db.commit()
    await db.refresh(pref)
    return pref