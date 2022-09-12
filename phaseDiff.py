# -*- coding: utf-8 -*-
# @Time    : 2022/9/5 13:46
# @Author  : Salieri
# @FileName: phaseDiff.py
# @Software: PyCharm
# @Others  :

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from readsquidFiles import readsquidfiles


def getPhaseDiff():
    # 读取tdsm文件
    DataMat, Fs, FileName = readsquidfiles()
    # print(DataMat.size)

    window_size = 1000

    # 选取通道
    channel_code_1 = 0
    channel_code_2 = 7
    channel_name_1 = '/\'Magnetic\'/\'通道' + str(channel_code_1) + '\''
    channel_name_2 = '/\'Magnetic\'/\'通道' + str(channel_code_2) + '\''

    channel_1 = DataMat[channel_name_1]
    channel_2 = DataMat[channel_name_2]
    ch_test = channel_1[0: 100]
    print(findMaxArray(ch_test))
    # ch1_max = findMaxArray(channel_1)
    # ch2_max = findMaxArray(channel_2)


# 寻找周期性信号的峰值与谷值
def findMaxArray(channel):
    print(len(channel))  # 列数
    # 使用一阶差分求最值
    cha_df = channel.diff(1)
    maxSeries = pd.Series(dtype=float)
    print(cha_df)
    for i in range (1, len(cha_df) - 1):
        if cha_df[i] > 0 and cha_df[i + 1] < 0:
            maxSeries[str(i)] = channel[i]

    print(maxSeries)


    # # 补0使长度匹配
    # if channel_max.shape[1] > channel_min.shape[1]:
    #     channel_min = np.pad(channel_min, np.zeros(channel_max.size - channel_min.size + 1))
    # elif channel_max.size < channel_min.size:
    #     channel_max = np.pad(channel_max, np.zeros(channel_min.size - channel_max.size + 1))
    # return channel_max
