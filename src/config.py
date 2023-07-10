import os


class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.mongo_uri = os.getenv("MONGODB_URI")
        self.secret_key = os.getenv(
            "SECRET_KEY",
            "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7",
        )
        self.algorithm = os.getenv("ALGORITHM", "HS256")
        self.access_token_expire_minutes = os.getenv("TOKEN_EXPIRE", 60)


config = Config()
