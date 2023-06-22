import math
from typing import Any, Dict
from src.db import database
from src.wallet.constants import Info
from src.wallet.schemas import WalletCreate

def metadata_pagination(total_wallets: int, page: int, limit: int) -> Dict[str, Any]:
    total_pages = math.ceil(total_wallets / limit)
    next_page = page + 1 if page < total_pages else None
    prev_page = page - 1 if page > 1 else None

    return   {
        "page": page,
        "limit": limit,
        "prevPage": prev_page,
        "nextPage": next_page,
        "totalPage": total_pages
    }

async def get_wallet(user_id: str, page: int, limit: int) -> Dict[str, Any]:
    skip = (page - 1) * limit
    total_wallets = await database["wallets"].count_documents({"userId": user_id})
    wallets = await database["wallets"].find(
        {"userId": user_id}, 
        {"_id": 0}
    ).skip(skip).limit(limit).to_list(length=None)
    metadata = metadata_pagination(total_wallets, page, limit)
    return {
        "metadata": metadata,
        "data": wallets
    }

async def create_wallet(wallet: WalletCreate) -> Dict[str, str]:
    wallet_data = wallet.dict()
    await database["wallets"].insert_one(wallet_data)
    return {"detail": Info.WALLET_CREATED}
