import logging
from logging.handlers import RotatingFileHandler


def configure_logger():
    # Create a logger
    logger = logging.getLogger("app_logger")
    logger.setLevel(logging.DEBUG)

    # Create handlers
    console_handler = logging.StreamHandler()
    file_handler = RotatingFileHandler("app.log", maxBytes=1000000, backupCount=3)

    # Set log levels
    console_handler.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)

    # Create formatters and add them to handlers
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# Configure the logger
logger = configure_logger()
