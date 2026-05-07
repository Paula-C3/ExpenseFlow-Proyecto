from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

from app.domain.enums import RoleType


class UserLogin(BaseModel):
    """Schema para login."""
    email: EmailStr
    password: str


class UserRegister(BaseModel):
    """Schema para registro."""
    email: EmailStr
    password: str
    full_name: str


class TokenResponse(BaseModel):
    """Response con token JWT."""
    access_token: str
    token_type: str = "bearer"
    role: str
    user_id: int


class UserResponse(BaseModel):
    """Response con datos de usuario."""
    id: int
    email: str
    full_name: str
    role_id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
