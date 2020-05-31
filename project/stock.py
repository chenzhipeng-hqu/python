# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/05/31
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

from project import log

logger = log.Log(__name__, log_path=os.getcwd()).getlog()

class Stock(object):
    """

    """
    def __init__(self, name, code):
        if type(code) != str:
            return ("错误， 输入参数必须为字符型")
        self.__code = code
        self.__name = name

    def get_attr(self):
        return (self.__code, self.__name)

    @classmethod
    def split(cls, sc):
        print('123')
        stock, code = map(str, sc.split('-'))
        dd = cls(stock, code)
        return dd
    

if __name__ == '__main__':
    logger.info('\r\n ---------------- welcom to use -----------------')
    stock = Stock('正川股份', '603976')
    print(stock.get_attr())


