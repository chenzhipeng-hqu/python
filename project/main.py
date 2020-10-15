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


if __name__ == '__main__':
    logger.info('\r\n ---------------- welcom to use -----------------')
    d = u2.connect('192.168.31.70')

    # 到桌面
    # cmd = "input keyevent 3"
    # adbshellcommand(cmd)

    # 自动发朋友圈
    sendPYQ()
