import datetime
import logging

import paramiko

from config import config

# server for sftp and ssh
SERVER_HOST = config.getValue("server", "Host")
SERVER_PORT = config.getValue("server", "Port")
SERVER_USERNAME = config.getValue("server", "Username")
SERVER_PASSWD = config.getValue("server", "Password")

# v2ray log
LOG_DIR = config.getValue("v2ray_log", "Log_dir")
LOG_BACKUP_DIR = config.getValue("v2ray_log", "Backup_dir")
LOG_FILENAME = config.getValue("v2ray_log", "Log_filename")

class Server:
    def __sftpConn(self):
        transport = paramiko.Transport((SERVER_HOST, SERVER_PORT))
        transport.connect(
            username=SERVER_USERNAME, password=SERVER_PASSWD
        )  # connect to server
        return transport


    def __sshConn(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=SERVER_HOST,
            port=SERVER_PORT,
            username=SERVER_USERNAME,
            password=SERVER_PASSWD,
        )
        return ssh


    def downloadLog(self,logdir: str = LOG_DIR, filename: str = LOG_FILENAME):  # /root/logbackup/
        """
        Download log from server
        """
        if logdir[-1] != "/":
            logdir += "/"
        try:
            transport = self.__sftpConn()  # create sftp connect
        except:
            logging.error("sftp connect error!")
            return False
        try:
            sftp = paramiko.SFTPClient.from_transport(transport)
            sftp.get(logdir + filename, "access.log")  # download log file
        except:
            logging.error("can not download target file!")
            return False
        transport.close()
        return True


    def cheakLog(self):
        """
        Check if the logs have been uploaded,limited to one upload a day.
        """
        try:
            ssh = self.__sshConn()
            stdin, stdout, stderr = ssh.exec_command(
                "cd {backupdir};ls".format(backupdir=LOG_BACKUP_DIR)
            )
        except:
            logging.error("ssh connect error")
            raise
        result = str(stdout.read(), encoding="utf-8")
        ssh.close()
        if str(datetime.date.today()) in result:
            return False
        else:
            return True


    def clearLog(self,logdir:str=LOG_DIR, logfilename:str=LOG_FILENAME, backupdir:str=LOG_BACKUP_DIR):  # clean server log file
        """
        Clean up the logs on the server,and backup the logs to the specified folder
        """
        try:
            ssh = self.__sshConn()
            ssh.exec_command(
                "cp {logdir}/{logfilename} {backupdir}/acc-".format(logdir=logdir, logfilename=logfilename, backupdir=logfilename)
                + str(datetime.date.today()) 
                + "-"
                + str(datetime.datetime.time(datetime.datetime.today()))[:8]
                + ".log;echo \"\" > {logdir}/{logfilename}".format(logdir=logdir, logfilename=logfilename)
            )
            ssh.close()
        except:
            logging.error("ssh connect error!")
            return False
        return True
