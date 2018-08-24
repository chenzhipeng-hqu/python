
#
# -*- coding: utf-8 -*-

"""
In this example, we create a simple window in PyQt5.

author: chenzhipeng3472
last edited: 04-July-2018
"""
__author__ = 'chenzhipeng3472'

import time


nowTime = lambda:int(round(time.time()*1000))

class CanopenProtocol:
    '''
    canopen
    '''

    __CAN_HEAD = int(0xAA)
    __CAN_CTRL = int(0xA5)
    __CAN_TAIL = int(0x55)

    PDO1_Tx = 0x0180
    PDO2_Tx = 0x0280
    PDO3_Tx = 0x0380
    PDO4_Tx = 0x0480

    PDO1_Rx = 0x0200
    PDO2_Rx = 0x0300
    PDO3_Rx = 0x0400
    PDO4_Rx = 0x0500

    def __init__(self):
        pass

    def __del__(self):
        pass

    def setInterfaceDev(self, dev):
        self.can_cmd = list()
        self.__dev = dev
        pass

    def sendData(self, send_type, node_id, length, data):
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

        while  nowTime() - start_time < wait_time:
            time.sleep(0.001)
            while 0 < len(self.can_cmd):
                dat = self.can_cmd.pop(0)
                print(" ".join(hex(k) for k in dat))
                if dat[3] == 0x02:  #PDO1（接收）
                    pass
                elif dat[3] == 0x01: #PDO1（发送）
                    pass
                elif dat[3] == 0x07:
                    if dat[2] == node_id:
                        receive_data.append(dat)
                    elif 0 == node_id:  # 获取所有nodeid的启动命令
                        receive_data.append(dat)
                    print(' 0x%02X Boot up' % (dat[2]))

            if len(receive_data):
                break
        return receive_data

    def receiveData(self, data):
        # if data != '':
        self.can_cmd = self.find_can_command_format(data)
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
        # for i, dat in enumerate(self.can_cmd):
            # print(" ".join(hex(i) for i in dat))
        # print('find_can_command_format... end')
        return can_cmd

if __name__ == "__main__":
    '''
    main
    '''
    pass

