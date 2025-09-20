
# =======================
# File: app/modules/doctors/router.py
# Path: app/modules/doctors/router.py
# =======================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from database.models import Doctor, User
from pydantic import BaseModel
from typing import Optional

doctors_router = APIRouter()

class DoctorProfile(BaseModel):
    name: str
    specialization: str
    experience: Optional[int] = None
    qualification: Optional[str] = None
    location: str
    consultation_fee: Optional[float] = None
    phone: Optional[str] = None
    whatsapp: Optional[str] = None

@doctors_router.get("/profile/{doctor_id}")
async def get_doctor_profile(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@doctors_router.put("/profile/{doctor_id}")
async def update_doctor_profile(
    doctor_id: int, 
    profile_data: DoctorProfile, 
    db: Session = Depends(get_db)
):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    for key, value in profile_data.dict().items():
        setattr(doctor, key, value)
    
    db.commit()
    db.refresh(doctor)
    return doctor

@doctors_router.put("/availability/{doctor_id}")
async def toggle_availability(doctor_id: int, available: bool, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    doctor.is_available = available
    db.commit()
    
    return {"message": f"Availability set to {available}", "is_available": available}
