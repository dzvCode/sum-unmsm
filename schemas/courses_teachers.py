from pydantic import BaseModel

class CT(BaseModel):
    id_course: str
    id_teacher: int
    section: int

class CTUpdate(BaseModel):
    id_course: int
  


