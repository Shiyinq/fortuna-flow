from src.auth.constants import ErrorCode
from src.exceptions import (
    Conflict,
    InternalServerError,
    NotAuthenticated,
    UnprocessableContent,
)


class IncorrectEmailOrPassword(NotAuthenticated):
    DETAIL = ErrorCode.INCORRECT_EMAIL_ERROR_PASSWORD


class JwtTokenError(NotAuthenticated):
    DETAIL = ErrorCode.JWT_ERROR
