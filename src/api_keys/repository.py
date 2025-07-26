from datetime import datetime
from src.database import database


async def insert_api_key(api_key_data: dict):
    return await database["api_keys"].insert_one(api_key_data)


async def find_user_api_key(user_id: str):
    return await database["api_keys"].find_one({"userId": user_id})


async def delete_user_api_key(user_id: dict):
    return await database["api_keys"].delete_one({"userId": user_id})


async def update_last_used_api_key(user_id: str):
    return await database["api_keys"].update_one({"userId": user_id}, {"$set": {"lastUsedAt": datetime.now()}})


async def find_api_key(query: str, length=None):
    cursor = database["api_keys"].aggregate(query)
    return await cursor.to_list(length=length)
