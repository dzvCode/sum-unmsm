from pydantic import BaseModel

class Faculty(BaseModel):
    name: str

class FacultyUpdate(BaseModel):
    name: str

class CreateFaculty(BaseModel):
    id: int
    name: str
    id_area: int