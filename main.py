# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/03/26
# @Author  : 陈志鹏
# @File    : financial_tools.py

import os
import sys
import codecs
import logging
import pyautogui
import xml.sax
import configparser
import pandas as pd
from financial_ui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from other_payables import *

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

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
        self.configure_init()
        self.payables_init()
        self.mouse_init()

    def initUI(self):
        self.setupUi(self)
        self.download_payables_pushButton.clicked.connect(self.download_payables)

        # 自定义文本验证器
        validator = QRegExpValidator(self)
        # 设置属性 设置文本允许出现的字符内容
        validator.setRegExp(QRegExp('^(20[1-2][0-9])$'))
        self.s_year_lineEdit.setValidator(validator)
        self.e_year_lineEdit.setValidator(validator)

        # 自定义文本验证器
        validator = QRegExpValidator(self)
        # 设置属性 设置文本允许出现的字符内容
        validator.setRegExp(QRegExp('^(1[0-2]|0?[1-9])$'))
        self.s_month_lineEdit.setValidator(validator)
        self.e_month_lineEdit.setValidator(validator)

        self.s_year_lineEdit.editingFinished.connect(self.s_year_editingFinished)
        self.s_month_lineEdit.editingFinished.connect(self.s_month_editingFinished)
        self.e_year_lineEdit.editingFinished.connect(self.e_year_editingFinished)
        self.e_month_lineEdit.editingFinished.connect(self.e_month_editingFinished)
        self.subject_lineEdit.editingFinished.connect(self.subject_editingFinished)

    def configure_init(self):
        self.conf = configparser.ConfigParser()
        self.conf_path = os.path.join(os.getcwd(), 'configure.ini')
        self.conf.read(self.conf_path, encoding="utf-8-sig")
        # self.conf.readfp(codecs.open(self.conf_path, 'r', 'utf-8-sig'))

        if self.conf.has_option('payables', 'start_year'):
            s_year = self.conf.get('payables', 'start_year')
            self.s_year_lineEdit.setText(s_year)

        if self.conf.has_option('payables', 'start_month'):
            s_month = self.conf.get('payables', 'start_month')
            self.s_month_lineEdit.setText(s_month)

        if self.conf.has_option('payables', 'end_year'):
            e_year = self.conf.get('payables', 'end_year')
            self.e_year_lineEdit.setText(e_year)

        if self.conf.has_option('payables', 'end_month'):
            e_month = self.conf.get('payables', 'end_month')
            self.e_month_lineEdit.setText(e_month)

        if self.conf.has_option('payables', 'subject'):
            subject = self.conf.get('payables', 'subject')
            self.subject_lineEdit.setText(subject)

    def payables_init(self):
        self.thread_other_payables = QThread()
        self.worker_other_payables = WorkerOtherPayables()
        self.worker_other_payables.message_singel.connect(self.message_singel)
        self.worker_other_payables.finish_singel.connect(self.finish_singel)
        self.worker_other_payables.statusBar_singel.connect(self.statusBar_singel)
        self.worker_other_payables.moveToThread(self.thread_other_payables)
        self.thread_other_payables.started.connect(self.worker_other_payables.download)
        # self.thread_other_payables.finished.connect(self.finish_singel)

    def mouse_init(self):
        self.thread_get_mouse = QThread()
        self.worker_get_mouse = WorkerGetMouse()
        self.worker_get_mouse.mouse_singel.connect(self.mouse_singel)
        self.worker_get_mouse.moveToThread(self.thread_get_mouse)
        self.thread_get_mouse.started.connect(self.worker_get_mouse.run)
        self.thread_get_mouse.start()

    def download_payables(self):
        self.download_payables_pushButton.setEnabled(False)
        self.thread_other_payables.start()

    def s_year_editingFinished(self):
        # print(self.s_year_lineEdit.text())
        self.conf.set('payables', 'start_year', self.s_year_lineEdit.text())
        self.conf.write(codecs.open(self.conf_path, 'w', 'utf-8-sig'))

    def s_month_editingFinished(self):
        # print(self.s_month_lineEdit.text())
        self.conf.set('payables', 'start_month', self.s_month_lineEdit.text())
        self.conf.write(codecs.open(self.conf_path, 'w', 'utf-8-sig'))

    def e_year_editingFinished(self):
        # print(self.e_year_lineEdit.text())
        self.conf.set('payables', 'end_year', self.e_year_lineEdit.text())
        self.conf.write(codecs.open(self.conf_path, 'w', 'utf-8-sig'))

    def e_month_editingFinished(self):
        # print(self.e_month_lineEdit.text())
        self.conf.set('payables', 'end_month', self.e_month_lineEdit.text())
        self.conf.write(codecs.open(self.conf_path, 'w', 'utf-8-sig'))

    def subject_editingFinished(self):
        print(self.subject_lineEdit.text())
        self.conf.set('payables', 'subject', self.subject_lineEdit.text())
        self.conf.write(codecs.open(self.conf_path, 'w', 'utf-8-sig'))

    def message_singel(self, str):
        # 移动光标到最后的文字
        text_cursor = self.textBrowser.textCursor()
        text_cursor.movePosition(text_cursor.End)
        self.textBrowser.setTextCursor(text_cursor)
        self.textBrowser.insertPlainText(str)

    def statusBar_singel(self, msg):
        self.statusBar().showMessage(msg)

    def finish_singel(self):
        self.thread_other_payables.quit()
        self.download_payables_pushButton.setEnabled(True)
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
