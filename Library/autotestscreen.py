from PIL import Image as IM
from Tools.path import VOYAHLOGO_DIR, SCREENSHOT_DIR
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import sys
from tkinter import filedialog
import os


WIN = sys.platform.startswith('win')


def selectPath(path):
    path_ = filedialog.askopenfilename() #使用askdirectory()方法返回文件夹的路径
    if path_ == "":
        path.get()  # 当打开文件路径选择框后点击"取消" 输入框会清空路径，所以使用get()方法再获取一次路径
    else:
        path_ = path_.replace("/", "\\")  # 实际在代码中执行的路径为“\“ 所以替换一下
        path.set(path_)


def openPath(path):
    dir = os.path.dirname(os.path.dirname(os.path.abspath(path.get())+"\\"))
    print(dir)
    os.system('start ' + dir)
    #print(dir)


class MainScreen(object):
    def __init__(self):
        """创建一个操作界面，用于用户交互"""
        # 创建一个TK控件并且实例化
        self.windows = tk.Tk()
        self.windows.title("爱瑟福OTA自动化测试")
        # 设置操作界面的尺寸和在显示屏中的位置
        self.windows.geometry("1200x600+250+100")
        # 设置Logo图片
        self.windows.iconphoto(False, tk.PhotoImage(file=f'{VOYAHLOGO_DIR}\EX.png'))
        self.windows.resizable(False, False)
        # 创建一个垂直滚动条
        scroll = tk.Scrollbar(bd=2)
        # 创建一个文本显示框
        self.log_text = Text(self.windows, width=65, height=38, relief=SOLID)
        # 固定滚动条的位置靠右，垂直滚动条
        scroll.pack(side=RIGHT, fill=Y)
        # 设置文本框的尺寸
        self.log_text.place(x=700, y=60)
        # 滚动条与文本框关联
        scroll.config(command=self.log_text.yview)
        self.log_text.config(yscrollcommand=scroll.set)

        # 创建一个图片显示区域
        self.image = IM.open(fr'{VOYAHLOGO_DIR}\logo.png')
        base_width = 600
        w_percent = base_width / float(self.image.size[0])
        h_size = int(float(self.image.size[1]) * float(w_percent))
        self.image1 = self.image.resize((base_width, h_size), IM.ANTIALIAS)
        self.image1.save(f'{VOYAHLOGO_DIR}\logo.png')
        self.bm = PhotoImage(file=f'{VOYAHLOGO_DIR}\logo.png')
        self.w = tk.Label(self.windows, image=self.bm)
        self.w.bm = self.bm
        self.w.place(x=40, y=60)

        # 文件选择
        path = StringVar()
        # 默认路径
        # path.set(os.path.abspath("."))
        self.entry = Entry(self.windows, textvariable=path, font=('宋体', 12), width=55)
        self.entry.place(x=40, y=322)  # , state="readonly" # .grid(row=0, column=1, ipadx=200)
        Button(self.windows, text="路径选择", width=10, command=lambda: selectPath(path=path)).place(x=490,
                                                                                                 y=322)  # .grid(row=0, column=2)
        Button(self.windows, text="打开文件位置", command=lambda: openPath(path=path)).place(x=570,
                                                                                       y=322)  # .grid(row=0, column=3)
        Label(self.windows, text="Sheet名").place(x=40, y=350)

        self.entry1 = Entry(self.windows, font=('宋体', 12),
                            width=55)  # , state="readonly") # .grid(row=0, column=1, ipadx=200)
        self.entry1.place(x=40, y=372)

        # 成功次数显示
        self.E2 = Entry(self.windows, relief=SOLID, width=8, state="disabled")
        self.E2.configure(state="normal")
        self.E2.delete(0, "end")
        self.E2.insert('insert', "0")
        self.E2.configure(state="disabled")
        self.E2.place(x=40, y=542)

        # 失败次数显示
        self.E3 = Entry(self.windows, relief=SOLID, width=8, state="disabled")
        self.E3.configure(state="normal")
        self.E3.delete(0, "end")
        self.E3.insert('insert', "0")
        self.E3.configure(state="disabled")
        self.E3.place(x=280, y=542)
        # # 成功率显示
        self.E4 = Entry(self.windows, relief=SOLID, width=8, state="disabled")
        self.E4.configure(state="normal")
        self.E4.delete(0, "end")
        self.E4.insert('insert', "0")
        self.E4.configure(state="disabled")
        self.E4.place(x=160, y=542)
        # 统计总数显示
        self.E5 = Entry(self.windows, relief=SOLID, width=8, state="disabled")
        self.E5.configure(state="normal")
        self.E5.delete(0, "end")
        self.E5.insert('insert', "0")
        self.E5.configure(state="disabled")
        self.E5.place(x=400, y=542)
        #
        # 任务ID显示
        self.E7 = Entry(self.windows, relief=SOLID, width=63, state="disabled")
        self.E7.configure(state="normal")
        self.E7.delete(0, "end")
        self.E7.insert('insert', "None")
        self.E7.configure(state="disabled")
        self.E7.place(x=40, y=482)

        # 用例标题
        self.E8 = Entry(self.windows, relief=SOLID, width=63, state="disabled")
        self.E8.configure(state="normal")
        self.E8.delete(0, "end")
        self.E8.insert('insert', "None")
        self.E8.configure(state="disabled")
        self.E8.place(x=40, y=422)



    def LabelText(self,textsize={"x": 40, "y": 30},labtext="车机图片显示", fontsize=10, h=None, w=None, b=None):
        """显示车机图片的标签"""
        w = tk.Label(self.windows, font=('Arial', fontsize),  height=h, width=w, bg=b)
        w.config(text=labtext)
        w.place(textsize)

    def ScreenButton(self, button_position={"x": 540, "y": 400}, button_param={"width": 7, "height": 1, "text": "开始",
                                                                              "bg": "green", "command": None}):
        """
        生成按钮方法
        :param button_position: 按钮在主屏幕中的位置，示例：{"x": 40, "y": 80}
        :param button_parameter: 按钮相关的参数，示例：{"width": 25, "height": 3,"text": "开始", "command": None}
        """
        BT = tk.Button(self.windows, button_param)
        BT.place(button_position)

    def hit_me(self):
        """警告提示框"""
        messagebox.showinfo(title='提示', message='请输入升级ECU或升级测试')

    def sertPicture(self, filename='VOYAH'):
        """插入车机片方法函数"""
        image = IM.open(fr'{SCREENSHOT_DIR}\{filename}.png')
        # 调整图片大小，并保持比例不变
        # 给定一个基本宽度
        base_width = 400
        # 基本宽度与原图宽度的比例
        w_percent = base_width / float(image.size[0])
        h_size = int(float(image.size[1]) * float(w_percent))
        image1 = image.resize((base_width, h_size), IM.ANTIALIAS)
        image1.save(fr'{SCREENSHOT_DIR}\{filename}.png')
        bm2 = PhotoImage(file=fr'{SCREENSHOT_DIR}\{filename}.png')
        self.w.configure(image=bm2)
        self.w.bm = bm2
        self.w.place(x=50, y=60)
        self.w.update()

    def InsertText(self, str):
        """实时显示Log日志"""
        self.log_text.insert('insert', str + '\n')
        self.log_text.see(END)
        self.log_text.update()

    def gettestcasepath(self):
        """获取需要升级的ECU名"""
        self.testcasepath = self.entry.get()
        if self.testcasepath == "":
            messagebox.showinfo(title='提示', message='请输入测试用例路径')
        else:
            return self.testcasepath

    def getsheetname(self):
        """获取升级的次数"""
        self.sheetname = self.entry1.get()
        if self.sheetname == "":
            messagebox.showinfo(title='提示', message='请输入需要测试的sheet名')
        else:
            return self.sheetname

    def showsuccess(self, str):
        """显示升级成功次数"""
        self.E2.configure(state="normal")
        self.E2.delete(0, "end")
        self.E2.insert("insert", str)
        self.E2.configure(state="disabled")
        self.E2.update()

    def showfail(self, str):
        """显示升级失败次数"""
        self.E3.configure(state="normal")
        self.E3.delete(0, "end")
        self.E3.insert("insert", str)
        self.E3.configure(state="disabled")
        self.E3.update()

    def showrate(self, strs, strf):
        """显示升级成功率"""
        intT = int(strs) + int(strf)
        successrate = int(strs) / intT * 100
        strsu = (str(successrate)).split(".")[0] + "%"
        self.E4.configure(state="normal")
        self.E4.delete(0, "end")
        self.E4.insert("insert", strsu)
        self.E4.configure(state="disabled")
        self.E4.update()

    def showtotal(self, strs, strf):
        """显示完成升级的总数"""
        strT = str(int(strs) + int(strf))
        self.E5.configure(state="normal")
        self.E5.delete(0, "end")
        self.E5.insert("insert", strT)
        self.E5.configure(state="disabled")
        self.E5.update()

    def showID(self,str):
        """显示任务ID"""
        self.E7.configure(state="normal")
        self.E7.delete(0, "end")
        self.E7.insert("insert", str)
        self.E7.configure(state="disabled")
        self.E7.update()

    def showcasetitle(self, str):
        """用例标题"""
        self.E8.configure(state="normal")
        self.E8.delete(0, "end")
        self.E8.insert("insert", str)
        self.E8.configure(state="disabled")
        self.E8.update()

    def MainLoop(self):
        self.windows.mainloop()


