# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/03/26
# @Author  : 陈志鹏
# @File    : other_payables.py

import os
import sys
import logging
import pyautogui
import xml.sax
import pandas as pd
import financial_ui as ui
from PySide2.QtWidgets import *
from PySide2.QtCore import *

# logging.basicConfig(level=logging.DEBUG,
#         filename='out.log',
#         datefmt='%Y/%m/%d %H:%M:%S',
# format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s
# - %(message)s')


class ExcelHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.chars = []
        self.cells = []
        self.rows = []
        self.tables = []

    def characters(self, content):
        self.chars.append(content)

    def startElement(self, name, atts):
        if name == "Cell":
            self.chars = []
        elif name == "Row":
            self.cells = []
        elif name == "Table":
            self.rows = []

    def endElement(self, name):
        if name == "Cell":
            self.cells.append(''.join(self.chars))
        elif name == "Row":
            self.rows.append(self.cells)
        elif name == "Table":
            self.tables.append(self.rows)




class WorkerGetOtherPayables(QThread):
    def __init__(self, ui):
        pass

    def login(self):
        # 1. 打开任务栏软件
        # 2. 双击用户
        # 3. 输入账号
        # 4. 输入密码
        # 5. 点击确定
        pass

    def select_center(self):
        # 1. 选择营运中心
        # 2. 点击确定
        pass

    def filter(self):
        # 1. 点击年开始
        # 2. 输入年开始
        # 3. 点击月开始
        # 4. 输入月开始
        # 5. 点击年结束
        # 6. 输入年结束
        # 7. 点击月结束
        # 8. 输入月结束
        # 9. 点击科目
        # 10. 输入科目
        pass

    def export(self):
        pass

    def rename(self):
        pass

    def get(self):
        # 1. 打开软件，登入账号
        self.login()
        # 2. 选择营运中心
        self.select_center()
        # 3. 筛选条件（期间（年、月、年、月）， 科目（两次））
        # 4. 点击确定筛选
        self.filter()
        # 5. 导出/汇出excel
        self.export()
        # 6. 保存
        # 7. 更改文件名(添加 法人主体(营运中心)-默认)
        self.rename()
        # 7. 最后一列添加‘法人主体’， 已经在合并里面实现
        pass


class WorkerOtherPayables(QObject):
    message_singel = Signal(str)
    finish_singel = Signal()
    statusBar_singel = Signal(str)

    def __init__(self):
        super(WorkerOtherPayables, self).__init__()

    def __del__(self):
        print('delete WorkerOtherPayables')

    def merge_files(self, file_path, dst_name):
        filelist = []

        for root, dirs, files in os.walk(file_path, topdown=False):
            for name in files:
                str = os.path.join(root, name)
                if str.split('.')[-1] == 'xls':
                    filelist.append(str)
        print(filelist)

        dfs = []
        for file in filelist:
            file_name = os.path.basename(file)
            # print(file_name.split('-')[0])
            excelHandler = ExcelHandler()
            xml.sax.parse(file, excelHandler)  # 文件名
            df = pd.DataFrame(
                excelHandler.tables[0][1:], columns=excelHandler.tables[0][0])
            df['法人主体'] = file_name.split('-')[0]
            dfs.append(df)

        # 将多个DataFrame合并为一个
        df = pd.concat(dfs)
        print(df.head(), df.shape)
        df.to_excel(r'%s/%s.xlsx' % (file_path, dst_name), index=False)

    def merge(self):
        # self.message_singel.emit('start merge_inner_order...\r\n')
        self.statusBar_singel.emit('开始合并...')
        file_path = os.path.join(os.getcwd(), 'original_data/merge_datas')
        # file_path = "D:/CZP/python/FinancialTools/original_data/merge_datas"
        self.merge_files(file_path, 'merge')
        # self.message_singel.emit('merge_inner_order ok!\r\n')
        self.statusBar_singel.emit('合并完成。')
        self.finish_singel.emit()


if __name__ == '__main__':
    worker_other_payables = WorkerOtherPayables()
    worker_other_payables.merge()

