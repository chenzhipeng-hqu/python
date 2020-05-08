# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/03/26
# @Author  : 陈志鹏
# @File    : financial_tools.py

import os
import sys
import codecs
import logging
import pyautogui
import xml.sax
import unittest
import configparser
import pandas as pd
from financial_ui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from other_payables import *
from internal_orders import *
from custom_control import *
from others.merge import *
from others.fetch import *

logging.basicConfig(
    level=logging.DEBUG,
    filename='out.log',
    datefmt='%Y-%m-%d %H:%M:%S',
    format='%(asctime)s - %(levelname)s - %(filename)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s')

logger = logging.getLogger()

class test:
    def warning(self):
        logger.warning('this is warning message')
        print(__name__)
    def info(self):
        logger.info('this is info message')
        print(__name__)
    def debug(self):
        logger.debug('this is debug message')
        print(__name__)

    def setLogName(self, name):
        handler = logging.FileHandler(name, mode='w')
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', '%a, %d %b %Y %H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)


class Dict(dict):
    def __init__(self, **kw):
        super(Dict, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


class TestDict(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('setUpClass %s' % cls.__class__.__name__)

    @classmethod
    def tearDownClass(cls):
        print('tearDownClass %s' % cls.__class__.__name__)

    def setUp(self):
        print('setUp %s' % self.__class__.__name__)

    def tearDown(self):
        print('tearDown %s' % self.__class__.__name__)

    @unittest.skip("i don't want to run this case.")
    def test_init(self):
        d = Dict(a=1, b='test')
        self.assertEqual(d.a, 1)  # 判断d.a是否等于1
        self.assertEqual(d.b, 'test')  # 判断d.b是否等于test
        self.assertTrue(isinstance(d, dict))  # 判断d是否是dict类型

    def test_key(self):
        d = Dict()
        d['key'] = 'value'
        self.assertEqual(d.key, 'value')

    def test_attr(self):
        d = Dict()
        d.key = 'value'
        self.assertTrue('key' in d)
        self.assertEqual(d['key'], 'value')

    def test_keyerror(self):
        d = Dict()
        with self.assertRaises(KeyError):  # 通过d['empty']访问不存在的key时，断言会抛出keyerror
            value = d['empty']

    def test_attrerror(self):
        d = Dict()
        with self.assertRaises(AttributeError):  # 通过d.empty访问不存在的key时，我们期待抛出AttributeError
            value = d.empty


if __name__ == '__main__':
    # setLogName('out.log')
    # test.info()
    # test.warning()
    # test.debug()
    # print(__name__)
    unittest.main(verbosity=2)
