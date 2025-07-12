from src.config import config

class ErrorCode:
    INCORRECT_EMAIL_ERROR_PASSWORD = "Incorrect username or password."
    JWT_ERROR = "Could not validate credentials."


class Info:
    LOGOUT_SUCCESS = "Logout successful."

REFRESH_TOKEN_MAX_AGE = config.refresh_token_max_age_days * 24 * 60 * 60  # days to seconds
REFRESH_TOKEN_COOKIE_KEY = "refresh_token"
