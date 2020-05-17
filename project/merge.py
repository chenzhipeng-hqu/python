# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/03/26
# @Author  : 陈志鹏
# @File    : other_payables.py

"""
合并一个文件夹下的所有excel文件，并添加月份一列
"""

import os
import xlrd
from project import log
import pandas as pd
from PySide2.QtCore import *

# logging.basicConfig(level=logging.DEBUG,  filename='out.log',
#                     datefmt='%Y/%m/%d %H:%M:%S',
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')
#
# logger = logging.getLogger(__name__)

logger = log.Log(__name__).getlog()

class WorkerMerge(QObject):
    #message_singel = Signal(str)
    finish_singel = Signal()
    statusBar_singel = Signal(str)

    def __init__(self):
        super(WorkerMerge, self).__init__()
        logger.info(" ")

    def __del__(self):
        print('delete %s' % self.__class__.__name__)

    def merge(self, src_path, dst_name):
        file_path = os.path.join(src_path)
        dst_name = os.path.join(src_path, dst_name)
        print(file_path)
        print(dst_name)
        filelist = []

        for root, dirs, files in os.walk(file_path, topdown=False):
            for name in files:
                str = os.path.join(root, name)
                if str.split('.')[-1] == 'xlsx' or str.split('.')[-1] == 'xls':
                    if os.path.basename(str) != 'merge.xlsx':
                        filelist.append(str)
        print(filelist)

        dfs = []
        for file in filelist:
            file_name = os.path.basename(file)
            # print(file_name.split('-')[0])
            workbook = xlrd.open_workbook(file)
            worksheets = workbook.sheet_names()
            # month = os.path.splitext(file_name)[0].split('-')[0]
            for sheet in worksheets:
                df = pd.read_excel(file, sheet_name=sheet)
                df['文件'] = file_name
                df['sheet'] = sheet
                dfs.append(df)

        if dfs:
            # 将多个DataFrame合并为一个
            df = pd.concat(dfs)
            # print(df.head(), df.shape)
            # df.to_excel(r'%s/%s.xlsx' % (file_path, dst_name), index=False)
            df.to_excel(dst_name, index=False)
            self.statusBar_singel.emit('合并完成')
        else:
            self.statusBar_singel.emit('未发现合并需要的文件.\r\n')


if __name__ == '__main__':
    worker_merge = WorkerMerge()
    worker_merge.merge('D:\CZP\python\FinancialTools\datas\merge', 'merge.xlsx')