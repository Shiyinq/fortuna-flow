from fastapi import APIRouter, Depends, Query

from src import dependencies
from src.categories import service
from src.categories.schemas import CategoryCreate, CategoryCreateResponse, CategoriesResponse
from src.logging_config import create_logger

router = APIRouter()

logger = create_logger("categories", __name__)


@router.get("/categories", response_model=CategoriesResponse)
async def get_categories(
    page: int = Query(1),
    limit: int = Query(10),
    current_user=Depends(dependencies.get_current_user),
):
    """
    Get a paginated list of categories for the current user.

    Parameters:
        page (int, optional): Page number for pagination (default: 1).
        limit (int, optional): Number of items per page (default: 10).

    Returns:
        CategoriesResponse: Metadata and list of categories.
    """
    logger.info(f"[GET_CATEGORIES] Incoming request: user_id={current_user.userId}, page={page}, limit={limit}")
    try:
        categories = await service.get_categories(current_user.userId, page, limit)
        logger.info(f"[GET_CATEGORIES] Success: user_id={current_user.userId}, count={len(categories['data']) if 'data' in categories else 'unknown'}")
        return CategoriesResponse(**categories)
    except Exception as e:
        logger.exception(f"[GET_CATEGORIES] Error: {str(e)}")
        raise


@router.post("/categories", status_code=201, response_model=CategoryCreateResponse)
async def add_category(
    category: CategoryCreate, current_user=Depends(dependencies.get_current_user)
):
    """
    Add a new custom category for the current user.

    Parameters:
        category (CategoryCreate): The category data to create.

    Returns:
        CategoryCreateResponse: Confirmation message or created category data.
    """
    logger.info(f"[ADD_CATEGORY] Incoming request: user_id={current_user.userId}")
    try:
        category.userId = current_user.userId
        new_category = await service.create_category(category)
        logger.info(f"[ADD_CATEGORY] Success: user_id={current_user.userId}, category_id={getattr(new_category, 'categoryId', None)}")
        return new_category
    except Exception as e:
        logger.exception(f"[ADD_CATEGORY] Error: {str(e)}")
        raise
