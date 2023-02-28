from pydantic import BaseModel
import datetime

class SHR(BaseModel):
    id_school: int
    id_headquarter: int
    
class SHR_Update(BaseModel):
    id_school: int
    id_headquarter: int

    
class SHR_Create(BaseModel):
    id_school: int
    id_headquarter: int
