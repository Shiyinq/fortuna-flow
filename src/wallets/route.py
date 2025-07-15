from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src import dependencies
from src.wallets import service
from src.wallets.schemas import (
    TotalBalance,
    Wallet,
    WalletCreate,
    WalletCreateResponse,
    Wallets,
    WalletTransactionsResponse
)
from src.logging_config import create_logger

router = APIRouter()

logger = create_logger("wallets", __name__)


@router.get("/wallets/total-balance", response_model=TotalBalance)
async def get_total_balance(
    current_user=Depends(dependencies.get_current_user),
):
    """
    Get the total balance for all wallets owned by the current user.

    Returns:
        TotalBalance: The total balance across all wallets.
    """
    logger.info(f"[TOTAL_BALANCE] Incoming request: user_id={current_user.userId}")
    try:
        total = await service.get_total_balance(current_user)
        logger.info(f"[TOTAL_BALANCE] Success: user_id={current_user.userId}")
        return total
    except Exception as e:
        logger.exception(f"[TOTAL_BALANCE] Error: {str(e)}")
        raise


@router.get("/wallets", response_model=Wallets)
async def get_wallets(
    page: int = Query(1),
    limit: int = Query(10),
    current_user=Depends(dependencies.get_current_user),
):
    """
    Get a paginated list of wallets for the current user.

    Parameters:
        page (int, optional): Page number for pagination (default: 1).
        limit (int, optional): Number of items per page (default: 10).

    Returns:
        Wallets: Metadata and list of wallets.
    """
    logger.info(f"[GET_WALLETS] Incoming request: user_id={current_user.userId}, page={page}, limit={limit}")
    try:
        wallets = await service.get_wallets(current_user.userId, page, limit)
        logger.info(f"[GET_WALLETS] Success: user_id={current_user.userId}, count={len(wallets) if hasattr(wallets, '__len__') else 'unknown'}")
        return wallets
    except Exception as e:
        logger.exception(f"[GET_WALLETS] Error: {str(e)}")
        raise


@router.get("/wallets/{wallet_id}/transactions", response_model=WalletTransactionsResponse)
async def get_wallet_transaction(
    wallet_id: UUID,
    page: int = Query(1),
    limit: int = Query(32),
    month_year: str = Query(
        default=datetime.now().strftime("%m/%Y"), regex=r"^\d{2}/\d{4}$"
    ),
    current_user=Depends(dependencies.get_current_user),
):
    """
    Get all transactions from a specific wallet for the current user, with pagination and month/year filter.

    Parameters:
        wallet_id (UUID): The ID of the wallet.
        page (int, optional): Page number for pagination (default: 1).
        limit (int, optional): Number of items per page (default: 32).
        month_year (str, optional): Month and year in MM/YYYY format (default: current month/year).

    Returns:
        WalletTransactionsResponse: Metadata and list of transactions for the wallet.
    """
    logger.info(f"[WALLET_TRANSACTIONS] Incoming request: user_id={current_user.userId}, wallet_id={wallet_id}, page={page}, limit={limit}, month_year={month_year}")
    try:
        transactions = await service.get_wallet_transactions(
            str(wallet_id), current_user.userId, month_year, page, limit
        )
        logger.info(f"[WALLET_TRANSACTIONS] Success: user_id={current_user.userId}, wallet_id={wallet_id}")
        return WalletTransactionsResponse(**transactions)
    except Exception as e:
        logger.exception(f"[WALLET_TRANSACTIONS] Error: {str(e)}")
        raise


@router.get("/wallets/{wallet_id}", response_model=Wallet)
async def get_wallet(
    wallet_id: str, current_user=Depends(dependencies.get_current_user)
):
    """
    Get a specific wallet by its ID for the current user.

    Parameters:
        wallet_id (str): The ID of the wallet to retrieve.

    Returns:
        Wallet: The wallet data.
    """
    logger.info(f"[GET_WALLET] Incoming request: user_id={current_user.userId}, wallet_id={wallet_id}")
    try:
        wallet = await service.get_wallet(wallet_id, current_user.userId)
        logger.info(f"[GET_WALLET] Success: user_id={current_user.userId}, wallet_id={wallet_id}")
        return wallet
    except Exception as e:
        logger.exception(f"[GET_WALLET] Error: {str(e)}")
        raise


@router.post("/wallets", status_code=201, response_model=WalletCreateResponse)
async def add_wallet(
    wallet: WalletCreate, current_user=Depends(dependencies.get_current_user)
):
    """
    Create a new wallet for the current user.

    Parameters:
        wallet (WalletCreate): The wallet data to create.

    Returns:
        WalletCreateResponse: Confirmation message or created wallet data.
    """
    logger.info(f"[ADD_WALLET] Incoming request: user_id={current_user.userId}")
    try:
        wallet.userId = current_user.userId
        new_wallet = await service.create_wallet(wallet)
        logger.info(f"[ADD_WALLET] Success: user_id={current_user.userId}, wallet_id={getattr(new_wallet, 'walletId', None)}")
        return new_wallet
    except Exception as e:
        logger.exception(f"[ADD_WALLET] Error: {str(e)}")
        raise
