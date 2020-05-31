# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/05/30
# @Author  : 陈志鹏
# @File    : xx.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../")))

import tushare as ts
import  matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY, date2num
# from matplotlib.finance import candlestick_ohlc
# from mpl_finance import candlestick_ohlc
import mplfinance as mpf
import talib as ta
import pandas as pd
from project import log
from cycler import cycler# 用于定制线条颜色

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

    # candlePlot(df, title='2020 K Plot')

# def candlePlot(seriesData, title="a"):
#     # 设定日期格式
#     Date = [date2num(date) for date in seriesData.index]
#     seriesData.loc[:, 'Date'] = Date
#     listData = []
#     for i in range(len(seriesData)):
#         a = [seriesData.Date[i], \
#              seriesData.open[i], seriesData.high[i], \
#              seriesData.low[i], seriesData.close[i]]
#         listData.append(a)
#
#     # 设定绘图相关参数
#     ax = plt.subplot()
#     mondays = WeekdayLocator(MONDAY)
#     # 日期格式为‘15-Mar-09’形式
#     weekFormatter = DateFormatter('%y %b %d')
#     ax.xaxis.set_major_locator(mondays)
#     ax.xaxis.set_minor_locator(DayLocator())
#     ax.xaxis.set_major_formatter(weekFormatter)
#
#     # 调用candlestick_ohlc函数
#     candlestick_ohlc(ax, listData, width=0.7, \
#                      colorup='r', colordown='g')
#     ax.set_title(title)  # 设定标题
#     # 设定x轴日期显示角度
#     plt.setp(plt.gca().get_xticklabels(), \
#              rotation=50, horizontalalignment='center')
#     return (plt.show())


# 蜡烛图与线图
# def candleLinePlots(candleData, candleTitle='a', **kwargs):
#     Date = [date2num(date) for date in candleData.index]
#     candleData.loc[:, 'Date'] = Date
#     listData = []
#
#     for i in range(len(candleData)):
#         a = [candleData.Date[i], \
#              candleData.Open[i], candleData.High[i], \
#              candleData.Low[i], candleData.Close[i]]
#         listData.append(a)
#     # 如 果 不 定 长 参 数 无 取 值 ， 只 画 蜡 烛 图
#     ax = plt.subplot()
#
#     # 如 果 不 定 长 参 数 有 值 ， 则 分 成 两 个 子 图
#     flag = 0
#     if kwargs:
#         if kwargs['splitFigures']:
#             ax = plt.subplot(211)
#             ax2 = plt.subplot(212)
#             flag = 1;
#         # 如 果 无 参 数 splitFigures ， 则 只 画 一 个 图 形 框
#         # 如 果 有 参 数 splitFigures ， 则 画 出 两 个 图 形 框
#
#         for key in kwargs:
#             if key == 'title':
#                 ax2.set_title(kwargs[key])
#             if key == 'ylabel':
#                 ax2.set_ylabel(kwargs[key])
#             if key == 'grid':
#                 ax2.grid(kwargs[key])
#             if key == 'Data':
#                 plt.sca(ax)
#                 if flag:
#                     plt.sca(ax2)
#
#                 # 一维数据
#                 if kwargs[key].ndim == 1:
#                     plt.plot(kwargs[key], \
#                              color='k', \
#                              label=kwargs[key].name)
#                     plt.legend(loc='best')
#                 # 二维数据有两个columns
#                 elif all([kwargs[key].ndim == 2, \
#                           len(kwargs[key].columns) == 2]):
#                     plt.plot(kwargs[key].iloc[:, 0], color='k',
#                              label=kwargs[key].iloc[:, 0].name)
#                     plt.plot(kwargs[key].iloc[:, 1], \
#                              linestyle='dashed', \
#                              label=kwargs[key].iloc[:, 1].name)
#                     plt.legend(loc='best')
#
#     mondays = WeekdayLocator(MONDAY)
#     weekFormatter = DateFormatter('%y %b %d')
#     ax.xaxis.set_major_locator(mondays)
#     ax.xaxis.set_minor_locator(DayLocator())
#     ax.xaxis.set_major_formatter(weekFormatter)
#     plt.sca(ax)
#
#     candlestick_ohlc(ax, listData, width=0.7, \
#                      colorup='r', colordown='g')
#     ax.set_title(candleTitle)
#     plt.setp(ax.get_xticklabels(), \
#              rotation=20, \
#              horizontalalignment='center')
#     ax.autoscale_view()
#
#     return (plt.show())


