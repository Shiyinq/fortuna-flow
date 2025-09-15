import os

from dotenv import load_dotenv

load_dotenv(verbose=True)


def validate_required_env_vars():
    required_vars = [
        "SECRET_KEY",
        "MONGODB_URI",
        "ALGORITHM",
        "GOOGLE_CLIENT_ID",
        "GOOGLE_CLIENT_SECRET",
        "GOOGLE_REDIRECT_URI",
        "GITHUB_CLIENT_ID",
        "GITHUB_CLIENT_SECRET",
        "GITHUB_REDIRECT_URI",
        "FRONTEND_URL",
        "RESEND_API_KEY",
        "EMAIL_FROM",
        "ORIGINS",
    ]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {missing_vars}")


def get_cors_origins(origins_str: str, is_dev: bool = False) -> list:
    if not origins_str:
        if is_dev:
            return ["http://localhost:5050", "http://localhost:5173"]
        else:
            raise ValueError("ORIGINS environment variable is required in production")

    origins = [origin.strip() for origin in origins_str.split(",") if origin.strip()]

    if not is_dev:
        for origin in origins:
            if origin == "*":
                raise ValueError("Wildcard (*) origins are not allowed in production")
            if not origin.startswith("https://"):
                raise ValueError(f"Only HTTPS origins allowed in production: {origin}")

    return origins


class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        validate_required_env_vars()
        self.mongo_uri = os.getenv("MONGODB_URI")
        self.secret_key = os.getenv("SECRET_KEY")
        self.algorithm = os.getenv("ALGORITHM")
        self.access_token_expire_minutes = int(
            os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15")
        )
        self.refresh_token_max_age_days = int(
            os.getenv("REFRESH_TOKEN_MAX_AGE_DAYS", "30")
        )
        self.google_client_id = os.getenv("GOOGLE_CLIENT_ID")
        self.google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        self.google_redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
        self.github_client_id = os.getenv("GITHUB_CLIENT_ID")
        self.github_client_secret = os.getenv("GITHUB_CLIENT_SECRET")
        self.github_redirect_uri = os.getenv("GITHUB_REDIRECT_URI")
        self.frontend_url = os.getenv("FRONTEND_URL")
        self.is_env_dev = os.getenv("ENV", "dev") == "dev"

        # Email configuration
        self.resend_api_key = os.getenv("RESEND_API_KEY")
        self.email_from = os.getenv("EMAIL_FROM", "onboarding@resend.dev")
        self.email_verification_expire_hours = int(
            os.getenv("EMAIL_VERIFICATION_EXPIRE_HOURS", "24")
        )
        self.password_reset_expire_hours = int(
            os.getenv("PASSWORD_RESET_EXPIRE_HOURS", "1")
        )

        # Security configuration
        self.max_login_attempts = int(os.getenv("MAX_LOGIN_ATTEMPTS", "5"))
        self.account_lockout_minutes = int(os.getenv("ACCOUNT_LOCKOUT_MINUTES", "15"))
        self.max_requests_per_minute = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "60"))
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_path = os.getenv("LOG_PATH", "/var/log/fortuna-flow/")

        # CORS configuration
        self.cors_origins = get_cors_origins(os.getenv("ORIGINS", ""), self.is_env_dev)

        # API Key Prefix
        self.api_key_prefix = "ffk_"


config = Config()
