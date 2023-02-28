from pydantic import BaseModel

class Headquarter(BaseModel):
    id: int
    name: str
    address: str