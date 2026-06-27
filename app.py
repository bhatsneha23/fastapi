from fastapi import FastAPI
from pydantic import BaseModel , Field , computed_field
from typing import Literal ,Annotated
import pickle
import pandas as pd
from fastapi.responses import JSONResponse

with open("model.pkl" ,'rb') as f:
    model  = pickle.load(f)

app = FastAPI()

tier_1_cities = {"mumbai", "delhi", "bangalore", "chennai", "kolkata"}
tier_2_cities = {"pune", "hyderabad", "ahmedabad", "surat", "jaipur"}

class UserInput(BaseModel):
    age: Annotated[int,Field(...,gt = 0 , lt = 120 , description = "age of the user")]
    weight: Annotated[float,Field(...,gt = 0 , description = "weight of the user")]
    height: Annotated[float,Field(...,gt = 0 , description = "height of the user")]
    income_lpa: Annotated[float,Field(...,gt = 0 , description = "income of the user")]
    smoker: Annotated[bool,Field(... , description = "is the user smoker")]
    city: Annotated[str,Field(... , description = "the city that the user belongs to")]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'],Field(..., description = "occupation of the user")]
    

@computed_field
@property
def bmi(self) -> float:        #here name of function should be same as the name of the field
    return self.weight/(self.height**2)

@computed_field
@property
def lifestyle_risk(self) -> str:
    if self.smoker and self.bmi > 30:
        return "high"
    elif self.smoker or self.bmi > 27:
        return "medium"
    else:
        return "low"

@computed_field
@property
def age_group(self) -> str:
    if self.age < 25:
        return "young"
    elif self.age <60:
        return "adult"
    elif self.age < 60:
        return "middle_aged"
    return "senior"

@computed_field
@property
def city_tier(self) -> int:
    if self.city in tier_1_cities:
        return 1
    elif self.city in tier_2_cities:
        return 2
    else:
        return 3
    

@app.post("/predict")
def predict_premium(data: UserInput):

    input_df = pd.DataFrame([{
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }])

    prediction = model.predict(input_df)[0]
    return JSONResponse(status_code = 200 , content = {'predicted_category' : prediction})

