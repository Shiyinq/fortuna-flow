from fastapi import APIRouter, Depends, Query

from src import dependencies
from src.categories import service
from src.categories.schemas import CategoryCreate, CategoryCreateResponse

router = APIRouter()


@router.get("/categories")
async def get_categories(
    page: int = Query(1),
    limit: int = Query(10),
    current_user=Depends(dependencies.get_current_user),
):
    """Get list category for current user login"""
    categories = await service.get_categories(current_user.userId, page, limit)
    return categories


@router.post("/categories", status_code=201, response_model=CategoryCreateResponse)
async def add_category(
    category: CategoryCreate, current_user=Depends(dependencies.get_current_user)
):
    """Add new custom category for current user login"""
    category.userId = current_user.userId
    new_category = await service.create_category(category)
    return new_category
