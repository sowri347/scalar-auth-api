from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None
    exp: Optional[datetime] = None

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=100)
    disabled: bool = False

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=72)  # Added max_length=72
    
    @validator('password')
    def password_complexity(cls, v):
        if len(v.encode('utf-8')) > 72:  # Check byte length
            raise ValueError('Password must be less than 72 bytes')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one number')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v

class UserLogin(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)

class User(UserBase):
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True  # Changed from orm_mode = True

class UserInDB(User):
    hashed_password: str