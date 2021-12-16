import paramiko
import datetime

backupdir = "/var/log/v2ray/"
todaylog = "acc-"+str(datetime.date.today())+".log"


def sftpConn():
    transport = paramiko.Transport(
        ("104.128.88.164", 26359))    # 获取Transport实例
    transport.connect(username="root", password="Yyk997470..")    # 建立连接
    return transport


def sshConn():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname="104.128.88.164", port=26359,
                username="root", password="Yyk997470..")
    return ssh


def downloadLog(logdir: str = "/var/log/v2ray/", filename: str = "access.log"):  # /root/logbackup/
    if logdir[-1] != '/':
        return False, "log dir mast end with \'/\'"
    try:
        transport = sftpConn()  # 创建连接
    except:
        return False, "Access error"
    try:
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.get(logdir+filename, filename)  # 下载log文件
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
        ssh.exec_command("cp /var/log/v2ray/access.log /root/logbackup/acc-" +  # 备份
                         str(datetime.date.today())+"-"+str(datetime.datetime.time(datetime.datetime.today()))[:8]+".log;echo \"\" > /var/log/v2ray/access.log")
        ssh.close()
    except:
        return False, "Connect error"
