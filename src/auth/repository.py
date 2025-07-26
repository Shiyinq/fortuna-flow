from datetime import datetime, timezone

from src.database import database


async def find_user(query: dict):
    return await database["users"].find_one(query)


async def insert_refresh_token(data: dict):
    return await database["refresh_tokens"].insert_one(data)


async def find_refresh_token(token: str):
    return await database["refresh_tokens"].find_one({"hashRefreshToken": token})


async def update_refresh_token_last_used(token: str):
    return await database["refresh_tokens"].update_one(
        {"hashRefreshToken": token},
        {"$set": {"lastUsedAt": datetime.now(timezone.utc).isoformat()}},
    )


async def delete_refresh_token(token: str):
    return await database["refresh_tokens"].delete_one({"hashRefreshToken": token})


async def insert_login_history(data: dict):
    return await database["login_history"].insert_one(data)


async def find_last_login_history(user_id: str):
    return await database["login_history"].find_one(
        {"userId": user_id}, sort=[("loginAt", -1)]
    )
