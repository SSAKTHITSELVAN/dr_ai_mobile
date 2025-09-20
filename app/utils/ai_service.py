
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
