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
import tushare as ts
import pandas as pd
import sqlite3

from project import log

logger = log.Log(__name__, log_path=os.getcwd()).getlog()

def test1():
    import mysql.connector
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

def test2():
    import pymysql

    conn = pymysql.connect(
        host='localhost',  # 本地数据库
        user='root',  # 你设置的用户名
        passwd='123456',  # 你设置的密码
        db='stocks',  # 使用的数据库
        charset='utf8'  # 编码格式
    )

    # while True:
    cur = conn.cursor()  # 创建游标
    a = 1
    b = 2
    c = 3
    d = 4
    e = 5
    ret = cur.execute("insert into stocks values(%s,%s,%s,%s)" % (a, b, c, d))  # 存入你需要的相应的数据
    conn.commit()
    cur.close()

def test3():
    import pymysql

    # 将所有的股票名称和股票代码、行业、地区写入到名为allstock的表中，这个文件只需要执行一次

    # 通过tushare库获取所有的A股列表
    stock_info = ts.get_stock_basics()
    # 连接数据库
    conn = pymysql.connect(
        host='localhost',  # 本地数据库
        user='root',  # 你设置的用户名
        passwd='123456',  # 你设置的密码
        db='stocks',  # 使用的数据库
        charset='utf8'  # 编码格式
    )

    cur = conn.cursor()  # 创建游标

    codes = stock_info.index
    names = stock_info.name
    industrys = stock_info.industry
    areas = stock_info.area
    # 通过for循环遍历所有股票，然后拆分获取到需要的列，将数据写入到数据库中
    a = 0
    for i in range(0, len(stock_info)):
        print('(%s,%s,%s,%s)' % (codes[i], names[i], industrys[i], areas[i]))
        cur.execute('insert into stocks (code,name,industry,area) values (%s,%s,%s,%s)' % (codes[i], names[i], industrys[i], areas[i]))
        a += 1
    # 统计所有A股数量
    print('共获取到%d(%d)支股票 ' % (a, i+1))

    conn.commit()
    cur.close()

def test4():
    # 将所有的股票名称和股票代码、行业、地区写入到名为allstock的表中，这个文件只需要执行一次

    # 通过tushare库获取所有的A股列表
    stock_info = ts.get_stock_basics()

    codes = stock_info.index
    names = stock_info.name
    industrys = stock_info.industry
    areas = stock_info.area

    stock_info.to_excel('./test.xlsx')

    for i in range(0, len(stock_info)):
        print('(%s,%s,%s,%s)' % (codes[i], names[i], industrys[i], areas[i]))
    # 统计所有A股数量
    print('共获取到(%d)支股票 ' % (i+1))

def test5():
    import tushare as ts
    # import mysql.connector
    import pymysql
    import re, time
    # 创建所有股票的表格以及插入每支股票的近段时间的行情，这个文件只需要执行一次！！！
    # 想要写入哪一段时间的数据只需要修改starttime,endtime的时间就可以了
    def everdate(starttime, endtime):
        # 获取所有有股票
        stock_info = ts.get_stock_basics()
        # 连接数据库
        conn = pymysql.connect(user='root', password='123456', database='stocks')
        cursor = conn.cursor()

        codes = stock_info.index
        a = 0
        # 通过for循环以及获取A股只数来遍历每一只股票
        for x in range(0, len(stock_info)):
            # 匹配深圳股票（因为整个A股太多，所以我选择深圳股票做个筛选）
            if re.match('000', codes[x]) or re.match('002', codes[x]):
                # 以stock_加股票代码为表名称创建表格
                cursor.execute('create table stock_' + codes[
                    x] + ' (date varchar(32),open varchar(32),close varchar(32),high varchar(32),low varchar(32),volume varchar(32),p_change varchar(32),unique(date))')
                # 利用tushare包获取单只股票的阶段性行情
                df = ts.get_hist_data(codes[x], starttime, endtime)
                print('%s的表格创建完成' % codes[x])
                a += 1
                # 这里使用try，except的目的是为了防止一些停牌的股票，获取数据为空，插入数据库的时候失败而报错
                # 再使用for循环遍历单只股票每一天的行情
                try:
                    for i in range(0, len(df)):
                        # 获取股票日期，并转格式（这里为什么要转格式，是因为之前我2018-03-15这样的格式写入数据库的时候，通过通配符%之后他居然给我把-符号当做减号给算出来了查看数据库日期就是2000百思不得其解想了很久最后决定转换格式）
                        times = time.strptime(df.index[i], '%Y-%m-%d')
                        time_new = time.strftime('%Y%m%d', times)
                        # 插入每一天的行情
                        cursor.execute('insert into stock_' + codes[
                            x] + ' (date,open,close,high,low,volume,p_change) values (%s,%s,%s,%s,%s,%s,%s)' % (
                                       time_new, df.open[i], df.close[i], df.high[i], df.low[i], df.volume[i],
                                       df.p_change[i]))

                except:
                    print('%s这股票目前停牌' % codes[x])

        conn.close()
        cursor.close()
        # 统计总共插入了多少张表的数据
        print('所有股票总共插入数据库%d张表格' % a)

    everdate('2020-03-01', '2020-06-03')

def test6():
    conn = sqlite3.connect('kingname.db')
    try:
        with conn:
            conn.execute('''
            CREATE TABLE user (
            name TEXT,
            age INTEGER,
            address TEXT,
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT);
            ''')
    except Exception as err:
        print(err)

    sql = 'insert into user (id, name, age, address) values(?, ?, ?, ?)'
    datas = [
        (1, 'kingname', 20, '浙江省杭州市'),
        (2, '产品经理', 18, '上海市'),
        (3, '胖头猪', 8, '吃屁岛')
    ]
    with conn:
        conn.executemany(sql, datas)

    with conn:
        datas = conn.execute("select * from user where name = 'kingname'")
        for data in datas:
            print(data)

import tushare as ts

def test7():
    conn = sqlite3.connect('stocks.db')
    # cursor = conn.cursor()
    try:
        with conn:
            conn.execute('''
            create table allstock (
                code varchar(32),
                name varchar(32),
                industry varchar(32),
                area varchar(32))
            ''')
    except Exception as err:
        print(err)

    # 通过tushare库获取所有的A股列表
    stock_info = ts.get_stock_basics()

    codes = stock_info.index
    names = stock_info.name
    industrys = stock_info.industry
    areas = stock_info.area

    #通过for循环遍历所有股票，然后拆分获取到需要的列，将数据写入到数据库中
    a=0
    for i in range(0, len(stock_info)):
        sql = 'insert into allstock (code,name,industry,area) values (?, ?, ?, ?)'
        datas = [
            (codes[i],
             names[i],
             industrys[i],
             areas[i])
        ]
        conn.executemany(sql, datas)
        sql = 'insert into allstock (code,name,industry,area) values (%s,%s,%s,%s)' % (codes[i], names[i], industrys[i], areas[i])
        # cursor.execute(sql)
        a += 1
    #统计所有A股数量
    print('共获取到%d支股票' % a)

    conn.close()
    # cursor.close()


if __name__ == '__main__':
    logger.info('\r\n ---------------- welcom to use -----------------')
    # test1()
    # test2()
    # test3()
    # test4()
    # test5()
    # test6()
    test7()
