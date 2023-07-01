import math
from typing import Any, Dict
from src.db import database
from src.wallet.constants import Info
from src.wallet.schemas import WalletCreate
from src.wallet.exceptions import WalletNotFound
from src.utils import pagination

async def get_wallets(user_id: str, page: int, limit: int) -> Dict[str, Any]:
    skip = (page - 1) * limit
    total_wallets = await database["wallets"].count_documents({"userId": user_id})
    wallets = await database["wallets"].find(
        {"userId": user_id}, 
        {"_id": 0}
    ).skip(skip).limit(limit).to_list(length=None)
    metadata = pagination(total_wallets, page, limit)
    return {
        "metadata": metadata,
        "data": wallets
    }

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
