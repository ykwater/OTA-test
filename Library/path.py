import os
from times import strftime

# 项目目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 读取配置信息
BASEDATA_PATH = os.path.join(BASE_DIR, 'BaseDta')
# 配置信息
CONFIG_PATH = os.path.join(BASE_DIR, 'Config')
# 功能函数
LIBRARY_PATH = os.path.join(BASE_DIR, 'Library')
# LOG日志
LOG_PATH = os.path.join(BASE_DIR, 'LogFile')
# 图片目录
PICTURE_PATH = os.path.join(BASE_DIR, 'Picture')
# 基础图片库
BASEPICTURE_DIR = os.path.join(PICTURE_PATH, 'BasePicture')
# Logo图片
VOYAHLOGO_DIR = os.path.join(BASEPICTURE_DIR, 'VoyahLogo')
# 保存截图
SCREENSHOT_DIR = os.path.join(PICTURE_PATH, 'ScreenShot')
# 临时图片
SCREENTEMP_DIR = os.path.join(PICTURE_PATH, 'ScreenTemp')
# 临时目录
TEMP_PATH = os.path.join(BASE_DIR, 'Temp')
# 基本方法
TOOLS_PATH = os.path.join(BASE_DIR, 'Tools')
# 测试用例目录
TESTCASE_PATH = os.path.join(BASE_DIR, 'TestCase')
# 测试报告目录
TESTREPORT_PATH = os.path.join(BASE_DIR, 'Report')
# ECU软件目录
PACKAGE_PATH = os.path.join(BASE_DIR, 'Ecupackge')
# CAN工程目录
CAN_PATH = os.path.join(BASE_DIR, 'CAN')



class ConfigManager(object):

    def log_file(self):
        """
        创建log记录文件，如果文件的目录不存在就新建一个目录
        :return:
        """
        self.log_dir = LOG_PATH
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        return os.path.join(self.log_dir, '{}.log'.format(strftime(fmt="%Y%m%d%H%M")))

    def screen_path(self):
        """
        保存一个临时图片,如果目录不存在即新建这个目录
        :return:
        """
        if not os.path.exists(SCREENTEMP_DIR):
            os.makedirs(SCREENTEMP_DIR)
        now_time = strftime("%Y%m%d%H%M%S")
        screen_file = os.path.join(SCREENTEMP_DIR, "{}.png".format(now_time))
        return now_time, screen_file


cm = ConfigManager()

if __name__ == '__main__':
    print(CAN_PATH)
