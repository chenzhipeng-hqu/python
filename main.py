# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/03/26
# @Author  : 陈志鹏
# @File    : financial_tools.py

import os, sys, logging
import pyautogui
import xml.sax
import pandas as pd
import financial_ui as ui
from PySide2.QtWidgets import *
from PySide2.QtCore import *

# logging.basicConfig(level=logging.DEBUG,
#         filename='out.log',
#         datefmt='%Y/%m/%d %H:%M:%S',
#         format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')

logger = logging.getLogger(__name__)

class ExcelHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.chars = [  ]
        self.cells = [  ]
        self.rows = [  ]
        self.tables = [  ]
    def characters(self, content):
        self.chars.append(content)
    def startElement(self, name, atts):
        if name=="Cell":
            self.chars = [  ]
        elif name=="Row":
            self.cells=[  ]
        elif name=="Table":
            self.rows = [  ]
    def endElement(self, name):
        if name=="Cell":
            self.cells.append(''.join(self.chars))
        elif name=="Row":
            self.rows.append(self.cells)
        elif name=="Table":
            self.tables.append(self.rows)

def merge_files(file_path, dst_name):
    filelist = []

    for root, dirs, files in os.walk(file_path, topdown=False):
        for name in files:
            str = os.path.join(root, name)
            if str.split('.')[-1] == 'xls':
                filelist.append(str)
    print(filelist)

    dfs = []
    for file in filelist:
        file_name = os.path.basename(file)
        # print(file_name.split('-')[0])
        excelHandler = ExcelHandler()
        xml.sax.parse(file, excelHandler) #文件名
        df = pd.DataFrame(excelHandler.tables[0][1:], columns=excelHandler.tables[0][0])
        df['法人主体'] = file_name.split('-')[0]
        dfs.append(df)

    # 将多个DataFrame合并为一个
    df = pd.concat(dfs)
    print(df.head(), df.shape)
    df.to_excel(r'%s/%s.xlsx' % (file_path, dst_name), index=False)


class UI_MainWindow(ui.Ui_MainWindow, QMainWindow):

    def __init__(self):
        super(UI_MainWindow, self).__init__()
        self.initUI()

        self.worker_merge_other_payables = Worker_Merge_Other_Payables(self)
        self.worker_merge_other_payables.message_singel.connect(self.message_singel)

        self.worker_get_mouse = Worker_Get_Mouse(self)
        self.worker_get_mouse.mouse_singel.connect(self.mouse_singel)
        self.worker_get_mouse.start()

    def initUI(self):
        self.setupUi(self)

        self.merge_other_payables_pushButton.clicked.connect(self.merge_other_payables)

    def merge_other_payables(self):
        self.worker_merge_other_payables.start()

    def message_singel(self, str):
        # 移动光标到最后的文字
        textCursor = self.textBrowser.textCursor()
        textCursor.movePosition(textCursor.End)
        self.textBrowser.setTextCursor(textCursor)

        self.textBrowser.insertPlainText(str)

    def mouse_singel(self, x, y):
        self.x_label.setText('X: '+str(x))
        self.y_label.setText('Y: '+str(y))



class Worker_Get_Other_Payables(QThread):
    def __init__(self, ui):
        pass

    def login(self):
        # 1. 打开任务栏软件
        # 2. 双击用户
        # 3. 输入账号
        # 4. 输入密码
        # 5. 点击确定
        pass

    def select_center(self):
        # 1. 选择营运中心
        # 2. 
        pass

    def filter(self):
        pass

    def export(self):
        pass

    def rename(self):
        pass

    def get(self):
        # 1. 打开软件，登入账号
        self.login()
        # 1. 选择营运中心
        self.select_center()
        # 2. 筛选条件（期间（年、月、年、月）， 科目（两次））
        # 3. 点击确定筛选
        self.filter()
        # 4. 导出/汇出excel
        self.export()
        # 5. 保存
        # 6. 更改文件名，法人-默认
        self.rename()
        # 7. 最后一列添加‘法人主体’， 已经在合并里面实现
        pass

class Worker_Merge_Other_Payables(QThread):
    message_singel = Signal(str)

    def __init__(self, ui):
        super(Worker_Merge_Other_Payables, self).__init__()
        self.ui = ui

    def __del__(self):
        print('delete Worker_Merge_Other_Payables')

    def run(self):
        self.ui.merge_other_payables_pushButton.setEnabled(False)
        self.message_singel.emit('start merge_inner_order...\r\n')
        file_path = "D:/CZP/python/FinancialTools/original_data/merge_datas"
        merge_files(file_path, 'merge')
        self.message_singel.emit('merge_inner_order ok!\r\n')
        self.ui.merge_other_payables_pushButton.setEnabled(True)


class Worker_Get_Mouse(QThread):
    mouse_singel = Signal(int, int)

    def __init__(self, ui):
        super(Worker_Get_Mouse, self).__init__()
        self.ui = ui

    def __del__(self):
        print('delete Worker_Get_Mouse')

    def run(self):
        while True:
            x, y = pyautogui.position()
            self.mouse_singel.emit(x, y)
            QThread.usleep(100000)
            # positionStr = 'X: ' + str(x).rjust(4) + 'Y: ' + str(y).rjust(4)


if __name__ == '__main__':

    try:
        #每一pyqt5应用程序必须创建一个应用程序对象。sys.argv参数是一个列表，从命令行输入参数
        app = QApplication(sys.argv)
        ui = UI_MainWindow()
        ui.show()

        #系统exit()方法确保应用程序干净的退出
        #的exec_()方法有下划线。因为执行是一个Python关键词。因此，exec_()代替
        app.exec_()
    except Exception as err:
        print('catch error!!!')
        print(err)
    finally:
        # 系统exit()方法确保应用程序干净的退出
        sys.exit()



