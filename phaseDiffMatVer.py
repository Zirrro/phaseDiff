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

globals(start = 10000,
        end = 12000)

def phaseDiff_mat():
    """
    求相位差，输入数据为.mat格式
    :return:
    """
    # 读取mat文件
    DataMat, Fs, FileName = readsquidfiles()
    Fs = 2000

    df = pd.DataFrame(DataMat[0])

    series = pd.Series(df[0].values, index=range(0, len(df)))

    # 绘制滤波后的数据
    x = np.array(range(10000, 12000))
    y = series.values[10000:12000]
    plt.plot(x, y)
    plt.show()

    # print(series[10000:12000])
    findMaxArray(series[10000:12000])


def findMaxArray(data):
    """
    使用一阶差分寻找正弦波每个周期的最大值
    :param data: 输入格式为Series
    :return: 返回区间内的最大值和index，格式为Series
    """
    data_df = data.diff(1)
    maxSeries = pd.Series(dtype=float)
    for i in range(start, len(data_df) - 1):
        if data_df[i] > 0 > data_df[i + 1]:
            maxSeries[str(i)] = data[i]

    print(maxSeries)
    return maxSeries
