#
# -*- coding: utf-8 -*-

"""
In this example, we create a simple window in PyQt5.

author: chenzhipeng3472
last edited: 04-July-2018
"""

import sys
import time
import serial
import serial.tools.list_ports
import threading
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QCheckBox)
from PyQt5.QtCore import (pyqtSignal, QTimer, QThread)
from PyQt5.QtGui import QFont
from PyQt5 import QtCore

import UI_ProgramUpdate


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
run_time = nowTime()

'''
'''
class UI_MainWindow(UI_ProgramUpdate.Ui_Form, QWidget):

    def __init__(self):
        super(UI_MainWindow,self).__init__()

        self.MainWindow = QWidget()

        self.setupUi(self.MainWindow)

        #----initialize----QThread 任务
        self.ProgramUpdate_thread = ProgramUpdateThread()
        self.ProgramUpdate_thread.start()
        #----end---- 

        self.initUI()
        self.MainWindow.show()

    def initUI(self):

        self.NodeID_button =list()
        self.BoxID_checkBox =list()
        for i in range(8):
            for j in range(8):
                # self.NodeID_button.append(QPushButton(hex(i*16+j), self))
                self.NodeID_button.append(QPushButton(self.gridLayoutWidget_2))
                self.NodeID_button[i*8+j].setEnabled(False)
                self.NodeID_button[i*8+j].setText("")
                self.NodeID_button[i*8+j].setCheckable(True)
                self.NodeID_button[i*8+j].setFlat(True)
                # self.NodeID_button[i*8+j].pressed.connect(self.selectNodeID)
                self.gridLayout_3.addWidget(self.NodeID_button[i*8+j], j+2, i+1, 1, 1)
                pass

            # self.BoxID_checkBox.append(QPushButton('Box '+str(i), self))
            self.BoxID_checkBox.append(QCheckBox('机箱 '+str(i), self.gridLayoutWidget_2))
            self.BoxID_checkBox[i].setEnabled(False)
            font = QFont()
            font.setPointSize(11)
            font.setBold(True)
            font.setWeight(75)
            self.BoxID_checkBox[i].setFont(font)
            self.BoxID_checkBox[i].setFocusPolicy(QtCore.Qt.StrongFocus)
            self.BoxID_checkBox[i].setLayoutDirection(QtCore.Qt.LeftToRight)
            self.BoxID_checkBox[i].setChecked(False)
            self.BoxID_checkBox[i].setAutoRepeat(False)
            self.BoxID_checkBox[i].setTristate(False)
            # self.BoxID_checkBox[i].setCheckable(False)
            # # self.BoxID_checkBox[i*8+j].clicked[bool].connect(self.selectNodeID)
            self.gridLayout_3.addWidget(self.BoxID_checkBox[i], 1, i+1, 1, 1)

        self.ser_detect_button.clicked.connect(self.DetectSerial)

        # message_singel
        self.ProgramUpdate_thread.message_singel.connect(self.message_singel)
        self.Msg_TextEdit.insertPlainText('欢迎使用，请选择串口。。。\r\n')
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
        self.Progress_bar.setValue(99)

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
        self.ProgramUpdate_thread.refreshBoard()

    #message_singel
    def message_singel(self, str):
        textCursor = self.Msg_TextEdit.textCursor()
        textCursor.movePosition(textCursor.End)
        self.Msg_TextEdit.setTextCursor(textCursor)
        self.Msg_TextEdit.insertPlainText(str)

    def processBar_singel(self, val):
        self.Progress_bar.setValue(val)

    #refresh_singel
    def refresh_singel(self, cmd, i, j, is_down):
        if is_down == 2:
            is_down = True

        if cmd == 1:  # clear node_id
            self.NodeID_button[i*8+j].setText('    ')
            self.NodeID_button[i*8+j].setCheckable(False)
            self.NodeID_button[i*8+j].setEnabled(False)
            self.NodeID_button[i*8+j].setFlat(True)
            # self.NodeID_button[i*8+j].clicked[bool].connect(self.selectNodeID)
            # self.NodeID_button[i*8+j].clicked[bool].disconnect(self.selectNodeID)

        if cmd == 2:  # clear box_id
            # self.BoxID_button[i].setText('    ')
            self.BoxID_checkBox[i].setCheckable(False)
            self.BoxID_checkBox[i].setEnabled(False)
            pass

        if cmd == 3:  # set node_id
            # print('cmd=%d, i=0x%02X, j=%d' % (cmd, i, j))
            self.NodeID_button[(i>>4)*8+j].setFlat(False)
            self.NodeID_button[(i>>4)*8+j].setText(hex(i))
            self.NodeID_button[(i>>4)*8+j].setCheckable(True)
            self.NodeID_button[(i>>4)*8+j].setChecked(is_down)
            self.NodeID_button[(i>>4)*8+j].setEnabled(True)
            # self.NodeID_button[(i>>4)*8+j].clicked[bool].connect(self.selectNodeID)
            # self.BoardTypeUI.BoxID_button[(i>>4)].setText('Box '+str(i>>4))
            self.BoxID_checkBox[(i>>4)].setCheckable(True)
            self.BoxID_checkBox[(i>>4)].setEnabled(True)

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
        self.timer.start(1)
        #----end---- 

        #----initialize----threading 任务
        self.thread_1 = threading.Thread(target=self.receive_data_thread)
        self.thread_1.setDaemon(True)
        self.thread_1.start()
        #----end---- 

        self.download_process_flag = 0
        self.download_select = 0
        self.refreshBoardFlag = 0

    def run(self):
        while True:
            # QThread.msleep(1000)
            # print('tick2=%d ' % (self.tick))
            if self.refreshBoardFlag == 1:
                # print('refreshBoardFlag=%d ' % (self.refreshBoardFlag))
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

                print('node_id_all_exist:')
                print(", ".join(hex(i) for i in self.node_id_all_exist))
                print('  1、音频板卡    : %s' % " ".join(hex(i) for i in self.node_id_audio))
                print('  2、模拟IO板卡  : %s' % " ".join(hex(i) for i in self.node_id_analog))
                print('  3、数字IO板卡  : %s' % " ".join(hex(i) for i in self.node_id_digital))
                print('  4、电源控制板卡: %s' % " ".join(hex(i) for i in self.node_id_power))
                print('  5、模拟信号板卡: %s' % " ".join(hex(i) for i in self.node_id_analog_video))
                print('  6、数字信号板卡: %s' % " ".join(hex(i) for i in self.node_id_digital_video))
                print('  7、LVDS_IN 板卡: %s' % " ".join(hex(i) for i in self.node_id_lvds_in))
                print('  8、底板 板卡   : %s' % " ".join(hex(i) for i in self.node_id_pcie_base))
                self.refreshBoardFlag = 0
                self.message_singel.emit('刷新节点完成.\r\n')

            pass

    # openSerial
    def openSerial(self, COMn):
        try:
            self.ser = serial.Serial(COMn, 115200, timeout=0.0000001)  #/dev/ttyUSB0

            if  self.ser.isOpen():
                print("打开成功 -> %s" % (self.ser.port))
                self.message_singel.emit('打开成功 -> '+ COMn + '\r\n')
                ret = 0
            else:
                print("打开失败,请检查串口后重启程序!")
                self.message_singel.emit("打开失败,请检查串口后重启程序!\r\n")
                ret = 1
        except:
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
        return ret

    #BoardRefresh_button
    def refreshBoard(self):
        if  self.ser.isOpen():
            self.message_singel.emit('刷新节点.\r\n')
            self.refreshBoardFlag = 1
            pass
        else:
            # print('please select uart and open it!')
            self.message_singel.emit('请检查串口是否打开！\r\n')
            return

    def receive_data_thread(self):
        while True:
            # time.sleep(1)
            # print('tick3=%d ' % (self.tick))
            pass


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

'''
main
'''
if __name__ == "__main__":
    if sys.stdout.isatty():
        default_encoding = sys.stdout.encoding
    else:
        default_encoding = locale.getpreferredencoding()

    #每一pyqt5应用程序必须创建一个应用程序对象。sys.argv参数是一个列表，从命令行输入参数。
    app = QApplication(sys.argv)


    ui = UI_MainWindow()

    # ui.setupUi(MainWindow)


    # MainWindow.show()


    #系统exit()方法确保应用程序干净的退出
    #的exec_()方法有下划线。因为执行是一个Python关键词。因此，exec_()代替
    sys.exit(app.exec_())

    print('runing time is {}s '.format((nowTime()-run_time)/1000))

    pass
