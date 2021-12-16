import configparser
import os

CONFIGFILE = os.getcwd() + "\\config.ini"


def initConfig():
    config = configparser.ConfigParser()
    config.read(CONFIGFILE)
    print(config.sections())
