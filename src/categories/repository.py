from src.database import database

async def count_categories(query: dict):
    return await database["categories"].count_documents(query)

async def find_categories(query: dict, projection: dict, skip: int, limit: int):
    return await database["categories"].find(query, projection).skip(skip).limit(limit).to_list(length=None)

async def insert_category(category_data: dict):
    return await database["categories"].insert_one(category_data) 