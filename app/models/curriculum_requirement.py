from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid

class CurriculumRequirement(Base):
    __tablename__ = "curriculum_requirements"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)  
    student_group_id = Column(Integer, ForeignKey("student_groups.id"), nullable=False)  
    weekly_hours = Column(Integer, nullable=False) 
    sync_block_identity = Column(UUID(as_uuid=True), nullable=True)  