from Tools.cmder import *
from Tools.path import SCREENSHOT_DIR
from Tools.value import var
from Tools.times import *
from pykeyboard import PyKeyboard
import os


def adbscreenshot(screenname):
    """adb screen shot save picture"""
    adbscreen = f"{var.V_SHOTPATH}/{screenname}.png"
    process = subprocess.Popen(f'adb shell /system/bin/screencap -p {adbscreen}',
                               shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = process.communicate()
    retcode = process.poll()
    if retcode:
        log.error(f'{screenname} screenshot Failed!\n' + str(err)[2:-5])
        return False
    else:
        log.info(f'{screenname} screenshot Success')
    process = subprocess.Popen(fr'adb pull {adbscreen} {SCREENSHOT_DIR}',
                               shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = process.communicate()
    retcode = process.poll()
    if retcode:
        log.info(f'adb pull {screenname} screen FAILED!\n' + " " + str(err)[2:-5])
        return False
    else:
        log.info(f'adb pull {screenname} screen Success')
        return True


def clickbutton(coordinate, buttonname):
    """adb simulation click button"""
    x_coordinate, y_coordinate = coordinate
    if x_coordinate and y_coordinate:
        x_y_coordinate = str(x_coordinate) + " " + str(y_coordinate)
        if runcmd(f"adb shell input tap " + x_y_coordinate):
            log.info(f"Click {buttonname} Button success")
            return True
        else:
            log.error(f"Click {buttonname} Button FAILED")
            return False


def touchhome():
    """adb simulation touch home hardkey"""
    if runcmd(f"adb shell input keyevent 3"):
        log.info("Touch Home HardKey success")
        return True
    else:
        log.error("Touch Home HardKey FAILED")
        return False


def touchback():
    """adb simulation touch back hardkey"""
    if runcmd(f"adb shell input keyevent 4"):
        log.info("Touch Back HardKey success")
        return True
    else:
        log.error("Touch Back HardKey FAILED")
        return False


def swipscreen(coordinate1, coordinate2):
    x_coordinate1, y_coordinate1 = coordinate1
    x_coordinate2, y_coordinate2 = coordinate2
    x_y_coordinate = str(x_coordinate1) + " " + str(y_coordinate1) + " " + str(x_coordinate2) + " " + str(y_coordinate2)
    if runcmd(f"adb shell input swipe " + x_y_coordinate):
        log.info(f"swipe screen success")
        return True
    else:
        log.error(f"swip screen FAILED")
        return False

def inputstring(name):
    """adb simulation input string"""
    if runcmd(f"adb shell input keyboard text {name}"):
        log.info(f"adb input {name} success")
        return True
    else:
        log.error(f"adb input {name}  FAILED")
        return False

def adbInit():
    keyinput = PyKeyboard()
    os.system(r"cmd/c start")
    time.sleep(1)
    keyinput.type_string('adb root\n')
    time.sleep(2)
    keyinput.type_string('adb shell\n')
    time.sleep(2)
    keyinput.type_string('adb shell\n')
    time.sleep(5)
    keyinput.type_string('exit\n')
    time.sleep(0.5)
    keyinput.type_string('exit\n')
    time.sleep(0.5)
    keyinput.type_string('exit\n')
    if runcmd(f"adb shell adb shell ls"):
        return True
    else:
        return False

def gosetting():
    touchhome()
    sleep(1)
    clickbutton((55,466), "主菜单")
    sleep(1)
    clickbutton((550, 484), "设置")
    sleep(1)
    swipscreen((800, 57), (1, 57))
    sleep(2)
    clickbutton((717, 57), "系统设定")
    sleep(1)
    clickbutton((379, 359), "设置")





if __name__ == '__main__':
    # gosetting()
    clickbutton((829, 435), "确认失败")
    sleep(1)
    adbscreenshot("1234")
    # print(adbInit())
    # clickbutton(var.V_UPDATE, "立即升级")
    # clickbutton((1062, 284), "系统升级")
    # clickbutton(var.V_UPDATE, "立即升级")
    # clickbutton(var.V_UPDATE, "知道了")
