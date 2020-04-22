# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/03/26
# @Author  : 陈志鹏
# @File    : fetch.py

"""
提取一个工作簿的所有sheet信息， 合并成一个新的文件
"""

import os
import sys
import time
import logging
import pyautogui
import pyperclip
import xml.sax
import configparser
import pandas as pd
import financial_ui as ui
from PySide2.QtWidgets import *
from PySide2.QtCore import *

logging.basicConfig(level=logging.DEBUG,  filename='out.log',
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')

logger = logging.getLogger(__name__)

class Practice(QObject):
    #message_singel = Signal(str)
    finish_singel = Signal()
    statusBar_singel = Signal(str)

    def __init__(self):
        super(Practice, self).__init__()

    def __del__(self):
        print('delete %s' % self.__class__.__name__)

    def practice1(self):
        df = pd.DataFrame({'ID':[1, 2, 3], 'Name':['Tim', 'Victor', 'Nick']})
        # df = pd.DataFrame()
        df.set_index('ID', inplace=True)
        file_path = os.getcwd()
        file_name = os.path.join(file_path, 'datas/practice1.xlsx')
        df.to_excel(file_name)
        print('Done!')

    def practice2(self):
        file_path = os.getcwd()
        file_name = os.path.join(file_path, 'datas/practice1.xlsx')
        df = pd.read_excel(file_name, header=None)
        df.columns = ['col1', 'col2']   # 添加列名
        print(df.head())
        print('Done!')


if __name__ == '__main__':
    practice = Practice()
    # practice.practice1()
    practice.practice2()
