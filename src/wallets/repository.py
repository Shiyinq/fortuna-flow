from src.database import database


async def count_wallets(query: dict):
    return await database["wallets"].count_documents(query)


async def find_wallets(query: dict, projection: dict, skip: int, limit: int):
    return (
        await database["wallets"]
        .find(query, projection)
        .skip(skip)
        .limit(limit)
        .to_list(length=None)
    )


async def find_one_wallet(query: dict, projection: dict):
    return await database["wallets"].find_one(query, projection)


async def insert_wallet(wallet_data: dict):
    return await database["wallets"].insert_one(wallet_data)


async def aggregate_wallets(query):
    cursor = database.wallets.aggregate(query)
    return await cursor.to_list(length=None)
