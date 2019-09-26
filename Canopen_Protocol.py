
#
# -*- coding: utf-8 -*-

"""
In this example, we create a simple window in PyQt5.

author: chenzhipeng3472
last edited: 04-July-2018
"""
__author__ = 'chenzhipeng3472'

import canopen
import sys
import os
import traceback

import time

from myserial.serial_can import SerialBus
import can

import logging

# logging.basicConfig(level=logging.DEBUG,
        # filename='out.log')
logging.basicConfig(level=logging.DEBUG,
        filename='out.log',
        datefmt='%Y/%m/%d %H:%M:%S',
        format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')

logger = logging.getLogger(__name__)

from CANalystII_Driver import *

USE_UART = 0
USE_CANALYST_II = 1
global CAN_DRIVER
CAN_DRIVER = USE_UART
USE_USB_UART = 0
# __all__ = ["CAN_DRIVER"]

nowTime = lambda:int(round(time.time()*1000))

class CanopenProtocol:
    '''
    canopen
    '''

    __CAN_HEAD = int(0xAA)
    __CAN_CTRL = int(0xA5)
    __CAN_TAIL = int(0x55)

    NMT = 0x00<<7
    SYNC = 0x01<<7
    TIME_STAMP = 0x02<<7
    PDO1_Tx = 0x03<<7
    PDO1_Rx = 0x04<<7
    PDO2_Tx = 0x05<<7
    PDO2_Rx = 0x06<<7
    PDO3_Tx = 0x07<<7
    PDO3_Rx = 0x08<<7
    PDO4_Tx = 0x09<<7
    PDO4_Rx = 0x0a<<7
    SDO_Tx = 0x0b<<7
    SDO_Rx = 0x0c<<7
    NODE_GUARD = 0x0e<<7
    LSS = 0x0f<<7

    TO_MASTER = 0x0081


    # def __init__(self, channel=None, ):
    def __init__(self, channel=None, *args, **kwargs):
        self.comx = channel
        # try:
            # bus = SerialBus(channel=self.comx, baudrate=460800)
            # self.network = canopen.Network(bus=bus)
            # listeners = [can.Printer()] + self.network.listeners
            # self.network.notifier = can.Notifier(bus, listeners, 1)
            # self.network.check()
            # self.network.scanner.search()

            # # print(type(self.network.scanner.nodes))
            # for node_id in self.network.scanner.nodes:
                # print("Found node 0x%02X!" % node_id)
                # # node = self.network.add_node(node_id, 'objDict.eds')

                # # node.nmt.state = 'RESET COMMUNICATION'
                # # node.nmt.state = 'OPERATIONAL'
                # # value = node.sdo[0x1000].raw = 1
                # # print(value)
                # # value = node.sdo[0x1018][1].raw
                # # print(value)

                # # node.nmt.wait_for_bootup(10)

            # # self.network = network

        # except KeyboardInterrupt:
            # pass
        # except Exception as e:
            # exc_type, exc_obj, exc_tb = sys.exc_info()
            # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # print(exc_type, fname, exc_tb.tb_lineno)
            # traceback.print_exc()
        # finally:
            # # Disconnect from CAN bus
            # print('going to exit... stoping...')
            # if self.network:
                # print('network disconnect')
                # # # for node_id in network:
                    # # # node = network[node_id]
                    # # # node.nmt.state = 'PRE-OPERATIONAL'
                    # # # node.nmt.stop_node_guarding()
                # # # network.sync.stop()
            # self.network.disconnect()
        pass

    def __del__(self):
        # print('going to exit... stoping...')
        # if self.network:
            # self.network.disconnect()
        pass

    def scanner(self):
        node_id_all = list()
        for node_id in self.network.scanner.nodes:
            if node_id & 0xf0 == 0x10:
                for node_id_temp in range(0x12, 0x20):
                    node_id_all.append(node_id_temp)
            if node_id & 0xf0 == 0x20:
                for node_id_temp in range(0x22, 0x30):
                    node_id_all.append(node_id_temp)
            if node_id & 0xf0 == 0x30:
                for node_id_temp in range(0x32, 0x40):
                    node_id_all.append(node_id_temp)
            if node_id & 0xf0 == 0x40:
                for node_id_temp in range(0x42, 0x50):
                    node_id_all.append(node_id_temp)
            if node_id & 0xf0 == 0x50:
                for node_id_temp in range(0x52, 0x60):
                    node_id_all.append(node_id_temp)
            if node_id & 0xf0 == 0x60:
                for node_id_temp in range(0x62, 0x70):
                    node_id_all.append(node_id_temp)
            if node_id & 0xf0 == 0x70:
                for node_id_temp in range(0x72, 0x80):
                    node_id_all.append(node_id_temp)

        node_id_all = list(set(node_id_all))

        return node_id_all

    def setInterfaceDev(self, dev, can_dev):
        global CAN_DRIVER
        CAN_DRIVER = can_dev
        print('CAN_DRIVER = %d' % CAN_DRIVER)
        self.can_cmd = list()
        self.__dev = dev
        # self.__dev = self.network.bus.ser

        # node = self.network[0x1D]
        # print(node)

        if CAN_DRIVER == USE_UART:
            if USE_USB_UART == 0:
                # self.__dev.baudrate = 115200 * 8
                pass
            elif USE_USB_UART == 1 :
                self.__dev.baudrate = 460800
        elif CAN_DRIVER == USE_CANALYST_II:
            pass
        pass

    def devIsOpen(self):
        global CAN_DRIVER
        isOpen = False
        if CAN_DRIVER == USE_UART:
            isOpen = self.__dev.isOpen()

        elif CAN_DRIVER == USE_CANALYST_II:
            isOpen = True

        return isOpen

    def devClose(self):
        global CAN_DRIVER
        if CAN_DRIVER == USE_UART:
            self.__dev.close()
            # self.network.disconnect()

        elif CAN_DRIVER == USE_CANALYST_II:
            self.__dev.VCI_CloseDevice()
            pass

    def sendData(self, send_type, node_id, length, data):
        global CAN_DRIVER
        if CAN_DRIVER == USE_UART:
            if USE_USB_UART == 0:
                send = [0xAA, 0xAA,
                        node_id|(send_type&0xff), (send_type>>8)&0xff, 0x00, 0x00,
                        # data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7],
                        length, 0x00, 0x00, 0x00,
                        0x00,
                        0x55 , 0x55
                        ]
                send = send[0:6]+data[:length]+send[6:]
                send[18] = (send[2]+send[3]+send[14]+sum(data[:length]))&0xff # 校验位
                send = self.__dataCtrlDeal(send)

            elif USE_USB_UART == 1 :
                send = [0x66, 0xCC,
                        0x00, 0x00, 0x30, 0x03,
                        0x00, 0x00, (send_type>>8)&0xff, node_id|(send_type&0xff),
                        length,
                        # data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7],
                        0x00,
                        ]
                send = send[0:11]+data[:length]+send[11:]
                send[2] = ((len(send) - 4) >> 8) & 0xff # 0x66 0xcc length length 共4个字节
                send[3] = ((len(send) - 4)) & 0xff
                send[11+length] = (sum(send[2:(11+length)]))&0xff # 校验位

            # print(" ".join(hex(k) for k in send))
            self.__dev.write(send)

        elif CAN_DRIVER == USE_CANALYST_II:
            VCI_CAN_OBJ_ARRAY_2500 = VCI_CAN_OBJ * 15 # 结构体定义数组传入
            receive_can_data = VCI_CAN_OBJ_ARRAY_2500()

            self.__dev.VCI_Receive(ctypes.byref(receive_can_data), 15, 1)

            ubyte_array_8 = ctypes.c_ubyte * length
            data = ubyte_array_8( data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])
            ubyte_array_3 = ctypes.c_ubyte * 3
            reserved = ubyte_array_3(0, 0, 0)

            vci_can_obj = VCI_CAN_OBJ(send_type|node_id, 0, 0, 1, 0, 0, length, data, reserved)

            self.__dev.VCI_Transmit(ctypes.byref(vci_can_obj), 1)
            pass

    def sendStartCmd(self, node_id):
       data = [0x01, node_id, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
       self.sendData(self.NMT, 0, 8 , data)

    def __dataCtrlDeal(self, send_data):
        send_data2 = list(send_data)        # another list, 创建了的内存
        ctrl_times = int(0)
        for send_i, send_data_each in enumerate(send_data2[2:-2]):
            if send_data_each == CanopenProtocol.__CAN_HEAD or send_data_each == CanopenProtocol.__CAN_CTRL or send_data_each == CanopenProtocol.__CAN_TAIL :
                send_data.insert(send_i+ctrl_times+2, CanopenProtocol.__CAN_CTRL)
                ctrl_times = ctrl_times + 1

        return send_data

    def getRevData(self, rev_type, node_id, wait_time):
        receive_data = list()
        start_time = nowTime()

        if CAN_DRIVER == USE_UART:
            # self.can_cmd = self.find_can_command_format(self.__dev.read_all())
            while  nowTime() - start_time < wait_time:
                time.sleep(0.001)
                while 0 < len(self.can_cmd):
                    dat = self.can_cmd.pop(0)
                    # print(" ".join(hex(k) for k in dat))
                    if USE_USB_UART == 0:
                        can_id = (dat[3]<<8 | dat[2])
                        if node_id == 0:
                            if can_id >= rev_type|node_id: #上电返回
                                receive_data.append(dat)
                            pass
                        else:
                            if dat[3] == 0x02:  #PDO1（接收）
                                pass
                            elif can_id == self.PDO1_Tx|node_id: #PDO1（发送）
                                receive_data.append(dat[6:14])

                            elif dat[3] == 0x01 and dat[2] == 0x81: #PDO1（发送）
                                receive_data.append(dat[6:14])

                            elif can_id == rev_type|node_id: #上电返回
                                receive_data.append(dat)

                            elif dat[3] == 0x07:
                                # if dat[2] == node_id:
                                    # receive_data.append(dat)
                                # elif 0 == node_id:  # 获取所有nodeid的启动命令
                                    # receive_data.append(dat)

                                print(' 0x%02X Boot up' % (dat[2]))
                            elif dat[2] == rev_type and dat[3] == 0x00:  # 0x81 启动命令 返回
                                receive_data.append(dat[6:14])
                    elif USE_USB_UART == 1 :
                        can_id = (dat[3]<< 0 | dat[2]<< 8 | dat[1]<< 16 | dat[0] << 24)
                        if node_id == 0:
                            if can_id >= rev_type|node_id: #上电返回
                                # receive_data.append(dat)
                                # print(" ".join(hex(k) for k in dat))
                                dat_temp = [0xaa, 0xaa, dat[3], dat[2], dat[1], dat[0]]
                                # print(" ".join(hex(k) for k in dat_temp))
                                receive_data.append(dat_temp)
                                print(' 0x%02X Boot up1' % (dat[3]))
                            pass
                        else:
                            if can_id == self.PDO1_Tx|node_id: #PDO1（发送）
                                receive_data.append(dat[4:12])

                            elif (can_id & self.NODE_GUARD) == self.NODE_GUARD: #上电返回
                                receive_data.append(dat)
                                # print(1)
                                # dat = [0xaa, 0xaa, receive_can_data[i].ID&0xff]
                                # receive_data.append(dat)
                                # print(nowTime())
                                print(' 0x%02X Boot up2' % (dat[3]))

                            elif (can_id & self.SYNC) == self.SYNC : # 0x80 启动命令 返回
                                receive_data.append(dat[4:12])

                            else:
                                # print(" ".join(hex(k) for k in dat))
                                print('Rx: %s' % (" ".join(hex(k) for k in dat)))


                if len(receive_data):
                    # print(receive_data)
                    break

        elif CAN_DRIVER == USE_CANALYST_II:
            VCI_CAN_OBJ_ARRAY_2500 = VCI_CAN_OBJ * 20 # 结构体定义数组传入
            receive_can_data = VCI_CAN_OBJ_ARRAY_2500()

            while  (nowTime() - start_time) < wait_time:
                time.sleep(0.001)
                length = self.__dev.VCI_Receive(ctypes.byref(receive_can_data), 20, 1)

                if length > 0:
                    # print('receive length: %d' % length)
                    for i in range(length):
                        # for j in range(8):
                            # print('%02x' % receive_can_data[i].Data[j])
                        # print('i=%d ' % i, end='')
                        # print('ID=%02X ' % receive_can_data[i].ID, end='')  # 帧ID

                        # if receive_can_data[i].TimeFlag != 0: # 时间标识
                            # print('时间标识：%d ' % (receive_can_data[i].TimeStamp), end='')

                        # if receive_can_data[i].ExternFlag == 0:
                            # print('标准帧 ', end='')
                        # else:
                            # print('扩展帧 ', end='')

                        # if receive_can_data[i].RemoteFlag == 0:
                            # print('数据帧 ', end='')
                            # if receive_can_data[i].DataLen > (8):
                                # receive_can_data[i].DataLen = 8
                            # print('DataLen=%d ' % receive_can_data[i].DataLen, end='')
                            # print('数据：%s' % " ".join(hex(k) for k in receive_can_data[i].Data), end='')
                            # # print(type(receive_can_data[i].Data))
                            # # print('数据：%02X'list(receive_can_data[i].Data), end='')
                        # else:
                            # print('远程帧 ', end='')

                        # print('')

                        if receive_can_data[i].ID == 0x181:
                            if receive_can_data[i].Data[0] == node_id:
                                if receive_can_data[i].Data[2] >= receive_can_data[i].Data[3]:
                                    # receive_data.append(receive_can_data[i].Data[4])
                                    # receive_data.append(receive_can_data[i].Data[5])
                                    # receive_data.append(receive_can_data[i].Data[6])
                                    # receive_data.append(receive_can_data[i].Data[7])
                                    receive_data.append(receive_can_data[i].Data[0:8])
                        elif receive_can_data[i].ID == 0x81:
                            if receive_can_data[i].Data[0] != 0:
                                receive_data.append(receive_can_data[i].Data[0:8])

                        elif (receive_can_data[i].ID & rev_type) == rev_type:  # 目前只有上电启动发送过来的信息符合
                            print(1)
                            dat = [0xaa, 0xaa, receive_can_data[i].ID&0xff]
                            receive_data.append(dat)
                            print(nowTime())

                        elif receive_can_data[i].ID >= rev_type | 0x00 and receive_can_data[i].ID <= rev_type | 0x0F:
                            if node_id == 0:
                                receive_data.append(receive_can_data[i].Data[0:8])

                    break;


        if len(receive_data) != 0:
            # print(receive_data)
            pass
        return receive_data

    def receiveData(self):
        # if data != '':
        if CAN_DRIVER == USE_UART:
            if self.devIsOpen():
                while self.__dev.inWaiting() > 0:
                    can_cmd = self.find_can_command_format(self.__dev.read_all())
                    self.can_cmd = self.can_cmd + can_cmd
                    # try:
                        # # ser.read can return an empty string
                        # # or raise a SerialException
                        # rx_byte = self.__dev.read(1)
                    # except serial.SerialException:
                        # # return None, False
                        # pass

                    # if len(rx_byte) and ord(rx_byte) == 0x66:
                        # # print(ord(rx_byte))
                        # self.__dev.read(1)
                        # length = self.__dev.read(2)
                        # cmd = self.__dev.read(1)
                        # if len(cmd) and ord(cmd) == 0xB1:
                            # self.__dev.read(1)
                            # # id
                            # s = bytearray(self.__dev.read(4))
                            # # s = s[::-1]
                            # # arb_id = (struct.unpack('<I', s))[0]

                            # # dlc
                            # dlc = ord(self.__dev.read(1))

                            # # data
                            # data = self.__dev.read(dlc)

                            # checksum = self.__dev.read(1)
                            # # if rxd_byte == 0xBB:
                                # # received message data okay
                            # # msg = Message(timestamp=0,
                                          # # arbitration_id=arb_id,
                                          # # dlc=dlc,
                                          # # data=data)
                            # s = list(s)
                            # data = list(data)
                            # msg = s[:] + data[:]
                            # # print('rx: {}'.format(msg))
                            # self.can_cmd.append(msg)
                            # # return msg, False
                pass
            time.sleep(0.01)
        elif CAN_DRIVER == USE_CANALYST_II:
            pass
        # print(data)
        # data = ''
        # print(can_cmd)


    def find_can_command_format(self, data):
        # print('find_can_command_format...start')
        # print(type(data))
        data = list(data)
        can_cmd = list()
        # print(" ".join(hex(i) for i in data))

        if USE_USB_UART == 0:
            # print(len(data))
            # print(type(data))
            try:
                # for i,dat in enumerate(data[2:-3]):
                i = 2
                while i<len(data[:-2]):
                    # print('i=%d data=%#x, %#x, %#x' % (i, data[i-2], data[i-1], data[i]))
                    if (data[i-1] == CanopenProtocol.__CAN_CTRL) and (data[i]== CanopenProtocol.__CAN_HEAD or data[i]== CanopenProtocol.__CAN_CTRL or data[i]== CanopenProtocol.__CAN_TAIL): #去除重复的A5
                        data.pop(i-1)
                        # print(len(data))
                        # print(" ".join(hex(i) for i in data))
                    i = i+1
            except Exception as e:
                print(e)
                print('i=%d data=%#x, %#x' % (i, data[i-2], data[i-1]))

            # print('before:')
            # print(" ".join(hex(i) for i in data))

            # for i,dat1 in enumerate(data):
            # print(len(data))
            try:
                i = 1
                while i<len(data):
                    if data[i] == CanopenProtocol.__CAN_HEAD and data[i-1] == CanopenProtocol.__CAN_HEAD:
                        for j,dat2 in enumerate(data[i+9:]):
                            if data[i+9+j] == CanopenProtocol.__CAN_TAIL and data[i+9+j-1] == CanopenProtocol.__CAN_TAIL:
                                can_cmd.append(data[i-1:i+9+j+1])
                                # print('i=%d, j=%d ' % (i, j))
                                # print(" ".join(hex(k) for k in data[i-1:i+9+j+1]))
                                i = i + 9
                                break
                    else:
                        i = i + 1
            except Exception as e:
                print(e)
                print('i=%d, j=%d ' % (i, j))
                print(", ".join(hex(k) for k in self.can_cmd[0]))

            # print('after:')
            # for i, dat in enumerate(can_cmd):
                # print(" ".join(hex(i) for i in dat))
                # print(' ')
            # print('find_can_command_format... end')

        elif USE_USB_UART == 1 :
            i = 1
            while i<len(data):
                if data[i] == 0xCC and data[i-1] == 0x66 and data[i+3] == 0xb1 and data[i+4] == 0x03:
                    # print(data[i+5])
                    # print(data[i+9])
                    # print(data[i+9+data[i+9]])
                    dat = data[i+5:i+9] + data[i+10:i+10+data[i+9]]
                    # can_cmd.append(data[i+5:i+10+data[i+9]])
                    can_cmd.append(dat)
                    # print(can_cmd)
                    i = i + 10
                else:
                    i = i + 1

        return can_cmd

if __name__ == "__main__":
    '''
    main
    '''
    pass

