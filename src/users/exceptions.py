from src.exceptions import BadRequest, Conflict, InternalServerError
from src.users.constants import ErrorCode


class UsernameTaken(Conflict):
    DETAIL = ErrorCode.USERNAME_TAKEN


class EmailTaken(Conflict):
    DETAIL = ErrorCode.EMAIL_TAKEN


class PasswordNotMatch(BadRequest):
    DETAIL = ErrorCode.PASSWORD_MISMATCH


class PasswordRules(BadRequest):
    DETAIL = ErrorCode.PASSWORD_RULES


class EmailAlreadyVerified(BadRequest):
    DETAIL = "Email has already been verified."


class EmailNotVerified(BadRequest):
    DETAIL = (
        "Email not verified. Please check your email and click the verification link."
    )


class InvalidVerificationToken(BadRequest):
    DETAIL = "Verification token is invalid or has expired."


class AccountLocked(BadRequest):
    DETAIL = "Your account has been locked due to too many failed login attempts."


class TooManyRequests(BadRequest):
    DETAIL = "Too many requests. Please try again later."


class ServerError(InternalServerError):
    DETAIL = "Internal server error."
