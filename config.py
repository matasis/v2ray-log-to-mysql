import configparser
import os
import logging

CONFIGFILE = os.getcwd() + "\\config.ini"


class Config:
    def __init__(self) -> None:
        self.config = self.__initConfig()

    def __initConfig(self):
        config = configparser.ConfigParser()
        config.read(CONFIGFILE)
        return config

    def __cheakValue(self, section: str, key: str):
        if self.config.has_section(section):
            if self.config.has_option(section=section, option=key):
                return True
            else:
                logging.error('The option "' + key + '" is not in config file!')
        else:
            logging.error('The section "' + section + '" is not in config file!')
        return False

    def getsection(self):
        return self.config.sections()

    def getValue(self, section: str, key: str):
        if self.__cheakValue(section, key):
            return self.config.get(section=section, option=key)
        else:
            raise

    def getBoolen(self, section: str, key: str):
        if self.__cheakValue(section, key):
            return self.config.getboolean(section=section, option=key)
        else:
            raise

    def getInt(self, section: str, key: str):
        if self.__cheakValue(section, key):
            return self.config.getint(section=section, option=key)
        else:
            raise

config = Config()

