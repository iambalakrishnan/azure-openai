import logging
import os

LOG_FILE = os.path.join("artifacts", "app.log")  # Path to the log file

def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)  # Set the logging level

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger
