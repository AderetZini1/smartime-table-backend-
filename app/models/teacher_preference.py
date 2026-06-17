from sqlalchemy import Column, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base

class TeacherPreference(Base):
    __tablename__ = "teacher_preferences"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False, unique=True)
    min_hours = Column(Integer, default=18)
    max_hours = Column(Integer, default=26)
    preferred_consecutive = Column(Boolean, default=False)
    priority_early_finish = Column(Integer, default=3)
    priority_no_gaps = Column(Integer, default=3)
    priority_free_day = Column(Integer, default=3)
    priority_consecutive = Column(Integer, default=3)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())