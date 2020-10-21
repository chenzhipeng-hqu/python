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

from project import log

logger = log.Log(__name__, log_path=os.getcwd()).getlog()

class JDFarmer(object):
    """

    """
    def __init__(self, addr):
        self.d = u2.connect(addr)

    def open(self):
        pass

    def collect(self):
        pass

    def run(self):
        # 京东app
        self.d.xpath('//android.view.ViewGroup/android.widget.RelativeLayout[5]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.ImageView[1]').click()
        time.sleep(1)

        # 免费水果
        self.d(text="免费水果").click()
        time.sleep(1)

        # 领水滴
        self.d.xpath('//*[@resource-id="app"]/android.view.View[1]/android.view.View[1]/android.view.View[2]/android.view.View[2]/android.view.View[9]/android.view.View[2]').click()
        time.sleep(1)

        # 去领取
        self.d(text="去领取").click()
        time.sleep(5)

        # 收下水滴
        self.d(text="收下水滴").click()
        time.sleep(1)

        #关闭领取水滴
        self.d.xpath('//*[@resource-id="app"]/android.view.View[1]/android.view.View[1]/android.view.View[3]/android.view.View[1]/android.view.View[3]').click()
        time.sleep(1)

        #返回
        self.d.press('back')
        time.sleep(1)

    def run2(self):
        # 京东app2
        self.d.xpath('//android.view.ViewGroup/android.widget.RelativeLayout[6]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.ImageView[1]').click()
        time.sleep(1)

        # 免费水果
        self.d(text="免费水果").click()
        time.sleep(3)

        # 领水滴
        self.d.click(0.273, 0.717)
        time.sleep(1)

        # 去领取
        self.d.click(0.839, 0.586)
        time.sleep(5)

        # 收下水滴
        self.d.click(0.494, 0.691)
        time.sleep(1)

        #关闭领取水滴
        self.d.click(0.964, 0.493)
        time.sleep(1)

        #返回
        self.d.press('back')
        time.sleep(1)



if __name__ == '__main__':
    logger.info('\r\n ---------------- welcom to use -----------------')

