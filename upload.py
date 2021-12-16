import pandas as pd
import re


def getLogList():  # 从log文件中读取内容
    logfile = open("access.log", "r")
    logtext = logfile.readlines()
    accept_log = []
    reject_log = []
    loglist = [x[:-1].split(' ') for x in logtext]
    while [""] in loglist:
        loglist.remove([""])
    for log in loglist:
        if "accepted" in log:
            accept_log.append(log)
        elif "rejected" in log:
            reject_log.append(log)
        else:
            print(log)
    return accept_log, reject_log


def standAcceptItem(item: list) -> list:  # 处理分割协议、地址、端口
    def spl(ip_record: str) -> list:
        pre = ip_record.split(":")
        pre_len = len(pre)
        if pre_len == 2:
            pre.insert(0, "")
            rec = pre
        elif pre_len > 3:
            rec = re.split(":\[|\]:", ip_record)
        else:
            rec = pre
        return rec
    from_info = spl(item[2])
    target_info = spl(item[4])
    try:
        user = item[-1].split('@')[0]
        record = item[:2]+from_info+item[3:4]+target_info+[user]
    except:
        print(item, from_info, target_info)
    return record


def standRejectItem(item: list) -> list:  # 处理拒绝的协议
    while "" in item:
        item.remove("")
    from_info = item[2].split(":")
    if len(from_info) == 2:
        from_info.insert(0, "")
    error_info = " ".join(item[4:])
    record = item[:2]+from_info+item[3:4]+[error_info]
    record[-1] = record[-1].strip()
    return record


def produce():  # 处理数据
    try:
        accept_log, reject_log = getLogList()
    except:
        return False, "can not load log file"
    accept_columns = ['rdate', 'rtime', 'from_protocol', 'from_ip', 'from_port',
                      'state', 'target_protocol', 'target', 'target_port', 'user']
    reject_columns = ['rdate', 'rtime', 'from_protocol',
                      'from_ip', 'from_port', 'state', 'err_msg']
    accepted_record = []
    rejected_record = []
    try:
        for accept in accept_log:
            accepted_record.append(standAcceptItem(accept))
        for reject in reject_log:
            rejected_record.append(standRejectItem(reject))
        accept_log_dataframe = pd.DataFrame(
            accepted_record, index=None, columns=accept_columns)
        accept_log_dataframe = accept_log_dataframe.drop_duplicates()
        accept_log_dataframe.to_csv("accept.csv", index=False)
        reject_log_dataframe = pd.DataFrame(
            rejected_record, index=None, columns=reject_columns)
        reject_log_dataframe = reject_log_dataframe.drop_duplicates()
        reject_log_dataframe.to_csv("reject.csv", index=False)
    except:
        return False, "data error"
    return True, "Success"
