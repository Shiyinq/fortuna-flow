from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src import dependencies
from src.transactions import service
from src.transactions.schemas import (
    TransactionCreate,
    TransactionCreateResponse,
    TransactionUpdate,
)
from src.logging_config import create_logger

router = APIRouter()

logger = create_logger("transactions", __name__)


@router.get("/transactions/recent")
async def get_recent_transactions(
    limit: int = Query(5), current_user=Depends(dependencies.get_current_user)
):
    """Get recent transactions"""
    logger.info(f"[GET_RECENT_TRANSACTIONS] Incoming request: user_id={current_user.userId}, limit={limit}")
    try:
        recent = await service.get_recent_transactions(current_user.userId, limit)
        logger.info(f"[GET_RECENT_TRANSACTIONS] Success: user_id={current_user.userId}, count={len(recent) if hasattr(recent, '__len__') else 'unknown'}")
        return recent
    except Exception as e:
        logger.exception(f"[GET_RECENT_TRANSACTIONS] Error: {str(e)}")
        raise


@router.get("/transactions")
async def get_transactions(
    page: int = Query(1),
    limit: int = Query(10),
    month_year: str = Query(
        default=datetime.now().strftime("%m/%Y"), regex=r"^\d{2}/\d{4}$"
    ),
    current_user=Depends(dependencies.get_current_user),
):
    """Get all transactions"""
    logger.info(f"[GET_TRANSACTIONS] Incoming request: user_id={current_user.userId}, page={page}, limit={limit}, month_year={month_year}")
    try:
        transactions = await service.get_transactions(
            current_user.userId, month_year, page, limit
        )
        logger.info(f"[GET_TRANSACTIONS] Success: user_id={current_user.userId}, count={len(transactions) if hasattr(transactions, '__len__') else 'unknown'}")
        return transactions
    except Exception as e:
        logger.exception(f"[GET_TRANSACTIONS] Error: {str(e)}")
        raise


@router.post("/transactions", status_code=201, response_model=TransactionCreateResponse)
async def add_transaction(
    transaction: TransactionCreate, current_user=Depends(dependencies.get_current_user)
):
    """Create new transaction"""
    logger.info(f"[ADD_TRANSACTION] Incoming request: user_id={current_user.userId}")
    try:
        transaction.userId = current_user.userId
        new_transaction = await service.create_transaction(transaction)
        logger.info(f"[ADD_TRANSACTION] Success: user_id={current_user.userId}, transaction_id={getattr(new_transaction, 'transactionId', None)}")
        return new_transaction
    except Exception as e:
        logger.exception(f"[ADD_TRANSACTION] Error: {str(e)}")
        raise


@router.put("/transactions/{transaction_id}")
async def update_transaction(
    transaction_id: UUID,
    transaction: TransactionUpdate,
    current_user=Depends(dependencies.get_current_user),
):
    """Update new transaction"""
    logger.info(f"[UPDATE_TRANSACTION] Incoming request: user_id={current_user.userId}, transaction_id={transaction_id}")
    try:
        updated = await service.update_transaction(
            current_user.userId, str(transaction_id), transaction.to_dict()
        )
        logger.info(f"[UPDATE_TRANSACTION] Success: user_id={current_user.userId}, transaction_id={transaction_id}")
        return updated
    except Exception as e:
        logger.exception(f"[UPDATE_TRANSACTION] Error: {str(e)}")
        raise


@router.delete("/transactions/{transaction_id}")
async def delete_transaction(
    transaction_id: UUID, current_user=Depends(dependencies.get_current_user)
):
    """Delete transaction"""
    logger.info(f"[DELETE_TRANSACTION] Incoming request: user_id={current_user.userId}, transaction_id={transaction_id}")
    try:
        deleted = await service.delete_transactions(
            current_user.userId, str(transaction_id)
        )
        logger.info(f"[DELETE_TRANSACTION] Success: user_id={current_user.userId}, transaction_id={transaction_id}")
        return deleted
    except Exception as e:
        logger.exception(f"[DELETE_TRANSACTION] Error: {str(e)}")
        raise
