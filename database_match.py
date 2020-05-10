# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/03/26
# @Author  : 陈志鹏
# @File    : financial_tools.py

import os
import sys
import codecs
import logging
import pyautogui
import xml.sax
import configparser
import pandas as pd
from financial_ui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from other_payables import *
from internal_orders import *
from custom_control import *
from others.merge import *
from others.fetch import *

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

logging.basicConfig(
    level=logging.DEBUG,
    filename='out.log',
    datefmt='%Y/%m/%d %H:%M:%S',
    format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')

logger = logging.getLogger(__name__)

nowTime = lambda:int(round(time.time()*1000))

class DatabaseMatch(QObject):
    finish_singel = Signal()
    statusBar_singel = Signal(str)

    def __init__(self):
        super(DatabaseMatch, self).__init__()

    def __del__(self):
        print('delete %s' % self.__class__.__name__)

    def subject_num_ops(self, data):
        # print(type(data))
        # print(data['功能范围'])
        if data['总账科目'] >= 66030000:
            ret = self.src_index_df[self.src_index_df['总账科目'] == data['总账科目']]['长文本'].values[0]
        elif pd.isnull(data['功能范围']):
            ret = '#N/A'
        else:
            ret = self.src_index_df[self.src_index_df['功能范围'] == data['功能范围']]['功能范围名称'].values[0] + \
                  self.src_index_df[self.src_index_df['总账科目'] == data['总账科目']]['长文本'].values[0]

        return ret

    def abstract_ops(self, data):
        if str(data['分配']).find('FI') == -1:
            ret = data['文本']
        else:
            ret = data['分配'] + ',' +  data['文本']

        return ret

    def department_name_ops(self, data):
        temp = self.src_index_df[self.src_index_df['成本中心编码'] == data['成本中心']]
        if temp.empty:
            ret = '#N/A'
        else:
            ret = temp['成本中心'].values[0]
        return ret

    def project_num_ops(self, data):
        if pd.isnull(data['订单']):
            ret = ''
        else:
            temp = self.src_index_df[self.src_index_df['SAP订单号'] == data['订单']]
            if temp.empty:
                ret = '#N/A'
            else:
                ret = temp['SAP项目名称'].values[0]
        return ret

    def company_ops(self, data):
    #     if pd.isnull(data['公司代码']):
    #         ret = ''
    #     else:
        temp = self.src_index_df[self.src_index_df['编码'] == data['公司代码']]
        if temp.empty:
            ret = '#N/A'
        else:
            ret = temp['简称'].values[0]
        return ret

    def run(self):
        src_file = r'./datas/original_data/调整内部订单号.xls'
        dst_file = r'./datas/original_data/module.xls'

        self.src_index_df = pd.read_excel(src_file, sheet_name='索引')
        src_data_df = pd.read_excel(src_file, sheet_name='FAGLL03')
        # print(src_index_df.head())
        # print(src_data_df.head())

        # dst_df = pd.DataFrame(columns=['会计年度', '期间', '凭证日期', '凭证编号', '科目编号', '科目名称', '借方本币', '摘要', '部门', '部门名称', '申请人',
        #                                '员工姓名', '项目编号', '项目名称', '账套'])
        dst_df = pd.read_excel(dst_file)
        dst_df['会计年度'] = src_data_df['会计年度']
        dst_df['期间'] = src_data_df['记帐期间']
        dst_df['凭证日期'] = src_data_df['过账日期'].dt.strftime('%Y-%m-%d')
        dst_df['凭证编号'] = src_data_df['凭证编号']
        dst_df['科目编号'] = src_data_df['总账科目']
        dst_df['借方本币'] = src_data_df['本币金额']
        dst_df['部门'] = src_data_df['成本中心']
        dst_df['项目编号'] = src_data_df['订单']

        dst_df['科目名称'] = src_data_df.apply(self.subject_num_ops, axis=1)
        dst_df['摘要'] = src_data_df.apply(self.abstract_ops, axis=1)
        dst_df['部门名称'] = src_data_df.apply(self.department_name_ops, axis=1)
        dst_df['项目名称'] = src_data_df.apply(self.project_num_ops, axis=1)
        dst_df['账套'] = src_data_df.apply(self.company_ops, axis=1)

        # print(temp)
        # print(len(temp))
        # dst_df['科目名称'] = temp


        dst_df.to_excel(dst_file, index=False, engine='openpyxl')

if __name__ == '__main__':
    starttime = nowTime()
    database_match = DatabaseMatch()
    database_match.run()
    print('finish', nowTime()-starttime, 'ms')