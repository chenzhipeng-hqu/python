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
import threading
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QCheckBox)
from PyQt5.QtCore import (pyqtSignal, QTimer, QThread)
from PyQt5 import QtCore, QtGui

import UI_ProgramUpdate


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
class UI_MainWindow(UI_ProgramUpdate.Ui_Form, QWidget):

    def __init__(self):
        super(UI_MainWindow,self).__init__()

        self.MainWindow = QWidget()

        self.setupUi(self.MainWindow)

        # self.GroupBox.resize(self.GroupBox.sizeHint())
        # self.MainWindow.resize(self.MainWindow.sizeHint())

        #----initialize----QThread 任务
        self.ProgramUpdate_thread = ProgramUpdateThread()
        self.ProgramUpdate_thread.start()
        #----end---- 

        self.initUI()
        self.MainWindow.show()

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
            for j in range(8):
                # self.NodeID_button.append(QPushButton(hex(i*16+j), self))
                self.NodeID_button.append(QPushButton(self.gridLayoutWidget_2))
                self.NodeID_button[i*8+j].setEnabled(False)
                self.NodeID_button[i*8+j].setText("")
                self.NodeID_button[i*8+j].setCheckable(True)
                self.NodeID_button[i*8+j].setFlat(True)
                self.NodeID_button[i*8+j].setPalette(palette)
                self.NodeID_button[i*8+j].clicked[bool].connect(self.selectNodeID)
                self.gridLayout_3.addWidget(self.NodeID_button[i*8+j], j+2, i+1, 1, 1)

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
            # self.BoxID_checkBox[i].setCheckable(False)
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
            self.NodeID_button[(i>>4)*8+j].setText(str(version))
            self.NodeID_button[(i>>4)*8+j].setCheckable(True)
            self.NodeID_button[(i>>4)*8+j].setChecked(is_down)
            self.NodeID_button[(i>>4)*8+j].setEnabled(True)
            self.NodeID_button[(i>>4)*8+j].id_ = i
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

        #node_id_list
        self.node_id_need_program = list()
        self.box_id_need_program = list()

        self.box_id_exist = list()
        self.node_id_all_exist = list()

            #seq, board_type, file_name, node_idx_exist, node_idx_need_program i
        self.AllNodeList = [\
            ( 0 , AUDIO_BOARD         , FILE_NAME_AUDIO           , list()    , list() ),\
            ( 1 , IO_ANALOG_BOARD     , FILE_NAME_ANALOG_IO       , list()    , list() ),\
            ( 2 , IO_DIGITAL_BOARD    , FILE_NAME_DIGITAL_IO      , list()    , list() ),\
            ( 3 , POWER_BOARD         , FILE_NAME_POWER           , list()    , list() ),\
            ( 4 , ANALOG_VIDEO_BOARD  , FILE_NAME_ANALOG_VIDEO    , list()    , list() ),\
            ( 5 , DIGITAL_VIDEO_BOARD , FILE_NAME_DIGITAL_VIDEO   , list()    , list() ),\
            ( 6 , LVDS_IN_BOARD       , FILE_NAME_LVDS_IN         , list()    , list() ),\
            ( 7 , PCIE_BASE_BOARD     , FILE_NAME_PCIE_BASE       , list()    , list() )\
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

    def run(self):
        while True:
            # print('tick2=%d ' % (self.tick))
            if self.refreshBoardFlag == 1:
                self.refreshBoard()

            if self.download_process_flag == 1:
                # self.download_process()
                self.download_process2()

            QThread.msleep(1)

            pass

    def download_process2(self):
        if self.Download_state == 0: #---- 初始化数据---
            if  self.ser.isOpen():
                self.message_singel.emit('下载程序...\r\n')
                self.run_time = nowTime()
                self.Download_state = 1
            else:
                print('please select uart and open it!')
                self.message_singel.emit('请检查串口并选择节点！\r\n')
                self.download_process_flag = 0
                self.Download_state = 1
                return

        if self.Download_state == 1: #---- 复位看门狗---
            for seq, board_type, file_name, node_idx_exist, node_idx_need_program in self.AllNodeList:
                if len(node_idx_need_program)>0:
                    print(" ".join(hex(i) for i in node_idx_need_program))

                    for node_id in node_idx_need_program:
                        self.send_reset_iwdg_command(self.ser, node_id)
                        self.message_singel.emit('发送重启指令：节点：' + str(hex(node_id)) + ' \r\n')
                        data = ''
                        while True:
                            while self.ser.inWaiting() > 0:
                                data = self.ser.read_all()
                                # print(data)
                            if data != '' and len(data) > 41 and data [2]< 0x90 and data[23] == node_id:
                                # print(" ".join(hex(i) for i in data))
                                print("重启成功 节点 --> 0x%02X" % (data[23]))
                                self.message_singel.emit('重启成功 --> ' + str(hex(data[23])) + ' \r\n')

                                self.send_start_command(self.ser, node_id) #------- 发送启动命令
                                QThread.msleep(1)
                                self.send_erase_commane(self.ser, node_id) #------- 发送擦除扇区命令
                                QThread.msleep(1)
                                break;

                    self.send_file_ret = 1
                    QThread.sleep(2)
                    self.Download_state = 2
                    self.send_file_tell = -1
                    break
                if seq == 7 and len(node_idx_need_program) <=0:
                    print('seq=%d' % (seq))
                    print('升级结束，请重启机箱，并确认各板卡绿灯全亮！')
                    self.message_singel.emit('升级用时 {}s \r\n'.format((nowTime()-self.run_time)/1000))
                    self.message_singel.emit('升级结束，请重启机箱，并刷新节点确认版本号！ ')
                    self.Download_state = 0
                    self.download_process_flag = 0



        elif self.Download_state == 2: #send file
            for seq, board_type, file_name, node_idx_exist, node_idx_need_program in self.AllNodeList:
                # print("1")
                if len(node_idx_need_program)>0:
                    # print("2")
                    # print(" ".join(hex(i) for i in node_idx_need_program))
                    self.send_file_tell, self.send_file_ret = self.send_file_data(file_name, self.send_file_ret, self.send_file_tell, node_idx_need_program)
                    if self.send_file_ret == 0 :
                        self.Download_state = 3
                    break;
                # print('send_file_ret=%d' % (self.send_file_ret))

        elif self.Download_state == 3: #----start--- 发送重启命令
            for seq, board_type, file_name, node_idx_exist, node_idx_need_program in self.AllNodeList:
                print('seq=%d' % (seq))
                print(" ".join(hex(i) for i in node_idx_need_program))
                if len(node_idx_need_program)>0:
                    self.send_command_reboot(self.ser, node_idx_need_program)
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
                            QThread.sleep(2)
                            print('烧录 OK， 请关闭软件!....')
                            if seq < 7 :
                                self.Download_state = 1
                                return
                    self.Download_state = 1
                    break

                    # if len(node_idx_need_program) <= 0:
                        # print('烧录 OK， 请关闭软件!....')
                        # QThread.sleep(1)
                        # break
                        # if seq < 7 and len(node_idx_need_program) <=0 and len(self.AllNodeList[seq+1][4])>0:
                            # self.Download_state = 1
                            # break
                if seq >= 7 and len(node_idx_need_program) <=0:
                    # print('download_process_flag=%d' % (self.download_process_flag))
                    print('升级结束，请重启机箱，并确认各板卡绿灯全亮！')
                    self.message_singel.emit('升级用时 {}s \r\n'.format((nowTime()-self.run_time)/1000))
                    self.message_singel.emit('升级结束，请重启机箱，并刷新节点确认版本号！ ')
                    self.Download_state = 0
                    self.download_process_flag = 0

                    # node_idx_need_program.clear()




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
        print(" ".join(hex(i) for i in send))
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
        # print(input_node_id)

        for seq, board_type, file_name, node_idx_exist, node_idx_need_program in self.AllNodeList:
            if pressed:
                if input_node_id[0] in node_idx_exist:
                    node_idx_need_program.append(input_node_id[0])
                    if (input_node_id[0] in self.node_id_all_exist):
                        self.node_id_need_program.append(input_node_id[0])

            else:
                if input_node_id[0] in node_idx_need_program:
                    node_idx_need_program.remove(input_node_id[0])
                    if (input_node_id[0] in self.node_id_need_program):
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

    # openSerial
    def openSerial(self, COMn):
        try:
            self.ser = serial.Serial(COMn, 115200, timeout=0.0000001)  #/dev/ttyUSB0

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
            for j in range(8):
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
        for node_id in node_id_all:
            self.send_start_command(self.ser, node_id)
            QThread.msleep(5)
            while self.ser.inWaiting() > 0:
                data = self.ser.read_all()
            if data != '' and len(data)>20:
                data = self.find_start_head(data)
                # print(" ".join(hex(i) for i in data))

                version = self.find_version(data)

                for seq, board_type, file_name, node_idx_exist, node_idx_need_program in self.AllNodeList:
                    if data[7] == board_type:
                        node_idx_exist.append((data[6]))
                        self.node_id_all_exist.append(data[6])
                        self.box_id_exist.append(data[6]>>4)
                        self.refresh_singel.emit(3, data[6], seq, version, self.download_select)
                        if self.download_select == 2:
                            self.node_id_need_program.append(data[6])
                            node_idx_need_program.append((data[6]))

                data = ''

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
        self.message_singel.emit(' --> 完成.\r\n')

        self.refreshBoardFlag = 0

    def download_process(self):

        if self.Download_state == 0: #---- 初始化数据---
            self.Download_state = 1

        if self.Download_state == 1: #---- 复位看门狗---
            if  self.ser.isOpen() and len(self.node_id_need_program) > 0:
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
                        QThread.msleep(1)
                    #----end-----

                    #----start--- 发送擦除扇区命令
                        self.send_erase_commane(self.ser, node_id)
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
                    self.message_singel.emit('正在升级 ' + file_name + '  Version: ' + self.TimeStampToTime(creat_time) + ' ... \r\n')
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

                # print('send_file_data ...1')
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

                    if f_bin.tell() >= self.size:
                        self.message_singel.emit(file_name + ' -> ' + str(round(f_bin.tell()/self.size*100, 1)) + '% \r\n')

                    self.old_tell = f_bin.tell()
                    send_tell = f_bin.tell()

                #----start--- 发送烧录命令
                    self.send_program_command(self.ser, check_sum_1K, node_id_need_program)
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
                return data[i:i+42]

    def find_version(self, data):
        if len(data) >40:
            pass
        else:
            print('there is no version, maybe in boot')
            return 'Boot'

        year = ((data[29] >> 2)&0x3f)
        month = (((data[29]<<2)&0x0c) | ((data[30]>>6)&0x03))&0x0f
        day = (data[30]>>1)&0x1f
        hour = ((data[30]<<4)&0x10) | data[31]>>4
        minute = ((data[31]&0x0f)<<2) | ((data[32]>>6)&0x0f)
        version = str(year)+'_'+str(month)+'_'+str(day)
        # print('year=%d, month=%d, day=%d, hour=%d, minute=%d' % (year, month, day, hour, minute))
        return version

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
                    # print(send_data)
                # print(" ".join(hex(i) for i in send_data))
                ser.write(send_data) #数据写回
                # input("按回车键继续")

            check_sum_1K += sum(f_bin_data)
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
