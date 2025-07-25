import os

import motor.motor_asyncio
from dotenv import load_dotenv

load_dotenv(verbose=True)


class Database:
    _instance = None

    @staticmethod
    def get_instance():
        if Database._instance is None:
            Database._instance = Database()
        return Database._instance

    def __init__(self):
        os.environ.setdefault("MONGODB_URI", "mongodb://localhost:27017")
        os.environ.setdefault("DB_NAME", "local")
        mongo_uri = os.getenv("MONGODB_URI")
        db_name = os.getenv("DB_NAME")

        from src.logging_config import create_logger

        self.logger = create_logger("database", __name__)

        try:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(
                mongo_uri, maxPoolSize=50
            )
            self.database = self.client[db_name]
            self.logger.info(f"Connected to database: {db_name}")
        except Exception as e:
            self.logger.exception(
                f"An error occurred while connecting to the database: {str(e)}"
            )


database_instance = Database.get_instance()
database = database_instance.database
