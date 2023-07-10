from typing import Dict

import pymongo
from pymongo import MongoClient

from src.config import config
from src.db import database
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
