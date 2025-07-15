from src.config import config


class ErrorCode:
    # Authentication errors
    INCORRECT_EMAIL_OR_PASSWORD = "Incorrect email or password."
    INVALID_REFRESH_TOKEN = "Invalid refresh token."
    INVALID_JWT_TOKEN = "Invalid JWT token."
    REFRESH_TOKEN_EXPIRED = "Refresh token expired, please login again."
    SUSPICIOUS_ACTIVITY = "Suspicious activity detected, please login again."

    # Email verification errors
    EMAIL_NOT_FOUND_OR_VERIFIED = "Email not found or already verified."
    EMAIL_VERIFIED_SUCCESS = "Email verified successfully!"
    VERIFICATION_TOKEN_INVALID = "Verification token is invalid or has expired."

    # Password reset errors
    PASSWORD_RESET_SENT = (
        "If the email is registered, a password reset link has been sent to your email."
    )
    PASSWORDS_NOT_MATCH = "Passwords do not match."
    PASSWORD_POLICY_VIOLATION = "Password must be at least 8 characters with uppercase, lowercase, digits, and symbols."
    PASSWORD_RESET_SUCCESS = "Password reset successfully!"
    PASSWORD_RESET_TOKEN_INVALID = "Password reset token is invalid or has expired."


class Info:
    LOGOUT_SUCCESS = "Logout successful."
    EMAIL_VERIFICATION_SENT = (
        "Verification email has been sent. Please check your inbox."
    )


REFRESH_TOKEN_MAX_AGE = (
    config.refresh_token_max_age_days * 24 * 60 * 60
)  # days to seconds
REFRESH_TOKEN_COOKIE_KEY = "refresh_token"
