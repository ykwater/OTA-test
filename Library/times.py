import time
import datetime

def timestamp():
    """时间戳"""
    return time.time()


def strftime(fmt="%Y-%m-%d %H:%M:%S"):
    """
    datetime格式化时间
    :param fmt "%Y%m%d %H%M%S
    """
    return datetime.datetime.now().strftime(fmt)


def sleep(sconds):
    """
    睡眠时间
    """
    time.sleep(sconds)


def betime(a, b):
    """计时"""
    return f"{time.localtime(b-a).tm_hour}：{time.localtime(b-a).tm_min}: {time.localtime(b-a).tm_sec}"


if __name__ == '__main__':
    # print(strftime(fmt="%H%M"))
    # print(str(timestamp()).split(".")[0])
    timer = timestamp()
    while timestamp() - timer <= 10:
        print("a")
        sleep(2)