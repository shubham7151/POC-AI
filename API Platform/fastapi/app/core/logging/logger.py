import logging
from logging.handlers import RotatingFileHandler

def configure_logger() -> logging.Logger:
    logger = logging.getLogger("app_logger")
    logger.setLevel(logging.DEBUG)
    
    # Create handlers
    console_handler = logging.StreamHandler()
    file_handler = RotatingFileHandler("app.log", maxBytes=10485760, backupCount=3)

    # Set level for handlers
    console_handler.setLevel(logging.DEBUG)
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger

logger = configure_logger()