from src.database import database


async def aggregate_transactions(query, length=None):
    cursor = database.transactions.aggregate(query)
    return await cursor.to_list(length=length)
