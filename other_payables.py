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
        self.save_path = save_path

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
        # 0. 显示桌面 （1587, 888）
        pyautogui.click(1587, 888, duration=3)
        # 1. 打开Genero Desktop Client 软件（112, 574）
        pyautogui.doubleClick(112, 574, duration=5)
        # 2. 双击用户（624, 350）
        pyautogui.doubleClick(624, 350, duration=2)
        # 3. 输入账号（540, 512）
        pyautogui.click(540, 512, duration=2)
        pyautogui.write('G190513')
        # 4. 输入密码（540, 540）
        pyautogui.click(540, 540, duration=3)
        pyautogui.write('123456')
        # 5. 点击确定（483, 580）
        pyautogui.click(483, 580, duration=2)
        pass

    def select_center(self, center):
        # print(center)
        # 1. 选择账套(营运中心) 点击查询放大镜(1218, 558)
        pyautogui.click(1218, 558, duration=1)
        pyautogui.doubleClick(int(center[1][0]), int(center[1][1]))
        # 2. 点击确定(1150, 200),
        pyautogui.click(1150, 200, duration=1)
        # 3. 点击确定(1200, 460)
        pyautogui.click(1200, 460, duration=1)
        pass

    def input_job(self):
        # 1. 输入作业，cglq307(490, 145)
        pyautogui.click(490, 145, duration=1)
        pyautogui.write('cglq307')
        # 2. 点击确定(760, 170)
        pyautogui.click(760, 170, duration=1)
        pass

    def filter(self):  # 4. 筛选条件(期间(年、月、年、月)， 科目, 点击确定筛选
        # 1. 点击年开始(100, 150)->(130, 150)
        pyautogui.moveTo(100, 150)
        pyautogui.dragTo(130, 150, 0.2, button='left')
        # 2. 输入年开始
        pyautogui.write(self.duration[0])
        # print(self.duration[0], end='.')
        # 3. 点击月开始(220, 150)->(250, 150)
        pyautogui.moveTo(220, 150)
        pyautogui.dragTo(250, 150, 0.2, button='left')
        # 4. 输入月开始
        pyautogui.write(self.duration[1])
        # print(self.duration[1], end=' - ')
        # 5. 点击年结束(100, 180)->(130, 180)
        pyautogui.moveTo(100, 180)
        pyautogui.dragTo(130, 180, 0.2, button='left')
        # 6. 输入年结束
        pyautogui.write(self.duration[2])
        # print(self.duration[2], end='.')
        # 7. 点击月结束(220, 180)->(250, 180)
        pyautogui.moveTo(220, 180)
        pyautogui.dragTo(250, 180, 0.2, button='left')
        # 8. 输入月结束
        pyautogui.write(self.duration[3])
        # print(self.duration[3], end='  ')
        # 9. 点击科目(30, 240)
        pyautogui.click(30, 240)
        # 10. 输入科目编号（1221*，2241*）
        pyautogui.write(self.subject)
        # print(self.subject)
        # 11. 点击确定(1500, 115)
        pyautogui.click(1500, 115, duration=8)
        pass

    def export(self, center):
        # 1. 点击汇出execl(330, 75)
        pyautogui.click(330, 75, duration=2)
        # 2. 修改保存路径(905, 418)->(648, 418)
        pyautogui.moveTo(905, 418)
        pyautogui.dragTo(648, 418, 0.2, button='left')

        # 3. 新建营运中心文件夹
        path = os.path.join(self.save_path, 'download')
        if not os.path.exists(path):
            os.makedirs(path)
        path = os.path.join(self.save_path, 'export')
        if not os.path.exists(path):
            os.makedirs(path)

        # 4. 更改文件名(添加 法人主体(营运中心)-默认) (800, 380), ('HOME')
        pyautogui.click(800, 380, duration=1)
        pyautogui.press('HOME')
        pyautogui.write(center[0])
        # print(center[0])
        # 5. 保存(800, 520)
        pyautogui.click(800, 520, duration=1)
        pass

    def reback_center(self, center): # 1. 回到选择账套(营运中心)界面
        # 1. 关闭下载页面 (1133, 216)
        pyautogui.click(1133, 216, duration=1)
        # 2. 最小化网页 (1500, 15)
        pyautogui.click(1500, 15, duration=1)
        # 3. 关闭查询页面 (1580, 8)
        pyautogui.click(1580, 8, duration=1)
        # 4. 点击更改营运中心 (970, 143)
        pyautogui.click(970, 143, duration=1)
        # 5. 点击查询放大镜 (1112, 640)
        pyautogui.click(1112, 640, duration=1)
        # 6. 拖拽下拉页面(1206, 550), 选择营运中心
        pyautogui.moveTo(1206, 550)
        pyautogui.dragTo(1206, 650, 0.2, button='left')
        pyautogui.doubleClick(int(center[1][0]), int(center[1][1]))
        # 7. 点击确定选择营运中心(1150, 200)
        pyautogui.click(1150, 200, duration=1)
        # 8. 点击营运中心确定(1200, 460)
        pyautogui.click(1200, 460, duration=1)
        pass

    def download(self):
        # 1. 打开软件，登入账号
        self.login()
        self.message_singel.emit('开始下载.\r\n')
        input()

        # 2. 选择营运中心
        self.select_center(center)
        input()

        for center in self.centers.items():
            # print(center[0])
            self.message_singel.emit('正在下载%s...\r\n' % center[0])
            # 3. 输入作业，cglq307, 点击确定
            self.input_job()
            input()
            # 4. 点击查询，筛选条件(期间(年、月、年、月)， 科目, 点击确定筛选
            self.filter()
            input()
            # 5. 导出/汇出excel
            # 6. 新建营运中心文件夹，保存、更改文件名(添加 法人主体(营运中心)-默认)
            self.export(center)
            input()
            # 7. 回到选择账套(营运中心)界面
            self.reback_center(center)
            input()

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

