
# =======================
# File: app/modules/ai_services/router.py
# Path: app/modules/ai_services/router.py
# =======================

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database.connection import get_db
from database.models import Prescription, Patient
from utils.ai_service import AIService
from pydantic import BaseModel
import os
import uuid

ai_router = APIRouter()

@ai_router.post("/prescription/analyze")
async def analyze_prescription(
    patient_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Create uploads directory if it doesn't exist
    os.makedirs("uploads/prescriptions", exist_ok=True)
    
    # Save uploaded file
    file_extension = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = f"uploads/prescriptions/{filename}"
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # For demo, simulate OCR text extraction
    extracted_text = f"Sample prescription text from {file.filename}"
    
    # Analyze with AI
    ai_analysis = AIService.analyze_prescription(extracted_text)
    
    # Save prescription record
    prescription = Prescription(
        patient_id=patient_id,
        image_path=file_path,
        extracted_text=extracted_text,
        ai_analysis=ai_analysis,
        medicines=ai_analysis.get("medicines", [])
    )
    
    db.add(prescription)
    db.commit()
    db.refresh(prescription)
    
    return {
        "prescription_id": prescription.id,
        "extracted_text": extracted_text,
        "analysis": ai_analysis
    }

@ai_router.get("/health-tip/daily")
async def get_daily_health_tip():
    tip = AIService.generate_health_tip()
    return {"tip": tip, "type": "daily_health_tip"}

@ai_router.post("/chat")
async def ai_chat(query: str):
    # Simple AI chat for health queries
    prompt = f"""
    You are a helpful health assistant for people in Tier 2/3 cities in India.
    Answer this health-related query in simple language: {query}
    
    Keep the response practical and actionable.
    """
    
    try:
        import google.generativeai as genai
        genai.configure(api_key="AIzaSyDEzVsTrDG0UnCGusugZjzNKkzSKgKyUJc")
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return {"response": response.text}
    except Exception as e:
        return {"response": "I'm sorry, I couldn't process your query right now. Please try again later."}
