import os
import yaml
from Tools.path import *


class Element(object):
    """获取元素"""

    def __init__(self):
        self.file_name = 'elment.yaml'
        self.element_path = os.path.join(CONFIG_PATH, self.file_name)
        if not os.path.exists(self.element_path):
            raise FileNotFoundError("%s 文件不存在！" % self.element_path)
        with open(self.element_path, encoding='utf-8') as f:
            self.data = yaml.safe_load(f)

    def __getitem__(self, item):
        """获取属性"""
        data = self.data.get(item)
        if data:
            name, value = data.split('==')
            return item, value
        raise ArithmeticError("{}中不存在关键字：{}".format(self.file_name, item))


elment = Element()

if __name__ == '__main__':
    A = elment['任务描述框']
    print(A)