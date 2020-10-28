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

def go(x, y):
    for i in range(task):
        os.system('adb shell input tap {} {}'.format(x, y))  # 触摸店铺按钮
        print('---开始任务---')
        time.sleep(4)
        print('---等待15秒---')
        for j in range(12):
            os.system('adb shell input tap {} {}'.format(1, 1))  # 模拟滑动界面
            time.sleep(1)
            print(j, end=' ')
        print('\r\n---领取完成---')
        time.sleep(1)
        os.system('adb shell input keyevent KEYCODE_BACK')
        time.sleep(2)
        # os.system('adb shell input tap 518 2202')
        print('第{}任务领取完成'.format(i + 1))
        print('______________________')


def go_2():
    if os.path.exists('123.txt'):
        c = open('123.txt', encoding='UTF-8')
        a = c.read()
        e = re.findall('<node index="1" text="去浏览"(.*?)/>', a)  # 找到所有去浏览坐标
        for i in e:
            g = re.search('\[(.*?)\]', i).group()
            print(g)
        print('以上是按照当前淘宝所有排序的“去浏览”按钮,请根据排序填入要刷取的任务')
        print('---------------------------')
    else:
        try:
            os.system('adb shell uiautomator dump /data/local/tmp/uidump.xml')
            time.sleep(2)
            os.system('adb shell uiautomator dump /data/local/tmp/uidump.xml')
            time.sleep(1)
            os.system('adb pull /data/local/tmp/uidump.xml 123.txt')
            size = get_FileSize('123.txt')
            print(size)
            if size >= 0.02:  # 第一次获取ui会出现文件非淘宝xml
                go_2()
            else:
                print('xml文件错误正在重新下载，请勿翻动手机界面')
                os.remove('123.txt')
                go_2()
        except:
            print('错误！正在回调函数')
            if os.path.exists('123.txt'):
                os.remove('123.txt')
            go_2()


def get_FileSize(filePath):
    fsize = os.path.getsize(filePath)
    fsize = fsize / float(1024 * 1024)
    return round(fsize, 2)


if __name__ == '__main__':
    logger.info('\r\n ---------------- welcom to use -----------------')

    if os.path.exists('123.txt'):
        os.remove('123.txt')

    print('正在获取页面布局')
    print('----------------')
    go_2()
    print('author：刘秉哲')
    # while 1:
    task = int(input('请输入任务个数：'))
    x = int(input('请输入任务X坐标：'))
    y = int(input('请输入任务y坐标：'))
    go(x + 20, y + 20)