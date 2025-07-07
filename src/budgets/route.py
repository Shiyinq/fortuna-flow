from fastapi import APIRouter, Depends, Query
from src import dependencies
from src.budgets import service
from src.budgets.schemas import BudgetCreate, BudgetUpdate, BudgetResponse

router = APIRouter()

@router.get("/budgets")
async def get_budgets(
    walletId: str = Query(None),
    current_user=Depends(dependencies.get_current_user),
):
    """Get list budget for current user login, grouped by type (atau startDate-endDate jika custom)"""
    budgets = await service.get_budgets(current_user.userId, wallet_id=walletId)
    return budgets

@router.get("/budgets/{budget_id}")
async def get_budget(
    budget_id: str, current_user=Depends(dependencies.get_current_user)
):
    """Get specific budget"""
    budget = await service.get_budget(budget_id, current_user.userId)
    return budget

@router.post("/budgets", status_code=201, response_model=BudgetResponse)
async def add_budget(
    budget: BudgetCreate, current_user=Depends(dependencies.get_current_user)
):
    """Create new budget for current user login"""
    budget.userId = current_user.userId
    new_budget = await service.create_budget(budget)
    return new_budget

@router.put("/budgets/{budget_id}", response_model=BudgetResponse)
async def update_budget(
    budget_id: str,
    update_data: BudgetUpdate,
    current_user=Depends(dependencies.get_current_user),
):
    """Update budget"""
    updated = await service.update_budget(budget_id, current_user.userId, update_data)
    return updated

@router.delete("/budgets/{budget_id}", response_model=BudgetResponse)
async def delete_budget(
    budget_id: str, current_user=Depends(dependencies.get_current_user)
):
    """Delete budget"""
    deleted = await service.delete_budget(budget_id, current_user.userId)
    return deleted 