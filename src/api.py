from fastapi import APIRouter

from src.auth.route import router as auth_router
from src.user.route import router as user_router
from src.wallet.route import router as wallet_router

router = APIRouter()

router.include_router(auth_router, tags=["Auth"])
router.include_router(user_router, tags=["User"])
router.include_router(wallet_router, tags=["Wallet"])