from src.exceptions import NotFound
from src.wallets.constants import ErrorCode


class WalletNotFound(NotFound):
    DETAIL = ErrorCode.WALLET_NOT_FOUND
