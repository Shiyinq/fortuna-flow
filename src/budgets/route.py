from fastapi import APIRouter, Depends, Query, Request

from src.budgets import service
from src.budgets.schemas import (
    BudgetCreate,
    BudgetDetailResponse,
    BudgetResponse,
    BudgetsResponse,
    BudgetUpdate,
)
from src.dependencies import get_current_user, require_csrf_protection
from src.logging_config import create_logger

router = APIRouter()

logger = create_logger("budgets", __name__)


@router.get("/budgets", response_model=BudgetsResponse)
async def get_budgets(
    walletId: str = Query(None),
    current_user=Depends(get_current_user),
):
    """
    Get a list of budgets for the current user, grouped by type or by custom date range.

    Parameters:
        walletId (str, optional): Filter budgets by wallet ID.

    Returns:
        BudgetsResponse: Budgets grouped by type or custom date range.
    """
    logger.info(
        f"[GET_BUDGETS] Incoming request: user_id={current_user.userId}, walletId={walletId}"
    )
    try:
        budgets = await service.get_budgets(current_user.userId, wallet_id=walletId)
        logger.info(
            f"[GET_BUDGETS] Success: user_id={current_user.userId}, count={len(budgets) if hasattr(budgets, '__len__') else 'unknown'}"
        )
        return BudgetsResponse.parse_obj(budgets)
    except Exception as e:
        logger.exception(f"[GET_BUDGETS] Error: {str(e)}")
        raise


@router.get("/budgets/{budget_id}", response_model=BudgetDetailResponse)
async def get_budget(budget_id: str, current_user=Depends(get_current_user)):
    """
    Get a specific budget by its ID for the current user.

    Parameters:
        budget_id (str): The ID of the budget to retrieve.

    Returns:
        BudgetDetailResponse: The budget data.
    """
    logger.info(
        f"[GET_BUDGET] Incoming request: user_id={current_user.userId}, budget_id={budget_id}"
    )
    try:
        budget = await service.get_budget(budget_id, current_user.userId)
        logger.info(
            f"[GET_BUDGET] Success: user_id={current_user.userId}, budget_id={budget_id}"
        )
        return BudgetDetailResponse(**budget)
    except Exception as e:
        logger.exception(f"[GET_BUDGET] Error: {str(e)}")
        raise


@router.post("/budgets", status_code=201, response_model=BudgetResponse)
async def add_budget(
    budget: BudgetCreate,
    request: Request,
    current_user=Depends(get_current_user),
    _: bool = Depends(require_csrf_protection),
):
    """
    Create a new budget for the current user.

    Parameters:
        budget (BudgetCreate): The budget data to create.

    Returns:
        BudgetResponse: The created budget data.
    """
    logger.info(f"[ADD_BUDGET] Incoming request: user_id={current_user.userId}")
    try:
        budget.userId = current_user.userId
        new_budget = await service.create_budget(budget)
        logger.info(
            f"[ADD_BUDGET] Success: user_id={current_user.userId}, budget_id={getattr(new_budget, 'budgetId', None)}"
        )
        return new_budget
    except Exception as e:
        logger.exception(f"[ADD_BUDGET] Error: {str(e)}")
        raise


@router.put("/budgets/{budget_id}", response_model=BudgetResponse)
async def update_budget(
    budget_id: str,
    update_data: BudgetUpdate,
    request: Request,
    current_user=Depends(get_current_user),
    _: bool = Depends(require_csrf_protection),
):
    """
    Update an existing budget for the current user.

    Parameters:
        budget_id (str): The ID of the budget to update.
        update_data (BudgetUpdate): The updated budget data.

    Returns:
        BudgetResponse: The updated budget data.
    """
    logger.info(
        f"[UPDATE_BUDGET] Incoming request: user_id={current_user.userId}, budget_id={budget_id}"
    )
    try:
        updated = await service.update_budget(
            budget_id, current_user.userId, update_data
        )
        logger.info(
            f"[UPDATE_BUDGET] Success: user_id={current_user.userId}, budget_id={budget_id}"
        )
        return updated
    except Exception as e:
        logger.exception(f"[UPDATE_BUDGET] Error: {str(e)}")
        raise


@router.delete("/budgets/{budget_id}", response_model=BudgetResponse)
async def delete_budget(
    budget_id: str,
    request: Request,
    current_user=Depends(get_current_user),
    _: bool = Depends(require_csrf_protection),
):
    """
    Delete a budget by its ID for the current user.

    Parameters:
        budget_id (str): The ID of the budget to delete.

    Returns:
        BudgetResponse: The deleted budget data or confirmation message.
    """
    logger.info(
        f"[DELETE_BUDGET] Incoming request: user_id={current_user.userId}, budget_id={budget_id}"
    )
    try:
        deleted = await service.delete_budget(budget_id, current_user.userId)
        logger.info(
            f"[DELETE_BUDGET] Success: user_id={current_user.userId}, budget_id={budget_id}"
        )
        return deleted
    except Exception as e:
        logger.exception(f"[DELETE_BUDGET] Error: {str(e)}")
        raise
