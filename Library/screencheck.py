from Library.cmdaction import adbscreenshot, clickbutton
from Tools.imagerecognition import checkimage
from Tools.logger import log
from Tools.times import sleep


def checkupdatenoyify():
    """检查升级弹框是否弹出"""
    i = 0
    clickbutton((1062, 284), "系统升级")
    while adbscreenshot("updatenotify") is False and i < 120:
        i+=1
        sleep(1)
    if i == 120:
        return False
    else:
        pass
    if checkimage("updatenotify", "updatenotify_base"):
        log.info("升级提示框已经弹出")
        return True
    else:
        log.info("等待弹出升级提示框")
        return False

def checksafetytips():
    i = 0
    while adbscreenshot("safetytips") is False and i < 120:
        i+=1
        sleep(1)
    if i == 120:
        return False
    else:
        pass
    if checkimage("safetytips", "safetytips_base"):
        log.info("安全提示框已经弹出")
        return True
    else:
        log.info("等待弹出安全提示框")
        return False


def checkcountdown():
    i = 0
    while adbscreenshot("countdown") is False and i < 120:
        i += 1
        sleep(1)
    if i == 120:
        return False
    else:
        pass
    if checkimage("countdown", "countdown_base"):
        log.info("开始倒计时90秒")
        return True
    else:
        log.info("等待倒计时开始")
        return False


def checkpolicy():
    i = 0
    while adbscreenshot("policystatus") is False and i < 1200:
        i += 1
        sleep(1)
    if i == 1200:
        return False
    else:
        pass
    if checkimage("policystatus", "policyfail_base"):
        log.info("升级策略不通过")
        return True
    else:
        return False

def checkupdateing():
    """检查是否在升级中"""
    i = 0
    while adbscreenshot("updateing") is False and i < 1200:
        i+=1
        sleep(1)
    if i == 1200:
        return False
    else:
        pass
    if checkimage("updateing", "updateing_base"):
        log.info("正在升级中")
        return True
    else:
        return False


def checkupdateresult():
    """检查升级结果"""
    i = 0
    while adbscreenshot("updateresult") is False and i < 1200:
        i+=1
        sleep(1)
    if i == 1200:
        return False
    else:
        pass
    if checkimage("updateresult", "updatesuccessed_base"):
        log.info("弹出升级成果提示框")
        return True
    elif checkimage("updateresult", "updatefailed_base"):
        log.info("弹出升级失败提示框")
        return False
    else:
        pass


if __name__ == '__main__':
    checkupdatenoyify()