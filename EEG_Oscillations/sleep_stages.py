# -*- coding: utf-8 -*-
"""

@author: Lukas Kirst

License: BSD Style.

Sources of the data:
        B Kemp, AH Zwinderman, B Tuk, HAC Kamphuisen, JJL Oberyé. Analysis of 
        a sleep-dependent neuronal feedback loop: the slow-wave 
        microcontinuity of the EEG. IEEE-BME 47(9):1185-1194 (2000). 2(1,2)

        Goldberger AL, Amaral LAN, Glass L, Hausdorff JM, Ivanov PCh, Mark RG, 
        Mietus JE, Moody GB, Peng C-K, Stanley HE. (2000) PhysioBank, 
        PhysioToolkit, and PhysioNet: Components of a New Research Resource 
        for Complex Physiologic Signals. Circulation 101(23):e215-e2203

"""


import numpy as np
import matplotlib.pyplot as plt
import os

import mne
from mne.time_frequency import psd_welch

# %% download the data and create file path variables

# create a folder for the sleep data
path_sleep_data = mne.datasets.sleep_physionet.age.data_path()
if not os.path.isdir(path_sleep_data):
    os.mkdir(path_sleep_data)

link = 'https://physionet.org/physiobank/database/sleep-edfx/sleep-cassette/' 
print(f'\nPlease download the first two files from\n\t{link}\n to the folder\n\t{path_sleep_data}')

fp_raw = os.path.join(path_sleep_data, 'SC4001E0-PSG.edf')
fp_annot = os.path.join(path_sleep_data, 'SC4001EC-Hyponogram.edf')

# %% load the data

raw = mne.io.read_raw_edf(fp_raw)
annot = mne.read_annotations(fp_annot)






