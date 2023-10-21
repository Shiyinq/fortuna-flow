from src.exceptions import InternalServerError, NotFound, UnprocessableContent
from src.transaction.constants import ErrorCode


class TransactionError(InternalServerError):
    DETAIL = ErrorCode.TRANSACTION_ERROR


class TransactionDeleteError(InternalServerError):
    DETAIL = ErrorCode.TRANSACTION_DELETE_ERROR


class TransactionIDNotFound(NotFound):
    DETAIL = ErrorCode.TRANSACTION_ID_NOT_FOUND


class BalanceNotUpdated(UnprocessableContent):
    DETAIL = ErrorCode.BALANCE_NOT_UPDATED
