# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/05/30
# @Author  : 陈志鹏
# @File    : xx.py
"""

"""

__author__ = '陈志鹏'

import os
import sys
work_path = os.path.join(os.path.dirname(sys.argv[0]), "../")
sys.path.append(os.path.abspath(work_path))
os.chdir(work_path)

import uiautomator2 as u2

from project.do_adb_click import *
from project.do_adb_arobot import *
from project.jingdong import *
from project.taobao import *

from project import log

logger = log.Log(__name__, log_path=os.getcwd()).getlog()


if __name__ == '__main__':
    logger.info('\r\n ---------------- welcom to use -----------------')
    # d = u2.connect('192.168.31.70')
    # d = u2.connect('10.42.0.179')
    # d = u2.connect('6c2a9126')
    # d = u2.connect_usb('6c2a9126')
    # d.click(0.123, 0.724)
    # d.xpath('//*[@resource-id="app"]/android.view.View[1]/android.view.View[1]/android.view.View[2]/android.view.View[2]/android.view.View[9]/android.view.View[1]').click()
    # d.xpath('//*[@resource-id="app"]/android.view.View[1]/android.view.View[3]/android.view.View[2]/android.view.View[1]')


    # 到桌面
    # cmd = "input keyevent 3"
    # adbshellcommand(cmd)

    # 东东农场
    # jingdong_farmer = JDFarmer('6c2a9126')
    # jingdong_farmer.run2()

    # 淘宝农场
    taobao_farmer = TBFarmer('6c2a9126')
    taobao_farmer.run()

    # send_touch_event('tap', 432, 1217)
    # send_touch_event('swipe', 432, 1217, 432+100, 1217)

    # element = Element()
    # element.getPicture()

