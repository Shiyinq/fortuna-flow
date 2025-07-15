from typing import Any, Dict

from src.categories import repository
from src.categories.constants import Info
from src.categories.schemas import CategoryCreate
from src.utils import pagination


async def get_categories(user_id: str, page: int, limit: int) -> Dict[str, Any]:
    skip = (page - 1) * limit
    total_categories = await repository.count_categories({"userId": user_id})
    categories = await repository.find_categories(
        {"userId": user_id}, {"_id": 0}, skip, limit
    )
    metadata = pagination(total_categories, page, limit)
    return {"metadata": metadata, "data": categories}


async def create_category(category: CategoryCreate) -> Dict[str, str]:
    wallet_data = category.dict()
    await repository.insert_category(wallet_data)
    return {"detail": Info.CATEGORY_CREATED}
