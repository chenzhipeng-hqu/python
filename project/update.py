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

from project import log
from project import ssh

logger = log.Log(__name__, log_path=os.getcwd()).getlog()

import time
import threading
import configparser
from PyQt5.QtCore import (pyqtSignal, QTimer, QThread, QTime, QRect)


nowTime = lambda: int(round(time.time()*1000))

class Update(QThread):

    message_singel = pyqtSignal(str)
    pass_singel = pyqtSignal(bool)
    startup_singel = pyqtSignal(bool)
    statusBar_singel = pyqtSignal(str)
    timeDisp_singel = pyqtSignal(QTime)

    def __init__(self):
        super(Update, self).__init__()
        self.wait_receive = 0
        self.startup_flag = 0
        self.start_time = 0
        self.remote_path = ''
        self.select_file_path = ''
        self.send_flag = 0
        self.ip_addr = ''
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timeout_slot)
        self.timer.start(1000)
        self.time_tick=QTime()
        self.time_tick.setHMS(0,0,0)  #初始时设置时间为  00：00：00
        # self.thread_1 = threading.Thread(target=self.receive_data_thread) #建立一个线程，调用receive_data_thread方法，不带参数
        # self.thread_1.setDaemon(True) #声明为守护线程，设置的话，子线程将和主线程一起运行，并且直接结束，不会再执行循环里面的子线程
        # self.thread_1.start()

        # 加载现有配置文件
        self.conf = configparser.ConfigParser()
        # self.conf.read("../configure/configure.ini", encoding="utf-8-sig")
        self.conf.read("files/configure.ini", encoding="utf-8-sig")

            # dataset = [[] for i in range(len(lines)-1)]
            # for i in range(len(dataset)):
                # dataset[i][:] = (item for item in lines[i].strip().split(','))   # 逐行读取数据
                # logger.info("dateset:",dataset)

        pass

    def run(self):
        while True:

            if self.start_time != 0:
                if nowTime() - self.start_time > 120000:
                    self.statusBar_singel.emit("超时，烧录失败，请重新烧录!!!")
                    self.pass_singel.emit(False)
                    self.start_time = 0

            if self.send_flag == 1:
                try:
                    # self.remote_path = self.conf.get('remote_path', "file_"+os.path.splitext(os.path.basename(self.select_file_path))[0])
                    # self.remote_path = os.path.join(self.remote_path, os.path.basename(self.select_file_path))
                    # getattr(self.obj,'put')(self.select_file_path, self.remote_path)

                    self.statusBar_singel.emit("发送中...")
                    path = os.path.join('.', 'files')
                    exclue_files = ['configure.ini', 'version.txt']
                    for i in os.listdir(path):
                        if i in exclue_files:
                            continue
                        temp_file = os.path.join(path, i)
                        if os.path.isfile(temp_file):
                            if self.conf.has_option('remote_path', "file_"+os.path.splitext(os.path.basename(temp_file))[0]):
                                self.remote_path = self.conf.get('remote_path', "file_"+os.path.splitext(os.path.basename(temp_file))[0])
                                self.remote_path = os.path.join(self.remote_path, os.path.basename(temp_file))
                                getattr(self.obj,'put')(temp_file, self.remote_path)
                                logger.info('[OK] %s' % (temp_file))
                            else :
                                logger.warn('[ERR] %s (not config file path)' % (temp_file))

                    # version.txt 文件放在最后发送, 用于确认其他文件都发送完成
                    temp_file = os.path.join(path, 'version.txt')
                    self.remote_path = self.conf.get('remote_path', "file_"+os.path.splitext(os.path.basename(temp_file))[0])
                    self.remote_path = os.path.join(self.remote_path, os.path.basename(temp_file))
                    getattr(self.obj,'put')(temp_file, self.remote_path)

                    getattr(self.obj, 'cmd')('sync')
                    self.statusBar_singel.emit("发送成功!")
                    logger.info('发送完成！')
                except Exception as err:
                    logger.error(err)
                    self.statusBar_singel.emit("发送失败，请检查文件配置和网络端口是否正常！")
                finally:
                    self.send_flag = 0;

            QThread.usleep(10000)
            pass

    def connect_ssh(self, ip_addr):
        username = self.conf.get('user', "username")
        password = self.conf.get('user', "password")
        port = self.conf.get('user', "port")
        # self.obj = Tools(username, password, port, ip_addr)
        self.obj = ssh.SecureShell(username, password, port, ip_addr)
        self.statusBar_singel.emit("连接中...")

        if 0 == getattr(self.obj, "connect")():
            self.statusBar_singel.emit("连接成功！")
            getattr(self.obj, 'cmd')('killall VideoIn')
            getattr(self.obj, 'cmd')('killall videoTransfer')

            try:
                temp_file = 'files/version.txt'
                version_path = self.conf.get('remote_path', "file_"+os.path.splitext(os.path.basename(temp_file))[0])
                version_file = os.path.join(version_path, 'version.txt')
                getattr(self.obj, 'get')('version_r.txt', version_file)

                f_remote = open('version_r.txt', 'r')
                r_line = f_remote.readline()

                f_local = open('files/version.txt', 'r')
                l_line = f_local.readline()

                self.message_singel.emit('\r\nfile:           local:      remote:    status:\r\n')

                while l_line:
                    l_version = l_line.split(' ')[-1].strip('\n')
                    r_version = r_line.split(' ')[-1].strip('\n')

                    l_file = l_line.split(' ')[0]
                    r_file = r_line.split(' ')[0]

                    # print(l_file, ' ', r_file)
                    logger.info('%s' % (l_file + ' ' +l_version + ' ' + r_version))

                    if l_version != r_version:
                        self.message_singel.emit(l_line.strip('\n')+'    '+r_version + '    diff\r\n')
                    else:
                        self.message_singel.emit(l_line.strip('\n')+'    '+r_version + '\r\n')

                    r_line = f_remote.readline()
                    l_line = f_local.readline()
            except Exception as err:
                logger.error(err)

            return 0
        else:
            self.statusBar_singel.emit("连接失败！")
            return 1

    def disConnect_ssh(self):
        getattr(self.obj, 'close')()
        self.statusBar_singel.emit("断开成功！")
        return 0

    def receive_data_thread(self):
        # logger.info('start receive_data_thread.')
        while True:
            time.sleep(0.001)
            try:
                pass

            except Exception as err:
                logger.error('receive error: %s' % err)
            pass

    def timeout_slot(self):
        if self.time_tick.msec() % 1000 == 0 and self.startup_flag == 1:
            self.time_tick = self.time_tick.addMSecs(1000)
            self.timeDisp_singel.emit(self.time_tick)

if __name__ == '__main__':
    logger.info('\r\n ---------------- welcom to use -----------------')
