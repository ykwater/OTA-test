from Tools.PCANBasic import *
from Tools.logger import log
from Tools.times import sleep
import threading



class callpacn(object):
    def __init__(self):
        self.pcanfunction1 = PCANBasic()
        self.pcanfunction1.Initialize(PCAN_USBBUS1, PCAN_BAUD_500K)

    def sendmsg(self,msglist):
        msg = TPCANMsg()
        msg.ID = msglist[0]
        msg.LEN = 8
        msg.DATA[0] = msglist[1]
        msg.DATA[1] = msglist[2]
        msg.DATA[2] = msglist[3]
        msg.DATA[3] = msglist[4]
        msg.DATA[4] = msglist[5]
        msg.DATA[5] = msglist[6]
        msg.DATA[6] = msglist[7]
        msg.DATA[7] = msglist[8]
        status = self.pcanfunction1.Write(PCAN_USBBUS1, msg)
        if status == 0:
            pass
        else:
            log.error(f"ID为：{msg.ID}的{msglist[1:]}发送失败.")


    def readmesg(self):
        mesgdata = []
        masglist = []
        self.versionstr = ''
        m1 = [0x72B, 0x3, 0x22, 0xF1, 0x89, 0x0, 0x0, 0x0, 0x0]
        self.sendmsg(m1)
        while True:
            status, msg, timestamp = self.pcanfunction1.Read(PCAN_USBBUS1)
            if msg.ID == 0x7AB:
                i = msg.DATA
                mesgdata.append(i)
                if len(mesgdata) == 3:
                     break
                else:
                    pass
            else:
                pass
        self.unitialize()
        for i in range(8):
            if i > 4:
                masglist.append(hex(mesgdata[0][i]))
            else:
                pass
        for i in range(8):
            if i > 0:
                masglist.append(hex(mesgdata[1][i]))
            else:
                pass
        for i in range(8):
            if i > 0:
                masglist.append(hex(mesgdata[2][i]))
            else:
                pass
        for i in masglist:
             self.versionstr = self.versionstr + str(chr(int(i, 16)))
        return self.versionstr

    def we23(self):
        global timeout
        timeout = True
        while timeout:
            self.pcanfunction1.Initialize(PCAN_USBBUS1, PCAN_BAUD_500K)
            m2 = [0x72B, 0x30, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0]
            self.sendmsg(m2)
            sleep(0.1)

    def getacuversion(self):
        global timeout
        t2 = threading.Thread(target=self.we23)
        t2.start()
        sleep(1)
        acuversion = self.readmesg()
        timeout = False
        return acuversion

    def sendpolicy(self):
        self.pcanfunction1.Initialize(PCAN_USBBUS1, PCAN_BAUD_500K)
        m = [0x318, 0x00, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0]
        self.sendmsg(m)
        fun.unitialize()

    def unitialize(self):
        self.pcanfunction1.Uninitialize(PCAN_USBBUS1)


fun = callpacn()
if __name__ == '__main__':
    print(fun.getacuversion())
    fun.unitialize()
