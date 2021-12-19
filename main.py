import logging

from log import createLog
from server import Server
from dataprocess import process
from mysql import df2mysql
from config import config

logger = createLog(config.getBoolen("debug", "Debug_mode"))  # init log mode

server = Server()


logging.info("cheak log......")
if server.cheakLog():
    logging.info("try to download log from server......")
    if not server.downloadLog():
        raise
    logging.info("download success!")
    logging.info("---------------------------------------")
    logging.info("try to process log file......")
    log_data = process()
    if log_data is None:
        raise
    logging.info("process success!")
    logging.info("---------------------------------------")
    logging.info("try to upload to mysql......")
    accept = log_data[0]
    reject = log_data[1]
    df2mysql(accept, "accept")
    df2mysql(reject, "reject")
    logging.info("clean file......")
    server.clearLog()
    logging.info("insert into mysql success")

else:
    logging.info("Log already exist")

