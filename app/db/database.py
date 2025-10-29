from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime
from typing import Optional
from bson.objectid import ObjectId

from ..schema.login_schemas import UserInDB, TokenData, User

# MongoDB Configuration
MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
database = client.user_db
user_collection = database.users

# Security Configuration
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

# OAuth2 scheme for token
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
    auto_error=True
)

async def connect_to_mongo():
    try:
        await client.admin.command('ping')
        print("✅ Connected to MongoDB")
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        raise

async def get_user_by_username(username: str) -> Optional[UserInDB]:
    """Retrieve user from database by username"""
    try:
        if user_dict := await user_collection.find_one({"username": username}):
            # Convert MongoDB _id to string id
            user_dict['id'] = str(user_dict.pop('_id'))
            print(f"Found user: {user_dict}")  # Debug log
            return UserInDB(**user_dict)
        print(f"No user found with username: {username}")  # Debug log
        return None
    except Exception as e:
        print(f"Error retrieving user: {str(e)}")  # Debug log
        return None

async def get_user_by_id(user_id: str) -> Optional[UserInDB]:
    """Retrieve user from database by ID"""
    if user_dict := await user_collection.find_one({"id": user_id}):  # Changed from _id to id
        return UserInDB(**user_dict)
    return None

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    """Dependency to get current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    # Get user from database
    user = await get_user_by_username(username=token_data.username)
    if user is None:
        raise credentials_exception
        
    return user

async def get_current_active_user(
    current_user: UserInDB = Depends(get_current_user)
) -> User:
    """Dependency to get current active user"""
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

# Database utilities
async def create_indexes():
    """Create database indexes"""
    await user_collection.create_index("id", unique=True)  # Index on user id

    await user_collection.create_index("username", unique=True)
