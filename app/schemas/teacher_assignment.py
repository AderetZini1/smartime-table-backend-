from pydantic import BaseModel

# בסיס - שדות משותפים
class TeacherAssignmentBase(BaseModel):
    teacher_id: int
    cur_requirement_id: int  # הדרישה המוקצית למורה

# ליצירת הקצאה חדשה
class TeacherAssignmentCreate(TeacherAssignmentBase):
    pass

# מה שחוזר מהשרת
class TeacherAssignmentResponse(TeacherAssignmentBase):
    id: int

    class Config:
        from_attributes = True