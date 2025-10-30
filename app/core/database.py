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

async def get_database():
    """Return the MongoDB database object"""
    if database is None:
        raise Exception("Database not initialized. Call connect_to_mongo() first.")
    return database
