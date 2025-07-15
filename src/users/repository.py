from src.database import database


async def insert_user(user_data: dict):
    return await database["users"].insert_one(user_data)
