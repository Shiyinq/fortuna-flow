from src.exceptions import InternalServerError, UnprocessableContent
from src.transaction.constants import ErrorCode


class TransactionError(InternalServerError):
    DETAIL = ErrorCode.TRANSACTION_ERROR


class BalanceNotUpdated(UnprocessableContent):
    DETAIL = ErrorCode.BALANCE_NOT_UPDATED
