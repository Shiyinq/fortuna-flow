from fastapi import APIRouter, Depends, Query
from src import dependencies
from src.budgets import service
from src.budgets.schemas import BudgetCreate, BudgetUpdate, BudgetResponse
from src.logging_config import create_logger

router = APIRouter()

logger = create_logger("budgets", __name__)

@router.get("/budgets")
async def get_budgets(
    walletId: str = Query(None),
    current_user=Depends(dependencies.get_current_user),
):
    """Get list budget for current user login, grouped by type (atau startDate-endDate jika custom)"""
    logger.info(f"[GET_BUDGETS] Incoming request: user_id={current_user.userId}, walletId={walletId}")
    try:
        budgets = await service.get_budgets(current_user.userId, wallet_id=walletId)
        logger.info(f"[GET_BUDGETS] Success: user_id={current_user.userId}, count={len(budgets) if hasattr(budgets, '__len__') else 'unknown'}")
        return budgets
    except Exception as e:
        logger.exception(f"[GET_BUDGETS] Error: {str(e)}")
        raise

@router.get("/budgets/{budget_id}")
async def get_budget(
    budget_id: str, current_user=Depends(dependencies.get_current_user)
):
    """Get specific budget"""
    logger.info(f"[GET_BUDGET] Incoming request: user_id={current_user.userId}, budget_id={budget_id}")
    try:
        budget = await service.get_budget(budget_id, current_user.userId)
        logger.info(f"[GET_BUDGET] Success: user_id={current_user.userId}, budget_id={budget_id}")
        return budget
    except Exception as e:
        logger.exception(f"[GET_BUDGET] Error: {str(e)}")
        raise

@router.post("/budgets", status_code=201, response_model=BudgetResponse)
async def add_budget(
    budget: BudgetCreate, current_user=Depends(dependencies.get_current_user)
):
    """Create new budget for current user login"""
    logger.info(f"[ADD_BUDGET] Incoming request: user_id={current_user.userId}")
    try:
        budget.userId = current_user.userId
        new_budget = await service.create_budget(budget)
        logger.info(f"[ADD_BUDGET] Success: user_id={current_user.userId}, budget_id={getattr(new_budget, 'budgetId', None)}")
        return new_budget
    except Exception as e:
        logger.exception(f"[ADD_BUDGET] Error: {str(e)}")
        raise

@router.put("/budgets/{budget_id}", response_model=BudgetResponse)
async def update_budget(
    budget_id: str,
    update_data: BudgetUpdate,
    current_user=Depends(dependencies.get_current_user),
):
    """Update budget"""
    logger.info(f"[UPDATE_BUDGET] Incoming request: user_id={current_user.userId}, budget_id={budget_id}")
    try:
        updated = await service.update_budget(budget_id, current_user.userId, update_data)
        logger.info(f"[UPDATE_BUDGET] Success: user_id={current_user.userId}, budget_id={budget_id}")
        return updated
    except Exception as e:
        logger.exception(f"[UPDATE_BUDGET] Error: {str(e)}")
        raise

@router.delete("/budgets/{budget_id}", response_model=BudgetResponse)
async def delete_budget(
    budget_id: str, current_user=Depends(dependencies.get_current_user)
):
    """Delete budget"""
    logger.info(f"[DELETE_BUDGET] Incoming request: user_id={current_user.userId}, budget_id={budget_id}")
    try:
        deleted = await service.delete_budget(budget_id, current_user.userId)
        logger.info(f"[DELETE_BUDGET] Success: user_id={current_user.userId}, budget_id={budget_id}")
        return deleted
    except Exception as e:
        logger.exception(f"[DELETE_BUDGET] Error: {str(e)}")
        raise 