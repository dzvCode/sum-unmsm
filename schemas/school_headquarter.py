from pydantic import BaseModel
import datetime

class SHR(BaseModel):
    id_school: int
    id_headquarter: int
    
class SHRUpdate(BaseModel):
    id_headquarter: int
    
