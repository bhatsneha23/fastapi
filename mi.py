from fastapi import FastAPI , Path , HTTPException , Query 
import json

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


    
