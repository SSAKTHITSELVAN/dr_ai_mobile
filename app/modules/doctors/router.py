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
from modules.auth.dependencies import get_current_user # CORRECTED: Import dependency

doctors_router = APIRouter()

# ... DoctorProfile model is the same ...
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

@doctors_router.put("/profile/me") # CORRECTED: Changed endpoint to /me for security
async def update_my_doctor_profile(
    profile_data: DoctorProfile, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # CORRECTED: Protected endpoint
):
    if current_user.user_type != "doctor" or not current_user.doctor:
        raise HTTPException(status_code=403, detail="Not authorized")

    doctor = current_user.doctor
    
    for key, value in profile_data.dict(exclude_unset=True).items():
        setattr(doctor, key, value)
    
    db.commit()
    db.refresh(doctor)
    return doctor

@doctors_router.put("/availability/me") # CORRECTED: Changed endpoint to /me
async def toggle_my_availability(
    available: bool, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # CORRECTED: Protected endpoint
):
    if current_user.user_type != "doctor" or not current_user.doctor:
        raise HTTPException(status_code=403, detail="Not authorized")

    doctor = current_user.doctor
    doctor.is_available = available
    db.commit()
    
    return {"message": f"Availability set to {available}", "is_available": available}