
# =======================
# File: app/modules/pharmacy/router.py
# Path: app/modules/pharmacy/router.py
# =======================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from database.models import Pharmacy, Medicine
from utils.ai_service import AIService
from pydantic import BaseModel
from typing import List, Optional

pharmacy_router = APIRouter()

class MedicineCreate(BaseModel):
    name: str
    generic_name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    usage: Optional[str] = None
    dosage: Optional[str] = None
    side_effects: Optional[str] = None
    price: Optional[float] = None

@pharmacy_router.get("/medicines")
async def get_medicines(
    search: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Medicine)
    
    if search:
        query = query.filter(Medicine.name.ilike(f"%{search}%"))
    if category:
        query = query.filter(Medicine.category == category)
    
    medicines = query.all()
    return medicines

@pharmacy_router.get("/medicines/{medicine_id}")
async def get_medicine_details(medicine_id: int, db: Session = Depends(get_db)):
    medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    
    # Get AI explanation
    medicine_details = {
        "name": medicine.name,
        "generic_name": medicine.generic_name,
        "category": medicine.category,
        "usage": medicine.usage,
        "dosage": medicine.dosage
    }
    
    ai_explanation = AIService.explain_medicine(medicine.name, medicine_details)
    
    return {
        "medicine": medicine,
        "ai_explanation": ai_explanation
    }

@pharmacy_router.post("/medicines")
async def add_medicine(
    medicine_data: MedicineCreate,
    pharmacy_id: int,
    db: Session = Depends(get_db)
):
    medicine = Medicine(**medicine_data.dict(), pharmacy_id=pharmacy_id)
    db.add(medicine)
    db.commit()
    db.refresh(medicine)
    return medicine
