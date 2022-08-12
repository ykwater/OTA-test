from MainScreen.autotestscreen import mainscreen
from Library.cmdaction import *
from Library.screencheck import *
import serial.tools.list_ports
from Tools.powerIO import power_contor

# def Car_powercontrol(value1,value2):
#     port = None
#     ports = list(serial.tools.list_ports.comports())
#     for port_no, description, address in ports:
#         if 'USB' in description:
#             port = port_no
#             break
#     if port is None:
#         log.error("任务结束，没有链接电源控制板卡，请连接")
#         mainscreen.InsertText(f"{strftime()} 任务结束，没有链接电源控制板卡，请连接")
#         return False
#     power = RelayControl(port, 19200)
#     power.connect()
#     if value1 == "connect":
#         if str(value2).isdigit():
#             status = power.connectSingle(value2)
#         else:
#             status = power.connectAll()
#         if status:
#             mainscreen.InsertText(f"{strftime()} {str(value2)}号开关已连接")
#             return True
#         else:
#             mainscreen.InsertText(f"{strftime()} {str(value2)}号开关连接失败")
#             return False
#     elif value1 == "disconnect":
#         if str(value2).isdigit():
#             status = power.disConnectSingle(value2)
#         else:
#             status = power.disConnectAll()
#         if status:
#             mainscreen.InsertText(f"{strftime()} {str(value2)}号开关已连接")
#             return True
#         else:
#             mainscreen.InsertText(f"{strftime()} {str(value2)}号开关连接失败")
#             return False

def Car_powercontrol(value1,value2):
    port = None
    ports = list(serial.tools.list_ports.comports())
    for port_no, description, address in ports:
        if 'USB' in description:
            port = port_no
            break
    if port is None:
        log.error("任务结束，没有链接电源控制板卡，请连接")
        mainscreen.InsertText(f"{strftime()} 任务结束，没有链接电源控制板卡，请连接")
        return False
    status = power_contor(s=value1, ecu=value2, ports=port)
    if status is True:
        log.info(f"{value2}成功{value1}")
        mainscreen.InsertText(f"{strftime()} {value2}成功{value1}")
        return True
    else:
        log.error(f"{value2} {value1}失败")
        mainscreen.InsertText(f"{strftime()} {value2} {value1}失败")
        return False



def Car_reboottbox():
    status = runcmd(f"adb shell adb reboot")
    log.info("重启TBOX")
    mainscreen.InsertText(f"{strftime()} 重启TBOX")
    if status:
        sleep(10)
        for i in range(10):
            status = runcmd(f"adb shell adb shell ls")
            if status:
                log.info("重启TBOX成功")
                mainscreen.InsertText(f"{strftime()} 重启TBOX成功")
                return True
            else:
                sleep(1)
        log.info("重启TBOX失败")
        mainscreen.InsertText(f"{strftime()} 重启TBOX失败")
        return False


def Car_check_updatenotify():
    """检查升级通知"""
    timer = timestamp()
    gosetting()
    mainscreen.InsertText(f"{strftime()} 进入系统设置画面，等待弹出升级通知")
    while timestamp() - timer <= 2400:
        if checkupdatenoyify():
            sleep(1)
            mainscreen.sertPicture("updatenotify")
            mainscreen.InsertText(f"{strftime()} 弹出升级通知")
            return True
        else:
            mainscreen.sertPicture("updatenotify")
            log.info("任务进行中，等待弹出升级通知")
        timer += 1
        sleep(2)
    return False

def Car_clickbutton(value1):
    if value1 == "立即升级":
        value = var.V_UPDATE
    elif value1 == "知道了":
        value = var.V_CONFIRMTIME
    else:
        value = var.V_UPDATECOMPLETED
    status = clickbutton(value, value1)
    if status:
        mainscreen.InsertText(f"{strftime()} 点击{value1}按钮成功")
        return True
    else:
        mainscreen.InsertText(f"{strftime()} 点击{value1}按钮失败")
        return False


