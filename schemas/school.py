from pydantic import BaseModel

class School(BaseModel):
    name: str

class SchoolUpdate(BaseModel):
    name: str

class CreateSchool(BaseModel):
    id: int
    name: str
    id_facultad: int