import os
import logging
import sys
from logging.handlers import RotatingFileHandler


FORMATTER = logging.Formatter('%(asctime)s — %(name)s — %(levelname)s — %(message)s')
INFO_LOG_FILE = os.path.join('logs', 'info.log')
DEBUG_LOG_FILE = os.path.join('logs', 'debug.log')
ERROR_LOG_FILE = os.path.join('logs', 'error.log')

# Create log folder if it doesn't exist.
if not os.path.isdir('logs'):
    os.mkdir('logs')


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    console_handler.setLevel(logging.INFO)
    return console_handler


def get_info_handler():
    return get_file_handler(file_path=INFO_LOG_FILE, level=logging.INFO)


def get_debug_handler():
    return get_file_handler(file_path=DEBUG_LOG_FILE, level=logging.DEBUG)


def get_error_handler():
    return get_file_handler(file_path=ERROR_LOG_FILE, level=logging.ERROR)


def get_file_handler(file_path: str, level: int) -> RotatingFileHandler:
    file_handler = RotatingFileHandler(file_path)
    file_handler.setFormatter(FORMATTER)
    file_handler.setLevel(level)

    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_info_handler())
    logger.addHandler(get_debug_handler())
    logger.addHandler(get_error_handler())
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger
