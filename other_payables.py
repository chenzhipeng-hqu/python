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
import configparser
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


class WorkerOtherPayables(QObject):
    message_singel = Signal(str)
    finish_singel = Signal()
    statusBar_singel = Signal(str)

    def __init__(self):
        super(WorkerOtherPayables, self).__init__()
        self.center_list = []
        # 加载现有配置文件
        conf = configparser.ConfigParser()
        path = os.path.join(os.getcwd(), 'configure.ini')
        conf.read(path, encoding="utf-8-sig")
        # self.sections = conf.sections()
        self.center_list = conf.get("center", 'centers').split(',')
        # print('center_list:', self.center_list)

    def __del__(self):
        print('delete WorkerOtherPayables')

    def merge(self):

        file_path = os.path.join(os.getcwd(), 'original_data/merge_datas')
        dst_name = 'merge'

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

    def login(self):
        # 1. 打开任务栏软件
        pyautogui.moveTo(100, 200)
        # 2. 双击用户
        pyautogui.moveTo(200, 200)
        # 3. 输入账号
        pyautogui.moveTo(300, 200)
        # 4. 输入密码
        pyautogui.moveTo(400, 200)
        # 5. 点击确定
        pyautogui.moveTo(500, 200)
        pass

    def select_center(self):
        # 1. 选择营运中心
        pyautogui.moveTo(500, 200)
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
        # 11. 点击确定
        pass

    def export(self):
        # 1. 点击汇出execl
        # 2. 点击保存
        pass

    def rename(self):
        # 1. 点击
        pass

    def reback_center(self):
        # 1. 点击
        pass

    def download(self):
        # self.message_singel.emit('start merge_inner_order...\r\n')
        self.statusBar_singel.emit('开始下载...')
        # 1. 打开软件，登入账号
        self.login()

        for center in self.center_list:
            # 2. 选择营运中心
            self.select_center()
            # 3. 筛选条件（期间（年、月、年、月）， 科目（两次））
            # 4. 点击确定筛选
            self.filter()
            # 5. 导出/汇出excel
            self.export()
            # 6. 保存、更改文件名(添加 法人主体(营运中心)-默认)
            self.rename()
            # 7. 回到选择营运中心界面
            self.reback_center()

        # 8. 最后一列添加‘法人主体’， 已经在合并里面实现
        # self.merge()
        self.statusBar_singel.emit('下载完成。')
        self.finish_singel.emit()
        pass


if __name__ == '__main__':
    worker_other_payables = WorkerOtherPayables()
    worker_other_payables.download()

