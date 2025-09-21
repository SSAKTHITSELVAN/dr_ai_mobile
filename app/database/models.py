# =======================
# File: app/database/models.py
# Path: app/database/models.py
# =======================

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .connection import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    user_type = Column(String, nullable=False)  # patient, doctor, pharmacy
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    
    # --- CORRECTED RELATIONSHIPS ---
    patient = relationship("Patient", back_populates="user", uselist=False, cascade="all, delete-orphan")
    doctor = relationship("Doctor", back_populates="user", uselist=False, cascade="all, delete-orphan")
    pharmacy = relationship("Pharmacy", back_populates="user", uselist=False, cascade="all, delete-orphan")
    posts = relationship("Post", back_populates="user")


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
    
    user = relationship("User", back_populates="posts")

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