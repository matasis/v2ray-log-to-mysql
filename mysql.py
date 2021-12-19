import logging
from pandas.core.frame import DataFrame
from sqlalchemy import create_engine

from config import config

MYSQL_HOST = config.getValue("mysql", "Host")
MYSQL_PORT = config.getValue("mysql", "Port")
MYSQL_USERNAME = config.getValue("mysql", "Username")
MYSQL_PASSWD = config.getValue("mysql", "Password")
MYSQL_DATABASE = config.getValue("mysql", "Database")


def df2mysql(df: DataFrame, table: str):
    """
    Please create a database before use.
    Tables are automatically created in the database when first used.
    """
    try:
        mysql_link = "mysql+pymysql://{user}:{passwd}@{host}:{port}/{database}".format(
            user=MYSQL_USERNAME,
            passwd=MYSQL_PASSWD,
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            database=MYSQL_DATABASE,
        )
        logging.debug("create mysql engine with " + mysql_link)
        engine = create_engine(mysql_link)
    except Exception as e:
        logging.error(e)
        logging.error("mysql connect error")
        raise
    try:
        df.to_sql(table, engine, if_exists="append", index=False)
        logging.debug("insert dataframe to mysql")
        engine.dispose()
    except Exception as e:
        logging.error(e)
        logging.error("can not insert into mysql.")
        raise

