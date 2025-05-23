from pydantic import BaseModel, Field
from datetime import date
 
class User(BaseModel):
    id: int
    name: str
    dob: date = Field(title="Date of Birth")