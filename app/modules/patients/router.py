
# =======================
# File: app/modules/patients/router.py
# Path: app/modules/patients/router.py
# =======================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from database.models import Patient, Doctor, Insurance
from utils.ai_service import AIService
from pydantic import BaseModel
from typing import List, Optional

patients_router = APIRouter()

class PatientProfile(BaseModel):
    name: str
    age: int
    gender: str
    location: str
    medical_history: Optional[str] = None
    family_members: int = 1
    monthly_income: Optional[float] = None

@patients_router.get("/profile/{patient_id}")
async def get_patient_profile(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@patients_router.put("/profile/{patient_id}")
async def update_patient_profile(
    patient_id: int, 
    profile_data: PatientProfile, 
    db: Session = Depends(get_db)
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    for key, value in profile_data.dict().items():
        setattr(patient, key, value)
    
    db.commit()
    db.refresh(patient)
    return patient

@patients_router.get("/doctors/available")
async def get_available_doctors(
    location: Optional[str] = None,
    specialization: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Doctor).filter(Doctor.is_available == True)
    
    if location:
        query = query.filter(Doctor.location.ilike(f"%{location}%"))
    if specialization:
        query = query.filter(Doctor.specialization.ilike(f"%{specialization}%"))
    
    doctors = query.all()
    return doctors

@patients_router.get("/insurance-recommendations/{patient_id}")
async def get_insurance_recommendations(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Prepare patient profile for AI
    patient_profile = {
        "age": patient.age,
        "location": patient.location,
        "family_members": patient.family_members,
        "monthly_income": patient.monthly_income,
        "medical_history": patient.medical_history
    }
    
    # Get AI recommendations
    ai_recommendations = AIService.recommend_insurance(patient_profile)
    
    # Get available insurance plans from database
    insurance_plans = db.query(Insurance).all()
    
    return {
        "ai_recommendations": ai_recommendations,
        "available_plans": insurance_plans
    }

@patients_router.get("/government-schemes/{patient_id}")
async def get_government_schemes(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient_profile = {
        "age": patient.age,
        "gender": patient.gender,
        "family_members": patient.family_members,
        "monthly_income": patient.monthly_income
    }
    
    schemes = AIService.find_government_schemes(patient.location, patient_profile)
    return schemes
