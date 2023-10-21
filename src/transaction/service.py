from typing import Any, Dict

import pymongo
from pymongo import MongoClient

from src.config import config
from src.db import database
from src.transaction.constants import Info
from src.transaction.exceptions import BalanceNotUpdated, TransactionError
from src.transaction.schemas import TransactionCreate
from src.utils import month_year_transactions, pagination


async def reduce_balance(walletId: str, amount: int) -> bool:
    result = await database["wallets"].update_one(
        {"walletId": str(walletId)}, {"$inc": {"balance": -amount}}
    )
    return result


async def create_transaction(transaction: TransactionCreate) -> Dict[str, str]:
    client = MongoClient(config.mongo_uri)
    session = client.start_session()
    with session.start_transaction():
        try:
            balance_update = await reduce_balance(
                transaction.walletId, transaction.amount
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


async def get_data_transactions(
    query_count: dict, query: dict, page: int, limit: int
) -> Dict[str, Any]:
    skip = (page - 1) * limit
    total_transactions = await database["transactions"].count_documents(query_count)
    transactions = (
        await database["transactions"]
        .find(query, {"_id": 0})
        .skip(skip)
        .limit(limit)
        .to_list(length=None)
    )
    metadata = pagination(total_transactions, page, limit)
    return {"metadata": metadata, "data": transactions}


async def get_transactions(
    user_id: str, month_year: str, page: int, limit: int
) -> Dict[str, Any]:
    query_count = {"userId": user_id}
    query = {"userId": user_id, "transactionDate": month_year_transactions(month_year)}
    transactions = await get_data_transactions(query_count, query, page, limit)
    return transactions


async def get_wallet_transactions(
    wallet_id: str, user_id: str, month_year: str, page: int, limit: int
) -> Dict[str, Any]:
    query_count = {"userId": user_id, "walletId": wallet_id}
    query = {
        "userId": user_id,
        "walletId": wallet_id,
        "transactionDate": month_year_transactions(month_year),
    }
    transactions = await get_data_transactions(query_count, query, page, limit)
    return transactions
