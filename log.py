import datetime
import os
import logging
from logging.handlers import TimedRotatingFileHandler

DEBUG_MODE = True

if "log" not in os.listdir():   # cheak the log folder is in the root directory if not create it
    os.mkdir("log")

ALL_LOG = os.getcwd() + "\\log\\all.log"
ERROR_LOG = os.getcwd() + "\\log\\error.log"


def createLog(debug_mode: bool = False):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    st_handler=logging.StreamHandler()
    st_handler.setLevel(logging.INFO)
    if debug_mode:
        st_handler.setLevel(logging.debug)
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
    logger.addHandler(st_handler)
    logger.addHandler(rf_handler)
    logger.addHandler(f_handler)
    return logger
