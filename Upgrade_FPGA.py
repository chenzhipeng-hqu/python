
#
# -*- coding: utf-8 -*-

"""
In this example, we create a simple window in PyQt5.

author: chenzhipeng3472
last edited: 04-July-2018
"""
__author__ = 'chenzhipeng3472'

import os
from enum import Enum, unique
from PyQt5.QtCore import (pyqtSignal, QThread)

from Canopen_Protocol import CanopenProtocol

@unique       #如果要限制定义枚举时，不能定义相同值的成员。可以使用装饰器@unique【要导入unique模块】
class DOWNLOAD_STATE(Enum):
    INITIALIZE      = 0x00
    ENTER_UPGRADE   = 0x01
    SEND_FILE       = 0x02
    REBOOT          = 0x03
    FINISH_UPGRADE  = 0x04

class UpgradeFPGA(QThread):
    '''
    UpgradeFPGA
    '''
    #定义一个信号
    processBar_singel = pyqtSignal(int)
    message_singel = pyqtSignal(str)

    def __init__(self):
        super(UpgradeMCU, self).__init__()
        self.Download_state = DOWNLOAD_STATE.INITIALIZE.value
        pass

    def __del__(self):
        pass

    def setInterfaceDev(self, dev):
        self.__dev = dev
        # print(dir(self.dev))

    def sendData(self, send_type, node_id, data):
        self.__dev.sendData(send_type, node_id, 8, data)
        pass

    def getRevData(self, rev_type, node_id, wait_time):
        return self.__dev.getRevData(rev_type, node_id, wait_time)

    def downloadProcess(self, file_name, node_idx_need_program):

        isDownloadFinish = False

        if self.Download_state == DOWNLOAD_STATE.INITIALIZE.value: #---- 初始化数据---
            print('下载程序...')
            self.Download_state = DOWNLOAD_STATE.ENTER_UPGRADE.value
            pass

        elif self.Download_state == DOWNLOAD_STATE.ENTER_UPGRADE.value: #---- 复位看门狗---
            self.Download_state = DOWNLOAD_STATE.SEND_FILE.value

        elif self.Download_state == DOWNLOAD_STATE.SEND_FILE.value: #send file
            self.Download_state = DOWNLOAD_STATE.REBOOT.value

        elif self.Download_state == DOWNLOAD_STATE.REBOOT.value: #----start--- 发送重启命令
            self.Download_state = DOWNLOAD_STATE.FINISH_UPGRADE.value

        elif self.Download_state == DOWNLOAD_STATE.FINISH_UPGRADE.value: #----完成烧录---
            isDownloadFinish = True
            self.Download_state = DOWNLOAD_STATE.ENTER_UPGRADE.value
            print(self.Download_state)
            print(dir(self.Download_state))
