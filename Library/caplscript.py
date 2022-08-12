from Tools.path import CAN_PATH
from Library.PythonCANoe import app
from MainScreen.autotestscreen import mainscreen
from Tools.times import *
import math
from Tools.logger import log
import pyautogui as pg
from Library.calltoolswindow import callwindow
import pythoncom


def sendpolicy_start(IGstatus=0,lockstatus=0,socvol=11):

    socvol = float(socvol*10)
    policytxt = """
variables
{
  mstimer cycle;
  message BCM_BCAN_1 vestatus;
  message ICM_3_B volvalue;
}

on timer cycle
{
  setTimer(cycle, 100);
  output(vestatus);
  output(volvalue);
}

on start
{
    """
    policytxth = f"""
 setTimer(cycle, 100);
  vestatus.BCM_KeySt = {IGstatus};
  vestatus.BCM_ATWS_St = {lockstatus};
  volvalue.ICM_BattVolt = {socvol};
    """
    policyscriot = policytxt + policytxth + "}"
    scriptpath = rf"{CAN_PATH}\demode.can"
    f = open(scriptpath, 'w', encoding="utf-8")
    f.write(policyscriot)
    # 关闭文件
    f.close()
    try:
        app.appinitalize()
        app.open_cfg() #导入某个CANoe congif
        mainscreen.InsertText(f"{strftime()} 导入工程")
        app.start_Measurement()
        mainscreen.InsertText(f"{strftime()} 开始发送升级策略报文")
        return True
    except:
        mainscreen.InsertText(f"{strftime()} 升级策略报文发送失败")
        return False


def getversion(ECU):
    if ECU == "ACU":
        messageid = "0x72B"
    if ECU == "TBOX":
        messageid = "0x72D"
        ECU = "TEL"
    else:
        messageid = None
    varables = """
variables
{
    """
    idvalues = f"""
    mstimer cycle;
    timer sleeptime;
    message {messageid} ECU_FunRx;
    message {messageid} ECU_Flow;
    """

    caplstr = """

}

on timer cycle
{
  setTimer(cycle, 100);
    output(ECU_Flow);
}

on timer sleeptime
{
   output(ECU_FunRx);
}

on start
{
  setTimer(cycle, 100);
  setTimer(sleeptime, 2);
  ECU_FunRx.dlc = 8;
  ECU_FunRx.byte(0) = 0x03;
  ECU_FunRx.byte(1) = 0x22;
  ECU_FunRx.byte(2) = 0xF1;
  ECU_FunRx.byte(3) = 0x89;
  ECU_Flow.dlc = 8;
  ECU_Flow.byte(0) = 0x30;
 }
    """
    checkversionscript = varables + idvalues + caplstr
    scriptpath = rf"{CAN_PATH}\readversion.can"
    f = open(scriptpath, 'w', encoding="utf-8")
    f.write(checkversionscript)
    # 关闭文件
    f.close()
    app.appinitalize()
    mainscreen.InsertText(f"{strftime()} 打开CANoe程序")
    app.open_cfg(cfgname=rf"{CAN_PATH}\checkversion.cfg")  # 导入某个CANoe 工程
    mainscreen.InsertText(f"{strftime()} 导入查询{ECU}版本工程")
    app.start_Measurement()
    mainscreen.InsertText(f"{strftime()} 开始查询{ECU}版本")
    list_message = []
    while True:
        responseversion = app.get_SigVal(channel_num=1, msg_name=f"{ECU}_Diag_Tx", sig_name=f"{ECU}_Diag_Response",
                                         bus_type="CAN")
        if responseversion != 0:
            if hex(responseversion)[:4] == "0x10":
                d = math.ceil((int(hex(responseversion)[4:6]) + 1) / 7)
            list_message.append(hex(responseversion))
            list_message = list(set(list_message))
            if len(list_message) == d:
                break
    list_message = sorted(list_message, reverse=False)
    bvsersion = ''
    for i in list_message:
        if "0x10" in i:
            i = i[12:]
        else:
            i = i[4:]
        bvsersion = bvsersion + i
    ecuversion = ""
    for i in range(0, 34, 2):
        ecuversion = ecuversion + str(chr(int(bvsersion[i:i + 2], 16)))
    app.stop_Measurement()
    callwindow(title="Vector CANoe")
    sleep(3)
    pg.keyDown("ctrl")
    pg.press("s")
    pg.keyUp("ctrl")
    sleep(1)
    callwindow(title="OTA自动化")
    mainscreen.InsertText(f"{strftime()} 保存工程成功")
    return ecuversion


def sendpolicy_stop():
    app.stop_Measurement()
    pythoncom.CoInitialize()
    try:
        callwindow(title="Vector CANoe")
        sleep(3)
        pg.keyDown("ctrl")
        pg.press("s")
        pg.keyUp("ctrl")
        sleep(1)
        callwindow(title="OTA自动化")
        mainscreen.InsertText(f"{strftime()} 保存工程成功")
        return True
    except:
        log.error("保存CANoe工程失败")
        mainscreen.InsertText(f"{strftime()} 保存CANoe工程失败")
        return False


if __name__ == '__main__':
    sendpolicy_stop()
