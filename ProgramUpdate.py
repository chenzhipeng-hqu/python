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
import serial
import binascii
import threading
import serial.tools.list_ports
from enum import Enum, unique
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QCheckBox, QComboBox)
from PyQt5.QtCore import (pyqtSignal, QTimer, QThread, QTime)
from PyQt5 import QtCore, QtGui

import UI_ProgramUpdate
from CANalystII_Driver import *
from Upgrade_MCU import UpgradeMCU
from Upgrade_FPGA import UpgradeFPGA
from Upgrade_LVDS import UpgradeLVDS
from Upgrade_USBPD import UpgradeUSBPD
from Canopen_Protocol import (CanopenProtocol, USE_UART, USE_CANALYST_II)


DEBUG = int(0)

# POWER_BOARD         = int(0x02)
# IO_ANALOG_BOARD     = int(0x04)
# AUDIO_BOARD         = int(0x05)
# IO_DIGITAL_BOARD    = int(0x06)
ANALOG_VIDEO_BOARD  = int(0x07)  # MCU 调用，暂不取消
DIGITAL_VIDEO_BOARD = int(0x08)
LVDS_IN_BOARD       = int(0x09)
TYPEC_SWITCH_BOARD  = int(0x0d)
# PCIE_BASE_BOARD     = int(0x0a)
# ANALOG_FPGA_BOARD   = int(0x07)
# DIGITAL_FPGA_BOARD  = int(0x08)
# LVDS_FPGA_BOARD     = int(0x09)
MCU_BOARD_MAX       = int(0x0b)
FPGA_BOARD_MAX      = int(0x0b)

AUDIO_BOARD_SEQ         = int(0)
IO_ANALOG_BOARD_SEQ     = int(1)
IO_DIGITAL_BOARD_SEQ    = int(2)
POWER_BOARD_SEQ         = int(3)
VIDEO_ANALOG_BOARD_SEQ  = int(4)
VIDEO_DIGITAL_BOARD_SEQ = int(5)
LVDS_IN_BOARD_SEQ       = int(6)
PCIE_BASE_BOARD_SEQ     = int(7)
TYPEC_BOARD_SEQ         = int(8)
USB_MONITOR_BOARD_SEQ   = int(9)
USB_MONITOR2_BOARD_SEQ  = int(10)
FPGA_ANALOG_BOARD_SEQ   = int(11)
FPGA_DIGITAL_BOARD_SEQ  = int(12)
FPGA_LVDS_BOARD_SEQ     = int(13)
USB_PD_BOARD_SEQ        = int(14)

AUDIO_BOARD_FILE         = str('..//bin//AudioBoard.bin')
IO_ANALOG_BOARD_FILE     = str('..//bin//IoBoardAnalog.bin')
IO_DIGITAL_BOARD_FILE    = str('..//bin//IoBoardDigital.bin')
POWER_BOARD_FILE         = str('..//bin//PowerBoard.bin')
VIDEO_ANALOG_BOARD_FILE  = str('..//bin//AnalogVideo.bin')
VIDEO_DIGITAL_BOARD_FILE = str('..//bin//DigitalVideo.bin')
LVDS_IN_BOARD_FILE       = str('..//bin//LVDSIn.bin')
PCIE_BASE_BOARD_FILE     = str('..//bin//PcieBase.bin')
TYPEC_BOARD_FILE         = str('..//bin//TypecSwitch.bin')
USB_MONITOR_BOARD_FILE   = str('..//bin//UsbMonitor.bin')
USB_MONITOR2_BOARD_FILE  = str('..//bin//UsbMonitor2.bin')
FPGA_ANALOG_BOARD_FILE   = str('..//bin//AnalogFPGA.mcs')
FPGA_DIGITAL_BOARD_FILE  = str('..//bin//DigitalFPGA.mcs')
FPGA_LVDS_BOARD_FILE     = str('..//bin//lvds_test.bin')
USB_PD_BOARD_FILE        = str('..//bin//UsbPd.bin')

F103BL_FILE              = str('..//bin//f103BL.bin')
F407BL_FILE              = str('..//bin//f407BL.bin')

BOX_ID_MAX = int(8)
BOARD_NUM_MAX = int(15)

nowTime = lambda:int(round(time.time()*1000))

class SerialComboBox(QComboBox):
    '''
    串口选择框
    '''
    message_singel = pyqtSignal(str)

    def __init__(self, parent = None):
        super(SerialComboBox,self).__init__(parent)
        self.setMaxVisibleItems(10)
        plist = list(serial.tools.list_ports.comports())
        for i in range(0, len(plist)):
            print(plist[i])
            self.addItem(str(plist[i].device))
        self.addItem('CANalystII')
        print('')

    # 重写showPopup函数
    def showPopup(self):
        # 先清空原有的选项
        self.clear()
        # 获取接入的所有串口信息，插入combobox的选项中
        plist = list(serial.tools.list_ports.comports())
        for i in range(0, len(plist)):
            print(plist[i])
            self.message_singel.emit(str(plist[i])+'\r\n')
            self.addItem(str(plist[i].device))
        self.addItem('CANalystII')
        print('')
        QComboBox.showPopup(self)   # 弹出选项框


