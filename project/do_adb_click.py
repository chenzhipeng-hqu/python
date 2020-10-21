#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @File    : do_adb_click.py
# @Date    : 2020-10-15
# @Author  : chenzhipeng

"""
# 通过python调用adb命令实现用元素名称、id、class定位元素
# http://blog.csdn.net/gb112211/article/details/33730221
"""

__author__ = '陈志鹏'

import os
import sys

work_path = os.path.join(os.path.dirname(sys.argv[0]), "../")
sys.path.append(os.path.abspath(work_path))
os.chdir(work_path)

from project import log

logger = log.Log(__name__, log_path=os.getcwd()).getlog()


import tempfile
import os
import re
import time
import xml.etree.cElementTree as ET

class Element(object):
    """
    通过元素定位,需要Android 4.0以上
    """
    def __init__(self):
        """
        初始化，获取系统临时文件存储目录，定义匹配数字模式
        """
        self.tempFile = tempfile.gettempdir()
        logger.debug('temp file path "%s"' % self.tempFile)
        self.pattern = re.compile(r"\d+")

    def __uidump(self):
        """
        获取当前Activity控件树
        """
        temp = os.popen("adb shell uiautomator dump /data/local/tmp/uidump.xml")
        # logger.debug(temp.read())
        time.sleep(0.1)
        os.popen("adb pull /data/local/tmp/uidump.xml " + self.tempFile)
        time.sleep(2)

    def __element(self, attrib, name):
        """
        同属性单个元素，返回单个坐标元组
        """
        self.__uidump()
        tree = ET.ElementTree(file=os.path.join(self.tempFile, "uidump.xml"))
        treeIter = tree.iter(tag="node")

        for elem in treeIter:
            if elem.attrib[attrib] == name:
                logger.debug('find %s' % (name))
                bounds = elem.attrib["bounds"]
                coord = self.pattern.findall(bounds)
                Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                return Xpoint, Ypoint

    def __elements(self, attrib, name):
        """
        同属性多个元素，返回坐标元组列表
        """
        list = []
        self.__uidump()
        tree = ET.ElementTree(file=os.path.join(self.tempFile, 'uidump.xml'))
        treeIter = tree.iter(tag="node")

        for elem in treeIter:
            if elem.attrib[attrib] == name:
                bounds = elem.attrib["bounds"]
                coord = self.pattern.findall(bounds)
                Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                list.append((Xpoint, Ypoint))

        return list

    def findElementByContentDesc(self, name):
        return self.__element("content-desc", name)

    def findElementByName(self, name):
        """
        通过元素名称定位
        usage: findElementByName(u"设置")
        """
        return self.__element("text", name)

    def findElementsByName(self, name):
        return self.__elements("text", name)

    def findElementByClass(self, className):
        """
        通过元素类名定位
        usage: findElementByClass("android.widget.TextView")
        """
        return self.__element("class", className)

    def findElementsByClass(self, className):
        return self.__elements("class", className)

    def findElementById(self, id):
        """
        通过元素的resource-id定位
        usage: findElementsById("com.android.deskclock:id/imageview")
        """
        return self.__element("resource-id", id)

    def findElementsById(self, id):
        return self.__elements("resource-id", id)

    def getPicture(self):
        """
        获取手机截图
        :return:
        """
        os.popen("adb shell /system/bin/screencap -p /data/local/tmp/tmp.png")
        time.sleep(1)
        os.popen("adb pull /data/local/tmp/tmp.png " + os.path.join(self.tempFile, "tmp.png"))

    def findElementsByxPath(self, xpath):
        """
        同属性单个元素，返回单个坐标元组
        """
        self.__uidump()
        tree = ET.ElementTree(file=os.path.join(self.tempFile, "uidump.xml"))
        treeIter = tree.xpath(xpath)
        logger.debug(treeIter)
        for elem in treeIter:
            bounds = elem.attrib["bounds"]
            coord = self.pattern.findall(bounds)
            Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
            Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
            return Xpoint, Ypoint


class Event(object):

    def __init__(self):
        os.popen("adb wait-for-device ")

    def touch(self, dx, dy):
        """
        触摸事件
        usage: touch(500, 500)
        """
        os.popen("adb shell input tap " + str(dx) + " " + str(dy))
        time.sleep(0.5)


def sendPYQ():
    element = Element()
    evevt = Event()

    e1 = element.findElementByName(u"微信")
    evevt.touch(e1[0], e1[1])
    time.sleep(1)

    e2 = element.findElementByName(u"发现")
    evevt.touch(e2[0], e2[1])

    e3 = element.findElementByName(u"朋友圈")
    evevt.touch(e3[0], e3[1])

    e4 = element.findElementByContentDesc(u"更多功能按钮")
    evevt.touch(e4[0], e4[1])

    e5 = element.findElementByName(u"照片")
    evevt.touch(e5[0], e5[1])

    # 选择第一张照片
    e7 = element.findElementById(u"com.tencent.mm:id/b2y")
    evevt.touch(e7[0], e7[1])

    e7 = element.findElementById(u"com.tencent.mm:id/fb")
    evevt.touch(e7[0], e7[1])

    e7 = element.findElementById(u"com.tencent.mm:id/fb")
    evevt.touch(e7[0], e7[1])


def sendDianzan():
    element = Element()
    evevt = Event()
    e1 = element.findElementByName(u"微信")
    evevt.touch(e1[0], e1[1])

    time.sleep(1)

    e2 = element.findElementByName(u"发现")
    evevt.touch(e2[0], e2[1])

    e3 = element.findElementByName(u"朋友圈")
    evevt.touch(e3[0], e3[1])

    e7 = element.findElementById(u"com.tencent.mm:id/ce3")
    evevt.touch(e7[0], e7[1])

    e7 = element.findElementById(u"com.tencent.mm:id/cdd")
    evevt.touch(e7[0], e7[1])

# sendPYQ()
# sendDianzan()

def JindDongFarmer(addr):
    element = Element()
    evevt = Event()

    e = element.findElementByName(u"京东")
    logger.debug(e)
    evevt.touch(e[0], e[1]-200)
    time.sleep(2)

    e2 = element.findElementByName('u"免费水果"')
    evevt.touch(e2[0], e2[1])

    e2 = element.findElementsByxPath('//*[@resource-id="app"]/android.view.View[1]/android.view.View[1]/android.view.View[2]/android.view.View[2]/android.view.View[9]/android.view.View[1]')
    evevt.touch(e2[0], e2[1])

    # e3 = element.findElementByName(u"朋友圈")
    # evevt.touch(e3[0], e3[1])
    #
    # e4 = element.findElementByContentDesc(u"更多功能按钮")
    # evevt.touch(e4[0], e4[1])
    #
    # e5 = element.findElementByName(u"照片")
    # evevt.touch(e5[0], e5[1])
    #
    # # 选择第一张照片
    # e7 = element.findElementById(u"com.tencent.mm:id/b2y")
    # evevt.touch(e7[0], e7[1])
    #
    # e7 = element.findElementById(u"com.tencent.mm:id/fb")
    # evevt.touch(e7[0], e7[1])
    #
    # e7 = element.findElementById(u"com.tencent.mm:id/fb")
    # evevt.touch(e7[0], e7[1])
