from pydantic import BaseModel
import datetime

class Tuition(BaseModel):
    id_student: int
    id_course: str
    id_teacher: int
    section: int
    score: float
    date: datetime.date

class VW_TuitionAll(BaseModel):
    cod_estudiante: int
    ciclo: int
    cod_curso: str
    asignatura: str
    creditos: int
    seccion: int
    docente: str


class VW_TuitionID(BaseModel):
    ciclo: int
    cod_curso: str
    asignatura: str
    creditos: int
    seccion: int
    docente: str

class TuitionCreate(BaseModel):
    id_student: int
    id_course: str
    id_teacher: int
    section: int
    
class TuitionUpdate(BaseModel):
    id_student: int
    id_course: int
    score: float
    

