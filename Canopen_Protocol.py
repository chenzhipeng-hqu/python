
#
# -*- coding: utf-8 -*-

"""
In this example, we create a simple window in PyQt5.

author: chenzhipeng3472
last edited: 04-July-2018
"""
__author__ = 'chenzhipeng3472'


import time

from CANalystII_Driver import *

USE_UART = 0
USE_CANALYST_II = 1
global CAN_DRIVER
CAN_DRIVER = USE_CANALYST_II
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


    def __init__(self):
        pass

    def __del__(self):
        pass

    def setInterfaceDev(self, dev, can_dev):
        global CAN_DRIVER
        CAN_DRIVER = can_dev
        print('CAN_DRIVER = %d' % CAN_DRIVER)
        self.can_cmd = list()
        if CAN_DRIVER == USE_UART:
            self.__dev = dev
        elif CAN_DRIVER == USE_CANALYST_II:
            self.__dev = dev
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

        elif CAN_DRIVER == USE_CANALYST_II:
            self.__dev.VCI_CloseDevice()
            pass

    def sendData(self, send_type, node_id, length, data):
        global CAN_DRIVER
        if CAN_DRIVER == USE_UART:
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
            self.__dev.write(send)

        elif CAN_DRIVER == USE_CANALYST_II:
            VCI_CAN_OBJ_ARRAY_2500 = VCI_CAN_OBJ * 200 # 结构体定义数组传入
            receive_can_data = VCI_CAN_OBJ_ARRAY_2500()

            self.__dev.VCI_Receive(ctypes.byref(receive_can_data), 200, 1)

            ubyte_array_8 = ctypes.c_ubyte * length
            data = ubyte_array_8( data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])
            ubyte_array_3 = ctypes.c_ubyte * 3
            reserved = ubyte_array_3(0, 0, 0)

            vci_can_obj = VCI_CAN_OBJ(send_type|node_id, 0, 0, 1, 0, 0, length, data, reserved)

            self.__dev.VCI_Transmit(ctypes.byref(vci_can_obj), 1)
            pass

    def sendStartCmd(self, node_id):
       data = [0x01, node_id, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
       self.sendData(0, 0, 8 , data)

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
            while  nowTime() - start_time < wait_time:
                time.sleep(0.001)
                while 0 < len(self.can_cmd):
                    dat = self.can_cmd.pop(0)
                    # print(" ".join(hex(k) for k in dat))
                    can_id = (dat[3]<<8 | dat[2])
                    if node_id == 0:
                        if can_id >= rev_type|node_id: #上电返回
                            receive_data.append(dat)
                        pass
                    else:
                        if dat[3] == 0x02:  #PDO1（接收）
                            pass
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


                if len(receive_data):
                    # print(receive_data)
                    break

        elif CAN_DRIVER == USE_CANALYST_II:
            VCI_CAN_OBJ_ARRAY_2500 = VCI_CAN_OBJ * 2500 # 结构体定义数组传入
            receive_can_data = VCI_CAN_OBJ_ARRAY_2500()

            while  nowTime() - start_time < wait_time:
                time.sleep(0.001)
                length = self.__dev.VCI_Receive(ctypes.byref(receive_can_data), 2500, wait_time*1000)

                if length > 0:
                    # print('receive length: %d' % length)
                    for i in range(length):
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
                            if receive_can_data[i].Data[0] == node_id:
                                receive_data.append(receive_can_data[i].Data[0:8])

                        elif receive_can_data[i].ID == rev_type | node_id:  # 目前只有上电启动发送过来的信息符合
                            print(1)
                            dat = [0xaa, 0xaa, receive_can_data[i].ID&0xff]
                            receive_data.append(dat)

                        elif receive_can_data[i].ID >= rev_type | 0x00 and receive_can_data[i].ID <= rev_type | 0x0F:
                            if node_id == 0:
                                receive_data.append(receive_can_data[i].Data[0:8])


        # print(receive_data)
        return receive_data

    def receiveData(self):
        # if data != '':
        if CAN_DRIVER == USE_UART:
            if self.devIsOpen():
                while self.__dev.inWaiting() > 0:
                    self.can_cmd = self.find_can_command_format(self.__dev.read_all())
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
        # print(type(data))
        for i,dat in enumerate(data[2:-2]):
            if (data[i-1] == CanopenProtocol.__CAN_CTRL) and (data[i]== CanopenProtocol.__CAN_HEAD or data[i]== CanopenProtocol.__CAN_CTRL or data[i]== CanopenProtocol.__CAN_TAIL): #去除重复的A5
                data.remove(data[i-1])

        # print('before:')
        # print(" ".join(hex(i) for i in data))

        # for i,dat1 in enumerate(data):
        i = 1
        # print(len(data))
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
        # print(", ".join(hex(k) for k in self.can_cmd[0]))
        # print('after:')
        # for i, dat in enumerate(can_cmd):
            # print(" ".join(hex(i) for i in dat))
            # print(' ')
        # print('find_can_command_format... end')
        return can_cmd

if __name__ == "__main__":
    '''
    main
    '''
    pass

