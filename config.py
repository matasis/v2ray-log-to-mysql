import configparser

CONFIGFILE="/usr/local/etc/pyssr/config.ini"

def initConfig():
    config=configparser.ConfigParser()
    config.read(CONFIGFILE)
    print(config.sections())