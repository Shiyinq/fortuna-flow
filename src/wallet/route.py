from fastapi import APIRouter, Depends

from src.wallet import service
from src import dependencies
from src.wallet.schemas import WalletCreate, WalletCreateResponse

router = APIRouter()

@router.get("/wallets")
async def get_wallet():
    """Get list wallet for current user login"""
    return "OK"

@router.post("/wallet", status_code=201, response_model=WalletCreateResponse)
async def new_wallet(wallet: WalletCreate, current_user = Depends(dependencies.get_current_user)):
    """Create new wallet for current user login"""
    wallet.userId = current_user.userId
    new_wallet = await service.create_wallet(wallet)
    return new_wallet