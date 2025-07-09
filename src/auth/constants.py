class ErrorCode:
    INCORRECT_EMAIL_ERROR_PASSWORD = "Incorrect username or password."
    JWT_ERROR = "Could not validate credentials."


class Info:
    LOGOUT_SUCCESS = "Logout successful."

REFRESH_TOKEN_MAX_AGE = 30 * 24 * 60 * 60  # 30 days in seconds
REFRESH_TOKEN_COOKIE_KEY = "refresh_token"
