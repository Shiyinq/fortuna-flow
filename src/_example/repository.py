from src.database import database


async def find_examples(query: dict, projection: dict = None):
    return await database["examples"].find(query, projection).to_list(length=None)


async def insert_example(data: dict):
    return await database["examples"].insert_one(data)


async def update_example(query: dict, update_data: dict):
    return await database["examples"].update_one(query, {"$set": update_data})


async def delete_example(query: dict):
    return await database["examples"].delete_one(query)
