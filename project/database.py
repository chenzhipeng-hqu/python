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
import xlwt
work_path = os.path.join(os.path.dirname(sys.argv[0]), "../")
sys.path.append(os.path.abspath(work_path))
os.chdir(work_path)

import time
import sqlite3
import tushare as ts
from project import log

logger = log.Log(__name__, log_path=os.getcwd()).getlog()

class DataBase(object):
    """
    数据库操作
    """
    def __init__(self, start, database):
        logger.debug ('open %s database' % (database))
        if os.path.exists(database):
            first_flag = 0
        else:
            first_flag = 1

        self.conn = sqlite3.connect(database)
        self.cursor = self.conn.cursor()

        if first_flag:
            self.__creat_table_allstocks()
            # self.__creat_table_stocks(start='2020-06-03', end='2020-06-05')
            # self.__creat_table_stocks(start='2020-06-01', end='2020-06-04')
            self.__creat_table_stocks(start=start, end='2020-06-04')

    def __del__ (self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def __creat_table_allstocks(self):
        '''
        https://www.jianshu.com/p/0bcf47ce1239
        :return:
        '''
        try:
            self.conn.execute('''
            create table allstock (
                code varchar(32) NOT NULL UNIQUE,
                name varchar(32) ,
                industry varchar(32) ,
                area varchar(32))
            ''')
            # cursor = self.conn.cursor()
            # cursor.execute('alter table allstock add unique (date)')
        except Exception as err:
            logger.warning(err)
        stock_info = ts.get_stock_basics()
        stock_info.sort_index(inplace=True)
        stock_info.to_sql('allstock', self.conn, if_exists='replace', chunksize=10000)

        # 统计所有A股数量
        logger.info('共获取到%d支股票' % (len(stock_info)))

    def __creat_table_allstocks2(self):
        try:
            self.conn.execute('''
            create table allstock (
                code varchar(32) NOT NULL UNIQUE,
                name varchar(32) ,
                industry varchar(32) ,
                area varchar(32))
            ''')
            # cursor = self.conn.cursor()
            # cursor.execute('alter table allstock add unique (date)')
        except Exception as err:
            logger.warning(err)

        stock_info = ts.get_stock_basics()
        # stock_info = sorted(stock_info)
        stock_info.sort_index(inplace=True)
        codes = stock_info.index
        names = stock_info.name
        industrys = stock_info.industry
        areas = stock_info.area

        # 通过for循环遍历所有股票，然后拆分获取到需要的列，将数据写入到数据库中
        datas = [(codes[i], names[i], industrys[i], areas[i]) for i in range(0, len(stock_info))]
        sql = 'insert or ignore into allstock (code,name,industry,area) values (?, ?, ?, ?)'
        self.conn.executemany(sql, datas)

        # stock_info.to_sql('allstock', self.conn, if_exists='replace')

        # 统计所有A股数量
        logger.info('共获取到%d支股票' % (len(stock_info)))

    def export2excel(self, table_name):
        cur = self.conn.cursor()
        sql = 'select * from %s' % table_name
        cur.execute(sql)  # 返回受影响的行数

        fields = [field[0] for field in cur.description]  # 获取所有字段名
        all_data = cur.fetchall()  # 所有数据

        # 写入excel
        book = xlwt.Workbook()
        sheet = book.add_sheet('sheet1')

        for col, field in enumerate(fields):
            sheet.write(0, col, field)

        row = 1
        for data in all_data:
            for col, field in enumerate(data):
                sheet.write(row, col, field)
            row += 1
        book.save("./datas/%s.xls" % table_name)

        cur.close()

    def __strptime(self, data):
        times = time.strptime(data, '%Y-%m-%d')
        time_new = time.strftime('%Y%m%d', times)
        return time_new

    def __creat_table_stocks(self, start, end=time.strftime('%Y-%m-%d')):
        # 获取所有有股票
        stock_info = ts.get_stock_basics()
        codes = sorted(stock_info.index)[:5]
        for code in codes:
            df = ts.get_hist_data(code, start=start, end=end)
            df.sort_index(inplace=True)
            df.index = df.index.map(self.__strptime)
            df = df[['open', 'close', 'high', 'low', 'volume', 'p_change']]

            try:
                # self.conn.execute('create table stock_' + code
                #      + ' (date varchar(32),'
                #        'open varchar(32),'
                #        'close varchar(32),'
                #        'high varchar(32),'
                #        'low varchar(32),'
                #        'volume varchar(32),'
                #        'price_change varchar(32),'
                #        'p_change varchar(32),'
                #        'ma5 varchar(32),'
                #        'ma10 varchar(32),'
                #        'ma20 varchar(32),'
                #        'v_ma5 varchar(32),'
                #        'v_ma10 varchar(32),'
                #        'v_ma20 varchar(32),'
                #        'unique(date))')
                # self.conn.commit()

                self.cursor.execute(
                    'create table if not exists stock_' + code + ' (date varchar(32),open varchar(32),close varchar(32),high varchar(32),low varchar(32),volume varchar(32),p_change varchar(32),unique(date))')

                # 利用tushare包获取单只股票的阶段性行情
                # 这里使用try，except的目的是为了防止一些停牌的股票，获取数据为空，插入数据库的时候失败而报错
                # 再使用for循环遍历单只股票每一天的行情
                # for i in range(0, len(df)):
                #     # 获取股票日期，并转格式（这里为什么要转格式，是因为之前我2018-03-15这样的格式写入数据库的时候，通过通配符%之后他居然给我把-符号当做减号给算出来了查看数据库日期就是2000百思不得其解想了很久最后决定转换格式）
                #     times = time.strptime(df.index[i], '%Y-%m-%d')
                #     time_new = time.strftime('%Y%m%d', times)
                #     # 插入每一天的行情
                #     self.cursor.execute('insert or ignore into stock_' + code + ' (date,open,close,high,low,volume,p_change) values (%s,%s,%s,%s,%s,%s,%s)' %
                #                    (time_new, df.open[i], df.close[i], df.high[i], df.low[i], df.volume[i],
                #                    df.p_change[i]))

                df.to_sql('stock_'+ code, self.conn, if_exists='append', chunksize=10000)
                # self.conn.execute('alter table stock_' + code + ' add unique (date)')  # 删除重复的数据
                logger.info('stock_%s的表格创建完成' % (code))
            except Exception as err:
                logger.warning(err)
                logger.info('%s这股票目前停牌' % code)
        logger.info('所有股票总共插入数据库%d张表格' % len(codes))

    def __add_data_to_stocks(self, start=time.strftime('%Y-%m-%d'), end=time.strftime('%Y-%m-%d')):
        # 获取所有有股票
        stock_info = ts.get_stock_basics()
        codes = sorted(stock_info.index)[:5]
        for code in codes:
            df = ts.get_hist_data(code, start=start, end=end)
            df.sort_index(inplace=True)
            df = df[['open', 'close', 'high', 'low', 'volume', 'p_change']]

            try:
                # 利用tushare包获取单只股票的阶段性行情
                # 这里使用try，except的目的是为了防止一些停牌的股票，获取数据为空，插入数据库的时候失败而报错
                # 再使用for循环遍历单只股票每一天的行情
                for i in range(0, len(df)):
                    # 获取股票日期，并转格式（这里为什么要转格式，是因为之前我2018-03-15这样的格式写入数据库的时候，通过通配符%之后他居然给我把-符号当做减号给算出来了查看数据库日期就是2000百思不得其解想了很久最后决定转换格式）
                    times = time.strptime(df.index[i], '%Y-%m-%d')
                    time_new = time.strftime('%Y%m%d', times)
                    # 插入每一天的行情
                    self.cursor.execute('insert or ignore into stock_' + code + ' (date,open,close,high,low,volume,p_change) values (%s,%s,%s,%s,%s,%s,%s)' %
                                   (time_new, df.open[i], df.close[i], df.high[i], df.low[i], df.volume[i],
                                   df.p_change[i]))

                logger.info('stock_%s的表格添加完成' % (code))
            except Exception as err:
                logger.warning(err)
                logger.info('%s这股票目前停牌' % code)
        logger.info('%d张表格数据插入完成' % len(codes))

    def fetch_data(self, start, end):
        cursor.execute('select * from stock_' + value_code[i][0] + ' where date=%s or date =%s order by date desc' % (
        today, str_yestoday))  # 当天
        # cursor.execute('select * from stock_'+ value_code[i][0]+ ' where date=%s or date =%s'%('20180315','20180314'))
        value = cursor.fetchall()

    def update(self):

        self.__add_data_to_stocks('2020-06-03')


if __name__ == '__main__':
    logger.info('\r\n ---------------- welcom to use -----------------')
    db = DataBase(start='2020-06-01', database='./datas/stocks.db')
    db.update()

    db.export2excel('allstock')
    db.export2excel('stock_000001')
