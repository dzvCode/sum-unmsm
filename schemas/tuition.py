from pydantic import BaseModel
import datetime

class Tuition(BaseModel):
    id_student: int
    id_course: int
    score: float
    date: datetime.date
    
class Tuition_Update(BaseModel):
    id_student: int
    id_course: int
    score: float
    
class Tuition_Create(BaseModel):
    id_student: int
    id_course: int
    score: float
    date: datetime.date
