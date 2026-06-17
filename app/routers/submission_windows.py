from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from datetime import datetime
from app.database import get_db
from app.models.submission_window import SubmissionWindow
from app.models.teacher import Teacher
from app.auth import get_current_teacher, get_current_admin
from pydantic import BaseModel
from zoneinfo import ZoneInfo

class SubmissionWindowCreate(BaseModel):
    title: str
    start_date: datetime
    end_date: datetime
    is_active: bool = True

class SubmissionWindowResponse(BaseModel):
    id: int
    title: str
    start_date: datetime
    end_date: datetime
    is_active: bool

    class Config:
        from_attributes = True

router = APIRouter(prefix="/submission-windows", tags=["submission-windows"])

@router.get("/", response_model=List[SubmissionWindowResponse])
async def list_windows(
    db: AsyncSession = Depends(get_db),
    _: Teacher = Depends(get_current_teacher)
):
    result = await db.execute(select(SubmissionWindow).order_by(SubmissionWindow.start_date.desc()))
    return result.scalars().all()

@router.get("/active", response_model=SubmissionWindowResponse | None)
async def get_active_window(
    db: AsyncSession = Depends(get_db),
    _: Teacher = Depends(get_current_teacher)
):
    """בודק אם יש חלון הגשה פעיל כרגע"""
    now = datetime.now(ZoneInfo("Asia/Jerusalem")).replace(tzinfo=None)
    result = await db.execute(
        select(SubmissionWindow).where(
            SubmissionWindow.is_active == True,
            SubmissionWindow.start_date <= now,
            SubmissionWindow.end_date >= now
        )
    )
    return result.scalar_one_or_none()

@router.post("/", response_model=SubmissionWindowResponse)
async def create_window(
    data: SubmissionWindowCreate,
    db: AsyncSession = Depends(get_db),
    _: Teacher = Depends(get_current_admin)
):
    dump = data.model_dump()
    dump['start_date'] = dump['start_date'].replace(tzinfo=None)
    dump['end_date'] = dump['end_date'].replace(tzinfo=None)
    window = SubmissionWindow(**dump)
    db.add(window)
    await db.commit()
    await db.refresh(window)
    return window

@router.delete("/{window_id}")
async def delete_window(
    window_id: int,
    db: AsyncSession = Depends(get_db),
    _: Teacher = Depends(get_current_admin)
):
    result = await db.execute(select(SubmissionWindow).where(SubmissionWindow.id == window_id))
    window = result.scalar_one_or_none()
    if not window:
        raise HTTPException(status_code=404, detail="Window not found")
    await db.delete(window)
    await db.commit()
    return {"message": "Deleted"}