
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
