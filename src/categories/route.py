from fastapi import APIRouter, Depends, Query

from src import dependencies
from src.categories import service
from src.categories.schemas import CategoryCreate, CategoryCreateResponse
from src.logging_config import create_logger

router = APIRouter()

logger = create_logger("categories", __name__)


@router.get("/categories")
async def get_categories(
    page: int = Query(1),
    limit: int = Query(10),
    current_user=Depends(dependencies.get_current_user),
):
    """Get list category for current user login"""
    logger.info(f"[GET_CATEGORIES] Incoming request: user_id={current_user.userId}, page={page}, limit={limit}")
    try:
        categories = await service.get_categories(current_user.userId, page, limit)
        logger.info(f"[GET_CATEGORIES] Success: user_id={current_user.userId}, count={len(categories) if hasattr(categories, '__len__') else 'unknown'}")
        return categories
    except Exception as e:
        logger.exception(f"[GET_CATEGORIES] Error: {str(e)}")
        raise


@router.post("/categories", status_code=201, response_model=CategoryCreateResponse)
async def add_category(
    category: CategoryCreate, current_user=Depends(dependencies.get_current_user)
):
    """Add new custom category for current user login"""
    logger.info(f"[ADD_CATEGORY] Incoming request: user_id={current_user.userId}")
    try:
        category.userId = current_user.userId
        new_category = await service.create_category(category)
        logger.info(f"[ADD_CATEGORY] Success: user_id={current_user.userId}, category_id={getattr(new_category, 'categoryId', None)}")
        return new_category
    except Exception as e:
        logger.exception(f"[ADD_CATEGORY] Error: {str(e)}")
        raise
