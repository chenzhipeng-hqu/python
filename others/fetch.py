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
import numpy as np
import financial_ui as ui
from PySide2.QtWidgets import *
from PySide2.QtCore import *

logging.basicConfig(level=logging.DEBUG,  filename='out.log',
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')

logger = logging.getLogger(__name__)


class WorkerFetch(QObject):
    #message_singel = Signal(str)
    finish_singel = Signal()
    statusBar_singel = Signal(str)

    def __init__(self):
        super(WorkerFetch, self).__init__()

    def __del__(self):
        print('delete %s' % self.__class__.__name__)

    def balance_sheet_set_parameter(self, *args, **kwargs):
        self.src_file = kwargs.get('src_file')
        # self.dst_file = kwargs.get('dst_file')
        self.subject = kwargs.get('subject')
        self.month = kwargs.get('month')
        self.dst_file = os.path.dirname(self.src_file)
        self.dst_file = os.path.join(self.dst_file, '%s-%s.xlsx' % (self.subject, self.month))
        # print(self.dst_file)

    def balance_sheet_fetch(self):
        # print(self.src_file)
        # print(self.subject)
        # print(self.month)
        if self.subject == '' or self.month == '':
            self.statusBar_singel.emit('请填入提取信息.\r\n')
            self.finish_singel.emit()
            return

        f = pd.ExcelFile(self.src_file)
        print(f.sheet_names)
        # data = np.array(['sheet', '项目', '月份', '数据'])
        # s = pd.Series(data)
        # data = pd.DataFrame()
        data = pd.DataFrame(columns=['sheet', '项目', '月份', '数据'])
        # data.loc[0] = data.apply(['项目', '月份'], axis=1)
        data['sheet'] = f.sheet_names
        for i, name in enumerate(f.sheet_names):
        #     df = pd.read_excel(src_file, sheet_name=i)
        #     print(i, ': ', name)
            self.statusBar_singel.emit('正在提取sheet%d %s...\r\n' % (i, name))
            data['项目'].at[i] = self.subject
            data['月份'].at[i] = self.month
            df = pd.read_excel(self.src_file, sheet_name=name, header=4, index_col=0, dtype=str)
            value = df[df.index == self.subject][self.month].values
            data['数据'].at[i] = float(value[0])
            # data['数据'].at[i] = round(float(value[0]), 2)
        # df = pd.read_excel(src_file, sheet_name=f.sheet_names[0], header=4, index_col=0, dtype=str)
        # print(df.head())
        # print(df.columns)
        # print(df['1月'])
        # print(df[df.index == subject][month].values)
        # pd.Series([subject, month, value], index=['项目', '月份', '数据'])

        data.to_excel(self.dst_file, index=False)
        print(data.head(3))
        print('finish')
        self.statusBar_singel.emit('提取完成, %s\r\n' % (os.path.basename(self.dst_file)))
        self.finish_singel.emit()


if __name__ == '__main__':
    worker_fetch = WorkerFetch()

    worker_fetch.balance_sheet_set_parameter(\
                src_file=r'D:\CZP\python\FinancialTools\datas\\2020年02月各公司财务报表-V3.xlsx',\
                dst_file=r'D:\CZP\python\FinancialTools\datas\\fetch.xlsx',\
                subject=u'货币资金',\
                month=u'1月')
    worker_fetch.balance_sheet_fetch()