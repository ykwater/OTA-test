import cv2
from Tools.logger import log
from Tools.path import SCREENSHOT_DIR, BASEPICTURE_DIR



def checkimage(screenname,screenname_base):
    """图片相似度对比"""
    # 读取图片
    img_src = cv2.imread(fr'{SCREENSHOT_DIR}\{screenname}.png')
    # 读取置灰的图片
    template = cv2.imread(fr'{BASEPICTURE_DIR}\{screenname_base}.png', 0)
    # 获取base图片的高宽属性
    w, h = template.shape[::-1]
    # 图像置灰
    img_gray = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)
    # 滑动匹配
    result = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    # 获取匹配的最大值最小值和起始位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    log.info('The similarity between the current picture and the template picture is ：{:.2%}'.format(max_val))
    if max_val >= 0.9:
        # 左上角
        left_top = max_loc
        # 右下角
        right_bottom = (left_top[0] + w, left_top[1] + h)
        # 原图上作画 参数为 源图 左上角 右下角 框的颜色 框的粗细
        cv2.rectangle(img_src, left_top, right_bottom, (0, 0, 225), 2, 8, 0)
        if True:
            # 保存重新重新作画的图片
            cv2.imwrite(fr'{SCREENSHOT_DIR}\{screenname}.png', img_src)
            # 直接显示画完的图片
            # cv2.imshow("res", img_src)
            # cv2.waitKey(1000) & 0xFF
            # # cv2.waitKey(0) & 0xFF
            # cv2.destroyAllWindows()
        return True
    else:
        return False


if __name__ == '__main__':
    if checkimage("updatenotify", 'updatenotify_base'):
        print("升级成功的图片已经弹出")
    else:
        print("等待升级完成中........")
