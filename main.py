from pandas.core.frame import DataFrame
from fromServer import cheakLog, clearLog, downloadLog
from upload import produce
from sqlalchemy import create_engine
import pandas as pd
import os


def pd2mysql(df: DataFrame, table: str):
    try:
        engine = create_engine(
            "mysql+pymysql://root:997470@localhost/vnetlog?charset=utf8"
        )
        df.to_sql(table, engine, if_exists="append", index=False)
        engine.dispose()
    except:
        raise UserWarning("mysql connect error")


print("cheak log......")
if cheakLog():
    print("try to download log from server......")
    download_state, download_msg = downloadLog()
    if not download_state:
        print(download_msg)
        raise UserWarning(download_msg)
    print("download success!")
    print("---------------------------------------")
    print("try to produce log file......")
    produce_state, produce_msg = produce()
    if not produce_state:
        print(produce_msg)
        raise UserWarning(produce_msg)
    print("produce success!")
    print("---------------------------------------")
    print("try to upload to mysql......")
    try:
        accept = pd.read_csv("accept.csv")
        reject = pd.read_csv("reject.csv")
    except:
        raise UserWarning("打开csv文件错误")
    pd2mysql(accept, "record")
    pd2mysql(reject, "rejected")
    print("clean file......")
    os.remove("accept.csv")
    os.remove("reject.csv")
    os.remove("access.log")
    clearLog()
    print("insert into mysql success")

else:
    print("Log already exist")
