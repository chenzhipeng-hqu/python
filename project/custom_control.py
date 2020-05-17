# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/03/26
# @Author  : 陈志鹏
# @File    : custom_control.py

from project.internal_orders import *

# if hasattr(sys, 'frozen'):
#     os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']


class WorkerCustCtrl(QObject):
    message_singel = Signal(str)
    finish_singel = Signal()
    statusBar_singel = Signal(str)
    mouse_singel = Signal(int, int)

    def __init__(self):
        super(WorkerCustCtrl, self).__init__()

        # 加载现有配置文件
        conf = configparser.ConfigParser()
        path = os.path.join(os.getcwd(), 'configure.ini')
        conf.read(path, encoding="utf-8-sig")
        # self.sections = conf.sections()
        # centers = conf.get("center", 'centers')
        # print(centers)
        # self.center_list = centers.split(',')
        # print('center_list:', self.center_list)

        control = conf.items("control")
        # center_list = [position[0] for position in center]
        # position_list = [position[1].split(',') for position in center]
        # self.centers = dict(zip(center_list, position_list))
        self.controls = {ctrl[0]: ctrl[1].split(',') for ctrl in control}
        # print(self.controls)

    def set_parameter(self):
        pass

    def start(self):
        for ctrl in self.controls.items():
            print(ctrl)
            if ctrl[1][0] == 'move':
                pyautogui.moveTo(int(ctrl[1][1]), int(ctrl[1][2]))
            elif ctrl[1][0] == 'click':
                if len(ctrl[1]) > 1:
                    pyautogui.click(duration=int(ctrl[1][1]))
                else:
                    pyautogui.click()
            elif ctrl[1][0] == 'doubleClick':
                if len(ctrl[1]) > 1:
                    pyautogui.doubleClick(duration=int(ctrl[1][1]))
                else:
                    pyautogui.doubleClick()
            elif ctrl[1][0] == 'dragTo':
                if len(ctrl[1]) > 3:
                    pyautogui.dragTo(int(ctrl[1][1]), int(ctrl[1][2]), duration=int(ctrl[1][3]))
                else:
                    pyautogui.dragTo(int(ctrl[1][1]), int(ctrl[1][2]))
            elif ctrl[1][0] == 'input':
                pyautogui.write(ctrl[1][1])
            elif ctrl[1][0] == 'press':
                pyautogui.press(ctrl[1][1])
            elif ctrl[1][0] == 'hotkey':
                pyautogui.hotkey(ctrl[1][1], ctrl[1][2])
        pass

    def get_size(self):
        return pyautogui.size()

    def run(self):
        # x, y = pyautogui.size()
        # self.message_singel.emit("当前屏幕的分辨率是{}*{}\r\n".format(x, y))
        while True:
            x, y = pyautogui.position()
            self.mouse_singel.emit(x, y)
            QThread.usleep(100000)
            # positionStr = 'X: ' + str(x).rjust(4) + 'Y: ' + str(y).rjust(4)

    def get_pic_center(self):
        pass

if __name__ == '__main__':
    worker_cust_ctrl = WorkerCustCtrl()
    worker_cust_ctrl.set_parameter()
    # worker_cust_ctrl.start()
    button7location = pyautogui.locateOnScreen('datas/picture/button7.png')
    print(button7location)
    button7location = pyautogui.locateCenterOnScreen('datas/picture/button7.png')
    print(button7location)

    button7greylocation = None
    while(button7greylocation == None):
        button7greylocation = pyautogui.locateCenterOnScreen( 'datas/picture/button7grey.png')
        # button7greylocation = pyautogui.locateCenterOnScreen(
        #                 'datas/picture/button7grey.png', region=(190, 250, 300, 200))
        print(button7greylocation)
        time.sleep(3)

    # try:
    #     while True:
    #         x, y = pyautogui.position()
    #         positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
    #         pixelColor = pyautogui.screenshot().getpixel((x, y))
    #         positionStr += 'RGB: (' + str(pixelColor[0]).rjust(3)
    #         positionStr += ', ' + str(pixelColor[1]).rjust(3)
    #         positionStr += ', ' + str(pixelColor[2]).rjust(3) + ')'
    #         print(positionStr, end='')
    #         print('\b' * len(positionStr), end='')
    # except KeyboardInterrupt:
    #     print('\nDone.')