class UI_MainWindow(UI_ProgramUpdate.Ui_Form, QWidget):
    '''
    直接继承界面类
    '''
    def __init__(self):
        super(UI_MainWindow,self).__init__()

        self.setupUi(self)

        #----initialize----QThread 任务
        self.ProgramUpdate_thread = ProgramUpdateThread()
        self.ProgramUpdate_thread.start()
        #----end----

        self.initUI()

    def __del__(self):
        print('UI_MainWindow delete.')
        self.ProgramUpdate_thread.stop()

    def initUI(self):

        self.NodeID_button =list()
        self.BoxID_checkBox = [
                                self.Box0_checkBox, self.Box1_checkBox, self.Box2_checkBox, self.Box3_checkBox,
                                self.Box4_checkBox, self.Box5_checkBox, self.Box6_checkBox, self.Box7_checkBox
                            ]
        self.BoardType_checkBox = [
                                    self.Audio_checkBox       ,
                                    self.AnalogIO_checkBox    ,
                                    self.DigitalIO_checkBox   ,
                                    self.PScontrol_checkBox   ,
                                    self.AnalogVideo_checkBox ,
                                    self.DigitalVideo_checkBox,
                                    self.LVDS_checkBox        ,
                                    self.PcieBase_checkBox    ,
                                    self.TypecSwitch_checkBox ,
                                    self.UsbMonitor_checkBox  ,
                                    self.UsbMonitor2_checkBox  ,
                                    self.AnalogFpga_checkBox  ,
                                    self.DigitalFpga_checkBox ,
                                    self.LvdsFpga_checkBox    ,
                                    self.Usb_PD_checkBox
                                ]

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

        self.ser_com_combo = SerialComboBox()
        self.ser_com_combo.message_singel.connect(self.message_singel)
        self.ser_com_combo.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.ser_com_combo.setDuplicatesEnabled(False)
        self.ser_com_combo.setFrame(False)
        self.ser_com_combo.setObjectName("ser_com_combo")
        self.gridLayout.addWidget(self.ser_com_combo, 0, 0, 1, 1)

        for i in range(BOX_ID_MAX):
            for j in range(BOARD_NUM_MAX):
                self.NodeID_button.append(QPushButton())
                self.NodeID_button[i*BOARD_NUM_MAX+j].setEnabled(False)
                self.NodeID_button[i*BOARD_NUM_MAX+j].setText("")
                self.NodeID_button[i*BOARD_NUM_MAX+j].setCheckable(True)
                self.NodeID_button[i*BOARD_NUM_MAX+j].setFlat(True)
                self.NodeID_button[i*BOARD_NUM_MAX+j].setPalette(palette)
                self.NodeID_button[i*BOARD_NUM_MAX+j].clicked[bool].connect(self.selectNodeID)
                self.gridLayout_3.addWidget(self.NodeID_button[i*BOARD_NUM_MAX+j], j+2, i+1, 1, 1)
            self.BoxID_checkBox[i].stateChanged.connect(self.download_select)
            self.BoxID_checkBox[i].id_ = i<<4
            self.BoxID_checkBox[i].setCheckable(False)

        for board_id in range(BOARD_NUM_MAX):
            self.BoardType_checkBox[board_id].stateChanged.connect(self.download_select)
            self.BoardType_checkBox[board_id].id_ = board_id & 0x0f
            self.BoardType_checkBox[board_id].setCheckable(False)

        #downloadSelect_combox
        self.downloadMode_comboBox.currentIndexChanged.connect(self.download_select)
        self.downloadMode_comboBox.id_ = BOX_ID_MAX<<4

        #dispfileversion_singel
        self.ProgramUpdate_thread.dispFileVersion_singel.connect(self.dispFileVersion)

        # message_singel
        self.ProgramUpdate_thread.message_singel.connect(self.message_singel)
        self.ProgramUpdate_thread.MCU.message_singel.connect(self.message_singel)
        self.ProgramUpdate_thread.FPGA.message_singel.connect(self.message_singel)
        self.ProgramUpdate_thread.LVDS.message_singel.connect(self.message_singel)
        self.ProgramUpdate_thread.UsbPD.message_singel.connect(self.message_singel)
        textCursor = self.Msg_TextEdit.textCursor()
        textCursor.movePosition(textCursor.End)
        self.Msg_TextEdit.setTextCursor(textCursor)

        # openSerial
        self.ser_open_button.clicked.connect(self.openSerial)

        #refreshBoard
        self.BoardRefresh_button.clicked.connect(self.refreshBoard)

        #refresh_singel
        self.ProgramUpdate_thread.refresh_singel.connect(self.refresh_singel)

        #processbar_singel
        self.ProgramUpdate_thread.processBar_singel.connect(self.processBar_singel)
        self.ProgramUpdate_thread.MCU.processBar_singel.connect(self.processBar_singel)
        self.ProgramUpdate_thread.FPGA.processBar_singel.connect(self.processBar_singel)
        self.ProgramUpdate_thread.LVDS.processBar_singel.connect(self.processBar_singel)
        self.ProgramUpdate_thread.UsbPD.processBar_singel.connect(self.processBar_singel)

        #timeDisp_singel
        self.ProgramUpdate_thread.timeDisp_singel.connect(self.timeDisp_singel)

        #download_singel
        self.ProgramUpdate_thread.download_singel.connect(self.download_singel)

        #download_process
        self.download_button.clicked.connect(self.download_process)

        #ctrl_220V_button
        self.ctrl_220V_button.clicked.connect(self.ctrl_220V)

        #Lvds_combobox
        self.Lvds_comboBox.currentIndexChanged.connect(self.lvds_select_addr)

    #Lvds_combobox
    def lvds_select_addr(self):
        source = self.sender()
        # print(source.currentIndex(), end=' ')
        # print(source.currentText())
        if source.currentText() == 'LVDS':
            self.ProgramUpdate_thread.lvdsStartAddr = 0x000000
            self.ProgramUpdate_thread.AllNodeList[FPGA_LVDS_BOARD_SEQ][2] = str('..//bin//lvds_ddr.bin')

        elif source.currentText() == 'N10':
            self.ProgramUpdate_thread.lvdsStartAddr = 0x170000
            self.ProgramUpdate_thread.AllNodeList[FPGA_LVDS_BOARD_SEQ][2] = str('..//bin//N10.bin')

        elif source.currentText() == 'N86_1':
            self.ProgramUpdate_thread.lvdsStartAddr = 0x2e0000
            self.ProgramUpdate_thread.AllNodeList[FPGA_LVDS_BOARD_SEQ][2] = str('..//bin//N86_1.bin')

        elif source.currentText() == 'N81':
            self.ProgramUpdate_thread.lvdsStartAddr = 0x450000
            self.ProgramUpdate_thread.AllNodeList[FPGA_LVDS_BOARD_SEQ][2] = str('..//bin//N81.bin')

        elif source.currentText() == 'PT320':
            self.ProgramUpdate_thread.lvdsStartAddr = 0x5C0000
            self.ProgramUpdate_thread.AllNodeList[FPGA_LVDS_BOARD_SEQ][2] = str('..//bin//PT320.bin')

        elif source.currentText() == 'N86_2':
            self.ProgramUpdate_thread.lvdsStartAddr = 0x730000
            self.ProgramUpdate_thread.AllNodeList[FPGA_LVDS_BOARD_SEQ][2] = str('..//bin//N86_2.bin')

        elif source.currentText() == 'PT320_2':
            self.ProgramUpdate_thread.lvdsStartAddr = 0x8A0000
            self.ProgramUpdate_thread.AllNodeList[FPGA_LVDS_BOARD_SEQ][2] = str('..//bin//PT320_2.bin')

        elif source.currentText() == 'EXT_2':
            self.ProgramUpdate_thread.lvdsStartAddr = 0xA10000
            self.ProgramUpdate_thread.AllNodeList[FPGA_LVDS_BOARD_SEQ][2] = str('..//bin//N10_2.bin')

        elif source.currentText() == 'Bootloader':
            self.ProgramUpdate_thread.lvdsStartAddr = 0xB80000
            self.ProgramUpdate_thread.mcuBoot       = 1
            self.ProgramUpdate_thread.AllNodeList[FPGA_LVDS_BOARD_SEQ][2]     = str('..//bin//boot_test.bin')

            self.ProgramUpdate_thread.AllNodeList[AUDIO_BOARD_SEQ][2]         = F407BL_FILE
            self.ProgramUpdate_thread.AllNodeList[IO_ANALOG_BOARD_SEQ][2]     = F407BL_FILE
            self.ProgramUpdate_thread.AllNodeList[IO_DIGITAL_BOARD_SEQ][2]    = F407BL_FILE
            self.ProgramUpdate_thread.AllNodeList[POWER_BOARD_SEQ][2]         = F407BL_FILE
            self.ProgramUpdate_thread.AllNodeList[USB_MONITOR_BOARD_SEQ][2]   = F407BL_FILE
            self.ProgramUpdate_thread.AllNodeList[USB_MONITOR2_BOARD_SEQ][2]  = F407BL_FILE

            self.ProgramUpdate_thread.AllNodeList[VIDEO_ANALOG_BOARD_SEQ][2]  = F103BL_FILE
            self.ProgramUpdate_thread.AllNodeList[VIDEO_DIGITAL_BOARD_SEQ][2] = F103BL_FILE
            self.ProgramUpdate_thread.AllNodeList[LVDS_IN_BOARD_SEQ][2]       = F103BL_FILE
            self.ProgramUpdate_thread.AllNodeList[PCIE_BASE_BOARD_SEQ][2]     = F103BL_FILE
            self.ProgramUpdate_thread.AllNodeList[TYPEC_BOARD_SEQ][2]         = F103BL_FILE

        elif source.currentText() == 'NORMAL':
            self.ProgramUpdate_thread.mcuBoot       = 0
            self.ProgramUpdate_thread.AllNodeList[AUDIO_BOARD_SEQ][2]         = AUDIO_BOARD_FILE
            self.ProgramUpdate_thread.AllNodeList[IO_ANALOG_BOARD_SEQ][2]     = IO_ANALOG_BOARD_FILE
            self.ProgramUpdate_thread.AllNodeList[IO_DIGITAL_BOARD_SEQ][2]    = IO_DIGITAL_BOARD_FILE
            self.ProgramUpdate_thread.AllNodeList[POWER_BOARD_SEQ][2]         = POWER_BOARD_FILE
            self.ProgramUpdate_thread.AllNodeList[USB_MONITOR_BOARD_SEQ][2]   = USB_MONITOR_BOARD_FILE
            self.ProgramUpdate_thread.AllNodeList[USB_MONITOR2_BOARD_SEQ][2]  = USB_MONITOR2_BOARD_FILE

            self.ProgramUpdate_thread.AllNodeList[VIDEO_ANALOG_BOARD_SEQ][2]  = VIDEO_ANALOG_BOARD_FILE
            self.ProgramUpdate_thread.AllNodeList[VIDEO_DIGITAL_BOARD_SEQ][2] = VIDEO_DIGITAL_BOARD_FILE
            self.ProgramUpdate_thread.AllNodeList[LVDS_IN_BOARD_SEQ][2]       = LVDS_IN_BOARD_FILE
            self.ProgramUpdate_thread.AllNodeList[PCIE_BASE_BOARD_SEQ][2]     = PCIE_BASE_BOARD_FILE
            self.ProgramUpdate_thread.AllNodeList[TYPEC_BOARD_SEQ][2]         = TYPEC_BOARD_FILE

        print(hex(self.ProgramUpdate_thread.lvdsStartAddr))
        self.dispFileVersion(FPGA_LVDS_BOARD_SEQ, self.ProgramUpdate_thread.AllNodeList[FPGA_LVDS_BOARD_SEQ][2])

    #dispfileversion
    def dispFileVersion(self, seq, file_name):
        self.BoardType_checkBox[seq].setToolTip(self.TimeStampToTime(os.path.getmtime(file_name)))

    #ctrl_220V
    def ctrl_220V(self, pressed):
        source = self.sender()
        self.ProgramUpdate_thread.send_ctrl_220V_command(pressed)

    #allNodeID_checkBox
    def download_select(self, state):
        source = self.sender()

        box_id = source.id_ >> 4

        if (box_id == BOX_ID_MAX):

            self.ProgramUpdate_thread.download_mode = source.currentText()

            for i in range(BOARD_NUM_MAX):
                for j in range(BOX_ID_MAX):
                    self.ProgramUpdate_thread.download_select[i][j] = QtCore.Qt.Unchecked

            if source.currentText() == 'NORMAL':
                for i in range(BOX_ID_MAX):
                    self.BoxID_checkBox[i].setCheckState(QtCore.Qt.Unchecked)
                    self.BoxID_checkBox[i].setCheckable(False)

                for i in range(BOARD_NUM_MAX):
                    self.BoardType_checkBox[i].setCheckState(QtCore.Qt.Unchecked)
                    self.BoardType_checkBox[i].setCheckable(False)

            elif source.currentText() == 'BOARD':
                for i in range(BOX_ID_MAX):
                    # self.BoxID_checkBox[i].setCheckState(QtCore.Qt.Unchecked)
                    self.BoxID_checkBox[i].setCheckable(False)

                for i in range(BOARD_NUM_MAX):
                    self.BoardType_checkBox[i].setCheckable(True)
                    self.BoardType_checkBox[i].setCheckState(QtCore.Qt.Unchecked)

            elif source.currentText() == 'BOX':
                for i in range(BOX_ID_MAX):
                    self.BoxID_checkBox[i].setCheckable(True)
                    self.BoxID_checkBox[i].setCheckState(QtCore.Qt.Unchecked)

                for i in range(BOARD_NUM_MAX):
                    # self.BoardType_checkBox[i].setCheckState(QtCore.Qt.Unchecked)
                    self.BoardType_checkBox[i].setCheckable(False)

            elif source.currentText() == 'ALL':
                for i in range(BOX_ID_MAX):
                    self.BoxID_checkBox[i].setCheckable(True)
                    self.BoxID_checkBox[i].setCheckState(QtCore.Qt.Checked)

                for i in range(BOARD_NUM_MAX):
                    self.BoardType_checkBox[i].setCheckable(True)
                    self.BoardType_checkBox[i].setCheckState(QtCore.Qt.Checked)
        else:
            self.ProgramUpdate_thread.downloadSelect(state, self.ProgramUpdate_thread.download_mode, source.id_)
            self.groupBox_3.setEnabled(False)

    #selectNodeID
    def selectNodeID(self, pressed):
        source = self.sender()
        self.ProgramUpdate_thread.selectNodeID(pressed, str(source.id_))
        self.download_button.setEnabled(True)

    def download_process(self):
        self.ProgramUpdate_thread.time_tick.setHMS(0, 0, 0)#初始时设置时间为  00：00：00
        source = self.sender()
        self.groupBox.setEnabled(False)
        self.groupBox_3.setEnabled(False)
        self.Msg_TextEdit.setEnabled(True)
        self.ProgramUpdate_thread.download_process_flag = 1
        self.ProgramUpdate_thread.run_time = nowTime()
        self.Progress_bar.setValue(0)
        self.Msg_TextEdit.insertPlainText('\r\n')
        self.Msg_TextEdit.insertPlainText('\r\n')
        self.Msg_TextEdit.insertPlainText('\r\n')
        self.Msg_TextEdit.insertPlainText('\r\n')
        self.Msg_TextEdit.insertPlainText('\r\n')
        self.Msg_TextEdit.insertPlainText('\r\n')

    # openSerial
    def openSerial(self):
        source = self.sender()
        if source.text() == '打开':
            ret = self.ProgramUpdate_thread.openSerial(str(self.ser_com_combo.currentText()))
            if ret == 0:
                self.ser_com_combo.setEnabled(False)
                source.setText('关闭')
                source.setChecked(True)
                self.groupBox_3.setEnabled(True)
                self.Lvds_comboBox.setEnabled(True)
                self.downloadMode_comboBox.setEnabled(True)
                # self.allNodeID_checkBox.setEnabled(True)
            else:
                source.setChecked(False)

        elif source.text() == '关闭':
            ret = self.ProgramUpdate_thread.closeSerial()
            if ret == 0:
                self.ser_com_combo.setEnabled(True)
                source.setText('打开')
                source.setChecked(False)
                self.groupBox_3.setEnabled(False)
            else:
                source.setChecked(True)

    #BoardRefresh_button
    def refreshBoard(self):
        source = self.sender()
        self.ProgramUpdate_thread.refreshBoardFlag = 1
        self.groupBox_3.setEnabled(False)
        self.Progress_bar.setValue(0)

    #message_singel
    def message_singel(self, str):
        # 移动光标到最后的文字
        textCursor = self.Msg_TextEdit.textCursor()
        textCursor.movePosition(textCursor.End)
        self.Msg_TextEdit.setTextCursor(textCursor)

        self.Msg_TextEdit.insertPlainText(str)

    def processBar_singel(self, val):
        self.Progress_bar.setValue(val)

    def download_singel(self, isFinished):
        if isFinished == 1:
            self.ProgramUpdate_thread.refreshBoardFlag = 1
            # self.setEnabled(True)
            self.groupBox.setEnabled(True)
            # self.groupBox_3.setEnabled(True)
            self.groupBox_3.setEnabled(False)
            self.download_button.setEnabled(False)

    #refresh_singel
    def refresh_singel(self, cmd, i, j, version ,is_down):

        if cmd == 1:  # clear node_id
            self.NodeID_button[i*BOARD_NUM_MAX+j].setText('    ')
            self.NodeID_button[i*BOARD_NUM_MAX+j].setCheckable(False)
            self.NodeID_button[i*BOARD_NUM_MAX+j].setEnabled(False)
            self.NodeID_button[i*BOARD_NUM_MAX+j].setFlat(True)

        if cmd == 2:  # clear box_id
            self.BoxID_checkBox[i].setEnabled(False)

        if cmd == 3: # clear board type
            self.BoardType_checkBox[i].setEnabled(False)

        if cmd == 4:  # set node_id
            box_id = i>>4
            self.NodeID_button[(box_id)*BOARD_NUM_MAX+j].setFlat(False)     # 使用框框
            self.NodeID_button[(box_id)*BOARD_NUM_MAX+j].setText(str(version))
            self.NodeID_button[(box_id)*BOARD_NUM_MAX+j].setCheckable(True) # 防止选中之后节点丢失残留
            self.NodeID_button[(box_id)*BOARD_NUM_MAX+j].setChecked(is_down)
            self.NodeID_button[(box_id)*BOARD_NUM_MAX+j].setEnabled(True)  # 防止未显示的节点被选中
            self.NodeID_button[(box_id)*BOARD_NUM_MAX+j].setToolTip(hex(i))

            self.BoardType_checkBox[j].setEnabled(True)
            self.BoxID_checkBox[(box_id)].setEnabled(True)

            if j >= MCU_BOARD_MAX-1 :
                self.NodeID_button[(box_id)*BOARD_NUM_MAX+j].id_ = i | 0x80   # 最高位置1 表示FPGA板
            else:
                self.NodeID_button[(box_id)*BOARD_NUM_MAX+j].id_ = i

        if cmd == 5:  # refresh node_id finish
            self.groupBox_3.setEnabled(True)
            self.download_button.setEnabled(is_down)

    def timeDisp_singel(self, now_time):
        self.timeDisp.setText(now_time.toString("hh:mm:ss"))
        pass

    def TimeStampToTime(self, timestamp):
        timeStruct = time.localtime(timestamp)
        return time.strftime('%Y-%m-%d',timeStruct)

