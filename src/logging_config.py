import logging
from logging.handlers import TimedRotatingFileHandler


def create_logger(app_name, name):
    LOGGING_LEVEL = logging.INFO
    LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOGGING_LOCATION = "logs/"
    LOGGING_FILENAME = f"{LOGGING_LOCATION}/{app_name}.log"

    handler = TimedRotatingFileHandler(
        LOGGING_FILENAME, when="D", interval=1, backupCount=7
    )

    handler.suffix = "%Y-%m-%d"
    handler.setLevel(LOGGING_LEVEL)
    handler.setFormatter(logging.Formatter(LOGGING_FORMAT))

    logger = logging.getLogger(name)
    logger.setLevel(LOGGING_LEVEL)
    logger.addHandler(handler)

    return logger
