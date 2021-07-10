import logging
import sys
from os import environ as env
from logging.handlers import TimedRotatingFileHandler

FORMATTER: logging.Formatter = logging.Formatter("%(asctime)-16s - %(name)24s - %(levelname)8s - %(message)s")
LOG_FILE: str = "logs/ArchieMate.log"
IRC_FILE: str = "logs/IRC.log"
DEBUG: bool = env.get("DEBUG", "0").upper() in ("TRUE", "1")

def get_console_handler() -> logging.StreamHandler:
    console_handler : logging.StreamHandler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler

def get_file_handler() -> TimedRotatingFileHandler:
    file_handler : TimedRotatingFileHandler = TimedRotatingFileHandler(LOG_FILE, when="W0")
    file_handler.setFormatter(FORMATTER)
    return file_handler

def get_logger(logger_name: str) -> logging.Logger:
    logger: logging.Logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG if DEBUG else logging.WARNING) # Better to have too much log than not enough
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    # With this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger

def get_irc_logger(logger_name: str) -> logging.Logger:
    irc_handler: TimedRotatingFileHandler = TimedRotatingFileHandler(IRC_FILE, when="W0")
    irc_handler.setFormatter(FORMATTER)
    
    irc_logger: logging.Logger = logging.getLogger(f"IRC_{logger_name}")
    irc_logger.setLevel(logging.DEBUG)
    irc_logger.addHandler(irc_handler)
    irc_logger.propagate = False
    return irc_logger
