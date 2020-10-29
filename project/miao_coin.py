# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/05/30
# @Author  : 陈志鹏
# @File    : xx.py
"""

"""

__author__ = '陈志鹏'

import os
import sys
work_path = os.path.join(os.path.dirname(sys.argv[0]), "../")
sys.path.append(os.path.abspath(work_path))
os.chdir(work_path)

import uiautomator2 as u2
import random

from project.do_adb_click import *
from project.do_adb_arobot import *
from project.jingdong import *

from project import log

logger = log.Log(__name__, log_path=os.getcwd()).getlog()

def tapXY(x, y, task):
    for i in range(task):
        os.system('adb shell input tap {} {}'.format(x, y))  # 触摸店铺按钮
        print('---开始任务---')
        time.sleep(2)
        #随机生成触摸点 X Y
        tapx = random.randint(1, 500)
        tapy = random.randint(1, 500)
        print('---等待15秒---')
        for j in range(15):
            os.system('adb shell input swipe {} {} {} {}'.format(tapx, tapy, tapx, tapy))  # 模拟滑动界面
            time.sleep(1)
            print(j, end=' ')
        print('\r\n---领取完成---')
        os.system('adb shell input keyevent KEYCODE_BACK')
        time.sleep(2)
        # os.system('adb shell input tap 518 2202')
        print('第{}任务领取完成'.format(i + 1))
        print('______________________')


def downloadUi():
    if not os.path.exists('123.txt'):
        try:
            os.system('adb shell uiautomator dump /data/local/tmp/uidump.xml')
            time.sleep(2)
            os.system('adb shell uiautomator dump /data/local/tmp/uidump.xml')
            time.sleep(1)
            os.system('adb pull /data/local/tmp/uidump.xml 123.txt')
            size = os.path.getsize('123.txt')
            # print(size)
            if size < 2000:  # 第一次获取ui会出现文件非淘宝xml
                # print('xml文件错误正在重新下载，请勿翻动手机界面')
                # os.remove('123.txt')
                # downloadUi()
                raise Exception(print('xml文件错误正在重新下载，请勿翻动手机界面'))
        except Exception as e:
            # print('adb连接错误请重新打开')
            print('出现异常:', e)
            if os.path.exists('123.txt'):
                os.remove('123.txt')
            downloadUi()

def rearchTask(tapPosition):
    tapList = list()
    pattern = re.compile(r"\d+")
    for i in tapPosition:
        tapXYstr = re.search('\[(.*?)\]\[(.*?)\]', i).group()
        tapXYList = pattern.findall(tapXYstr)
        taskName = re.search('(.*)[\'|"] resource-id=', i).group(1)
        taskCntStr = re.search('(\d{1,}/\d{1,})', taskName).group()
        taskCntList = pattern.findall(taskCntStr)
        taskCnt = int(taskCntList[1]) - int(taskCntList[0])
        tapX = (int(tapXYList[2]) - int(tapXYList[0])) / 2.0 + int(tapXYList[0])
        tapY = (int(tapXYList[3]) - int(tapXYList[1])) / 2.0 + int(tapXYList[1])
        # print('%-20s cnt:%-2d [%4d,%4d]' % (taskName, taskCnt, tapX, tapY))
        if taskCnt > 0:
            tap_list = list()
            tap_list.append(taskName)
            tap_list.append(taskCnt)
            tap_list.append(tapX)
            tap_list.append(tapY)
            tapList.append(tap_list)
    return tapList

def openUi():
    tapList = list()
    c = open('123.txt', encoding='UTF-8')
    uiText = c.read()
    tapPosition = re.findall('<node index="0" text=[\'|"]浏(.*?)/>', uiText)  # 找到所有去浏览坐标
    tap_list = rearchTask(tapPosition)
    # print(tap_list)
    if len(tap_list) > 0:
        for i in tap_list:
            tapList.append(i)
            print('浏%-20s cnt:%-2d [%4d,%4d]' % (i[0], i[1], i[2], i[3]))

    tapPosition = re.findall('<node index="0" text=[\'|"]逛(.*?)/>', uiText)
    tap_list = rearchTask(tapPosition)
    if len(tap_list) > 0:
        for i in tap_list:
            tapList.append(i)
            print('逛%-20s cnt:%-2d [%4d,%4d]' % (i[0], i[1], i[2], i[3]))

    tapPosition = re.findall('<node index="0" text=[\'|"]搜(.*?)/>', uiText)
    tap_list = rearchTask(tapPosition)
    if len(tap_list) > 0:
        for i in tap_list:
            tapList.append(i)
            print('搜%-20s cnt:%-2d [%4d,%4d]' % (i[0], i[1], i[2], i[3]))

    tapPosition = re.findall('<node index="0" text=[\'|\"]去[^蚂|特|芭](.*?)/>', uiText)
    tap_list = rearchTask(tapPosition)
    if len(tap_list) > 0:
        for i in tap_list:
            tapList.append(i)
            print('去%-20s cnt:%-2d [%4d,%4d]' % (i[0], i[1], i[2], i[3]))

    print('以上是[去浏览/完成/搜索/开通]按钮坐标和任务坐标,请根据任务选取触摸坐标')
    print('---------------------------')

    return tapList


def get_FileSize(filePath):
    fsize = os.path.getsize(filePath)
    fsize = fsize / float(1024 * 1024)
    return round(fsize, 2)

if __name__ == '__main__':
    logger.info('\r\n ---------------- welcom to use -----------------')

    while 1:
        if os.path.exists('123.txt'):
            os.remove('123.txt')

        print('正在获取页面布局')
        print('----------------')
        downloadUi()
        tapList = openUi()
        print(tapList)
        if len(tapList) > 0:
            for name, task, x, y in tapList:
                startTime = time.time()
                tapXY(x, y, task)
                overTime = time.time()
                print('耗时：' + str(int(overTime - startTime)) + 's')
            # break
        else:
            print("任务全部完成")
            break