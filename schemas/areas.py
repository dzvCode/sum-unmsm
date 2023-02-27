from pydantic import BaseModel

class Area(BaseModel):
    name: str

class AreaUpdate(BaseModel):
    name: str

class CreateArea(BaseModel):
    id: int
    name: str