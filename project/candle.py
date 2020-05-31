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

import pandas as pd
import talib
import talib as ta
import tushare as ts
import matplotlib as mpl
import matplotlib.pyplot as plt
import mplfinance as mpf
from cycler import cycler# 用于定制线条颜色

logger = log.Log(__name__, log_path=os.getcwd()).getlog()


class Candle(object):
    """
        K 线模式识别
    """

    def __init__(self, name, code, start):
        self.__code = code
        self.__name = name
        self.df = ts.get_k_data(code, start=start)
        # df = ts.get_k_data('603976')

        self.df.index = pd.to_datetime(self.df.date)

        self.df.sort_index(inplace=True)

    def get_attr(self):
        return (self.__code, self.__name)

    def CDL2CROWS(self, open, high, low, close):
        """
        1， CDL2CROWS （Two Crows 两只乌鸦）
        简介：三日K线模式，第一天长阳，第二天高开收阴，第三天再次高开继续收阴，收盘比前一日收盘价低，预示股价下跌。
        例子：integer = CDL2CROWS(open, high, low, close)
        integer（values are - 100, 0 or 100）（以下指标如无特殊说明，返回值均为 - 100, 0, 100）
        """
        return talib.CDL2CROWS(open, high, low, close)

    def CDL3BLACKCROWS(self, open, high, low, close):
        """
        2，CDL3BLACKCROWS （Three Black Crows 三只乌鸦）
        简介：三日K线模式，连续三根阴线，每日收盘价都下跌且接近最低价，每日开盘价都在上根K线实体内，预示股价下跌。
        例子：integer = CDL3BLACKCROWS(open, high, low, close)
        """
        return talib.CDL3BLACKCROWS(open, high, low, close)

    def CDL3INSIDE(self, open, high, low, close):
        """
        3，CDL3INSIDE  （Three Inside Up / Down 三内部上涨和下跌）
        简介：三日K线模式，母子信号 + 长K线，以三内部上涨为例，K线为阴阳阳，第三天收盘价高于第一天开盘价，第二天K线在第一天K线内部，预示着股价上涨。
        例子：integer = CDL3INSIDE(open, high, low, close)
        """
        return talib.CDL3INSIDE(open, high, low, close)

    def CDL3LINESTRIKE(self, open, high, low, close):
        """
        4，CDL3LINESTRIKE  （Three - Line Strike 三线震荡）
        简介：四日K线模式，前三根阳线，每日收盘价都比前一日高，开盘价在前一日实体内，第四日市场高开，收盘价低于第一日开盘价，预示股价下跌。
        例子：integer = CDL3LINESTRIKE(open, high, low, close)
        """
        return talib.CDL3LINESTRIKE(open, high, low, close)

    def CDL3OUTSIDE(self, open, high, low, close):
        """
        5，CDL3OUTSIDE  （Three Outside Up / Down 三外部上涨和下跌）
        简介：三日K线模式，与三内部上涨和下跌类似，K线为阴阳阳，但第一日与第二日的K线形态相反，以三外部上涨为例，第一日K线在第二日K线内部，预示着股价上涨。
        例子：integer = CDL3OUTSIDE(open, high, low, close)
        """
        return talib.CDL3OUTSIDE(open, high, low, close)

    def CDL3STARSINSOUTH(self, open, high, low, close):
        """
        6，CDL3STARSINSOUTH  （Three Stars In The South 南方三星）
        简介：三日K线模式，与大敌当前相反，三日K线皆阴，第一日有长下影线，第二日与第一日类似，K线整体小于第一日，第三日无下影线实体信号，成交价格都在第一日振幅之内，预示下跌趋势反转，股价上升。,
        例子：integer = CDL3STARSINSOUTH(open, high, low, close)
        """
        return talib.CDL3STARSINSOUTH(open, high, low, close)

    def CDL3WHITESOLDIERS(self, open, high, low, close):
        """
        7，CDL3WHITESOLDIERS  （Three Advancing White Soldiers 三白兵）
        简介：三日K线模式，三日K线皆阳，每日收盘价变高且接近最高价，开盘价在前一日实体上半部，预示股价上升。
        例子：integer = CDL3WHITESOLDIERS(open, high, low, close)
        """
        return talib.CDL3WHITESOLDIERS(open, high, low, close)

    def CDLABANDONEDBABY(self, open, high, low, close):
        """
        8，CDLABANDONEDBABY  （Abandoned Baby 弃婴）
        简介：三日K线模式，第二日价格跳空且收十字星（开盘价与收盘价接近，最高价最低价相差不大），预示趋势反转，发生在顶部下跌，底部上涨。
        例子：integer = CDLABANDONEDBABY(open, high, low, close, penetration=0)
        """
        return talib.CDLABANDONEDBABY(open, high, low, close)

    def CDLADVANCEBLOCK(self, open, high, low, close):
        """
        9，CDLADVANCEBLOCK  （Advance Block 大敌当前 / 推进）
        简介：三日K线模式，三日都收阳，每日收盘价都比前一日高，开盘价都在前一日实体以内，实体变短，上影线变长。
        例子：integer = CDLADVANCEBLOCK(open, high, low, close)
        """
        return talib.CDLADVANCEBLOCK(open, high, low, close)

    def CDLBELTHOLD(self, open, high, low, close):
        """
        10，CDLBELTHOLD  （Belt - hold 捉腰带线）
        简介：两日K线模式，下跌趋势中，第一日阴线，第二日开盘价为最低价，阳线，收盘价接近最高价，预示价格上涨。
        例子：integer = CDLBELTHOLD(open, high, low, close)
        """
        return talib.CDLBELTHOLD(open, high, low, close)

    def CDLBREAKAWAY(self, open, high, low, close):
        """
        11，CDLBREAKAWAY  （Breakaway 脱离）
        简介：五日K线模式，以看涨脱离为例，下跌趋势中，第一日长阴线，第二日跳空阴线，延续趋势开始震荡，第五日长阳线，收盘价在第一天收盘价与第二天开盘价之间，预示价格上涨。
        例子：integer = CDLBREAKAWAY(open, high, low, close)
        """
        return talib.CDLBREAKAWAY(open, high, low, close)

    def CDLCLOSINGMARUBOZU(self, open, high, low, close):
        """
        12，CDLCLOSINGMARUBOZU  （Closing Marubozu 收盘光头光脚）
        简介：一日K线模式，以阳线为例，最低价低于开盘价，收盘价等于最高价，预示着趋势持续。
        例子：integer = CDLCLOSINGMARUBOZU(open, high, low, close)
        """
        return talib.CDLCLOSINGMARUBOZU(open, high, low, close)

    def CDLCONCEALBABYSWALL(self, open, high, low, close):
        """
        13，CDLCONCEALBABYSWALL  （Concealing Baby Swallow 藏婴吞没）
        简介：四日K线模式，下跌趋势中，前两日阴线无影线，第二日开盘、收盘价皆低于第二日，第三日倒锤头，第四日开盘价高于前一日最高价，收盘价低于前一日最低价，预示着底部反转。
        例子：integer = CDLCONCEALBABYSWALL(open, high, low, close)
        """
        return talib.CDLCONCEALBABYSWALL(open, high, low, close)

    def CDLCOUNTERATTACK(self, open, high, low, close):
        """
        14，CDLCOUNTERATTACK  （Counterattack 反击线）
        简介：二日K线模式，与分离线类似。
        例子：integer = CDLCOUNTERATTACK(open, high, low, close)
        """
        return talib.CDLCOUNTERATTACK(open, high, low, close)

    def CDLDARKCLOUDCOVER(self, open, high, low, close):
        """
        15，CDLDARKCLOUDCOVER  （Dark Cloud Cover 乌云盖顶）
        简介：二日K线模式，第一日长阳，第二日开盘价高于前一日最高价，收盘价处于前一日实体中部以下，预示着股价下跌。
        例子：integer = CDLDARKCLOUDCOVER(open, high, low, close, penetration=0)
        """
        return talib.CDLDARKCLOUDCOVER(open, high, low, close)

    def CDLDOJI(self, open, high, low, close):
        """
        16，CDLDOJI  （Doji 十字）
        简介：一日K线模式，开盘价与收盘价基本相同。
        例子：integer = CDLDOJI(open, high, low, close)
        """
        return talib.CDLDOJI(open, high, low, close)

    def CDLDOJISTAR(self, open, high, low, close):
        """
        17，CDLDOJISTAR  （Doji Star 十字星）
        简介：一日K线模式，开盘价与收盘价基本相同，上下影线不会很长，预示着当前趋势反转。
        例子：integer = CDLDOJISTAR(open, high, low, close)
        """
        return talib.CDLDOJISTAR(open, high, low, close)

    def CDLDOJISTAR(self, open, high, low, close):
        """
        17，CDLDOJISTAR  （Doji Star 十字星）
        简介：一日K线模式，开盘价与收盘价基本相同，上下影线不会很长，预示着当前趋势反转。
        例子：integer = CDLDOJISTAR(open, high, low, close)
        """
        return talib.CDLDOJISTAR(open, high, low, close)

    def CDLDOJISTAR(self, open, high, low, close):
        """
        17，CDLDOJISTAR  （Doji Star 十字星）
        简介：一日K线模式，开盘价与收盘价基本相同，上下影线不会很长，预示着当前趋势反转。
        例子：integer = CDLDOJISTAR(open, high, low, close)
        """
        return talib.CDLDOJISTAR(open, high, low, close)

    def CDLDRAGONFLYDOJI(self, open, high, low, close):
        """
        18，CDLDRAGONFLYDOJI  （Dragonfly Doji 蜻蜓十字 / T形十字）
        简介：一日K线模式，开盘后价格一路走低，之后收复，收盘价与开盘价相同，预示趋势反转。
        例子：integer = CDLDRAGONFLYDOJI(open, high, low, close)
        """
        return talib.CDLDRAGONFLYDOJI(open, high, low, close)

    def CDLENGULFING(self, open, high, low, close):
        """
        19，CDLENGULFING  （Engulfing Pattern 吞没模式）
        简介：两日K线模式，分多头吞噬和空头吞噬，以多头吞噬为例，第一日为阴线，第二日阳线，第一日的开盘价和收盘价在第二日开盘价收盘价之内，但不能完全相同。
        例子：integer = CDLENGULFING(open, high, low, close)
        """
        return talib.CDLENGULFING(open, high, low, close)

    def CDLEVENINGDOJISTAR(self, open, high, low, close):
        """
        20，CDLEVENINGDOJISTAR（Evening Doji Star 黄昏十字星）
        简介：三日K线模式，基本模式为暮星，第二日收盘价和开盘价相同，预示顶部反转。
        例子：integer = CDLEVENINGDOJISTAR(open, high, low, close, penetration=0)
        """
        return talib.CDLEVENINGDOJISTAR(open, high, low, close)

    def CDLEVENINGSTAR(self, open, high, low, close):
        """
        21，CDLEVENINGSTAR   （Evening Star 黄昏之星）
        简介：三日K线模式，与晨星相反，上升趋势中，第一日阳线，第二日价格振幅较小，第三日阴线，预示顶部反转。
        例子：integer = CDLEVENINGSTAR(open, high, low, close, penetration=0)
        """
        return talib.CDLEVENINGSTAR(open, high, low, close)

    def CDLGAPSIDESIDEWHITE(self, open, high, low, close):
        """
        22，CDLGAPSIDESIDEWHITE  （Up / Down - gap side - by - side white lines 向上 / 下跳空并列阳线）
        简介：二日K线模式，上升趋势向上跳空，下跌趋势向下跳空，第一日与第二日有相同开盘价，实体长度差不多，则趋势持续。
        例子：integer = CDLGAPSIDESIDEWHITE(open, high, low, close)
        """
        return talib.CDLGAPSIDESIDEWHITE(open, high, low, close)

    def CDLGRAVESTONEDOJI(self, open, high, low, close):
        """
        23，CDLGRAVESTONEDOJI  （Gravestone Doji 墓碑十字 / 倒T十字）
        简介：一日K线模式，开盘价与收盘价相同，上影线长，无下影线，预示底部反转。
        例子：integer = CDLGRAVESTONEDOJI(open, high, low, close)
        """
        return talib.CDLGRAVESTONEDOJI(open, high, low, close)

    def CDLHAMMER(self, open, high, low, close):
        """
        24，CDLHAMMER  （Hammer 锤头）
        简介：一日K线模式，实体较短，无上影线，下影线大于实体长度两倍，处于下跌趋势底部，预示反转。
        例子：integer = CDLHAMMER(open, high, low, close)
        """
        return talib.CDLHAMMER(open, high, low, close)

    def CDLHANGINGMAN(self, open, high, low, close):
        """
        25，CDLHANGINGMAN  （Hanging Man 上吊线）
        简介：一日K线模式，形状与锤子类似，处于上升趋势的顶部，预示着趋势反转。
        例子：integer = CDLHANGINGMAN(open, high, low, close)
        """
        return talib.CDLHANGINGMAN(open, high, low, close)

    def CDLHARAMI(self, open, high, low, close):
        """
        26，CDLHARAMI  （Harami Pattern 母子线 / 阴阳线）
        简介：二日K线模式，分多头母子与空头母子，两者相反，以多头母子为例，在下跌趋势中，第一日K线长阴，第二日开盘价收盘价在第一日价格振幅之内，为阳线，预示趋势反转，股价上升。
        例子：integer = CDLHARAMI(open, high, low, close)
        """
        return talib.CDLHARAMI(open, high, low, close)

    def CDLHARAMICROSS(self, open, high, low, close):
        """
        27，CDLHARAMICROSS(Harami Cross Pattern 十字孕线 )
        简介：二日K线模式，与母子县类似，若第二日K线是十字线，便称为十字孕线，预示着趋势反转。
        例子：integer = CDLHARAMICROSS(open, high, low, close)
        """
        return talib.CDLHARAMICROSS(open, high, low, close)

    def CDLHIGHWAVE(self, open, high, low, close):
        """
        28，CDLHIGHWAVE  （High - Wave Candle 风高浪大线 / 长脚十字线）
        简介：三日K线模式，具有极长的上 / 下影线与短的实体，预示着趋势反转。
        例子：integer = CDLHIGHWAVE(open, high, low, close)
        """
        return talib.CDLHIGHWAVE(open, high, low, close)

    def CDLHIKKAKE(self, open, high, low, close):
        """
        29，CDLHIKKAKE  （Hikkake Pattern 陷阱）
        简介：三日K线模式，与母子类似，第二日价格在前一日实体范围内，第三日收盘价高于前两日，反转失败，趋势继续。
        例子：integer = CDLHIKKAKE(open, high, low, close)
        """
        return talib.CDLHIKKAKE(open, high, low, close)

    def CDLHIKKAKEMOD(self, open, high, low, close):
        """
        30，CDLHIKKAKEMOD （Modified Hikkake Pattern 改良的陷阱）
        简介：三日K线模式，与陷阱类似，上升趋势中，第三日跳空高开；下跌趋势中，第三日跳空低开，反转失败，趋势继续。
        例子：integer = CDLHIKKAKEMOD(open, high, low, close)
        """
        return talib.CDLHIKKAKEMOD(open, high, low, close)

    def CDLHOMINGPIGEON(self, open, high, low, close):
        """
        31，CDLHOMINGPIGEON  （Homing Pigeon 家鸽）
        简介：二日K线模式，与母子线类似，不同的的是二日K线颜色相同，第二日最高价、最低价都在第一日实体之内，预示着趋势反转。
        例子：integer = CDLHOMINGPIGEON(open, high, low, close)
        """
        return talib.CDLHOMINGPIGEON(open, high, low, close)

    def CDLIDENTICAL3CROWS(self, open, high, low, close):
        """
        32，CDLIDENTICAL3CROWS  （Identical Three Crows 三胞胎乌鸦）
        简介：三日K线模式，上涨趋势中，三日都为阴线，长度大致相等，每日开盘价等于前一日收盘价，收盘价接近当日最低价，预示价格下跌。
        例子：integer = CDLIDENTICAL3CROWS(open, high, low, close)
        """
        return talib.CDLIDENTICAL3CROWS(open, high, low, close)

    def CDLINNECK(self, open, high, low, close):
        """
        33，CDLINNECK  （In - Neck Pattern 颈内线）
        简介：二日K线模式，下跌趋势中，第一日长阴线，第二日开盘价较低，收盘价略高于第一日收盘价，阳线，实体较短，预示着下跌继续。
        例子：integer = CDLINNECK(open, high, low, close)
        """
        return talib.CDLINNECK(open, high, low, close)

    def CDLINVERTEDHAMMER(self, open, high, low, close):
        """
        34，CDLINVERTEDHAMMER  （ Inverted Hammer 倒锤头）
        简介：一日K线模式，上影线较长，长度为实体2倍以上，无下影线，在下跌趋势底部，预示着趋势反转。
        例子：integer = CDLINVERTEDHAMMER(open, high, low, close)
        """
        return talib.CDLINVERTEDHAMMER(open, high, low, close)

    def CDLKICKING(self, open, high, low, close):
        """
        35，CDLKICKING  （Kicking 反冲形态）
        简介：二日K线模式，与分离线类似，两日K线为秃线，颜色相反，存在跳空缺口。
        例子：integer = CDLKICKING(open, high, low, close)
        """
        return talib.CDLKICKING(open, high, low, close)

    def CDLKICKINGBYLENGTH(self, open, high, low, close):
        """
        36，CDLKICKINGBYLENGTH  （Kicking - bull / bear determined by the longer marubozu 由较长光头光脚决定的反冲形态）
        简介：二日K线模式，与反冲形态类似，较长缺影线决定价格的涨跌。
        例子：integer = CDLKICKINGBYLENGTH(open, high, low, close)
        """
        return talib.CDLKICKINGBYLENGTH(open, high, low, close)

    def CDLLADDERBOTTOM(self, open, high, low, close):
        """
        37，CDLLADDERBOTTOM  （Ladder Bottom 梯底）
        简介：五日K线模式，下跌趋势中，前三日阴线，开盘价与收盘价皆低于前一日开盘、收盘价，第四日倒锤头，第五日开盘价高于前一日开盘价，阳线，收盘价高于前几日价格振幅，预示着底部反转。
        例子：integer = CDLLADDERBOTTOM(open, high, low, close)
        """
        return talib.CDLLADDERBOTTOM(open, high, low, close)

    def CDLLONGLEGGEDDOJI(self, open, high, low, close):
        """
        38，CDLLONGLEGGEDDOJI  （Long Legged Doji 长脚十字）
        简介：一日K线模式，开盘价与收盘价相同居当日价格中部，上下影线长，表达市场不确定性。
        例子：integer = CDLLONGLEGGEDDOJI(open, high, low, close)
        """
        return talib.CDLLONGLEGGEDDOJI(open, high, low, close)

    def CDLLONGLINE(self, open, high, low, close):
        """
        39，CDLLONGLINE  （Long Line Candle 长蜡烛线）
        简介：一日K线模式，K线实体长，无上下影线。
        例子：integer = CDLLONGLINE(open, high, low, close)
        """
        return talib.CDLLONGLINE(open, high, low, close)

    def CDLMARUBOZU(self, open, high, low, close):
        """
        40，CDLMARUBOZU  （Marubozu 光头光脚 / 缺影线）
        简介：一日K线模式，上下两头都没有影线的实体，阴线预示着熊市持续或者牛市反转，阳线相反。
        例子：integer = CDLMARUBOZU(open, high, low, close)
        """
        return talib.CDLMARUBOZU(open, high, low, close)

    def CDLMATCHINGLOW(self, open, high, low, close):
        """
        41，CDLMATCHINGLOW  （Matching Low 相同低价 / 匹配低价）
        简介：二日K线模式，下跌趋势中，第一日长阴线，第二日阴线，收盘价与前一日相同，预示底部确认，该价格为支撑位。
        例子：integer = CDLMATCHINGLOW(open, high, low, close)
        """
        return talib.CDLMATCHINGLOW(open, high, low, close)

    def CDLMATHOLD(self, open, high, low, close):
        """
        42，CDLMATHOLD  （Mat Hold 铺垫）
        简介：五日K线模式，上涨趋势中，第一日阳线，第二日跳空高开影线，第三、四日短实体影线，第五日阳线，收盘价高于前四日，预示趋势持续。
        例子：integer = CDLMATHOLD(open, high, low, close, penetration=0)
        """
        return talib.CDLMATHOLD(open, high, low, close)

    def CDLMORNINGDOJISTAR(self, open, high, low, close):
        """
        43，CDLMORNINGDOJISTAR  （Morning Doji Star 十字晨星 / 早晨十字星）
        简介：三日K线模式，基本模式为晨星，第二日K线为十字星，预示底部反转。
        例子：integer = CDLMORNINGDOJISTAR(open, high, low, close, penetration=0)
        """
        return talib.CDLMORNINGDOJISTAR(open, high, low, close)

    def CDLMORNINGSTAR(self, open, high, low, close):
        """
        44，CDLMORNINGSTAR  （Morning Star 晨星）
        简介：三日K线模式，下跌趋势，第一日阴线，第二日价格振幅较小，第三天阳线，预示底部反转。
        例子：integer = CDLMORNINGSTAR(open, high, low, close, penetration=0)
        """
        return talib.CDLMORNINGSTAR(open, high, low, close)

    def CDLONNECK(self, open, high, low, close):
        """
        45，CDLONNECK  （On - Neck Pattern 颈上线）
        简介：二日K线模式，下跌趋势中，第一日长阴线，第二日开盘价较低，收盘价与前一日最低价相同，阳线，实体较短，预示着延续下跌趋势。
        例子：integer = CDLONNECK(open, high, low, close)
        """
        return talib.CDLONNECK(open, high, low, close)

    def CDLPIERCING(self, open, high, low, close):
        """
        46，CDLPIERCING  （Piercing Pattern 刺透形态）
        简介：两日K线模式，下跌趋势中，第一日阴线，第二日收盘价低于前一日最低价，收盘价处在第一日实体上部，预示着底部反转。
        例子：integer = CDLPIERCING(open, high, low, close)
        """
        return talib.CDLPIERCING(open, high, low, close)

    def CDLRICKSHAWMAN(self, open, high, low, close):
        """
        47，CDLRICKSHAWMAN  （Rickshaw Man 黄包车夫）
        简介：一日K线模式，与长腿十字线类似，若实体正好处于价格振幅中点，称为黄包车夫。
        例子：integer = CDLRICKSHAWMAN(open, high, low, close)
        """
        return talib.CDLRICKSHAWMAN(open, high, low, close)

    def CDLRISEFALL3METHODS(self, open, high, low, close):
        """
        48，CDLRISEFALL3METHODS  （Rising / Falling Three Methods 上升 / 下降三法）
        简介： 五日K线模式，以上升三法为例，上涨趋势中，第一日长阳线，中间三日价格在第一日范围内小幅震荡，第五日长阳线，收盘价高于第一日收盘价，预示股价上升。
        例子：integer = CDLRISEFALL3METHODS(open, high, low, close)
        """
        return talib.CDLRISEFALL3METHODS(open, high, low, close)

    def CDLSEPARATINGLINES(self, open, high, low, close):
        """
        49，CDLSEPARATINGLINES  （Separating Lines 分离线 / 分割线）
        简介：二日K线模式，上涨趋势中，第一日阴线，第二日阳线，第二日开盘价与第一日相同且为最低价，预示着趋势继续。
        例子：integer = CDLSEPARATINGLINES(open, high, low, close)
        """
        return talib.CDLSEPARATINGLINES(open, high, low, close)

    def CDLSHOOTINGSTAR(self, open, high, low, close):
        """
        50，CDLSHOOTINGSTAR  （Shooting Star 射击之星 / 流星）
        简介：一日K线模式，上影线至少为实体长度两倍，没有下影线，预示着股价下跌
        例子：integer = CDLSHOOTINGSTAR(open, high, low, close)
        """
        return talib.CDLSHOOTINGSTAR(open, high, low, close)

    def CDLSHORTLINE(self, open, high, low, close):
        """
        51，CDLSHORTLINE  （Short Line Candle 短蜡烛线）
        简介：一日K线模式，实体短，无上下影线。
        例子：integer = CDLSHORTLINE(open, high, low, close)
        """
        return talib.CDLSHORTLINE(open, high, low, close)

    def CDLSPINNINGTOP(self, open, high, low, close):
        """
        52，CDLSPINNINGTOP  （Spinning Top 纺锤）
        简介：一日K线，实体小。
        例子：integer = CDLSPINNINGTOP(open, high, low, close)
        """
        return talib.CDLSPINNINGTOP(open, high, low, close)

    def CDLSTALLEDPATTERN(self, open, high, low, close):
        """
        53，CDLSTALLEDPATTERN  （Stalled Pattern 停顿形态）
        简介：三日K线模式，上涨趋势中，第二日长阳线，第三日开盘于前一日收盘价附近，短阳线，预示着上涨结束。
        例子：integer = CDLSTALLEDPATTERN(open, high, low, close)
        """
        return talib.CDLSTALLEDPATTERN(open, high, low, close)

    def CDLSTICKSANDWICH(self, open, high, low, close):
        """
        54，CDLSTICKSANDWICH  （Stick Sandwich 条形三明治）
        简介：三日K线模式，第一日长阴线，第二日阳线，开盘价高于前一日收盘价，第三日开盘价高于前两日最高价，收盘价于第一日收盘价相同。
        例子：integer = CDLSTICKSANDWICH(open, high, low, close)
        """
        return talib.CDLSTICKSANDWICH(open, high, low, close)

    def CDLTAKURI(self, open, high, low, close):
        """
        55，CDLTAKURI  （Takuri(Dragonfly Doji with very long lower shadow) 探水竿）
        简介：一日K线模式，大致与蜻蜓十字相同，下影线长度长。
        例子：integer = CDLTAKURI(open, high, low, close)
        """
        return talib.CDLTAKURI(open, high, low, close)

    def CDLTASUKIGAP(self, open, high, low, close):
        """
        56，CDLTASUKIGAP  （Tasuki Gap 跳空并列阴阳线）
        简介：三日K线模式，分上涨和下跌，以上升为例，前两日阳线，第二日跳空，第三日阴线，收盘价于缺口中，上升趋势持续。
        例子：integer = CDLTASUKIGAP(open, high, low, close)
        """
        return talib.CDLTASUKIGAP(open, high, low, close)

    def CDLTHRUSTING(self, open, high, low, close):
        """
        57，CDLTHRUSTING  （Thrusting Pattern 插入形态）
        简介：二日K线模式，与颈上线类似，下跌趋势中，第一日长阴线，第二日开盘价跳空，收盘价略低于前一日实体中部，与颈上线相比实体较长，预示着趋势持续。
        例子：integer = CDLTHRUSTING(open, high, low, close)
        """
        return talib.CDLTHRUSTING(open, high, low, close)

    def CDLTRISTAR(self, open, high, low, close):
        """
        58，CDLTRISTAR  （Tristar Pattern 三星形态）
        简介：三日K线模式，由三个十字组成，第二日十字必须高于或者低于第一日和第三日，预示着反转。
        例子：integer = CDLTRISTAR(open, high, low, close)
        """
        return talib.CDLTRISTAR(open, high, low, close)

    def CDLUNIQUE3RIVER(self, open, high, low, close):
        """
        59，CDLUNIQUE3RIVER  （Unique 3 River 独特三河）
        简介：三日K线模式，下跌趋势中，第一日长阴线，第二日为锤头，最低价创新低，第三日开盘价低于第二日收盘价，收阳线，收盘价不高于第二日收盘价，预示着反转，第二日下影线越长可能性越大。
        例子：integer = CDLUNIQUE3RIVER(open, high, low, close)
        """
        return talib.CDLUNIQUE3RIVER(open, high, low, close)

    def CDLUPSIDEGAP2CROWS(self, open, high, low, close):
        """
        60，CDLUPSIDEGAP2CROWS  （Upside Gap Two Crows 向上跳空的两只乌鸦 / 双飞乌鸦）
        简介：三日K线模式，第一日阳线，第二日跳空以高于第一日最高价开盘，收阴线，第三日开盘价高于第二日，收阴线，与第一日比仍有缺口。
        例子：integer = CDLUPSIDEGAP2CROWS(open, high, low, close)
        """
        return talib.CDLUPSIDEGAP2CROWS(open, high, low, close)

    def CDLXSIDEGAP3METHODS(self, open, high, low, close):
        """
        61，CDLXSIDEGAP3METHODS  （Upside / Downside Gap Three Methods 上升 / 下降跳空三法）
        简介：五日K线模式，以上升跳空三法为例，上涨趋势中，第一日长阳线，第二日短阳线，第三日跳空阳线，第四日阴线，开盘价与收盘价于前两日实体内，第五日长阳线，收盘价高于第一日收盘价，预示股价上升。
        例子：integer = CDLXSIDEGAP3METHODS(open, high, low, close)
        """
        return talib.CDLXSIDEGAP3METHODS(open, high, low, close)

    def plot(self):
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

    def get_mode(self):
        func_list = [
            # 1. function
            [self.CDL2CROWS],
            [self.CDL3BLACKCROWS],
            [self.CDL3INSIDE],
            [self.CDL3LINESTRIKE],
            [self.CDL3OUTSIDE],
            [self.CDL3STARSINSOUTH],
            [self.CDL3WHITESOLDIERS],
            [self.CDLABANDONEDBABY],
            [self.CDLADVANCEBLOCK],
            [self.CDLBELTHOLD],
            [self.CDLBREAKAWAY],
            [self.CDLCLOSINGMARUBOZU],
            [self.CDLCONCEALBABYSWALL],
            [self.CDLCOUNTERATTACK],
            [self.CDLDARKCLOUDCOVER],
            [self.CDLDOJI],
            [self.CDLDOJISTAR],
            [self.CDLDRAGONFLYDOJI],
            [self.CDLENGULFING],
            [self.CDLEVENINGDOJISTAR],
            [self.CDLEVENINGSTAR],
            [self.CDLGAPSIDESIDEWHITE],
            [self.CDLGRAVESTONEDOJI],
            [self.CDLHAMMER],
            [self.CDLHANGINGMAN],
            [self.CDLHARAMI],
            [self.CDLHARAMICROSS],
            [self.CDLHIGHWAVE],
            [self.CDLHIKKAKE],
            [self.CDLHIKKAKEMOD],
            [self.CDLHOMINGPIGEON],
            [self.CDLIDENTICAL3CROWS],
            [self.CDLINNECK],
            [self.CDLINVERTEDHAMMER],
            [self.CDLKICKING],
            [self.CDLKICKINGBYLENGTH],
            [self.CDLLADDERBOTTOM],
            [self.CDLLONGLEGGEDDOJI],
            [self.CDLLONGLINE],
            [self.CDLMARUBOZU],
            [self.CDLMATCHINGLOW],
            [self.CDLMATHOLD],
            [self.CDLMORNINGDOJISTAR],
            [self.CDLMORNINGSTAR],
            [self.CDLONNECK],
            [self.CDLPIERCING],
            [self.CDLRICKSHAWMAN],
            [self.CDLRISEFALL3METHODS],
            [self.CDLSEPARATINGLINES],
            [self.CDLSHOOTINGSTAR],
            [self.CDLSHORTLINE],
            [self.CDLSPINNINGTOP],
            [self.CDLSTALLEDPATTERN],
            [self.CDLSTICKSANDWICH],
            [self.CDLTAKURI],
            [self.CDLTASUKIGAP],
            [self.CDLTHRUSTING],
            [self.CDLTRISTAR],
            [self.CDLUNIQUE3RIVER],
            [self.CDLUPSIDEGAP2CROWS],
            [self.CDLXSIDEGAP3METHODS],
        ]

        for func in func_list:
            integer = func[0](self.df.open, self.df.high, self.df.low, self.df.close)
            data = integer[integer != 0]
            if data.empty == False:
                logger.info('%s: {%s}' % (func[0].__doc__, data))


if __name__ == '__main__':
    logger.info('\r\n ---------------- welcom to use -----------------')
    # candle = Candle('正川股份', '603976', start='2020-05-15')
    # candle = Candle('中兴通讯', '000063', start='2020-05-15')
    # candle = Candle('供销大集', '000564', start='2020-05-15')
    candle = Candle('轴研科技', '002046', start='2020-05-15')
    # print(candle.get_attr())
    candle.get_mode()
    # candle.plot()

