from src.auth.constants import ErrorCode
from src.exceptions import BadRequest, NotAuthenticated


class IncorrectEmailOrPassword(NotAuthenticated):
    DETAIL = ErrorCode.INCORRECT_EMAIL_OR_PASSWORD


class InvalidRefreshToken(NotAuthenticated):
    DETAIL = ErrorCode.INVALID_REFRESH_TOKEN


class InvalidJWTToken(NotAuthenticated):
    DETAIL = ErrorCode.INVALID_JWT_TOKEN


class RefreshTokenExpired(NotAuthenticated):
    DETAIL = ErrorCode.REFRESH_TOKEN_EXPIRED


class SuspiciousActivity(NotAuthenticated):
    DETAIL = ErrorCode.SUSPICIOUS_ACTIVITY


class VerificationTokenInvalid(BadRequest):
    DETAIL = ErrorCode.VERIFICATION_TOKEN_INVALID


class PasswordResetTokenInvalid(BadRequest):
    DETAIL = ErrorCode.PASSWORD_RESET_TOKEN_INVALID


class PasswordsNotMatch(BadRequest):
    DETAIL = ErrorCode.PASSWORDS_NOT_MATCH


class PasswordPolicyViolation(BadRequest):
    DETAIL = ErrorCode.PASSWORD_POLICY_VIOLATION
