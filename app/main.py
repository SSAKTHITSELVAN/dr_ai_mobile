
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

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
