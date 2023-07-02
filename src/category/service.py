from typing import Any, Dict

from src.category.constants import Info
from src.category.schemas import CategoryCreate
from src.db import database
from src.utils import pagination


async def get_categories(user_id: str, page: int, limit: int) -> Dict[str, Any]:
    skip = (page - 1) * limit
    total_categories = await database["categories"].count_documents({"userId": user_id})
    categories = (
        await database["categories"]
        .find({"userId": user_id}, {"_id": 0})
        .skip(skip)
        .limit(limit)
        .to_list(length=None)
    )
    metadata = pagination(total_categories, page, limit)
    return {"metadata": metadata, "data": categories}


async def create_category(category: CategoryCreate) -> Dict[str, str]:
    wallet_data = category.dict()
    await database["categories"].insert_one(wallet_data)
    return {"detail": Info.CATEGORY_CREATED}
