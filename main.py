import pandas as pd
import logging
import os

from log import createLog
from server import Server
from dataprocess import process
from mysql import pd2mysql

logger = createLog()  # init log mode

server = Server()


logging.info("cheak log......")
if server.cheakLog():
    logging.info("try to download log from server......")
    if not server.downloadLog():
        raise
    logging.info("download success!")
    logging.info("---------------------------------------")
    logging.info("try to process log file......")
    if not process():
        raise
    logging.info("process success!")
    logging.info("---------------------------------------")
    logging.info("try to upload to mysql......")
    try:
        accept = pd.read_csv("accept.csv")
        reject = pd.read_csv("reject.csv")
    except:
        logging.error("open csv file failed!")
        raise
    pd2mysql(accept, "record")
    pd2mysql(reject, "rejected")
    logging.info("clean file......")
    os.remove("accept.csv")
    os.remove("reject.csv")
    os.remove("access.log")
    server.clearLog()
    logging.info("insert into mysql success")

else:
    logging.info("Log already exist")
