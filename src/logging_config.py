import contextvars
import logging
import os
from logging.handlers import TimedRotatingFileHandler

from src.config import config

request_id_ctx_var = contextvars.ContextVar("request_id", default="-")


class RequestIdLogFormatter(logging.Formatter):
    def format(self, record):
        record.request_id = request_id_ctx_var.get("-")
        return super().format(record)


def create_logger(app_name, name):
    LOGGING_LEVEL = getattr(logging, config.log_level.upper(), logging.INFO)
    # Format: timestamp - logger - LEVEL [request_id] - message
    LOGGING_FORMAT = (
        "%(asctime)s - %(name)s - %(levelname)s [%(request_id)s] - %(message)s"
    )

    LOG_PATH = "logs/" if config.is_env_dev else config.log_path
    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH, exist_ok=True)

    LOGGING_FILENAME = f"{LOG_PATH}/{app_name}.log"
    handler = TimedRotatingFileHandler(
        LOGGING_FILENAME, when="D", interval=1, backupCount=7
    )
    handler.suffix = "%Y-%m-%d"
    handler.setLevel(LOGGING_LEVEL)
    handler.setFormatter(RequestIdLogFormatter(LOGGING_FORMAT))

    logger = logging.getLogger(name)
    logger.setLevel(LOGGING_LEVEL)
    logger.addHandler(handler)

    return logger
