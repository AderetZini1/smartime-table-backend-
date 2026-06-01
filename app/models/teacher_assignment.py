from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class TeacherAssignment(Base):
    __tablename__ = "teacher_assignments"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    cur_requirement_id = Column(Integer, ForeignKey("curriculum_requirements.id"), nullable=False)  