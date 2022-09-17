# -*- coding: utf-8 -*-
# @Time    : 2022/9/13 22:14
# @Author  : Salieri
# @FileName: phaseDiffMatVer.py
# @Software: PyCharm
# @Comment :

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from readsquidFiles import readsquidfiles

start = 10000
stop = 12000

def phaseDiff_mat():
    """
    求相位差，输入数据为.mat格式

    :return:
    """
    # 读取mat文件
    DataMat1, Fs, FileName1 = readsquidfiles()
    DataMat2, Fs, FileName2 = readsquidfiles()

    Fs = 2000

    df1 = pd.DataFrame(DataMat1[0])
    df2 = pd.DataFrame(DataMat2[0])

    series1 = pd.Series(df1[0].values, index=range(0, len(df1)))
    series2 = pd.Series(df2[0].values, index=range(0, len(df2)))
    
    
    # 绘制滤波后的数据
    x = np.array(range(start, stop))
    y = series1.values[start:stop]
    plt.plot(x, y)
    plt.show()

    # print(series1[10000:12000])
    channel1 = findMaxArray(series1[start:stop])
    channel2 = findMaxArray(series2[start:stop])


def findMaxArray(data):
    """
    使用一阶差分寻找正弦波每个周期的最大值
    :param data: 输入格式为Series
    :return: 返回区间内的最大值和index，格式为Series
    """
    data_df = data.diff(1)
    series = pd.Series(dtype=float)
    for i in range(start, len(data_df) - 1):
        if data_df[i] > 0 > data_df[i + 1]:
            series[str(i)] = data[i]

    print(series)
    return series
