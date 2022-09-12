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
    ch_test_max = findMaxArray(ch_test)
    print(ch_test_max)
    # ch1_max = findMaxArray(channel_1)
    # ch2_max = findMaxArray(channel_2)


# 寻找周期性信号的峰值与谷值
def findMaxArray(channel):
    print(len(channel))  # 列数
    temp_max = - 999999
    temp_min = 999999
    maxSeries = pd.Series(dtype='float64')
    minSeries = pd.Series(dtype='float64')

    for i in range(0, len(channel) - 3):
        if channel.loc[i] > channel[i + 1] and channel[i] > channel[i + 2] and channel[i] > channel[i + 3] and channel[i] > temp_max:
            if temp_max == -999999:
                s1 = pd.Series(data=[channel[i]])
                maxSeries.append(s1)
                temp_min = 999999
                temp_max = maxSeries

    # # 第一行存index，第二行存数据
    # channel_max = np.zeros([2, ])
    # channel_min = np.zeros([2, ])
    # print(channel.shape[1]) #列数
    # temp_max = - 999999
    # temp_min = 999999
    #
    # for i in range(0, channel.shape[1] - 3):
    #     if channel[2, i] > channel[2, (i + 1)] & channel[2, i] > channel[2, (i + 2)] & channel[2, i] > channel[2, (i + 3)] & channel[2, i] > temp_max:
    #         if temp_max == -999999:
    #             channel_max = np.hstack(channel_max, [i, channel[i]])
    #             temp_min = 999999
    #             temp_max = channel_max
    #
    #     if channel[2, i] < channel[2, (i + 1)] & channel[2, i] < channel[2, (i + 2)] & channel[2, i] < channel[i + 3] & channel[2, i] < temp_min:
    #         if temp_min == 999999:
    #             channel_min = np.hstack(channel_min, [i, channel[i]])
    #             temp_max = - 999999
    #             temp_min = channel_min
    #
    # # 补0使长度匹配
    # if channel_max.shape[1] > channel_min.shape[1]:
    #     channel_min = np.pad(channel_min, np.zeros(channel_max.size - channel_min.size + 1))
    # elif channel_max.size < channel_min.size:
    #     channel_max = np.pad(channel_max, np.zeros(channel_min.size - channel_max.size + 1))
    # return channel_max
