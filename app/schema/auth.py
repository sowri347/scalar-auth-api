from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=72)
    
    @field_validator('password')
    @classmethod
    def password_complexity(cls, v: str) -> str:
        if len(v.encode('utf-8')) > 72:
            raise ValueError('Password must be less than 72 bytes')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one number')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v

class UserResponse(UserBase):
    id: str
    created_at: datetime
    disabled: bool = False
    
    class Config:
        from_attributes = True

class UserInDB(UserResponse):
    hashed_password: str
