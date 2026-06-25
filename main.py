from fastapi import FastAPI , Path , HTTPException , Query
import json 
from pydantic import BaseModel, Field , computed_field
from typing import Annotated ,Literal , Optional
from fastapi.responses import JSONResponse

app = FastAPI()


class Patient(BaseModel):
    id: Annotated[str, Field(...,description= 'ID of the patient' , example = 'P001')]
    name: Annotated[str, Field(...,description= 'name of the patient' )]
    city:Annotated[str, Field(...,description= 'city of the patient')]
    age: Annotated[int, Field(...,gt= 0 , lt= 120 ,description= 'age of the patient' )]
    gender: Annotated[Literal['male','female','other'],Field(...,description='Gender of theh patient')]
    height: Annotated[float, Field(...,gt=0 ,description= 'height of the patient')]
    weight: Annotated[float, Field(...,gt=0 ,description= 'weight of the patient')]
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi


    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'underweight'
        elif self.bmi < 25:
            return 'normal'
        elif self.bmi <30:
            return 'normal'
        else:
            return 'obese'
        

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default= None)]
    city:Annotated[Optional[str], Field(default= None)]
    age: Annotated[Optional[int], Field(default= None, gt = 0)]
    gender: Annotated[Optional[Literal['male','female','other']],Field(default= None)]
    height: Annotated[Optional[float], Field(default= None , gt = 0)]
    weight: Annotated[Optional[float], Field(default= None , gt = 0)]




def load_data():  #utility function
    with open('patients.json' , 'r') as f:
        data = json.load(f)
    return data
 
def save_data(data): #utility function
    with open('patients.json' ,'w') as f:
        return json.dump(data, f)
    




@app.get("/")   #object of the class FastAPI is app and we are using the decorator get to create a route for the root endpoint
def hello():
    return{'message':'Patient management system api'} 

@app.get('/about')
def about():
    return{'message':'fully functional api to manage your patients records'}  

@app.get("/contact")
def contact():
    return{'message':'you can contact us'}

@app.get('/view')
def view():
    data = load_data()
    return data
    
@app.get('/view/{patient_id}')
def view_patient(patient_id : str = Path(...,description = 'ID of the patient in the DB' , example = 'P001')):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    # return{'message' : 'patient not found'}
    raise HTTPException(status_code = 404 , detail = 'Patient not found')

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description = 'sort on the basis of height , weight or bmi' ), order: str = Query('asc', description = 'sort in asc or desc order' )):
    valid_fields =  ['height' , 'weight' , 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code = 400 , detail = f'Invalid field select from {valid_fields}')
    
    if order not in ['asc' , 'desc']:
        raise HTTPException(status_code = 400 , detail = 'Invalid order select between asc and desc')
    
    data = load_data()
   
    sort_order = True if order =='desc' else False

    sorted_data = sorted(data.values() , key = lambda x: x.get(sort_by , 0) , reverse = sort_order)

    return sorted_data

@app.post('/create')
def create_patient(patient: Patient): #patient is the object of the class patient and we are using it to get the data from the request body

    #load the data from the json file
    data = load_data()  #dictionary

    #check if the patient already exist or not
    if patient.id in data:
        raise HTTPException(status_code = 400 , detail = 'Patient already exists')
    
    #new patient to add in database , but first we need to convert pydantic object to dictionary using model_dump
    data[patient.id] = patient.model_dump(exclude =['id'])

    #save into the json file
    save_data(data)

    return JSONResponse(status_code = 201 , content = {'message':'Patient created succesfully'})

@app.put('/edit/{patient_id}')
def update_patient(patient_id: str , patient_update = PatientUpdate):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code = 404 , detail = 'Patient not found')
    
    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset = True)

    for key,value in updated_patient_info.items():
        existing_patient_info[key] = value

    existing_patient_info
