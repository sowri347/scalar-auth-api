from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional

from app.config import settings
from app.schema.auth import UserInDB, TokenData
from app.core.security import decode_token

# MongoDB client
client: Optional[AsyncIOMotorClient] = None
database = None
user_collection = None

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/auth/login",
    auto_error=True
)

async def connect_to_mongo():
    """Connect to MongoDB"""
    global client, database, user_collection
    try:
        client = AsyncIOMotorClient(settings.MONGO_URL)
        await client.admin.command('ping')
        database = client[settings.DATABASE_NAME]
        user_collection = database.users
        await create_indexes()
      
    except Exception as e:
       
        raise

async def close_mongo_connection():
    """Close MongoDB connection"""
    global client
    if client:
        client.close()
        print("🔌 Disconnected from MongoDB")

async def create_indexes():
    """Create database indexes"""
    await user_collection.create_index("id", unique=True)
    await user_collection.create_index("username", unique=True)
    await user_collection.create_index("email", unique=True, sparse=True)

# User CRUD operations
async def get_user_by_username(username: str) -> Optional[UserInDB]:
    """Retrieve user by username"""
    try:
        if user_dict := await user_collection.find_one({"username": username}):
            user_dict['id'] = user_dict.pop('_id', user_dict.get('id'))
            return UserInDB(**user_dict)
        return None
    except Exception as e:
        print(f"Error retrieving user: {str(e)}")
        return None

async def get_user_by_id(user_id: str) -> Optional[UserInDB]:
    """Retrieve user by ID"""
    if user_dict := await user_collection.find_one({"id": user_id}):
        return UserInDB(**user_dict)
    return None

async def create_user(user_data: dict) -> Optional[UserInDB]:
    """Create a new user"""
    try:
        result = await user_collection.insert_one(user_data)
        if result.inserted_id:
            return await get_user_by_username(user_data["username"])
        return None
    except Exception as e:
        print(f"Error creating user: {str(e)}")
        return None

# Dependencies
async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    """Get current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    username = decode_token(token)
    if username is None:
        raise credentials_exception
    
    user = await get_user_by_username(username)
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_active_user(
    current_user: UserInDB = Depends(get_current_user)
) -> UserInDB:
    """Get current active user"""
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

