import paramiko
import datetime

from config import config

server_host = config.getValue("server", "Host")
server_port = config.getValue("server", "Port")
server_username = config.getValue("server", "Username")
server_passwd = config.getValue("server", "Password")


def sftpConn():
    transport = paramiko.Transport((server_host, server_port))
    transport.connect(
        username=server_username, password=server_passwd
    )  # connect to server
    return transport


def sshConn():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        hostname=server_host,
        port=server_port,
        username=server_username,
        password=server_passwd,
    )
    return ssh


def downloadLog(logdir: str = "/var/log/v2ray/", filename: str = "access.log"):  # /root/logbackup/
    if logdir[-1] != "/":
        return False, "log dir mast end with '/'"
    try:
        transport = sftpConn()  # create sftp connect
    except:
        return False, "Access error"
    try:
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.get(logdir + filename, filename)  # download log file
    except:
        return False, "Download error"
    transport.close()
    return True, "Success"


def cheakLog():
    try:
        ssh = sshConn()
        stdin, stdout, stderr = ssh.exec_command("cd /root/logbackup;ls")
    except:
        raise UserWarning("Connect error")
    result = str(stdout.read(), encoding="utf-8")
    ssh.close()
    if str(datetime.date.today()) in result:
        return False
    else:
        return True


def clearLog():  # 清除服务器日志文件
    try:
        ssh = sshConn()
        ssh.exec_command(
            "cp /var/log/v2ray/access.log /root/logbackup/acc-"
            + str(datetime.date.today())  # 备份
            + "-"
            + str(datetime.datetime.time(datetime.datetime.today()))[:8]
            + '.log;echo "" > /var/log/v2ray/access.log'
        )
        ssh.close()
    except:
        return False, "Connect error"
