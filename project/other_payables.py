# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/03/26
# @Author  : 陈志鹏
# @File    : other_payables.py

import os
import time
import pyautogui
import pyperclip
import xml.sax
import configparser
import pandas as pd
from PySide2.QtCore import *


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
    #message_singel = Signal(str)
    finish_singel = Signal()
    statusBar_singel = Signal(str)

    def __init__(self):
        super(WorkerOtherPayables, self).__init__()
        pyautogui.PAUSE = 0.5

    def __del__(self):
        print('delete WorkerOtherPayables')

    # def set_parameter(self, centers, duration, job, subjects, save_path):
    def set_parameter(self, *args, ** kwargs):
        self.centers = kwargs.get('centers')
        print(self.centers)
        self.duration = kwargs.get('duration')
        print(self.duration)
        self.job = kwargs.get('job')
        print(self.job)
        self.subjects = kwargs.get('subjects')
        print(self.subjects)
        self.save_path = kwargs.get('save_path')
        print(self.save_path)

    def wait_pic(self, pic, *args, ** kwargs):
        pci_location = None
        while (pci_location == None):
            pci_location = pyautogui.locateCenterOnScreen(
                    pic, region=(0, 0, 1000, 800))
            #pci_location = pyautogui.locateOnScreen(
            #        pic, confidence=0.9, region=(0, 0, 1000, 800))
            #print(pci_location)
            if pci_location:
                break
            else:
                tip = kwargs.get('tip')
                if tip == False:
                    pass
                else:
                    pyautogui.alert(text=r'未找到'+str(pic)+'的坐标', title='未找到坐标', button='OK')
                time.sleep(0.5)

        return pci_location

    def merge(self):
        file_path = os.path.join(self.save_path, 'download')
        dst_name = os.path.join(self.save_path, 'export')
        dst_name = os.path.join(dst_name, '%s-%s%s-%s%s.xlsx' % (self.job, self.duration[0], self.duration[1].zfill(2), self.duration[2], self.duration[3].zfill(2)))
        print(file_path)
        print(dst_name)
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

        if dfs:
            # 将多个DataFrame合并为一个
            df = pd.concat(dfs)
            # print(df.head(), df.shape)
            # df.to_excel(r'%s/%s.xlsx' % (file_path, dst_name), index=False)
            df.to_excel(dst_name, index=False)
        else:
            self.statusBar_singel.emit('未发现合并需要的文件.\r\n')

    def login(self):
        # 0. 显示桌面 （1587, 888）
        #pyautogui.moveTo(1592, 880)
        #pyautogui.click()
        #pyautogui.hotkey('win', 'd')
        #print('显示桌面')
        #time.sleep(1)
        # 1. 打开Genero Desktop Client 软件（112, 574）
        #pyautogui.moveTo(112, 574)
        #pyautogui.doubleClick(duration=1)
        os.system(r'"C:\Program Files\FourJs\gdc\bin\gdc.exe" -Da')
        time.sleep(0.5)
        #print('打开软件')
        # 查看软件是否打开
        position = self.wait_pic('datas/picture/GeneroDeskTop.png')
        # 2. 双击用户（624, 350）
        pyautogui.moveTo(position[0], position[1])
        pyautogui.doubleClick()
        # 3. 输入账号（540, 512）
        time.sleep(0.5)
        #pyautogui.moveTo(540, 512)
        #pyautogui.click()
        pyautogui.write('G190513')
        # 4. 输入密码（540, 540）
        #pyautogui.moveTo(540, 540)
        #pyautogui.click()
        pyautogui.press('tab')
        pyautogui.write('123456')
        # 5. 点击确定（483, 580）
        # pyautogui.moveTo(483, 580)
        # pyautogui.click(duration=1)
        pyautogui.press('ENTER')
        #time.sleep(1)
        pass

    def select_center(self, center):
        # 查看软件是否打开
        #self.wait_pic('datas/picture/select_center.png', tip=False)
        time.sleep(1)
        # print(center)
        # # 1. 选择账套(营运中心) 点击查询放大镜(1218, 558)
        # pyautogui.click(1218, 558, duration=1)
        # pyautogui.doubleClick(int(center[1][0]), int(center[1][1]))
        # # 2. 点击确定(1150, 200),
        # pyautogui.click(1150, 200, duration=1)
        # # 3. 点击确定(1200, 460)
        # pyautogui.click(1200, 460, duration=1)

        # 1. 选中营运中心输入框 (1080, 635)->(920, 635)
        #pyautogui.moveTo(1080, 635)
        #pyautogui.dragTo(920, 635, 0.2, button='left')
        # 2. 输入营运中心
        pyautogui.write(center)
        time.sleep(0.5)
        # 3. 点击确定(1200, 460)
        pyautogui.press('ENTER')
        # pyautogui.moveTo(1200, 460)
        # pyautogui.click(duration=1)
        pass

    def input_job(self):
        # 查看是否找到输入作业页面
        #self.wait_pic('datas/picture/input_job.png')
        # 1. 输入作业，cglq307(490, 145)
        pyautogui.moveTo(490, 145)
        pyautogui.click()
        pyautogui.write(self.job)
        # 2. 点击确定(760, 170)
        #pyautogui.moveTo(760, 170)
        #pyautogui.click()
        pyautogui.press('ENTER')
        pass

    def filter_duration(self):  # 4. 筛选条件(期间(年、月、年、月)， 科目, 点击确定筛选
        # 1. 点击年开始(100, 150)->(130, 150)
        #pyautogui.moveTo(100, 155)
        #pyautogui.click(duration=1)
        #pyautogui.hotkey('ctrl', 'a')
        time.sleep(1)
        pyautogui.press('tab')
        # pyautogui.moveTo(100, 150)
        # pyautogui.dragTo(130, 150, 0.2, button='left')
        # 2. 输入年开始
        pyautogui.write(self.duration[0])
        # print(self.duration[0], end='.')
        # 3. 点击月开始(220, 150)->(250, 150)
        #pyautogui.moveTo(220, 155)
        #pyautogui.click(duration=0.1)
        #pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('tab')
        # pyautogui.dragTo(250, 150, 0.2, button='left')
        # 4. 输入月开始
        pyautogui.write(self.duration[1])
        # print(self.duration[1], end=' - ')
        # 5. 点击年结束(100, 180)->(130, 180)
        #pyautogui.moveTo(100, 180)
        #pyautogui.click(duration=0.1)
        #pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('tab')
        # pyautogui.dragTo(130, 180, 0.2, button='left')
        # 6. 输入年结束
        pyautogui.write(self.duration[2])
        # print(self.duration[2], end='.')
        # 7. 点击月结束(220, 180)->(250, 180)
        #pyautogui.moveTo(220, 180)
        #pyautogui.click(duration=0.1)
        #pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('tab')
        # pyautogui.dragTo(250, 180, 0.2, button='left')
        # 8. 输入月结束
        pyautogui.write(self.duration[3])
        # print(self.duration[3], end='  ')

    def filter_subject(self, subject):  # 4. 筛选条件(期间(年、月、年、月)， 科目, 点击确定筛选
        # 9. 点击科目(30, 240)
        pyautogui.moveTo(30, 240)
        pyautogui.click(duration=0.5)
        # 10. 输入科目编号（1221*，2241*）
        pyautogui.write(subject)
        print(subject)
        # 11. 点击确定(1500, 115)
        pyautogui.hotkey('ctrl', 'enter')
        # pyautogui.moveTo(1500, 115)
        # pyautogui.click(duration=8)
        # time.sleep(16)
        # 查看是否查询完成
        self.wait_pic('datas/picture/export.png', tip=False)
        pass

    def export(self, center):
        # 1. 点击汇出execl(330, 75)
        pyautogui.moveTo(330, 75)
        pyautogui.click(duration=1)
        #time.sleep(1)
        # 查看是否打开下载页面
        self.wait_pic('datas/picture/download.png', tip=False)
        # 2. 更改文件名(添加 法人主体(营运中心)-默认) (800, 380), ('home')
        pyperclip.copy(str(center[0]))
        pyautogui.moveTo(800, 380)
        pyautogui.click()
        pyautogui.press('home')
        #time.sleep(1)
        # pyperclip.paste()
        pyautogui.hotkey('ctrl', 'v')
        # pyautogui.write(str(center[0]))
        pyautogui.write('-')

        # 3. 修改保存路径(905, 418)->(648, 418)
        # pyautogui.moveTo(905, 418)
        # pyautogui.dragTo(648, 418, 0.2, button='left')
        #pyautogui.moveTo(905, 418)
        #pyautogui.click(duration=1)
        #pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('tab')

        # 4. 新建营运中心文件夹
        path = os.path.join(self.save_path, 'download')
        pyautogui.write(path)
        time.sleep(0.5)
        if not os.path.exists(path):
            os.makedirs(path)

        path = os.path.join(self.save_path, 'export')
        if not os.path.exists(path):
            os.makedirs(path)
        # logger.debug(type(center[0]), center[0])
        # print(center[0])
        # 5. 保存(800, 520)
        #pyautogui.moveTo(800, 520)
        #pyautogui.click(duration=1)
        pyautogui.press('enter')
        pass

    def reback_filter(self): # 1. 回到过滤页面
        # 1. 关闭下载页面 (1133, 216)
        pyautogui.moveTo(1133, 216)
        pyautogui.click(duration=1)
        # 2. 最小化网页 (1500, 15)
        pyautogui.moveTo(1500, 15)
        pyautogui.click(duration=1)

    def click_query(self):
        # 3. 点击查询按钮 (408, 63)
        pyautogui.moveTo(408, 63)
        pyautogui.click(duration=1)

    def reback_center(self): # 1. 回到选择账套(营运中心)界面
        # 1. 关闭查询页面 (1580, 8)
        pyautogui.moveTo(1580, 8)
        pyautogui.click(duration=1)
        # 2. 点击更改营运中心 (970, 143)
        pyautogui.moveTo(970, 143)
        pyautogui.click(duration=1)

        # # 5. 点击查询放大镜 (1112, 640)
        # pyautogui.click(1112, 640, duration=1)
        # # 6. 拖拽下拉页面(1206, 550), 选择营运中心
        # pyautogui.moveTo(1206, 550)
        # pyautogui.dragTo(1206, 650, 0.2, button='left')
        # pyautogui.doubleClick(int(center[1][0]), int(center[1][1]))
        # # 7. 点击确定选择营运中心(1150, 200)
        # pyautogui.click(1150, 200, duration=1)
        # # 8. 点击营运中心确定(1200, 460)
        # pyautogui.click(1200, 460, duration=1)
        pass

    def download(self):
        try:
            # 1. 打开软件，登入账号
            self.login()
            self.statusBar_singel.emit('开始下载.\r\n')

            for center in self.centers.items():
                # 2. 选择营运中心
                self.select_center(center[1][0])
                # print(center[0])
                self.statusBar_singel.emit('正在下载%s...\r\n' % center[0])
                # 3. 输入作业，cglq307, 点击确定
                self.input_job()
                # 4. 筛选条件(期间(年、月、年、月)
                self.filter_duration()
                for subject in self.subjects:
                    # 4. 输入科目, 点击确定筛选
                    self.filter_subject(subject)
                    # 5. 导出/汇出excel
                    # 6. 新建营运中心文件夹，保存、更改文件名(添加 法人主体(营运中心)-默认)
                    self.export(center)
                    # 7. 回到过滤页面
                    self.reback_filter()
                    # 8. 点击查询按钮
                    if subject != self.subjects[-1]:
                        self.click_query()
                # 8. 回到选择账套(营运中心)界面
                self.reback_center()

            # 8. 最后一列添加‘法人主体’， 合并文件名为‘科目-期间’
            self.merge()
            # print('download finished')
            self.statusBar_singel.emit('下载完成.\r\n')
            self.finish_singel.emit()
        except Exception as err:
            print('payables catch error!!!')
            print(err)
            pyautogui.alert(text=str(err), title='error', button='OK')


if __name__ == '__main__':
    worker_other_payables = WorkerOtherPayables()

    # 加载现有配置文件
    conf = configparser.ConfigParser()
    path = os.path.join(os.getcwd(), 'configure.ini')
    conf.read(path, encoding="utf-8-sig")
    center = conf.items("center")
    centers = {position[0]: position[1].split(',') for position in center}
    print(centers)
    duration = [conf.get('payables', 'start_year'),
                conf.get('payables', 'start_month'),
                conf.get('payables', 'end_year'),
                conf.get('payables', 'end_month'),
                ]
    subjects = conf.get('payables', 'subject').split(',')
    print(subjects)
    save_path = conf.get('payables', 'save_path')
    job = conf.get('payables', 'job')
    worker_other_payables.set_parameter(centers=centers,
                                        duration=duration,
                                        job=job,
                                        subjects=subjects,
                                        save_path=save_path)
    #worker_other_payables.download()

    worker_other_payables.login()
    center = centers.popitem()
    # worker_other_payables.select_center(center[1][0])
    # worker_other_payables.input_job()
    # worker_other_payables.filter()
    #worker_other_payables.export(center)
    #worker_other_payables.merge()
