
from fastapi import APIRouter, Depends

from src import dependencies
from src.analytics import service
from src.analytics.schemas import TotalTransactions

router = APIRouter()

@router.get("/analytics/recent-transactions", response_model=TotalTransactions)
async def get_total_transactions(
    start_date: str,
    end_date: str,
    current_user=Depends(dependencies.get_current_user),
):
    """Get total recent transactions"""
    total = await service.get_recent_expense_income(current_user.userId, start_date, end_date)
    return total