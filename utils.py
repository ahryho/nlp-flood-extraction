# utils.py

import logging
import logging.handlers
from os import path
import sys
import traceback
from datetime import datetime
from signal import signal, SIGINT

LOG_FILE_PATH='logs'
LOG_NAME='nlp_flex'

def handler(signalnum, frame):
    signame = SIGINT.name
    print(f'Signal handler called with signal {signame} ({signalnum})')
    raise TypeError

def listener_configurer(log_name, log_file_path):
    """ Configures and returns a log file based on the given name

    Arguments:
        log_name (str): String of the log name to use
        log_file_path (str): String of the log file path

    Returns:
        logger: configured logging object
    """
    logger = logging.getLogger(log_name)

    fh = logging.FileHandler(
        path.join(log_file_path, f'{log_name}.log')) #_{datetime.now().strftime('%Y-%m-%d')}.log'), encoding='cp1252')
    fmtr = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(fmtr)
    logger.setLevel(logging.INFO)
    # current_fh_names = [fh.__dict__.get(
    #    'baseFilename', '') for fh in logger.handlers]
    # if not fh.__dict__['baseFilename'] in current_fh_names: # This prevents multiple logs to the same file
    logger.addHandler(fh)

    return logger

def listener_process(queue, configurer, log_name):
    """ Listener process is a target for a multiprocess process that runs and listens to a queue for logging events.

    Arguments:
        queue (multiprocessing.manager.Queue): queue to monitor
        configurer (func): configures loggers
        log_name (str): name of the log to use

    Returns:
        None
    """
    configurer(log_name, LOG_FILE_PATH)

    while True:
        try:
            record = queue.get()
            if record is None:
                break
            logger = logging.getLogger(record.name)
            logger.handle(record)
        except Exception:
            print('Failure in listener_process', file=sys.stderr)
            traceback.print_last(limit=1, file=sys.stderr)

# def configure_logging():
#     """
#     Configures logging to write both to the console and a file.

#     Returns:
#         None
#     """
#     # Create a log file with a timestamp
#     log_file = f"logs/nlp_flex_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

#     # Log everything to file
#     logging.basicConfig(level=logging.INFO)

#     # Create a file handler and set the logging level to INFO
#     file_handler = logging.FileHandler(log_file, encoding='cp1252')
#     file_handler.setLevel(logging.INFO)

#     # Create a console handler and set the logging level to INFO
#     console_handler = logging.StreamHandler(sys.stdout)
#     console_handler.setLevel(logging.INFO)

#     # Create a formatter
#     formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

#     # Set the formatter for both handlers
#     file_handler.setFormatter(formatter)
#     console_handler.setFormatter(formatter)

#     # Get the root logger
#     logger = logging.getLogger()

#     # Add both handlers to the logger
#     logger.addHandler(file_handler)
#     logger.addHandler(console_handler)

#     # Return the log file path
#     return log_file
