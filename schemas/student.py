from pydantic import BaseModel


class Student(BaseModel):
    id: int
    name: str
    last_name: str

class CreateStudent(BaseModel):
    name: str
    last_name:str