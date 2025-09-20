
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
