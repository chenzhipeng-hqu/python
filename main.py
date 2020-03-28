# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/03/26
# @Author  : 陈志鹏
# @File    : financial_tools.py

import os
import sys
import logging
import pyautogui
import xml.sax
import pandas as pd
from financial_ui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from other_payables import *

# logging.basicConfig(level=logging.DEBUG,
#         filename='out.log',
#         datefmt='%Y/%m/%d %H:%M:%S',
# format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s
# - %(message)s')

logger = logging.getLogger(__name__)


class UIMainWindow(Ui_MainWindow, QMainWindow):

    def __init__(self):
        super(UIMainWindow, self).__init__()
        self.initUI()

        self.thread_other_payables = QThread()
        self.worker_other_payables = WorkerOtherPayables()
        self.worker_other_payables.message_singel.connect(self.message_singel)
        self.worker_other_payables.finish_singel.connect(self.finish_singel)
        self.worker_other_payables.statusBar_singel.connect(self.statusBar_singel)
        self.worker_other_payables.moveToThread(self.thread_other_payables)
        self.thread_other_payables.started.connect(self.worker_other_payables.merge)
        # self.thread_other_payables.finished.connect(self.finish_singel)

        self.thread_get_mouse = QThread()
        self.worker_get_mouse = WorkerGetMouse()
        self.worker_get_mouse.mouse_singel.connect(self.mouse_singel)
        self.worker_get_mouse.moveToThread(self.thread_get_mouse)
        self.thread_get_mouse.started.connect(self.worker_get_mouse.run)
        self.thread_get_mouse.start()

    def initUI(self):
        self.setupUi(self)

        self.merge_other_payables_pushButton.clicked.connect(self.merge_other_payables)

    def merge_other_payables(self):
        self.merge_other_payables_pushButton.setEnabled(False)
        self.thread_other_payables.start()

    def message_singel(self, str):
        # 移动光标到最后的文字
        textCursor = self.textBrowser.textCursor()
        textCursor.movePosition(textCursor.End)
        self.textBrowser.setTextCursor(textCursor)
        self.textBrowser.insertPlainText(str)

    def statusBar_singel(self, msg):
        self.statusBar().showMessage(msg)

    def finish_singel(self):
        self.thread_other_payables.quit()
        self.merge_other_payables_pushButton.setEnabled(True)
        # print('finished')

    def mouse_singel(self, x, y):
        self.x_label.setText('X: ' + str(x))
        self.y_label.setText('Y: ' + str(y))


class WorkerGetMouse(QObject):
    mouse_singel = Signal(int, int)

    def __init__(self):
        super(WorkerGetMouse, self).__init__()

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
        # 每一pyqt5应用程序必须创建一个应用程序对象。sys.argv参数是一个列表，从命令行输入参数
        app = QApplication(sys.argv)
        ui = UIMainWindow()
        ui.show()

        # 系统exit()方法确保应用程序干净的退出
        # 的exec_()方法有下划线。因为执行是一个Python关键词。因此，exec_()代替
        app.exec_()
    except Exception as err:
        print('catch error!!!')
        print(err)
    finally:
        # 系统exit()方法确保应用程序干净的退出
        sys.exit()
