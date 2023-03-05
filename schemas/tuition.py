from pydantic import BaseModel
import datetime

class Tuition(BaseModel):
    id_student: int
    id_course: int
    score: float
    date: datetime.date
    
class TuitionUpdate(BaseModel):
    id_student: int
    id_course: int
    score: float
    
class TuitionCreate(BaseModel):
    id_student: int
    id_course: int
    score: float
    date: datetime.date
