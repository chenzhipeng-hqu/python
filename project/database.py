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
import datetime
import sqlite3
import tushare as ts
from project import log

logger = log.Log(__name__, log_path=os.getcwd()).getlog()

class DataBase(object):
    """
    数据库操作
    https://tushare.pro/document/2
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
            # self.__creat_table_stocks(start=start, end='2020-06-04')
            self.__creat_table_stocks(start=start)

        logger.info('max_date: %s' % self.fetch_max_date('000001'))

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
            create table allstocks (
                code varchar(32) NOT NULL UNIQUE,
                name varchar(32) ,
                industry varchar(32) ,
                area varchar(32))
            ''')
            # cursor = self.conn.cursor()
            # cursor.execute('alter table allstocks add unique (date)')
        except Exception as err:
            logger.warning(err)
        stock_info = ts.get_stock_basics()
        stock_info.sort_index(inplace=True)
        stock_info.to_sql('allstocks', self.conn, if_exists='replace', chunksize=10000)

        # 统计所有A股数量
        logger.info('共获取到%d支股票' % (len(stock_info)))

    def __creat_table_allstocks2(self):
        try:
            self.conn.execute('''
            create table allstocks (
                code varchar(32) NOT NULL UNIQUE,
                name varchar(32) ,
                industry varchar(32) ,
                area varchar(32))
            ''')
            # cursor = self.conn.cursor()
            # cursor.execute('alter table allstocks add unique (date)')
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
        sql = 'insert or ignore into allstocks (code,name,industry,area) values (?, ?, ?, ?)'
        self.conn.executemany(sql, datas)

        # stock_info.to_sql('allstocks', self.conn, if_exists='replace')

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

    def __time2format(self, data, i_fmt, o_fmt):
        times = time.strptime(data, i_fmt)
        return time.strftime(o_fmt, times)

    def __date2time(self, data):
        return self.__time2format(data, '%Y-%m-%d', '%Y%m%d')

    def __creat_table_stocks(self, start, end=time.strftime('%Y-%m-%d')):
        # 获取所有有股票
        stock_info = ts.get_stock_basics()
        # codes = sorted(stock_info.index)[:24]
        codes = sorted(stock_info.index)
        for code in codes:
            df = ts.get_hist_data(code, start=start, end=end)

            try:
                df.sort_index(inplace=True)
                df.index = df.index.map(self.__date2time)
                df = df[['open', 'close', 'high', 'low', 'volume', 'p_change']]

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

                self.conn.execute(
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
        # 每次将 000001 放在最后更新, update中判断000001是否最新数据
        # codes = sorted(sorted(stock_info.index)[:24], reverse=True)
        codes = sorted(stock_info.index, reverse=True)
        # codes = sorted(stock_info.index)
        for code in codes:
            cursor = self.conn.execute(
                'create table if not exists stock_' + code + ' (date varchar(32),open varchar(32),close varchar(32),high varchar(32),low varchar(32),volume varchar(32),p_change varchar(32),unique(date))')
            # logger.info(len(list(cursor)))
            # logger.info(code)

            # 利用tushare包获取单只股票的阶段性行情
            df = ts.get_hist_data(code, start=start, end=end)

            try:
                df.sort_index(inplace=True)
                df = df[['open', 'close', 'high', 'low', 'volume', 'p_change']]
                # 这里使用try，except的目的是为了防止一些停牌的股票，获取数据为空，插入数据库的时候失败而报错
                # 再使用for循环遍历单只股票每一天的行情
                # for i in range(0, len(df)):
                #     # 获取股票日期，并转格式（这里为什么要转格式，是因为之前我2018-03-15这样的格式写入数据库的时候，通过通配符%之后他居然给我把-符号当做减号给算出来了查看数据库日期就是2000百思不得其解想了很久最后决定转换格式）
                #     time_new = self.__date2time(df.index[i])
                #     # logger.debug(time_new)
                #     # 插入每一天的行情
                #     sql = r'insert or ignore into stock_' + code + ' (date,open,close,high,low,volume,p_change) values (%s,%s,%s,%s,%s,%s,%s)' %\
                #                    (time_new, df.open[i], df.close[i], df.high[i], df.low[i], df.volume[i],
                #                    df.p_change[i])
                #     self.conn.execute(sql)
                #     # logger.info(sql)

                # 通过for循环遍历所有股票，然后拆分获取到需要的列，将数据写入到数据库中
                datas = [(self.__date2time(df.index[i]), \
                          df.open[i], df.close[i], df.high[i], df.low[i], \
                          df.volume[i], df.p_change[i]) for i in range(0, len(df))]
                # sql = 'insert or ignore into allstocks (code,name,industry,area) values (?, ?, ?, ?)'
                sql = r'insert or ignore into stock_' + code + ' (date,open,close,high,low,volume,p_change) values (?,?,?,?,?,?,?)'
                self.conn.executemany(sql, datas)

                logger.info('stock_%s 表格添加完成' % (code))
            except Exception as err:
                logger.warning(err)
                logger.info('%s这股票目前无数据' % code)
        logger.info('%d张表格数据插入完成' % len(codes))

    def get_all_stocks(self):
        cur = self.conn.cursor()
        sql = 'select * from allstocks'
        cur.execute(sql)  # 返回受影响的行数
        all_data = cur.fetchall()  # 所有数据
        # print(len(all_data))
        # print(all_data)
        return all_data

    def fetch_data(self, code, start, end=None):
        '''
        https://cloud.tencent.com/developer/article/1532914
        https://www.cnblogs.com/z3286586/p/11845004.html
        https://www.jb51.net/article/121089.htm
        '''
        # self.cursor.execute('select * from stock_' + code + ' order by date desc limit 1')  # 当天
        self.cursor.execute('select * from stock_' + code + ' where date>=%s and date<=%s' % (start, end))
        value = self.cursor.fetchall()
        logger.debug(value)
        return value

    def fetch_min_date(self, code):
        self.cursor.execute('select min(date) from stock_' + code) # 返回 date 列的最大值
        value = self.cursor.fetchone()
        # print(value)
        return value

    def fetch_max_date(self, code):
        self.cursor.execute('select max(date) from stock_' + code) # 返回 date 列的最大值
        # cursor.execute('select * from stock_'+ value_code[i][0]+ ' where date=%s or date =%s'%('20180315','20180314'))
        value = self.cursor.fetchone()
        # print(value)
        return value

    def fetch_history_data(self, start):
        '''
        第一条数据比 start 更大 则更新数据
        '''
        start_day = self.__time2format(start, '%Y-%m-%d', '%Y%m%d')
        first_day = self.fetch_min_date('000001')[0]

        if start_day < first_day:
            logger.info('code:000001, start_day:%s, db_first_day:%s' % (start_day, first_day))
            start = self.__time2format(start_day, '%Y%m%d', '%Y-%m-%d')
            first = self.__time2format(first_day, '%Y%m%d', '%Y-%m-%d')
            self.__add_data_to_stocks(start, first)

    def fetch_len_allstocks(self):
        # 先计算一个数据库表中的行数
        self.cursor.execute('select count(*) from allstocks;')
        # cursor.execute('select * from stock_'+ value_code[i][0]+ ' where date=%s or date =%s'%('20180315','20180314'))
        value = self.cursor.fetchone()[0]
        # print(value)
        return value

    def update_allstocks(self):
        '''
        每次启动的时候检查一次是否更新, 以股票数量为主
        :return:
        '''
        len = self.fetch_len_allstocks()
        # 获取所有有股票
        stock_info = ts.get_stock_basics()
        logger.debug(stock_info.shape[0])
        if len < stock_info.shape[0]:
            self.__creat_table_allstocks()

    def update_stock_code(self):
        '''
        每次启动的时候检查一次是否更新, 以000001为准
        :return:
        '''
        last_day = self.fetch_max_date('000001')[0]
        today = datetime.datetime.now()

        now = time.strftime('%H:%M:%S')
        if now < '15:06:06':
            logger.info('没到下午3点')
            today = today + datetime.timedelta(days=-1)

        today = today.strftime('%Y%m%d')

        if today != last_day:
            start = self.__time2format(last_day, '%Y%m%d', '%Y-%m-%d')
            today = time.strftime('%Y-%m-%d')
            logger.info('code:000001, db_last_day:%s, today:%s' % (last_day, today))
            self.__add_data_to_stocks(start, today)
            # self.__add_data_to_stocks('2020-06-01')

    def update(self):
        '''
        每次启动的时候检查一次是否更新, 以000001为准
        :return:
        '''
        self.update_allstocks()
        self.update_stock_code()

    def valid_stock(self, dates):
        '''
        从数据库获取股票数据，统计想要查找日期的满足阳包阴并且当天涨停的股票
        '''
        # 先将字符串格式的时间转换为时间格式才能计算昨天的日期
        now = datetime.date(*map(int,dates.split('-')))
        oneday = datetime.timedelta(days=1)
        yestody = str(now - oneday)
        #将昨天日期转换为规定的字符串格式
        times = time.strptime(yestody,'%Y-%m-%d')
        str_yestoday = time.strftime('%Y%m%d',times)
        logger.info('执行的时间前一天是%s'%str_yestoday)
        #将想要查找的日期转换为规定的字符串格式
        str_today = time.strptime(dates,'%Y-%m-%d')
        today = time.strftime('%Y%m%d',str_today)
        logger.info('执行的时间是%s'%today)
        #连接数据库
        cursor = self.conn.cursor()
        #查找allstock表获取所有股票代码
        cursor.execute('select code from allstocks')
        value_code = cursor.fetchall()
        a = 0
        count = []
        #遍历所有股票
        for i in range(0,len(value_code)):
            # if re.match('000',value_code[i][0]) or re.match('002',value_code[i][0]):
            #查询所有匹配到的股票，将今天与昨天的数据对比
            try:
                sql = 'select * from stock_'+ value_code[i][0]+ ' where date=%s or date =%s order by date desc' % (today, str_yestoday)
                # logger.info(sql)
                cursor.execute(sql)  #当天
                #cursor.execute('select * from stock_'+ value_code[i][0]+ ' where date=%s or date =%s'%('20180315','20180314'))
                value = cursor.fetchall()

                #1是昨天，2是今天
                #今天的开盘价
                opens1 = float(value[0][1])
                #今天的收盘价
                close1 = float(value[0][2])
                #今天的涨幅
                p_change1 = float(value[0][6])
                #昨天的。。。。。
                opens2 = float(value[1][1])
                close2 = float(value[1][2])
                p_change2 = float(value[1][6])

                #加入这两天的数据满足昨天下跌超过2%，而且今天的开盘价低于昨天的收盘价，且今天的收盘价高于昨天的收盘价，就满足阳包阴的条件
                if opens2<close1 and close2>opens1 and p_change2<-2 and p_change1>9.8:
                    # logger.info('%s票%s的开盘价是%s'%(value_code[i][0],today,opens1))
                    # logger.info('%s票%s的收盘价是%s'%(value_code[i][0],today,close1))
                    # logger.info('%s票%s的涨幅是%s'%(value_code[i][0],today,p_change1))
                    # logger.info('%s票%s的开盘价是%s'%(value_code[i][0],str_yestoday,opens2))
                    # logger.info('%s票%s的收盘价价是%s'%(value_code[i][0],str_yestoday,close2))
                    # logger.info('%s票%s的涨幅是%s'%(value_code[i][0],str_yestoday,p_change2))
                    logger.info('%s: %s' % (value_code[i][0], value[0]))
                    logger.info('%s: %s' % ('      ', value[1]))
                    # logger.info('%s' % (value[1]))
                    #将满足条件的股票代码放进列表中，统计当天满足条件的股票
                    count.append(value_code[i][0])
                    a += 1
            except:
                #之前有次sql语句出错了，order by后面没加date，每次寻找都是0支，找了半个多小时才找出来是sql语句的问题
                logger.debug('%s停牌无数据,或者请查看sql语句是否正确' % value_code[i][0])#一般不用管，除非执行好多天的数据都为0时那可能输sql语句有问题了

        logger.info('总共找到%d支满足条件的股票:%s' % (a, count))
        return count, a

if __name__ == '__main__':
    logger.info('\r\n ---------------- welcom to use -----------------')
    db = DataBase(start='2020-06-03', database='./datas/stocks.db')
    # db.fetch_history_data('2019-01-01')
    db.update()
    # value = db.fetch_data('000001', '20200603', '20200605')

    # db.export2excel('allstocks')
    db.export2excel('stock_000001')

    # for stock in db.get_all_stocks():
    #     print(stock[0])
    # db.valid_stock('2020-06-10')
