
#
# -*- coding: utf-8 -*-

"""
In this example, we create a simple window in PyQt5.

author: chenzhipeng3472
last edited: 04-July-2018
"""
__author__ = 'chenzhipeng3472'

import os
import time
from enum import Enum, unique
# from PyQt5.QtCore import (pyqtSignal, QThread)
from PySide2.QtCore import (Signal, QThread)

from Canopen_Protocol import CanopenProtocol

nowTime = lambda:int(round(time.time()*1000))

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
    processBar_singel = Signal(int)
    message_singel = Signal(str)

    def __init__(self):
        super(UpgradeFPGA, self).__init__()
        self.Download_state = DOWNLOAD_STATE.INITIALIZE.value
        self.errCnt = 0
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
        receive_data = list()
        can_cmd = self.__dev.getRevData(rev_type, node_id, wait_time)

        while 0 < len(can_cmd):
            dat = can_cmd.pop(0)
            if len(dat) > 7 and dat[0] == node_id and dat[2] >= dat[3]: # 这里取值逻辑与MCU储存逻辑相反，可能由于大小端模式影响，待确认
                receive_data.append(dat[4])
                receive_data.append(dat[5])
                receive_data.append(dat[6])
                receive_data.append(dat[7])

        return receive_data

    def downloadProcess(self, boardType, file_name, nodes_idx_need_program):

        isDownloadFinish = False
        node_idx_need_program = [nodes_idx_need_program[0]]
        # print('fpga downloadProcess ')
        # print(" ".join(hex(i) for i in nodes_idx_need_program))
        # print(" ".join(hex(i) for i in node_idx_need_program))

        if self.Download_state == DOWNLOAD_STATE.INITIALIZE.value: #---- 初始化数据---
            print('下载程序...')
            self.Download_state = DOWNLOAD_STATE.ENTER_UPGRADE.value
            pass

        elif self.Download_state == DOWNLOAD_STATE.ENTER_UPGRADE.value: #---- 复位看门狗---
            print('into Analog/Digital FPGA bootloader...')
            self.blockNum = 0
            Is_File_exist = int(0)
            while Is_File_exist == 0:
                Is_File_exist = os.path.exists(file_name)
                if Is_File_exist:
                    self.size = os.path.getsize(file_name)
                    creat_time = os.path.getmtime(file_name)
                    print('')
                    print("%s  %s  %d bytes" % (file_name, self.TimeStampToTime(creat_time), self.size))
                    print('正在升级...  ')
                    self.message_singel.emit('找到文件，正在升级 ' + file_name + '  Version: ' + self.TimeStampToTime(creat_time) + ' ... \r\n')
                else:
                    print("找不到该文件  %s , 请放置该文件到该目录下,放置后自动开始下载" % (file_name))
                    self.message_singel.emit('找不到该文件  %s , 请放置该文件到bin目录下,\r\n' % (file_name))
                    time.sleep(3)
                    # print('当前工作路径为：%s ' % (os.getcwd()))
                    # os.chdir(".//bin")  # 如果找不到bin文件路径就切换到当前目录下找到bin文件夹
                    # print('切换后工作路径为：%s ' % (os.getcwd()))

            with open(file_name, 'rb') as f_mcs:
                for i, line in enumerate(f_mcs):
                    if line.__len__()>10  and ord('4') == line[8] and ord('0') == line[7]:
                        self.blockNum = self.blockNum.__add__(1)

            send = 'enterUpgrade tvs200 %s bin %d\n' % (boardType, self.blockNum)
            print(send)
            for node_id in node_idx_need_program:
                self.sendFpgaUpgradeCmd_AD(node_id, send)
                time.sleep(0.1)
                receive_data = bytes(self.getRevData(self.__dev.PDO1_Tx, node_id, 3000)).decode()
                if 'OK enterUpg 00 #A4\n' in receive_data:
                # if 'enterUpg' in receive_data.decode():
                    print('cmp OK! enterUpgrade model.')
                else:
                    print('cmp ERR!')
                    print(receive_data)

                with open(file_name, 'rb') as f_mcs:
                    isFileEnd = False
                    isSendFail = False
                    addr = 0
                    curBlock = 0
                    length = 0
                    totalLength = 0
                    binSum = 0
                    binData = [0xff] * 65536
                    offset = 0
                    self.errCnt = 0
                    for i, line in enumerate(f_mcs):
                        if not isFileEnd and isSendFail == False:
                            lineData = self.str2hex(line)
                            if lineData[0]+5 != len(lineData):
                                continue
                                print('lineData err!!!!!!!')
                                print(lineData)

                            if lineData[3] == 0x04: #segment address
                            # if lineData[3] == 0x04 or lineData[3] == 0x01: #segment address    # end file: 
                                # print(lineData)
                                if length > 0:
                                    curBlock = curBlock + 1
                                    # upgrade Section
                                    # print('1. start upgradeSection')
                                    isSendFail = self.upgradeSection(node_id, addr, length, binSum, boardType, binData)
                                    # print('1. end upgradeSection')
                                    print('1.curBlock:%d' % curBlock)
                                    self.processBar_singel.emit((curBlock/self.blockNum)*100)
                                    totalLength = totalLength + length
                                    length = 0
                                    binSum = 0
                                    pass
                                else:
                                    #file head, update UI
                                    self.processBar_singel.emit((curBlock/self.blockNum)*100)
                                    print('2.curBlock:%d' % curBlock)
                                    pass

                                if lineData[0] == 0x02:
                                    # addr = lineData[4]
                                    addr = ((lineData[4]<<8) | lineData[5]) << 16
                                    # addr <<= 16
                                elif lineData[0] == 0x01:
                                    addr = lineData[4] << 16
                                    # addr <<= 16

                                pass
                            elif lineData[3] == 0x01: # end file
                                if length > 0:
                                    curBlock = curBlock + 1
                                    # upgrade Section
                                    # print('2. start upgradeSection')
                                    isSendFail = self.upgradeSection(node_id, addr, length, binSum, boardType, binData)
                                    # print('2. end upgradeSection')
                                    self.processBar_singel.emit((curBlock/self.blockNum)*100)
                                    totalLength = totalLength + length
                                    length = 0
                                    binSum = 0
                                    print('3.curBlock:%d' % curBlock)

                                # print(lineData)
                                isFileEnd = True
                                pass
                            elif lineData[3] == 0x00: # data
                                length = length + lineData[0]
                                offset = lineData[1]
                                offset = offset<<8 | lineData[2]
                                for i in range(0, lineData[0]):
                                    # print(binData[0])
                                    binData[i+offset] = lineData[i+4]
                                    binSum = binSum + lineData[i+4]

                                # if lineData[0] == 0x02: # 最后一行数据
                                    # print(lineData)
                                pass
            if not isSendFail:
                send = 'upgrade %s %d \n' % (boardType, totalLength)
                self.sendFpgaUpgradeCmd_AD(node_id, send)
                print(send)

                receive_data = bytes(self.getRevData(self.__dev.PDO1_Tx, node_id, 20000)).decode()

                if len(receive_data) <= 0:  # time_out
                    print('sendFpgaUpgradePack time_out node_id=0x%02X' % node_id)
                else:
                    print(receive_data)
                    if 'OK' in receive_data:
                    # if 'OK Upgrade finish!' in receive_data:
                        print('升级成功\n')
                        self.message_singel.emit('升级成功 --> ' + str(hex(node_id)) + ' \r\n')
                    else:
                        isSendFail = True

            if isSendFail:
                self.message_singel.emit('升级失败 --> ' + str(hex(node_id)) + ' \r\n')
                print('isSendFail = {} !!!'.format(isSendFail))
                print('升级失败！！！！！！！\n')

            self.Download_state = DOWNLOAD_STATE.SEND_FILE.value

        elif self.Download_state == DOWNLOAD_STATE.SEND_FILE.value: #send file
            self.Download_state = DOWNLOAD_STATE.REBOOT.value

        elif self.Download_state == DOWNLOAD_STATE.REBOOT.value: #----start--- 发送重启命令
            node_idx_need_program.pop(0)
            nodes_idx_need_program.pop(0)
            self.Download_state = DOWNLOAD_STATE.FINISH_UPGRADE.value

        elif self.Download_state == DOWNLOAD_STATE.FINISH_UPGRADE.value: #----完成烧录---
            if len(nodes_idx_need_program) == 0:
                isDownloadFinish = True
            self.Download_state = DOWNLOAD_STATE.ENTER_UPGRADE.value

        return isDownloadFinish

    def upgradeSection(self, node_id, addr, length, binSum, boardType, binData):
        isSendFail = True
        errCnt = 0;
        self.errCnt = 0

        send = 'loadBin %s %x %x %x ' % (boardType, addr, length, binSum&0x7fffffff)
        byteSum = 0;
        for dat_ in send:
            byteSum = byteSum + ord(dat_)
        send = send + ('%x\n' % (byteSum))

        while isSendFail == True and errCnt < 3:
            isSendFail = False
            # self.getRevData(self.__dev.PDO1_Tx, node_id, 1)
            self.sendFpgaUpgradeCmd_AD(node_id, send)
            time.sleep(0.01)

            receive_data = bytes(self.getRevData(self.__dev.PDO1_Tx, node_id, 3000)).decode()

            if len(receive_data) <= 0:  # time_out
                print(receive_data)
                print(send)
                print('sendFpgaUpgradeCmd_AD time_out node_id=0x%02X' % node_id)
                self.errCnt = self.errCnt + 1
                errCnt = errCnt + 1
                print('errCnt=%d' % (errCnt))
            else:
                # print(receive_data)
                pass

            # self.getRevData(self.__dev.PDO1_Tx, node_id, 1)
            self.sendFpgaUpgradeData_AD(node_id, binData, length)
            time.sleep(0.03)

            receive_data = bytes(self.getRevData(self.__dev.PDO1_Tx, node_id, 3000)).decode()

            if len(receive_data) <= 0:  # time_out
                print(receive_data)
                print(send)
                print('sendFpgaUpgradeData_AD time_out node_id=0x%02X' % node_id)
                self.errCnt = self.errCnt + 1
                errCnt = errCnt + 1
                print('errCnt=%d' % (errCnt))
                isSendFail = True
            else:
                # print(len(receive_data))
                # print(receive_data)
                if 'OK' in receive_data:
                # if 'OK %X' % (binSum) in receive_data:
                    isSendFail = False
                    self.errCnt = 0
                    errCnt = 0
                else:
                    print(len(receive_data))
                    print(receive_data)
                    print(send)
                    print('     receive err!!!!!!!!!!!!!!!!!!!!!!!\r\n')
                    self.getRevData(self.__dev.PDO1_Tx, node_id, 1)
                    isSendFail = True
                    self.errCnt = self.errCnt + 1
                    errCnt = errCnt + 1
                    print('errCnt=%d' % (errCnt))
                    # isSendFail = False
        # print('isSendFail = {}'.format(isSendFail))
        # print('errCnt=%d' % errCnt)

        return isSendFail

    def sendFpgaUpgradeCmd_AD(self, node_id, dat):
        self.getRevData(self.__dev.PDO1_Tx, node_id, 1)
        send_data = list(dat)
        for i, dat_ in enumerate(send_data):
            # print(type(dat_))
            send_data[i] = ord(dat_)
            # print(type(str(dat_)))

        length = len(send_data)
        send_times_high = length//7
        send_times_low = length%7
        # print(send_times_high)
        # print(send_times_low)

        send_times_cnt = 0
        send = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02]

        if send_times_high >= 1:
            # print('send_times_high')
            for i in range(0,send_times_high):
                send[:7] = send_data[i*7:i*7+7]
                self.sendData(self.__dev.PDO1_Rx, node_id, send)
                send_times_cnt = i + 1

        # print(send_times_cnt)
        send = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02]
        if (send_times_low >= 1):
            # print('send_times_low')
            send[:send_times_low] = send_data[(send_times_cnt)*7:(send_times_cnt)*7+send_times_low]
            self.sendData(self.__dev.PDO1_Rx, node_id, send)

    def sendFpgaUpgradeData_AD(self, node_id, dat, length):
        self.getRevData(self.__dev.PDO1_Tx, node_id, 1)
        send_data = list(dat)

        # length = length
        send_times_high = length//7
        send_times_low = length%7
        # print(send_times_high)
        # print(send_times_low)

        send_times_cnt = 0
        send = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02]

        # print(nowTime()%1000000)
        start_time = nowTime()
        if send_times_high >= 1:
            # print('send_times_high')
            for i in range(0,send_times_high):
                send[:7] = send_data[i*7:i*7+7]
                self.sendData(self.__dev.PDO3_Rx, node_id, send)
                send_times_cnt = i + 1
                if(i%3 == 0):
                    time.sleep(0.001)

        # print(send_times_cnt)
        # send = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02]
        send = [0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x02]
        if (send_times_low >= 0):
            # print('send_times_low')
            send[:send_times_low] = send_data[(send_times_cnt)*7:(send_times_cnt)*7+send_times_low]
            self.sendData(self.__dev.PDO1_Rx, node_id, send)
        # print(nowTime()-start_time, )

    def str2hex(self, line):
        lineData = list()
        idx = 1
        while idx < line.__len__()-1:
            if (line[idx] != ord('\r') and line[idx+1] != ord('\n')):
                # data = '%c%c' % (line[idx], line[idx+1])
                lineData.append(int('%c%c' % (line[idx], line[idx+1]), 16))
                # print(type(lineData[0]))
            idx = idx + 2

        return lineData


    def TimeStampToTime(self, timestamp):
        timeStruct = time.localtime(timestamp)
        return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)



