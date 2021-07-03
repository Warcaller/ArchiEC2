import logging
import sys
from os import environ as env
from logging.handlers import TimedRotatingFileHandler
FORMATTER = logging.Formatter("%(asctime)-16s - %(name)24s - %(levelname)8s - %(message)s")
LOG_FILE = "logs/ArchieMate.log"
DEBUG = env.get("DEBUG").upper() in ("TRUE", "1")

def get_console_handler() -> logging.StreamHandler:
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler

def get_file_handler() -> TimedRotatingFileHandler:
    file_handler = TimedRotatingFileHandler(LOG_FILE, when="W0")
    file_handler.setFormatter(FORMATTER)
    return file_handler

def get_logger(logger_name: str) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG if DEBUG else logging.WARNING) # Better to have too much log than not enough
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    # With this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger
