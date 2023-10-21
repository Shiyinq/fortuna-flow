from typing import Any, Dict
from datetime import datetime, timedelta

import pymongo
from pymongo import MongoClient

from src.config import config
from src.db import database
from src.utils import pagination
from src.transaction.constants import Info
from src.transaction.exceptions import BalanceNotUpdated, TransactionError
from src.transaction.schemas import TransactionCreate


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


async def get_transactions(
    user_id: str, month_year: str, page: int, limit: int
) -> Dict[str, Any]:
    skip = (page - 1) * limit

    month, year = month_year.split("/")
    start_date = datetime(int(year), int(month), 1)
    end_date = datetime(int(year), int(month) + 1, 1) - timedelta(
        microseconds=1
    )

    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    query = {
        "userId": user_id,
        "transactionDate": {
            "$gte": start_date_str, 
            "$lte": end_date_str
        }
    }

    total_wallets = await database["transactions"].count_documents({"userId": user_id})
    wallets = (
        await database["transactions"]
        .find(query, {"_id": 0})
        .skip(skip)
        .limit(limit)
        .to_list(length=None)
    )
    metadata = pagination(total_wallets, page, limit)
    return {"metadata": metadata, "data": wallets}
