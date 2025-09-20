
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