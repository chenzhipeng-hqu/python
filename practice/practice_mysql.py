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

# import MySQLdb
# from ReadCode import ReadCode
import mysql.connector
import tushare as ts

from project import log

logger = log.Log(__name__, log_path=os.getcwd()).getlog()



if __name__ == '__main__':
    logger.info('\r\n ---------------- welcom to use -----------------')

    # 将所有的股票名称和股票代码、行业、地区写入到名为allstock的表中，这个文件只需要执行一次

    # 通过tushare库获取所有的A股列表
    stock_info = ts.get_stock_basics()
    # 连接数据库
    conn = mysql.connector.connect(user='root', password='password', database='test')
    cursor = conn.cursor()

    codes = stock_info.index
    names = stock_info.name
    industrys = stock_info.industry
    areas = stock_info.area
    # 通过for循环遍历所有股票，然后拆分获取到需要的列，将数据写入到数据库中
    a = 0
    for i in range(0, len(stock_info)):
        cursor.execute('insert into allstock (code,name,industry,area) values (%s,%s,%s,%s)',
                       (codes[i], names[i], industrys[i], areas[i]))
        a += 1
    # 统计所有A股数量
    print('共获取到%d支股票' % a)

    conn.commit()
    cursor.close()
    conn.close()
