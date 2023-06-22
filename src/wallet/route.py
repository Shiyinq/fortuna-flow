from fastapi import APIRouter, Depends, Query

from src.wallet import service
from src import dependencies
from src.wallet.schemas import Wallets, WalletCreate, WalletCreateResponse

router = APIRouter()

@router.get("/wallets", response_model=Wallets)
async def get_wallet(
    page: int = Query(1), 
    limit: int = Query(10),
    current_user = Depends(dependencies.get_current_user)
):
    """Get list wallet for current user login"""
    wallets = await service.get_wallet(current_user.userId, page, limit)
    return wallets

@router.post("/wallet", status_code=201, response_model=WalletCreateResponse)
async def new_wallet(
    wallet: WalletCreate, 
    current_user = Depends(dependencies.get_current_user)
):
    """Create new wallet for current user login"""
    wallet.userId = current_user.userId
    new_wallet = await service.create_wallet(wallet)
    return new_wallet