from pydantic import BaseModel , EmailStr , AnyUrl ,Field  #field for meta data
from typing import List , Dict , Optional , Annotated

#annotated for extra details about the field and also for validation purpose
 
class Patient(BaseModel):
       name: Annotated[str , Field(max_length = 50 , title = 'Name of the patient' , description ='Give the name of the patient in less than 50 characters' , examples = ['sneha', 'ronak'])]
       email: EmailStr
       url: AnyUrl
       age: int
       weight: Annotated[float , Field(gt = 0 , strict = True)]
       married: Annotated[bool , Field(default = None , description = 'Is the patient married or not')]
       allergies: Annotated[Optional[List[str]] , Field(default = None ,max_length=5)]
       contact_details: Dict[str , str]
       
def insert_patient_data (patient : Patient):          
    print(patient.name)
    print(patient.age) 
    print(patient.contact_details)
    print(patient.allergies)
    print(patient.email)
    print('inserted into database')

def update_patient_data (patient : Patient):          
    print(patient.name)
    print(patient.age)
    print('updated in database')
    

patient_info = {'name' : 'sneha' ,'email':'bhat@gmail.com','url':'https://linkedin.com/13222222' ,'age' : '19' , 'weight' :47.3 ,'married': False ,  'contact_details': { 'phone': '6230707794'}}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)