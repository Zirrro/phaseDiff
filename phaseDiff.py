# -*- coding: utf-8 -*-
# @Time    : 2022/9/5 13:46
# @Author  : Salieri
# @FileName: phaseDiff.py
# @Software: PyCharm
# @Others  :

import numpy as np
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



# 寻找周期性信号的峰值与谷值
def findMaxArray(channel):
    channel_max = np.zeros()
    channel_min = np.zeros()
    index_max = np.zeros()
    index_min = np.zeros()
    print(channel.size)
    temp_max = - 999999
    temp_min = 999999
    for i in range(0, channel.size - 3):
        if channel[i] > channel[i + 1] & channel[i] > channel[i + 2] & channel[i] > channel[i + 3] & channel[i] > temp_max:
            if temp_max == -999999:
                channel_max = np.array(channel_max, channel[i])
                index_max = np.array(index_max, i)
                temp_min = 999999
                temp_max = channel_max

        if channel[i] < channel[i + 1] & channel[i] < channel[i + 2] & channel[i] < channel[i + 3] & channel[i] < temp_min:
            if temp_min == 999999:
                channel_min = np.array(channel_min, channel[i])
                index_min = np.array(index_min, i)
                temp_max = - 999999
                temp_min = channel_min

    # 补0使长度匹配
    if channel_max.size > channel_min.size:
        channel_min = np.pad(channel_min, np.zeros(channel_max.size - channel_min.size + 1))
    elif channel_max.size < channel_min.size:
        channel_max = np.pad(channel_max, np.zeros(channel_min.size - channel_max.size + 1))
    return channel_max
