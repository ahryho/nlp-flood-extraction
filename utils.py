# utils.py

import logging
import sys
from datetime import datetime
from signal import signal, SIGINT

def handler(signalnum, frame):
    signame = SIGINT.name
    print(f'Signal handler called with signal {signame} ({signalnum})')
    raise TypeError

def configure_logging():
    """
    Configures logging to write both to the console and a file.

    Returns:
        None
    """
    # Create a log file with a timestamp
    log_file = f"logs/nlp_flex_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

    logging.basicConfig(level=logging.INFO)

    # Create a file handler and set the logging level to INFO
    file_handler = logging.FileHandler(log_file, encoding='cp1252')
    file_handler.setLevel(logging.INFO)

    # Create a console handler and set the logging level to INFO
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Set the formatter for both handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Get the root logger
    logger = logging.getLogger()

    # Add both handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Return the log file path
    return log_file
