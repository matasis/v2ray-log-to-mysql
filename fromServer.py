import logging
import paramiko
import datetime

from config import config

# server for sftp and ssh
SERVER_HOST = config.getValue("server", "Host")
SERVER_PORT = config.getValue("server", "Port")
SERVER_USERNAME = config.getValue("server", "Username")
SERVER_PASSWD = config.getValue("server", "Password")

# v2ray log
LOG_DIR = config.getValue("v2ray_log", "Logdir")
LOG_BACKUP_DIR = config.getValue("v2ray_log", "Backup_dir")
LOG_FILENAME = config.getValue("v2ray_log", "Log_filename")


def sftpConn():
    transport = paramiko.Transport((SERVER_HOST, SERVER_PORT))
    transport.connect(
        username=SERVER_USERNAME, password=SERVER_PASSWD
    )  # connect to server
    return transport


def sshConn():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        hostname=SERVER_HOST,
        port=SERVER_PORT,
        username=SERVER_USERNAME,
        password=SERVER_PASSWD,
    )
    return ssh


def downloadLog(logdir: str = LOG_DIR, filename: str = LOG_FILENAME):  # /root/logbackup/
    if logdir[-1] != "/":
        logdir += "/"
    try:
        transport = sftpConn()  # create sftp connect
    except:
        logging.error("sftp connect error!")
        return False
    try:
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.get(logdir + filename, filename)  # download log file
    except:
        logging.error("can not download target file!")
        return False
    transport.close()
    return True


def cheakLog():
    try:
        ssh = sshConn()
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


def clearLog():  # clean server log file
    try:
        ssh = sshConn()
        ssh.exec_command(
            "cp {logdir}/{logfilename} {backupdir}/acc-".format(logdir=LOG_DIR, logfilename=LOG_FILENAME, backupdir=LOG_BACKUP_DIR)
            + str(datetime.date.today()) 
            + "-"
            + str(datetime.datetime.time(datetime.datetime.today()))[:8]
            + ".log;echo \"\" > /var/log/v2ray/access.log"
        )
        ssh.close()
    except:
        logging.error("ssh connect error!")
        return False
    return True
