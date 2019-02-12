
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
from PyQt5.QtCore import (pyqtSignal, QThread)

from Canopen_Protocol import CanopenProtocol


@unique       #   如果要限制定义枚举时，不能定义相同值的成员。可以使用装饰器@unique【要导入unique模块】
class DOWNLOAD_STATE(Enum):
    INITIALIZE      = 0x00
    ENTER_UPGRADE   = 0x01
    SEND_FILE       = 0x02
    REBOOT          = 0x03
    FINISH_UPGRADE  = 0x04


@unique       #  如果要限制定义枚举时，不能定义相同值的成员。可以使用装饰器@unique【要导入unique模块】
class FPGA_CMD(Enum):
    GET_SW_VERSION  = 0x00
    ACK             = 0x01
    RET_SW_VERSION  = 0x02
    GET_HW_INFO     = 0x03
    RET_HW_INFO     = 0x04
    START_UPGRADE   = 0x05
    SEND_DATA       = 0x06
    RET_CRC         = 0x07
    SWITCH_TO_ISP   = 0x08
    RET_ISP         = 0x09
    SWITCH_MAP      = 0x0a
    SET_LVDS_PARAM  = 0x0b
    SET_OUTPUT_TIM  = 0x0c

class UpgradeUSBPD(QThread):
    '''
    UpgradeUSBPD
    '''
    #定义一个信号
    processBar_singel = pyqtSignal(int)
    message_singel = pyqtSignal(str)

    def __init__(self):
        super(UpgradeUSBPD, self).__init__()
        self.Download_state = DOWNLOAD_STATE.INITIALIZE.value
        print('{}'.format(self.Download_state))
        pass

    def __del__(self):
        pass

    def setInterfaceDev(self, dev):
        self.__dev = dev

    def sendData(self, send_type, node_id, data):
        self.__dev.sendData(send_type, node_id, 8, data)
        pass

    def getRevData(self, rev_type, node_id, wait_time):
        receive_data = list()
        can_cmd = self.__dev.getRevData(rev_type, node_id, wait_time)


        while 0 < len(can_cmd):
            dat = can_cmd.pop(0)
            # print('     dat: %s' % (" ".join(hex(k) for k in dat)))
            if dat[0] == node_id and dat[2] >= dat[3]: # 这里取值逻辑与MCU储存逻辑相反，可能由于大小端模式影响，待确认
                receive_data.append(dat[4])
                receive_data.append(dat[5])
                receive_data.append(dat[6])
                receive_data.append(dat[7])

        # print(receive_data)
        return receive_data

    def setMcuEnterIspSystem(self, node_idx_need_program):
        for node_id in node_idx_need_program:
            # set boot0 = 1
            send = [0x01, 0x42, 0x40, 0x00, 0x00, 0x00, 0x01, 0x0d]
            self.sendData(self.__dev.PDO1_Rx, node_id, send)

            # set reset = 0
            send = [0x01, 0x42, 0x80, 0x01, 0x00, 0x00, 0x02, 0x0d]
            self.sendData(self.__dev.PDO1_Rx, node_id, send)

            time.sleep(1)

            # set reset = 1
            send = [0x01, 0x42, 0x80, 0x00, 0x00, 0x00, 0x03, 0x0d]
            self.sendData(self.__dev.PDO1_Rx, node_id, send)

            time.sleep(1)
            # send 0x7f
            send = [0x05, 0xF0, 0x7F, 0x00, 0x00, 0x00, 0x04, 0x0d]
            self.sendData(self.__dev.PDO1_Rx, node_id, send)
            receiveCanData = self.getRevData(0x01, node_id, 1000)

            send = [0x05, 0xF1, 0x01, 0x0F, 0x00, 0x00, 0x05, 0x0d]
            self.sendData(self.__dev.PDO1_Rx, node_id, send)

            receiveCanData = self.getRevData(0x01, node_id, 3000)

            if len(receiveCanData) <= 0:  # time_out
                print('sendFpgaUpgradePack time_out node_id=0x%02X' % node_id)
                print('     receive from 0x%02X FPGA: %s' % (node_id , " ".join(hex(k) for k in receiveCanData)))
                return 1
            elif receiveCanData[0] == 0x79:
                print('     receive from 0x%02X FPGA: %s' % (node_id , " ".join(hex(k) for k in receiveCanData)))
                return 0
            else:
                print('     receive from 0x%02X FPGA: %s' % (node_id , " ".join(hex(k) for k in receiveCanData)))
                return 1

    def setMcuExitIspSystem(self, node_idx_need_program):
        for node_id in node_idx_need_program:
            # set boot0 = 0
            send = [0x01, 0x42, 0x40, 0x01, 0x00, 0x00, 0x01, 0x0d]
            self.sendData(self.__dev.PDO1_Rx, node_id, send)

            # set reset = 0
            send = [0x01, 0x42, 0x80, 0x01, 0x00, 0x00, 0x02, 0x0d]
            self.sendData(self.__dev.PDO1_Rx, node_id, send)

            time.sleep(1)

            # set reset = 1
            send = [0x01, 0x42, 0x80, 0x00, 0x00, 0x00, 0x03, 0x0d]
            self.sendData(self.__dev.PDO1_Rx, node_id, send)

    def downloadProcess(self, startAddr, file_name, node_idx_need_program):

        isDownloadFinish = False

        if self.Download_state == DOWNLOAD_STATE.INITIALIZE.value: #---- 初始化数据---
            if self.setMcuEnterIspSystem(node_idx_need_program) == 0:
                print('{}'.format(self.Download_state))
                self.Download_state = DOWNLOAD_STATE.ENTER_UPGRADE.value
            else:
                print('mcu did not reset.')

        elif self.Download_state == DOWNLOAD_STATE.ENTER_UPGRADE.value: #---- 复位看门狗---

            for node_id in node_idx_need_program:
                # get command
                data = [0x00, 0x00 ^ 0xff]
                receiveCanData = self.sendUsbPdData(node_id, data)

                if len(receiveCanData) <= 0:  # time_out
                    print('sendFpgaUpgradePack time_out node_id=0x%02X' % node_id)
                    print('     receive from 0x%02X FPGA: %s' % (node_id , " ".join(hex(k) for k in receiveCanData)))
                else:
                    print('     receive from 0x%02X FPGA: %s' % (node_id , " ".join(hex(k) for k in receiveCanData)))

                Is_File_exist = int(0)

                while Is_File_exist == 0:
                    Is_File_exist = os.path.exists(file_name)
                    if Is_File_exist:
                        self.size = os.path.getsize(file_name)
                        creat_time = os.path.getmtime(file_name)
                        print('')
                        print("%s  %s  %d bytes" % (file_name, self.TimeStampToTime(creat_time), self.size))
                        print('正在升级...  ',  end=' ')
                        self.message_singel.emit('找到文件，正在升级 ' + file_name + '  Version: ' + self.TimeStampToTime(creat_time) + ' ... \r\n')
                    else:
                        print("找不到该文件  %s , 请放置该文件到该目录下,放置后自动开始下载" % (file_name))
                        self.message_singel.emit('找不到该文件  %s , 请放置该文件到bin目录下,\r\n' % (file_name))
                        time.sleep(3)

                with open(file_name, 'rb') as f_bin:
                    print('file size: %d' % self.size)
                    self.f_bin_data = f_bin.read(self.size)

                self.cmdEraseMemory(node_id)

                self.send_file_ret = 1
                self.send_file_tell = -1

            print('{}'.format(self.Download_state))
            self.Download_state = DOWNLOAD_STATE.SEND_FILE.value

        elif self.Download_state == DOWNLOAD_STATE.SEND_FILE.value: #send file
            self.send_file_ret = self.sendBinFile(file_name, self.send_file_ret, node_idx_need_program)
            print('{}'.format(self.Download_state))
            self.Download_state = DOWNLOAD_STATE.REBOOT.value

        elif self.Download_state == DOWNLOAD_STATE.REBOOT.value: #----start--- 发送重启命令
            # self.setMcuExitIspSystem(node_idx_need_program)
            print('{}'.format(self.Download_state))
            node_idx_need_program.pop()
            self.Download_state = DOWNLOAD_STATE.FINISH_UPGRADE.value

        elif self.Download_state == DOWNLOAD_STATE.FINISH_UPGRADE.value:  #  ----完成烧录---
            print('{}'.format(self.Download_state))
            self.Download_state = DOWNLOAD_STATE.INITIALIZE.value
            isDownloadFinish = True

        return isDownloadFinish

    def sendUsbPdData(self, node_id, dat):

        send_data = list(dat)

        send_times_high = len(send_data)//4
        send_times_low = len(send_data)%4
        # print(send_times_high)
        # print(send_times_low)

        # print('sendFpgaUpgradePack: %s' % " ".join(hex(k) for k in send_data))

        send_times_cnt = 0
        send = [0x05, 0xF0, 0x00, 0x00, 0x00, 0x00, 0x05, 0x0d]

        if send_times_high >= 1:
            # print('send_times_high')
            for i in range(0,send_times_high):
                send[2:6] = send_data[i*4:i*4+4]
                self.sendData(self.__dev.PDO1_Rx, node_id, send)
                # time.sleep(0.002)
                # print(i)
                # print('     %s' % " ".join(hex(k) for k in send))
                send_times_cnt = i + 1

        # print(send_times_cnt)
        send = [0x05, 0xF0, 0x00, 0x00, 0x00, 0x00, 0x05, 0x0d]
        if (send_times_low >= 1):
            # print('send_times_low')
            send[2:2+send_times_low] = send_data[(send_times_cnt)*4:(send_times_cnt)*4+send_times_low]
            self.sendData(self.__dev.PDO1_Rx, node_id, send)
            # print('     %s' % " ".join(hex(k) for k in send))

        send = [0x05, 0xF1, len(send_data), 0x02, 0x00, 0x00, 0x09, 0x0d]
        self.sendData(self.__dev.PDO1_Rx, node_id, send)

        receiveCanData = self.getRevData(0x01, node_id, 1000)

        if len(receiveCanData) <= 0:  # time_out
            print('sendFpgaUpgradePack time_out node_id=0x%02X' % node_id)
            print('     receive from 0x%02X FPGA: %s' % (node_id , " ".join(hex(k) for k in receiveCanData)))
        else:
            # print('     receive from 0x%02X FPGA: %s' % (node_id , " ".join(hex(k) for k in receiveCanData)))
            pass

        return receiveCanData

    def cmdEraseMemory(self, node_id, sectors = None):
        data = [0x44, 0xbb, 0xff, 0xff, 0x00]
        receiveCanData = self.sendUsbPdData(node_id, data)

        if len(receiveCanData) <= 0:  # time_out
            print('sendFpgaUpgradePack time_out node_id=0x%02X' % node_id)
            print('     receive from 0x%02X FPGA: %s' % (node_id , " ".join(hex(k) for k in receiveCanData)))
        else:
            print('     receive from 0x%02X FPGA: %s' % (node_id , " ".join(hex(k) for k in receiveCanData)))

        return receiveCanData

    def cmdWriteMemory(self, node_id, addr, data):
        # assert(len(data) <= 128)

        send_data = [0x31, 0x31 ^ 0xff]
        receiveCanData = self.sendUsbPdData(node_id, send_data)

        if len(receiveCanData) <= 0:  # time_out
            print('sendFpgaUpgradePack time_out node_id=0x%02X' % node_id)
            print('     receive from 0x%02X FPGA: %s' % (node_id , " ".join(hex(k) for k in receiveCanData)))
        else:
            # print('     receive from 0x%02X FPGA: %s' % (node_id , " ".join(hex(k) for k in receiveCanData)))
            pass

        byte3 = (addr >> 0) & 0xFF
        byte2 = (addr >> 8) & 0xFF
        byte1 = (addr >> 16) & 0xFF
        byte0 = (addr >> 24) & 0xFF
        crc = byte0 ^ byte1 ^ byte2 ^ byte3

        send_data = [byte0, byte1, byte2, byte3, crc]
        receiveCanData = self.sendUsbPdData(node_id, send_data)

        if len(receiveCanData) <= 0:  # time_out
            print('sendFpgaUpgradePack time_out node_id=0x%02X' % node_id)
            print('     receive from 0x%02X FPGA: %s' % (node_id , " ".join(hex(k) for k in receiveCanData)))
        else:
            # print('     receive from 0x%02X FPGA: %s' % (node_id , " ".join(hex(k) for k in receiveCanData)))
            pass

        send_data = [len(data)-1] + data

        crc = 0x00
        for c in send_data:
            crc = crc ^ c
        send_data.append(crc)
        receiveCanData = self.sendUsbPdData(node_id, send_data)

        if len(receiveCanData) <= 0:  # time_out
            print('sendFpgaUpgradePack time_out node_id=0x%02X' % node_id)
            print('     receive from 0x%02X FPGA: %s' % (node_id , " ".join(hex(k) for k in receiveCanData)))
        else:
            # print('     receive from 0x%02X FPGA: %s' % (node_id , " ".join(hex(k) for k in receiveCanData)))
            pass

        return receiveCanData


    def sendBinFile(self, file_name, send_file_state, node_id_need_program):
        if send_file_state == 0: # 初始化变量，升级中只执行一次
            send_file_state = 1

        if send_file_state == 1:
            packetLen = 128
            packetNum = (self.size + packetLen - 1) // packetLen
            current_pos = 0
            # packetIndex = 0xb36
            # current_pos = 1484513
            current_packerLen = 0
            MAX_TRY_TIMES = 20

            addr = 0x8000000
            while (current_pos < self.size):

                if self.size <= (current_pos + packetLen):
                    current_packerLen = self.size - current_pos
                    packed_timeout = 300
                else:
                    current_packerLen = packetLen

                send_data = list(self.f_bin_data[current_pos:current_pos+current_packerLen])

                for node_id in node_id_need_program:
                    try_times = 0
                    while try_times < MAX_TRY_TIMES:
                        # print(hex(addr))
                        # print('current_pos = %d' % current_pos)
                        revData = self.cmdWriteMemory(node_id, addr, send_data)
                        # time.sleep(0.002)
                        # print(type(revData))
                        if len(revData) >= 0x01 and revData[0] == 0x79:
                            addr += 0x80
                            break
                        # elif len(revData) >= 0x01 and revData[0] == 0x1f:
                            # pass
                            # return 1
                        else:
                            print('current_pos = %d' % current_pos)
                            # return 1

                        try_times = try_times + 1

                    if try_times > MAX_TRY_TIMES:
                        self.message_singel.emit('try_times = %d \r\n' % (try_times))
                        print('try_times = %d' % (try_times))
                        try_times = 0
                        return 1
                        # break

                current_pos = current_pos + current_packerLen
                # print('current_pos = %d' % current_pos)
                self.processBar_singel.emit((current_pos/self.size)*100)

            if current_pos < self.size:
                self.message_singel.emit('升级失败! \r\n')
                print('升级失败')
            else:
                # self.message_singel.emit('升级成功! \r\n')
                # print('升级成功')
                pass

            send_file_state = 2

        elif send_file_state == 2:
            send_file_state = 3

        elif send_file_state == 3:
            send_file_state = 0

        return send_file_state

    def TimeStampToTime(self, timestamp):
        timeStruct = time.localtime(timestamp)
        return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)



