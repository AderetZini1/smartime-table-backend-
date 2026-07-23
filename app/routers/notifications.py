from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import List, Optional
from datetime import datetime
from app.database import get_db
from app.models.teacher import Teacher
from app.auth import get_current_teacher, get_current_admin
from pydantic import BaseModel
import resend
import os

resend.api_key = os.getenv("RESEND_API_KEY")

class NotificationCreate(BaseModel):
    title: str
    body: str

class NotificationResponse(BaseModel):
    id: int
    notification_id: int
    title: str
    body: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.post("/")
async def send_notification(
    data: NotificationCreate,
    db: AsyncSession = Depends(get_db),
    current_teacher: Teacher = Depends(get_current_admin)
):
    # שמירה ב-DB
    result = await db.execute(
        text("INSERT INTO notifications (title, body, created_by) VALUES (:title, :body, :created_by) RETURNING id"),
        {"title": data.title, "body": data.body, "created_by": current_teacher.id}
    )
    notification_id = result.scalar()

    # שליפת כל המורים
    teachers_result = await db.execute(
        text("SELECT id, email, first_name FROM teachers WHERE is_admin = false")
    )
    teachers = teachers_result.mappings().all()

    # יצירת teacher_notifications לכל מורה
    for teacher in teachers:
        await db.execute(
            text("INSERT INTO teacher_notifications (notification_id, teacher_id) VALUES (:nid, :tid)"),
            {"nid": notification_id, "tid": teacher["id"]}
        )

    await db.commit()

    # שליחת מייל לכל מורה
    for teacher in teachers:
        try:
            resend.Emails.send({
                "from": "Smartime <onboarding@resend.dev>",
                "to": teacher["email"],
                "subject": f"הודעה חדשה: {data.title}",
                "html": f"""
                <div dir="rtl" style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2 style="color: #4a3f35;">הודעה חדשה מהמנהל</h2>
                    <h3 style="color: #8a9e78;">{data.title}</h3>
                    <p style="color: #4a3f35;">{data.body}</p>
                    <hr style="border-color: #e2dacc;">
                    <p style="color: #c8baa6; font-size: 12px;">Smartime — מערכת שעות חכמה</p>
                </div>
                """
            })
        except Exception as e:
            print(f"Failed to send email to {teacher['email']}: {e}")

    return {"message": f"נשלחה התראה ל-{len(teachers)} מורים"}

@router.get("/me")
async def get_my_notifications(
    db: AsyncSession = Depends(get_db),
    current_teacher: Teacher = Depends(get_current_teacher)
):
    result = await db.execute(
        text("""
            SELECT tn.id, tn.notification_id, n.title, n.body, tn.is_read, n.created_at
            FROM teacher_notifications tn
            JOIN notifications n ON tn.notification_id = n.id
            WHERE tn.teacher_id = :tid
            ORDER BY n.created_at DESC
        """),
        {"tid": current_teacher.id}
    )
    return [dict(r) for r in result.mappings().all()]

@router.patch("/me/{notification_id}/read")
async def mark_as_read(
    notification_id: int,
    db: AsyncSession = Depends(get_db),
    current_teacher: Teacher = Depends(get_current_teacher)
):
    await db.execute(
        text("UPDATE teacher_notifications SET is_read = true, read_at = NOW() WHERE notification_id = :nid AND teacher_id = :tid"),
        {"nid": notification_id, "tid": current_teacher.id}
    )
    await db.commit()
    return {"message": "נסומן כנקרא"}