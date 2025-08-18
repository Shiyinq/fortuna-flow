from datetime import datetime
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request

from src import dependencies
from src.logging_config import create_logger
from src.transactions import service
from src.transactions.schemas import (
    RecentTransactionItem,
    TransactionCreate,
    TransactionCreateResponse,
    TransactionsMetadata,
    TransactionsResponse,
    TransactionUpdate,
)
from src.dependencies import get_current_user, require_csrf_protection

router = APIRouter()

logger = create_logger("transactions", __name__)


@router.get("/transactions/recent", response_model=List[RecentTransactionItem])
async def get_recent_transactions(
    limit: int = Query(5), current_user=Depends(get_current_user)
):
    """
    Get a list of the most recent transactions for the current user.

    Parameters:
        limit (int, optional): Maximum number of transactions to return (default: 5).

    Returns:
        List[RecentTransactionItem]: List of recent transactions.
    """
    logger.info(
        f"[GET_RECENT_TRANSACTIONS] Incoming request: user_id={current_user.userId}, limit={limit}"
    )
    try:
        recent = await service.get_recent_transactions(current_user.userId, limit)
        logger.info(
            f"[GET_RECENT_TRANSACTIONS] Success: user_id={current_user.userId}, count={len(recent) if hasattr(recent, '__len__') else 'unknown'}"
        )
        return recent
    except Exception as e:
        logger.exception(f"[GET_RECENT_TRANSACTIONS] Error: {str(e)}")
        raise


@router.get("/transactions", response_model=TransactionsResponse)
async def get_transactions(
    page: int = Query(1),
    limit: int = Query(10),
    month_year: str = Query(
        default=datetime.now().strftime("%m/%Y"), regex=r"^\d{2}/\d{4}$"
    ),
    current_user=Depends(get_current_user),
):
    """
    Get a paginated list of all transactions for the current user in a specific month and year.

    Parameters:
        page (int, optional): Page number for pagination (default: 1).
        limit (int, optional): Number of items per page (default: 10).
        month_year (str, optional): Month and year in MM/YYYY format (default: current month/year).

    Returns:
        TransactionsResponse: Metadata and list of transactions.
    """
    logger.info(
        f"[GET_TRANSACTIONS] Incoming request: user_id={current_user.userId}, page={page}, limit={limit}, month_year={month_year}"
    )
    try:
        transactions = await service.get_transactions(
            current_user.userId, month_year, page, limit
        )
        logger.info(
            f"[GET_TRANSACTIONS] Success: user_id={current_user.userId}, count={len(transactions['data']) if 'data' in transactions else 'unknown'}"
        )

        if not len(transactions):
            return TransactionsResponse(
                metadata=TransactionsMetadata(
                    totalData=0,
                    totalPage=0,
                    previousPage=None,
                    currentPage=page,
                    nextPage=None
                ),
                data=[]
            )

        return TransactionsResponse(**transactions)
    except Exception as e:
        logger.exception(f"[GET_TRANSACTIONS] Error: {str(e)}")
        raise


@router.post("/transactions", status_code=201, response_model=TransactionCreateResponse)
async def add_transaction(
    transaction: TransactionCreate,
    request: Request,
    current_user=Depends(get_current_user),
    _: bool = Depends(require_csrf_protection)
):
    """
    Create a new transaction for the current user.

    Parameters:
        transaction (TransactionCreate): The transaction data to create.

    Returns:
        TransactionCreateResponse: Confirmation message or created transaction data.
    """
    logger.info(f"[ADD_TRANSACTION] Incoming request: user_id={current_user.userId}")
    try:
        transaction.userId = current_user.userId
        new_transaction = await service.create_transaction(transaction)
        logger.info(
            f"[ADD_TRANSACTION] Success: user_id={current_user.userId}, transaction_id={getattr(new_transaction, 'transactionId', None)}"
        )
        return new_transaction
    except Exception as e:
        logger.exception(f"[ADD_TRANSACTION] Error: {str(e)}")
        raise


@router.put("/transactions/{transaction_id}")
async def update_transaction(
    transaction_id: UUID,
    transaction: TransactionUpdate,
    request: Request,
    current_user=Depends(get_current_user),
    _: bool = Depends(require_csrf_protection)
):
    """
    Update an existing transaction for the current user.

    Parameters:
        transaction_id (UUID): The ID of the transaction to update.
        transaction (TransactionUpdate): The updated transaction data.

    Returns:
        dict: The updated transaction data or confirmation message.
    """
    logger.info(
        f"[UPDATE_TRANSACTION] Incoming request: user_id={current_user.userId}, transaction_id={transaction_id}"
    )
    try:
        updated = await service.update_transaction(
            current_user.userId, str(transaction_id), transaction.to_dict()
        )
        logger.info(
            f"[UPDATE_TRANSACTION] Success: user_id={current_user.userId}, transaction_id={transaction_id}"
        )
        return updated
    except Exception as e:
        logger.exception(f"[UPDATE_TRANSACTION] Error: {str(e)}")
        raise


@router.delete("/transactions/{transaction_id}")
async def delete_transaction(
    transaction_id: UUID,
    request: Request,
    current_user=Depends(get_current_user),
    _: bool = Depends(require_csrf_protection)
):
    """
    Delete a transaction by its ID for the current user.

    Parameters:
        transaction_id (UUID): The ID of the transaction to delete.

    Returns:
        dict: The deleted transaction data or confirmation message.
    """
    logger.info(
        f"[DELETE_TRANSACTION] Incoming request: user_id={current_user.userId}, transaction_id={transaction_id}"
    )
    try:
        deleted = await service.delete_transactions(
            current_user.userId, str(transaction_id)
        )
        logger.info(
            f"[DELETE_TRANSACTION] Success: user_id={current_user.userId}, transaction_id={transaction_id}"
        )
        return deleted
    except Exception as e:
        logger.exception(f"[DELETE_TRANSACTION] Error: {str(e)}")
        raise
