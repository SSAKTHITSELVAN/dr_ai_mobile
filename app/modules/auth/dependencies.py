# =======================
# File: app/modules/auth/dependencies.py
# Path: app/modules/auth/dependencies.py
# =======================

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError
from pydantic import BaseModel

from database.connection import get_db
from database.models import User
from utils.security import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

class TokenData(BaseModel):
    email: str | None = None
    user_id: int | None = None

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id = payload.get("user_id")
    if user_id is None:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    return user