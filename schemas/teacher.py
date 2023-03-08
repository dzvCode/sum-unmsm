
from pydantic import BaseModel

class Teacher(BaseModel):
    id: int
    name: str
    degree: str
    email: str
    phone: int

class CreateTeacher(BaseModel):
    id: int
    name: str
    degree: str
    email: str
    phone: int
    id_school: int