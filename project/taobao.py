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

import random
import uiautomator2 as u2

from project.do_adb_click import *
from project.do_adb_arobot import *

from project import log

logger = log.Log(__name__, log_path=os.getcwd()).getlog()

class TBFarmer(object):
    """

    """
    def __init__(self, addr):
        # self.d = u2.connect(addr)
        self.element = Element()
        # self.evevt = Event()
        pass

    def open(self):
        pass

    def collect(self):
        pass

    def baba_farmer_sunny(self):
        # 点击领阳光
        # e = self.element.findElementByName(u"领阳光")
        # self.evevt.touch(e[0], e[1])
        adbshellcommand('input tap %d %d' % (950, 1780))
        time.sleep(0.5)

        # 点击去浏览
        adbshellcommand('input tap %d %d' % (920, 1560))
        time.sleep(17)
        adbshellcommand('input keyevent KEYCODE_BACK')
        time.sleep(2)

    def baba_farmer_tree(self):
        # 点击芒果
        # adbshellcommand('input tap %d %d' % (150, 700))
        # time.sleep(4)
        #
        # # 点击集肥料
        adbshellcommand('input tap %d %d' % (980, 1700))
        time.sleep(3)

        # 点击去领取 7/12/20/22点
        e = self.element.findElementByName(u"去领取")
        logger.debug('[%d, %d]' % (e[0], e[1]))
        adbshellcommand('input tap %d %d' % (e[0], e[1]))


        # adbshellcommand('input keyevent KEYCODE_BACK')

    def miao_coin_contiune_click(self):
        """
        2020双十一淘宝点击喵币
        :return:
        """
        for i in range(500):
            logger.debug(i)
            x = 400 + random.randint(0, 250)
            y = 1000 + random.randint(0, 300)
            adbshellcommand('input tap %d %d' % (x, y))
            time.sleep(0.3)

    def run(self):
        # self.baba_farmer_sunny()
        # self.baba_farmer_tree()
        # self.miao_coin_contiune_click()

if __name__ == '__main__':
    logger.info('\r\n ---------------- welcom to use -----------------')

