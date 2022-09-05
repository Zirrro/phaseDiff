# -*- coding: utf-8 -*-
# @Time    : 2022/9/5 13:46
# @Author  : Salieri
# @FileName: phaseDiff.py
# @Software: PyCharm
# @Others  :

import pandas as pd
from readsquidFiles import readsquidfiles

def getPhaseDiff():

    # 读取tdsm文件
    DataMat, Fs, FileName = readsquidfiles()

    print(DataMat.loc[0])
