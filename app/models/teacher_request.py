from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base

class TeacherRequest(Base):
    __tablename__ = "teacher_requests"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    request_type = Column(String(50), nullable=False)  # constraint_change / absence / general
    description = Column(Text, nullable=False)          # תוכן הפנייה
    status = Column(String(20), default='pending')      # pending / approved / rejected
    admin_response = Column(Text, nullable=True)        # תשובת המנהל
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())