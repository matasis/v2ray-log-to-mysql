import datetime
import os
import logging
from logging.handlers import TimedRotatingFileHandler

DEBUG_MODE = True
ALL_LOG = os.getcwd() + "\\all.log"
ERROR_LOG = os.getcwd() + "\\error.log"


def createLog():
    logger = logging.getLogger()

    if DEBUG_MODE:
        logger.setLevel(logging.DEBUG)

    rf_handler = TimedRotatingFileHandler(
        ALL_LOG,
        when="midnight",
        interval=1,
        backupCount=7,
        atTime=datetime.time(0, 0, 0, 0),
    )
    rf_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )

    f_handler = logging.FileHandler(ERROR_LOG)
    f_handler.setLevel(logging.ERROR)
    f_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"
        )
    )

    logger.addHandler(rf_handler)
    logger.addHandler(f_handler)
    return logger

