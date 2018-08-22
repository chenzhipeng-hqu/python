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
import time
import serial
import binascii
import threading
import serial.tools.list_ports
from enum import Enum, unique
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QCheckBox)
from PyQt5.QtCore import (pyqtSignal, QTimer, QThread, QTime)
from PyQt5 import QtCore, QtGui

import UI_ProgramUpdate
# import CANalystDriver
from CANalystDriver import *


DEBUG = int(0)

CAN_HEAD = int(0xAA)
CAN_CTRL = int(0xA5)
CAN_TAIL = int(0x55)
PACK_SIZE = int(1024)
READ_SIZE = int(8)

FILE_NAME_PCIE_BASE     = str('..//bin//PcieBaseBoard.bin')
FILE_NAME_DIGITAL_VIDEO = str('..//bin//DigitalVideo.bin')
FILE_NAME_ANALOG_VIDEO  = str('..//bin//AnalogVideo.bin')
FILE_NAME_LVDS_IN       = str('..//bin//LVDSIn.bin')
FILE_NAME_DIGITAL_IO    = str('..//bin//IoBoardDigital.bin')
FILE_NAME_ANALOG_IO     = str('..//bin//IoBoardAnalog.bin')
FILE_NAME_POWER         = str('..//bin//PowerBoard.bin')
FILE_NAME_AUDIO         = str('..//bin//AudioBoard.bin')
FILE_NAME_ANALOG_FPGA   = str('..//bin//AnalogFPGA.mcs')
FILE_NAME_DIGITAL_FPGA  = str('..//bin//DigitalFPGA.mcs')
FILE_NAME_LVDS_LVDS_FPGA     = str('..//bin//lvds_ddr.bin')
FILE_NAME_LVDS_N10_FPGA     = str('..//bin//N10.bin')
FILE_NAME_LVDS_N86_1_FPGA     = str('..//bin//N86_1.bin')
FILE_NAME_LVDS_N81_FPGA     = str('..//bin//N81.bin')
FILE_NAME_LVDS_PT320_FPGA     = str('..//bin//PT320.bin')
FILE_NAME_LVDS_N86_2_FPGA     = str('..//bin//N86_2.bin')
FILE_NAME_LVDS_PT320_2_FPGA     = str('..//bin//PT320_2.bin')
FILE_NAME_LVDS_N10_2_FPGA     = str('..//bin//N10_2.bin')
FILE_NAME_LVDS_BOOT_FPGA     = str('..//bin//boot_test.bin')

E_UPG_CMD_ERASE     = int(0x01)
E_UPG_CMD_DATA      = int(0x02)
E_UPG_CMD_PROGRAM   = int(0x03)
E_UPG_CMD_REBOOT    = int(0x04)

E_CMD_RESER         = int(0x01)
E_CMD_UPDATE        = int(0x02)

POWER_BOARD         = int(0x02)
IO_ANALOG_BOARD     = int(0x04)
AUDIO_BOARD         = int(0x05)
IO_DIGITAL_BOARD    = int(0x06)
ANALOG_VIDEO_BOARD  = int(0x07)
DIGITAL_VIDEO_BOARD = int(0x08)
LVDS_IN_BOARD       = int(0x09)
PCIE_BASE_BOARD     = int(0x0a)
ANALOG_FPGA_BOARD   = int(0x07)
DIGITAL_FPGA_BOARD  = int(0x08)
LVDS_FPGA_BOARD     = int(0x09)

USE_UART = 0
USE_CANALYST_II = 1
CAN_DRIVER = USE_UART

nowTime = lambda:int(round(time.time()*1000))

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


