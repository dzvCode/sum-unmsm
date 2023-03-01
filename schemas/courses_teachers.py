from pydantic import BaseModel

class CT(BaseModel):
    id_course: int
    id_teacher: int

class CTUpdate(BaseModel):
    id_course: int
  


