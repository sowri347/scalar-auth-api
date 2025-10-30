import bcrypt
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional
import uuid
import hashlib
from time import time

from app.config import settings


def _prepare_password(password: str) -> bytes:
    """
    Prepare password for bcrypt hashing.
    If password exceeds 72 bytes, hash it first with SHA256.
    """
    password_bytes = password.encode('utf-8')
    
    # bcrypt has a 72-byte limit
    if len(password_bytes) > 72:
        # Hash long passwords with SHA256 first
        return hashlib.sha256(password_bytes).hexdigest().encode('utf-8')
    
    return password_bytes


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt (handles passwords longer than 72 bytes)"""
    prepared_password = _prepare_password(password)
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(prepared_password, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its bcrypt hash"""
    try:
        prepared_password = _prepare_password(plain_password)
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(prepared_password, hashed_bytes)
    except Exception as e:
        print(f"Password verification error: {e}")
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow()
    })
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[str]:
    """Decode JWT token and return username"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        return username
    except JWTError:
        return None


def generate_user_id() -> str:
    """Generate a unique user ID"""
    timestamp = str(int(time() * 1000))
    unique_id = str(uuid.uuid4().hex[:6])
    return f"{timestamp}-{unique_id}"