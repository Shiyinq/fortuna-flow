from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src import dependencies
from src.transaction import service
from src.transaction.schemas import TransactionCreate, TransactionCreateResponse

router = APIRouter()


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
    transactions = await service.get_transactions(
        current_user.userId, month_year, page, limit
    )
    return transactions


@router.get("/transaction/wallet/{wallet_id}")
async def get_wallet_transaction(
    wallet_id: UUID,
    page: int = Query(1),
    limit: int = Query(10),
    month_year: str = Query(
        default=datetime.now().strftime("%m/%Y"), regex=r"^\d{2}/\d{4}$"
    ),
    current_user=Depends(dependencies.get_current_user),
):
    """Get all transaction from specific wallet"""
    transactions = await service.get_wallet_transactions(
        str(wallet_id), current_user.userId, month_year, page, limit
    )
    return transactions


@router.post("/transaction", status_code=201, response_model=TransactionCreateResponse)
async def add_transaction(
    transaction: TransactionCreate, current_user=Depends(dependencies.get_current_user)
):
    """Create new transaction"""
    transaction.userId = current_user.userId
    new_transaction = await service.create_transaction(transaction)
    return new_transaction


@router.put("/transaction/{transaction_id}")
async def update_transaction(
    transaction_id: UUID, current_user=Depends(dependencies.get_current_user)
):
    """Update new transaction"""
    return "OK"


@router.delete("/transaction/{transaction_id}")
async def delete_transaction(
    transaction_id: UUID, current_user=Depends(dependencies.get_current_user)
):
    """Delete transaction"""
    deleted = await service.delete_transactions(
        current_user.userId, str(transaction_id)
    )
    return deleted
