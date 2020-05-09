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

def append_df_to_excel(filename, df, sheet_name='Sheet1', startrow=None,
                       truncate_sheet=False,
                       **to_excel_kwargs):
    """
    Append a DataFrame [df] to existing Excel file [filename]
    into [sheet_name] Sheet.
    If [filename] doesn't exist, then this function will create it.
    Parameters:
      filename : File path or existing ExcelWriter
                 (Example: '/path/to/file.xlsx')
      df : dataframe to save to workbook
      sheet_name : Name of sheet which will contain DataFrame.
                   (default: 'Sheet1')
      startrow : upper left cell row to dump data frame.
                 Per default (startrow=None) calculate the last row
                 in the existing DF and write to the next row...
      truncate_sheet : truncate (remove and recreate) [sheet_name]
                       before writing DataFrame to Excel file
      to_excel_kwargs : arguments which will be passed to `DataFrame.to_excel()`
                        [can be dictionary]
    Returns: None
    """
    # from openpyxl import load_workbook

    # import pandas as pd

    # ignore [engine] parameter if it was passed
    starttime = nowTime()
    if 'engine' in to_excel_kwargs:
        to_excel_kwargs.pop('engine')

    starttime = nowTime()
    writer = pd.ExcelWriter(filename, engine='openpyxl')
    print('pd.ExcelWriter: ', nowTime()-starttime)

    # Python 2.x: define [FileNotFoundError] exception if it doesn't exist
    try:
        FileNotFoundError
    except NameError:
        FileNotFoundError = IOError

    try:
        # try to open an existing workbook
        starttime = nowTime()
        writer.book = openpyxl.load_workbook(filename)
        print('openpyxl.load_workbook: ', nowTime()-starttime)

        # get the last row in the existing Excel sheet
        # if it was not specified explicitly
        if startrow is None and sheet_name in writer.book.sheetnames:
            startrow = writer.book[sheet_name].max_row

        # truncate sheet
        if truncate_sheet and sheet_name in writer.book.sheetnames:
            # index of [sheet_name] sheet
            idx = writer.book.sheetnames.index(sheet_name)
            # remove [sheet_name]
            writer.book.remove(writer.book.worksheets[idx])
            # create an empty sheet [sheet_name] using old index
            writer.book.create_sheet(sheet_name, idx)

        starttime = nowTime()
        # copy existing sheets
        writer.sheets = {ws.title: ws for ws in writer.book.worksheets}
        print('writer.sheets: ', nowTime()-starttime)
    except FileNotFoundError:
        # file does not exist yet, we will create it
        pass

    if startrow is None:
        startrow = 0

    starttime = nowTime()
    # write out the new sheet
    df.to_excel(writer, sheet_name, startrow=startrow, **to_excel_kwargs)
    print('df.to_excel: ', nowTime()-starttime)

    # save the workbook
    starttime = nowTime()
    writer.save()
    print('writer.save: ', nowTime()-starttime)
    starttime = nowTime()
    writer.close()
    print('writer.close: ', nowTime()-starttime)

class MergeExpense(QObject):
    #message_singel = Signal(str)
    finish_singel = Signal()
    statusBar_singel = Signal(str)

    def __init__(self):
        super(MergeExpense, self).__init__()
        self.expense_table = [
            #0.identification   1.expense 2.max_row
            ['G', '管理费用', 98-5],
            ['Y', '研发费用', 98-5],
            ['X', '营业费用', 103-5],
            ['C', '财务费用', 13-5],
            ['Z', '制造费用', 97-5],
        ]

        self.company_table = [
            #0.company in file  #1.company in sheet
            ['池州天赐', '池州天赐'],
            ['江西创新', '江西创新'],
            ['宜春天赐', '宜春天赐'],
            ['中硝', '中硝'],
            ['中天鸿锂', '中天鸿锂'],
            ['天津', '天津'],
            ['安徽天孚', '安徽天孚'],
            ['九江天祺', '九江天祺'],
            ['宁德', '宁德'],
            ['九江天赐', '九江'],
            ['香港', '香港'],
            ['高新', '高新'],
            ['有机硅', '有机硅'],
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
        file_path = r'./datas/费用合并底稿/202003'
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

        dst_file = r'./datas/费用合并底稿/123.xlsx'
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
                if src_sheet != '':
                    print(src_sheet, end=', ')
                # else:
                #     print('')
                #     continue

                # 找到目标文件对应公司对应的费用名称费用的表格
                dst_sheet = ''
                dst_sheet_match = expense[0]+'-'+company[1]
                for sheet in self.writer.sheets:
                    if dst_sheet_match in sheet:
                        dst_sheet = sheet
                        break

                if dst_sheet != '' and src_sheet != '':
                    # print(src_sheet, end=', ')
                    print(dst_sheet, end=', ')
                    src_df = pd.read_excel(src_file, sheet_name=src_sheet, header=4, index_col=2)
                    print(len(src_df['3月']))
                    if len(src_df['3月']) <= expense[2]:
                        src_data = src_df['3月']
                    else:
                        src_data = src_df['3月'][:expense[2]]
                    self.modify_dst_file(src_data, sheet_name=dst_sheet, startcol=6, startrow=5, index=False, header=False)

                print('')

                pass
            print('')
            excel_file.close()

        # src_file = r'./datas/费用合并底稿/202003/202003安徽天孚报表-费用.xlsx'
        # src_sheet = r'2020实际制造费用安徽天孚'
        # src_df = pd.read_excel(src_file, sheet_name=src_sheet, header=4, index_col=2)
        # print(src_df.head())
        # src_data = src_df['3月'][:92]
        #
        # self.modify_dst_file(src_data, sheet_name=dst_sheet, startcol=6, startrow=5, index=False, header=False)
        #
        self.save_dst_file()

if __name__ == '__main__':
    starttime = nowTime()
    merge_expense = MergeExpense()
    merge_expense.run()
    print('finish', nowTime()-starttime, 'ms')