# 蜡烛图与成交量柱状图
# def candleVolume(seriesData, candletitle='a', bartitle='b'):
#     Date = [date2num(date) for date in seriesData.index]
#     seriesData.index = list(range(len(Date)))
#     seriesData['Date'] = Date
#     listData = zip(seriesData.Date, seriesData.Open, seriesData.High, seriesData.Low,
#                    seriesData.Close)
#     ax1 = plt.subplot(211)
#     ax2 = plt.subplot(212)
#     for ax in ax1, ax2:
#         mondays = WeekdayLocator(MONDAY)
#         weekFormatter = DateFormatter('%m/%d/%Y')
#         ax.xaxis.set_major_locator(mondays)
#         ax.xaxis.set_minor_locator(DayLocator())
#         ax.xaxis.set_major_formatter(weekFormatter)
#         ax.grid(True)
#
#     ax1.set_ylim(seriesData.Low.min() - 2, seriesData.High.max() + 2)
#     ax1.set_ylabel('蜡烛图及收盘价线')
#     candlestick_ohlc(ax1, listData, width=0.7, colorup='r', colordown='g')
#     plt.setp(plt.gca().get_xticklabels(), \
#              rotation=45, horizontalalignment='center')
#     ax1.autoscale_view()
#     ax1.set_title(candletitle)
#     ax1.plot(seriesData.Date, seriesData.Close, \
#              color='black', label='收盘价')
#     ax1.legend(loc='best')
#
#     ax2.set_ylabel('成交量')
#     ax2.set_ylim(0, seriesData.Volume.max() * 3)
#     ax2.bar(np.array(Date)[np.array(seriesData.Close >= seriesData.Open)]
#             , height=seriesData.iloc[:, 4][np.array(seriesData.Close >= seriesData.Open)]
#             , color='r', align='center')
#     ax2.bar(np.array(Date)[np.array(seriesData.Close < seriesData.Open)]
#             , height=seriesData.iloc[:, 4][np.array(seriesData.Close < seriesData.Open)]
#             , color='g', align='center')
#     ax2.set_title(bartitle)
#     return (plt.show())

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

def test3():
    """
        https://blog.csdn.net/qq_41437512/article/details/105319421
    """
    # 导入数据
    symbol = '603976'
    df = ts.get_k_data(symbol, start='2020-01-12')

    # print(df.head())

    # 格式化列名，用于之后的绘制
    df.rename(
        columns={
            'date': 'Date', 'open': 'Open',
            'high': 'High', 'low': 'Low',
            'close': 'Close', 'volume': 'Volume'},
        inplace=True)
    # 转换为日期格式
    df['Date'] = pd.to_datetime(df['Date'])
    # 将日期列作为行索引
    df.set_index(['Date'], inplace=True)

    # print(df.head())

    # 设置基本参数
    # type:绘制图形的类型，有candle, renko, ohlc, line等
    # 此处选择candle,即K线图
    # mav(moving average):均线类型,此处设置7,30,60日线
    # volume:布尔类型，设置是否显示成交量，默认False
    # title:设置标题
    # y_label:设置纵轴主标题
    # y_label_lower:设置成交量图一栏的标题
    # figratio:设置图形纵横比
    # figscale:设置图形尺寸(数值越大图像质量越高)
    kwargs = dict(
        type='candle',
        mav=(5, 10, 20),
        volume=True,
        title='\nA_stock %s candle_line' % (symbol),
        ylabel='OHLC Candles',
        ylabel_lower='Shares\nTraded Volume',
        figratio=(15, 10),
        figscale=5)

    # 设置marketcolors
    # up:设置K线线柱颜色，up意为收盘价大于等于开盘价
    # down:与up相反，这样设置与国内K线颜色标准相符
    # edge:K线线柱边缘颜色(i代表继承自up和down的颜色)，下同。详见官方文档)
    # wick:灯芯(上下影线)颜色
    # volume:成交量直方图的颜色
    # inherit:是否继承，选填
    mc = mpf.make_marketcolors(
        up='red',
        down='green',
        edge='i',
        wick='i',
        volume='in',
        inherit=True)

    # 设置图形风格
    # gridaxis:设置网格线位置
    # gridstyle:设置网格线线型
    # y_on_right:设置y轴位置是否在右
    s = mpf.make_mpf_style(
        gridaxis='both',
        gridstyle='-.',
        y_on_right=False,
        marketcolors=mc)

    # 设置均线颜色，配色表可见下图
    # 建议设置较深的颜色且与红色、绿色形成对比
    # 此处设置七条均线的颜色，也可应用默认设置
    mpl.rcParams['axes.prop_cycle'] = cycler(
        color=['dodgerblue', 'goldenrod', 'deeppink',
               'navy', 'teal', 'maroon', 'darkorange',
               'indigo'])

    # 设置线宽
    mpl.rcParams['lines.linewidth'] = .5

    # 图形绘制
    # show_nontrading:是否显示非交易日，默认False
    # savefig:导出图片，填写文件名及后缀
    period = '5'
    mpf.plot(df,
             **kwargs,
             style=s,
             show_nontrading=False,
                savefig='A_stock-%s %s_candle_line'
                 % (symbol, period) + '.png')
    plt.show()

def test4():

    df = ts.get_k_data('603976', start='2020-01-12')
    # df = ts.get_k_data('603976')

    df.index = pd.to_datetime(df.date)

    df = df.sort_index()

    # 1. Two Crows 两只乌鸦
    integer = ta.CDL2CROWS(df.open, df.high, df.low, df.close)
    print(integer[integer > 0])

    integer = ta.CDL3BLACKCROWS(df.open, df.high, df.low, df.close)
    print(integer[integer > 0])

    integer = ta.CDL3INSIDE(df.open, df.high, df.low, df.close)
    print(integer[integer > 0])

    integer = ta.CDL3INSIDE(df.open, df.high, df.low, df.close)
    print(integer[integer > 0])


if __name__ == '__main__':
    logger.info('\r\n welcom to use candle predict')
    # test3()
    test4()
