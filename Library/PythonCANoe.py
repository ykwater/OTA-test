# coding: utf-8
"""API for setup/usage of Canoe COM Client interface.
"""
# --------------------------------------------------------------------------
# Standard library imports
import os
import sys
import subprocess
import time
import msvcrt
from win32com.client import *
w = gencache.EnsureDispatch
from Tools.path import CAN_PATH
import pythoncom
from Tools.logger import log


# Vector Canoe Class
class CANoe(object):
    def appinitalize(self):
        try:
            pythoncom.CoInitialize()
            self.application = None
            self.application = Dispatch("CANoe.Application")
            ver = self.application.Version
            log.info(f'打开的CANoe版本为: {ver.major}.{ver.minor}.{ ver.Build}') #, sep,''
            self.Measurement = self.application.Measurement.Running
            log.info("CANoe 初始化成功")
        except Exception as error:
            log.error(f"{error}: CANoe 初始化失败")


    def open_cfg(self, cfgname=rf"{CAN_PATH}\AM8DEMO1.cfg"):
        # open CANoe simulation
        if (self.application != None):
            # check for valid file and it is *.cfg file
            if os.path.isfile(cfgname) and (os.path.splitext(cfgname)[1] == ".cfg"):
                self.application.Open(cfgname)

                log.info("导入CANoe工程: "+cfgname + "成功")
            else:
                log.error("导入CANoe工程失败")
                raise RuntimeError("导入CANoe工程失败")
        else:
            log.error("CANoe应用程序出错，无法打开模拟")
            raise RuntimeError("CANoe应用程序出错，无法打开模拟")


    def close_cfg(self):
        # close CANoe simulation
        if (self.application != None):
            log.info("关闭CANoe cfg成功")
            # self.stop_Measurement()
            self.application.Quit()
            self.application = None

    def start_Measurement(self):
        retry = 0
        retry_counter = 5
        # try to establish measurement within 5s timeout
        while not self.application.Measurement.Running and (retry < retry_counter):
            self.application.Measurement.Start()
            time.sleep(1)
            retry += 1
        log.info("CANoe start measuremet success")
        if (retry == retry_counter):
            log.error("CANoe start measuremet failed")
            raise RuntimeWarning("CANoe start measuremet failed, Please Check Connection!")

    def stop_Measurement(self):
        if self.application.Measurement.Running:

            self.application.Measurement.Stop()
            log.info("CANoe stop measuremet success")
        else:
            log.error("CANoe stop measuremet failed")

    def get_SigVal(self, channel_num, msg_name, sig_name, bus_type="CAN"):
        """
        @summary Get the value of a raw CAN signal on the CAN simulation bus
        @param channel_num - Integer value to indicate from which channel we will read the signal, usually start from 1,
                             Check with CANoe can channel setup.
        @param msg_name - String value that indicate the message name to which the signal belong. Check DBC setup.
        @param sig_name - String value of the signal to be read
        @param bus_type - String value of the bus type - e.g. "CAN", "LIN" and etc.
        @return The CAN signal value in floating point value.
                Even if the signal is of integer type, we will still return by
                floating point value.
        @exception None
        """
        if (self.application != None):
            result = self.application.GetBus(bus_type).GetSignal(channel_num, msg_name, sig_name)
            return result.RawValue
        else:
            raise RuntimeError("CANoe is not open,unable to GetVariable")

    def set_SigVal(self, channel_num, msg_name, sig_name, bus_type, setValue):
        if (self.application != None):
            result = self.application.GetBus(bus_type).GetSignal(channel_num, msg_name, sig_name)
            result.Value = setValue
            print(result.Value)
        else:
            raise RuntimeError("CANoe is not open,unable to GetVariable")

    def DoEvents(self):
        pythoncom.PumpWaitingMessages()
        time.sleep(1)

    def get_EnvVar(self, var):
        if (self.application != None):
            result = self.application.Environment.GetVariable(var)
            return result.Value
        else:
            raise RuntimeError("CANoe is not open,unable to GetVariable")

    def set_EnvVar(self, var, value):
        result = None
        if (self.application != None):
            # set the environment varible
            result = self.application.Environment.GetVariable(var)
            result.Value = value
            checker = self.get_EnvVar(var)
            # check the environment varible is set properly?
            while (checker != value):
                checker = self.get_EnvVar(var)
        else:
            raise RuntimeError("CANoe is not open,unable to SetVariable")

    def get_SysVar(self, ns_name, sysvar_name):
        if (self.application != None):
            systemCAN = self.application.System.Namespaces
            sys_namespace = systemCAN(ns_name)
            sys_value = sys_namespace.Variables(sysvar_name)
            return sys_value.Value
        else:
            raise RuntimeError("CANoe is not open,unable to GetVariable")

    def set_SysVar(self, ns_name, sysvar_name, var):
        if (self.application != None):
            systemCAN = self.application.System.Namespaces
            sys_namespace = systemCAN(ns_name)
            sys_value = sys_namespace.Variables(sysvar_name)
            sys_value.Value = var
        else:
            raise RuntimeError("CANoe is not open,unable to GetVariable")


    def callcapl(self):
        a = self.application.CAPL.GetFunction('func1')
        a.call()

app = CANoe() #定义CANoe为app

if __name__ == '__main__':
    app.appinitalize()
    app.open_cfg() #导入某个CANoe congif
    print("导入canoe工程成功")
    app.start_Measurement()
    print("运行canoe")
    # app.set_SigVal(channel_num=1, msg_name="BCM_BCAN_1", sig_name="BCM_KeySt", bus_type="CAN", setValue="1")
    # while not msvcrt.kbhit():
    # # while True:
    #     try:
    #         a = app.get_SigVal(channel_num=1, msg_name="TEL_Diag_Tx", sig_name="TEL_Diag_Response", bus_type="CAN")
    #         print(a)
    #     except:
    #         print("等待接受版本")
    #     if a != 0:
    #         print(hex(a)[2:3])
    time.sleep(5)
    app.stop_Measurement()
    app.close_cfg()
    print("结束运行caone")
    # time.sleep(1)
    # app.start_Measurement()
    # print("再次运行")
    # while not msvcrt.kbhit():
    #     a = app.get_SigVal(channel_num=1, msg_name=" IVI_control", sig_name="ivi_v2vChrgOptCurntSet", bus_type="CAN")
    # time.sleep(10)
    # app.stop_Measurement()
    # print("结束")
    # while not msvcrt.kbhit():
    # EngineSpeedDspMeter = app.get_SysVar("BCM_BCAN_1", "BCM_KeySt")
    # print(EngineSpeedDspMeter)
    #     # if(EngineSpeedDspMeter==2):
    #     #     app.set_SysVar("Engine","EngineSpeedDspMeter",3.0)
    #     app.DoEvents()