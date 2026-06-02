from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from datetime import datetime
from app.database import get_db
from app.models.teacher_request import TeacherRequest
from app.models.teacher import Teacher
from app.auth import get_current_teacher, get_current_admin
from pydantic import BaseModel

class TeacherRequestCreate(BaseModel):
    request_type: str
    description: str

class TeacherRequestResponse(BaseModel):
    id: int
    teacher_id: int
    request_type: str
    description: str
    status: str
    admin_response: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class AdminResponseUpdate(BaseModel):
    status: str
    admin_response: Optional[str] = None

router = APIRouter(prefix="/teacher-requests", tags=["teacher-requests"])

@router.get("/", response_model=List[TeacherRequestResponse])
async def list_requests(
    db: AsyncSession = Depends(get_db),
    current_teacher: Teacher = Depends(get_current_teacher)
):
    if current_teacher.is_admin:
        result = await db.execute(select(TeacherRequest).order_by(TeacherRequest.created_at.desc()))
    else:
        result = await db.execute(
            select(TeacherRequest)
            .where(TeacherRequest.teacher_id == current_teacher.id)
            .order_by(TeacherRequest.created_at.desc())
        )
    return result.scalars().all()

@router.post("/", response_model=TeacherRequestResponse)
async def create_request(
    data: TeacherRequestCreate,
    db: AsyncSession = Depends(get_db),
    current_teacher: Teacher = Depends(get_current_teacher)
):
    request = TeacherRequest(
        teacher_id=current_teacher.id,
        request_type=data.request_type,
        description=data.description
    )
    db.add(request)
    await db.commit()
    await db.refresh(request)
    return request

@router.patch("/{request_id}/respond", response_model=TeacherRequestResponse)
async def respond_to_request(
    request_id: int,
    data: AdminResponseUpdate,
    db: AsyncSession = Depends(get_db),
    _: Teacher = Depends(get_current_admin)
):
    result = await db.execute(select(TeacherRequest).where(TeacherRequest.id == request_id))
    req = result.scalar_one_or_none()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    req.status = data.status
    req.admin_response = data.admin_response
    await db.commit()
    await db.refresh(req)
    return req