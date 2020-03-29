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
        # self.center_list = []
        # 加载现有配置文件
        # conf = configparser.ConfigParser()
        # path = os.path.join(os.getcwd(), 'configure.ini')
        # conf.read(path, encoding="utf-8-sig")
        # # self.sections = conf.sections()
        # # centers = conf.get("center", 'centers')
        # # print(centers)
        # # self.center_list = centers.split(',')
        # # print('center_list:', self.center_list)
        #
        # center = conf.items("center")
        # # center_list = [position[0] for position in center]
        # # position_list = [position[1].split(',') for position in center]
        # self.centers = {position[0]: position[1].split(',') for position in center}
        # # self.centers = dict(zip(center_list, position_list))
        # print(self.centers)

    def __del__(self):
        print('delete WorkerOtherPayables')

    def set_parameter(self, centers, duration, subject, save_path):
        self.centers = centers
        self.duration = duration
        self.subject = subject
        self.save_path = os.path.join(save_path, subject)

    def merge(self):
        file_path = os.path.join(self.save_path, 'download')
        dst_name = os.path.join(self.save_path, 'export/%s-%s%s-%s%s.xlsx' % (self.subject, self.duration[0], self.duration[1].zfill(2), self.duration[2], self.duration[3].zfill(2)))

        filelist = []

        for root, dirs, files in os.walk(file_path, topdown=False):
            for name in files:
                str = os.path.join(root, name)
                if str.split('.')[-1] == 'xls':
                    filelist.append(str)
        # print(filelist)

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

        if dfs:
            # 将多个DataFrame合并为一个
            df = pd.concat(dfs)
            # print(df.head(), df.shape)
            # df.to_excel(r'%s/%s.xlsx' % (file_path, dst_name), index=False)
            df.to_excel(dst_name, index=False)
        else:
            self.message_singel.emit('未发现合并需要的文件.\r\n')

    def login(self):
        # 1. 打开任务栏软件
        pyautogui.moveTo(100, 200)
        # 2. 双击用户
        # 3. 输入账号
        # 4. 输入密码
        # 5. 点击确定
        pass

    def select_center(self, center):
        # 1. 选择账套(营运中心)
        # print(center)
        pyautogui.moveTo(int(center[1][0]), int(center[1][1]))
        # 2. 点击确定
        pass

    def input_job(self):
        # 1. 输入作业，cglq307
        pyautogui.moveTo(700, 200)
        # 2. 点击确定
        pass

    def filter(self):  # 4. 点击查询，筛选条件(期间(年、月、年、月)， 科目, 点击确定筛选
        # 1. 点击年开始
        # 2. 输入年开始
        # print(self.duration[0], end='.')
        # 3. 点击月开始
        # 4. 输入月开始
        # print(self.duration[1], end=' - ')
        # 5. 点击年结束
        # 6. 输入年结束
        # print(self.duration[2], end='.')
        # 7. 点击月结束
        # 8. 输入月结束
        # print(self.duration[3], end='  ')
        # 9. 点击科目
        # 10. 输入科目
        # print(self.subject)
        # 11. 点击确定
        pass

    def export(self, center):
        # 1. 点击汇出execl
        # 2. 点击保存

        # 3. 新建营运中心文件夹
        path = os.path.join(self.save_path, 'download')
        if not os.path.exists(path):
            os.makedirs(path)
        path = os.path.join(self.save_path, 'export')
        if not os.path.exists(path):
            os.makedirs(path)

        # 4. 保存、更改文件名(添加 法人主体(营运中心)-默认)
        # print(center[0])
        pass

    def reback_center(self):
        # 1. 回到选择账套(营运中心)界面
        pass

    def download(self):
        # 1. 打开软件，登入账号
        self.login()
        self.message_singel.emit('开始下载.\r\n')

        for center in self.centers.items():
            # print(center[0])
            self.message_singel.emit('正在下载%s...\r\n' % center[0])
            # 2. 选择营运中心
            self.select_center(center)
            # 3. 输入作业，cglq307, 点击确定
            self.input_job()
            # 4. 点击查询，筛选条件(期间(年、月、年、月)， 科目, 点击确定筛选
            self.filter()
            # 5. 导出/汇出excel
            # 6. 新建营运中心文件夹，保存、更改文件名(添加 法人主体(营运中心)-默认)
            self.export(center)
            # 7. 回到选择账套(营运中心)界面
            self.reback_center()

        # 8. 最后一列添加‘法人主体’， 合并文件名为‘科目-期间’
        self.merge()
        # print('download finished')
        self.message_singel.emit('下载完成.\r\n')
        self.finish_singel.emit()
        pass


if __name__ == '__main__':
    worker_other_payables = WorkerOtherPayables()

    # 加载现有配置文件
    conf = configparser.ConfigParser()
    path = os.path.join(os.getcwd(), 'configure.ini')
    conf.read(path, encoding="utf-8-sig")
    center = conf.items("center")
    centers = {position[0]: position[1].split(',') for position in center}
    print(centers)
    duration = []
    subject = ''
    save_path = ''
    worker_other_payables.set_parameter(centers, duration, subject, save_path)
    worker_other_payables.download()

