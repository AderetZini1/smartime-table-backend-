from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class TeacherConstraint(Base):
    __tablename__ = "teacher_constraints"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False) 
    timeslot_id = Column(Integer, ForeignKey("timeslots.id"), nullable=False)  
    weight = Column(Integer, nullable=False)  