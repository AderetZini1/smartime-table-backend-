from pydantic import BaseModel

# בסיס - שדות משותפים
class RoomBase(BaseModel):
    room_name: str
    capacity: int

# ליצירת חדר חדש
class RoomCreate(RoomBase):
    pass

# לעדכון חדר
class RoomUpdate(BaseModel):
    room_name: str | None = None
    capacity: int | None = None

# מה שחוזר מהשרת
class RoomResponse(RoomBase):
    id: int

    class Config:
        from_attributes = True