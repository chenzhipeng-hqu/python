# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/03/26
# @Author  : 陈志鹏
# @File    : xxx.py

import logging
import unittest
from test_all import *

logging.basicConfig(
    level=logging.DEBUG,
    filename='out.log',
    datefmt='%Y-%m-%d %H:%M:%S',
    format='%(asctime)s - %(levelname)s - %(filename)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s')

logger = logging.getLogger()


if __name__ == '__main__':
    '''
    https://blog.csdn.net/xiaoquantouer/article/details/75089200
    '''
    suite = unittest.TestSuite()

    tests = [TestDict("test_init"),
             TestDict("test_key"),
             TestDict("test_attr"),
             TestDict("test_keyerror"),
             TestDict("test_attrerror")]

    suite.addTests(tests)

    # with open('UnittestTextReport.txt', 'a') as f:
    #     runner = unittest.TextTestRunner(stream=f, verbosity=2)
    #     runner.run(suite)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)