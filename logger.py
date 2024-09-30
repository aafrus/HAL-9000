# logger.py
import logging
from datetime import datetime

def setup_logger():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"logs_{timestamp}.log"

    logging.basicConfig(
        filename=filename,
        level=logging.INFO,
        format='%(asctime)s_%(message)s',
        datefmt='%d/%m/%Y_%H:%M'
    )

def log_event(message):
    logging.info(message)