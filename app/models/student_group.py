from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class StudentGroup(Base):
    __tablename__ = "student_groups"

    id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String, unique=True, nullable=False)  
    student_count = Column(Integer, nullable=False)  
    home_room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)  