class UI_MainWindow(UI_ProgramUpdate.Ui_Form, QWidget):
    '''
    直接继承界面类
    '''
    def __init__(self):
        super(UI_MainWindow,self).__init__()

        self.setupUi(self)

        # self.GroupBox.resize(self.GroupBox.sizeHint())
        # self.MainWindow.resize(self.MainWindow.sizeHint())

        #----initialize----QThread 任务
        self.ProgramUpdate_thread = ProgramUpdateThread()
        self.ProgramUpdate_thread.start()
        #----end---- 

        self.initUI()

    def initUI(self):

        self.NodeID_button =list()
        self.BoxID_checkBox =list()
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(85, 85, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        for i in range(8):
            for j in range(11):
                self.NodeID_button.append(QPushButton(self.gridLayoutWidget_2))
                self.NodeID_button[i*11+j].setEnabled(False)
                self.NodeID_button[i*11+j].setText("")
                self.NodeID_button[i*11+j].setCheckable(True)
                self.NodeID_button[i*11+j].setFlat(True)
                self.NodeID_button[i*11+j].setPalette(palette)
                self.NodeID_button[i*11+j].clicked[bool].connect(self.selectNodeID)
                self.gridLayout_3.addWidget(self.NodeID_button[i*11+j], j+2, i+1, 1, 1)

            self.BoxID_checkBox.append(QCheckBox('机箱 '+str(i), self.gridLayoutWidget_2))
            self.BoxID_checkBox[i].setEnabled(False)
            font = QtGui.QFont()
            font.setPointSize(11)
            font.setBold(True)
            font.setWeight(75)
            self.BoxID_checkBox[i].setFont(font)
            self.BoxID_checkBox[i].setFocusPolicy(QtCore.Qt.StrongFocus)
            self.BoxID_checkBox[i].setLayoutDirection(QtCore.Qt.LeftToRight)
            self.BoxID_checkBox[i].setChecked(False)
            self.BoxID_checkBox[i].setAutoRepeat(False)
            self.BoxID_checkBox[i].setTristate(False)
            # # self.BoxID_checkBox[i*8+j].clicked[bool].connect(self.selectNodeID)
            self.gridLayout_3.addWidget(self.BoxID_checkBox[i], 1, i+1, 1, 1)

        # DetectSerial
        self.ser_detect_button.clicked.connect(self.DetectSerial)
        self.ser_detect_button.setShortcut('F6')

        # message_singel
        self.ProgramUpdate_thread.message_singel.connect(self.message_singel)
        self.Msg_TextEdit.insertPlainText('欢迎使用，请选择串口。。。\r\n')
        textCursor = self.Msg_TextEdit.textCursor()
        textCursor.movePosition(textCursor.End)
        self.Msg_TextEdit.setTextCursor(textCursor)

        # openSerial
        self.ser_open_button.clicked.connect(self.openSerial)
        self.ser_open_button.setShortcut('F7')

        #refreshBoard
        self.BoardRefresh_button.clicked.connect(self.refreshBoard)
        self.BoardRefresh_button.setShortcut('F5')

        #refresh_singel
        self.ProgramUpdate_thread.refresh_singel.connect(self.refresh_singel)

        #processbar_singel
        self.ProgramUpdate_thread.processBar_singel.connect(self.processBar_singel)

        #download_process
        self.download_button.clicked.connect(self.download_process)
        self.download_button.setShortcut('F8')

        #allNodeID_checkBox
        self.allNodeID_checkBox.stateChanged.connect(self.download_select)

        #ctrl_220V_button
        self.ctrl_220V_button.clicked.connect(self.ctrl_220V)

        #Lvds_combobox
        self.Lvds_comboBox.currentIndexChanged.connect(self.lvds_select_addr)



    #Lvds_combobox
    def lvds_select_addr(self):
        source = self.sender()
        # print(source.currentIndex(), end=' ')
        # print(source.currentText())

        if source.currentText() == 'LVDS' or source.currentText() == 'NORMAL':
            self.ProgramUpdate_thread.lvdsStartAddr = 0x000000
        elif source.currentText() == 'N10':
            self.ProgramUpdate_thread.lvdsStartAddr = 0x170000
        elif source.currentText() == 'N86_1':
            self.ProgramUpdate_thread.lvdsStartAddr = 0x2e0000
        elif source.currentText() == 'N81':
            self.ProgramUpdate_thread.lvdsStartAddr = 0x450000
        elif source.currentText() == 'PT320':
            self.ProgramUpdate_thread.lvdsStartAddr = 0x5C0000
        elif source.currentText() == 'N86_2':
            self.ProgramUpdate_thread.lvdsStartAddr = 0x730000
        elif source.currentText() == 'PT320_2':
            self.ProgramUpdate_thread.lvdsStartAddr = 0x8A0000
        elif source.currentText() == 'EXT_2':
            self.ProgramUpdate_thread.lvdsStartAddr = 0xA10000
        elif source.currentText() == 'Bootloader':
            self.ProgramUpdate_thread.lvdsStartAddr = 0xB80000

        print(hex(self.ProgramUpdate_thread.lvdsStartAddr))

    #ctrl_220V
    def ctrl_220V(self, pressed):
        source = self.sender()
        # print(source.text())
        self.ProgramUpdate_thread.send_ctrl_220V_command(pressed)

    #allNodeID_checkBox
    def download_select(self, state):
        source = self.sender()
        # print(source.currentIndex(), end=' ')
        # print(source.text())
        # print(str(state))
        # print(source.currentIndexChanged())
        if state == 0:
       # if state == QtCore.Qt.UnChecked:
            self.ProgramUpdate_thread.downloadSelect(0)

        elif state == 2:
            self.ProgramUpdate_thread.downloadSelect(2)

    #selectNodeID 
    def selectNodeID(self, pressed):
        source = self.sender()
        self.ProgramUpdate_thread.selectNodeID(pressed, str(source.id_))

    def download_process(self):

        now_time = time.strftime("%H:%M:%S", time.localtime())
        self.timeEdit.setTime(QTime.fromString(now_time, 'hh:mm:ss'))
        print(now_time)
        source = self.sender()
        # print(dir(source))
        # print(self.Download_combo.currentText())
        self.ProgramUpdate_thread.download_process_flag = 1

    # DetectSerial
    def DetectSerial(self):
        source = self.sender()
        print(source)
        print(source.text())
        self.ser_com_combo.clear()
        plist = list(serial.tools.list_ports.comports())
        for i in range(0, len(plist)):
            print(plist[i])
            self.message_singel(str(plist[i])+'\r\n')
            self.ser_com_combo.addItem(str(plist[i].device))

    # openSerial
    def openSerial(self):
        source = self.sender()
        # print(source)
        if source.text() == '打开':
            ret = self.ProgramUpdate_thread.openSerial(str(self.ser_com_combo.currentText()))
            if ret == 0:
                source.setText('关闭')
                source.setChecked(True)
            else:
                source.setChecked(False)

        elif source.text() == '关闭':
            ret = self.ProgramUpdate_thread.closeSerial()
            if ret == 0:
                source.setText('打开')
                source.setChecked(False)
            else:
                source.setChecked(True)

    #BoardRefresh_button
    def refreshBoard(self):
        source = self.sender()
        # self.ProgramUpdate_thread.refreshBoard()
        self.ProgramUpdate_thread.refreshBoardFlag = 1

    #message_singel
    def message_singel(self, str):
        textCursor = self.Msg_TextEdit.textCursor()
        textCursor.movePosition(textCursor.End)
        self.Msg_TextEdit.setTextCursor(textCursor)
        self.Msg_TextEdit.insertPlainText(str)

    def processBar_singel(self, val):
        self.Progress_bar.setValue(val)

    #refresh_singel
    def refresh_singel(self, cmd, i, j, version ,is_down):
        if is_down == 2:
            is_down = True

        if cmd == 1:  # clear node_id
            self.NodeID_button[i*11+j].setText('    ')
            self.NodeID_button[i*11+j].setCheckable(False)
            self.NodeID_button[i*11+j].setEnabled(False)
            self.NodeID_button[i*11+j].setFlat(True)
            # self.NodeID_button[i*8+j].clicked[bool].connect(self.selectNodeID)
            # self.NodeID_button[i*8+j].clicked[bool].disconnect(self.selectNodeID)

        if cmd == 2:  # clear box_id
            # self.BoxID_button[i].setText('    ')
            self.BoxID_checkBox[i].setCheckable(False)
            self.BoxID_checkBox[i].setEnabled(False)
            pass

        if cmd == 3:  # set node_id
            # print('cmd=%d, i=0x%02X, j=%d' % (cmd, i, j))
            self.NodeID_button[(i>>4)*11+j].setFlat(False)
            self.NodeID_button[(i>>4)*11+j].setText(str(version))
            self.NodeID_button[(i>>4)*11+j].setCheckable(True)
            self.NodeID_button[(i>>4)*11+j].setChecked(is_down)
            self.NodeID_button[(i>>4)*11+j].setEnabled(True)
            if j >= 8 :
                self.NodeID_button[(i>>4)*11+j].id_ = i | 0x80   # 最高位置1 表示FPGA板
            else:
                self.NodeID_button[(i>>4)*11+j].id_ = i
            # self.NodeID_button[(i>>4)*8+j].clicked[bool].connect(self.selectNodeID)
            # self.BoardTypeUI.BoxID_button[(i>>4)].setText('Box '+str(i>>4))
            self.BoxID_checkBox[(i>>4)].setCheckable(True)
            self.BoxID_checkBox[(i>>4)].setEnabled(True)

'''
'''
class ProgramUpdateThread(QThread):
    #定义一个信号
    refresh_singel = pyqtSignal(int, int, int, str, int)
    processBar_singel = pyqtSignal(int)
    message_singel = pyqtSignal(str)

    def __init__(self):
        super(ProgramUpdateThread, self).__init__()
        self.ser = serial.Serial()  #/dev/ttyUSB0
        self.data_receive = ''
        self.wait_receive = int(1)
        self.can_cmd = list()
        # self.lvdsStartAddr = 0x000000
        self.lvdsStartAddr = 0x170000

        #node_id_list
        self.node_id_need_program = list()
        self.box_id_need_program = list()

        self.box_id_exist = list()
        self.node_id_all_exist = list()

            #seq, board_type, file_name, node_idx_exist, node_idx_need_program i
        self.AllNodeList = [\
            ( 0     , AUDIO_BOARD         , FILE_NAME_AUDIO           , list()    , list() ),\
            ( 1     , IO_ANALOG_BOARD     , FILE_NAME_ANALOG_IO       , list()    , list() ),\
            ( 2     , IO_DIGITAL_BOARD    , FILE_NAME_DIGITAL_IO      , list()    , list() ),\
            ( 3     , POWER_BOARD         , FILE_NAME_POWER           , list()    , list() ),\
            ( 4     , ANALOG_VIDEO_BOARD  , FILE_NAME_ANALOG_VIDEO    , list()    , list() ),\
            ( 5     , DIGITAL_VIDEO_BOARD , FILE_NAME_DIGITAL_VIDEO   , list()    , list() ),\
            ( 6     , LVDS_IN_BOARD       , FILE_NAME_LVDS_IN         , list()    , list() ),\
            ( 7     , PCIE_BASE_BOARD     , FILE_NAME_PCIE_BASE       , list()    , list() ),\
            ( 8     , ANALOG_FPGA_BOARD   , FILE_NAME_ANALOG_FPGA     , list()    , list() ),\
            ( 9     , DIGITAL_FPGA_BOARD  , FILE_NAME_DIGITAL_FPGA    , list()    , list() ),\
            ( 10    , LVDS_FPGA_BOARD     , FILE_NAME_LVDS_N10_FPGA   , list()    , list() )\
            ]


        #----initialize----QTimer 任务
        self.tick = int(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timeout_slot)
        self.timer.start(1)
        #----end---- 

        #----initialize----threading 任务
        self.thread_1 = threading.Thread(target=self.receive_data_thread) #建立一个线程，调用receive_data_thread方法，不带参数
        self.thread_1.setDaemon(True) #声明为守护线程，设置的话，子线程将和主线程一起运行，并且直接结束，不会再执行循环里面的子线程
        self.thread_1.start()
        # self.thread_1.join() #作用是执行完所有子线程才去执行主线程
        #----end---- 

        self.download_process_flag = 0
        self.download_select = 0
        self.refreshBoardFlag = 0
        self.send_file_state = int(1)
        self.Download_state = int(0)
        self.receive_can_data = list()

        #----can driver----
        if CAN_DRIVER == USE_UART:
            pass
        else:
            index = 0
            can_num = 0
            self.canDll = CANalystDriver(VCI_USBCAN2A, index, can_num)
            self.canDll.VCI_OpenDevice(0)
            initConfig = VCI_INIT_CONFIG()
            initConfig.AccCode = 0x80000008
            initConfig.AccMask = 0xFFFFFFFF
            initConfig.Reserved = 0
            initConfig.Filter = 0
            initConfig.Timing0 = 0x00
            initConfig.Timing1 = 0x14
            initConfig.Mode = 0
            self.canDll.VCI_InitCAN(ctypes.byref(initConfig))
            self.canDll.VCI_StartCAN()
            # self.canDll.thread_1.start()

            ubyte_array_8 = ctypes.c_ubyte * 8
            data = ubyte_array_8(1, 2, 3, 4, 5, 6, 7, 8)
            ubyte_array_3 = ctypes.c_ubyte * 3
            reserved = ubyte_array_3(0, 0, 0)

            vci_can_obj = VCI_CAN_OBJ(0x712, 0, 0, 1, 0, 0, 8, data, reserved)

            self.canDll.VCI_Transmit(ctypes.byref(vci_can_obj), 1)

    def run(self):
        while True:
            # print('tick2=%d ' % (self.tick))
            if self.refreshBoardFlag == 1:
                self.refreshBoard()
                if CAN_DRIVER == USE_UART:
                    pass
                else:
                    self.ser.close()

            if self.download_process_flag == 1:
                # self.download_process()
                self.download_process2()

            if self.data_receive != '':
                self.data_receive = self.find_can_command_format(self.data_receive)
                self.data_receive = ''

                # if len(self.can_cmd) > 0:
                i = int(0)
                self.lvds_rx_data = list()
                while i < len(self.can_cmd):
                    dat = self.can_cmd[i]
                    print(" ".join(hex(k) for k in dat))
                    if dat[3] == 0x02:  #PDO1（接收）
                        pass
                    elif dat[3] == 0x01: #PDO1（发送）
                        if dat[6] in self.AllNodeList[6][3]: # LVDS_IN_BOARD
                            if dat[8] >= dat[9]: # 这里取值逻辑与MCU储存逻辑相反，可能由于大小端模式影响，待确认
                                self.lvds_rx_data.append(dat[10])
                                self.lvds_rx_data.append(dat[11])
                                self.lvds_rx_data.append(dat[12])
                                self.lvds_rx_data.append(dat[13])
                        pass
                    elif dat[3] == 0x07 and dat[2] < 0x81:
                        print(' 0x%02X Boot up' % (dat[2]))
                    self.can_cmd.remove(dat)
                print(bytes(self.lvds_rx_data))


            QThread.msleep(1)

            pass

    def download_process2(self):
        if self.Download_state == 0: #---- 初始化数据---
            if  self.ser.isOpen() or CAN_DRIVER == USE_CANALYST_II:
                self.message_singel.emit('下载程序...\r\n')
                print('下载程序...')
                self.run_time = nowTime()
                self.Download_state = 1
                self.wait_receive = 0
            else:
                print('please select uart and open it!')
                self.message_singel.emit('请检查串口并选择节点！\r\n')
                self.download_process_flag = 0
                self.Download_state = 0
                return

        if self.Download_state == 1: #---- 复位看门狗---
            data = ''
            for seq, board_type, file_name, node_idx_exist, node_idx_need_program in self.AllNodeList:
                print('reset iwdg: seq=%d' % (seq))
                # print(id(node_idx_need_program))
                print(" ".join(hex(i) for i in node_idx_need_program))
                if seq <=7 and len(node_idx_need_program)>0:
                    print(" ".join(hex(i) for i in node_idx_need_program))

                    for node_id in node_idx_need_program:
                        self.send_reset_iwdg_command(node_id)
                        self.message_singel.emit('发送重启指令：节点：' + str(hex(node_id)) + ' \r\n')
                        data = ''
                        reboot_time = time.time()
                        while True:
                            while (time.time() - reboot_time) > 15:
                                self.send_reset_iwdg_command(node_id)
                                self.message_singel.emit('发送重启指令：节点：' + str(hex(node_id)) + ' \r\n')
                                reboot_time = time.time()

                            while self.ser.inWaiting() > 0:
                                reboot_time = time.time()
                                data = self.ser.read_all()
                                # print(data)
                            if data != '' and len(data) > 41 and data [2]< 0x90 and data[23] == node_id:
                                # print(" ".join(hex(i) for i in data))
                                print("重启成功 节点 --> 0x%02X" % (data[23]))
                                self.message_singel.emit('重启成功 --> ' + str(hex(data[23])) + ' \r\n')

                                self.send_start_command(self.ser, node_id) #------- 发送启动命令
                                QThread.msleep(1)
                                self.send_erase_commane(node_id) #------- 发送擦除扇区命令
                                QThread.msleep(1)
                                break;

                    self.send_file_ret = 1
                    QThread.sleep(2)
                    self.Download_state = 2
                    self.send_file_tell = -1
                    break
                elif seq <= 9 and len(node_idx_need_program)>0:
                    print('into Analog/Digital FPGA bootloader...')
                    blockNum = 0
                    if seq == 9:
                        boardType = 'digital'
                    elif seq == 8:
                        boardType = 'analog'

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
                            print("找不到该文件  %s , 请放置该文件到该目录下,放置后请按回车键确认" % (file_name))
                            self.message_singel.emit('找不到该文件  %s , 请放置该文件到bin目录下,\r\n' % (file_name))
                            print('当前工作路径为：%s ' % (os.getcwd()))
                            os.chdir(".//bin")  # 如果找不到bin文件路径就切换到当前目录下找到bin文件夹
                            print('切换后工作路径为：%s ' % (os.getcwd()))

                    with open(file_name, 'rb') as f_mcs:
                        for i, line in enumerate(f_mcs):
                            if line.__len__()>10  and ord('4') == line[8] and ord('0') == line[7]:
                                blockNum = blockNum + 1

                    send = 'enterUpgrade tvs200 %s bin %d\n' % (boardType, blockNum)
                    print(send)
                    for node_id in node_idx_need_program:
                        self.sendFpgaUpgradeCmd_AD(node_id, send)
                        receiveCanData = self.receiveCanCmdUart(node_id, 3)
                        receiveCanData = bytes(receiveCanData)
                        print(receiveCanData.decode())
                        if 'OK enterUpg 00 #A4\n' in receiveCanData.decode():
                            print('cmp OK! enterUpgrade model.')
                        else:
                            print('cmp ERR!')

                        self.size = os.path.getsize(file_name)

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
                            for i, line in enumerate(f_mcs):
                                if not isFileEnd:
                                    lineData = self.str2hex(line)
                                    if lineData[0]+5 != len(lineData):
                                        continue
                                        print('lineData err!!!!!!!')
                                        print(lineData)

                                    if lineData[3] == 0x04: #segment address
                                        # print(lineData)
                                        if length > 0:
                                            curBlock = curBlock + 1
                                            self.processBar_singel.emit((curBlock/blockNum)*100)
                                            # upgrade Section
                                            isSendFail = self.upgradeSection(node_id, addr, length, binSum, boardType, binData)
                                            totalLength = totalLength + length
                                            length = 0
                                            binSum = 0
                                            pass
                                        else:
                                            #file head, update UI
                                            self.processBar_singel.emit((curBlock/blockNum)*100)
                                            pass

                                        if lineData[0] == 0x02:
                                            addr = lineData[4]
                                            addr = (addr<<8) | lineData[5]
                                            addr <<= 16
                                        elif lineData[0] == 0x01:
                                            addr = lineData[4]
                                            addr <<= 16

                                        pass
                                    elif lineData[3] == 0x01: # end file
                                        if length > 0:
                                            curBlock = curBlock + 1
                                            # upgrade Section
                                            isSendFail = self.upgradeSection(node_id, addr, length, binSum, boardType, binData)
                                            self.processBar_singel.emit((curBlock/blockNum)*100)
                                            totalLength = totalLength + length
                                            length = 0
                                            binSum = 0

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
                    # upgrade
                    if not isSendFail:
                        send = 'upgrade %s %d \n' % (boardType, totalLength)
                        self.sendFpgaUpgradeCmd_AD(node_id, send)
                        print(send)

                        if CAN_DRIVER == USE_UART:
                            receiveCanData = self.receiveCanCmdUart(node_id, 20)
                        else:
                            receiveCanData = self.receiveCanCmdCanDevice(node_id, 20)

                        if len(receiveCanData) <= 0:  # time_out
                            print('sendFpgaUpgradePack time_out node_id=0x%02X' % node_id)
                        else:
                            receiveCanData = bytes(receiveCanData)
                            print(receiveCanData.decode())

                            if 'OK Upgrade finish!' in receiveCanData.decode():
                                print('升级成功\n')
                                self.message_singel.emit('升级成功 --> ' + str(hex(node_id)) + ' \r\n')
                            else:
                                isSendFail = True

                    if isSendFail:
                        self.message_singel.emit('升级失败 --> ' + str(hex(node_id)) + ' \r\n')
                        print('升级失败！！！！！！！\n')



                elif seq == 10 and len(node_idx_need_program)>0:
                    print('into LVDS FPGA bootloader...')
                    for node_id in node_idx_need_program:
                        # send_data = [0xF0] #查询版本
                        send_data = [0x28] # into bootloader
                        self.sendFpgaUpgradePack(node_id, send_data)

                        send_data = [0x05, 0x08] # into isp model
                        reboot_time = time.time()
                        revData = self.sendFpgaUpgradePack(node_id, send_data)
                        while True:
                            while (time.time() - reboot_time) > 3:
                                revData = self.sendFpgaUpgradePack(node_id, send_data)
                                reboot_time = time.time()
                            if len(revData) > 3 and revData[2] == 0x05 and revData[3] == 0x09 and revData[4] == 0x01:
                                print('into ISP model...')
                                break

                        # 发送bin文件crc校验/长度/起始地址
                        if self.lvdsStartAddr == 0x000000:
                            file_name = FILE_NAME_LVDS_LVDS_FPGA
                        elif self.lvdsStartAddr == 0x170000:
                            file_name = FILE_NAME_LVDS_N10_FPGA
                        elif self.lvdsStartAddr == 0x2e0000:
                            file_name = FILE_NAME_LVDS_N86_1_FPGA
                        elif self.lvdsStartAddr == 0x450000:
                            file_name = FILE_NAME_LVDS_N81_FPGA
                        elif self.lvdsStartAddr == 0x5C0000:
                            file_name = FILE_NAME_LVDS_PT320_FPGA
                        elif self.lvdsStartAddr == 0x730000:
                            file_name = FILE_NAME_LVDS_N86_2_FPGA
                        elif self.lvdsStartAddr == 0x8A0000:
                            file_name = FILE_NAME_LVDS_PT320_2_FPGA
                        elif self.lvdsStartAddr == 0xA10000:
                            file_name = FILE_NAME_LVDS_N10_2_FPGA
                        elif self.lvdsStartAddr == 0xBB0000:
                            file_name = FILE_NAME_LVDS_BOOT_FPGA

                        # self.AllNodeList[10][2] = str(file_name)
                        print('file=%s' % (file_name))
                        print('file=%s' % (self.AllNodeList[10][2]))

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
                                print("找不到该文件  %s , 请放置该文件到该目录下,放置后请按回车键确认" % (file_name))
                                self.message_singel.emit('找不到该文件  %s , 请放置该文件到bin目录下,\r\n' % (file_name))
                                print('当前工作路径为：%s ' % (os.getcwd()))
                                os.chdir(".//bin")  # 如果找不到bin文件路径就切换到当前目录下找到bin文件夹
                                print('切换后工作路径为：%s ' % (os.getcwd()))
                        with open(file_name, 'rb') as f_bin:
                            print(self.size)
                            self.f_bin_data = f_bin.read(self.size)
                            fileCrc = binascii.crc32(self.f_bin_data)
                            print(fileCrc)
                            print(type(fileCrc))
                        startAddr = self.lvdsStartAddr; # N10
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
                    self.Download_state = 2
                    self.send_file_tell = -1
                    break

                if seq == 10 and len(node_idx_need_program) <=0:
                    print('seq=%d' % (seq))
                    print('升级结束，请重启机箱，并确认各板卡绿灯全亮！iwdg reset')
                    self.message_singel.emit('升级用时 {}s \r\n'.format((nowTime()-self.run_time)/1000))
                    self.message_singel.emit('升级结束，请重启机箱，并刷新节点确认版本号！版本号正确即可。 \r\n')
                    self.Download_state = 0
                    self.download_process_flag = 0
                    self.wait_receive = 1



        elif self.Download_state == 2: #send file
            for seq, board_type, file_name, node_idx_exist, node_idx_need_program in self.AllNodeList:
                # print("1")
                if seq <=7 and len(node_idx_need_program)>0:
                    # print("2")
                    # print(" ".join(hex(i) for i in node_idx_need_program))
                    self.send_file_tell, self.send_file_ret = self.send_file_data(file_name, self.send_file_ret, self.send_file_tell, node_idx_need_program)
                    if self.send_file_ret == 0 :
                        self.Download_state = 3
                    break;
                elif seq == 10 and len(node_idx_need_program)>0:
                    print('send_FPGA_file_data')
                    self.send_file_ret = self.sendFpgaFile(file_name, self.send_file_ret, node_idx_need_program)
                    if self.send_file_ret == 0 :
                        self.Download_state = 3
                    break;
                # print('send_file_ret=%d' % (self.send_file_ret))

        elif self.Download_state == 3: #----start--- 发送重启命令
            data = ''
            for seq, board_type, file_name, node_idx_exist, node_idx_need_program in self.AllNodeList:
                print('reboot: seq=%d' % (seq))
                # print(id(node_idx_need_program))
                print(" ".join(hex(i) for i in node_idx_need_program))
                if seq <=7 and len(node_idx_need_program)>0:
                    self.send_command_reboot(node_idx_need_program)
                    reboot_time = time.time()
                    print('reboot_time=%d' % reboot_time)
                    self.message_singel.emit('检查是否升级成功，请稍后...  \r\n')
                    while (time.time() - reboot_time) < 20:
                        while self.ser.inWaiting() > 0:
                            data = self.ser.read_all()
                            QThread.msleep(1)
                            # print(data)
                        if data != '' and len(data) > 40 and data[2]< 0x90 and data[23] in node_idx_need_program:
                            print("升级成功 --> 0x%02X" % (data[23]))
                            self.message_singel.emit('升级成功 --> ' + str(hex(data[23])) + ' \r\n')
                            print(node_idx_need_program)
                            node_idx_need_program.remove(data[23])
                            print(node_idx_need_program)
                            data = ''
                            print(time.time() - reboot_time)
                            reboot_time = time.time()
                        if len(node_idx_need_program) <= 0:
                            QThread.sleep(5)
                            print('烧录 OK....')
                            if seq <= 7 :
                                self.Download_state = 1
                                return
                    if len(node_idx_need_program) > 0:
                        self.Download_state = 1
                        print('升级失败节点: %s' % " ".join(hex(i) for i in self.node_id_need_program))
                        self.message_singel.emit('---升级失败节点 --> ' )
                        for node_id in node_idx_need_program:
                            self.message_singel.emit(str(hex(node_id)) + ', ')
                        node_idx_need_program.clear()
                        self.message_singel.emit(' 请刷新节点，重新选择失败节点升级！！！ \r\n')
                        return


                    # self.Download_state = 1
                    # break
                elif seq == 10 and len(node_idx_need_program)>0:
                    print('reboot FPGA')
                    print('检查是否升级成功，请稍后...')
                    print("升级成功 --> ")
                    node_idx_need_program.pop(0)
                    if seq < 10 :
                        self.Download_state = 1
                        return

                    # if len(node_idx_need_program) <= 0:
                        # print('烧录 OK， 请关闭软件!....')
                        # QThread.sleep(1)
                        # break
                        # if seq < 7 and len(node_idx_need_program) <=0 and len(self.AllNodeList[seq+1][4])>0:
                            # self.Download_state = 1
                            # break
                if seq >= 10 and len(node_idx_need_program) <=0:
                    # print('download_process_flag=%d' % (self.download_process_flag))
                    print('升级结束，请重启机箱，并确认各板卡绿灯全亮！reboot')
                    self.message_singel.emit('升级用时 {}s \r\n'.format((nowTime()-self.run_time)/1000))
                    self.message_singel.emit('升级结束，请重启机箱，并刷新节点确认版本号！ ')
                    self.Download_state = 0
                    self.download_process_flag = 0
                    self.wait_receive = 1

                    # node_idx_need_program.clear()

    def upgradeSection(self, node_id, addr, length, binSum, boardType, binData):
        isSendFail = False
        send = 'loadBin %s %x %x %x ' % (boardType, addr, length, binSum&0x7fffffff)
        byteSum = 0;
        for dat_ in send:
            byteSum = byteSum + ord(dat_)
        send = send + ('%x\n' % (byteSum))
        self.sendFpgaUpgradeCmd_AD(node_id, send)
        print(send)

        if CAN_DRIVER == USE_UART:
            receiveCanData = self.receiveCanCmdUart(node_id, 3)
        else:
            receiveCanData = self.receiveCanCmdCanDevice(node_id, 3)

        if len(receiveCanData) <= 0:  # time_out
            print('sendFpgaUpgradePack time_out node_id=0x%02X' % node_id)
        else:
            receiveCanData = bytes(receiveCanData)
            print(receiveCanData.decode())

        self.sendFpgaUpgradeData_AD(node_id, binData, length)

        if CAN_DRIVER == USE_UART:
            receiveCanData = self.receiveCanCmdUart(node_id, 5)
        else:
            receiveCanData = self.receiveCanCmdCanDevice(node_id, 5)

        if len(receiveCanData) <= 0:  # time_out
            print('sendFpgaUpgradePack time_out node_id=0x%02X' % node_id)
            isSendFail = True
        else:
            receiveCanData = bytes(receiveCanData)
            print(receiveCanData.decode())
            if 'OK %X' % (binSum) in receiveCanData.decode():
                isSendFail = False
            else:
                isSendFail = True
                print('     receive err!!!!!!!!!!!!!!!!!!!!!!!\r\n')

        return isSendFail


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
                self.send_can_command(node_id, send)
                # time.sleep(0.002)
                # print(i)
                # print('     %s' % " ".join(hex(k) for k in send))
                send_times_cnt = i + 1

        # print(send_times_cnt)
        send = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02]
        if (send_times_low >= 1):
            # print('send_times_low')
            send[:send_times_low] = send_data[(send_times_cnt)*7:(send_times_cnt)*7+send_times_low]
            self.send_can_command(node_id, send)
            # print('     %s' % " ".join(hex(k) for k in send))

        if CAN_DRIVER == USE_UART:
            receiveCanData = self.receiveCanCmdUart(node_id, 3)
        else:
            receiveCanData = self.receiveCanCmdCanDevice(node_id, 3)

        if len(receiveCanData) <= 0:  # time_out
            print('sendFpgaUpgradePack time_out node_id=0x%02X' % node_id)
            print('sendFpgaUpgradePack: %s' % " ".join(hex(k) for k in send_data))
        else:
            print('     receive from 0x%02X FPGA: %s' % (node_id , " ".join(hex(k) for k in receiveCanData)))

        return receiveCanData

    def receiveCanCmdCanDevice(self, node_id, wait_time):
        VCI_CAN_OBJ_ARRAY_2500 = VCI_CAN_OBJ * 2500 # 结构体定义数组传入
        receive_data = VCI_CAN_OBJ_ARRAY_2500()
        self.receive_can_data.clear()

        reboot_time = time.time()

        length = self.canDll.VCI_Receive(ctypes.byref(receive_data), 2500, wait_time*1000)
        if length > 0:
            print('receive length: %d' % length)
            for i in range(length):
                # print('i=%d ' % i, end='')
                # print('ID=%02X ' % receive_data[i].ID, end='')  # 帧ID

                # if receive_data[i].TimeFlag != 0: # 时间标识
                    # print('时间标识：%d ' % (receive_data[i].TimeStamp), end='')

                # if receive_data[i].ExternFlag == 0:
                    # print('标准帧 ', end='')
                # else:
                    # print('扩展帧 ', end='')

                # if receive_data[i].RemoteFlag == 0:
                    # print('数据帧 ', end='')
                    # if receive_data[i].DataLen > (8):
                        # receive_data[i].DataLen = 8
                    # print('DataLen=%d ' % receive_data[i].DataLen, end='')
                    # print('数据：%s' % " ".join(hex(k) for k in receive_data[i].Data), end='')
                    # # print(type(receive_data[i].Data))
                    # # print('数据：%02X'list(receive_data[i].Data), end='')
                # else:
                    # print('远程帧 ', end='')

                # print('')

                if receive_data[i].ID == 0x181:
                    if receive_data[i].Data[0] == node_id:
                        if receive_data[i].Data[2] >= receive_data[i].Data[3]:
                            self.receive_can_data.append(receive_data[i].Data[4])
                            self.receive_can_data.append(receive_data[i].Data[5])
                            self.receive_can_data.append(receive_data[i].Data[6])
                            self.receive_can_data.append(receive_data[i].Data[7])
            else:
                pass

        return self.receive_can_data

    def receiveCanCmdUart(self, node_id, wait_time):
        reboot_time = time.time()
        data = ''
        self.receive_can_data.clear()
        while True:
            while (time.time() - reboot_time) > wait_time:
                # reboot_time = time.time()
                print('sendFpgaUpgradePack time_out node_id=0x%02X, diff_time=%d, wait_time=%d' % (node_id, time.time() - reboot_time, wait_time))
                # print('sendFpgaUpgradePack: %s' % " ".join(hex(k) for k in send_data))
                return  self.receive_can_data

            while self.ser.inWaiting() > 0:
                data = self.ser.read_all()
                reboot_time = time.time()
            if data != '':
                data = self.find_can_command_format(data)
                i = int(0)
                while i < len(self.can_cmd):
                    dat = self.can_cmd[i]
                    # print(" ".join(hex(k) for k in dat))
                    if dat[3] == 0x02:  #PDO1（接收）
                        pass
                    elif dat[3] == 0x01: #PDO1（发送）
                        # if dat[6] in self.AllNodeList[6][3]: # LVDS_IN_BOARD
                        if dat[6] == node_id: # LVDS_IN_BOARD
                            if dat[8] >= dat[9]: # 这里取值逻辑与MCU储存逻辑相反，可能由于大小端模式影响，待确认
                                self.receive_can_data.append(dat[10])
                                self.receive_can_data.append(dat[11])
                                self.receive_can_data.append(dat[12])
                                self.receive_can_data.append(dat[13])
                        pass
                    self.can_cmd.remove(dat)
                # print('     receive from 0x%02X FPGA: %s' % (node_id , " ".join(hex(k) for k in self.receive_can_data)))
                # print('     ', end='')
                # print(bytes(self.receive_can_data))
                break
        return self.receive_can_data

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

                        try_times = try_times + 1

                    if try_times > MAX_TRY_TIMES:
                        self.message_singel.emit('try_times = %d \r\n' % (try_times))
                        print('try_times = %d' % (try_times))
                        try_times = 0
                        break

                packetIndex = packetIndex + 1
                current_pos = current_pos + current_packerLen
                print('current_pos = %d' % current_pos)
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


    def _crc32(self, v):
      """
        Generates the crc32 hash of the v.
        @return: str, the str value for the crc32 of the v
      """
      return '0x%x' % (binascii.crc32(v) & 0xffffffff) #取crc32的八位数据 %x返回16进制


    #send_ctrl_220V_command
    def send_ctrl_220V_command(self, pressed):
        if  self.ser.isOpen():
            self.message_singel.emit('220V状态：%s...\r\n' % pressed)
            print('220V状态：%s...' % pressed)
            pass
        else:
            self.message_singel.emit('请检查串口并选择节点！\r\n')

        send_data = [0x00, pressed, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02]
        for node_idx_exist in self.AllNodeList[3][3]:
            self.send_can_command(node_idx_exist, send_data)

    def send_can_command(self, node_id, data):
        if CAN_DRIVER == USE_UART:
            self.send_can_command_uart(node_id, data)
        else:
            self.send_can_command_candriver(node_id, data)


    def send_can_command_candriver(self, node_id, data):
        ubyte_array_8 = ctypes.c_ubyte * 8
        data = ubyte_array_8( data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])
        ubyte_array_3 = ctypes.c_ubyte * 3
        reserved = ubyte_array_3(0, 0, 0)

        vci_can_obj = VCI_CAN_OBJ(0x200|node_id, 0, 0, 1, 0, 0, 8, data, reserved)

        self.canDll.VCI_Transmit(ctypes.byref(vci_can_obj), 1)

    def send_can_command_uart(self, node_id, data):
        send = [0xAA, 0xAA,
                node_id, 0x02, 0x00, 0x00,
                # data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7],
                0x08, 0x00, 0x00, 0x00,
                0x00,
                0x55 , 0x55
                ]
        send = send[0:6]+data+send[6:]
        send[18] = (send[2]+send[3]+send[14]+sum(data))&0xff
        send = self.send_command_ctrl_deal(send)
        # print(" ".join(hex(i) for i in send))
        try:
            self.ser.write(send)
        except :
            print("***打开失败,请检查串口是否被占用或其他异常!!!")
            self.message_singel.emit("***打开失败,请检查串口是否被占用或其他异常!!!\r\n")
            return

    # download_select
    def downloadSelect(self, download_select):

        self.download_select = download_select
        self.refreshBoard()

        if download_select == 0:
            pass

        elif download_select == 1:
            pass

        elif download_select == 2:
            pass

    #selectNodeID 
    def selectNodeID(self, pressed, input_node_str):
        input_node_id = eval('[%s]'% input_node_str)
        print(", ".join(hex(i) for i in input_node_id))

        for seq, board_type, file_name, node_idx_exist, node_idx_need_program in self.AllNodeList:
            # print(seq)
            # print(node_idx_exist)
            if pressed:
                if seq < 8 and input_node_id[0] in node_idx_exist:
                    node_idx_need_program.append(input_node_id[0])
                    if (input_node_id[0] in self.node_id_all_exist):
                        self.node_id_need_program.append(input_node_id[0])
                elif seq >= 8 and input_node_id[0] >= 0x80:
                    # print(input_node_id[0])
                    if input_node_id[0]&0x7f in node_idx_exist:
                        input_node_id[0] = input_node_id[0]&0x7f
                        node_idx_need_program.append(input_node_id[0])
                        if (input_node_id[0] in self.node_id_all_exist):
                            self.node_id_need_program.append(input_node_id[0])


            else:
                if seq < 8 and input_node_id[0] in node_idx_need_program:
                    if (input_node_id[0] in self.node_id_need_program):
                        node_idx_need_program.remove(input_node_id[0])
                        self.node_id_need_program.remove(input_node_id[0])
                elif input_node_id[0] >= 0x80 and seq >= 8 :
                    # input_node_id[0] = input_node_id[0]&0x7f
                    if input_node_id[0]&0x7f in node_idx_need_program:
                        input_node_id[0] = input_node_id[0]&0x7f
                        node_idx_need_program.remove(input_node_id[0])
                        self.node_id_need_program.remove(input_node_id[0])

        # print(id(self.node_id_need_program))
        # self.node_id_need_program = list(set(self.node_id_need_program))  # 设为集合再设回列表，清除重复数值, 会改变储存地址
        # print(id(self.node_id_need_program))

        print('\r\nnode_id_need_program:', end=' ')
        print(", ".join(hex(i) for i in self.node_id_need_program))
        print('  1、音频板卡    : %s' % " ".join(hex(i) for i in self.AllNodeList[0][4]))
        print('  2、模拟IO板卡  : %s' % " ".join(hex(i) for i in self.AllNodeList[1][4]))
        print('  3、数字IO板卡  : %s' % " ".join(hex(i) for i in self.AllNodeList[2][4]))
        print('  4、电源控制板卡: %s' % " ".join(hex(i) for i in self.AllNodeList[3][4]))
        print('  5、模拟信号板卡: %s' % " ".join(hex(i) for i in self.AllNodeList[4][4]))
        print('  6、数字信号板卡: %s' % " ".join(hex(i) for i in self.AllNodeList[5][4]))
        print('  7、LVDS_IN 板卡: %s' % " ".join(hex(i) for i in self.AllNodeList[6][4]))
        print('  8、底板 板卡   : %s' % " ".join(hex(i) for i in self.AllNodeList[7][4]))
        print('  9、模拟FPGA板卡: %s' % " ".join(hex(i) for i in self.AllNodeList[8][4]))
        print('  10、数字FPGA板 : %s' % " ".join(hex(i) for i in self.AllNodeList[9][4]))
        print('  11、LVDS FPGA  : %s' % " ".join(hex(i) for i in self.AllNodeList[10][4]))

    # openSerial
    def openSerial(self, COMn):
        try:
            self.ser = serial.Serial(COMn, 115200, timeout=0.001)  #/dev/ttyUSB0

            if  self.ser.isOpen():
                print("打开成功 -> %s" % (self.ser.port))
                self.message_singel.emit('打开成功 -> '+ COMn + '\r\n')
                ret = 0
            else:
                self.download_process_flag = 0
                print("打开失败,请检查串口后重启程序!")
                self.message_singel.emit("打开失败,请检查串口后重启程序!\r\n")
                ret = 1
        except:
            self.download_process_flag = 0
            print("***打开失败,请检查串口是否被占用或其他异常!!!")
            self.message_singel.emit("***打开失败,请检查串口是否被占用或其他异常!!!\r\n")
            ret = 1
        return ret

    def closeSerial(self):
        try:
            if  self.ser.isOpen():
                self.ser.close()
                print("关闭成功 -> %s" % (self.ser.port))
                self.message_singel.emit('关闭成功 -> '+ str(self.ser.port) + '\r\n')
                ret = 0
            else:
                print("关闭失败,请检查串口后重启程序!")
                self.message_singel.emit("关闭失败,请检查串口后重启程序!\r\n")
            # self.SerialUI.ser_com_combo.setEnable(True)
        except ( IndexError,AttributeError, SyntaxError, NameError, TypeError) as err:
            print(err)
            print("***打开失败,请检查串口是否被占用或其他异常!!!")
            self.message_singel.emit("***打开失败,请检查串口是否被占用或其他异常!!!\r\n")
            ret = 1
        finally:
            self.download_process_flag = 0

        return ret

    #BoardRefresh_button
    def refreshBoard(self):
        if  self.ser.isOpen():
            self.message_singel.emit('刷新节点...')
            pass
        else:
            # print('please select uart and open it!')
            self.message_singel.emit('请检查串口是否打开！\r\n')
            self.refreshBoardFlag = 0
            return

        # print('refreshBoardFlag=%d ' % (self.refreshBoardFlag))
        for i in range(8):
            for j in range(11):
                self.refresh_singel.emit(1, i, j, ' ', 0)
            self.refresh_singel.emit(2, i, j,' ', 0)

        self.node_id_all_exist.clear()
        self.node_id_need_program.clear()

        for seq, board_type, file_name, node_idx_exist, node_idx_need_program in self.AllNodeList:
            node_idx_exist.clear()
            node_idx_need_program.clear()

        node_id_all = list(range(0x02, 0x10))
        for node_id_temp in range(0x12, 0x20):
            node_id_all.append(node_id_temp)
        for node_id_temp in range(0x22, 0x30):
            node_id_all.append(node_id_temp)
        for node_id_temp in range(0x32, 0x40):
            node_id_all.append(node_id_temp)
        for node_id_temp in range(0x42, 0x50):
            node_id_all.append(node_id_temp)
        for node_id_temp in range(0x52, 0x60):
            node_id_all.append(node_id_temp)
        for node_id_temp in range(0x62, 0x70):
            node_id_all.append(node_id_temp)
        for node_id_temp in range(0x72, 0x80):
            node_id_all.append(node_id_temp)

        data = ''
        self.wait_receive = 0
        for node_id in node_id_all:
            self.send_start_command(self.ser, node_id)
            QThread.msleep(5)
            while self.ser.inWaiting() > 0:
                data = self.ser.read_all()
            if data != '' and len(data)>20:
                data = self.find_start_head(data)
                # print(" ".join(hex(i) for i in data))

                version_mcu, version_fpga = self.find_version(data)

                for seq, board_type, file_name, node_idx_exist, node_idx_need_program in self.AllNodeList:
                    if seq < 8 and data[7] == board_type:
                        node_idx_exist.append((data[6]))
                        self.node_id_all_exist.append(data[6])
                        self.box_id_exist.append(data[6]>>4)
                        self.refresh_singel.emit(3, data[6], seq, version_mcu, self.download_select)
                        if self.download_select == 2:
                            self.node_id_need_program.append(data[6])
                            node_idx_need_program.append((data[6]))
                    elif seq >=8 and data[7] == board_type:
                        node_idx_exist.append((data[6]))
                        self.node_id_all_exist.append(data[6])
                        self.box_id_exist.append(data[6]>>4)
                        self.refresh_singel.emit(3, data[6], seq, version_fpga, self.download_select)
                        if self.download_select == 2:
                            self.node_id_need_program.append(data[6])
                            node_idx_need_program.append((data[6]))

                data = ''
        self.wait_receive = 1

        print('\r\nnode_id_all_exist:', end=' ')
        print(", ".join(hex(i) for i in self.node_id_all_exist))
        print('  1、音频板卡    : %s' % " ".join(hex(i) for i in self.AllNodeList[0][3]))
        print('  2、模拟IO板卡  : %s' % " ".join(hex(i) for i in self.AllNodeList[1][3]))
        print('  3、数字IO板卡  : %s' % " ".join(hex(i) for i in self.AllNodeList[2][3]))
        print('  4、电源控制板卡: %s' % " ".join(hex(i) for i in self.AllNodeList[3][3]))
        print('  5、模拟信号板卡: %s' % " ".join(hex(i) for i in self.AllNodeList[4][3]))
        print('  6、数字信号板卡: %s' % " ".join(hex(i) for i in self.AllNodeList[5][3]))
        print('  7、LVDS_IN 板卡: %s' % " ".join(hex(i) for i in self.AllNodeList[6][3]))
        print('  8、底板 板卡   : %s' % " ".join(hex(i) for i in self.AllNodeList[7][3]))
        print('  9、模拟FPGA板卡: %s' % " ".join(hex(i) for i in self.AllNodeList[8][3]))
        print('  10、数字FPGA板 : %s' % " ".join(hex(i) for i in self.AllNodeList[9][3]))
        print('  11、LVDS FPGA  : %s' % " ".join(hex(i) for i in self.AllNodeList[10][3]))
        self.message_singel.emit(' --> 完成.\r\n')

        self.refreshBoardFlag = 0

    def download_process(self):

        if self.Download_state == 0: #---- 初始化数据---
            self.Download_state = 1

        if self.Download_state == 1: #---- 复位看门狗---
            if  self.ser.isOpen() and len(self.node_id_need_program) > 0:
                self.wait_receive = 0
                self.message_singel.emit('下载程序...\r\n')
                self.run_time = nowTime()
            else:
                print('please open uart and select update node!')
                print('Download_state=%d ' % (self.Download_state))
                self.message_singel.emit('请检查串口并选择节点！\r\n')
                self.download_process_flag = 0
                self.Download_state = 1
                return
            data = ''
            node_id_cnt = int(0)
            for node_id in self.node_id_need_program:
                self.send_reset_iwdg_command(node_id)
                self.message_singel.emit('发送重启指令：节点：' + str(hex(node_id)) + ' \r\n')
                reboot_time = time.time()
                while True:
                    while (time.time() - reboot_time) > 15:
                        self.send_reset_iwdg_command(node_id)
                        self.message_singel.emit('发送重启指令：节点：' + str(hex(node_id)) + ' \r\n')
                        reboot_time = time.time()

                    while self.ser.inWaiting() > 0:
                        reboot_time = time.time()
                        data = self.ser.read_all()
                        # print(data)
                    if data != '' and len(data) > 41 and data [2]< 0x90 and data[23] == node_id:
                        # print(" ".join(hex(i) for i in data))
                        node_id_cnt+=1
                        print("重启成功 节点%d --> 0x%02X" % (node_id_cnt, data[23]))
                        self.message_singel.emit('重启成功 --> ' + str(hex(data[23])) + ' \r\n')

                    #----start--- 发送启动命令
                        self.send_start_command(self.ser, node_id)
                        QThread.msleep(1)
                    #----end-----

                    #----start--- 发送擦除扇区命令
                        self.send_erase_commane(node_id)
                        QThread.msleep(1)
                    #----end-----

                            # data = ''
                        break;
                        data = ''
            QThread.sleep(2)
            self.Download_state = 2

            self.send_file_pcie_base_ret = 0
            self.send_file_digital_video_ret = 0
            self.send_file_analog_video_ret = 0
            self.send_file_lvds_in_ret = 0
            self.send_file_io_digital_ret = 0
            self.send_file_io_analog_ret = 0
            self.send_file_power_ret = 0
            self.send_file_audio_ret = 0

            self.send_file_pcie_base_tell = -1
            self.send_file_digital_video_tell = -1
            self.send_file_analog_video_tell = -1
            self.send_file_lvds_in_tell = -1
            self.send_file_io_digital_tell = -1
            self.send_file_io_analog_tell = -1
            self.send_file_power_tell = -1
            self.send_file_audio_tell = -1
            pass

        elif self.Download_state == 2: #send file
            if len(self.AllNodeList[7][4]) > 0:
                self.send_file_pcie_base_tell, self.send_file_pcie_base_ret = self.send_file_data(self.AllNodeList[7][2], self.send_file_pcie_base_ret, self.send_file_pcie_base_tell, self.AllNodeList[7][4])

            if len(self.AllNodeList[5][4]) > 0:
                self.send_file_digital_video_tell, self.send_file_digital_video_ret = self.send_file_data(self.AllNodeList[5][2], self.send_file_digital_video_ret, self.send_file_digital_video_tell, self.AllNodeList[5][4])

            if len(self.AllNodeList[4][4]) > 0:
                self.send_file_analog_video_tell, self.send_file_analog_video_ret = self.send_file_data(self.AllNodeList[4][2], self.send_file_analog_video_ret, self.send_file_analog_video_tell, self.AllNodeList[4][4])

            if len(self.AllNodeList[6][4]) > 0:
                self.send_file_lvds_in_tell, self.send_file_lvds_in_ret = self.send_file_data(self.AllNodeList[6][2], self.send_file_lvds_in_ret, self.send_file_lvds_in_tell, self.AllNodeList[6][4])

            if len(self.AllNodeList[2][4]) > 0:
                self.send_file_io_digital_tell, self.send_file_io_digital_ret = self.send_file_data(self.AllNodeList[2][2], self.send_file_io_digital_ret, self.send_file_io_digital_tell, self.AllNodeList[2][4])

            if len(self.AllNodeList[1][4]) > 0:
                self.send_file_io_analog_tell, self.send_file_io_analog_ret = self.send_file_data(self.AllNodeList[1][2], self.send_file_io_analog_ret, self.send_file_io_analog_tell, self.AllNodeList[1][4])

            if len(self.AllNodeList[3][4]) > 0:
                self.send_file_power_tell, self.send_file_power_ret = self.send_file_data(self.AllNodeList[3][2], self.send_file_power_ret, self.send_file_power_tell, self.AllNodeList[3][4])

            if len(self.AllNodeList[0][4]) > 0:
                self.send_file_audio_tell, self.send_file_audio_ret = self.send_file_data(self.AllNodeList[0][2], self.send_file_audio_ret, self.send_file_audio_tell, self.AllNodeList[0][4])

            if self.send_file_pcie_base_ret == 0 and self.send_file_digital_video_ret == 0 and self.send_file_analog_video_ret == 0 and self.send_file_lvds_in_ret == 0 and self.send_file_io_digital_ret == 0 and self.send_file_io_analog_ret == 0 and self.send_file_power_ret == 0 and self.send_file_audio_ret == 0:
                self.Download_state = 3

        elif self.Download_state == 3: #----start--- 发送重启命令
            self.send_command_reboot(self.node_id_need_program)
            Is_upgrade_OK = int(1)
            reboot_start_time = time.time()
            reboot_time = time.time()
            self.message_singel.emit('检查是否升级成功，请稍后...  \r\n')
            # print(reboot_time)
            while (time.time() - reboot_time) < 20:
                while self.ser.inWaiting() > 0:
                    data = self.ser.read_all()
                    # print(data)
                if data != '' and len(data) > 41 and data[2]< 0x90 and data[23] in self.node_id_need_program:
                    # print(" ".join(hex(i) for i in data))
                    print("升级成功 --> 0x%02X" % (data[23]))
                    self.message_singel.emit('升级成功 --> ' + str(hex(data[23])) + ' \r\n')
                    self.node_id_need_program.remove(data[23])
                    data = ''
                    print(time.time() - reboot_time)
                    reboot_time = time.time()

                if len(self.node_id_need_program) <= 0:
                    print('烧录 OK， 请关闭软件!....')
                    break

            # self.Download_state = 4

        # elif self.Download_state == 4:
            if len(self.node_id_need_program) > 0:
                print('升级失败节点: %s' % " ".join(hex(i) for i in self.node_id_need_program))
                self.message_singel.emit('---升级失败节点 --> ' )
                for node_id in self.node_id_need_program:
                    self.message_singel.emit(str(hex(node_id)) + ', ')
                # self.message_singel.emit(' \r\n')
                self.message_singel.emit(' 请刷新节点，重新选择失败节点升级！！！ \r\n')

            print('升级结束，请重启机箱，并确认各板卡绿灯全亮！')
            self.message_singel.emit('升级结束，请重启机箱，并确认各板卡绿灯全亮！ ')
            # time.sleep(1)
            # self.ser.close()
            print('runing time is {}s '.format((nowTime()-self.run_time)/1000))
            self.message_singel.emit('升级用时 {}s \r\n'.format((nowTime()-self.run_time)/1000))

            self.Download_state = 1
            self.download_process_flag = 0
            self.wait_receive = 1


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
                                send_data = [0xAA, 0xAA,
                                            0x12, 0x03, 0x00, 0x00,
                                            0x08, 0x00, 0x00, 0x00,
                                            0x31,
                                            0x55 , 0x55
                                            ]
                                send_data[2] = node_id
                                check_sum = (send_data[2]+send_data[3]+send_data[6]+sum(f_bin_data))
                                send_data[10] = check_sum&0xff
                                send_data = send_data[0:6:1] +f_bin_data + send_data[6::1]

                                send_data = self.send_command_ctrl_deal(send_data)
                                self.ser.write(send_data) #数据写回
                            check_sum_1K += sum(f_bin_data)
                            send_file_state = 3
                            # send_file_ret = 1
                    else:
                    #----start--- 发送1K数据
                        # print('send_file_data ...3')
                        check_sum_1K = self.send_1K_bin_data(self.ser, f_bin, node_id_need_program)
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


    def receive_data_thread(self):
        print('start receive_data_thread.')
        while True:
            time.sleep(0.001)
            try:
                if self.ser.isOpen() and self.wait_receive == 1:
                    while self.ser.inWaiting() > 0:
                        self.data_receive = self.ser.read_all()
                        # self.wait_receive = 0
            except:
                print('receive error')
            # print('tick3=%d ' % (self.tick))
            pass

    def find_can_command_format(self, data):
        # print('find_can_command_format...start')
        # print(type(data))
        data = list(data)
        # print(type(data))
        for i,dat in enumerate(data[2:-2]):
            if (data[i-1] == CAN_CTRL) and (data[i]== CAN_HEAD or data[i]== CAN_CTRL or data[i]== CAN_TAIL): #去除重复的A5
                data.remove(data[i-1])

        # print(" ".join(hex(i) for i in data))

        # for i,dat1 in enumerate(data):
        i = 1
        # print(len(data))
        while i<len(data):
            if data[i] == CAN_HEAD and data[i-1] == CAN_HEAD:
                for j,dat2 in enumerate(data[i+9:]):
                    if data[i+9+j] == CAN_TAIL and data[i+9+j-1] == CAN_TAIL:
                        self.can_cmd.append(data[i-1:i+9+j+1])
                        # print('i=%d, j=%d ' % (i, j))
                        # print(" ".join(hex(k) for k in data[i-1:i+9+j+1]))
                        i = i + 9
                        break
            else:
                i = i + 1
        # print(", ".join(hex(k) for k in self.can_cmd[0]))
        # for i, dat in enumerate(self.can_cmd):
            # print(" ".join(hex(i) for i in dat))
        # print('find_can_command_format... end')
        return data

    def sendFpgaUpgradeData_AD(self, node_id, dat, length):
        send_data = list(dat)

        # length = length
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
                self.send_can_command(node_id, send)
                send_times_cnt = i + 1
                # time.sleep(0.001)

        # print(send_times_cnt)
        send = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02]
        if (send_times_low >= 1):
            # print('send_times_low')
            send[:send_times_low] = send_data[(send_times_cnt)*7:(send_times_cnt)*7+send_times_low]
            self.send_can_command(node_id, send)

    def sendFpgaUpgradeCmd_AD(self, node_id, dat):
        send_data = list(dat)
        try:
            for i, dat_ in enumerate(send_data):
                # print(type(dat_))
                send_data[i] = ord(dat_)
                # print(type(str(dat_)))
        except Exception as e:
            # print('except')
            print(e)

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
                self.send_can_command(node_id, send)
                send_times_cnt = i + 1

        # print(send_times_cnt)
        send = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02]
        if (send_times_low >= 1):
            # print('send_times_low')
            send[:send_times_low] = send_data[(send_times_cnt)*7:(send_times_cnt)*7+send_times_low]
            self.send_can_command(node_id, send)


    def timeout_slot(self):
        self.tick = self.tick + 1
        # if (self.tick % 1000 == 0):
            # print('tick1=%d ' % (self.tick))

    def send_start_command(self, ser, node_id):
        send = [0xAA, 0xAA,
                0x00, 0x00, 0x00, 0x00,
                0x01, node_id, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x02, 0x00, 0x00, 0x00,
                0x15,
                0x55 , 0x55
                ]
        send[18] = (send[6]+send[7]+send[14])&0xff
        send = self.send_command_ctrl_deal(send)
        # print(" ".join(hex(i) for i in send))
        ser.write(send)

    def find_start_head(self, data):
        for i,data_ in enumerate(data):
            if data[i] == CAN_HEAD and data[i+1] == CAN_HEAD and data[i+2] == 0x81:
                return data[i:i+42]

    def find_version(self, data):
        if len(data) >40:
            version2 = ' '
            pass
        else:
            print('there is no version, maybe in boot')
            return 'Boot', 'Boot'

        if data[28] == DIGITAL_VIDEO_BOARD or data[28] == LVDS_IN_BOARD or data[28] == ANALOG_VIDEO_BOARD:
            year2 = ((data[29] >> 2)&0x3f)
            month2 = (((data[29]<<2)&0x0c) | ((data[30]>>6)&0x03))&0x0f
            day2 = (data[30]>>1)&0x1f

            year = ((data[31] >> 2)&0x3f)
            month = (((data[31]<<2)&0x0c) | ((data[32]>>6)&0x03))&0x0f
            day = (data[32]>>1)&0x1f

            version2 = str(year2)+'_'+str(month2)+'_'+str(day2)

        else:
            year = ((data[29] >> 2)&0x3f)
            month = (((data[29]<<2)&0x0c) | ((data[30]>>6)&0x03))&0x0f
            day = (data[30]>>1)&0x1f
            hour = ((data[30]<<4)&0x10) | data[31]>>4
            minute = ((data[31]&0x0f)<<2) | ((data[32]>>6)&0x0f)

        version = str(year)+'_'+str(month)+'_'+str(day)
        # print('year=%d, month=%d, day=%d, hour=%d, minute=%d' % (year, month, day, hour, minute))
        return version, version2

    def send_command_ctrl_deal(self, send_data):
        send_data2 = list(send_data)        # another list, 创建了的内存
        ctrl_times = int(0)
        for send_i, send_data_each in enumerate(send_data2[2:-2]):
            if send_data_each == CAN_HEAD or send_data_each == CAN_CTRL or send_data_each == CAN_TAIL :
                send_data.insert(send_i+ctrl_times+2, CAN_CTRL)
                ctrl_times = ctrl_times + 1

        return send_data

    def send_reset_iwdg_command(self, node_id):
        send = [ 0x99, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, E_CMD_RESER ]
        self.send_can_command(node_id, send)
        print("发送重启指令：节点： 0x%02X " % (node_id))

    def send_erase_commane(self, node_id):
        send = [ 0x01, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, E_CMD_UPDATE ]
        self.send_can_command(node_id, send)
        print("send_erase_commane...  node_id = 0x%02X " % (node_id))

    def send_data_command(self, node_ids):
        send = [ 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, E_CMD_UPDATE ]
        for node_id in node_ids:
            self.send_can_command(node_id, send)

    def send_1K_bin_data(self, ser, f_bin, node_ids):
        check_sum_1K = int()
        for i in range(0, PACK_SIZE//READ_SIZE):
            f_bin_data = f_bin.read(READ_SIZE)
            # byte = ord(f_bin_data)
            # print( hex(byte))
            f_bin_data = list(f_bin_data)

            for node_id in node_ids:
                send_data = [0xAA, 0xAA,
                            0x12, 0x03, 0x00, 0x00,
                            0x08, 0x00, 0x00, 0x00,
                            0x31,
                            0x55 , 0x55
                            ]
                send_data[2] = node_id
                check_sum = (send_data[2]+send_data[3]+send_data[6]+sum(f_bin_data))
                send_data[10] = check_sum&0xff
                send_data = send_data[0:6:1] +f_bin_data + send_data[6::1]

                send_data = self.send_command_ctrl_deal(send_data)
                ser.write(send_data) #数据写回

            check_sum_1K += sum(f_bin_data)
        return check_sum_1K

    def send_program_command(self, check_sum, node_ids):
        send = [
                    0x03,
                    (check_sum>>0)&0xff,
                    (check_sum>>8)&0xff,
                    (check_sum>>16)&0xff,
                    (check_sum>>24)&0xff,
                    0x00,
                    0x00,
                    0x02
                ]
        for node_id in node_ids:
            self.send_can_command(node_id, send)

    def send_command_reboot(self, node_ids):
        send = [ 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02 ]
        for node_id in node_ids:
            self.send_can_command(node_id, send)
            print("send_command_reboot...  node_id = 0x%02X " % (node_id))

    def TimeStampToTime(self, timestamp):
        timeStruct = time.localtime(timestamp)
        return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)

'''
main
'''
if __name__ == "__main__":
    if sys.stdout.isatty():
        default_encoding = sys.stdout.encoding
    else:
        default_encoding = locale.getpreferredencoding()

    print('当前工作路径为：%s ' % (os.getcwd()))
    print('当前运行程序为：%s ' % (sys.argv[0]))
    run_time = nowTime()

    try:
        #每一pyqt5应用程序必须创建一个应用程序对象。sys.argv参数是一个列表，从命令行输入参数。
        app = QApplication(sys.argv)

        ui = UI_MainWindow()

        ui.show()

        #系统exit()方法确保应用程序干净的退出
        #的exec_()方法有下划线。因为执行是一个Python关键词。因此，exec_()代替
        app.exec_()
    except Exception as e:
        print('catch error!!!')
        print(e)
        while True:
            time.sleep(3)
            pass

    finally:
        print('runing time is {}s '.format((nowTime()-run_time)/1000))
        #系统exit()方法确保应用程序干净的退出
        sys.exit()

    pass
