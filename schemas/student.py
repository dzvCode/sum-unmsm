from pydantic import BaseModel

class Student(BaseModel):
    id: int
    name: str
    email: str

class CreateStudent(BaseModel):
    id: int
    name: str
    email: str
    phone: int
    id_school: int