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

mysql_host = config.getValue("mysql", "Host")
mysql_port = config.getValue("mysql", "Port")
mysql_username = config.getValue("mysql", "Username")
mysql_passwd = config.getValue("mysql", "Password")
mysql_database = config.getValue("mysql", "Database")


def pd2mysql(df: DataFrame, table: str):
    try:
        engine = create_engine(
            "mysql+pymysql://{user}:{passwd}@{host}:{port}/{database}".format(
                user=mysql_username,
                passwd=mysql_passwd,
                host=mysql_host,
                port=mysql_port,
                database=mysql_database,
            )
        )
        df.to_sql(table, engine, if_exists="append", index=False)
        engine.dispose()
    except:
        raise UserWarning("mysql connect error")


print("cheak log......")
if fromServer.cheakLog():
    print("try to download log from server......")
    download_state, download_msg = fromServer.downloadLog()
    if not download_state:
        print(download_msg)
        raise UserWarning(download_msg)
    print("download success!")
    print("---------------------------------------")
    print("try to process log file......")
    process_state, process_msg = upload.process()
    if not process_state:
        print(process_msg)
        raise UserWarning(process_msg)
    print("process success!")
    print("---------------------------------------")
    print("try to upload to mysql......")
    try:
        accept = pd.read_csv("accept.csv")
        reject = pd.read_csv("reject.csv")
    except:
        raise UserWarning("open csv file failed!")
    pd2mysql(accept, "record")
    pd2mysql(reject, "rejected")
    print("clean file......")
    os.remove("accept.csv")
    os.remove("reject.csv")
    os.remove("access.log")
    fromServer.clearLog()
    print("insert into mysql success")

else:
    print("Log already exist")
