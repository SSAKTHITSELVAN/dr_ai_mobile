
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
