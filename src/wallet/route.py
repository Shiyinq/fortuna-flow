from fastapi import APIRouter, Depends, Query

from src.wallet import service
from src import dependencies
from src.wallet.schemas import Wallet, Wallets, WalletCreate, WalletCreateResponse

router = APIRouter()

@router.get("/wallets", response_model=Wallets)
async def get_wallets(
    page: int = Query(1), 
    limit: int = Query(10),
    current_user = Depends(dependencies.get_current_user)
):
    """Get list wallet for current user login"""
    wallets = await service.get_wallets(current_user.userId, page, limit)
    return wallets

@router.get("/wallet/{wallet_id}", response_model=Wallet)
async def get_wallet(
    wallet_id: str,
    current_user = Depends(dependencies.get_current_user)
):
    """Get specific wallet"""
    wallet = await service.get_wallet(wallet_id, current_user.userId)
    return wallet

@router.post("/wallet", status_code=201, response_model=WalletCreateResponse)
async def add_wallet(
    wallet: WalletCreate, 
    current_user = Depends(dependencies.get_current_user)
):
    """Create new wallet for current user login"""
    wallet.userId = current_user.userId
    new_wallet = await service.create_wallet(wallet)
    return new_wallet