from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    subject_name = Column(String, unique=True, nullable=False)  
    required_room_id = Column(Integer, ForeignKey("rooms.id"), nullable=True)  