# -*- coding:utf-8 -*-
import configparser
import os
from Tools.path import CONFIG_PATH



class ReadConfig(object):
    """配置文件"""

    def __init__(self):
        self.ini_file = os.path.join(CONFIG_PATH, "config.ini")
        self.config = configparser.RawConfigParser()  # 当有%的符号时请使用Raw读取
        self.config.read(self.ini_file, encoding='utf-8')

    def get(self, section, option):
        """获取"""
        return self.config.get(section, option)

    def set(self, section, option, value):
        """更新"""
        self.config.set(section, option, value)
        with open(self.ini_file, 'w') as f:
            self.config.write(f)

    def buttoncoordinate(self,  section, option):
        name = self.get(section, option)
        self.x_coordinate = int(name.split(' ')[0])
        self.y_coordinate = int(name.split(' ')[1])
        return self.x_coordinate, self.y_coordinate


ini = ReadConfig()

if __name__ == '__main__':
    print(ini.get("CAMPAIGN", "fmt"))