# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 2020

@author: Lukas Kirst
"""


import os
import mne
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# Open plots in a dedicated matplotlib qt window:
get_ipython().run_line_magic('matplotlib', 'qt')

# Get the data folder (only works if you downloaded the entire project, 
# including the Data folder)
scripts_folder       = Path(__file__).parent.parent.parent
data_folder_expanded = os.path.join(scripts_folder, 'Data')
assert os.path.isdir(data_folder_expanded), ('There is no Data folder '
    'where the script assumes there should be one. You could try setting the '
    'data_folder_expanded variable manually to the folder where you saved the data.')

# %% load the data

data_filename = 'LK_1_post1'
data_filepath_ave = os.path.join(data_folder_expanded, 
                                 data_filename + '_epo.fif')

epochs = mne.read_epochs(data_filepath_ave, preload = True)

# %% average and filter

evoked_standard = epochs['standard'].average().filter(l_freq = None, h_freq = 40)
evoked_deviant  = epochs['deviant'].average().filter(l_freq = None, h_freq = 40)

# %% topographies

fig, axesl = plt.subplots(2, 10)
times = np.linspace(-0.1, 0.8, 10)
evoked_standard.plot_topomap(times = times, axes = axesl[0,:])
evoked_deviant.plot_topomap(times = times,  axes = axesl[1,:])

# %% compare data at Pz

mne.viz.plot_compare_evokeds(
    dict(standard = evoked_standard, deviant = evoked_deviant),
    picks = 'Pz')


# %% difference wave at Pz

evoked_diff = mne.combine_evoked([evoked_standard, -evoked_deviant], 
                                 weights = 'equal')

evoked_diff.plot_topo(color = 'r')