def Car_reteyupdate():
    clickbutton(var.V_RETRY, "重试")
    mainscreen.InsertText(f"{strftime()} 点击重试按钮成功")
    # sleep(1)
    # clickbutton((1062, 284), "系统升级")
    # mainscreen.InsertText(f"{strftime()} 点击系统升级按钮成功")
    # sleep(1)
    # clickbutton(var.V_UPDATE, "立即升级")
    # mainscreen.InsertText(f"{strftime()} 点击立即升级按钮成功")
    # sleep(1)
    # clickbutton(var.V_UPDATE, "知道了")
    # mainscreen.InsertText(f"{strftime()} 点击知道了按钮成功")
    sleep(1)
    return True

def Car_check_safetytips():
    timer = timestamp()
    mainscreen.InsertText(f"{strftime()} 进入系统设置画面，等待弹出升级通知")
    while timestamp() - timer <= 2400:
        if checksafetytips():
            sleep(1)
            mainscreen.sertPicture("safetytips")
            mainscreen.InsertText(f"{strftime()} 弹出安全提示")
            return True
        else:
            mainscreen.sertPicture("safetytips")
            mainscreen.InsertText(f"{strftime()} 等待安全提示")
        timer += 1
        sleep(2)
    return False

def Car_check_countdown():
    """判断倒计时"""
    global satrtstatus
    timer = timestamp()
    while timestamp() - timer <= 180:
        if checkcountdown():
            satrtstatus = False
            sleep(1)
            mainscreen.sertPicture("countdown")
            mainscreen.InsertText(f"{strftime()} 开始倒计时90秒")
            return True
        else:
            mainscreen.sertPicture("countdown")
            mainscreen.InsertText(f"{strftime()} 等待倒计时")
        timer += 1
        sleep(1)
    satrtstatus = False
    return False

def Car_check_policy():
    for i in range(300):
        result = checkpolicy()
        if result is True:
            mainscreen.sertPicture("policystatus")
            mainscreen.InsertText(f"{strftime()} 升级中")
            return True
        else:
            mainscreen.sertPicture("policystatus")
        sleep(0.2)
    return False

def Car_check_updateing():
    for i in range(300):
        result = checkupdateing()
        if result is True:
            mainscreen.sertPicture("updateing")
            mainscreen.InsertText(f"{strftime()} 升级中")
            return True
        else:
            mainscreen.sertPicture("updateing")
        sleep(0.2)
    return False

def Car_check_updateresult():
    clickbutton((1, 1), "点亮屏幕")
    mainscreen.InsertText(f"{strftime()} 点亮屏幕")
    timer = timestamp()
    while timestamp()-timer <= 2400:
        result = checkupdateresult()
        if result is True:
            mainscreen.sertPicture("updateresult")
            log.info(f"弹出升级完成弹窗")
            clickbutton(var.V_UPDATECOMPLETED, "确认成功")
            mainscreen.InsertText(f"{strftime()} 点击确认成功按钮")
            return True
        elif result is False:
            log.info("升级失败")
            mainscreen.sertPicture("updateresult")
            mainscreen.InsertText(f"{strftime()} 升级失败")
            clickbutton((829,435), "确认失败")
            mainscreen.InsertText(f"{strftime()} 点击确认失败按钮")
            return False
        else:
            mainscreen.sertPicture("updateresult")
            log.info("升级中，等待升级结果")
        sleep(1)
    log.error("The Upgrade timeout")
    mainscreen.InsertText(f"{strftime()} Upgrade timeout")
    return False

def Car_sleep(value1):
    log.info(f"等待{value1}S")
    mainscreen.InsertText(f"{strftime()} 等待{value1}S")
    sleep(value1)
    return True

if __name__ == '__main__':
    Car_powercontrol("connect", "TBOX")
    # Car_reteyupdate()
    # clickbutton((829, 435), "确认失败")