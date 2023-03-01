from pydantic import BaseModel
import datetime

class CT(BaseModel):
    id_course: int
    id_teacher: int
    score: float
    date: datetime.date
class CT_Update(BaseModel):
    id_course: int
    id_teacher: int
  
class CT_Create(BaseModel):
    id_course: int
    id_teacher: int

