# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/05/30
# @Author  : 陈志鹏
# @File    : xx.py
"""

"""

__author__ = '陈志鹏'

import os
import sys
work_path = os.path.join(os.path.dirname(sys.argv[0]), "../")
sys.path.append(os.path.abspath(work_path))
os.chdir(work_path)

# ImportError: unable to find Qt5Core.dll on PATH
# https://blog.csdn.net/zwyact/article/details/99778898  
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
	
from project import log
from project import ssh
from project import update
from project import ui

logger = log.Log(__name__, log_path=os.getcwd()).getlog()

import time
import configparser
from PyQt5.QtWidgets import (QWidget, QFileDialog, QApplication, QMainWindow, QComboBox)
from PyQt5.QtCore import (pyqtSignal, QTimer, QThread, QTime, QRect)


import configparser
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', help='Specify config file, use absolute path')
args = parser.parse_args()
if args.config:
    # 加载现有配置文件
    conf = configparser.ConfigParser()
    path = os.path.join(os.getcwd(), args.config)
    logger.info(path)
    conf.read(path, encoding="utf-8-sig")
    # 登陆信息
    ip_conf = conf.get('ethernet', 'ip')
else:
    ip_conf = ''


nowTime = lambda:int(round(time.time()*1000))

class UI_MainWindow(ui.Ui_MainWindow, QMainWindow):
    '''
    直接继承界面类
    '''
    def __init__(self):
        super(UI_MainWindow,self).__init__()

        self.setupUi(self)

        self.initUI()

        self.last_open_path = '../'

        self.AudoDownload = False
        if args.config:
            self.AutoDownload = True
            self.ip_lineEdit.setText(ip_conf)
            time.sleep(1)
            self.connect_button.click()
            time.sleep(1)
            self.send_pushButton.click()

    def __del__(self):
        logger.info('MainWindow delete.')

    def initUI(self):

        self.interface = update.Update()
        self.interface.message_singel.connect(self.message_singel)
        self.interface.statusBar_singel.connect(self.statusBar_singel)
        self.interface.startup_singel.connect(self.startup_singel)
        self.interface.timeDisp_singel.connect(self.timeDisp_singel)
        self.interface.start()

        textCursor = self.Msg_TextEdit.textCursor()
        textCursor.movePosition(textCursor.End)
        self.Msg_TextEdit.setTextCursor(textCursor)
        # self.message_singel("welcome to use.\r\n");

        #Send_LineEdit_Finished
        self.Send_LineEdit.editingFinished.connect(self.Send_LineEdit_Finished)
        # self.Send_LineEdit.setEnabled(True)

        self.select_file.clicked.connect(self.OpenFileDialog)
        self.select_file.setEnabled(False)

        # self.remote_path.clicked.connect(self.remote_path_select)

        self.connect_button.clicked.connect(self.connect_ssh)

        self.send_pushButton.clicked.connect(self.send_file)

        pass

    def send_file(self):
        # self.interface.ip_addr = self.ip_lineEdit.text().strip()
        # logger.info(self.ip_lineEdit.text())
        self.interface.send_flag = 1

    def OpenFileDialog(self):
        fname,ftype=QFileDialog.getOpenFileName(self,'打开文件',self.last_open_path)
        # if fname[0]:
        if os.path.isfile(fname):
            self.last_open_path = os.path.dirname(fname)
            self.select_file.setText(fname)
            self.statusBar_singel(fname)
            # logger.info(os.path.basename(fname))
            self.interface.select_file_path = fname

    def connect_ssh(self):
        source = self.sender()
        if source.text() == '连接':
            ret = self.interface.connect_ssh(self.ip_lineEdit.text().strip())
            if ret == 0:
                source.setText('断开')
                source.setChecked(True)
            else:
                source.setChecked(False)

        elif source.text() == '断开':
            ret = self.interface.disConnect_ssh()
            if ret == 0:
                source.setText('连接')
                source.setChecked(False)
            else:
                source.setChecked(True)

    #message_singel
    def message_singel(self, str):
        # 移动光标到最后的文字
        textCursor = self.Msg_TextEdit.textCursor()
        textCursor.movePosition(textCursor.End)
        self.Msg_TextEdit.setTextCursor(textCursor)

        self.Msg_TextEdit.insertPlainText(str)

    def timeDisp_singel(self, now_time):
        self.mac_lineEdit.setText(now_time.toString("hh:mm:ss"))

    #statusBar_singel
    def statusBar_singel(self, str):
        self.statusBar().showMessage(str)

    #startup_singel
    def startup_singel(self, is_startup):
        if is_startup == True:
            # self.statusBar().showMessage("板卡进入boot成功")
            self.statusBar().showMessage(' ')


    def Send_LineEdit_Finished(self):
        logger.info(self.Send_LineEdit.text())
        send_data = '%s\r\n' % self.Send_LineEdit.text()
        self.interface.sendCmd(send_data)

def main():
    '''
    main
    '''

    # if sys.stdout.isatty():
    #     default_encoding = sys.stdout.encoding
    # else:
    #     default_encoding = locale.getpreferredencoding()

    logger.info('当前工作路径为：%s ' % (os.getcwd()))
    logger.info('当前运行程序为：%s ' % (sys.argv[0]))

    run_time = nowTime()

    try:
        #每一pyqt5应用程序必须创建一个应用程序对象。sys.argv参数是一个列表，从命令行输入参数。
        app = QApplication(sys.argv)

        ui = UI_MainWindow()

        ui.show()

        #系统exit()方法确保应用程序干净的退出
        #的exec_()方法有下划线。因为执行是一个Python关键词。因此，exec_()代替
        app.exec_()
    except Exception as err:
        logger.error('catch error!!!')
        logger.error(err)

    finally:
        logger.info('runing time is {}s '.format((nowTime()-run_time)/1000))
        #系统exit()方法确保应用程序干净的退出
        sys.exit()

if __name__ == '__main__':
    logger.info('\r\n\r\n ---------------- welcom to use -----------------')
    main()
