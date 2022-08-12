import win32gui
import win32con
import win32com.client


hwnd_map = {}

def get_all_hwnd(hwnd, mouse):
    if (win32gui.IsWindow(hwnd) and
            win32gui.IsWindowEnabled(hwnd) and
            win32gui.IsWindowVisible(hwnd)):
        hwnd_map.update({hwnd: win32gui.GetWindowText(hwnd)})


def callwindow(title):
    win32gui.EnumWindows(get_all_hwnd, 0)
    for h, t in hwnd_map.items():
        if t:
            if title in t:
                # h 为想要放到最前面的窗口句柄
                win32gui.BringWindowToTop(h)
                shell = win32com.client.Dispatch("WScript.Shell")
                shell.SendKeys('%')
                # 解决被最小化的情况
                # win32gui.ShowWindow(h, win32con.SW_RESTORE)
                # 被其他窗口遮挡，调用后放到最前面
                win32gui.SetForegroundWindow(h)

if __name__ == '__main__':
    callwindow(title="Vector CANoe")