from typing import Any, Dict

import pymongo
from pymongo import MongoClient

from src.config import config
from src.database import database
from src.transactions.constants import Info
from src.transactions.exceptions import (
    BalanceNotUpdated,
    TransactionDeleteError,
    TransactionError,
    TransactionIDNotFound,
)
from src.transactions.schemas import TransactionCreate
from src.utils import month_year_transactions, pagination_aggregate


async def update_balance(walletId: str, amount: int, type: str = None):
    amount = -amount if type == "minus" else amount
    result = await database["wallets"].update_one(
        {"walletId": str(walletId)}, {"$inc": {"balance": amount}}
    )
    return result


async def create_transaction(transaction: TransactionCreate) -> Dict[str, str]:
    client = MongoClient(config.mongo_uri)
    session = client.start_session()
    with session.start_transaction():
        try:
            type_update_balance = "minus" if transaction.type == "expense" else None
            balance_update = await update_balance(
                transaction.walletId, transaction.amount, type_update_balance
            )
            if balance_update.modified_count > 0:
                transaction_data = transaction.to_dict()
                await database["transactions"].insert_one(transaction_data)
                return {"detail": Info.TRANSACTION_CREATED}
            else:
                raise BalanceNotUpdated()
        except pymongo.errors.PyMongoError as e:
            session.abort_transaction()
            raise TransactionError()
        except Exception:
            session.abort_transaction()
            raise TransactionError()
        finally:
            session.end_session()


async def get_data_transactions(match: dict, page: int, limit: int) -> Dict[str, Any]:
    query = [
        {"$match": match},
        {
            "$lookup": {
                "from": "categories",
                "localField": "categoryId",
                "foreignField": "categoryId",
                "as": "categoryDetails",
            }
        },
        {"$unwind": "$categoryDetails"},
        {
            "$group": {
                "_id": "$transactionDate",
                "totalAmountExpense": {
                    "$sum": {"$cond": [{"$eq": ["$type", "expense"]}, "$amount", 0]}
                },
                "totalAmountIncome": {
                    "$sum": {"$cond": [{"$eq": ["$type", "income"]}, "$amount", 0]}
                },
                "transactions": {
                    "$push": {
                        "transactionId": "$transactionId",
                        "walletId": "$walletId",
                        "categoryId": "$categoryId",
                        "categoryDetail": {
                            "categoryIcon": "$categoryDetails.categoryIcon",
                            "name": "$categoryDetails.name",
                            "type": "$categoryDetails.type",
                        },
                        "amount": "$amount",
                        "type": "$type",
                        "note": "$note",
                        "createdAt": "$createdAt",
                        "updatedAt": "$updatedAt",
                    }
                },
            }
        },
        {
            "$project": {
                "_id": 0,
                "transactionDate": "$_id",
                "totalAmountExpense": 1,
                "totalAmountIncome": 1,
                "transactions": 1,
            }
        },
        {"$sort": {"transactionDate": -1}},
        {"$facet": pagination_aggregate(page, limit)},
        {"$unwind": "$metadata"},
    ]

    cursor = database.transactions.aggregate(query)
    transactions = await cursor.to_list(length=None)
    if transactions:
        return transactions[0]

    return transactions


async def get_recent_transactions(user_id: str, limit: int) -> Dict[str, Any]:
    query = [
        {"$match": {"userId": user_id}},
        {"$sort": {"transactionDate": -1}},
        {"$limit": limit},
        {
            "$lookup": {
                "from": "categories",
                "localField": "categoryId",
                "foreignField": "categoryId",
                "as": "category",
            }
        },
        {"$unwind": "$category"},
        {
            "$project": {
                "_id": 0,
                "transactionId": 1,
                "type": 1,
                "amount": 1,
                "note": 1,
                "transactionDate": 1,
                "categoryIcon": "$category.categoryIcon",
                "categoryName": "$category.name",
            }
        },
    ]

    cursor = database.transactions.aggregate(query)
    transactions = await cursor.to_list(length=limit)
    return transactions


async def get_transactions(
    user_id: str, month_year: str, page: int, limit: int
) -> Dict[str, Any]:
    match = {
        "userId": user_id,
        "transactionDate": month_year_transactions(month_year),
    }
    transactions = await get_data_transactions(match, page, limit)
    return transactions


async def delete_transactions(user_id: str, transaction_id: str) -> Dict[str, str]:
    try:
        query = {"userId": user_id, "transactionId": transaction_id}
        result = await database["transactions"].find_one_and_delete(query)

        if result is None:
            raise TransactionIDNotFound()
        else:
            await update_balance(result["walletId"], result["amount"])
            return {"detail": Info.TRANSACTION_DELETED}
    except Exception:
        raise TransactionDeleteError()


async def update_transaction(user_id: str, transaction_id: str, new_data: dict):
    old_data = await database["transactions"].find_one(
        {"userId": user_id, "transactionId": transaction_id}
    )

    if old_data is None:
        raise TransactionIDNotFound()

    await database["transactions"].update_one(
        {"userId": user_id, "transactionId": transaction_id}, {"$set": new_data}
    )

    diff = new_data["amount"] - old_data["amount"]

    if new_data == "expense":
        type = "minus" if diff > 0 else None
    else:
        type = "minus" if diff < 0 else None

    if diff != 0:
        await update_balance(old_data["walletId"], abs(diff), type)

    return {"detail": Info.TRANSACTION_UPDATED}
