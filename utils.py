# utils.py

import logging.config
import logging.handlers
import sys
import os
from signal import signal, SIGINT
from datetime import datetime

LOG_FILE_PATH='log'
LOG_NAME=f"nlp_flex_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.log"

# Check if the log path exists, and create the directory if it doesn't
if not os.path.exists(LOG_FILE_PATH):
    os.makedirs(LOG_FILE_PATH)

def handler(signalnum, frame):
    signame = SIGINT.name
    print(f'Signal handler called with signal {signame} ({signalnum})')
    raise TypeError

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": f"{LOG_FILE_PATH}/{LOG_NAME}",
            "maxBytes": 10485760,  # 10 MB
            "backupCount": 5,
            "formatter": "verbose",
        },
        # "error_file_handler": {
        #     "class": "logging.handlers.RotatingFileHandler",
        #     "filename": f"{LOG_FILE_PATH}/{LOG_NAME}",
        #     "maxBytes": 10485760,  # 10 MB
        #     "backupCount": 5,
        #     "level": "ERROR",
        #     "formatter": "verbose",
        # },
        # "warning_file_handler": {
        #     "class": "logging.handlers.RotatingFileHandler",
        #     "filename": f"{LOG_FILE_PATH}/{LOG_NAME}",
        #     "maxBytes": 10485760,  # 10 MB
        #     "backupCount": 5,
        #     "level": "WARNING",
        #     "formatter": "verbose",
        # },
        "info_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": f"{LOG_FILE_PATH}/{LOG_NAME}",
            "maxBytes": 10485760,  # 10 MB
            "backupCount": 5,
            "level": "INFO",
            "formatter": "verbose",
        },
        "console_handler": {
            "class": "logging.StreamHandler",
            "level": "DEBUG", # "INFO", # "WARNING", # "ERROR", # "CRITICAL", 
            "formatter": "verbose",
            "stream": "ext://sys.stdout",
        },
    },
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "root": {
        "handlers": ["file_handler", "console_handler"],
        "level": "INFO",
    },
}
