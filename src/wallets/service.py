from typing import Any, Dict

from src.auth.schemas import UserCurrent
from src.database import database
from src.transactions.service import get_data_transactions
from src.utils import month_year_transactions, pagination
from src.wallets.constants import Info
from src.wallets.exceptions import WalletNotFound
from src.wallets.schemas import TotalBalance, WalletCreate


async def get_wallets(user_id: str, page: int, limit: int) -> Dict[str, Any]:
    skip = (page - 1) * limit
    total_wallets = await database["wallets"].count_documents({"userId": user_id})
    wallets = (
        await database["wallets"]
        .find({"userId": user_id}, {"_id": 0})
        .skip(skip)
        .limit(limit)
        .to_list(length=None)
    )
    metadata = pagination(total_wallets, page, limit)
    return {"metadata": metadata, "data": wallets}


async def get_wallet(wallet_id: str, user_id: str):
    query = {"walletId": wallet_id, "userId": user_id}
    projection = {"_id": 0, "userId": 0}
    wallet = await database["wallets"].find_one(query, projection)
    if wallet:
        return wallet
    raise WalletNotFound()


async def create_wallet(wallet: WalletCreate) -> Dict[str, str]:
    wallet_data = wallet.dict()
    await database["wallets"].insert_one(wallet_data)
    return {"detail": Info.WALLET_CREATED}


async def get_wallet_transactions(
    wallet_id: str, user_id: str, month_year: str, page: int, limit: int
) -> Dict[str, Any]:
    match = {
        "userId": user_id,
        "walletId": wallet_id,
        "transactionDate": month_year_transactions(month_year),
    }
    transactions = await get_data_transactions(match, page, limit)
    return transactions


async def get_total_balance(current_user: UserCurrent) -> TotalBalance:
    query = [
        {"$match": {"userId": current_user.userId}},
        {"$group": {"_id": "$userId", "totalBalance": {"$sum": "$balance"}}},
        {"$project": {"_id": 0, "totalBalance": 1}},
    ]

    cursor = database.wallets.aggregate(query)
    result = await cursor.to_list(length=None)
    if result:
        return result[0]
    else:
        return {"totalBalance": 0}
