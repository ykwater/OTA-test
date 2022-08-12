from warnings import simplefilter
simplefilter(action='ignore', category=FutureWarning)
import visa
from Tools.logger import log
from Tools.times import sleep, strftime
from MainScreen.autotestscreen import mainscreen



class Multimeter:
    def __init__(self, usb='USB0::0x0952::0x8201::0152802227000001::RAW'):
        rm = visa.ResourceManager()
        self.ser = rm.open_resource(usb)

    def powerInitial(self):
        try:
            self.Write("SBEEP 1")
            log.info("电源初始化成功")
        except:
            log.error("电源初始化失败")

    def Write(self, data):
        self.ser.write(data)

    def set_maxvol(self, data=20):
        self.Write("SETT:VOLT:MAX" + str(data))
        log.info(f"设置最大电压为：{data}")
        mainscreen.InsertText(f"{strftime()} 设置最大电压为：{data}")

    def set_maxcurr(self, data=10):
        self.Write("SETT:CURR:MAX " + str(data))
        log.info(f"设置最大电流为：{data}")
        mainscreen.InsertText(f"{strftime()} 设置最大电流为：{data}")

    def set_vol(self, data=13):
        self.Write("VOLT " + str(data))
        log.info(f"设置当前电压为：{data}")
        mainscreen.InsertText(f"{strftime()} 设置当前电压为：{data}")

    def set_curr(self, data=5):
        self.Write("CURR " + str(data))
        log.info(f"设置当前电流为：{data}")
        mainscreen.InsertText(f"{strftime()} 设置当前电流为：{data}")

    def power_off(self):
        self.Write("OUTP 0")
        log.info(f"关闭电源开关")
        mainscreen.InsertText(f"{strftime()} 关闭电源开关")

    def power_on(self):
        self.Write("OUTP 1")
        log.info(f"打开电源开关")
        mainscreen.InsertText(f"{strftime()} 打开电源开关")

    def contor_off(self):
        self.powerInitial()
        sleep(1)
        self.power_off()

    def contor_on(self):
        self.powerInitial()
        sleep(1)
        self.set_maxvol()
        sleep(1)
        self.set_maxcurr()
        sleep(1)
        self.set_vol()
        sleep(1)
        self.set_curr()
        sleep(1)
        self.power_on()

powercontor = Multimeter()
if __name__ == '__main__':
    powercontor.contor_on()
    # powercontor.contor_off()
