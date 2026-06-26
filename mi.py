from fastapi import FastAPI , Path , HTTPException , Query
import json 
from pydantic import BaseModel, Field , computed_field
from typing import Annotated ,Literal , Optional
from fastapi.responses import JSONResponse

app = FastAPI()

def load_data():
    with open('patients.json' ,'r') as f :
        data = json.load(f)
    return data 

@app.get('/view')
def view():
    data = load_data()
    return data


@app.get('/view/{patient_id}')
def view_patient(patient_id: str):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    return {'message' : 'patient not found'}

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default= None)]
    city:Annotated[Optional[str], Field(default= None)]
    age: Annotated[Optional[int], Field(default= None, gt = 0)]
    gender: Annotated[Optional[Literal['male','female','other']],Field(default= None)]
    height: Annotated[Optional[float], Field(default= None , gt = 0)]
    weight: Annotated[Optional[float], Field(default= None , gt = 0)]

@app.put('edit/{patient_id}')
def update_patient(patient_id: str , patient_update = PatientUpdate):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code = 404 , detail = 'Patient not found')
    
    existing_patient_info = data[patient_id]
    
    updated_patient_info = patient_update.model_dump(exclude_unset = True)
