
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
import binascii
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

@unique       #如果要限制定义枚举时，不能定义相同值的成员。可以使用装饰器@unique【要导入unique模块】
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

class UpgradeLVDS(QThread):
    '''
    UpgradeLVDS
    '''
    #定义一个信号
    processBar_singel = pyqtSignal(int)
    message_singel = pyqtSignal(str)

    def __init__(self):
        super(UpgradeLVDS, self).__init__()
        self.Download_state = DOWNLOAD_STATE.INITIALIZE.value
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
            if dat[0] == node_id and dat[2] >= dat[3]: # 这里取值逻辑与MCU储存逻辑相反，可能由于大小端模式影响，待确认
                receive_data.append(dat[4])
                receive_data.append(dat[5])
                receive_data.append(dat[6])
                receive_data.append(dat[7])

        return receive_data

    def downloadProcess(self, startAddr, file_name, node_idx_need_program):

        isDownloadFinish = False

        if self.Download_state == DOWNLOAD_STATE.INITIALIZE.value: #---- 初始化数据---
            print('下载程序...')
            print('into LVDS FPGA bootloader...')
            print('addr=0x%6X, file=%s' % (startAddr, file_name))
            self.Download_state = DOWNLOAD_STATE.ENTER_UPGRADE.value
            pass

        elif self.Download_state == DOWNLOAD_STATE.ENTER_UPGRADE.value: #---- 复位看门狗---
            for node_id in node_idx_need_program:
                # send_data = [0xF0] #查询版本
                send_data = [0x28] # into bootloader
                self.sendFpgaUpgradePack(node_id, send_data)
                revData = self.sendFpgaUpgradePack(node_id, send_data)
                # revDataStr = bytes(revData)
                # print(revDataStr.decode())

                send_data = [0x05, 0x08] # into isp model
                revData = self.sendFpgaUpgradePack(node_id, send_data)
                if len(revData) > 3 and revData[3] == 0x05 and revData[4] == 0x09 and revData[5] == 0x01:
                    print('into ISP model...')

                Is_File_exist = int(0)
                while Is_File_exist == 0:
                    Is_File_exist = os.path.exists(file_name)
                    if Is_File_exist:
                        self.size = os.path.getsize(file_name)
                        creat_time = os.path.getmtime(file_name)
                        print('')
                        print("%s  %s  %d bytes" % (file_name, self.TimeStampToTime(creat_time), self.size))
                        print('正在升级...  ',  end='')
                        self.message_singel.emit('找到文件，正在升级 ' + file_name + '  Version: ' + self.TimeStampToTime(creat_time) + ' ... \r\n')
                    else:
                        print("找不到该文件  %s , 请放置该文件到该目录下,放置后自动开始下载" % (file_name))
                        self.message_singel.emit('找不到该文件  %s , 请放置该文件到bin目录下,\r\n' % (file_name))
                        time.sleep(3)

                with open(file_name, 'rb') as f_bin:
                    print(self.size)
                    self.f_bin_data = f_bin.read(self.size)
                    fileCrc = binascii.crc32(self.f_bin_data)
                    print(fileCrc)
                send_data = [0x05, FPGA_CMD.START_UPGRADE.value, 0x00,
                            0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00
                            ]
                send_data[3] = (fileCrc>>24)&0xff
                send_data[4] = (fileCrc>>16)&0xff
                send_data[5] = (fileCrc>>8)&0xff
                send_data[6] = (fileCrc)&0xff
                send_data[7] = (self.size>>24)&0xff
                send_data[8] = (self.size>>16)&0xff
                send_data[9] = (self.size>>8)&0xff
                send_data[10] = (self.size)&0xff
                send_data[11] = (startAddr>>24)&0xff
                send_data[12] = (startAddr>>16)&0xff
                send_data[13] = (startAddr>>8)&0xff
                send_data[14] = (startAddr)&0xff
                # print(" ".join(hex(k) for k in send_data))

                reboot_time = time.time()
                revData = self.sendFpgaUpgradePack(node_id, send_data)
                while True:
                    while (time.time() - reboot_time) > 3:
                        revData = self.sendFpgaUpgradePack(node_id, send_data)
                        reboot_time = time.time()
                    if len(revData) > 0x0b and revData[3] == 0x05 and revData[4] == FPGA_CMD.ACK.value and revData[5] == 0x00:
                        print('into upgrade model...')
                        break

                self.send_file_ret = 1
                self.send_file_tell = -1

            self.Download_state = DOWNLOAD_STATE.SEND_FILE.value

        elif self.Download_state == DOWNLOAD_STATE.SEND_FILE.value: #send file
            self.send_file_ret = self.sendFpgaFile(file_name, self.send_file_ret, node_idx_need_program)
            self.Download_state = DOWNLOAD_STATE.REBOOT.value

        elif self.Download_state == DOWNLOAD_STATE.REBOOT.value: #----start--- 发送重启命令
            node_idx_need_program.pop()
            self.Download_state = DOWNLOAD_STATE.FINISH_UPGRADE.value

        elif self.Download_state == DOWNLOAD_STATE.FINISH_UPGRADE.value: #----完成烧录---
            isDownloadFinish = True
            self.Download_state = DOWNLOAD_STATE.ENTER_UPGRADE.value

        return isDownloadFinish


    def sendFpgaUpgradePack(self, node_id, dat):
        send_data = [0xFF, 0x33, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        send_data[2] = len(dat) +4
        check_sum = send_data[2]+sum(dat)
        send_data = send_data[:3] + list(dat)
        send_data.append(0x100 - (check_sum)&0xff)


        send_times_high = len(send_data)//7
        send_times_low = len(send_data)%7
        # print(send_times_high)
        # print(send_times_low)

        # print('sendFpgaUpgradePack: %s' % " ".join(hex(k) for k in send_data))

        send_times_cnt = 0
        send = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02]

        if send_times_high >= 1:
            # print('send_times_high')
            for i in range(0,send_times_high):
                send[:7] = send_data[i*7:i*7+7]
                self.sendData(self.__dev.PDO1_Rx, node_id, send)
                # time.sleep(0.002)
                # print(i)
                # print('     %s' % " ".join(hex(k) for k in send))
                send_times_cnt = i + 1

        # print(send_times_cnt)
        send = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02]
        if (send_times_low >= 1):
            # print('send_times_low')
            send[:send_times_low] = send_data[(send_times_cnt)*7:(send_times_cnt)*7+send_times_low]
            self.sendData(self.__dev.PDO1_Rx, node_id, send)
            # print('     %s' % " ".join(hex(k) for k in send))

        receiveCanData = self.getRevData(0x01, node_id, 1000)

        if len(receiveCanData) <= 0:  # time_out
            print('sendFpgaUpgradePack time_out node_id=0x%02X' % node_id)
            print('sendFpgaUpgradePack: %s' % " ".join(hex(k) for k in send_data))
            print('     receive from 0x%02X FPGA: %s' % (node_id , " ".join(hex(k) for k in receiveCanData)))
        else:
            # print('     receive from 0x%02X FPGA: %s' % (node_id , " ".join(hex(k) for k in receiveCanData)))
            pass

        return receiveCanData

    def sendFpgaFile(self, file_name, send_file_state, node_id_need_program):

        if send_file_state == 0: # 初始化变量，升级中只执行一次
            send_file_state = 1

        if send_file_state == 1:
            packetLen = 230
            packetNum = (self.size + packetLen - 1) // packetLen
            packetIndex = 0
            current_pos = 0
            # packetIndex = 0xb36
            # current_pos = 1484513
            current_packerLen = 0
            MAX_TRY_TIMES = 20

            while (current_pos < self.size):
                zero_count = 0

                for k in range(current_pos, self.size):
                    if self.f_bin_data[k] == 0:
                        zero_count = zero_count + 1
                    else:
                        break

                    if zero_count > 65500:
                        zero_count = 65500
                        break

                current_pos = k

                if self.size <= (current_pos + packetLen):
                    current_packerLen = self.size - current_pos
                    packed_timeout = 300
                else:
                    current_packerLen = packetLen

                send_data = [0x05, FPGA_CMD.SEND_DATA.value, 0x00,
                            0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00
                            ]
                send_data[2] = (packetIndex>>24)&0xff
                send_data[3] = (packetIndex>>16)&0xff
                send_data[4] = (packetIndex>>8)&0xff
                send_data[5] = (packetIndex)&0xff
                send_data[6] = (packetNum>>24)&0xff
                send_data[7] = (packetNum>>16)&0xff
                send_data[8] = (packetNum>>8)&0xff
                send_data[9] = (packetNum)&0xff
                send_data[10] = (zero_count>>8)&0xff
                send_data[11] = (zero_count)&0xff

                send_data = send_data[:12] + list(self.f_bin_data[current_pos:current_pos+current_packerLen])

                for node_id in node_id_need_program:
                    try_times = 0
                    while try_times < MAX_TRY_TIMES:
                        revData = self.sendFpgaUpgradePack(node_id, send_data)
                        if len(revData) >= 0x0A and len(revData) <= 0x0C and revData[3] == 0x05 and revData[4] == 0x01:
                            packetIndex2 = revData[7]<<24 | revData[8]<<16 | revData[9]<<8 | revData[10]
                            if  revData[6] == FPGA_CMD.SEND_DATA.value and packetIndex2 == packetIndex:
                                break

                        elif len(revData) >= 0x04 and len(revData) <= 0x08:
                            if len(revData) == 0x04:
                                if revData[0] != 0x05:
                                    continue

                            for i, rev_dat in enumerate(revData):
                                if revData[i] == 0x05 and revData[i+1] == FPGA_CMD.RET_CRC.value:
                                    if 1 == revData[i+2]:
                                        self.message_singel.emit('升级成功! \r\n')
                                        print('升级成功')
                                    else:
                                        self.message_singel.emit('CRC 校验错误! \r\n')
                                        print('CRC 校验错误')
                                    break
                            print(i)
                            if i < 0x04:
                                break
                        else:
                            print('current_pos = %d' % current_pos)

                        try_times = try_times + 1

                    if try_times > MAX_TRY_TIMES:
                        self.message_singel.emit('try_times = %d \r\n' % (try_times))
                        print('try_times = %d' % (try_times))
                        try_times = 0
                        break

                packetIndex = packetIndex + 1
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
        return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)




