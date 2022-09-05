# Designed and Programmed by WSURE.
# Version 2.0. August 31st, 2022.

# Function for extracting data from tdms, mat or txt files.
# Python version.

# Return the original data matrix as DataMat in pandas DataFrame
# format. DataMat is formatted as a matrix of large
# dimension × small dimension.

# If tdms files contain valid sampling rate data, it will be returned as Fs.
# mat and txt files originally contain no sampling rate, therefore
# Fs will be returned as NaN.

# FileName returns a pure file name string without path and suffix.

def readsquidfiles(*FilePath):
    import numpy as np
    from nptdms import TdmsFile
    import pandas as pd
    import tkinter as tk
    from tkinter import filedialog
    import os
    import scipy.io as sio
    import h5py

    if len(FilePath) == 0:
        # %% 获取文件信息
        # 实例化
        root = tk.Tk()
        root.withdraw()
        # 获取文件夹路径
        f_path_total = filedialog.askopenfilename()
        f_path = os.path.dirname(f_path_total)
        f_name = os.path.basename(f_path_total)
        FileName = f_name.split(".")[0]
        suffix = f_name.split(".")[1]
        print(suffix)

    else:
        f_path_total = FilePath[0]
        f_name = os.path.basename(f_path_total)
        FileName = f_name.split(".")[0]
        suffix = f_name.split(".")[1]
        print(suffix)


    if suffix == "tdms":
        # %% 读取 TDMS 文件
        tdms_file = TdmsFile.read(f_path_total)

        for group in tdms_file.groups():
            group_name = group.name
            for channel in group.channels():
                channel_name = channel.name
                # Access dictionary of properties:
                properties = channel.properties
        Fs = int(round((1 / properties['wf_increment']) / 100) * 100)
        DataMat = tdms_file.as_dataframe(time_index=False, absolute_time=False)


    elif suffix == "txt":
        # %% 读取txt文件
        DataMat = pd.read_csv(f_path_total, sep='\t')
        Fs = None

    else:
        # %% 读取mat文件
        try:
            rawdata = sio.loadmat(f_path_total)
            DataMat = pd.DataFrame(rawdata[FileName])
            Fs = None

        except NotImplementedError:
            rawdata = h5py.File(f_path_total, 'r')
            arrays = {}
            for k, v in rawdata.items():
                arrays[k] = np.array(v)

            KeysName = list(arrays.keys())[0]
            DataMat = pd.DataFrame(arrays[KeysName])
            Fs = None

        except:
            ValueError('Can not read this mat file.')
            DataMat = None
            Fs = None

    # %% 检查矩阵维度
    HNum, VNum = DataMat.shape
    if HNum < VNum:
        DataMat = DataMat.T

    return DataMat, Fs, FileName