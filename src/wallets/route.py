from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src import dependencies
from src.wallets import service
from src.wallets.schemas import Wallet, WalletCreate, WalletCreateResponse, Wallets

router = APIRouter()


@router.get("/wallets", response_model=Wallets)
async def get_wallets(
    page: int = Query(1),
    limit: int = Query(10),
    current_user=Depends(dependencies.get_current_user),
):
    """Get list wallet for current user login"""
    wallets = await service.get_wallets(current_user.userId, page, limit)
    return wallets


@router.get("/wallets/{wallet_id}/transactions")
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


@router.get("/wallets/{wallet_id}", response_model=Wallet)
async def get_wallet(
    wallet_id: str, current_user=Depends(dependencies.get_current_user)
):
    """Get specific wallet"""
    wallet = await service.get_wallet(wallet_id, current_user.userId)
    return wallet


@router.post("/wallets", status_code=201, response_model=WalletCreateResponse)
async def add_wallet(
    wallet: WalletCreate, current_user=Depends(dependencies.get_current_user)
):
    """Create new wallet for current user login"""
    wallet.userId = current_user.userId
    new_wallet = await service.create_wallet(wallet)
    return new_wallet
