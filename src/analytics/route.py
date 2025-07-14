from fastapi import APIRouter, Depends

from src import dependencies
from src.analytics import service
from src.analytics.schemas import TotalTransactions
from src.logging_config import create_logger

router = APIRouter()

logger = create_logger("analytics", __name__)


@router.get("/analytics/recent-transactions", response_model=TotalTransactions)
async def get_total_transactions(
    start_date: str,
    end_date: str,
    current_user=Depends(dependencies.get_current_user),
):
    """Get total recent transactions"""
    logger.info(f"[GET_TOTAL_TRANSACTIONS] Incoming request: user_id={current_user.userId}, start_date={start_date}, end_date={end_date}")
    try:
        total = await service.get_recent_expense_income(
            current_user.userId, start_date, end_date
        )
        logger.info(f"[GET_TOTAL_TRANSACTIONS] Success: user_id={current_user.userId}")
        return total
    except Exception as e:
        logger.exception(f"[GET_TOTAL_TRANSACTIONS] Error: {str(e)}")
        raise

@router.get("/analytics/activities")
async def get_activities(
    current_user=Depends(dependencies.get_current_user),
):
    """Get user activities"""
    logger.info(f"[GET_ACTIVITIES] Incoming request: user_id={current_user.userId}")
    try:
        activity = await service.get_activities(current_user.userId)
        logger.info(f"[GET_ACTIVITIES] Success: user_id={current_user.userId}")
        return activity
    except Exception as e:
        logger.exception(f"[GET_ACTIVITIES] Error: {str(e)}")
        raise
