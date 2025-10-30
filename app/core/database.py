from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional

from app.config import settings

# MongoDB client
client: Optional[AsyncIOMotorClient] = None
database = None

async def connect_to_mongo():
    """Connect to MongoDB"""
    global client, database
    try:
        print("🔄 Connecting to MongoDB...")
        client = AsyncIOMotorClient(settings.MONGO_URL)
        
        # Test the connection
        await client.admin.command('ping')
        
        database = client[settings.DATABASE_NAME]
        
        # Create indexes
        await create_indexes()
        
        print(f"✅ Connected to MongoDB database: {settings.DATABASE_NAME}")
        
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {str(e)}")
        raise

async def close_mongo_connection():
    """Close MongoDB connection"""
    global client
    if client:
        client.close()
        print("🔌 Disconnected from MongoDB")

async def create_indexes():
    """Create database indexes"""
    global database
    if database is None:
        raise Exception("Database not initialized")
    
    user_collection = database.users
    
    try:
        await user_collection.create_index("id", unique=True)
        await user_collection.create_index("username", unique=True)
        await user_collection.create_index("email", unique=True, sparse=True)
        print("📑 Database indexes created successfully")
    except Exception as e:
        print(f"⚠️  Index creation warning: {str(e)}")

def get_database():
    """Return the MongoDB database object"""
    if database is None:
        raise Exception("Database not initialized. Ensure connect_to_mongo() is called on startup.")
    return database