class ProgramUpdateThread(QThread):
    '''
    ProgramUpdateThread
    '''
    #定义一个信号
    refresh_singel = pyqtSignal(int, int, int, str, int)
    processBar_singel = pyqtSignal(int)
    message_singel = pyqtSignal(str)
    timeDisp_singel = pyqtSignal(QTime)
    download_singel = pyqtSignal(int)
    dispFileVersion_singel =pyqtSignal(int, str)

    def __init__(self):
        super(ProgramUpdateThread, self).__init__()
        self.wait_receive = int(0)
        self.lvdsStartAddr = 0xA10000 # 默认一个起始下载地址，防止没选择地址的时候擦出0地址的数据
        self.mcuBoot = 0;

        self.AllNodeList = [
            #0.seq  , 1.board_type  , 2.file_name                , 3.node_idx_exist, 4.node_idx_need_program
            [ AUDIO_BOARD_SEQ            , 0x05      , AUDIO_BOARD_FILE         , list()        , list() ],   # 0.audio_board
            [ IO_ANALOG_BOARD_SEQ        , 0x04      , IO_ANALOG_BOARD_FILE     , list()        , list() ],   # 1.io_analog_board
            [ IO_DIGITAL_BOARD_SEQ       , 0x06      , IO_DIGITAL_BOARD_FILE    , list()        , list() ],   # 2.io_digital_board
            [ POWER_BOARD_SEQ            , 0x02      , POWER_BOARD_FILE         , list()        , list() ],   # 3.power_board
            [ VIDEO_ANALOG_BOARD_SEQ     , 0x07      , VIDEO_ANALOG_BOARD_FILE  , list()        , list() ],   # 4.analog_video_board
            [ VIDEO_DIGITAL_BOARD_SEQ    , 0x08      , VIDEO_DIGITAL_BOARD_FILE , list()        , list() ],   # 5.digital_video_board
            [ LVDS_IN_BOARD_SEQ          , 0x09      , LVDS_IN_BOARD_FILE       , list()        , list() ],   # 6.lvds_in_board
            [ PCIE_BASE_BOARD_SEQ        , 0x0a      , PCIE_BASE_BOARD_FILE     , list()        , list() ],   # 7.pcie_base_board
            [ TYPEC_BOARD_SEQ            , 0x0d      , TYPEC_BOARD_FILE         , list()        , list() ],   # 8.typec_switch
            [ USB_MONITOR_BOARD_SEQ      , 0x0c      , USB_MONITOR_BOARD_FILE   , list()        , list() ],   # 9.usb_monitor
            [ USB_MONITOR2_BOARD_SEQ     , 0x0E      , USB_MONITOR2_BOARD_FILE  , list()        , list() ],   # 10.usb_monitor
            [ FPGA_ANALOG_BOARD_SEQ      , 0x07      , FPGA_ANALOG_BOARD_FILE   , list()        , list() ],   # 11.analog_fpga_board
            [ FPGA_DIGITAL_BOARD_SEQ     , 0x08      , FPGA_DIGITAL_BOARD_FILE  , list()        , list() ],   # 12.digital_fpga_board
            [ FPGA_LVDS_BOARD_SEQ        , 0x09      , FPGA_LVDS_BOARD_FILE     , list()        , list() ],   # 13.lvds_fpga_board 此处使用列表，需要修改file_name
            [ USB_PD_BOARD_SEQ           , 0x0d      , USB_PD_BOARD_FILE        , list()        , list() ]    # 14.usb_pd
            ]

        #----initialize----QTimer 任务
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timeout_slot)
        self.timer.start(1000)
        self.time_tick=QTime()
        self.time_tick.setHMS(0,0,0)  #初始时设置时间为  00：00：00
        #----end----

        #----initialize----threading 任务
        self.thread_1 = threading.Thread(target=self.receive_data_thread) #建立一个线程，调用receive_data_thread方法，不带参数
        self.thread_1.setDaemon(True) #声明为守护线程，设置的话，子线程将和主线程一起运行，并且直接结束，不会再执行循环里面的子线程
        self.thread_1.start()
        # self.thread_1.join() #作用是执行完所有子线程才去执行主线程
        #----end----

        self.download_process_flag = 0
        self.refreshBoardFlag = 0
        self.download_select = [ [0 for i in range(BOX_ID_MAX)] for i in range(BOARD_NUM_MAX) ]

        #---- canopenprotocol----
        self.Canopen = CanopenProtocol()
        #---end---

        #---- MCU upgrade_creat----
        self.MCU = UpgradeMCU()
        self.MCU.setInterfaceDev(self.Canopen)
        #---end---

        #---- FPGA upgrade_creat----
        self.FPGA = UpgradeFPGA()
        self.FPGA.setInterfaceDev(self.Canopen)
        #---end---

        #---- LVDS upgrade_creat----
        self.LVDS = UpgradeLVDS()
        self.LVDS.setInterfaceDev(self.Canopen)

        #---- usb pd  upgrade_creat----
        self.UsbPD = UpgradeUSBPD()
        self.UsbPD.setInterfaceDev(self.Canopen)
        #---end---

        self.download_mode = 'NORMAL'

    def run(self):
        while True:
            if self.refreshBoardFlag == 1:
                self.refreshBoard()

            if self.download_process_flag == 1:
                self.download_process3()

            QThread.usleep(1)
            pass

    def download_process3(self):

        for seq, board_type, file_name, node_idx_exist, node_idx_need_program in self.AllNodeList:
            if seq < MCU_BOARD_MAX and len(node_idx_need_program):
                self.MCU.downloadProcess(file_name, node_idx_need_program, self.mcuBoot)
                break

            elif (seq == FPGA_ANALOG_BOARD_SEQ or seq == FPGA_DIGITAL_BOARD_SEQ) and len(node_idx_need_program):
                if seq == FPGA_DIGITAL_BOARD_SEQ:
                    boardType = 'digital'
                elif seq == FPGA_ANALOG_BOARD_SEQ:
                    boardType = 'analog'

                self.FPGA.downloadProcess(boardType, file_name, node_idx_need_program)
                break

            elif seq == FPGA_LVDS_BOARD_SEQ and len(node_idx_need_program):
                self.LVDS.downloadProcess(self.lvdsStartAddr, file_name, node_idx_need_program)
                break

            elif seq == USB_PD_BOARD_SEQ and len(node_idx_need_program):
                self.UsbPD.downloadProcess(file_name, node_idx_need_program)
                break

            elif seq >= BOARD_NUM_MAX-1:
                print('升级结束，请重启机箱，并确认各板卡绿灯全亮！iwdg reset')
                # self.message_singel.emit('升级用时 {}s \r\n'.format((nowTime()-self.run_time)/1000))
                self.message_singel.emit('升级结束，请重启机箱，并刷新节点确认版本号！版本号正确即可。 \r\n')
                self.download_singel.emit(1)
                self.download_process_flag = 0

    #send_ctrl_220V_command
    def send_ctrl_220V_command(self, pressed):
        if  self.ser.isOpen():
            self.message_singel.emit('220V状态：%s...\r\n' % pressed)
            print('220V状态：%s...' % pressed)
            pass
        else:
            self.message_singel.emit('请检查串口并选择节点！\r\n')

        send_data = [0x00, pressed, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02]
        for node_idx_exist in self.AllNodeList[POWER_BOARD_SEQ][3]:
            # self.send_can_command(node_idx_exist, send_data)
            self.Canopen.sendData(self.Canopen.PDO1_Rx, node_idx_exist, 8, send_data)

    # download_select
    def downloadSelect(self, download_select, download_mode, id_):

        if download_mode == 'NORMAL':
            pass

        elif download_mode == 'BOX':
            box_id = id_ >> 4
            for i in range(BOARD_NUM_MAX):
                self.download_select[i][box_id] = download_select

        elif download_mode == 'BOARD':
            board_id = id_ & 0x0f
            for j in range(BOX_ID_MAX):
                self.download_select[board_id][j] = download_select

        elif download_mode == 'ALL':
            for i in range(BOARD_NUM_MAX):
                for j in range(BOX_ID_MAX):
                    self.download_select[i][j] = download_select

        elif download_mode == 'BOOT':
            pass

        # self.refreshBoard()
        self.refreshBoardFlag = 1

    #selectNodeID
    def selectNodeID(self, pressed, input_node_str):
        input_node_id = eval('[%s]'% input_node_str)
        print(", ".join(hex(i) for i in input_node_id))

        for seq, board_type, file_name, node_idx_exist, node_idx_need_program in self.AllNodeList:
            if pressed:
                if seq < MCU_BOARD_MAX-1 and input_node_id[0] in node_idx_exist:
                    node_idx_need_program.append(input_node_id[0])
                elif seq >= MCU_BOARD_MAX-1 and input_node_id[0] >= 0x80:
                    if input_node_id[0]&0x7f in node_idx_exist:
                        input_node_id[0] = input_node_id[0]&0x7f
                        node_idx_need_program.append(input_node_id[0])

            else:
                if seq < MCU_BOARD_MAX-1 and input_node_id[0] in node_idx_need_program:
                    node_idx_need_program.remove(input_node_id[0])
                elif input_node_id[0] >= 0x80 :
                    if input_node_id[0]&0x7f in node_idx_need_program:
                        input_node_id[0] = input_node_id[0]&0x7f
                        node_idx_need_program.remove(input_node_id[0])

        print('\r\nnode_id_need_program:')
        print('  1、音频板卡    : %s' % " ".join(hex(i) for i in self.AllNodeList[0][4]))
        print('  2、模拟IO板卡  : %s' % " ".join(hex(i) for i in self.AllNodeList[1][4]))
        print('  3、数字IO板卡  : %s' % " ".join(hex(i) for i in self.AllNodeList[2][4]))
        print('  4、电源控制板卡: %s' % " ".join(hex(i) for i in self.AllNodeList[3][4]))
        print('  5、模拟信号板卡: %s' % " ".join(hex(i) for i in self.AllNodeList[4][4]))
        print('  6、数字信号板卡: %s' % " ".join(hex(i) for i in self.AllNodeList[5][4]))
        print('  7、LVDS_IN 板卡: %s' % " ".join(hex(i) for i in self.AllNodeList[6][4]))
        print('  8、底板 板卡   : %s' % " ".join(hex(i) for i in self.AllNodeList[7][4]))
        print('  9、typec 板卡  : %s' % " ".join(hex(i) for i in self.AllNodeList[8][4]))
        print('  10、usb监控板  : %s' % " ".join(hex(i) for i in self.AllNodeList[9][4]))
        print('  11、usb监控板2 : %s' % " ".join(hex(i) for i in self.AllNodeList[10][4]))
        print('  12、模拟FPGA板 : %s' % " ".join(hex(i) for i in self.AllNodeList[11][4]))
        print('  13、数字FPGA板 : %s' % " ".join(hex(i) for i in self.AllNodeList[12][4]))
        print('  14、LVDS FPGA  : %s' % " ".join(hex(i) for i in self.AllNodeList[13][4]))
        print('  15、usb pd     : %s' % " ".join(hex(i) for i in self.AllNodeList[14][4]))

    # openSerial
    def openSerial(self, COMn):
        try:
            if COMn == 'CANalystII':
                index = 0
                can_num = 0
                self.canDll = CANalystDriver(VCI_USBCAN2A, index, can_num)
                ret = self.canDll.VCI_OpenDevice(0)
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

                self.Canopen.setInterfaceDev(self.canDll, USE_CANALYST_II)
            else:
                self.ser = serial.Serial(COMn, 115200, timeout=0.001)  #/dev/ttyUSB0
                self.Canopen.setInterfaceDev(self.ser, USE_UART)

            if  self.Canopen.devIsOpen():
                print("打开成功 -> %s" % (COMn))
                self.message_singel.emit('打开成功 -> '+ COMn + '\r\n')
                self.wait_receive = 1
                ret = 0
            else:
                self.download_process_flag = 0
                print("打开失败,请检查串口后重启程序!")
                self.message_singel.emit("打开失败,请检查串口后重启程序!\r\n")
                ret = 1
        except Exception as e:
            self.download_process_flag = 0
            print(e)
            print("***打开失败,请检查串口是否被占用或其他异常!!!")
            self.message_singel.emit("***打开失败,请检查串口是否被占用或其他异常!!!\r\n")
            ret = 1
        return ret

    def closeSerial(self):
        try:
            if  self.Canopen.devIsOpen():
                self.Canopen.devClose()
                self.wait_receive = 0
                ret = 0
                # print("关闭成功 -> %s" % (self.ser.port))
                self.message_singel.emit('关闭成功\r\n')
            else:
                print("关闭失败,请检查串口后重启程序!")
                self.message_singel.emit("关闭失败,请检查串口后重启程序!\r\n")
        except Exception  as err:
            print(err)
            print("***打开失败,请检查串口是否被占用或其他异常!!!")
            self.message_singel.emit("***打开失败,请检查串口是否被占用或其他异常!!!\r\n")
            ret = 1
        finally:
            self.download_process_flag = 0

        return ret

    #BoardRefresh_button
    def refreshBoard(self):
        if  self.Canopen.devIsOpen():
            # self.message_singel.emit('刷新节点...')
            pass
        else:
            print('please select uart and open it!')
            self.message_singel.emit('请检查串口是否打开！\r\n')
            self.refreshBoardFlag = 0
            return

        for box_id in range(BOX_ID_MAX):
            for board_num in range(BOARD_NUM_MAX):
                self.refresh_singel.emit(1, box_id, board_num, ' ', 0)
            self.refresh_singel.emit(2, box_id, board_num,' ', 0)

        for seq, board_type, file_name, node_idx_exist, node_idx_need_program in self.AllNodeList:
            node_idx_exist.clear()
            node_idx_need_program.clear()
            self.refresh_singel.emit(3, seq, 0,' ', 0)
            if os.path.exists(file_name):
                self.dispFileVersion_singel.emit(seq, file_name)

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


        for node_id in node_id_all:
            self.Canopen.sendStartCmd(node_id) #------- 发送启动命令
            can_cmd = self.Canopen.getRevData(0x81, node_id, 5)

            if len(can_cmd):
                QThread.msleep(2) # 加了这个更不容易丢失刷新的节点
                version_mcu, version_fpga = self.MCU.findVersion(can_cmd)

                box_id = can_cmd[0][0]>>4

                for seq, board_type, file_name, node_idx_exist, node_idx_need_program in self.AllNodeList:
                    if can_cmd[0][1] == board_type:
                        node_idx_exist.append((can_cmd[0][0]))
                        if self.download_select[seq][box_id] == QtCore.Qt.Checked:
                            node_idx_need_program.append((can_cmd[0][0]))

                        if seq < MCU_BOARD_MAX:
                            self.refresh_singel.emit(4, can_cmd[0][0], seq, version_mcu, self.download_select[seq][box_id])
                        else:
                            self.refresh_singel.emit(4, can_cmd[0][0], seq, version_fpga, self.download_select[seq][box_id])

        print('\r\nnode_id_all_exist:')
        print('  1、音频板卡    : %s' % " ".join(hex(i) for i in self.AllNodeList[0][3]))
        print('  2、模拟IO板卡  : %s' % " ".join(hex(i) for i in self.AllNodeList[1][3]))
        print('  3、数字IO板卡  : %s' % " ".join(hex(i) for i in self.AllNodeList[2][4]))
        print('  4、电源控制板卡: %s' % " ".join(hex(i) for i in self.AllNodeList[3][3]))
        print('  5、模拟信号板卡: %s' % " ".join(hex(i) for i in self.AllNodeList[4][3]))
        print('  6、数字信号板卡: %s' % " ".join(hex(i) for i in self.AllNodeList[5][3]))
        print('  7、LVDS_IN 板卡: %s' % " ".join(hex(i) for i in self.AllNodeList[6][3]))
        print('  8、底板 板卡   : %s' % " ".join(hex(i) for i in self.AllNodeList[7][3]))
        print('  9、typec 板卡  : %s' % " ".join(hex(i) for i in self.AllNodeList[8][3]))
        print('  10、usb监控板  : %s' % " ".join(hex(i) for i in self.AllNodeList[9][3]))
        print('  11、usb监控板2 : %s' % " ".join(hex(i) for i in self.AllNodeList[10][3]))
        print('  12、模拟FPGA板 : %s' % " ".join(hex(i) for i in self.AllNodeList[11][3]))
        print('  13、数字FPGA板 : %s' % " ".join(hex(i) for i in self.AllNodeList[12][3]))
        print('  14、LVDS FPGA  : %s' % " ".join(hex(i) for i in self.AllNodeList[13][3]))
        print('  15、usb pd     : %s' % " ".join(hex(i) for i in self.AllNodeList[14][3]))
        # self.message_singel.emit(' --> 完成.\r\n')

        showDownloadButton = False
        for seq, board_type, file_name, node_idx_exist, node_idx_need_program in self.AllNodeList:
            if len(node_idx_need_program):
                showDownloadButton = True

        self.refresh_singel.emit(5, 0, 0, ' ', showDownloadButton) # 刷新节点完成

        self.refreshBoardFlag = 0

    def receive_data_thread(self):
        print('start receive_data_thread.')
        while True:
            time.sleep(0.001)
            try:
                if self.wait_receive == 1:
                    self.Canopen.receiveData()
            except Exception as err:
                print(err)

    def timeout_slot(self):
        self.time_tick = self.time_tick.addMSecs(1000)
        if self.time_tick.msec() % 1000 == 0 and self.download_process_flag == 1:
            self.timeDisp_singel.emit(self.time_tick)

def main():
    '''
    main
    '''
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
    except Exception as err:
        print('catch error!!!')
        print(err)

    finally:
        print('runing time is {}s '.format((nowTime()-run_time)/1000))
        #系统exit()方法确保应用程序干净的退出
        sys.exit()


if __name__ == "__main__":
    main()
    pass


