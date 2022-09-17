# -*- coding: utf-8 -*-
# @Time    : 2022/9/5 13:46
# @Author  : Salieri
# @FileName: phaseDiff.py
# @Software: PyCharm
# @Others  :
import math
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from readsquidFiles import readsquidfiles
from scipy import signal


def getPhaseDiff():
    """
    求相位差，输入数据格式为tdms格式

    :return:
    """
    # 读取tdsm文件
    DataMat, Fs, FileName = readsquidfiles()
    # print(DataMat.size)

    # 选取通道
    channel_code_1 = input('请输入选取的第一个通道：')
    channel_code_2 = input('请输入选取的第二个通道：')
    # channel_code_1 = 0
    # channel_code_2 = 7
    channel_name_1 = '/\'Magnetic\'/\'通道' + str(channel_code_1) + '\''
    channel_name_2 = '/\'Magnetic\'/\'通道' + str(channel_code_2) + '\''

    channel_1 = DataMat[channel_name_1]
    channel_2 = DataMat[channel_name_2]

    # 配置滤波器
    low = 9  # 低频
    high = 13  # 高频
    N = 3  # 滤波器阶数

    # # 绘制未滤波前图像
    # x = np.array(range(10000, 20000))
    # y = channel_1[10000: 20000]
    # plt.title('before')
    # plt.plot(x, y)
    # plt.show()

    # 滤波后图像
    b, a = signal.butter(N, [low, high], 'bandpass', fs=Fs)
    # b, a = signal.iirfilter(3, [9, 13], fs=Fs)
    ch_filt1 = signal.filtfilt(b, a, channel_1, padlen=3 * (max(len(a), len(b)) - 1))  # padlen设置与matlab相同
    ch_filt2 = signal.filtfilt(b, a, channel_2, padlen=3 * (max(len(a), len(b)) - 1))  # padlen设置与matlab相同
    # ch_filt = signal.filtfilt(b, a, channel_1, padlen=3*(max(len(a), len(b)) - 1))  # padlen设置与matlab相同
    x = np.array(range(0, len(ch_filt1)))
    # y = ch_filt1
    # plt.title('after')
    # plt.plot(x, y)
    # plt.show()

    # # 绘制滤波器频率响应曲线
    # w, h = signal.freqs(b, a, worN=np.linspace(0, 20, 100))
    # plt.plot(w, 20 * (abs(h)))
    # plt.xlabel('Frequency')
    # plt.ylabel('Amplitude response [dB]')
    # plt.grid(True)
    # plt.show()

    # 保存差分后的结果
    ch1_max = findMaxArray(ch_filt1)
    # print('filtered channel_1 length:' + str(len(ch1_max)))
    # writer1 = pd.ExcelWriter('channel_1.xlsx')
    # ch1_max.to_excel(writer1, 'page_1')
    # writer1.save()
    # writer1.close()

    ch2_max = findMaxArray(ch_filt2)
    # print('filtered channel_2 length:' + str(len(ch2_max)))
    # writer2 = pd.ExcelWriter('channel_2.xlsx')
    # ch2_max.to_excel(writer1, 'page_1')
    # writer2.save()
    # writer2.close()

    # # 补0使长度匹配
    # if len(ch1_max) > len(ch2_max):
    #     ch2_max = np.pad(ch2_max, (0, len(ch1_max) - len(ch2_max)), constant_values='0')
    # elif len(ch2_max) > len(ch1_max):
    #     ch1_max = np.pad(ch1_max, (0, len(ch2_max) - len(ch1_max)), constant_values='0')
    # print('ch1 pad length:' + str(len(ch1_max)))
    # print('ch2 pad length:' + str(len(ch2_max)))

    # 对最大值数组进行处理，输出结果
    diffp = np.zeros(shape=(1,))
    list_1 = list(ch1_max.index)
    list_2 = list(ch2_max.index)
    for i in range(0, min(len(ch1_max), len(ch2_max))):
        diffp = np.append(diffp, int(list_1[i]) - int(list_2[i]))

    diff = diffp / Fs * 11 * 360 / (2 * math.pi)
    data = pd.DataFrame(diff)
    try:
        if os.path.exists('diff.xlsx'):
            os.remove('diff.xlsx')
    except:
        ValueError('文件目前不可用')
    writer1 = pd.ExcelWriter('diff.xlsx')
    data.to_excel(writer1, 'page_1')
    writer1.save()
    writer1.close()


# 寻找周期性信号的峰值与谷值
def findMaxArray(channel):
    """
    使用一阶差分寻找正弦波每个周期中的最大值

    :param channel: ndarray
    :return: series
    """
    # print(len(channel))  # 列数
    # 使用一阶差分求最值
    cha_df = np.diff(channel)
    maxSeries = pd.Series(dtype=float)
    # print(cha_df)
    for i in range(1, len(cha_df) - 1):
        if cha_df[i] > 0 > cha_df[i + 1]:
            maxSeries[str(i)] = channel[i]

    return maxSeries
