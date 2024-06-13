from fastapi import APIRouter

from src.auth.route import router as auth_router
from src.categories.route import router as category_router
from src.transactions.route import router as transaction_router
from src.users.route import router as user_router
from src.wallets.route import router as wallet_router

router = APIRouter()

router.include_router(auth_router, tags=["Auth"])
router.include_router(user_router, tags=["Users"])
router.include_router(wallet_router, tags=["Wallets"])
router.include_router(category_router, tags=["Categories"])
router.include_router(transaction_router, tags=["Transactions"])
