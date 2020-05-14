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
            #0.identification, 1.expense, 2.copy_row, 3.read_row, 4.read_col, 5.other_cnt
            # ['G', '管理费用', 92-5, 4, [0, 1, 2]],
            # ['Y', '研发费用', 92-5, 4, [0, 1, 2]],
            # ['X', '营业费用', 92-5, 4, [0, 1, 2]],
            # ['X', '销售费用', 92-5, 4, [0, 1, 2]],
            # ['C', '财务费用', 12-5, 4, [0, 1]],
            # ['Z', '制造费用', 92-5, 4, [0, 1, 2]],
            ['G', '管理费用', 92-5, 4, [2], 5],
            ['Y', '研发费用', 92-5, 4, [2], 3],
            ['X', '营业费用', 92-5, 4, [2], 10],
            ['X', '销售费用', 92-5, 4, [2], 10],
            ['C', '财务费用', 12-5, 4, [1], 0],
            ['Z', '制造费用', 92-5, 4, [2], 4],
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

    def set_param(self, *args, ** kwargs):
        self.month = kwargs.get('month')
        self.file_path = kwargs.get('file_path')
        self.dst_file = kwargs.get('dst_file')

    def open_dst_file(self):
        self.writer = pd.ExcelWriter(self.dst_file, engine='openpyxl')
        # try to open an existing workbook
        self.writer.book = openpyxl.load_workbook(self.dst_file)

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
        filelist = []
        for root, dirs, files in os.walk(self.file_path, topdown=False):
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

        self.open_dst_file()
        print(self.writer.sheets.keys())

        wsheet = self.writer.book['目录']
        for i, sheet in enumerate(self.writer.sheets.keys()):
            link = r'{}#{}{}{}!E1'.format(os.path.basename(self.dst_file), "'", sheet, "'")
            wsheet.cell(row=i+1, column=1, value=sheet).hyperlink = link

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
                    src_month_col = list(src_df.columns.values).index(self.month)
                    print(src_month_col, end=', ')

                    if len(src_df['3月']) <= expense[2]:
                        src_data = src_df['3月']
                        print('11111111111111111111111111111111111111111111111111111111111')
                    else:
                        src_data = src_df['3月'][:expense[2]]

                        if expense[1] == '财务费用':
                            pass
                        else:
                            if company[1] == '天津' and expense[1] == '营业费用':
                                src_data_other = src_df['3月'][expense[2] + 1:expense[2] + 1 + 6]
                                src_data_other2 = src_df['3月'][expense[2] + 1 + 8:expense[2] + 1 + 12]
                                src_data_other = pd.concat([src_data_other, src_data_other2])
                                src_data_other.astype(dtype='float64')
                            else:
                                src_data_other = src_df['3月'][expense[2] + 1:expense[2] + 1 + expense[5]]
                                src_data_other.astype(dtype='float64')

                            self.modify_dst_file(src_data_other, sheet_name=dst_sheet, startcol=src_month_col-2, startrow=expense[2]+6, index=False, header=False)

                    src_data.astype(dtype='float64')
                    self.modify_dst_file(src_data, sheet_name=dst_sheet, startcol=src_month_col-2, startrow=expense[3]+1, index=False, header=False)
                print('')
            print('')
            excel_file.close()
        self.save_dst_file()

if __name__ == '__main__':
    starttime = nowTime()
    merge_expense = MergeExpense()
    merge_expense.set_param(month='3月', file_path=r'./datas/费用合并底稿/202004', dst_file=r'./datas/费用合并底稿/202004费用合并（公式）底稿(副本).xlsx')
    merge_expense.run()
    print('finish', nowTime()-starttime, 'ms')
