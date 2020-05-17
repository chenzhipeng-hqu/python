# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/03/26
# @Author  : 陈志鹏
# @File    : xxx.py

import unittest
from test_all import *
import log

logger = log.Log(__name__).getlog()

def log_test():
    logger.critical("test")
    logger.error("test")
    logger.warning("test")
    logger.info("test")
    logger.debug("test")


if __name__ == '__main__':
    '''
    https://blog.csdn.net/xiaoquantouer/article/details/75089200
    '''
    logger.critical("start")
    logger.error("start")
    logger.warning("start")
    logger.info("start")
    logger.debug("start")
    log_test()

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