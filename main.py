from pandas.core.frame import DataFrame
from sqlalchemy import create_engine
import pandas as pd
import logging
import os

from config import config
import log
import fromServer
import upload

logger = log.createLog()  # init log mode

MYSQL_HOST = config.getValue("mysql", "Host")
MYSQL_PORT = config.getValue("mysql", "Port")
MYSQL_USERNAME = config.getValue("mysql", "Username")
MYSQL_PASSWD = config.getValue("mysql", "Password")
MYSQL_DATABASE = config.getValue("mysql", "Database")


def pd2mysql(df: DataFrame, table: str):
    try:
        engine = create_engine(
            "mysql+pymysql://{user}:{passwd}@{host}:{port}/{database}".format(
                user=MYSQL_USERNAME,
                passwd=MYSQL_PASSWD,
                host=MYSQL_HOST,
                port=MYSQL_PORT,
                database=MYSQL_DATABASE,
            )
        )
        df.to_sql(table, engine, if_exists="append", index=False)
        engine.dispose()
    except:
        logging.error("mysql connect error")
        raise


logging.info("cheak log......")
if fromServer.cheakLog():
    logging.info("try to download log from server......")
    if not fromServer.downloadLog():
        raise
    logging.info("download success!")
    logging.info("---------------------------------------")
    logging.info("try to process log file......")
    if not upload.process():
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
    fromServer.clearLog()
    logging.info("insert into mysql success")

else:
    logging.info("Log already exist")
