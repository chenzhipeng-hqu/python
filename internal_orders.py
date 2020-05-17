# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/03/26
# @Author  : 陈志鹏
# @File    : *.py

import os
import sys
import codecs
import log
import pyautogui
import xml.sax
import configparser
import pandas as pd
from financial_ui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from other_payables import *


class WorkerInterOrders(QObject):
    message_singel = Signal(str)
    finish_singel = Signal()
    statusBar_singel = Signal(str)

    def __init__(self):
        super(WorkerInterOrders, self).__init__()

    def filter1(self, str):
        return '管理费用-研究开发费用' in str

    def filter2(self, x):
        return pd.isnull(x)

    def request_date(self, x):
        return x[0:10]

    def set_parameter(self, path):
        self.path = path

    def filter(self):
        self.message_singel.emit('开始调整.\r\n')
        # pd.options.display.max_columns = 777
        # sheet_FAGLL03 = pd.read_excel("D:/CZP/python/excel_openpyxl/original_data/调整内部订单号.xls", sheet_name='FAGLL03', index_col = r'年度/月份')
        # sheet_FAGLL03 = pd.read_excel("D:/CZP/python/excel_openpyxl/original_data/调整内部订单号.xls", sheet_name='FAGLL03')
        src_file = os.path.join(self.path, '调整内部订单号.xls')
        # print(src_file)
        sheet_FAGLL03 = pd.read_excel(src_file, sheet_name='FAGLL03')

        sheet_FAGLL03 = sheet_FAGLL03.loc[sheet_FAGLL03['科目名称'].apply(self.filter1)]\
                                .loc[sheet_FAGLL03['项目编号'].apply(self.filter2)]

        # sheet_FAGLL03['年度/月份'] = sheet_FAGLL03['年度/月份'].apply(request_date)
        sheet_FAGLL03['年度/月份'] = sheet_FAGLL03['年度/月份'].dt.strftime('%Y-%m-%d')
        sheet_FAGLL03['过账日期'] = sheet_FAGLL03['过账日期'].dt.strftime('%Y-%m-%d')
        sheet_FAGLL03['凭证日期'] = sheet_FAGLL03['凭证日期'].dt.strftime('%Y-%m-%d')

        # print(sheet_FAGLL03.head(), sheet_FAGLL03.shape)

        dst_file = os.path.join(self.path, 'export.xlsx')
        sheet_FAGLL03.to_excel(dst_file, sheet_name='FAGLL03', index=False)

        self.message_singel.emit('调整完成.\r\n')
        self.finish_singel.emit()


if __name__ == '__main__':
    worker_inter_orders = WorkerInterOrders()

    path = os.path.join(os.getcwd(), 'datas\original_data')
    worker_inter_orders.set_parameter(path)
    worker_inter_orders.filter()
