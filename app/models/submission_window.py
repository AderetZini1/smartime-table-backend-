from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class SubmissionWindow(Base):
    __tablename__ = "submission_windows"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)          # שם החלון
    start_date = Column(DateTime, nullable=False)         # תאריך פתיחה
    end_date = Column(DateTime, nullable=False)           # תאריך סגירה
    is_active = Column(Boolean, default=True)             # האם פעיל
    created_at = Column(DateTime, server_default=func.now())