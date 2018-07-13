#
# -*- coding: utf-8 -*-

"""
In this example, we create a simple window in PyQt5.

author: chenzhipeng3472
last edited: 04-July-2018
"""

import os
import sys
import time
import serial
import serial.tools.list_ports

#这里我们提供必要的引用。基本控件位于pyqt5.qtwidgets模块中。
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel, QComboBox, QPushButton, QHBoxLayout, QVBoxLayout, QGroupBox, QGridLayout, QProgressBar, QTextBrowser)
from PyQt5.QtCore import (pyqtSignal, QTimer, QThread)

DEBUG = int(0)

CAN_HEAD = int(0xAA)
CAN_CTRL = int(0xA5)
CAN_TAIL = int(0x55)
PACK_SIZE = int(1024)
READ_SIZE = int(8)
FILE_NAME_PCIE_BASE     = str('PcieBaseBoard.bin')
FILE_NAME_DIGITAL_VIDEO = str('DigitalVideo.bin')
FILE_NAME_ANALOG_VIDEO  = str('AnalogVideo.bin')
FILE_NAME_LVDS_IN       = str('LVDSIn.bin')
FILE_NAME_DIGITAL_IO    = str('IoBoardDigital.bin')
FILE_NAME_ANALOG_IO     = str('IoBoardAnalog.bin')
FILE_NAME_POWER         = str('PowerBoard.bin')
FILE_NAME_AUDIO         = str('AudioBoard.bin')

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

nowTime = lambda:int(round(time.time()*1000))

'''
'''
class SerialComboBox(QComboBox):
    popupAboutToBeShown = pyqtSignal()

    def __init__(self, parent = None):
        super(SerialComboBox,self).__init__(parent)
        self.setMaxVisibleItems(10)

    # 重写showPopup函数
    def showPopup(self):
        # 先清空原有的选项
        self.clear()
        # self.addItem(" ")
        # self.addItem( "请选择串口号")
        # 获取接入的所有串口信息，插入combobox的选项中
        portlist = self.get_port_list(self)
        if portlist is not None:
            for i in portlist:
                self.addItem(str(i))
        QComboBox.showPopup(self)   # 弹出选项框

    @staticmethod
    # 获取接入的所有串口号
    def get_port_list(self):
        try:
            port_list = list(serial.tools.list_ports.comports())
            for port in port_list:
                yield str(port.device)
        except Exception as e:
            logging.error("获取接入的所有串口设备出错！\n错误信息："+str(e))

