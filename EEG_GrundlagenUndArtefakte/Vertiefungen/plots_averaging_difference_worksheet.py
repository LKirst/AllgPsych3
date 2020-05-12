# -*- coding: utf-8 -*-
"""
Created on Tue May 12 2020

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
epochs_filtered = epochs.copy().filter(l_freq = None, h_freq = 40)

evoked_standard = epochs['standard'].average().filter(l_freq = None, h_freq = 40)
evoked_deviant  = epochs['deviant'].average().filter(l_freq = None, h_freq = 40)

# %% plot some trials for Pz

# get_data returns (n_epochs, n_channels, n_times)
data = epochs_filtered['deviant'].get_data(picks = 'Pz') 

fig = plt.figure()
gs  = fig.add_gridspec(7, 2)
epoch_inds = [np.arange(0, data.shape[0]/2, dtype = np.int), 
              np.arange(data.shape[0]/2, data.shape[0], dtype = np.int)]

for axes_ind, epoch_ind in enumerate(epoch_inds):
    if axes_ind == 0: axes = fig.add_subplot(gs[0:2, 0])
    else: 
        first_axes_ylim = axes.get_ylim()
        
        axes = fig.add_subplot(gs[4:6, 0])
        axes.set_ylim(first_axes_ylim)
    
    axes.plot(epochs_filtered.times, np.mean(data[epoch_ind, 0, :], 0))
    axes.axhline()

# the mean of these figures
mean_epoch = np.mean(data[0:data.shape[0], 0, :], 0)
ax_mean = fig.add_subplot(gs[2:4, 1])
ax_mean.plot(epochs_filtered.times, mean_epoch)
ax_mean.set_ylim(first_axes_ylim)
ax_mean.axhline()


# %%

fig, axesl = plt.subplots(2, sharex = True, sharey = True)

for ax in axesl:
    ax.axhline(color='k')
    ax.axvline(color='k')
    ax.set_xlabel('time (secs)')
    ax.set_ylabel('microvolt')

pz_ind = evoked_standard.info['ch_names'].index('Pz')

for evok in [evoked_standard, evoked_deviant]:
    axesl[0].plot(evok.times, evok.data[pz_ind, :]*1e6, # I multiply by 1e6 to get Microvolt
                  linewidth = 2) 

combined = np.vstack(
    (evoked_deviant.data[pz_ind, :], evoked_standard.data[pz_ind, :])
    )
mean_combined = np.mean(combined, 0)
# axesl[1].plot(evoked_standard.times, mean_combined*1e6,
#               linewidth = 2, color = 'purple') # I multiply by 1e6 to get Microvolt




