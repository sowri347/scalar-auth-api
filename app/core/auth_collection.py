from typing import Optional
from bson import ObjectId
from app.schema.auth import UserInDB
from app.core.database import get_database

def convert_objectid_to_str(user_dict: dict) -> dict:
    if user_dict and '_id' in user_dict:
        user_dict['_id'] = str(user_dict['_id'])
    if user_dict and 'id' in user_dict and isinstance(user_dict['id'], ObjectId):
        user_dict['id'] = str(user_dict['id'])
    return user_dict

async def get_user_by_username(username: str) -> Optional[UserInDB]:
    try:
        db = get_database()
        user_collection = db.users
        user_dict = await user_collection.find_one({"username": username})
        if user_dict:
            user_dict = convert_objectid_to_str(user_dict)
            user_dict.pop('_id', None)
            return UserInDB(**user_dict)
        return None
    except Exception as e:
        print(f"Error retrieving user: {str(e)}")
        return None

async def get_user_by_id(user_id: str) -> Optional[UserInDB]:
    try:
        db = get_database()
        user_collection = db.users
        user_dict = await user_collection.find_one({"id": user_id})
        if user_dict:
            user_dict = convert_objectid_to_str(user_dict)
            user_dict.pop('_id', None)
            return UserInDB(**user_dict)
        return None
    except Exception as e:
        print(f"Error retrieving user by ID: {str(e)}")
        return None

async def create_user(user_data: dict) -> Optional[UserInDB]:
    try:
        db = get_database()
        user_collection = db.users
        result = await user_collection.insert_one(user_data)
        if result.inserted_id:
            return await get_user_by_username(user_data["username"])
        return None
    except Exception as e:
        print(f"Error creating user: {str(e)}")
        return None
