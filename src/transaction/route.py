from uuid import UUID

from fastapi import APIRouter, Depends

from src import dependencies
from src.transaction import service
from src.transaction.schemas import TransactionCreate, TransactionCreateResponse

router = APIRouter()


@router.get("/transactions")
async def get_transactions(current_user=Depends(dependencies.get_current_user)):
    """Get all transactions"""
    return "OK"


@router.get("/transaction/wallet/{wallet_id}")
async def get_transaction(
    wallet_id: UUID, current_user=Depends(dependencies.get_current_user)
):
    """Get all transaction from specific wallet"""
    return "OK"


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
    return "OK"
