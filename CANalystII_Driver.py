
import os
import sys
import time
import ctypes
import threading

VCI_USBCAN2A = 4
STATUS_OK = 1

class VCI_INIT_CONFIG(ctypes.Structure):
    _fields_ = [
                ("AccCode"  , ctypes.c_ulong),
                ("AccMask"  , ctypes.c_ulong),
                ("Reserved" , ctypes.c_ulong),
                ("Filter"   , ctypes.c_ubyte),
                ("Timing0"  , ctypes.c_ubyte),
                ("Timing1"  , ctypes.c_ubyte),
                ("Mode"     , ctypes.c_ubyte),
            ]

class VCI_CAN_OBJ(ctypes.Structure):
    '''
    定义CAN信息帧的数据类型
    '''
    _fields_ = [
                ("ID"           , ctypes.c_uint),
                ("TimeStamp"    , ctypes.c_uint),
                ("TimeFlag"     , ctypes.c_ubyte),
                ("SendType"     , ctypes.c_ubyte),
                ("RemoteFlag"   , ctypes.c_ubyte),
                ("ExternFlag"   , ctypes.c_ubyte),
                ("DataLen"      , ctypes.c_ubyte),
                ("Data"         , ctypes.c_ubyte * 8),
                ("Reserved"     , ctypes.c_ubyte * 3),
            ]

class VCI_BAUD_TYPE(ctypes.Structure):
    _fields_ = [
                ("Baud"         , ctypes.c_ulong),
                ("SJW"          , ctypes.c_ubyte),
                ("BRP"          , ctypes.c_ubyte),
                ("SAM"          , ctypes.c_ubyte),
                ("PHSEG2_SEL"   , ctypes.c_ubyte),
                ("PRSEG"        , ctypes.c_ubyte),
                ("PHSEG1"       , ctypes.c_ubyte),
                ("PHSEG2"       , ctypes.c_ubyte),
            ]

class VCI_REF_NORMAL(ctypes.Structure):
    _fields_ = [
                ("Mode"     , ctypes.c_ubyte ),
                ("Filter"   , ctypes.c_ubyte),
                ("AccCode"  , ctypes.c_ulong),
                ("AccMask"  , ctypes.c_ulong),
                ("kBaudRate", ctypes.c_ulong),
                ("Timing0"  , ctypes.c_ubyte),
                ("Timing1"  , ctypes.c_ubyte),
                ("CANRX_EN" , ctypes.c_ubyte),
                ("UARTBAUD" , ctypes.c_ubyte),
            ]

class VCI_REF_STRUCT(ctypes.Structure):
    _fields_ = [
                ("RefNormal"    , ctypes.POINTER(VCI_REF_NORMAL) ),
                ("Reserved"     , ctypes.c_int8),
                ("BaudType"     , ctypes.POINTER(VCI_BAUD_TYPE) ),
            ]

