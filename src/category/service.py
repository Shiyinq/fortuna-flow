from typing import Any, Dict
from src.db import database
from src.category.schemas import CategoryCreate
from src.category.constants import Info

async def create_category(category: CategoryCreate) -> Dict[str, str]:
    wallet_data = category.dict()
    await database["categories"].insert_one(wallet_data)
    return {"detail": Info.CATEGORY_CREATED}