mainscreen = MainScreen()


if __name__ == '__main__':
    mainscreen.ScreenButton(button_position={"x": 540, "y": 500},
                            button_param={"width": 8, "height": 2, "text": "结束", "bg": "gray", "command": quit})

    mainscreen.ScreenButton(button_param={"width": 8, "height": 2, "text": "开始",
                                          "bg": "lightskyblue", "command": None})
    mainscreen.LabelText(textsize={"x": 40, "y": 300}, labtext="用例路径")
    mainscreen.LabelText(textsize={"x": 40, "y": 520}, labtext="成功数")
    mainscreen.LabelText(textsize={"x": 160, "y": 520}, labtext="成功率")
    mainscreen.LabelText(textsize={"x": 40, "y": 460}, labtext="任务ID")
    mainscreen.LabelText(textsize={"x": 280, "y": 520}, labtext="失败数")
    mainscreen.LabelText(textsize={"x": 400, "y": 520}, labtext="总数")
    mainscreen.LabelText(labtext="图片显示", fontsize=13)
    mainscreen.LabelText(textsize={"x": 700, "y": 30}, labtext="日志打印", fontsize=13)
    mainscreen.LabelText(textsize={"x": 40, "y": 400}, labtext="用例标题")
    mainscreen.MainLoop()








