import serial
from modbus_tk import modbus_rtu
import modbus_tk
import modbus_tk.defines as cst


# 进制转化实现
class Binary:
    """
        自定义进制转化
    """
    @staticmethod
    def Hex2Dex(e_hex):
        """
        十六进制转换十进制
        :param e_hex:
        :return:
        """
        return int(e_hex, 16)

    @staticmethod
    def Hex2Bin(e_hex):
        """
        十六进制转换二进制
        :param e_hex:
        :return:
        """
        return bin(int(e_hex, 16))

    @staticmethod
    def Dex2Bin(e_dex):
        """
        十进制转换二进制
        :param e_dex:
        :return:
        """
        return bin(e_dex)

# 校验方法实现
class CRC(object):
    """
     CRC验证
    """
    def __init__(self):
        self.Binary = Binary()

    def CRC16(self, hex_num="02 10 00 0A 00 03 06 0e ee 00 00 00 00"):
        """
        CRC16校验
        """
        crc = '0xffff'
        crc16 = '0xA001'
        # test = '01 06 00 00 00 00'
        test = hex_num.split(' ')
        crc = self.Binary.Hex2Dex(crc)  # 十进制
        crc16 = self.Binary.Hex2Dex(crc16)  # 十进制
        for i in test:
            temp = '0x' + i
            # 亦或前十进制准备
            temp = self.Binary.Hex2Dex(temp)  # 十进制
            # 亦或
            crc ^= temp  # 十进制
            for i in range(8):
                if self.Binary.Dex2Bin(crc)[-1] == '0':
                    crc >>= 1
                elif self.Binary.Dex2Bin(crc)[-1] == '1':
                    crc >>= 1
                    crc ^= crc16
                # print('crc_D:{}\ncrc_B:{}'.format(crc, self.Binary.Dex2Bin(crc)))
        crc = hex(crc)
        crc_H = crc[2:4]  # 高位
        crc_L = crc[-2:]  # 低位
        return crc, crc_H, crc_L


def power_contor(s,ecu, ports="COM7"):
    if s == "disconnect":
        c = "0"
    else:
        c = "e"
    a = f"0{c}"
    b = f"{c}{c}"
    if ecu == "TBOX":
        bytestr = f"02 10 00 0A 00 03 06 {a} ee 00 00 00 00"
    elif ecu == "IVI":
        bytestr = f"02 10 00 0A 00 03 06 ee {b} 00 00 00 00"
    else:
        bytestr = f"02 10 00 0A 00 03 06 {a} {b} 00 00 00 00"
    crc, crc_H, crc_L = CRC.CRC16(bytestr)
    byte = bytestr + ' ' + crc_L + ' ' + crc_H
    sendbytes = bytes.fromhex(byte)
    com = (serial.Serial(port=ports, baudrate=19200, bytesize=8, parity="N", stopbits=1))
    if com.is_open:  # 检测端口
        # 发送报文
        com.write(sendbytes)
        return True
    else:
        return False

CRC = CRC()
if __name__ == '__main__':
    power_contor(s="connect",ecu="ALL")




