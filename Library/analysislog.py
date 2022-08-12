import subprocess
import time
from Tools.value import var
from Tools.logger import log

class Check_dmlog(object):

    def __init__(self):
        self.year = var.V_YEAR

    def get_time(self, line):
        if line.startswith('0') or line.startswith('1'):  #####new change point
            log_time = line.split(" ")[0]
            month = log_time[0:2]
            day = log_time[3:5]
            log_time = line.split(" ")[1]
            hour = log_time[:2]
            minute = log_time[3:5]
            second = log_time[6:8]
            millisecond = log_time[15:18]
            whole_time = self.year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second  # + '.' + millisecond
            timeArray = time.strptime(whole_time, '%Y-%m-%d %H:%M:%S')
            timeStamp = int(time.mktime(timeArray))
            return timeStamp

    def getstr(self, cmd):
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = process.communicate()
        retcode = process.poll()
        if retcode:
            if len(str(err)[2:-1]) == 0:
                pass
            else:
                log.error(str(err)[2:-5])
            return False
        else:
            self.outputall = str(output).replace('\\r\\r\\n', '\n')[2:-5].split("\n")
            if self.outputall == ['grep: /mnt/ota/data/log/dmclient.log: No such file or direct']:
                log.error(self.outputall)
                return False
            else:
                return self.outputall

    # 检测车云通讯
    def check_connection(self, current_time):
        connect_line = self.getstr(f"adb shell adb shell grep DCS_SOTA_REPLY /mnt/sdcard/log/ota/dmclient.log")
        if connect_line is False:
            return False, None
        else:
            if len(connect_line) == 0 or connect_line == [""]:
                return False, None
            else:
                log_time = self.get_time(connect_line[-1])
                if isinstance(log_time, int):
                    gap_time = int(current_time) - log_time
                    if gap_time < 300:
                        log.info(connect_line)
                        return True, connect_line
                    else:
                        return False, None
                else:
                    return False, None

    # 接收任务
    def handle_campaign(self, ID):
        lines = self.getstr(f"adb shell adb shell cat /mnt/sdcard/log/ota/dmclient.log")
        for line in lines:
            if "xl4.sota-report" in line and f'"id": "{ID}"' in line:
                log.info(line)
                return True, line
            else:
                pass
        return False, None

    # 检查版本
    def get_version(self, ID):
        lines = self.getstr(f"adb shell adb shell cat /mnt/ota/data/log/dmclient.log")
        for line in lines:
            if "xl4.query-package" in line and f'"id": "{ID}"' in line:
                self.keyid = line.split('"reply-id": ')[1].split(', "body"')[0]
                log.info(line)
                return True, line
            else:
                pass
        return False, None

    # 检查版本
    def cehck_version(self):
        lines = self.getstr(f"adb shell adb shell cat /mnt/ota/data/log/dmclient.log")
        for line in lines:
            if "xl4.query-package" in line and self.keyid in line and "on_message" in line:
                line_version = line.split('"version": ')[1].split(' } } }')[0]
                if line_version == "null":
                    log.error("版本为空，任务无法下载")
                    return False, None
                else:
                    log.info(f"上传当前版本为：{line_version}")
                    return True, line
            else:
                pass
        log.error("未收到上传版本信息日志")
        return False, None

    # 任务开始
    def start_campaign(self, id):
        lines = self.getstr(f"adb shell adb shell cat /mnt/ota/data/log/dmclient.log")
        for line in lines:
            if "xl4.campaign-update" in line and '"event": "START"' in line and f'"id": "{id}"' in line:
                log.info(line)
                return True, line
            else:
                pass
        return False, None

    # 检查下载策略
    def download_policy_check(self, id):
        lines = self.getstr(f"adb shell adb shell cat /mnt/ota/data/log/dmclient.log")
        for line in lines:
            if "xl4.policy-check-query" in line and '"stage": "download"' in line and f'"id": "{id}"' in line:
                self.reference_id = line.split('"reference": ')[1].split(', "satisfied"')[0]
                log.info(line)
                return True, line
            else:
                pass
        return False, None

    # 检查下载策略结果
    def download_policy_result(self):
        line_list = []
        lines = self.getstr(f"adb shell adb shell cat /mnt/ota/data/log/dmclient.log")
        for line in lines:
            if "xl4.policy-check-update" in line and self.reference_id in line:
                line_list.append(line)
            else:
                pass
        if len(line_list) == 0:
            return False, None
        else:
            linefast = line_list[-1]
            if '"satisfied": true' in linefast:
                log.info("下载策略通过")
                return True, linefast
            elif '"satisfied": false' in linefast:
                log.error("下载策略不通过")
                return False, linefast
            else:
                return False, None

    # 准备好下载
    def ready_download(self, id):
        lines = self.getstr(f"adb shell adb shell cat /mnt/ota/data/log/dmclient.log")
        for line in lines:
            if "xl4.ready-download" in line and f'"id": "{id}"' in line:
                log.info(line)
                return True, line
            else:
                pass
        return False, None

    # 准备下载
    def download_prepare(self, id):
        lines = self.getstr(f"adb shell adb shell cat /mnt/ota/data/log/dmclient.log")
        for line in lines:
            if "xl4.download-report" in line and f'"id": "{id}"' in line and 'DS_PREPARE' in line:
                return True, line
            else:
                pass
        return False, None

    # 连接下载
    def download_connect(self, id):
        lines = self.getstr(f"adb shell adb shell cat /mnt/ota/data/log/dmclient.log")
        for line in lines:
            if "xl4.download-report" in line and f'"id": "{id}"' in line and 'DS_CONNECT' in line:
                log.info(line)
                return True, line
            else:
                pass
        return False, None

    def ivi_download_progress(self, id):
        a = []
        lines = self.getstr(f"adb shell grep DOWNLOAD_REPORT /data/logcat/logcat.txt")
        if lines is False:
            return False, "没有开始下载"
        else:
            for line in lines:
                line.split("\r")
                if "xl4.update-status" in line and 'DOWNLOAD_REPORT' in line:
                    a.append(line)
                else:
                    pass
            if a == []:
                return False, "没有开始下载"
            else:
                total_bytes = int(a[-1].split('"total-bytes": ')[-1].split(', "downloaded-bytes"')[0])
                download_bytes = int(a[-1].split('"downloaded-bytes": ')[-1].split(', "expected-bytes"')[0])
                downloadprogress = "{:.0%}".format(download_bytes / total_bytes)
                return True, downloadprogress

    # 下载进度
    def download_progress(self, id):
        a = []
        lines = self.getstr(f"adb shell adb shell cat /mnt/log/ota/dmclient.log")
        if lines is False:
            return False, "没有开始下载"
        else:
            for line in lines:
                if "xl4.download-report" in line and f'"id": "{id}"' in line and 'DS_DOWNLOAD' in line:
                    a.append(line)
                else:
                    pass
            if a == []:
                return False, "没有开始下载"
            else:
                total_bytes = int(a[-1].split('"total-bytes": ')[1].split(', "downloaded-bytes"')[0])
                download_bytes = int(a[-1].split('"downloaded-bytes": ')[1].split(', "expected-bytes"')[0])
                downloadprogress = "{:.0%}".format(download_bytes / total_bytes)
                return True, downloadprogress

    # 验签
    def download_verify(self, id):
        lines = self.getstr(f"adb shell adb shell cat /mnt/ota/data/log/dmclient.log")
        for line in lines:
            if "xl4.download-report" in line and f'"id": "{id}"' in line and "DS_VERIFY" in line:
                return True, line
            else:
                pass
        return False, None

    # 验签结果
    def verify_result(self, current_time):
        lines = self.getstr(f"adb shell adb shell cat /mnt/ota/data/log/dmclient.log")
        for line in lines:
            if "pkcs7 signature verified OK" in line:
                logtime = self.get_time(line)
                if logtime > current_time:
                    log.info("验签成功")
                    return True, line
                else:
                    pass
            elif "DLE_VERIFY" in line:
                log.info("验签失败")
                return False, line
            else:
                pass
        return None, None

    # 下载成功
    def download_success(self, id):
        lines = self.getstr(f"adb shell adb shell cat /mnt/ota/data/log/dmclient.log")
        for line in lines:
            if "xl4.download-report" in line and f'"id": "{id}"' in line and '"downloaded": true' in line:
                print(line)
                return True, line
            else:
                pass
        return False, None


    # 升级准备
    def prepare_update(self, id):
        lines = self.getstr(f"adb shell adb shell cat /mnt/ota/data/log/dmclient.log")
        for line in lines:
            if "xl4.prepare-update" in line and f'"id": "{id}"' in line:
                log.info(line)
                return True, line
            else:
                pass
        return False, None

    # 准备就绪
    def install_ready(self, current_time):
        lines = self.getstr(f"adb shell adb shell cat /mnt/ota/data/log/dmclient.log")
        for line in lines:
            if "xl4.update-status" in line and 'INSTALL_READY' in line:
                logtime = self.get_time(line)
                if logtime > current_time:
                    print(line)
                    return True, line
                else:
                    pass
            else:
                pass
        return False, None

    # 升级提示弹框
    def time_window(self, id):
        lines = self.getstr(f"adb shell adb shell cat /mnt/ota/data/log/dmclient.log")
        for line in lines:
            if "xl4.time-window" in line and f'"id": "{id}"' in line:
                log.info(line)
                self.windowid = line.split('"reply-id": ')[1].split(' }')[0]
                return True, line
            else:
                pass
        return False, None

    # 预约完成
    def app_window(self):
        lines = self.getstr(f"adb shell adb shell cat /mnt/ota/data/log/dmclient.log")
        for line in lines:
            if "xl4.time-window" in line and f'"confirmed":false' in line and self.windowid in line:
                log.info(line)
                return True, line
            else:
                pass
        return False, None

    # 到达预约时间
    def gototime(self, id):
        lines = self.getstr(f"adb shell adb shell cat /mnt/ota/data/log/dmclient.log")
        for line in lines:
            if "xl4.time-window" in line and f'"id": "{id}"' in line and ' "confirmation": { "start-time":' in line:
                log.info(line)
                return True, line
            else:
                pass
        return False, None

    # 用户确认
    def start_install(self):
        lines = self.getstr(f"adb shell adb shell cat /mnt/ota/data/log/dmclient.log")
        for line in lines:
            if "xl4.time-window" in line and '"instant":true' in line:
                print(line)
                return True, line
            else:
                pass
        return False, None

    # 检查策略
    def policy_check(self, id):
        lines = self.getstr(f"adb shell adb shell cat /mnt/ota/data/log/dmclient.log")
        for line in lines:
            if "xl4.policy-check-query" in line and f'"id": "{id}"' in line:
                self.policy_key = line.split('"reference": "')[1].split('", "satisfied"')[0]
                return True, line
            else:
                pass
        return False, None

    # 策略结果
    def policy_result(self):
        lines = self.getstr(f"adb shell adb shell cat /mnt/ota/data/log/dmclient.log")
        for line in lines:
            if "xl4.policy-check-update" in line and self.policy_key in line:
                if '"satisfied": true' in line:
                    return True, line
                if '"satisfied": false' in line:
                    return False, line
            else:
                pass
        return False, None

    # 准备安装
    def ready_update(self, id):
        lines = self.getstr(f"adb shell adb shell cat /mnt/ota/data/log/dmclient.log")
        for line in lines:
            if "xl4.ready-update" in line and f'"id": "{id}"' in line:
                print(line)
                return True, line
            else:
                pass
        return False, None

    # 升级中
    def installing(self, current_time):
        lines = self.getstr(f"adb shell adb shell cat /mnt/ota/data/log/dmclient.log")
        for line in lines:
            if "xl4.update-status" in line and "INSTALL_IN_PROGRESS" in line:
                logtime = self.get_time(line)
                if logtime > current_time:
                    return True, line
                else:
                    pass
            else:
                pass
        return False, None

    def install_progress(self):
        a = []
        lines = self.getstr(f"adb shell adb shell cat /mnt/log/ota/dmclient.log")
        if lines is False:
            return False, "没有开始升级"
        else:
            for line in lines:
                if 'US_INSTALL' in line and 'xl4.update-report' in line:
                    a.append(line)
                else:
                    pass
            if a == []:
                return False, "没有开始升级"
            else:
                c = int(a[-1].split('"progress": ')[1].split(', "indeterminate"')[0])
                print(c)
                return True, c

    def install_result(self, current_time):
        lines = self.getstr(f"adb shell adb shell cat /mnt/sdcard/log/ota/dmclient.log")
        for line in lines:
            if "INSTALL_COMPLETED" in line:
                logtime = self.get_time(line)
                if logtime > current_time:
                    return True, line
                else:
                    pass
            elif "INSTALL_FAILED" in line:
                logtime = self.get_time(line)
                if logtime > current_time:
                    return False, line
                else:
                    pass
            else:
                pass
        return None, None

    # 任务结束
    def close_task(self, current_time):
        lines = self.getstr(f"adb shell adb shell cat /mnt/ota/data/log/dmclient.log")
        for line in lines:
            logtime = self.get_time(line)
            if "xl4.campaign-update" in line and '"event": "END"' in line:
                if logtime > current_time:
                    return True, line
                else:
                    pass
            else:
                pass
        return None, None



catlog = Check_dmlog()
if __name__ == '__main__':
    b = 1654745912
    # c = 16112
    print(catlog.download_progress(""))
    # import time
    # while True:
    #     catlog.install_progress("TBOX-B")
    #     time.sleep(1)
    # a = 1
    # if isinstance (a,int):
    #     print(1)
    # else:
    #     print(2)
    # print(a, type(a))