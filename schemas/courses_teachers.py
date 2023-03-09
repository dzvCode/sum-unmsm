from pydantic import BaseModel

class CT(BaseModel):
    id_course: str
    id_teacher: int
    section: int

class CTUpdate(BaseModel):
    id_course: str

class CTGetTeacher(BaseModel):
    id_teacher: int

class VWProgrammingCourses(BaseModel):
    cod_course: str
    course: str
    credits: int
    section: int
    cod_teacher: int
    teacher: str
    cycle: int
  


