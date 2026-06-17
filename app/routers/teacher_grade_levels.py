from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import List
from app.database import get_db
from app.models.teacher import Teacher
from app.auth import get_current_teacher
from pydantic import BaseModel

class GradeLevelResponse(BaseModel):
    id: int
    teacher_id: int
    grade_level: int

    class Config:
        from_attributes = True

router = APIRouter(prefix="/teacher-grade-levels", tags=["teacher-grade-levels"])

@router.get("/me", response_model=List[GradeLevelResponse])
async def get_my_grade_levels(
    db: AsyncSession = Depends(get_db),
    current_teacher: Teacher = Depends(get_current_teacher)
):
    result = await db.execute(
        text("SELECT * FROM teacher_grade_levels WHERE teacher_id = :tid"),
        {"tid": current_teacher.id}
    )
    return [dict(r) for r in result.mappings().all()]

@router.post("/me/{grade_level}")
async def add_grade_level(
    grade_level: int,
    db: AsyncSession = Depends(get_db),
    current_teacher: Teacher = Depends(get_current_teacher)
):
    await db.execute(
        text("INSERT INTO teacher_grade_levels (teacher_id, grade_level) VALUES (:tid, :gl) ON CONFLICT DO NOTHING"),
        {"tid": current_teacher.id, "gl": grade_level}
    )
    await db.commit()
    return {"message": "Added"}

@router.delete("/me/{grade_level}")
async def remove_grade_level(
    grade_level: int,
    db: AsyncSession = Depends(get_db),
    current_teacher: Teacher = Depends(get_current_teacher)
):
    await db.execute(
        text("DELETE FROM teacher_grade_levels WHERE teacher_id = :tid AND grade_level = :gl"),
        {"tid": current_teacher.id, "gl": grade_level}
    )
    await db.commit()
    return {"message": "Deleted"}