from src.database import database


async def update_balance_db(walletId: str, amount: int, type: str = None):
    amount = -amount if type == "minus" else amount
    result = await database["wallets"].update_one(
        {"walletId": str(walletId)}, {"$inc": {"balance": amount}}
    )
    return result


async def insert_transaction_db(transaction_data: dict):
    return await database["transactions"].insert_one(transaction_data)


async def aggregate_transactions(query):
    cursor = database.transactions.aggregate(query)
    return await cursor.to_list(length=None)


async def aggregate_recent_transactions(query, limit):
    cursor = database.transactions.aggregate(query)
    return await cursor.to_list(length=limit)


async def find_one_and_delete_transaction(query):
    return await database["transactions"].find_one_and_delete(query)


async def find_one_transaction(query):
    return await database["transactions"].find_one(query)


async def update_one_transaction(query, new_data):
    return await database["transactions"].update_one(query, {"$set": new_data})