class CANalystDriver:
    '''
    类的帮助信息，可以通过 __doc__ 查看
    '''

    def __init__(self, DeviceType, DeviceInd, CanNum):
        self.canDll = ctypes.windll.LoadLibrary('ControlCAN.dll')
        self.DeviceType = DeviceType
        self.DeviceInd = DeviceInd
        self.CanNum = CanNum
        # print(dir(self.canDll))

    def VCI_OpenDevice(self, Reserved):
        VCI_OpenDevice = getattr(self.canDll, 'VCI_OpenDevice')
        ret = VCI_OpenDevice(self.DeviceType, self.DeviceInd, Reserved)
        if ret == STATUS_OK:
            print('can device is open.')
        else:
            print('can device open fail!!!')
        # print(VCI_OpenDevice)    # 两种调用动态库方法的方式
        # print(self.canDll.VCI_OpenDevice)

        return ret

    def VCI_CloseDevice(self):
        VCI_CloseDevice = getattr(self.canDll, 'VCI_CloseDevice')
        ret = VCI_CloseDevice(self.DeviceType, self.DeviceInd)
        if ret == STATUS_OK:
            print('can device is closed')
        else:
            print('can device close fail!!!')


    def VCI_InitCAN(self, pInitConfig):
        VCI_InitCAN = getattr(self.canDll, 'VCI_InitCAN')
        ret = VCI_InitCAN(self.DeviceType, self.DeviceInd, self.CanNum, pInitConfig)
        if ret == STATUS_OK:
            print('can device Init OK!')
            self.thread_1 = threading.Thread(target=self.ReceiveThread) #建立一个线程，调用receive_data_thread方法，不带参数
            self.thread_1.setDaemon(True) #声明为守护线程，设置的话，子线程将和主线程一起运行，并且直接结束，不会再执行循环里面的子线程
            # self.thread_1.start()
        else:
            print('can device Init fail!!!')

        pass

    def VCI_StartCAN(self):
        VCI_StartCAN = getattr(self.canDll, 'VCI_StartCAN')
        ret = VCI_StartCAN(self.DeviceType, self.DeviceInd, self.CanNum)
        if ret == STATUS_OK:
            print('can start ok.')
        else:
            print('can start fail!!!')

    def VCI_Transmit(self, pVci_can_obj, array_length):
        '''
        @bref: VCI_Transmit(self, vci_can_obj)
        '''
        VCI_Transmit = getattr(self.canDll, 'VCI_Transmit')
        real_length = VCI_Transmit(self.DeviceType, self.DeviceInd, self.CanNum, pVci_can_obj, array_length)

        return real_length


    def VCI_GetReference(self):
        '''
        未完成
        '''
        VCI_GetReference = getattr(self.canDll, 'VCI_GetReference')
        ret = VCI_GetReference(self.DeviceType, self.DeviceInd, self.CanNum, 0, 0)
        if ret == STATUS_OK:
            print('can start ok.')
        else:
            print('can start fail!!!')

    def VCI_Receive(self, pVci_can_obj, array_length, wait_time):
        '''
        @bref: VCI_Receive(self, vci_can_obj)
        '''
        VCI_Receive = getattr(self.canDll, 'VCI_Receive')
        length = VCI_Receive(self.DeviceType, self.DeviceInd, self.CanNum, pVci_can_obj, array_length, wait_time)
        return length

    def ReceiveThread(self):
        VCI_CAN_OBJ_ARRAY_2500 = VCI_CAN_OBJ * 2500 # 结构体定义数组传入
        receive_data = VCI_CAN_OBJ_ARRAY_2500()
        time.sleep(0.1)
        # print(type(receive_data))
        # print(dir(receive_data))
        # print(receive_data.__doc__)
        print('start ReceiveThread.')
        while True:
            length = self.VCI_Receive(ctypes.byref(receive_data), 2500, 200)
            if length > 0:
                print(length)
                for i in range(length):
                    print('i=%d ' % i, end='')
                    print('ID=%02X ' % receive_data[i].ID, end='')  # 帧ID

                    if receive_data[i].TimeFlag != 0: # 时间标识
                        print('时间标识：%d ' % (receive_data[i].TimeStamp), end='')

                    if receive_data[i].ExternFlag == 0:
                        print('标准帧 ', end='')
                    else:
                        print('扩展帧 ', end='')

                    if receive_data[i].RemoteFlag == 0:
                        print('数据帧 ', end='')
                        if receive_data[i].DataLen > (8):
                            receive_data[i].DataLen = 8
                        print('DataLen=%d ' % receive_data[i].DataLen, end='')
                        print('数据：%s' % " ".join(hex(k) for k in receive_data[i].Data), end='')
                        # print(type(receive_data[i].Data))
                        # print('数据：%02X'list(receive_data[i].Data), end='')
                    else:
                        print('远程帧 ', end='')

                    print('')


                pass
            else:
                pass

            time.sleep(0.001)
        pass


'''
main
'''
if __name__ == "__main__":

    print('当前工作路径为：%s ' % (os.getcwd()))
    print('当前运行程序为：%s ' % (sys.argv[0]))

    index = 0
    can_num = 0
    canDll = CANalystDriver(VCI_USBCAN2A, index, can_num)
    canDll.VCI_OpenDevice(0)
    initConfig = VCI_INIT_CONFIG()
    initConfig.AccCode = 0x80000008
    initConfig.AccMask = 0xFFFFFFFF
    initConfig.Reserved = 0
    initConfig.Filter = 2
    initConfig.Timing0 = 0x00
    initConfig.Timing1 = 0x14
    initConfig.Mode = 0
    canDll.VCI_InitCAN(ctypes.byref(initConfig))
    canDll.VCI_StartCAN()
    canDll.thread_1.start()

    ubyte_array_8 = ctypes.c_ubyte * 8
    data = ubyte_array_8(1, 2, 3, 4, 5, 6, 7, 8)
    ubyte_array_3 = ctypes.c_ubyte * 3
    reserved = ubyte_array_3(0, 0, 0)

    vci_can_obj = VCI_CAN_OBJ(0x712, 0, 0, 1, 0, 0, 8, data, reserved)

    canDll.VCI_Transmit(ctypes.byref(vci_can_obj), 1)

    # canDll.VCI_CloseDevice()

    while True:
        pass


