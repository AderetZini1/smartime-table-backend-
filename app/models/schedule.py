from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class Schedule(Base):
    __tablename__ = "schedule"

    id = Column(Integer, primary_key=True, index=True)
    timeslot_id = Column(Integer, ForeignKey("timeslots.id"), nullable=False) 
    tea_assignment_id = Column(Integer, ForeignKey("teacher_assignments.id"), nullable=False)  
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)  
    run_id = Column(Integer, ForeignKey("schedule_runs.id"), nullable=True) 