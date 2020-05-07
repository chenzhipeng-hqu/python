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
    if 'engine' in to_excel_kwargs:
        to_excel_kwargs.pop('engine')

    writer = pd.ExcelWriter(filename, engine='openpyxl')

    # Python 2.x: define [FileNotFoundError] exception if it doesn't exist
    try:
        FileNotFoundError
    except NameError:
        FileNotFoundError = IOError

    try:
        # try to open an existing workbook
        writer.book = openpyxl.load_workbook(filename)

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

        # copy existing sheets
        writer.sheets = {ws.title: ws for ws in writer.book.worksheets}
    except FileNotFoundError:
        # file does not exist yet, we will create it
        pass

    if startrow is None:
        startrow = 0

    # write out the new sheet
    df.to_excel(writer, sheet_name, startrow=startrow, **to_excel_kwargs)

    # save the workbook
    writer.save()

class MergeExpense(QObject):
    #message_singel = Signal(str)
    finish_singel = Signal()
    statusBar_singel = Signal(str)

    def __init__(self):
        super(MergeExpense, self).__init__()

    def __del__(self):
        print('delete %s' % self.__class__.__name__)

    def run(self):
        """
        1. 打开文件夹里待提取的第一个文件
        2. 提取 制造费用 数据
        3. 打开待合并文件， 填入相应位置
        """
        # file_path = r'D:\CZP\python\FinancialTools\datas\费用合并底稿\202003'
        # filelist = []
        # for root, dirs, files in os.walk(file_path, topdown=False):
        #     for name in files:
        #         str = os.path.join(root, name)
        #         if str.split('.')[-1] == 'xlsx' or str.split('.')[-1] == 'xls':
        #             if os.path.basename(str) != 'merge.xlsx':
        #                 filelist.append(str)
        # # print(filelist)
        # print(len(filelist))

        src_file = r'D:\CZP\python\FinancialTools\datas\费用合并底稿\202003\202003安徽天孚报表-费用.xlsx'
        src_sheet = r'2020实际制造费用安徽天孚'
        # f = pd.ExcelFile(src_file)
        # print(f.sheet_names)

        # src_df = pd.read_excel(f, sheet_name=src_sheet, header=4, index_col=2)
        src_df = pd.read_excel(src_file, sheet_name=src_sheet, header=4, index_col=2)
        # print(df.head())
        # print(src_df['3月'])
        dst_file = r'.\datas\费用合并底稿\123.xlsx'
        dst_sheet = r'Z-安徽天孚'
        # writer = pd.ExcelWriter(dst_file, engine='openpyxl')
        # writer.book = openpyxl.load_workbook(dst_file)
        # dst_df = pd.read_excel(writer, sheet_name=dst_sheet, header=4, index_col=2)
        # dst_df = pd.read_excel(dst_file, sheet_name=dst_sheet)
        print(src_df.head())
        # print(src_df.index)
        src_data = src_df['3月'][:92]
        # print(src_df['2020年3月'])
        print(src_data)
        append_df_to_excel(dst_file, src_data, sheet_name=dst_sheet, startcol=6, startrow=5, index=False, header=False)
        # for i, data in enumerate(src_df['3月']):
        #     print(data)
        #     dst_df['2020年4月'].at[i] = data
        # # dst_df['2020年4月'][:99] = src_df['3月'][:99]
        # print(dst_df['2020年4月'])
        # # dst_df.to_excel(r".\datas\费用合并底稿\123.xlsx", index=False)
        # dst_df.to_excel(writer, index=False)

if __name__ == '__main__':
    merge_expense = MergeExpense()
    merge_expense.run()
    print('finish')
