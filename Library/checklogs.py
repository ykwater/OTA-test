from Library.analysislog import catlog
from Tools.times import *
from Tools.logger import log
from MainScreen.autotestscreen import mainscreen



def Log_checksynccampaign(campaignid):
    timer = timestamp()
    log.info(f"等待任务同步...")
    mainscreen.InsertText(f"{strftime()} 等待任务同步...")
    while timestamp() - timer <= 1200:
        status = catlog.handle_campaign(campaignid)
        if status[0]:
            log.info(f"任务: {campaignid}已经同步")
            mainscreen.InsertText(f"{strftime()} 任务: {campaignid}已经同步")
            return True
        else:
            pass
            sleep(0.2)
    return False

def Log_recheckividownload(value1,campaignid):
    value1 = "{:.0%}".format(value1)
    timer = timestamp()
    log.info(f"等待断点继续下载...")
    mainscreen.InsertText(f"{strftime()} 等待断点继续下载...")
    while timestamp() - timer <= 1200:
        download_progress = catlog.ivi_download_progress(campaignid)
        if download_progress[0]:
            if int(download_progress[1][0:-1]) > int(value1[0:-1]) - 10:
                sleep(1)
                download = catlog.ivi_download_progress(campaignid)
                if int(download[1][0:-1]) > int(download_progress[1][0:-1]):
                    log.info(f"再次检查下载进度为: {download[1]}")
                    mainscreen.InsertText(f"{strftime()} 再次检查下载进度为：{download[1]}")
                    return True
            else:
                pass
        else:
            pass
            sleep(1)
    return False

def Log_recheckdownload(value1,campaignid):
    value1 = "{:.0%}".format(value1)
    timer = timestamp()
    log.info(f"等待断点继续下载...")
    mainscreen.InsertText(f"{strftime()} 等待断点继续下载...")
    while timestamp() - timer <= 1200:
        download_progress = catlog.download_progress(campaignid)
        if download_progress[0]:
            if int(download_progress[1][0:-1]) > int(value1[0:-1]) - 10:
                sleep(1)
                download = catlog.download_progress(campaignid)
                if int(download[1][0:-1]) > int(download_progress[1][0:-1]):
                    log.info(f"再次检查下载进度为: {download[1]}")
                    mainscreen.InsertText(f"{strftime()} 再次检查下载进度为：{download[1]}")
                    return True
            else:
                pass
        else:
            pass
            sleep(1)
    return False

def Log_checkividownload(value1,campaignid):
    """判断下载进度"""
    value1 = "{:.0%}".format(value1)
    timer = timestamp()
    log.info(f"等待下载版本中...")
    mainscreen.InsertText(f"{strftime()} 等待下载...")
    while timestamp() - timer <= 3600:
        download_progress = catlog.ivi_download_progress(campaignid)
        if download_progress[0]:
            if int(download_progress[1][0:-1]) > int(value1[0:-1])-10  and \
                    int(download_progress[1][0:-1]) < int(value1[0:-1])+10:
                log.info(f"当前下载进度为: {download_progress[1]}")
                mainscreen.InsertText(f"{strftime()} 当前下载进度为：{download_progress[1]}")
                return True
            else:
                log.info(f"当前下载进度为: {download_progress[1]}")
                mainscreen.InsertText(f"{strftime()} 当前下载进度为：{download_progress[1]}")
        else:
            pass
            sleep(1)
    return False


def Log_checkdownload(value1,campaignid):
    """判断下载进度"""
    value1 = "{:.0%}".format(value1)
    timer = timestamp()
    log.info(f"等待下载版本中...")
    mainscreen.InsertText(f"{strftime()} 等待下载...")
    while timestamp() - timer <= 3600:
        download_progress = catlog.download_progress(campaignid)
        if download_progress[0]:
            print(download_progress[1])
            if int(download_progress[1][0:-1]) > int(value1[0:-1])-10:
                log.info(f"当前下载进度为: {download_progress[1]}")
                mainscreen.InsertText(f"{strftime()} 当前下载进度为：{download_progress[1]}")
                return True
        else:
            pass
            sleep(0.2)
    return False

def Log_checkinstall(value1,campaignid):
    value1 = "{:.0%}".format(value1)
    timer = timestamp()
    log.info(f"升级中...")
    mainscreen.InsertText(f"{strftime()} 升级中...")
    while timestamp() - timer <= 2400:
        install_progress =catlog.install_progress()
        if install_progress[0]:
            if int(install_progress[1][0:-1]) > int(value1[0:-1]) - 10:
                log.info(f"当前升级进度为: {install_progress[1]}")
                mainscreen.InsertText(f"{strftime()} 当前升级进度为：{install_progress[1]}")
            return True
        else:
            pass
            sleep(0.2)
    return False

if __name__ == '__main__':
    print(Log_checkdownload(1,""))
