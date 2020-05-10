# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/03/26
# @Author  : 陈志鹏
# @File    : xxx.py

"""
提取一个多个工作簿的sheet信息， 合并到费用报表底稿文件
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
import openpyxl
import financial_ui as ui
from PySide2.QtWidgets import *
from PySide2.QtCore import *

logging.basicConfig(level=logging.DEBUG,  filename='out.log',
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')

logger = logging.getLogger(__name__)

nowTime = lambda:int(round(time.time()*1000))

class MergeExpense(QObject):
    #message_singel = Signal(str)
    finish_singel = Signal()
    statusBar_singel = Signal(str)

    def __init__(self):
        super(MergeExpense, self).__init__()
        self.expense_table = [
            #0.identification, 1.expense, 2.copy_row, 3.read_row, 4, read_col
            ['G', '管理费用', 92-5, 4, 2],
            ['Y', '研发费用', 92-5, 4, 2],
            ['X', '营业费用', 92-5, 4, 2],
            ['X', '销售费用', 92-5, 4, 2],
            ['C', '财务费用', 12-5, 4, 1],
            ['Z', '制造费用', 92-5, 4, 2],
        ]

        self.company_table = [
            #0.company in file  #1.company in sheet
            ['高新', '高新'],
            ['有机硅', '有机硅'],
            ['香港', '香港'],
            ['九江天祺', '天祺'],
            ['九江天赐', '九江'],
            ['池州天赐', '池州天赐'],
            ['江西创新', '创新中心'],
            ['宜春天赐', '宜春天赐'],
            ['中硝', '中硝'],
            ['中天鸿锂', '中天鸿锂'],
            ['天津', '天津'],
            ['安徽天孚', '安徽天孚'],
            ['宁德', '宁德'],
            ['捷克', '捷克天赐'],
            ['浙江天硕', '浙江天硕'],
        ]

    def __del__(self):
        print('delete %s' % self.__class__.__name__)

    def open_dst_file(self, filename):
        self.writer = pd.ExcelWriter(filename, engine='openpyxl')
        # try to open an existing workbook
        self.writer.book = openpyxl.load_workbook(filename)

        # copy existing sheets
        self.writer.sheets = {ws.title: ws for ws in self.writer.book.worksheets}

    def save_dst_file(self):
        self.writer.save()

    def modify_dst_file(self, dataframe, **to_excel_kwargs):
        dataframe.to_excel(self.writer, **to_excel_kwargs)

    def run(self):
        """
        1. 打开文件夹里待提取的第一个文件
        2. 提取 管理费用(G), 研究开发费用(Y), 销售费用(X), 财务费用(C), 制造费用(Z), 数据
        3. 打开待合并文件， 填入相应位置
        """
        file_path = r'./datas/费用合并底稿/202004'
        filelist = []
        for root, dirs, files in os.walk(file_path, topdown=False):
            for name in files:
                str = os.path.join(root, name)
                if str.endswith('.xlsx') or str.endswith('.xls'):
                    if str.endswith('merge.xlsx') or str.find('~') != -1:
                        continue
                    else:
                        filelist.append(str)
                        # break # just test
        # print(filelist)
        print(len(filelist))

        dst_file = r'./datas/费用合并底稿/202004费用合并（公式）底稿 - 副本.xlsx'
        self.open_dst_file(dst_file)
        print(self.writer.sheets.keys())

        for src_file in filelist:
            print(src_file)
            # 找到对应的公司名称
            for company in self.company_table:
                if company[0] in src_file:
                    print(company)
                    break
            excel_file = pd.ExcelFile(src_file)
            print(excel_file.sheet_names)
            for i, expense in enumerate(self.expense_table):
                # 找到源文件对应的费用名称
                print(expense, end=', ')
                src_sheet = ''
                src_sheet_match = '2020实际' + expense[1]
                for sheet in excel_file.sheet_names:
                    if src_sheet_match in sheet:
                        src_sheet = sheet
                        break
                # if src_sheet != '':
                #     print(src_sheet, end=', ')
                # else:
                #     print('')
                #     continue

                # 找到目标文件对应公司对应的费用名称费用的表格
                dst_sheet = ''
                dst_sheet_match = expense[0]+'-'+company[1]
                for sheet in self.writer.sheets:
                    if dst_sheet_match == sheet:
                        dst_sheet = sheet
                        break

                print(src_sheet, end=', ')
                print(dst_sheet, end=', ')

                if dst_sheet != '' and src_sheet != '':
                    src_df = pd.read_excel(src_file, sheet_name=src_sheet, header=expense[3], index_col=expense[4])
                    print(len(src_df['3月']), end=', ')
                    # print(src_df['3月'])
                    if len(src_df['3月']) <= expense[2]:
                        src_data = src_df['3月']
                    else:
                        src_data = src_df['3月'][:expense[2]]
                    # elif expense[2] == 86:
                    #     src_data = src_df['3月'][:86]
                    # elif expense[2] == 6:
                    #     src_data = src_df['3月'][:6]
                    self.modify_dst_file(src_data, sheet_name=dst_sheet, startcol=6, startrow=5, index=False, header=False)
                print('')
            print('')
            excel_file.close()
        self.save_dst_file()

if __name__ == '__main__':
    starttime = nowTime()
    merge_expense = MergeExpense()
    merge_expense.run()
    print('finish', nowTime()-starttime, 'ms')
