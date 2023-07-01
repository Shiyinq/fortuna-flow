from fastapi import APIRouter, Depends
from src.category.schemas import CategoryCreate, CategoryCreateResponse
from src import dependencies
from src.category import service

router = APIRouter()

@router.post("/category", status_code=201, response_model=CategoryCreateResponse)
async def add_category(
    category: CategoryCreate, 
    current_user = Depends(dependencies.get_current_user)
):
    """Add new custom category for current user login"""
    category.userId = current_user.userId
    new_category = await service.create_category(category)
    return new_category
