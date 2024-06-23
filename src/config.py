import os

from dotenv import load_dotenv

load_dotenv(verbose=True)


class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.mongo_uri = os.getenv("MONGODB_URI")
        self.secret_key = os.getenv("SECRET_KEY")
        self.algorithm = os.getenv("ALGORITHM")
        self.access_token_expire_minutes = os.getenv("TOKEN_EXPIRE")
        self.google_client_id = os.getenv("GOOGLE_CLIENT_ID")
        self.google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        self.google_redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
        self.github_client_id = os.getenv("GITHUB_CLIENT_ID")
        self.github_client_secret = os.getenv("GITHUB_CLIENT_SECRET")
        self.github_redirect_uri = os.getenv("GITHUB_REDIRECT_URI")
        self.frontend_url = os.getenv("FRONTEND_URL")


config = Config()
