from pydantic import BaseModel

class Course(BaseModel):
    id: str
    name: str
    weight: int
    cycle: int