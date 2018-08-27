
#
# -*- coding: utf-8 -*-

"""
In this example, we create a simple window in PyQt5.

author: chenzhipeng3472
last edited: 04-July-2018
"""
__author__ = 'chenzhipeng3472'

import os
import sys
sys.path.append(os.getcwd())

import time

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

CAN_HEAD = int(0xAA)
CAN_CTRL = int(0xA5)
CAN_TAIL = int(0x55)
PACK_SIZE = int(1024)
READ_SIZE = int(8)

E_UPG_CMD_ERASE     = int(0x01)
E_UPG_CMD_DATA      = int(0x02)
E_UPG_CMD_PROGRAM   = int(0x03)
E_UPG_CMD_REBOOT    = int(0x04)

E_CMD_RESER         = int(0x01)
E_CMD_UPDATE        = int(0x02)

class UpgradeMCU(QThread):
    '''
    '''
    #定义一个信号
    processBar_singel = pyqtSignal(int)
    message_singel = pyqtSignal(str)

    def __init__(self):
        super(UpgradeMCU, self).__init__()
        self.Download_state = DOWNLOAD_STATE.INITIALIZE.value
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
            print(" ".join(hex(i) for i in node_idx_need_program))
            for node_id in node_idx_need_program:
                print('reset iwdg: node_id=%d' % (node_id))
                self.send_reset_iwdg_command(node_id)
                self.message_singel.emit('发送重启指令：节点：' + str(hex(node_id)) + ' \r\n')
                receive_data = self.getRevData(0x07, node_id, 20000)
                if len(receive_data) :
                    print("重启成功 节点 --> 0x%02X" % (receive_data[0][2]))
                    self.message_singel.emit('重启成功 --> ' + str(hex(receive_data[0][2])) + ' \r\n')

                    self.__dev.sendStartCmd(node_id) #------- 发送启动命令
                    QThread.msleep(1)

                    self.send_erase_commane(node_id) #------- 发送擦除扇区命令
                    QThread.msleep(1)

                else:
                    print('iwdg reset err!!!!!')

            QThread.sleep(2)
            self.Download_state = DOWNLOAD_STATE.SEND_FILE.value
            self.send_file_ret = 1
            self.send_file_tell = -1

            pass

        elif self.Download_state == DOWNLOAD_STATE.SEND_FILE.value: #send file
            self.send_file_tell, self.send_file_ret = self.send_file_data(file_name, self.send_file_ret, self.send_file_tell, node_idx_need_program)
            if self.send_file_ret == 0 :
                self.Download_state = DOWNLOAD_STATE.REBOOT.value
            # break;
            pass

        elif self.Download_state == DOWNLOAD_STATE.REBOOT.value: #----start--- 发送重启命令
            self.send_command_reboot(node_idx_need_program)
            self.message_singel.emit('检查是否升级成功，请稍后...  \r\n')
            receive_data = self.getRevData(0x07, 0, 20000)
            try:
                if len(receive_data) and receive_data[0][2] in node_idx_need_program:
                    self.message_singel.emit('升级成功 --> ' + str(hex(receive_data[0][2])) + ' \r\n')
                    node_idx_need_program.remove(receive_data[0][2])
                else:
                    print('reboot err!!')
                    print(" ".join(hex(k) for k in receive_data[0]))
            except Exception as err:
                print(err)

            self.Download_state = DOWNLOAD_STATE.FINISH_UPGRADE.value
            pass

        elif self.Download_state == DOWNLOAD_STATE.FINISH_UPGRADE.value: #----完成烧录---
            isDownloadFinish = True
            self.Download_state = DOWNLOAD_STATE.ENTER_UPGRADE.value
            print(self.Download_state)
            pass

        return isDownloadFinish

    def send_reset_iwdg_command(self, node_id):
        send = [ 0x99, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, E_CMD_RESER ]
        self.sendData(self.__dev.PDO1_Rx, node_id, send)
        print("发送重启指令：节点： 0x%02X " % (node_id))

    def send_erase_commane(self, node_id):
        send = [ E_UPG_CMD_ERASE, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, E_CMD_UPDATE ]
        self.sendData(self.__dev.PDO1_Rx, node_id, send)
        print("send_erase_commane...  node_id = 0x%02X " % (node_id))

    def send_data_command(self, node_ids):
        send = [ E_UPG_CMD_DATA, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, E_CMD_UPDATE ]
        for node_id in node_ids:
            self.sendData(self.__dev.PDO1_Rx, node_id, send)

    def send_1K_bin_data(self, f_bin, node_ids):
        check_sum_1K = int()
        for i in range(0, PACK_SIZE//READ_SIZE):
            f_bin_data = f_bin.read(READ_SIZE)
            # byte = ord(f_bin_data)
            # print( hex(byte))
            f_bin_data = list(f_bin_data)

            for node_id in node_ids:
                self.sendData(self.__dev.PDO2_Rx, node_id, f_bin_data)

            check_sum_1K += sum(f_bin_data)
        return check_sum_1K

    def send_program_command(self, check_sum, node_ids):
        send = [
                    E_UPG_CMD_PROGRAM,
                    (check_sum>>0)&0xff,
                    (check_sum>>8)&0xff,
                    (check_sum>>16)&0xff,
                    (check_sum>>24)&0xff,
                    0x00,
                    0x00,
                    0x02
                ]
        for node_id in node_ids:
            self.sendData(self.__dev.PDO1_Rx, node_id, send)

    def send_command_reboot(self, node_ids):
        send = [ E_UPG_CMD_REBOOT, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, E_CMD_UPDATE ]
        for node_id in node_ids:
            self.sendData(self.__dev.PDO1_Rx, node_id, send)
            print("send_command_reboot...  node_id = 0x%02X " % (node_id))

    def send_file_data(self, file_name, send_file_state, send_tell, node_id_need_program):
        print('%s, tell=%d' % (file_name, send_tell))

        if send_tell == -1 and send_file_state == 0:
            send_file_state = 1

        if send_file_state == 1:
            Is_File_exist = int(0)
            while Is_File_exist == 0:
                Is_File_exist = os.path.exists(file_name)
                if Is_File_exist:
                    self.size = os.path.getsize(file_name)
                    creat_time = os.path.getmtime(file_name)
                    print('')
                    print("%s  %s  %d bytes" % (file_name, self.TimeStampToTime(creat_time), self.size))
                    print('正在升级...  ',  end='')
                    print(" ".join(hex(i) for i in node_id_need_program))
                    self.message_singel.emit('找到文件，正在升级 ' + file_name + '  Version: ' + self.TimeStampToTime(creat_time) + ' ... \r\n')
                else:
                    print("找不到该文件  %s , 请放置该文件到该目录下,放置后请按回车键确认" % (file_name))
                    self.message_singel.emit('找不到该文件  %s , 请放置该文件到bin目录下,\r\n' % (file_name))
                    print('当前工作路径为：%s ' % (os.getcwd()))
                    os.chdir(".//bin")  # 如果找不到bin文件路径就切换到当前目录下找到bin文件夹
                    print('切换后工作路径为：%s ' % (os.getcwd()))

        # # print("size_high %d, size_low %d, size_low_8_high %d  , size_low_8_low %d " % (size_high, size_low, size_low_8_high, size_low_8_low))

            send_file_ret = 1
            send_file_state = 2
            self.old_tell = 0
            send_tell = 0

        elif send_file_state == 2:
            self.size = os.path.getsize(file_name)
            if send_tell >= self.size:
                print('size=%d' % (self.size))
                return send_tell,0

            size_high = self.size//PACK_SIZE  # 1K的倍数
            size_low = self.size%PACK_SIZE   # 1K的余数
            size_low_8_high = size_low//READ_SIZE                  # 1K的余数 ， 8字节的倍数
            size_low_8_low = size_low%READ_SIZE                # 1K的余数 ， 8字节的余数
        #----start--- 打开文件串口发送操作
            with open(file_name, 'rb') as f_bin:

                # print('send_file_data ...1')
                f_bin.seek(send_tell)
                send_cnt = send_tell//PACK_SIZE
                if send_cnt < (size_high+1):
                # while self.send_cnt < (size_high+1):
                # for (send_cnt) in  range(size_high+1):
                #----start--- 发送装载数据命令
                    # print('send_file_data ...2')
                    self.send_data_command(node_id_need_program)
                #----end-----

                    if(send_cnt == size_high):                                 #最后1K字节发送
                        # print("this is size_sigh = %d " % (size_high))
                        check_sum_1K = int()
                        for i in range(0, PACK_SIZE//READ_SIZE):
                            if (i < size_low_8_high):
                                f_bin_data = f_bin.read(READ_SIZE)
                                f_bin_data = list(f_bin_data)
                            elif (i == size_low_8_high):                                   #bin文件最后8个字节，
                                f_bin_data = f_bin.read(size_low_8_low)
                                f_bin_data = list(f_bin_data)

                                for j in range(size_low_8_low, READ_SIZE):
                                    f_bin_data.append(0xFF)

                            else :
                                f_bin_data = [0xff]*READ_SIZE


                            for node_id in node_id_need_program:
                                self.sendData(self.__dev.PDO2_Rx, node_id, f_bin_data)
                            check_sum_1K += sum(f_bin_data)
                            send_file_state = 3
                            # send_file_ret = 1
                    else:
                    #----start--- 发送1K数据
                        # print('send_file_data ...3')
                        check_sum_1K = self.send_1K_bin_data(f_bin, node_id_need_program)
                        # send_file_ret = 1
                        # print(hex(check_sum_1K))
                    #----end---

                    self.processBar_singel.emit((f_bin.tell()/self.size)*100)

                    if f_bin.tell() >= self.size:
                        self.message_singel.emit(file_name + ' -> ' + str(round(f_bin.tell()/self.size*100, 1)) + '% \r\n')

                    self.old_tell = f_bin.tell()
                    send_tell = f_bin.tell()

                #----start--- 发送烧录命令
                    self.send_program_command(check_sum_1K, node_id_need_program)
                #----end-----
                    QThread.msleep(80)


        elif send_file_state == 3:
            send_file_state = 0
            # send_file_ret = 0
            send_tell = 0

        return send_tell, send_file_state

    def findVersion(self, data):
        from ProgramUpdate import DIGITAL_VIDEO_BOARD, LVDS_IN_BOARD, ANALOG_VIDEO_BOARD
        version_mcu = ''
        version_fpga = ''
        if len(data) == 2:
            pass
        else:
            print('version length error!!! len = %d' % len(data))
            return 'Boot', 'Boot'

        if data[1][1] == DIGITAL_VIDEO_BOARD or data[1][1] == LVDS_IN_BOARD or data[1][1] == ANALOG_VIDEO_BOARD:
            year2 = ((data[1][2] >> 2)&0x3f)
            month2 = (((data[1][2]<<2)&0x0c) | ((data[1][3]>>6)&0x03))&0x0f
            day2 = (data[1][3]>>1)&0x1f

            year = ((data[1][4] >> 2)&0x3f)
            month = (((data[1][4]<<2)&0x0c) | ((data[1][5]>>6)&0x03))&0x0f
            day = (data[1][5]>>1)&0x1f

            version_fpga = str(year2)+'_'+str(month2)+'_'+str(day2)

        else:
            year = ((data[1][2] >> 2)&0x3f)
            month = (((data[1][2]<<2)&0x0c) | ((data[1][3]>>6)&0x03))&0x0f
            day = (data[1][3]>>1)&0x1f
            hour = ((data[1][3]<<4)&0x10) | data[1][4]>>4
            minute = ((data[1][4]&0x0f)<<2) | ((data[1][5]>>6)&0x0f)

        version_mcu = str(year)+'_'+str(month)+'_'+str(day)

        return version_mcu, version_fpga

    def TimeStampToTime(self, timestamp):
        timeStruct = time.localtime(timestamp)
        return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)

if __name__ == "__main__":
    '''
    main
    '''
    pass

