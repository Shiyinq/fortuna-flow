from src.wallet.constants import ErrorCode
from src.exceptions import NotFound

class WalletNotFound(NotFound):
    DETAIL = ErrorCode.WALLET_NOT_FOUND