'''
'''
class UI_Message(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.GroupBox = QGroupBox('Message')

        self.Msg_TextEdit = QTextBrowser()
        self.Msg_TextEdit.setPlainText('initialize...\r\n')
        textCursor = self.Msg_TextEdit.textCursor()
        textCursor.movePosition(textCursor.End)
        self.Msg_TextEdit.setTextCursor(textCursor)

        # formLayout = QFormLayout()
        # formLayout.addRow(self.Msg_TextEdit)
        # self.GroupBox.setLayout(formLayout)

        # self.Msg_TextEdit.resize(500, 800)
        # hBox.addWidget(self.Msg_TextEdit)
        # self.GroupBox.resize(300, 600)
        # self.GroupBox.resize(self.GroupBox.sizeHint())

        gridLayout = QGridLayout()
        gridLayout.setSpacing(10)
        gridLayout.addWidget(self.Msg_TextEdit, 1, 0, 30, 100)
        self.GroupBox.setLayout(gridLayout)
'''
'''
class UI_Serial(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # plist = list(serial.tools.list_ports.comports())

        ser_com_label = QLabel('COM:', self)
        # ser_com_label.move(30, 20)
        # ser_com_label.resize(30, 30)

        self.ser_com_combo = SerialComboBox(self)
        # ser_com_combo.move(70, 20)
        # ser_com_combo.resize(60, 30)
        # for i in range(0, len(plist)):
            # print(plist[i])
            # self.ser_com_combo.addItem(str(plist[i].device))

        # self.ser_com_combo.setEditable(False)
        # self.ser_com_combo.clear()

        self.ser_open_button = QPushButton('close', self)
        self.ser_open_button.setCheckable(True)
        # self.ser_open_button.clicked.connect(self.switchSerial)
        # ser_open_button.move(30, 60)
        # ser_open_button.resize(100, 30)


        self.GroupBox = QGroupBox('Uart Setting')
        hBox = QHBoxLayout()
        hBox.addWidget(ser_com_label)
        hBox.addWidget(self.ser_com_combo)
        hBox.addStretch(1)  #添加空白

        vBox = QVBoxLayout()
        vBox.addLayout(hBox)
        vBox.addWidget(self.ser_open_button)
        vBox.addStretch(1)

        self.setLayout(vBox)

        self.GroupBox.setLayout(vBox)
        self.GroupBox.resize(self.GroupBox.sizeHint())


        # self.show()

    def switchSerial(self, pressed):
        source = self.sender()
        print("1")

        if source.text() == 'close':
            source.setText('open')
        else :
            val = 0

'''
'''
class UI_BoardType(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.GroupBox = QGroupBox('BoardType')

        AudioBoard_label = QLabel('Audio')
        AnalogIOBoard_label = QLabel('AnalogIO')
        DigitalIOBoard_label = QLabel('DigitalIO')
        PSConrtolBoard_label = QLabel('PSControl')
        AnalogVideoBoard_label = QLabel('AnalogVideo')
        DigitalVideoBoard_label = QLabel('DigitalVideo')
        LVDSInBoard_label = QLabel('LVDSIn')
        PcieBaseBoard_label = QLabel('PcieBase')

        gridLayout = QGridLayout()
        gridLayout.addWidget(AudioBoard_label, 2, 0)
        gridLayout.addWidget(AnalogIOBoard_label, 3, 0)
        gridLayout.addWidget(DigitalIOBoard_label, 4, 0)
        gridLayout.addWidget(PSConrtolBoard_label, 5, 0)
        gridLayout.addWidget(AnalogVideoBoard_label, 6, 0)
        gridLayout.addWidget(DigitalVideoBoard_label, 7, 0)
        gridLayout.addWidget(LVDSInBoard_label, 8, 0)
        gridLayout.addWidget(PcieBaseBoard_label, 9, 0)
        gridLayout.setSpacing(20)
        # gridLayout.setColumnStretch(0, 10)
        # gridLayout.setRowStretch(0, 10)

        self.NodeID_button =list()
        self.BoxID_button =list()
        for i in range(8):
            for j in range(8):
                # self.NodeID_button.append(QPushButton(hex(i*16+j), self))
                self.NodeID_button.append(QPushButton(' ', self))
                self.NodeID_button[i*8+j].setCheckable(False)
                # self.NodeID_button[i*8+j].clicked[bool].connect(self.selectNodeID)
                gridLayout.addWidget(self.NodeID_button[i*8+j], j+2, i+1)

            self.BoxID_button.append(QPushButton('Box '+str(i), self))
            self.BoxID_button[i].setCheckable(False)
            # self.BoxID_button[i*8+j].clicked[bool].connect(self.selectNodeID)
            gridLayout.addWidget(self.BoxID_button[i], 1, i+1)

        self.BoardRefresh_button = QPushButton('Refresh', self)
        self.BoardRefresh_button.setShortcut('F5')
        # self.BoardRefresh_button.setDown(True)
        # self.BoardRefresh_button.setDown(False)
        # BoardRefresh_button.clicked[bool].connect(self.refreshClicked)
        gridLayout.addWidget(self.BoardRefresh_button, 0, 0)

        # test_button = QPushButton('test', self)
        # test_button.setCheckable(True)
        # gridLayout.addWidget(test_button, 0, 1)

        self.Download_combo = QComboBox(self)
        self.Download_combo.addItem('Node')
        self.Download_combo.addItem('Box')
        self.Download_combo.addItem('All')
        # self.Download_combo.hidePopup()
        # self.Download_combo.setFrame(False)
        gridLayout.addWidget(self.Download_combo, 0, 1)

        self.Progress_bar = QProgressBar(self)
        self.Progress_bar.setValue(99)
        gridLayout.addWidget(self.Progress_bar, 0, 2, 1, 6)

        self.download_button = QPushButton('Download', self)
        gridLayout.addWidget(self.download_button, 0, 8)

        self.GroupBox.resize(self.GroupBox.sizeHint())
        self.GroupBox.setLayout(gridLayout)

        # self.show()


'''
'''
class UI_MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.SerialUI = UI_Serial()
        self.BoardTypeUI = UI_BoardType()
        self.MessageUI = UI_Message()

        mainLayout = QVBoxLayout()
        hboxLayout = QHBoxLayout()
        hboxLayout.addWidget(self.SerialUI.GroupBox)
        # self.MessageUI.GroupBox.addspacing(100)
        hboxLayout.addWidget(self.MessageUI.GroupBox)
        hboxLayout.addStretch(1)

        mainLayout.addLayout(hboxLayout)
        mainLayout.addWidget(self.BoardTypeUI.GroupBox)

        self.setLayout(mainLayout)

        # gridLayout = QGridLayout()
        # gridLayout.addWidget(self.SerialUI, 1, 0)
        # gridLayout.addWidget(self.BoardTypeUI, 2, 0)
        # gridLayout.addWidget(self.MessageUI, 3, 0)
        # self.setLayout(gridLayout)

        self.setGeometry(100, 100, 800, 500)
        self.setWindowTitle('ProgramUpdate')
        self.show()

        self.ProgramUpdate_thread = ProgramUpdateThread()
        self.ProgramUpdate_thread.refresh_singel.connect(self.refresh_singel)
        self.ProgramUpdate_thread.processBar_singel.connect(self.processBar_singel)
        self.ProgramUpdate_thread.message_singel.connect(self.message_singel)
        # self.ProgramUpdate_thread.start()

        # openSerial
        self.SerialUI.ser_open_button.clicked.connect(self.openSerial)

        #refreshBoard
        self.BoardTypeUI.BoardRefresh_button.clicked.connect(self.refreshBoard)

        #download_process
        self.BoardTypeUI.download_button.clicked.connect(self.download_process)

        #download_select
        self.BoardTypeUI.Download_combo.activated[str].connect(self.download_select)

    # openSerial
    def openSerial(self):
        source = self.sender()
        # print(source)
        if source.text() == 'close':
            source.setText('open')
            self.ProgramUpdate_thread.openSerial(str(self.SerialUI.ser_com_combo.currentText()))

        elif source.text() == 'open':
            source.setText('close')
            self.ProgramUpdate_thread.closeSerial()

    #selectNodeID 
    def selectNodeID(self, pressed):
        source = self.sender()
        self.ProgramUpdate_thread.selectNodeID(pressed, source.text())


    #BoardRefresh_button
    def refreshBoard(self):
        source = self.sender()
        self.ProgramUpdate_thread.refreshBoard()
        #selectNodeID 
        # for node_id in self.BoardTypeUI.NodeID_button:
            # node_id.clicked[bool].connect(self.selectNodeID)

    #refresh_singel
    def refresh_singel(self, cmd, i, j, is_down):
        if is_down == 2:
            is_down = True

        if cmd == 1:  # clear node_id
            self.BoardTypeUI.NodeID_button[i*8+j].setText('    ')
            self.BoardTypeUI.NodeID_button[i*8+j].setCheckable(False)
            self.BoardTypeUI.NodeID_button[i*8+j].clicked[bool].connect(self.selectNodeID)
            self.BoardTypeUI.NodeID_button[i*8+j].clicked[bool].disconnect(self.selectNodeID)

        if cmd == 2:  # clear box_id
            self.BoardTypeUI.BoxID_button[i].setText('    ')
            self.BoardTypeUI.BoxID_button[i].setCheckable(False)

        if cmd == 3:  # set node_id
            # print('cmd=%d, i=0x%02X, j=%d' % (cmd, i, j))
            self.BoardTypeUI.NodeID_button[(i>>4)*8+j].setText(hex(i))
            self.BoardTypeUI.NodeID_button[(i>>4)*8+j].setCheckable(True)
            self.BoardTypeUI.NodeID_button[(i>>4)*8+j].setDown(is_down)
            self.BoardTypeUI.NodeID_button[(i>>4)*8+j].clicked[bool].connect(self.selectNodeID)
            self.BoardTypeUI.BoxID_button[(i>>4)].setText('Box '+str(i>>4))
            self.BoardTypeUI.BoxID_button[(i>>4)].setCheckable(True)

    def download_process(self):
        source = self.sender()
        print(source.text())
        print(self.BoardTypeUI.Download_combo.currentText())
        # self.ProgramUpdate_thread.download_process()
        self.ProgramUpdate_thread.download_process_flag = 1
        self.ProgramUpdate_thread.start()

    def download_select(self, str):
        source = self.sender()
        print(source.currentIndex(), end=' ')
        print(source.currentText())
        # print(source.currentIndexChanged())
        self.ProgramUpdate_thread.downloadSelect(source.currentIndex())

    def processBar_singel(self, val):
        self.BoardTypeUI.Progress_bar.setValue(val)

    def message_singel(self, str):
        self.MessageUI.Msg_TextEdit.insertPlainText(str)
        textCursor = self.MessageUI.Msg_TextEdit.textCursor()
        textCursor.movePosition(textCursor.End)
        self.MessageUI.Msg_TextEdit.setTextCursor(textCursor)


'''
'''
class ProgramUpdateThread(QThread):
    #定义一个信号
    refresh_singel = pyqtSignal(int, int, int, int)
    processBar_singel = pyqtSignal(int)
    message_singel = pyqtSignal(str)

    def __init__(self):
        super(ProgramUpdateThread, self).__init__()
        self.ser = serial.Serial()  #/dev/ttyUSB0

        #node_id_list
        self.node_id_pcie_base_need_program = list()
        self.node_id_digital_video_need_program = list()
        self.node_id_analog_video_need_program = list()
        self.node_id_lvds_in_need_program = list()
        self.node_id_digital_need_program = list()
        self.node_id_analog_need_program = list()
        self.node_id_power_need_program = list()
        self.node_id_audio_need_program = list()
        self.node_id_need_program = list()
        self.box_id_need_program = list()

        self.box_id_exist = list()
        self.node_id_pcie_base = list()
        self.node_id_digital_video = list()
        self.node_id_analog_video = list()
        self.node_id_lvds_in = list()
        self.node_id_digital = list()
        self.node_id_analog = list()
        self.node_id_power = list()
        self.node_id_audio = list()
        self.node_id_all_exist = list()

        #----initialize----QTimer 任务
        self.tick = int(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timeout_slot)
        # self.timer.start(9000)
        #----end---- 

        self.download_process_flag = 0
        self.download_select = 0

    def run(self):
        while True:
            if self.download_process_flag == 1:
                self.download_process2()
                break

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


    # openSerial
    def openSerial(self, COMn):
        try:
            self.ser = serial.Serial(COMn, 115200, timeout=0.0000001)  #/dev/ttyUSB0

            if  self.ser.isOpen():
                print("打开成功 -> %s" % (self.ser.port))
                self.message_singel.emit('打开成功 -> '+ COMn + '\r\n')
            else:
                print("打开失败,请检查串口后重启程序!")
                self.message_singel.emit("打开失败,请检查串口后重启程序!\r\n")
        except:
            print("***打开失败,请检查串口是否被占用或其他异常!!!")
            self.message_singel.emit("***打开失败,请检查串口是否被占用或其他异常!!!\r\n")

    def closeSerial(self):
        try:
            if  self.ser.isOpen():
                self.ser.close()
                print("关闭成功 -> %s" % (self.ser.port))
                self.message_singel.emit('关闭成功 -> '+ str(self.ser.port) + '\r\n')
            else:
                print("关闭失败,请检查串口后重启程序!")
                self.message_singel.emit("关闭失败,请检查串口后重启程序!\r\n")
            # self.SerialUI.ser_com_combo.setEnable(True)
        except ( IndexError,AttributeError, SyntaxError, NameError, TypeError) as err:
            print(err)
            print("***打开失败,请检查串口是否被占用或其他异常!!!")
            self.message_singel.emit("***打开失败,请检查串口是否被占用或其他异常!!!\r\n")

    def selectNodeID(self, pressed, input_node_str):
        input_node_id = eval('[%s]'% input_node_str)
        print(input_node_id)

        if pressed:
            print(input_node_str + ' select')
            if (input_node_id[0] in self.node_id_all_exist):
                self.node_id_need_program.append(input_node_id[0])

            if (input_node_id[0] in self.node_id_analog):
                self.node_id_analog_need_program.append(input_node_id[0])

            elif (input_node_id[0] in self.node_id_digital):
                self.node_id_digital_need_program.append(input_node_id[0])

            elif (input_node_id[0] in self.node_id_audio):
                self.node_id_audio_need_program.append(input_node_id[0])

            elif (input_node_id[0] in self.node_id_power):
                self.node_id_power_need_program.append(input_node_id[0])

            elif (input_node_id[0] in self.node_id_digital_video):
                self.node_id_digital_video_need_program.append(input_node_id[0])

            elif (input_node_id[0] in self.node_id_analog_video):
                self.node_id_analog_video_need_program.append(input_node_id[0])

            elif (input_node_id[0] in self.node_id_lvds_in):
                self.node_id_lvds_in_need_program.append(input_node_id[0])

            elif (input_node_id[0] in self.node_id_pcie_base):
                self.node_id_pcie_base_need_program.append(input_node_id[0])

        else:
            print(input_node_str + ' unselect')
            if (input_node_id[0] in self.node_id_need_program):
                self.node_id_need_program.remove(input_node_id[0])

            if (input_node_id[0] in self.node_id_analog_need_program):
                self.node_id_analog_need_program.remove(input_node_id[0])

            elif (input_node_id[0] in self.node_id_digital_need_program):
                self.node_id_digital_need_program.remove(input_node_id[0])

            elif (input_node_id[0] in self.node_id_audio_need_program):
                self.node_id_audio_need_program.remove(input_node_id[0])

            elif (input_node_id[0] in self.node_id_power_need_program):
                self.node_id_power_need_program.remove(input_node_id[0])

            elif (input_node_id[0] in self.node_id_digital_video_need_program):
                self.node_id_digital_video_need_program.remove(input_node_id[0])

            elif (input_node_id[0] in self.node_id_analog_video_need_program):
                self.node_id_analog_video_need_program.remove(input_node_id[0])

            elif (input_node_id[0] in self.node_id_lvds_in_need_program):
                self.node_id_lvds_in_need_program.remove(input_node_id[0])

            elif (input_node_id[0] in self.node_id_pcie_base_need_program):
                self.node_id_pcie_base_need_program.remove(input_node_id[0])

        self.node_id_need_program = list(set(self.node_id_need_program))  # 设为集合再设回列表，清除重复数值
        self.node_id_analog_need_program = list(set(self.node_id_analog_need_program))  # 设为集合再设回列表，清除重复数值
        self.node_id_digital_need_program = list(set(self.node_id_digital_need_program))  # 设为集合再设回列表，清除重复数值
        self.node_id_audio_need_program = list(set(self.node_id_audio_need_program))  # 设为集合再设回列表，清除重复数值
        self.node_id_power_need_program = list(set(self.node_id_power_need_program))  # 设为集合再设回列表，清除重复数值
        self.node_id_digital_video_need_program = list(set(self.node_id_digital_video_need_program))  # 设为集合再设回列表，清除重复数值
        self.node_id_analog_video_need_program = list(set(self.node_id_analog_video_need_program))  # 设为集合再设回列表，清除重复数值
        self.node_id_lvds_in_need_program = list(set(self.node_id_lvds_in_need_program))  # 设为集合再设回列表，清除重复数值
        self.node_id_pcie_base_need_program = list(set(self.node_id_pcie_base_need_program))  # 设为集合再设回列表，清除重复数值
        print(", ".join(hex(i) for i in self.node_id_need_program))
        print('  1、模拟IO板卡  : %s' % " ".join(hex(i) for i in self.node_id_analog_need_program))
        print('  2、数字IO板卡  : %s' % " ".join(hex(i) for i in self.node_id_digital_need_program))
        print('  3、音频板卡    : %s' % " ".join(hex(i) for i in self.node_id_audio_need_program))
        print('  4、电源控制板卡: %s' % " ".join(hex(i) for i in self.node_id_power_need_program))
        print('  5、数字信号板卡: %s' % " ".join(hex(i) for i in self.node_id_digital_video_need_program))
        print('  6、模拟信号板卡: %s' % " ".join(hex(i) for i in self.node_id_analog_video_need_program))
        print('  7、LVDS_IN 板卡: %s' % " ".join(hex(i) for i in self.node_id_lvds_in_need_program))
        print('  8、底板 板卡   : %s' % " ".join(hex(i) for i in self.node_id_pcie_base_need_program))

    #BoardRefresh_button
    def refreshBoard(self):
        if  self.ser.isOpen():
            self.message_singel.emit('刷新节点.\r\n')
            pass
        else:
            print('please select uart and open it!')
            self.message_singel.emit('请检查串口是否打开！\r\n')
            return

        for i in range(8):
            for j in range(8):
                self.refresh_singel.emit(1, i, j, 0)
            self.refresh_singel.emit(2, i, j, 0)


        self.node_id_all_exist.clear()
        self.node_id_audio.clear()
        self.node_id_analog.clear()
        self.node_id_digital.clear()
        self.node_id_power.clear()
        self.node_id_analog_video.clear()
        self.node_id_digital_video.clear()
        self.node_id_lvds_in.clear()
        self.node_id_pcie_base.clear()
        self.node_id_need_program.clear()
        self.node_id_analog_need_program.clear()
        self.node_id_digital_need_program.clear()
        self.node_id_audio_need_program.clear()
        self.node_id_power_need_program.clear()
        self.node_id_digital_video_need_program.clear()
        self.node_id_analog_video_need_program.clear()
        self.node_id_lvds_in_need_program.clear()
        self.node_id_pcie_base_need_program.clear()

        # print(", ".join(hex(i) for i in self.node_id_need_program))
        # print('  1、模拟IO板卡  : %s' % " ".join(hex(i) for i in self.node_id_analog_need_program))
        # print('  2、数字IO板卡  : %s' % " ".join(hex(i) for i in self.node_id_digital_need_program))
        # print('  3、音频板卡    : %s' % " ".join(hex(i) for i in self.node_id_audio_need_program))
        # print('  4、电源控制板卡: %s' % " ".join(hex(i) for i in self.node_id_power_need_program))
        # print('  5、数字信号板卡: %s' % " ".join(hex(i) for i in self.node_id_digital_video_need_program))
        # print('  6、模拟信号板卡: %s' % " ".join(hex(i) for i in self.node_id_analog_video_need_program))
        # print('  7、LVDS_IN 板卡: %s' % " ".join(hex(i) for i in self.node_id_lvds_in_need_program))
        # print('  8、底板 板卡   : %s' % " ".join(hex(i) for i in self.node_id_pcie_base_need_program))

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
        for node_id in node_id_all:
            self.send_start_command(self.ser, node_id)
            time.sleep(0.005)
            while self.ser.inWaiting() > 0:
                data = self.ser.read_all()
            if data != '' :
                data = self.find_start_head(data)
                # print(" ".join(hex(i) for i in data))

                # print('123')
                if data[7] == AUDIO_BOARD:
                    self.node_id_audio.append(data[6])
                    self.node_id_all_exist.append(data[6])
                    if (data[6]>>4) not in self.box_id_exist:
                        self.box_id_exist.append(data[6]>>4)
                    self.refresh_singel.emit(3, data[6], 0, self.download_select)
                    if self.download_select == 2:
                        self.node_id_need_program.append(data[6])
                        self.node_id_audio_need_program.append(data[6])


                elif data[7] == POWER_BOARD:
                    self.node_id_power.append(data[6])
                    self.node_id_all_exist.append(data[6])
                    if (data[6]>>4) not in self.box_id_exist:
                        self.box_id_exist.append(data[6]>>4)
                    self.refresh_singel.emit(3, data[6], 3, self.download_select)
                    if self.download_select == 2:
                        self.node_id_need_program.append(data[6])
                        self.node_id_power_need_program.append(data[6])

                elif data[7] == IO_ANALOG_BOARD:
                    self.node_id_analog.append(data[6])
                    self.node_id_all_exist.append(data[6])
                    if (data[6]>>4) not in self.box_id_exist:
                        self.box_id_exist.append(data[6]>>4)
                    self.refresh_singel.emit(3, data[6], 1, self.download_select)
                    if self.download_select == 2:
                        self.node_id_need_program.append(data[6])
                        self.node_id_analog_need_program.append(data[6])

                elif data[7] == IO_DIGITAL_BOARD:
                    self.node_id_digital.append(data[6])
                    self.node_id_all_exist.append(data[6])
                    if (data[6]>>4) not in self.box_id_exist:
                        self.box_id_exist.append(data[6]>>4)
                    self.refresh_singel.emit(3, data[6], 2, self.download_select)
                    if self.download_select == 2:
                        self.node_id_need_program.append(data[6])
                        self.node_id_digital_need_program.append(data[6])

                elif data[7] == ANALOG_VIDEO_BOARD:
                    self.node_id_analog_video.append(data[6])
                    self.node_id_all_exist.append(data[6])
                    if (data[6]>>4) not in self.box_id_exist:
                        self.box_id_exist.append(data[6]>>4)
                    self.refresh_singel.emit(3, data[6], 4, self.download_select)
                    if self.download_select == 2:
                        self.node_id_need_program.append(data[6])
                        self.node_id_analog_video_need_program.append(data[6])

                elif data[7] == DIGITAL_VIDEO_BOARD:
                    self.node_id_digital_video.append(data[6])
                    self.node_id_all_exist.append(data[6])
                    if (data[6]>>4) not in self.box_id_exist:
                        self.box_id_exist.append(data[6]>>4)
                    self.refresh_singel.emit(3, data[6], 5, self.download_select)
                    if self.download_select == 2:
                        self.node_id_need_program.append(data[6])
                        self.node_id_digital_video_need_program.append(data[6])

                elif data[7] == LVDS_IN_BOARD:
                    self.node_id_lvds_in.append(data[6])
                    self.node_id_all_exist.append(data[6])
                    if (data[6]>>4) not in self.box_id_exist:
                        self.box_id_exist.append(data[6]>>4)
                    self.refresh_singel.emit(3, data[6], 6, self.download_select)
                    if self.download_select == 2:
                        self.node_id_need_program.append(data[6])
                        self.node_id_lvds_in_need_program.append(data[6])

                elif data[7] == PCIE_BASE_BOARD:
                    self.node_id_pcie_base.append(data[6])
                    self.node_id_all_exist.append(data[6])
                    if (data[6]>>4) not in self.box_id_exist:
                        self.box_id_exist.append(data[6]>>4)
                    self.refresh_singel.emit(3, data[6], 7, self.download_select)
                    if self.download_select == 2:
                        self.node_id_need_program.append(data[6])
                        self.node_id_pcie_base_need_program.append(data[6])


                data = ''

        print(", ".join(hex(i) for i in self.node_id_all_exist))
        print('  1、音频板卡    : %s' % " ".join(hex(i) for i in self.node_id_audio))
        print('  2、模拟IO板卡  : %s' % " ".join(hex(i) for i in self.node_id_analog))
        print('  3、数字IO板卡  : %s' % " ".join(hex(i) for i in self.node_id_digital))
        print('  4、电源控制板卡: %s' % " ".join(hex(i) for i in self.node_id_power))
        print('  5、模拟信号板卡: %s' % " ".join(hex(i) for i in self.node_id_analog_video))
        print('  6、数字信号板卡: %s' % " ".join(hex(i) for i in self.node_id_digital_video))
        print('  7、LVDS_IN 板卡: %s' % " ".join(hex(i) for i in self.node_id_lvds_in))
        print('  8、底板 板卡   : %s' % " ".join(hex(i) for i in self.node_id_pcie_base))


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
                return data[i:i+21]

    def send_command_ctrl_deal(self, send_data):
        send_data2 = list(send_data)        # another list, 创建了的内存
        ctrl_times = int(0)
        for send_i, send_data_each in enumerate(send_data2[2:-2]):
            if send_data_each == CAN_HEAD or send_data_each == CAN_CTRL or send_data_each == CAN_TAIL :
                # print(send_i, send_data_each)
                send_data.insert(send_i+ctrl_times+2, CAN_CTRL)
                ctrl_times = ctrl_times + 1
                # send_i = send_i + 1
                # print(send_data)
                # print(send_data2)

        # print(send_data)
        # print(send_data2)
        # print(send_data2 is send_data)
        return send_data

    def download_process(self):
        if  self.ser.isOpen() and len(self.node_id_need_program) > 0:
            self.message_singel.emit('下载程序...\r\n')
        else:
            print('please open uart and select update node!')
            self.message_singel.emit('请检查串口并选择节点！\r\n')
            self.download_process_flag = 0
            return
        #---- 判断文件名以及创建时间和文件大小---
        if len(self.node_id_pcie_base_need_program) > 0:
            self.Is_file_exist(self.node_id_pcie_base_need_program, FILE_NAME_PCIE_BASE)

        if len(self.node_id_digital_video_need_program) > 0:
            self.Is_file_exist(self.node_id_digital_video_need_program, FILE_NAME_DIGITAL_VIDEO)

        if len(self.node_id_analog_video_need_program) > 0:
            self.Is_file_exist(self.node_id_analog_video_need_program, FILE_NAME_ANALOG_VIDEO)

        if len(self.node_id_lvds_in_need_program) > 0:
            self.Is_file_exist(self.node_id_lvds_in_need_program, FILE_NAME_LVDS_IN)

        if len(self.node_id_digital_need_program) > 0:
            self.Is_file_exist(self.node_id_digital_need_program, FILE_NAME_DIGITAL_IO)

        if len(self.node_id_analog_need_program) > 0:
            self.Is_file_exist(self.node_id_analog_need_program, FILE_NAME_ANALOG_IO)

        if len(self.node_id_power_need_program) > 0:
            self.Is_file_exist(self.node_id_power_need_program, FILE_NAME_POWER)

        if len(self.node_id_audio_need_program) > 0:
            self.Is_file_exist(self.node_id_audio_need_program, FILE_NAME_AUDIO)
        #---- end---

        self.send_file_state = int(1)
        self.Download_state = int(1)
        self.timer.start(200)
        print('timer start')
        self.download_process_flag = 0


    def Is_file_exist(self, node_id_need_program, file_name):
        Is_File_exist = os.path.exists(file_name)
        if Is_File_exist:
            size = os.path.getsize(file_name)
            creat_time = os.path.getmtime(file_name)
            print('')
            print("请按回车键确认需要升级的文件名以及文件创建时间和文件大小！！！")
            print("%s  %s  %d bytes" % (file_name, self.TimeStampToTime(creat_time), size))
            # if DEBUG != 1:
                # input("\r\n")
        else:
            print("找不到该文件  %s , 请放置该文件到该目录下,放置后请按回车键确认" % (file_name))
            # input()

    def send_reset_iwdg_command(self, ser, node_id):
        # send = [AA AA 12 02 00 00 99 00 00 00 00 00 00 06 08 00 00 00 BB 55 55]
        send = [0xAA, 0xAA,
                node_id, 0x02, 0x00, 0x00,
                0x99, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, E_CMD_RESER,
                0x08, 0x00, 0x00, 0x00,
                0x15,
                0x55 , 0x55
                ]
        send[18] = (send[2]+send[3]+send[6]+send[13]+send[14])&0xff
        send = self.send_command_ctrl_deal(send)
        # print(" ".join(hex(i) for i in send))
        ser.write(send)
        print("发送重启指令：节点： 0x%02X " % (node_id))
        # print("send_reset_command...1.1 node_id = 0x%02X " % (node_id))

    def send_erase_commane(self, ser, node_id):
        send = [0xAA, 0xAA,
                node_id, 0x02, 0x00, 0x00,
                0x01, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, E_CMD_UPDATE,
                0x08, 0x00, 0x00, 0x00,
                0x20,
                0x55 , 0x55
                ]
        send[18] = (send[2]+send[3]+send[6]+send[9]+send[13]+send[14])&0xff
        send = self.send_command_ctrl_deal(send)
        # print(" ".join(hex(i) for i in send))
        ser.write(send)
        print("send_erase_commane...2  node_id = 0x%02X " % (node_id))
        # y = str(bytearray(send))
        # print(y)

    def TimeStampToTime(self, timestamp):
        timeStruct = time.localtime(timestamp)
        return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)

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
                else:
                    print("找不到该文件  %s , 请放置该文件到该目录下,放置后请按回车键确认" % (file_name))

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

                print('send_file_data ...1')
                f_bin.seek(send_tell)
                send_cnt = send_tell//PACK_SIZE
                if send_cnt < (size_high+1):
                # while self.send_cnt < (size_high+1):
                # for (send_cnt) in  range(size_high+1):
                #----start--- 发送装载数据命令
                    # print('send_file_data ...2')
                    self.send_data_command(self.ser, node_id_need_program)
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
                    self.message_singel.emit(file_name + ' -> ' + str(round(f_bin.tell()/self.size*100, 1)) + '% \r\n')
                    self.old_tell = f_bin.tell()
                    send_tell = f_bin.tell()

                #----start--- 发送烧录命令
                    self.send_program_command(self.ser, check_sum_1K, node_id_need_program)
                #----end-----
                    # time.sleep(0.001)


        elif send_file_state == 3:
            send_file_state = 0
            # send_file_ret = 0
            send_tell = 0

        return send_tell, send_file_state

    def send_data_command(self, ser, node_ids):
        # print("send_data_command...1")
        for node_id in node_ids:
            send = [0xAA, 0xAA,
                    0x12, 0x02, 0x00, 0x00,
                    0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, E_CMD_UPDATE,
                    0x08, 0x00, 0x00, 0x00,
                    0x20,
                    0x55 , 0x55
                    ]
            send[2] = node_id
            send[18] = (send[2]+send[3]+send[6]+send[13]+send[14])&0xff
            send = self.send_command_ctrl_deal(send)
            # print(" ".join(hex(i) for i in send))
            ser.write(send)
            # print("send_data_command...3  node_id = 0x%02X " % (node_id))

    def send_1K_bin_data(self, ser, f_bin, node_ids):
        check_sum_1K = int()
        # print(f_bin.seek(1024))
        # print(f_bin.tell())
        for i in range(0, PACK_SIZE//READ_SIZE):
            f_bin_data = f_bin.read(READ_SIZE)
            # f_bin_data = [ 0x88, 0x00, 0x00, 0x00, 0x00, 0xA0, 0x5A, 0x01]
            # f_bin_data = [ 0xA5, 0xA5, 0xA5, 0x00, 0x00, 0xA5, 0x00, 0x01]
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
                # print(hex(check_sum))
                # check = list(check_sum)
                # send_data.append(check)
                send_data[10] = check_sum&0xff
                send_data = send_data[0:6:1] +f_bin_data + send_data[6::1]

                send_data = self.send_command_ctrl_deal(send_data)
                # print(i)
                # if(i >= 21):
                    # sleep(3)
                    # print(send_data)
                # print(" ".join(hex(i) for i in send_data))
                ser.write(send_data) #数据写回
                # input("按回车键继续")

            check_sum_1K += sum(f_bin_data)
            # sleep(0.02)
        # print(f_bin.tell())
        return check_sum_1K

    def send_program_command(self, ser, check_sum, node_ids):
        for node_id in node_ids:
            send = [0xAA, 0xAA,
                    0x12, 0x02, 0x00, 0x00,
                    0x03,
                    0x08, 0x00, 0x00, 0x00,
                    0x20,
                    0x55 , 0x55
                    ]
            send_check_sum_1K = [(check_sum>>0)&0xff,
                                    (check_sum>>8)&0xff,
                                    (check_sum>>16)&0xff,
                                    (check_sum>>24)&0xff,
                                    0x00,
                                    0x00,
                                    0x02
                                ]
            send[2] = node_id
            check_sum_1K_program = (send[2]+send[3]+send[6]+send[7]+sum(send_check_sum_1K))&0xff
            send[11] = check_sum_1K_program
            send = send[0:7:1] +send_check_sum_1K + send[7::1]
            send = self.send_command_ctrl_deal(send)
            ser.write(send)
            # print(hex(check_sum_1K_program))
            # print(send)
            # print("send_program_command...4  node_id = 0x%02X " % (node_id))

    def send_command_reboot(self, ser, node_ids):
        for node_id in node_ids:
            send = [0xAA, 0xAA,
                    0x12, 0x02, 0x00, 0x00,
                    0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02,
                    0x08, 0x00, 0x00, 0x00,
                    0x22,
                    0x55 , 0x55
                    ]
            send[2] = node_id
            send[18] = (send[2]+send[3]+send[6]+send[13]+send[14])&0xff
            send = self.send_command_ctrl_deal(send)
            # print(" ".join(hex(i) for i in send))
            ser.write(send)
            print("send_command_reboot...  node_id = 0x%02X " % (node_id))

    def timeout_slot(self):
        self.tick = self.tick + 1
        print('tick=%d ' % (self.tick))

        if self.Download_state == 1: #---- 复位看门狗---
            data = ''
            node_id_cnt = int(0)
            for node_id in self.node_id_need_program:
                self.send_reset_iwdg_command(self.ser, node_id)
                self.message_singel.emit('发送重启指令：节点：' + str(hex(node_id)) + ' \r\n')
                while True:
                    while self.ser.inWaiting() > 0:
                        data = self.ser.read_all()
                        # print(data)
                    if data != '' and len(data) > 41 and data [2]< 0x90 and data[23] == node_id:
                        # print(" ".join(hex(i) for i in data))
                        node_id_cnt+=1
                        print("重启成功 节点%d --> 0x%02X" % (node_id_cnt, data[23]))
                        self.message_singel.emit('重启成功 --> ' + str(hex(data[23])) + ' \r\n')

                    #----start--- 发送启动命令
                        self.send_start_command(self.ser, node_id)
                    #----end-----
                        time.sleep(0.01)

                    #----start--- 发送擦除扇区命令
                        self.send_erase_commane(self.ser, node_id)
                    #----end-----

                            # data = ''
                        break;
                        data = ''
            time.sleep(2)
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
            if len(self.node_id_pcie_base_need_program) > 0:
                # if self.send_file_audio_ret !=0 :kkkkkkkkkkkkkkkkkkkkk
                self.send_file_pcie_base_tell, self.send_file_pcie_base_ret = self.send_file_data(FILE_NAME_PCIE_BASE, self.send_file_pcie_base_ret, self.send_file_pcie_base_tell, self.node_id_pcie_base_need_program)

            if len(self.node_id_digital_video_need_program) > 0:
                self.send_file_digital_video_tell, self.send_file_digital_video_ret = self.send_file_data(FILE_NAME_DIGITAL_VIDEO, self.send_file_digital_video_ret, self.send_file_digital_video_tell, self.node_id_digital_video_need_program)

            if len(self.node_id_analog_video_need_program) > 0:
                self.send_file_analog_video_tell, self.send_file_analog_video_ret = self.send_file_data(FILE_NAME_ANALOG_VIDEO, self.send_file_analog_video_ret, self.send_file_analog_video_tell, self.node_id_analog_video_need_program)

            if len(self.node_id_lvds_in_need_program) > 0:
                self.send_file_lvds_in_tell, self.send_file_lvds_in_ret = self.send_file_data(FILE_NAME_LVDS_IN, self.send_file_lvds_in_ret, self.send_file_lvds_in_tell, self.node_id_lvds_in_need_program)

            if len(self.node_id_digital_need_program) > 0:
                self.send_file_io_digital_tell, self.send_file_io_digital_ret = self.send_file_data(FILE_NAME_DIGITAL_IO, self.send_file_io_digital_ret, self.send_file_io_digital_tell, self.node_id_digital_need_program)

            if len(self.node_id_analog_need_program) > 0:
                self.send_file_io_analog_tell, self.send_file_io_analog_ret = self.send_file_data(FILE_NAME_ANALOG_IO, self.send_file_io_analog_ret, self.send_file_io_analog_tell, self.node_id_analog_need_program)

            if len(self.node_id_power_need_program) > 0:
                self.send_file_power_tell, self.send_file_power_ret = self.send_file_data(FILE_NAME_POWER, self.send_file_power_ret, self.send_file_power_tell, self.node_id_power_need_program)

            if len(self.node_id_audio_need_program) > 0:
                self.send_file_audio_tell, self.send_file_audio_ret = self.send_file_data(FILE_NAME_AUDIO, self.send_file_audio_ret, self.send_file_audio_tell, self.node_id_audio_need_program)

            if self.send_file_pcie_base_ret == 0 and self.send_file_digital_video_ret == 0 and self.send_file_analog_video_ret == 0 and self.send_file_lvds_in_ret == 0 and self.send_file_io_digital_ret == 0 and self.send_file_io_analog_ret == 0 and self.send_file_power_ret == 0 and self.send_file_audio_ret == 0:
                self.Download_state = 3

        elif self.Download_state == 3: #----start--- 发送重启命令
            self.send_command_reboot(self.ser, self.node_id_need_program)
            Is_upgrade_OK = int(1)
            reboot_start_time = time.time()
            reboot_time = time.time()
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

            self.Download_state = 4

        elif self.Download_state == 4:
            if len(self.node_id_need_program) > 0:
                print('升级失败节点: %s' % " ".join(hex(i) for i in self.node_id_need_program))
                for node_id in self.node_id_need_program:
                    self.message_singel.emit('---升级失败节点 --> ' + str(hex(node_id)) + ' \r\n')

            print('升级结束，请重启机箱，并确认各板卡绿灯全亮！')
            self.message_singel.emit('升级结束，请重启机箱，并确认各板卡绿灯全亮！\r\n')
            # time.sleep(1)
            # self.ser.close()
            print('runing time is {}s '.format((nowTime()-run_time)/1000))

            self.Download_state = 1
            self.timer.stop()
            self.download_process_flag = 0


    def download_process2(self):
        if  self.ser.isOpen():
            self.message_singel.emit('下载程序...\r\n')
        else:
            print('please select uart and open it!')
            self.message_singel.emit('请检查串口并选择节点！\r\n')
            self.download_process_flag = 0
            return
        #---- 判断文件名以及创建时间和文件大小---
        if len(self.node_id_pcie_base_need_program) > 0:
            self.Is_file_exist(self.node_id_pcie_base_need_program, FILE_NAME_PCIE_BASE)

        if len(self.node_id_digital_video_need_program) > 0:
            self.Is_file_exist(self.node_id_digital_video_need_program, FILE_NAME_DIGITAL_VIDEO)

        if len(self.node_id_analog_video_need_program) > 0:
            self.Is_file_exist(self.node_id_analog_video_need_program, FILE_NAME_ANALOG_VIDEO)

        if len(self.node_id_lvds_in_need_program) > 0:
            self.Is_file_exist(self.node_id_lvds_in_need_program, FILE_NAME_LVDS_IN)

        if len(self.node_id_digital_need_program) > 0:
            self.Is_file_exist(self.node_id_digital_need_program, FILE_NAME_DIGITAL_IO)

        if len(self.node_id_analog_need_program) > 0:
            self.Is_file_exist(self.node_id_analog_need_program, FILE_NAME_ANALOG_IO)

        if len(self.node_id_power_need_program) > 0:
            self.Is_file_exist(self.node_id_power_need_program, FILE_NAME_POWER)

        if len(self.node_id_audio_need_program) > 0:
            self.Is_file_exist(self.node_id_audio_need_program, FILE_NAME_AUDIO)
        #---- end---

        #---- 复位看门狗---
        data = ''
        node_id_cnt = int(0)
        for node_id in self.node_id_need_program:
            # send_reset_iwdg_command(ser, node_id, node_id_need_program[0])
            self.send_reset_iwdg_command(self.ser, node_id)
            self.message_singel.emit('发送重启指令：节点：' + str(hex(node_id)) + ' \r\n')
            while True:
                while self.ser.inWaiting() > 0:
                    data = self.ser.read_all()
                    # print(data)
                if data != '' and len(data) > 41 and data [2]< 0x90 and data[23] == node_id:
                    # print(" ".join(hex(i) for i in data))
                    node_id_cnt+=1
                    print("重启成功 节点%d --> 0x%02X" % (node_id_cnt, data[23]))
                    self.message_singel.emit('重启成功 --> ' + str(hex(data[23])) + ' \r\n')

                #----start--- 发送启动命令
                    self.send_start_command(self.ser, node_id)
                #----end-----

                #----start--- 发送擦除扇区命令
                    self.send_erase_commane(self.ser, node_id)
                #----end-----

                        # data = ''
                    break;
                    data = ''
                    # break;
        #---end---

        #----start--- 下载程序
        time.sleep(2)
        # time.sleep(2/(len(node_id_need_program)))
        if len(self.node_id_audio_need_program) > 0:
            self.send_file_data2(FILE_NAME_AUDIO, self.node_id_audio_need_program)

        if len(self.node_id_analog_need_program) > 0:
            self.send_file_data2(FILE_NAME_ANALOG_IO, self.node_id_analog_need_program)

        if len(self.node_id_digital_need_program) > 0:
            self.send_file_data2(FILE_NAME_DIGITAL_IO, self.node_id_digital_need_program)

        if len(self.node_id_power_need_program) > 0:
            self.send_file_data2(FILE_NAME_POWER, self.node_id_power_need_program)

        if len(self.node_id_analog_video_need_program) > 0:
            self.send_file_data2(FILE_NAME_ANALOG_VIDEO, self.node_id_analog_video_need_program)

        if len(self.node_id_digital_video_need_program) > 0:
            self.send_file_data2(FILE_NAME_DIGITAL_VIDEO, self.node_id_digital_video_need_program)

        if len(self.node_id_lvds_in_need_program) > 0:
            self.send_file_data2(FILE_NAME_LVDS_IN, self.node_id_lvds_in_need_program)

        if len(self.node_id_pcie_base_need_program) > 0:
            self.send_file_data2(FILE_NAME_PCIE_BASE, self.node_id_pcie_base_need_program)

        #----end-----

        #----start--- 发送重启命令
        self.send_command_reboot(self.ser, self.node_id_need_program)
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

        #----end-----

        if len(self.node_id_need_program) > 0:
            print('升级失败节点: %s' % " ".join(hex(i) for i in self.node_id_need_program))
            self.message_singel.emit('---升级失败节点 --> ' )
            for node_id in self.node_id_need_program:
                self.message_singel.emit(str(hex(node_id)) + ', ')
            self.message_singel.emit(' \r\n')

        print('升级结束，请重启机箱，并确认各板卡绿灯全亮！')
        self.message_singel.emit('升级结束，请重启机箱，并确认各板卡绿灯全亮！\r\n')
        time.sleep(1)
        # self.ser.close()
        print('runing time is {}s '.format((nowTime()-run_time)/1000))
        self.download_process_flag = 0

    def send_file_data2(self, file_name, node_id_need_program):
        Is_File_exist = int(0)
        while Is_File_exist == 0:
            Is_File_exist = os.path.exists(file_name)
            if Is_File_exist:
                size = os.path.getsize(file_name)
                creat_time = os.path.getmtime(file_name)
                print('')
                print("%s  %s  %d bytes" % (file_name, self.TimeStampToTime(creat_time), size))
                print('正在升级...  ',  end='')
                print(" ".join(hex(i) for i in node_id_need_program))
            else:
                print("找不到该文件  %s , 请放置该文件到该目录下,放置后请按回车键确认" % (file_name))
                input()

        size_high = size//PACK_SIZE  # 1K的倍数
        size_low = size%PACK_SIZE   # 1K的余数
        size_low_8_high = size_low//READ_SIZE                  # 1K的余数 ， 8字节的倍数
        size_low_8_low = size_low%READ_SIZE                # 1K的余数 ， 8字节的余数
        # print("size_high %d, size_low %d, size_low_8_high %d  , size_low_8_low %d " % (size_high, size_low, size_low_8_high, size_low_8_low))
#----start--- 打开文件串口发送操作
        # process_bar = tqdm((range(size)), ncols = 60)
        # process_bar = ShowProcess(size, 'OK')
        with open(file_name, 'rb') as f_bin:
            self.message_singel.emit('正在升级 ' + file_name + '   ...' ' \r\n')
            # print('send_file_data ...1')
            old_tell = f_bin.tell()
            for (i) in  range(size_high+1):
            #----start--- 发送装载数据命令
                # print('send_file_data ...2')
                self.send_data_command(self.ser, node_id_need_program)
            #----end-----
                # sleep(3)

                if(i == size_high):                                 #最后1K字节发送
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
                else:
                #----start--- 发送1K数据
                    # print('send_file_data ...3')
                    check_sum_1K = self.send_1K_bin_data(self.ser, f_bin, node_id_need_program)
                    # print(hex(check_sum_1K))
                #----end---

                # process_bar.write(f_bin.tell()- old_tell, end='\r')
                # process_bar.update(f_bin.tell()- old_tell)
                # process_bar.show_process(i=(f_bin.tell()))
                # print('\r', end='\r')
                # print('', end='\1b[nA')
                # sys.stdout.flush()
                # # process_bar.clear(nolock = True)
                # self.BoardTypeUI.Progress_bar.setValue((f_bin.tell()/size)*100)
                # print('send_file_data ...4')
                self.processBar_singel.emit((f_bin.tell()/size)*100)
                # self.message_singel.emit(file_name + ' -> ' + str(round(f_bin.tell()/size*100, 1)) + '% \r\n')
                # print('send_file_data ...5')
                old_tell = f_bin.tell()

            #----start--- 发送烧录命令
                self.send_program_command(self.ser, check_sum_1K, node_id_need_program)
            #----end-----
                time.sleep(0.15)
            self.message_singel.emit('   ' + file_name + '   升级完成！' ' \r\n')
'''
'''
class NodeID(object):

    def __init__(self, ser):
        self.node_id_pcie_base_need_program = list()
        self.node_id_digital_video_need_program = list()
        self.node_id_analog_video_need_program = list()
        self.node_id_lvds_in_need_program = list()
        self.node_id_digital_need_program = list()
        self.node_id_analog_need_program = list()
        self.node_id_power_need_program = list()
        self.node_id_audio_need_program = list()

        self.box_id_need_program = list()

        self.node_id_pcie_base = list()
        self.node_id_digital_video = list()
        self.node_id_analog_video = list()
        self.node_id_lvds_in = list()
        self.node_id_digital = list()
        self.node_id_analog = list()
        self.node_id_power = list()
        self.node_id_audio = list()
        self.node_id_all_exist = list()
        self.ser = ser
        self.find_exist_node_id()

    def find_exist_node_id():
        node_id_all = list(range(0x12, 0x20))
        for node_id_temp in range(0x02, 0x10):
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
            self.send_start_command(self.ser, node_id)
            time.sleep(0.005)
            while self.ser.inWaiting() > 0:
                data = self.ser.read_all()
            if data != '' :
                data = find_start_head(data)
                # print(" ".join(hex(i) for i in data))

                if data[7] == AUDIO_BOARD:
                    node_id_audio.append(data[6])
                    self.node_id_all_exist.append(data[6])
                elif data[7] == POWER_BOARD:
                    node_id_power.append(data[6])
                    self.node_id_all_exist.append(data[6])
                elif data[7] == IO_ANALOG_BOARD:
                    node_id_analog.append(data[6])
                    self.node_id_all_exist.append(data[6])
                elif data[7] == IO_DIGITAL_BOARD:
                    node_id_digital.append(data[6])
                    self.node_id_all_exist.append(data[6])
                elif data[7] == ANALOG_VIDEO_BOARD:
                    node_id_analog_video.append(data[6])
                    self.node_id_all_exist.append(data[6])
                elif data[7] == DIGITAL_VIDEO_BOARD:
                    node_id_digital_video.append(data[6])
                    self.node_id_all_exist.append(data[6])
                elif data[7] == LVDS_IN_BOARD:
                    node_id_lvds_in.append(data[6])
                    self.node_id_all_exist.append(data[6])
                elif data[7] == PCIE_BASE_BOARD:
                    self.node_id_pcie_base.append(data[6])
                    self.node_id_all_exist.append(data[6])

                data = ''

    def send_start_command(ser, node_id):
        send = [0xAA, 0xAA,
                0x00, 0x00, 0x00, 0x00,
                0x01, node_id, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x02, 0x00, 0x00, 0x00,
                0x15,
                0x55 , 0x55
                ]
        send[18] = (send[6]+send[7]+send[14])&0xff
        send = send = send_command_ctrl_deal(send)
        # print(" ".join(hex(i) for i in send))
        ser.write(send)

'''
'''
class ProgramUpdate(UI_MainWindow):
    def __init__(self):
        super().__init__()
        self.ser = serial.Serial()  #/dev/ttyUSB0
        self.init()

        #----initialize----QTimer 任务
        self.tick = int(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timeout_slot)
        self.timer.start(100)
        #----end---- 

        #----initialize----QThread 任务
        self.Download_thread = DownloadThread()
        self.Download_thread.trigger.connect(self.UpText)
        #----end---- 

    def init(self):

        #node_id_list
        self.node_id_pcie_base_need_program = list()
        self.node_id_digital_video_need_program = list()
        self.node_id_analog_video_need_program = list()
        self.node_id_lvds_in_need_program = list()
        self.node_id_digital_need_program = list()
        self.node_id_analog_need_program = list()
        self.node_id_power_need_program = list()
        self.node_id_audio_need_program = list()
        self.node_id_need_program = list()
        self.box_id_need_program = list()

        self.box_id_exist = list()
        self.node_id_pcie_base = list()
        self.node_id_digital_video = list()
        self.node_id_analog_video = list()
        self.node_id_lvds_in = list()
        self.node_id_digital = list()
        self.node_id_analog = list()
        self.node_id_power = list()
        self.node_id_audio = list()
        self.node_id_all_exist = list()

        # openSerial
        self.SerialUI.ser_open_button.clicked.connect(self.openSerial)

        # selectSerial
        self.SerialUI.ser_com_combo.currentIndexChanged.connect(self.selectSerial)

        # self.ser_com_combo = QComboBox(self)
        # self.ser_com_combo.move(170, 120)
        # self.ser_com_combo.addItem('1')
        # self.ser_com_combo.addItem('2')
        # self.ser_com_combo.addItem('3')
        # self.ser_com_combo.currentIndexChanged.connect(self.selectSerial)
        # self.show()

        #selectNodeID 
        for node_id in self.BoardTypeUI.NodeID_button:
            node_id.clicked[bool].connect(self.selectNodeID)

        #refreshBoard
        self.BoardTypeUI.BoardRefresh_button.clicked.connect(self.refreshBoard)

        #download_process
        self.BoardTypeUI.download_button.clicked.connect(self.download_process)

    # selectSerial
    def selectSerial(self):
        source = self.sender()
        # QMessageBox.warning(self,"警告",str(self.sexComboBox.currentIndex())+self.tr(':')+self.sexComboBox.currentText(),QMessageBox.Yes)
        # QMessageBox.warning(self, 'pycom','关闭串口失败')
        print(source.currentIndex(), end=': ')
        print(source.currentText())


    # openSerial
    def openSerial(self):
        source = self.sender()
        # print(source)
        if source.text() == 'close':
            source.setText('open')
            # print(str(self.SerialUI.ser_com_combo.currentText()))
            try:
                self.ser = serial.Serial(str(self.SerialUI.ser_com_combo.currentText()), 115200, timeout=0.0000001)  #/dev/ttyUSB0

                if  self.ser.isOpen():
                    print("打开成功 -> %s" % (self.ser.port))
                else:
                    print("打开失败,请检查串口后重启程序!")
            except:
                print("***打开失败,请检查串口是否被占用或其他异常!!!")

            # source.setEnable(False)
            # self.SerialUI.ser_com_combo.setEnable(False)
        elif source.text() == 'open':
            source.setText('close')
            try:
                if  self.ser.isOpen():
                    self.ser.close()
                    print("关闭成功 -> %s" % (self.ser.port))
                else:
                    print("关闭失败,请检查串口后重启程序!")
                # self.SerialUI.ser_com_combo.setEnable(True)
            except ( IndexError,AttributeError, SyntaxError, NameError, TypeError) as err:
                print(err)
                print("***打开失败,请检查串口是否被占用或其他异常!!!")

    #selectNodeID 
    def selectNodeID(self, pressed):
        source = self.sender()

        input_node_id = eval('[%s]'% source.text())

        if pressed:
            print(source.text() + ' select')
            self.node_id_need_program.append(input_node_id[0])
            if (input_node_id[0] in self.node_id_analog):
                self.node_id_analog_need_program.append(input_node_id[0])

            elif (input_node_id[0] in self.node_id_digital):
                self.node_id_digital_need_program.append(input_node_id[0])

            elif (input_node_id[0] in self.node_id_audio):
                self.node_id_audio_need_program.append(input_node_id[0])

            elif (input_node_id[0] in self.node_id_power):
                self.node_id_power_need_program.append(input_node_id[0])

            elif (input_node_id[0] in self.node_id_digital_video):
                self.node_id_digital_video_need_program.append(input_node_id[0])

            elif (input_node_id[0] in self.node_id_analog_video):
                self.node_id_analog_video_need_program.append(input_node_id[0])

            elif (input_node_id[0] in self.node_id_lvds_in):
                self.node_id_lvds_in_need_program.append(input_node_id[0])

            elif (input_node_id[0] in self.node_id_pcie_base):
                self.node_id_pcie_base_need_program.append(input_node_id[0])

        else:
            print(source.text() + ' unselect')
            self.node_id_need_program.remove(input_node_id[0])
            if (input_node_id[0] in self.node_id_analog):
                self.node_id_analog_need_program.remove(input_node_id[0])

            elif (input_node_id[0] in self.node_id_digital):
                self.node_id_digital_need_program.remove(input_node_id[0])

            elif (input_node_id[0] in self.node_id_audio):
                self.node_id_audio_need_program.remove(input_node_id[0])

            elif (input_node_id[0] in self.node_id_power):
                self.node_id_power_need_program.remove(input_node_id[0])

            elif (input_node_id[0] in self.node_id_digital_video):
                self.node_id_digital_video_need_program.remove(input_node_id[0])

            elif (input_node_id[0] in self.node_id_analog_video):
                self.node_id_analog_video_need_program.remove(input_node_id[0])

            elif (input_node_id[0] in self.node_id_lvds_in):
                self.node_id_lvds_in_need_program.remove(input_node_id[0])

            elif (input_node_id[0] in self.node_id_pcie_base):
                self.node_id_pcie_base_need_program.remove(input_node_id[0])

        # self.node_id_need_program = list(set(self.node_id_need_program))  # 设为集合再设回列表，清除重复数值
        print(", ".join(hex(i) for i in self.node_id_need_program))
        print('  1、模拟IO板卡  : %s' % " ".join(hex(i) for i in self.node_id_analog_need_program))
        print('  2、数字IO板卡  : %s' % " ".join(hex(i) for i in self.node_id_digital_need_program))
        print('  3、音频板卡    : %s' % " ".join(hex(i) for i in self.node_id_audio_need_program))
        print('  4、电源控制板卡: %s' % " ".join(hex(i) for i in self.node_id_power_need_program))
        print('  5、数字信号板卡: %s' % " ".join(hex(i) for i in self.node_id_digital_video_need_program))
        print('  6、模拟信号板卡: %s' % " ".join(hex(i) for i in self.node_id_analog_video_need_program))
        print('  7、LVDS_IN 板卡: %s' % " ".join(hex(i) for i in self.node_id_lvds_in_need_program))
        print('  8、底板 板卡   : %s' % " ".join(hex(i) for i in self.node_id_pcie_base_need_program))

    #BoardRefresh_button
    def refreshBoard(self):
        source = self.sender()
        print(source.text())
        # node_id_list = NodeID(self.ser)
        if  self.ser.isOpen():
            pass
        else:
            print('please select uart and open it!')
            return

        for i in range(8):
            for j in range(8):
                self.BoardTypeUI.NodeID_button[i*8+j].setText('    ')
                self.BoardTypeUI.NodeID_button[i*8+j].setCheckable(False)
            self.BoardTypeUI.BoxID_button[i].setText('    ')
            self.BoardTypeUI.BoxID_button[i].setCheckable(False)

        self.node_id_all_exist.clear()
        self.node_id_audio.clear()
        self.node_id_analog.clear()
        self.node_id_digital.clear()
        self.node_id_power.clear()
        self.node_id_analog_video.clear()
        self.node_id_digital_video.clear()
        self.node_id_lvds_in.clear()
        self.node_id_pcie_base.clear()
        self.node_id_need_program.clear()
        self.node_id_analog_need_program.clear()
        self.node_id_digital_need_program.clear()
        self.node_id_audio_need_program.clear()
        self.node_id_power_need_program.clear()
        self.node_id_digital_video_need_program.clear()
        self.node_id_analog_video_need_program.clear()
        self.node_id_lvds_in_need_program.clear()
        self.node_id_pcie_base_need_program.clear()

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
        for node_id in node_id_all:
            self.send_start_command(self.ser, node_id)
            time.sleep(0.005)
            while self.ser.inWaiting() > 0:
                data = self.ser.read_all()
            if data != '' :
                data = self.find_start_head(data)
                # print(" ".join(hex(i) for i in data))

                if data[7] == AUDIO_BOARD:
                    self.node_id_audio.append(data[6])
                    self.node_id_all_exist.append(data[6])
                    self.BoardTypeUI.NodeID_button[(data[6]>>4)*8+0].setText(hex(data[6]))
                    self.BoardTypeUI.NodeID_button[(data[6]>>4)*8+0].setCheckable(True)
                    self.BoardTypeUI.BoxID_button[(data[6]>>4)].setText('Box '+str(data[6]>>4))
                    self.BoardTypeUI.BoxID_button[(data[6]>>4)].setCheckable(True)
                    if (data[6]>>4) not in self.box_id_exist:
                        self.box_id_exist.append(data[6]>>4)
                elif data[7] == POWER_BOARD:
                    self.node_id_power.append(data[6])
                    self.node_id_all_exist.append(data[6])
                    self.BoardTypeUI.NodeID_button[(data[6]>>4)*8+3].setText(hex(data[6]))
                    self.BoardTypeUI.NodeID_button[(data[6]>>4)*8+3].setCheckable(True)
                    self.BoardTypeUI.BoxID_button[(data[6]>>4)].setText('Box '+str(data[6]>>4))
                    self.BoardTypeUI.BoxID_button[(data[6]>>4)].setCheckable(True)
                    if (data[6]>>4) not in self.box_id_exist:
                        self.box_id_exist.append(data[6]>>4)
                elif data[7] == IO_ANALOG_BOARD:
                    self.node_id_analog.append(data[6])
                    self.node_id_all_exist.append(data[6])
                    self.BoardTypeUI.NodeID_button[(data[6]>>4)*8+1].setText(hex(data[6]))
                    self.BoardTypeUI.NodeID_button[(data[6]>>4)*8+1].setCheckable(True)
                    self.BoardTypeUI.BoxID_button[(data[6]>>4)].setText('Box '+str(data[6]>>4))
                    self.BoardTypeUI.BoxID_button[(data[6]>>4)].setCheckable(True)
                    if (data[6]>>4) not in self.box_id_exist:
                        self.box_id_exist.append(data[6]>>4)
                elif data[7] == IO_DIGITAL_BOARD:
                    self.node_id_digital.append(data[6])
                    self.node_id_all_exist.append(data[6])
                    self.BoardTypeUI.NodeID_button[(data[6]>>4)*8+2].setText(hex(data[6]))
                    self.BoardTypeUI.NodeID_button[(data[6]>>4)*8+2].setCheckable(True)
                    self.BoardTypeUI.BoxID_button[(data[6]>>4)].setText('Box '+str(data[6]>>4))
                    self.BoardTypeUI.BoxID_button[(data[6]>>4)].setCheckable(True)
                    if (data[6]>>4) not in self.box_id_exist:
                        self.box_id_exist.append(data[6]>>4)
                elif data[7] == ANALOG_VIDEO_BOARD:
                    self.node_id_analog_video.append(data[6])
                    self.node_id_all_exist.append(data[6])
                    self.BoardTypeUI.NodeID_button[(data[6]>>4)*8+4].setText(hex(data[6]))
                    self.BoardTypeUI.NodeID_button[(data[6]>>4)*8+4].setCheckable(True)
                    self.BoardTypeUI.BoxID_button[(data[6]>>4)].setText('Box '+str(data[6]>>4))
                    self.BoardTypeUI.BoxID_button[(data[6]>>4)].setCheckable(True)
                    if (data[6]>>4) not in self.box_id_exist:
                        self.box_id_exist.append(data[6]>>4)
                elif data[7] == DIGITAL_VIDEO_BOARD:
                    self.node_id_digital_video.append(data[6])
                    self.node_id_all_exist.append(data[6])
                    self.BoardTypeUI.NodeID_button[(data[6]>>4)*8+5].setText(hex(data[6]))
                    self.BoardTypeUI.NodeID_button[(data[6]>>4)*8+5].setCheckable(True)
                    self.BoardTypeUI.BoxID_button[(data[6]>>4)].setText('Box '+str(data[6]>>4))
                    self.BoardTypeUI.BoxID_button[(data[6]>>4)].setCheckable(True)
                    if (data[6]>>4) not in self.box_id_exist:
                        self.box_id_exist.append(data[6]>>4)
                elif data[7] == LVDS_IN_BOARD:
                    self.node_id_lvds_in.append(data[6])
                    self.node_id_all_exist.append(data[6])
                    self.BoardTypeUI.NodeID_button[(data[6]>>4)*8+6].setText(hex(data[6]))
                    self.BoardTypeUI.NodeID_button[(data[6]>>4)*8+6].setCheckable(True)
                    self.BoardTypeUI.BoxID_button[(data[6]>>4)].setText('Box '+str(data[6]>>4))
                    self.BoardTypeUI.BoxID_button[(data[6]>>4)].setCheckable(True)
                    if (data[6]>>4) not in self.box_id_exist:
                        self.box_id_exist.append(data[6]>>4)
                elif data[7] == PCIE_BASE_BOARD:
                    self.node_id_pcie_base.append(data[6])
                    self.node_id_all_exist.append(data[6])
                    self.BoardTypeUI.NodeID_button[(data[6]>>4)*8+7].setText(hex(data[6]))
                    self.BoardTypeUI.NodeID_button[(data[6]>>4)*8+7].setCheckable(True)
                    self.BoardTypeUI.BoxID_button[(data[6]>>4)].setText('Box '+str(data[6]>>4))
                    self.BoardTypeUI.BoxID_button[(data[6]>>4)].setCheckable(True)
                    if (data[6]>>4) not in self.box_id_exist:
                        self.box_id_exist.append(data[6]>>4)

                data = ''

        print(", ".join(hex(i) for i in self.node_id_all_exist))
        print('  1、音频板卡    : %s' % " ".join(hex(i) for i in self.node_id_audio))
        print('  2、模拟IO板卡  : %s' % " ".join(hex(i) for i in self.node_id_analog))
        print('  3、数字IO板卡  : %s' % " ".join(hex(i) for i in self.node_id_digital))
        print('  4、电源控制板卡: %s' % " ".join(hex(i) for i in self.node_id_power))
        print('  5、模拟信号板卡: %s' % " ".join(hex(i) for i in self.node_id_analog_video))
        print('  6、数字信号板卡: %s' % " ".join(hex(i) for i in self.node_id_digital_video))
        print('  7、LVDS_IN 板卡: %s' % " ".join(hex(i) for i in self.node_id_lvds_in))
        print('  8、底板 板卡   : %s' % " ".join(hex(i) for i in self.node_id_pcie_base))

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
                return data[i:i+21]

    def send_command_ctrl_deal(self, send_data):
        send_data2 = list(send_data)        # another list, 创建了的内存
        ctrl_times = int(0)
        for send_i, send_data_each in enumerate(send_data2[2:-2]):
            if send_data_each == CAN_HEAD or send_data_each == CAN_CTRL or send_data_each == CAN_TAIL :
                # print(send_i, send_data_each)
                send_data.insert(send_i+ctrl_times+2, CAN_CTRL)
                ctrl_times = ctrl_times + 1
                # send_i = send_i + 1
                # print(send_data)
                # print(send_data2)

        # print(send_data)
        # print(send_data2)
        # print(send_data2 is send_data)
        return send_data

    def download_process(self):
        source = self.sender()
        print(source.text())
        if  self.ser.isOpen():
            pass
        else:
            print('please select uart and open it!')
            return
        #---- 判断文件名以及创建时间和文件大小---
        if len(self.node_id_pcie_base_need_program) > 0:
            self.Is_file_exist(self.node_id_pcie_base_need_program, FILE_NAME_PCIE_BASE)

        if len(self.node_id_digital_video_need_program) > 0:
            self.Is_file_exist(self.node_id_digital_video_need_program, FILE_NAME_DIGITAL_VIDEO)

        if len(self.node_id_analog_video_need_program) > 0:
            self.Is_file_exist(self.node_id_analog_video_need_program, FILE_NAME_ANALOG_VIDEO)

        if len(self.node_id_lvds_in_need_program) > 0:
            self.Is_file_exist(self.node_id_lvds_in_need_program, FILE_NAME_LVDS_IN)

        if len(self.node_id_digital_need_program) > 0:
            self.Is_file_exist(self.node_id_digital_need_program, FILE_NAME_DIGITAL_IO)

        if len(self.node_id_analog_need_program) > 0:
            self.Is_file_exist(self.node_id_analog_need_program, FILE_NAME_ANALOG_IO)

        if len(self.node_id_power_need_program) > 0:
            self.Is_file_exist(self.node_id_power_need_program, FILE_NAME_POWER)

        if len(self.node_id_audio_need_program) > 0:
            self.Is_file_exist(self.node_id_audio_need_program, FILE_NAME_AUDIO)
        #---- end---

        #---- 复位看门狗---
        data = ''
        node_id_cnt = int(0)
        for node_id in self.node_id_need_program:
            # send_reset_iwdg_command(ser, node_id, node_id_need_program[0])
            self.send_reset_iwdg_command(self.ser, node_id)
            while True:
                while self.ser.inWaiting() > 0:
                    data = self.ser.read_all()
                    # print(data)
                if data != '' and len(data) > 41 and data [2]< 0x90 and data[23] == node_id:
                    # print(" ".join(hex(i) for i in data))
                    node_id_cnt+=1
                    print("重启成功 节点%d --> 0x%02X" % (node_id_cnt, data[23]))

                #----start--- 发送启动命令
                    self.send_start_command(self.ser, node_id)
                #----end-----

                #----start--- 发送擦除扇区命令
                    self.send_erase_commane(self.ser, node_id)
                #----end-----

                        # data = ''
                    break;
                    data = ''
                    # break;
        #---end---

        #----start--- 下载程序
        time.sleep(2)
        # time.sleep(2/(len(node_id_need_program)))
        if len(self.node_id_pcie_base_need_program) > 0:
            self.send_file_data(FILE_NAME_PCIE_BASE, self.node_id_pcie_base_need_program)

        if len(self.node_id_digital_video_need_program) > 0:
            self.send_file_data(FILE_NAME_DIGITAL_VIDEO, self.node_id_digital_video_need_program)

        if len(self.node_id_analog_video_need_program) > 0:
            self.send_file_data(FILE_NAME_ANALOG_VIDEO, self.node_id_analog_video_need_program)

        if len(self.node_id_lvds_in_need_program) > 0:
            self.send_file_data(FILE_NAME_LVDS_IN, self.node_id_lvds_in_need_program)

        if len(self.node_id_digital_need_program) > 0:
            self.send_file_data(FILE_NAME_DIGITAL_IO, self.node_id_digital_need_program)

        if len(self.node_id_analog_need_program) > 0:
            self.send_file_data(FILE_NAME_ANALOG_IO, self.node_id_analog_need_program)

        if len(self.node_id_power_need_program) > 0:
            self.send_file_data(FILE_NAME_POWER, self.node_id_power_need_program)

        if len(self.node_id_audio_need_program) > 0:
            self.send_file_data(FILE_NAME_AUDIO, self.node_id_audio_need_program)
        #----end-----

        #----start--- 发送重启命令
        self.send_command_reboot(self.ser, self.node_id_need_program)
        Is_upgrade_OK = int(1)
        reboot_start_time = time.time()
        reboot_time = time.time()
        # print(reboot_time)
        while (time.time() - reboot_time) < 20:
            while self.ser.inWaiting() > 0:
                data = self.ser.read_all()
                # print(data)
            if data != '' and len(data) > 41 and data[2]< 0x90 and data[23] in self.node_id_need_program:
                # print(" ".join(hex(i) for i in data))
                print("升级成功 --> 0x%02X" % (data[23]))
                self.node_id_need_program.remove(data[23])
                data = ''
                print(time.time() - reboot_time)
                reboot_time = time.time()

            if len(self.node_id_need_program) <= 0:
                print('烧录 OK， 请关闭软件!....')
                break

        #----end-----

        if len(self.node_id_need_program) > 0:
            print('升级失败节点: %s' % " ".join(hex(i) for i in self.node_id_need_program))

        print('升级结束，请重启机箱，并确认各板卡绿灯全亮！')
        time.sleep(1)
        # self.ser.close()
        print('runing time is {}s '.format((nowTime()-run_time)/1000))

    def Is_file_exist(self, node_id_need_program, file_name):
        Is_File_exist = os.path.exists(file_name)
        if Is_File_exist:
            size = os.path.getsize(file_name)
            creat_time = os.path.getmtime(file_name)
            print('')
            print("请按回车键确认需要升级的文件名以及文件创建时间和文件大小！！！")
            print("%s  %s  %d bytes" % (file_name, self.TimeStampToTime(creat_time), size))
            # if DEBUG != 1:
                # input("\r\n")
        else:
            print("找不到该文件  %s , 请放置该文件到该目录下,放置后请按回车键确认" % (file_name))
            # input()

    def send_reset_iwdg_command(self, ser, node_id):
        # send = [AA AA 12 02 00 00 99 00 00 00 00 00 00 06 08 00 00 00 BB 55 55]
        send = [0xAA, 0xAA,
                node_id, 0x02, 0x00, 0x00,
                0x99, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, E_CMD_RESER,
                0x08, 0x00, 0x00, 0x00,
                0x15,
                0x55 , 0x55
                ]
        send[18] = (send[2]+send[3]+send[6]+send[13]+send[14])&0xff
        send = self.send_command_ctrl_deal(send)
        # print(" ".join(hex(i) for i in send))
        ser.write(send)
        print("发送重启指令：节点： 0x%02X " % (node_id))
        # print("send_reset_command...1.1 node_id = 0x%02X " % (node_id))

    def send_erase_commane(self, ser, node_id):
        send = [0xAA, 0xAA,
                node_id, 0x02, 0x00, 0x00,
                0x01, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, E_CMD_UPDATE,
                0x08, 0x00, 0x00, 0x00,
                0x20,
                0x55 , 0x55
                ]
        send[18] = (send[2]+send[3]+send[6]+send[9]+send[13]+send[14])&0xff
        send = self.send_command_ctrl_deal(send)
        # print(" ".join(hex(i) for i in send))
        ser.write(send)
        # print("send_erase_commane...2  node_id = 0x%02X " % (node_id))
        # y = str(bytearray(send))
        # print(y)

    def TimeStampToTime(self, timestamp):
        timeStruct = time.localtime(timestamp)
        return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)

    def send_file_data(self, file_name, node_id_need_program):
        Is_File_exist = int(0)
        while Is_File_exist == 0:
            Is_File_exist = os.path.exists(file_name)
            if Is_File_exist:
                size = os.path.getsize(file_name)
                creat_time = os.path.getmtime(file_name)
                print('')
                print("%s  %s  %d bytes" % (file_name, self.TimeStampToTime(creat_time), size))
                print('正在升级...  ',  end='')
                print(" ".join(hex(i) for i in node_id_need_program))
            else:
                print("找不到该文件  %s , 请放置该文件到该目录下,放置后请按回车键确认" % (file_name))
                input()

        size_high = size//PACK_SIZE  # 1K的倍数
        size_low = size%PACK_SIZE   # 1K的余数
        size_low_8_high = size_low//READ_SIZE                  # 1K的余数 ， 8字节的倍数
        size_low_8_low = size_low%READ_SIZE                # 1K的余数 ， 8字节的余数
        # print("size_high %d, size_low %d, size_low_8_high %d  , size_low_8_low %d " % (size_high, size_low, size_low_8_high, size_low_8_low))
#----start--- 打开文件串口发送操作
        # process_bar = tqdm((range(size)), ncols = 60)
        # process_bar = ShowProcess(size, 'OK')
        with open(file_name, 'rb') as f_bin:
            print('send_file_data ...1')
            old_tell = f_bin.tell()
            # self.Download_thread.start()

            # old_tick = int(0)
            # i = 0
            # while i < (size_high+1):
                # print('i=%d, self.tick=%d, old_tick=%d' % (i, self.tick, old_tick))
                # if (self.tick - old_tick) >= 100:
                    # i = i + 1
                    # old_tick = self.tick
                # #----start--- 发送装载数据命令
                    # print('send_file_data ...2')
                    # self.send_data_command(self.ser, node_id_need_program)
                # #----end-----
                    # if(i == size_high):                                 #最后1K字节发送
                        # # print("this is size_sigh = %d " % (size_high))
                        # check_sum_1K = int()
                        # for i in range(0, PACK_SIZE//READ_SIZE):
                            # if (i < size_low_8_high):
                                # f_bin_data = f_bin.read(READ_SIZE)
                                # f_bin_data = list(f_bin_data)
                            # elif (i == size_low_8_high):                                   #bin文件最后8个字节，
                                # f_bin_data = f_bin.read(size_low_8_low)
                                # f_bin_data = list(f_bin_data)

                                # for j in range(size_low_8_low, READ_SIZE):
                                    # f_bin_data.append(0xFF)

                            # else :
                                # f_bin_data = [0xff]*READ_SIZE


                            # for node_id in node_id_need_program:
                                # send_data = [0xAA, 0xAA,
                                            # 0x12, 0x03, 0x00, 0x00,
                                            # 0x08, 0x00, 0x00, 0x00,
                                            # 0x31,
                                            # 0x55 , 0x55
                                            # ]
                                # send_data[2] = node_id
                                # check_sum = (send_data[2]+send_data[3]+send_data[6]+sum(f_bin_data))
                                # send_data[10] = check_sum&0xff
                                # send_data = send_data[0:6:1] +f_bin_data + send_data[6::1]

                                # send_data = self.send_command_ctrl_deal(send_data)
                                # self.ser.write(send_data) #数据写回
                            # check_sum_1K += sum(f_bin_data)
                    # else:
                    # #----start--- 发送1K数据
                        # print('send_file_data ...3')
                        # check_sum_1K = self.send_1K_bin_data(self.ser, f_bin, node_id_need_program)
                        # # print(hex(check_sum_1K))
                    # #----end---

                    # # process_bar.write(f_bin.tell()- old_tell, end='\r')
                    # # process_bar.update(f_bin.tell()- old_tell)
                    # # process_bar.show_process(i=(f_bin.tell()))
                    # # print('\r', end='\r')
                    # # print('', end='\1b[nA')
                    # # sys.stdout.flush()
                    # # # process_bar.clear(nolock = True)
                    # self.BoardTypeUI.Progress_bar.setValue((f_bin.tell()/size)*100)
                    # old_tell = f_bin.tell()

                # #----start--- 发送烧录命令
                    # self.send_program_command(self.ser, check_sum_1K, node_id_need_program)
                # #----end-----


            for (i) in  range(size_high+1):
            #----start--- 发送装载数据命令
                print('send_file_data ...2')
                self.send_data_command(self.ser, node_id_need_program)
            #----end-----
                # sleep(3)

                if(i == size_high):                                 #最后1K字节发送
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
                else:
                #----start--- 发送1K数据
                    print('send_file_data ...3')
                    check_sum_1K = self.send_1K_bin_data(self.ser, f_bin, node_id_need_program)
                    # print(hex(check_sum_1K))
                #----end---

                # process_bar.write(f_bin.tell()- old_tell, end='\r')
                # process_bar.update(f_bin.tell()- old_tell)
                # process_bar.show_process(i=(f_bin.tell()))
                # print('\r', end='\r')
                # print('', end='\1b[nA')
                # sys.stdout.flush()
                # # process_bar.clear(nolock = True)
                self.BoardTypeUI.Progress_bar.setValue((f_bin.tell()/size)*100)
                old_tell = f_bin.tell()

            #----start--- 发送烧录命令
                self.send_program_command(self.ser, check_sum_1K, node_id_need_program)
            #----end-----
                time.sleep(0.1)

    def send_data_command(self, ser, node_ids):
        print("send_data_command...1")
        for node_id in node_ids:
            send = [0xAA, 0xAA,
                    0x12, 0x02, 0x00, 0x00,
                    0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, E_CMD_UPDATE,
                    0x08, 0x00, 0x00, 0x00,
                    0x20,
                    0x55 , 0x55
                    ]
            send[2] = node_id
            send[18] = (send[2]+send[3]+send[6]+send[13]+send[14])&0xff
            send = self.send_command_ctrl_deal(send)
            # print(" ".join(hex(i) for i in send))
            ser.write(send)
            print("send_data_command...3  node_id = 0x%02X " % (node_id))

    def send_1K_bin_data(self, ser, f_bin, node_ids):
        check_sum_1K = int()
        # print(f_bin.seek(1024))
        print(f_bin.tell())
        for i in range(0, PACK_SIZE//READ_SIZE):
            f_bin_data = f_bin.read(READ_SIZE)
            # f_bin_data = [ 0x88, 0x00, 0x00, 0x00, 0x00, 0xA0, 0x5A, 0x01]
            # f_bin_data = [ 0xA5, 0xA5, 0xA5, 0x00, 0x00, 0xA5, 0x00, 0x01]
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
                # print(hex(check_sum))
                # check = list(check_sum)
                # send_data.append(check)
                send_data[10] = check_sum&0xff
                send_data = send_data[0:6:1] +f_bin_data + send_data[6::1]

                send_data = self.send_command_ctrl_deal(send_data)
                # print(i)
                # if(i >= 21):
                    # sleep(3)
                    # print(send_data)
                # print(" ".join(hex(i) for i in send_data))
                ser.write(send_data) #数据写回
                # input("按回车键继续")

            check_sum_1K += sum(f_bin_data)
            # sleep(0.02)
        print(f_bin.tell())
        return check_sum_1K

    def send_program_command(self, ser, check_sum, node_ids):
        for node_id in node_ids:
            send = [0xAA, 0xAA,
                    0x12, 0x02, 0x00, 0x00,
                    0x03,
                    0x08, 0x00, 0x00, 0x00,
                    0x20,
                    0x55 , 0x55
                    ]
            send_check_sum_1K = [(check_sum>>0)&0xff,
                                    (check_sum>>8)&0xff,
                                    (check_sum>>16)&0xff,
                                    (check_sum>>24)&0xff,
                                    0x00,
                                    0x00,
                                    0x02
                                ]
            send[2] = node_id
            check_sum_1K_program = (send[2]+send[3]+send[6]+send[7]+sum(send_check_sum_1K))&0xff
            send[11] = check_sum_1K_program
            send = send[0:7:1] +send_check_sum_1K + send[7::1]
            send = self.send_command_ctrl_deal(send)
            ser.write(send)
            # print(hex(check_sum_1K_program))
            # print(send)
            print("send_program_command...4  node_id = 0x%02X " % (node_id))

    def send_command_reboot(self, ser, node_ids):
        for node_id in node_ids:
            send = [0xAA, 0xAA,
                    0x12, 0x02, 0x00, 0x00,
                    0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02,
                    0x08, 0x00, 0x00, 0x00,
                    0x22,
                    0x55 , 0x55
                    ]
            send[2] = node_id
            send[18] = (send[2]+send[3]+send[6]+send[13]+send[14])&0xff
            send = self.send_command_ctrl_deal(send)
            # print(" ".join(hex(i) for i in send))
            ser.write(send)
            print("send_command_reboot...  node_id = 0x%02X " % (node_id))

    def timeout_slot(self):
        self.tick = self.tick + 1
        # print(str(self.tick))

        # for (i) in  range(size_high+1):
        # #----start--- 发送装载数据命令
            # print('send_file_data ...2')
            # self.send_data_command(self.ser, node_id_need_program)
        # #----end-----
            # # sleep(3)

            # if(i == size_high):                                 #最后1K字节发送
                # # print("this is size_sigh = %d " % (size_high))
                # check_sum_1K = int()
                # for i in range(0, PACK_SIZE//READ_SIZE):
                    # if (i < size_low_8_high):
                        # f_bin_data = f_bin.read(READ_SIZE)
                        # f_bin_data = list(f_bin_data)
                    # elif (i == size_low_8_high):                                   #bin文件最后8个字节，
                        # f_bin_data = f_bin.read(size_low_8_low)
                        # f_bin_data = list(f_bin_data)

                        # for j in range(size_low_8_low, READ_SIZE):
                            # f_bin_data.append(0xFF)

                    # else :
                        # f_bin_data = [0xff]*READ_SIZE


                    # for node_id in node_id_need_program:
                        # send_data = [0xAA, 0xAA,
                                    # 0x12, 0x03, 0x00, 0x00,
                                    # 0x08, 0x00, 0x00, 0x00,
                                    # 0x31,
                                    # 0x55 , 0x55
                                    # ]
                        # send_data[2] = node_id
                        # check_sum = (send_data[2]+send_data[3]+send_data[6]+sum(f_bin_data))
                        # send_data[10] = check_sum&0xff
                        # send_data = send_data[0:6:1] +f_bin_data + send_data[6::1]

                        # send_data = self.send_command_ctrl_deal(send_data)
                        # self.ser.write(send_data) #数据写回
                    # check_sum_1K += sum(f_bin_data)
            # else:
            # #----start--- 发送1K数据
                # print('send_file_data ...3')
                # check_sum_1K = self.send_1K_bin_data(self.ser, f_bin, node_id_need_program)
                # # print(hex(check_sum_1K))
            # #----end---

            # # process_bar.write(f_bin.tell()- old_tell, end='\r')
            # # process_bar.update(f_bin.tell()- old_tell)
            # # process_bar.show_process(i=(f_bin.tell()))
            # # print('\r', end='\r')
            # # print('', end='\1b[nA')
            # # sys.stdout.flush()
            # # # process_bar.clear(nolock = True)
            # self.BoardTypeUI.Progress_bar.setValue((f_bin.tell()/size)*100)
            # old_tell = f_bin.tell()

        # #----start--- 发送烧录命令
            # self.send_program_command(self.ser, check_sum_1K, node_id_need_program)
        # #----end-----

    def UpText(self, str):
        print(str)
'''
'''
class DownloadThread(QThread):
    #定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self):
        super(DownloadThread, self).__init__()

    def run(self):
        time.sleep(5)
        self.trigger.emit('test2')

    def send_file_data(self, file_name, node_id_need_program):
        Is_File_exist = int(0)
        while Is_File_exist == 0:
            Is_File_exist = os.path.exists(file_name)
            if Is_File_exist:
                size = os.path.getsize(file_name)
                creat_time = os.path.getmtime(file_name)
                print('')
                print("%s  %s  %d bytes" % (file_name, self.TimeStampToTime(creat_time), size))
                print('正在升级...  ',  end='')
                print(" ".join(hex(i) for i in node_id_need_program))
            else:
                print("找不到该文件  %s , 请放置该文件到该目录下,放置后请按回车键确认" % (file_name))
                input()

        size_high = size//PACK_SIZE  # 1K的倍数
        size_low = size%PACK_SIZE   # 1K的余数
        size_low_8_high = size_low//READ_SIZE                  # 1K的余数 ， 8字节的倍数
        size_low_8_low = size_low%READ_SIZE                # 1K的余数 ， 8字节的余数
        with open(file_name, 'rb') as f_bin:
            print('send_file_data ...1')
            for (i) in  range(size_high+1):
            #----start--- 发送装载数据命令
                print('send_file_data ...2')
                self.send_data_command(self.ser, node_id_need_program)
            #----end-----
                # sleep(3)

                if(i == size_high):                                 #最后1K字节发送
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
                else:
                #----start--- 发送1K数据
                    print('send_file_data ...3')
                    check_sum_1K = self.send_1K_bin_data(self.ser, f_bin, node_id_need_program)
                #----end---

                self.BoardTypeUI.Progress_bar.setValue((f_bin.tell()/size)*100)

            #----start--- 发送烧录命令
                self.send_program_command(self.ser, check_sum_1K, node_id_need_program)
            #----end-----
                time.sleep(0.1)

'''
'''
if __name__ == '__main__':
    if sys.stdout.isatty():
        default_encoding = sys.stdout.encoding
    else:
        default_encoding = locale.getpreferredencoding()

    #每一pyqt5应用程序必须创建一个应用程序对象。sys.argv参数是一个列表，从命令行输入参数。
    app = QApplication(sys.argv)
    run_time = nowTime()

    MainWindowUI = UI_MainWindow()

    #系统exit()方法确保应用程序干净的退出
    #的exec_()方法有下划线。因为执行是一个Python关键词。因此，exec_()代替
    sys.exit(app.exec_())
