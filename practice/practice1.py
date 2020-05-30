# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/05/30
# @Author  : 陈志鹏
# @File    : xx.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../")))

import tushare as ts
import matplotlib.pyplot as plt
import talib as ta
import pandas as pd
from project import log

logger = log.Log(__name__).getlog()

def test():
    # 通过tushare获取股票信息
    # df = ts.get_k_data('002981', start='2020-01-12', end='2020-05-29')
    df = ts.get_k_data('603976', start='2019-01-12')

    # 提取收盘价
    closed = df['close'].values
    # 获取均线的数据，通过timeperiod参数来分别获取 5,10,20 日均线的数据。
    ma5 = talib.SMA(closed, timeperiod=5)
    ma10 = talib.SMA(closed, timeperiod=10)
    ma20 = talib.SMA(closed, timeperiod=20)

    # 打印出来每一个数据
    # print(closed)
    # print(ma5)
    # print(ma10)
    # print(ma20)

    # 通过plog函数可以很方便的绘制出每一条均线
    plt.plot(closed)
    plt.plot(ma5)
    plt.plot(ma10)
    plt.plot(ma20)
    # 添加网格，可有可无，只是让图像好看点
    plt.grid()
    # 记得加这一句，不然不会显示图像
    plt.show()

def test2():
    # df = ts.get_k_data('sh', start='2000-01-01')
    df = ts.get_k_data('603976', start='2020-01-12')

    df.index = pd.to_datetime(df.date)

    df = df.sort_index()

    types = ['SMA', 'EMA', 'WMA', 'DEMA', 'TEMA',

             'TRIMA', 'KAMA', 'MAMA', 'T3']

    df_ma = pd.DataFrame(df.close)

    for i in range(len(types)):

        df_ma[types[i]] = ta.MA(df.close, timeperiod=5, matype=i)

    df_ma.tail()

    df_ma.loc['2018-08-01':].plot(figsize=(16, 6))

    ax = plt.gca()

    ax.spines['right'].set_color('none')

    ax.spines['top'].set_color('none')

    plt.title(r'603976')

    plt.xlabel('')

    plt.show()


# def test2():
#     ta.BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
#
#     H_line, M_line, L_line = ta.BBANDS(df.close, timeperiod = 20, nbdevup = 2, nbdevdn = 2, matype = 0)
#
#     df1 = pd.DataFrame(df.close, index=df.index, columns=['close'])
#
#     df1['H_line'] = H_line
#
#     df1['M_line'] = M_line
#
#     df1['L_line'] = L_line
#
#     df1.tail()
#
#     df1.loc['2013-01-01':'2014-12-30'].plot(figsize=(16, 6))
#
#     ax = plt.gca()
#
#     ax.spines['right'].set_color('none')
#
#     ax.spines['top'].set_color('none')
#
#     plt.title('上证指数布林线', fontsize=15)
#
#     plt.xlabel('')
#
#     plt.show()

if __name__ == '__main__':
    logger.info('\r\n welcom to use candle predict')
    test2()