from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class ScheduleRun(Base):
    __tablename__ = "schedule_runs"

    id = Column(Integer, primary_key=True, index=True)
    algorithm = Column(String(20), nullable=False)  
    score = Column(Float, nullable=True)  
    run_at = Column(DateTime, server_default=func.now())  
    is_selected = Column(Boolean, nullable=False, default=False)  