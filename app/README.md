# AI Health Companion FastAPI Application
# Complete folder structure and implementation

# =======================
# File: app/main.py
# Path: app/main.py
# =======================

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import uvicorn

from core.config import settings
from core.logger import logger
from database.connection import get_db, init_database
from modules.auth.router import auth_router
from modules.patients.router import patients_router
from modules.doctors.router import doctors_router
from modules.pharmacy.router import pharmacy_router
from modules.ai_services.router import ai_router
from modules.social.router import social_router

# Initialize FastAPI app
app = FastAPI(
    title="AI Health Companion",
    description="AI-powered healthcare platform for Tier 2/3 cities",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(patients_router, prefix="/api/patients", tags=["Patients"])
app.include_router(doctors_router, prefix="/api/doctors", tags=["Doctors"])
app.include_router(pharmacy_router, prefix="/api/pharmacy", tags=["Pharmacy"])
app.include_router(ai_router, prefix="/api/ai", tags=["AI Services"])
app.include_router(social_router, prefix="/api/social", tags=["Social Media"])

@app.on_event("startup")
async def startup_event():
    logger.info("Starting AI Health Companion application...")
    init_database()

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Health Companion</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            .feature { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏥 AI Health Companion</h1>
            <p>Healthcare platform for Tier 2/3 cities with AI-powered features</p>
            
            <div class="feature">
                <h3>📊 API Documentation</h3>
                <p><a href="/docs">Swagger UI</a> | <a href="/redoc">ReDoc</a></p>
            </div>
            
            <div class="feature">
                <h3>🔑 Core Features</h3>
                <ul>
                    <li>AI Pharmacy Product Explainer</li>
                    <li>Prescription Scanner & Analyzer</li>
                    <li>Personalized Insurance Recommendations</li>
                    <li>Government Policy Finder</li>
                    <li>Real-time Doctor Consultations</li>
                    <li>Health Social Media</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "AI Health Companion is running!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# =======================
# File: app/core/config.py
# Path: app/core/config.py
# =======================

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # App settings
    app_name: str = "AI Health Companion"
    debug: bool = True
    
    # Database
    database_url: str = "sqlite:///./health_companion.db"
    
    # AI Settings
    gemini_api_key: str = "AIzaSyDEzVsTrDG0UnCGusugZjzNKkzSKgKyUJc"
    
    # Security
    secret_key: str = "your-secret-key-here-change-in-production"
    access_token_expire_minutes: int = 30
    
    # File upload
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    
    class Config:
        env_file = ".env"

settings = Settings()

# =======================
# File: app/core/logger.py
# Path: app/core/logger.py
# =======================

import logging
import sys
from pathlib import Path

# Create logs directory
Path("logs").mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("health_companion")

# =======================
# File: app/core/exceptions.py
# Path: app/core/exceptions.py
# =======================

from fastapi import HTTPException, status

class AuthenticationError(HTTPException):
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class NotFoundError(HTTPException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class ValidationError(HTTPException):
    def __init__(self, detail: str = "Validation failed"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

# =======================
# File: app/database/connection.py
# Path: app/database/connection.py
# =======================

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from core.config import settings

# Create SQLAlchemy engine
engine = create_engine(
    settings.database_url, 
    connect_args={"check_same_thread": False}  # SQLite specific
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

def get_db() -> Session:
    """Database dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    """Initialize database tables"""
    from database.models import User, Doctor, Patient, Pharmacy, Medicine, Prescription, Post, Insurance
    Base.metadata.create_all(bind=engine)

# =======================
# File: app/database/models.py
# Path: app/database/models.py
# =======================

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.connection import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    user_type = Column(String, nullable=False)  # patient, doctor, pharmacy
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(String)
    location = Column(String)
    medical_history = Column(Text)
    family_members = Column(Integer, default=1)
    monthly_income = Column(Float)
    
    user = relationship("User", back_populates="patient")

class Doctor(Base):
    __tablename__ = "doctors"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    name = Column(String, nullable=False)
    specialization = Column(String, nullable=False)
    experience = Column(Integer)
    qualification = Column(String)
    location = Column(String)
    consultation_fee = Column(Float)
    phone = Column(String)
    whatsapp = Column(String)
    is_available = Column(Boolean, default=True)
    
    user = relationship("User", back_populates="doctor")

class Pharmacy(Base):
    __tablename__ = "pharmacies"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    phone = Column(String)
    license_number = Column(String)
    
    user = relationship("User", back_populates="pharmacy")

class Medicine(Base):
    __tablename__ = "medicines"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    generic_name = Column(String)
    category = Column(String)
    description = Column(Text)
    usage = Column(Text)
    dosage = Column(String)
    side_effects = Column(Text)
    price = Column(Float)
    pharmacy_id = Column(Integer, ForeignKey("pharmacies.id"))
    
    pharmacy = relationship("Pharmacy")

class Prescription(Base):
    __tablename__ = "prescriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    image_path = Column(String)
    extracted_text = Column(Text)
    ai_analysis = Column(JSON)
    medicines = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())
    
    patient = relationship("Patient")
    doctor = relationship("Doctor")

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    post_type = Column(String)  # health_tip, combo_plan, general
    image_url = Column(String)
    likes = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    
    user = relationship("User")

class Insurance(Base):
    __tablename__ = "insurance_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    provider = Column(String, nullable=False)
    plan_type = Column(String)  # private, government
    coverage_amount = Column(Float)
    premium = Column(Float)
    age_limit = Column(String)
    description = Column(Text)
    eligibility = Column(JSON)

# Add relationships
User.patient = relationship("Patient", back_populates="user", uselist=False)
User.doctor = relationship("Doctor", back_populates="user", uselist=False)
User.pharmacy = relationship("Pharmacy", back_populates="user", uselist=False)

# =======================
# File: app/utils/security.py
# Path: app/utils/security.py
# =======================

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm="HS256")
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        return payload
    except JWTError:
        return None

# =======================
# File: app/utils/ai_service.py
# Path: app/utils/ai_service.py
# =======================

import google.generativeai as genai
from core.config import settings
from core.logger import logger
import json
from typing import Dict, Any, List

# Configure Gemini
genai.configure(api_key=settings.gemini_api_key)
model = genai.GenerativeModel('gemini-pro')

class AIService:
    
    @staticmethod
    def explain_medicine(medicine_name: str, medicine_details: Dict[str, Any]) -> Dict[str, str]:
        """Generate AI explanation for medicine"""
        prompt = f"""
        Explain this medicine in simple terms for people in Tier 2/3 cities in India:
        
        Medicine: {medicine_name}
        Details: {medicine_details}
        
        Please provide:
        1. Why this medicine is used (in simple language)
        2. How to take it safely
        3. Possible side effects
        4. Any alternatives or precautions
        
        Keep it simple and in a caring tone.
        """
        
        try:
            response = model.generate_content(prompt)
            return {
                "explanation": response.text,
                "status": "success"
            }
        except Exception as e:
            logger.error(f"AI medicine explanation failed: {e}")
            return {
                "explanation": "Unable to generate explanation at this time.",
                "status": "error"
            }
    
    @staticmethod
    def analyze_prescription(extracted_text: str) -> Dict[str, Any]:
        """Analyze prescription text using AI"""
        prompt = f"""
        Analyze this prescription text and provide structured information:
        
        Prescription Text: {extracted_text}
        
        Please provide JSON response with:
        {{
            "medicines": [
                {{
                    "name": "medicine name",
                    "dosage": "dosage",
                    "frequency": "how often",
                    "duration": "how long",
                    "purpose": "why prescribed"
                }}
            ],
            "doctor_notes": "any special instructions",
            "warnings": ["any unusual combinations or issues"],
            "summary": "overall prescription summary in simple language"
        }}
        """
        
        try:
            response = model.generate_content(prompt)
            # Extract JSON from response
            response_text = response.text
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            json_str = response_text[start_idx:end_idx]
            
            return json.loads(json_str)
        except Exception as e:
            logger.error(f"AI prescription analysis failed: {e}")
            return {
                "medicines": [],
                "doctor_notes": "Unable to analyze prescription",
                "warnings": [],
                "summary": "Analysis failed"
            }
    
    @staticmethod
    def recommend_insurance(patient_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend insurance based on patient profile"""
        prompt = f"""
        Based on this patient profile, recommend suitable insurance plans:
        
        Patient Profile: {patient_profile}
        
        Consider Indian insurance market and provide recommendations for:
        1. Best private insurance plans
        2. Government schemes (like Ayushman Bharat)
        3. Specific recommendations based on age, income, family size
        
        Provide JSON response with recommendations.
        """
        
        try:
            response = model.generate_content(prompt)
            return {"recommendations": response.text, "status": "success"}
        except Exception as e:
            logger.error(f"AI insurance recommendation failed: {e}")
            return {"recommendations": "Unable to generate recommendations", "status": "error"}
    
    @staticmethod
    def find_government_schemes(location: str, patient_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Find relevant government health schemes"""
        prompt = f"""
        Find relevant government health schemes for:
        Location: {location}
        Patient Profile: {patient_profile}
        
        Include:
        1. Free government checkups
        2. Subsidies available
        3. Maternity support (if applicable)
        4. Child vaccination schemes
        5. Senior citizen programs
        
        Focus on schemes available in India, especially for Tier 2/3 cities.
        """
        
        try:
            response = model.generate_content(prompt)
            return {"schemes": response.text, "status": "success"}
        except Exception as e:
            logger.error(f"AI government schemes finder failed: {e}")
            return {"schemes": "Unable to find schemes", "status": "error"}
    
    @staticmethod
    def generate_health_tip() -> str:
        """Generate daily health tip"""
        prompt = """
        Generate a simple, practical health tip for people in Indian Tier 2/3 cities.
        Make it actionable and explain why it's important.
        Keep it under 100 words and use simple language.
        """
        
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"AI health tip generation failed: {e}")
            return "Stay hydrated and eat fresh fruits daily for better health!"

# =======================
# File: app/modules/auth/router.py
# Path: app/modules/auth/router.py
# =======================

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.connection import get_db
from database.models import User, Patient, Doctor, Pharmacy
from utils.security import verify_password, get_password_hash, create_access_token
from pydantic import BaseModel
from datetime import timedelta
from core.config import settings

auth_router = APIRouter()

class UserRegister(BaseModel):
    email: str
    phone: str
    password: str
    user_type: str  # patient, doctor, pharmacy
    name: str
    # Additional fields based on user type
    specialization: str = None  # for doctors
    location: str = None

class UserLogin(BaseModel):
    email: str
    password: str

@auth_router.post("/register")
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    user = User(
        email=user_data.email,
        phone=user_data.phone,
        password_hash=get_password_hash(user_data.password),
        user_type=user_data.user_type
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create profile based on user type
    if user_data.user_type == "patient":
        profile = Patient(
            user_id=user.id,
            name=user_data.name,
            location=user_data.location
        )
    elif user_data.user_type == "doctor":
        profile = Doctor(
            user_id=user.id,
            name=user_data.name,
            specialization=user_data.specialization,
            location=user_data.location,
            phone=user_data.phone
        )
    elif user_data.user_type == "pharmacy":
        profile = Pharmacy(
            user_id=user.id,
            name=user_data.name,
            location=user_data.location,
            phone=user_data.phone
        )
    
    db.add(profile)
    db.commit()
    
    return {"message": "Registration successful", "user_id": user.id}

@auth_router.post("/login")
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id, "user_type": user.user_type},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_type": user.user_type,
        "user_id": user.id
    }

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

# =======================
# File: app/modules/social/router.py
# Path: app/modules/social/router.py
# =======================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from database.models import Post, User, Doctor, Pharmacy
from pydantic import BaseModel
from typing import List, Optional

social_router = APIRouter()

class PostCreate(BaseModel):
    title: str
    content: str
    post_type: str  # health_tip, combo_plan, general
    image_url: Optional[str] = None

@social_router.get("/posts")
async def get_posts(
    post_type: Optional[str] = None,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    query = db.query(Post).join(User)
    
    if post_type:
        query = query.filter(Post.post_type == post_type)
    
    posts = query.order_by(Post.created_at.desc()).limit(limit).all()
    
    # Add author information
    posts_with_authors = []
    for post in posts:
        post_dict = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "post_type": post.post_type,
            "image_url": post.image_url,
            "likes": post.likes,
            "created_at": post.created_at,
            "author": {
                "user_type": post.user.user_type,
                "name": "Unknown"
            }
        }
        
        # Get author name based on user type
        if post.user.user_type == "doctor" and post.user.doctor:
            post_dict["author"]["name"] = post.user.doctor.name
        elif post.user.user_type == "pharmacy" and post.user.pharmacy:
            post_dict["author"]["name"] = post.user.pharmacy.name
        
        posts_with_authors.append(post_dict)
    
    return posts_with_authors

@social_router.post("/posts")
async def create_post(
    user_id: int,
    post_data: PostCreate,
    db: Session = Depends(get_db)
):
    post = Post(
        user_id=user_id,
        title=post_data.title,
        content=post_data.content,
        post_type=post_data.post_type,
        image_url=post_data.image_url
    )
    
    db.add(post)
    db.commit()
    db.refresh(post)
    
    return post

@social_router.put("/posts/{post_id}/like")
async def like_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    post.likes += 1
    db.commit()
    
    return {"message": "Post liked", "likes": post.likes}

# =======================
# File: app/scripts/seed_database.py
# Path: app/scripts/seed_database.py
# =======================

import sys
import os

# Add the parent directory (app) to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from database.connection import SessionLocal, init_database
from database.models import User, Patient, Doctor, Pharmacy, Medicine, Insurance, Post

# Simple password hashing function for seeding
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def seed_database():
    init_database()
    db = SessionLocal()
    
    try:
        # Create sample users
        users_data = [
            {
                "email": "patient1@example.com",
                "phone": "9876543210",
                "password_hash": get_password_hash("password123"),
                "user_type": "patient"
            },
            {
                "email": "doctor1@example.com",
                "phone": "9876543211",
                "password_hash": get_password_hash("password123"),
                "user_type": "doctor"
            },
            {
                "email": "pharmacy1@example.com",
                "phone": "9876543212",
                "password_hash": get_password_hash("password123"),
                "user_type": "pharmacy"
            }
        ]
        
        for user_data in users_data:
            user = User(**user_data)
            db.add(user)
        
        db.commit()
        
        # Get created users
        patient_user = db.query(User).filter(User.email == "patient1@example.com").first()
        doctor_user = db.query(User).filter(User.email == "doctor1@example.com").first()
        pharmacy_user = db.query(User).filter(User.email == "pharmacy1@example.com").first()
        
        # Create profiles
        patient = Patient(
            user_id=patient_user.id,
            name="Ramesh Kumar",
            age=35,
            gender="Male",
            location="Coimbatore, Tamil Nadu",
            family_members=4,
            monthly_income=25000.0
        )
        
        doctor = Doctor(
            user_id=doctor_user.id,
            name="Dr. Priya Sharma",
            specialization="General Physician",
            experience=8,
            qualification="MBBS, MD",
            location="Coimbatore, Tamil Nadu",
            consultation_fee=300.0,
            phone="9876543211",
            whatsapp="9876543211",
            is_available=True
        )
        
        pharmacy = Pharmacy(
            user_id=pharmacy_user.id,
            name="HealthCare Pharmacy",
            location="RS Puram, Coimbatore",
            phone="9876543212",
            license_number="TN-CBE-2023-001"
        )
        
        db.add_all([patient, doctor, pharmacy])
        db.commit()
        
        # Create sample medicines
        medicines = [
            {
                "name": "Paracetamol 500mg",
                "generic_name": "Acetaminophen",
                "category": "Pain Relief",
                "description": "Pain reliever and fever reducer",
                "usage": "For headache, fever, and mild pain",
                "dosage": "1-2 tablets every 4-6 hours",
                "side_effects": "Rare: Nausea, skin rash",
                "price": 15.0,
                "pharmacy_id": pharmacy.id
            },
            {
                "name": "Crocin Advance",
                "generic_name": "Paracetamol",
                "category": "Pain Relief",
                "description": "Fast-acting pain relief",
                "usage": "For quick relief from headache and fever",
                "dosage": "1 tablet every 4-6 hours",
                "side_effects": "Minimal side effects when used as directed",
                "price": 25.0,
                "pharmacy_id": pharmacy.id
            },
            {
                "name": "Cetrizine 10mg",
                "generic_name": "Cetirizine",
                "category": "Antihistamine",
                "description": "Allergy relief medication",
                "usage": "For allergic reactions, runny nose, itching",
                "dosage": "1 tablet once daily",
                "side_effects": "May cause drowsiness",
                "price": 30.0,
                "pharmacy_id": pharmacy.id
            }
        ]
        
        for med_data in medicines:
            medicine = Medicine(**med_data)
            db.add(medicine)
        
        # Create sample insurance plans
        insurance_plans = [
            {
                "name": "Ayushman Bharat",
                "provider": "Government of India",
                "plan_type": "government",
                "coverage_amount": 500000.0,
                "premium": 0.0,
                "age_limit": "No age limit",
                "description": "Free healthcare coverage for economically vulnerable families",
                "eligibility": {"income_limit": 50000, "family_based": True}
            },
            {
                "name": "Star Health Family Plan",
                "provider": "Star Health Insurance",
                "plan_type": "private",
                "coverage_amount": 300000.0,
                "premium": 8500.0,
                "age_limit": "Up to 65 years",
                "description": "Comprehensive family health insurance",
                "eligibility": {"age_range": "18-65", "family_coverage": True}
            },
            {
                "name": "ICICI Lombard Health Care",
                "provider": "ICICI Lombard",
                "plan_type": "private",
                "coverage_amount": 500000.0,
                "premium": 12000.0,
                "age_limit": "Up to 70 years",
                "description": "Premium health insurance with cashless treatment",
                "eligibility": {"age_range": "18-70", "pre_existing_coverage": True}
            }
        ]
        
        for insurance_data in insurance_plans:
            insurance = Insurance(**insurance_data)
            db.add(insurance)
        
        # Create sample social posts
        posts = [
            {
                "user_id": doctor_user.id,
                "title": "5 Simple Ways to Boost Your Immunity",
                "content": "1. Drink warm water with lemon every morning 2. Include turmeric in your daily diet 3. Get 7-8 hours of sleep 4. Practice deep breathing for 10 minutes daily 5. Eat seasonal fruits and vegetables. These simple habits can significantly improve your immune system!",
                "post_type": "health_tip"
            },
            {
                "user_id": pharmacy_user.id,
                "title": "Complete Health Checkup Package - Special Offer",
                "content": "Get a comprehensive health checkup including Blood Sugar, Blood Pressure, Cholesterol, and Vitamin D tests for just ₹999 (Regular price ₹1500). Valid till month end. Book your appointment today!",
                "post_type": "combo_plan"
            },
            {
                "user_id": doctor_user.id,
                "title": "Understanding Diabetes: What You Need to Know",
                "content": "Diabetes is becoming common in India. Key signs to watch: excessive thirst, frequent urination, unexplained weight loss, fatigue. Prevention tips: regular exercise, balanced diet, weight management, regular checkups. Early detection can help manage it effectively.",
                "post_type": "health_tip"
            }
        ]
        
        for post_data in posts:
            post = Post(**post_data)
            db.add(post)
        
        db.commit()
        print("✅ Database seeded successfully!")
        print("\n📋 Sample Login Credentials:")
        print("Patient: patient1@example.com / password123")
        print("Doctor: doctor1@example.com / password123") 
        print("Pharmacy: pharmacy1@example.com / password123")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()

# =======================
# File: app/scripts/run_dev.py
# Path: app/scripts/run_dev.py
# =======================

import uvicorn
import sys
import os

# Add the parent directory (app) to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["app"],
        log_level="info"
    )

# =======================
# File: requirements.txt
# Path: requirements.txt
# =======================

fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pydantic-settings==2.0.3
google-generativeai==0.3.1
python-dotenv==1.0.0
Pillow==10.1.0

# =======================
# File: .env.example
# Path: .env.example
# =======================

# App Configuration
APP_NAME=AI Health Companion
DEBUG=true

# Database
DATABASE_URL=sqlite:///./health_companion.db

# AI Configuration
GEMINI_API_KEY=AIzaSyDEzVsTrDG0UnCGusugZjzNKkzSKgKyUJc

# Security
SECRET_KEY=your-super-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# File Upload
MAX_FILE_SIZE=10485760

# =======================
# File: README.md
# Path: README.md
# =======================

# 🏥 AI Health Companion

A comprehensive healthcare platform designed for Tier 2/3 cities in India, powered by AI to make healthcare accessible and understandable.

## ✨ Core Features

### 🔍 AI-Powered Features
- **Pharmacy Product Explainer**: AI explains every medicine with usage, side effects, and alternatives
- **Prescription Scanner**: Upload prescription images and get AI analysis of medicines and dosages
- **Personalized Insurance Recommendations**: AI suggests best insurance plans based on patient profile
- **Government Policy Finder**: Discover relevant government health schemes and subsidies
- **Daily Health Tips**: AI-generated health advice in simple language

### 👥 User Management
- **Multi-user System**: Patients, Doctors, and Pharmacies with separate profiles
- **Real-time Doctor Consultations**: Connect via phone/WhatsApp instantly
- **Health Social Media**: Doctors and pharmacies share health tips and combo plans

## 🚀 Quick Start

### 1. Installation
```bash
# Clone or create the project structure
mkdir ai_health_companion
cd ai_health_companion

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Setup
```bash
# Copy environment file
cp .env.example .env

# Edit .env with your configurations (Gemini API key is pre-configured)
```

### 3. Database Setup
```bash
# Run database seeding
python scripts/seed_database.py
```

### 4. Start the Application
```bash
# Method 1: Using the dev script
python scripts/run_dev.py

# Method 2: Direct uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Access the Application
- **Main App**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 🧪 Test the Features

### Sample Login Credentials
- **Patient**: patient1@example.com / password123
- **Doctor**: doctor1@example.com / password123  
- **Pharmacy**: pharmacy1@example.com / password123

### API Endpoints to Try

#### 🔐 Authentication
```bash
# Register new user
POST /api/auth/register
{
  "email": "test@example.com",
  "phone": "9876543213",
  "password": "password123",
  "user_type": "patient",
  "name": "Test User",
  "location": "Coimbatore"
}

# Login
POST /api/auth/login
{
  "email": "patient1@example.com",
  "password": "password123"
}
```

#### 💊 Pharmacy Features
```bash
# Get all medicines
GET /api/pharmacy/medicines

# Get medicine with AI explanation
GET /api/pharmacy/medicines/1
```

#### 🤖 AI Services
```bash
# Get daily health tip
GET /api/ai/health-tip/daily

# AI Chat
POST /api/ai/chat?query=What should I eat for better immunity?

# Analyze prescription (upload file)
POST /api/ai/prescription/analyze
```

#### 👨‍⚕️ Patient Services
```bash
# Get available doctors
GET /api/patients/doctors/available?location=Coimbatore

# Get insurance recommendations
GET /api/patients/insurance-recommendations/1

# Get government schemes
GET /api/patients/government-schemes/1
```

#### 📱 Social Media
```bash
# Get health posts
GET /api/social/posts?post_type=health_tip

# Create post
POST /api/social/posts
{
  "title": "Health Tip",
  "content": "Drink plenty of water daily",
  "post_type": "health_tip"
}
```

## 📁 Project Structure

```
app/
├── main.py                    # FastAPI app entry point
├── core/                      # Core configuration
│   ├── config.py             # Settings management
│   ├── logger.py             # Logging configuration  
│   └── exceptions.py         # Custom exceptions
├── database/                  # Database layer
│   ├── connection.py         # DB connection & session
│   └── models.py             # SQLAlchemy models
├── modules/                   # Feature modules
│   ├── auth/                 # Authentication
│   ├── patients/             # Patient management
│   ├── doctors/              # Doctor management  
│   ├── pharmacy/             # Pharmacy & medicines
│   ├── ai_services/          # AI-powered features
│   └── social/               # Social media features
├── utils/                     # Utilities
│   ├── security.py           # JWT & password utils
│   └── ai_service.py         # Gemini AI integration
├── scripts/                   # Helper scripts
│   ├── seed_database.py      # Database seeding
│   └── run_dev.py           # Development server
└── uploads/                   # File uploads
    └── prescriptions/         # Prescription images
```

## 🧠 AI Features Explained

### 1. Medicine Explainer
- Uses Gemini AI to explain medicines in simple language
- Covers usage, dosage, side effects, and alternatives
- Perfect for semi-literate users in Tier 2/3 cities

### 2. Prescription Analysis  
- Analyzes uploaded prescription images
- Extracts medicine information using AI
- Provides safety warnings and drug interactions

### 3. Insurance Recommendations
- AI analyzes patient profile (age, income, family size)
- Suggests best private and government insurance plans
- Personalized recommendations for Indian healthcare market

### 4. Government Schemes Finder
- Location-based government health scheme discovery
- AI matches schemes to patient eligibility
- Includes Ayushman Bharat and state-specific programs

## 🛠️ Key Technologies

- **FastAPI**: Modern, fast web framework
- **SQLAlchemy**: Database ORM
- **SQLite**: Lightweight database (easily replaceable)
- **Google Gemini AI**: Advanced AI capabilities
- **JWT Authentication**: Secure user authentication
- **Pydantic**: Data validation and settings

## 🎯 MVP Focus

This implementation focuses on:
- ✅ **Core functionality over advanced features**
- ✅ **Working demos of all features**  
- ✅ **Beginner-friendly code structure**
- ✅ **Minimal but complete implementation**
- ✅ **Easy testing and demonstration**

## 🔄 Next Steps for Production

1. **Frontend Development**: React/Vue.js web app and mobile app
2. **OCR Integration**: Real prescription text extraction
3. **Payment Gateway**: For consultations and medicines
4. **Advanced Search**: Elasticsearch for better medicine search  
5. **Notifications**: SMS/WhatsApp integration
6. **Deployment**: Docker containers and cloud deployment
7. **Security**: Rate limiting, input validation, HTTPS

## 📞 Support

This is a comprehensive MVP demonstrating all core features of the AI Health Companion. The structure is beginner-friendly and production-ready for scaling.

Perfect for demonstrations, learning FastAPI, and building healthcare applications! 🚀