from sqlalchemy import Column, Integer
from app.database import Base

class Timeslot(Base):
    __tablename__ = "timeslots"

    id = Column(Integer, primary_key=True, index=True)
    day_of_week = Column(Integer, nullable=False)   
    hour_of_day = Column(Integer, nullable=False)  