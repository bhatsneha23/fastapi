from pydantic import BaseModel , EmailStr , AnyUrl ,Field , field_validator
from typing import List , Dict , Optional , Annotated

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight : float
    married: bool
    allergies:List[str]
    contact_details: Dict[str , str]

    @field_validator('email')
    @classmethod
    def email_validator(cls , value):       