from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json
#  1. THIS IMPORT IS NEW
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# --- 2. THIS ENTIRE BLOCK IS THE FIX ---
# It tells your backend to accept requests from your frontend
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "http://localhost:3000",    # <-- ADDED YOUR FRONTEND PORT
    "http://127.0.0.1:3000", # <-- ADDED YOUR FRONTEND PORT
    "null",  # This allows the HTML file to connect
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, PUT, DELETE
    allow_headers=["*"],
)
# --- End of Fix ---


class Patient(BaseModel):
    id: Annotated[str, Field(..., description="Unique ID of the patient", example="P001")]
    name: Annotated[str, Field(..., description='Name of the patient')]
    city: Annotated[str, Field(..., description='City of the patient')]
    age: Annotated[int, Field(..., description='Age of the patient', gt=0, lt=120)]
    gender: Annotated[Literal['male', 'female', 'other'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., description='Height of the patient in meters', gt=0)]
    weight: Annotated[float, Field(..., description='Weight of the patient in kgs', gt=0)]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height**2), 2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif 18.5 <= self.bmi < 25:
            return 'Normal weight'
        elif 25 <= self.bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'


class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female', 'other']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


def load_data():
    try:
        with open('patients.json', 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    return data


def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f, indent=4)
    return data


@app.get("/")
def hello():
    return {'Message': 'Patient Management system API'}


@app.get('/about')
def about():
    return {'Message': 'A fully Functional API to mange your patient records'}


@app.get('/view')
def view():
    data = load_data()
    return data


@app.get('/patients/{patient_id}')
def view_patient(patient_id: str = Path(..., description="ID of the patient in the DB", example='P001')):
    data = load_data()
    if patient_id in data:
        patient_data = data[patient_id]
        patient_data['id'] = patient_id
        try:
            patient_model = Patient(**patient_data)
            return patient_model.model_dump()
        except Exception:
             return patient_data
    raise HTTPException(status_code=404, detail="Patient not found")


@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description="Sort on the basis of height,weight, or bmi"),
                  order: str = Query('asc', description='sort in asc or desc order')):
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail=f'Invalid order select between this {order}')

    data = load_data()
    patients_list = []
    for patient_id, patient_data in data.items():
        patient_data['id'] = patient_id
        try:
            temp_patient = Patient(**patient_data)
            patient_data['bmi'] = temp_patient.bmi
            patient_data['verdict'] = temp_patient.verdict
        except Exception:
            patient_data['bmi'] = 0
            patient_data['verdict'] = "N/A"
            
        patients_list.append(patient_data)

    sort_order = True if order == 'desc' else False
    sorted_data = sorted(patients_list, key=lambda x: x.get(sort_by, 0), reverse=sort_order)
    return sorted_data


@app.post('/create')
def create_patient(patient: Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient id is already exists')
    
    data[patient.id] = patient.model_dump(exclude={'id'})
    save_data(data)
    return JSONResponse(status_code=201, content={'message': 'Patient record created successfully'})


@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    existing_patient_info = data[patient_id]
    updatated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updatated_patient_info.items():
        existing_patient_info[key] = value
    
    existing_patient_info['id'] = patient_id

    try:
        patient_pydantic = Patient(**existing_patient_info)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Validation error: {e}")

    data[patient_id] = patient_pydantic.model_dump(exclude={'id'})
    save_data(data)
    return JSONResponse(status_code=200, content={'message': 'Patient updated successfully'})


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=200, content={'message': 'Patient record deleted successfully'})

