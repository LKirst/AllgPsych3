# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 12:30:50 2020

@author: LKirst
"""


import os
import mne

# Open plots in a dedicated matplotlib qt window:
get_ipython().run_line_magic('matplotlib', 'qt')


# %% Loading the raw data

# N.b.: don't use single backward slashes in your path.
# On Windows, if you copy a path, you have to replace every single backslash \
# with either a forward slash / or a double backslash \\
data_folder = '~\\Documents\\AllgPsyVI\\Lehre\\Allgemeine3\\Daten' 
data_folder_expanded = os.path.expanduser(data_folder) # this expands the tilde to contain the path of my windows user

data_filename_raw = 'LK_1_post1.bdf'
data_filepath_raw = os.path.join(data_folder_expanded, data_filename_raw)

print('The path you specified for the raw data: ' + data_filepath_raw)

raw = mne.io.read_raw_bdf(data_filepath_raw, preload = True) 

# We're only interested in EEG channels, so we can exclude other channels
raw.pick(picks = 'all', exclude = ['Resp', 'Plet', 'Temp', 'Erg1', 'Erg2'])

# %% Some info about the dataset

print(raw.info)

# Channel names
print(raw.ch_names)

# Indeces in python start at 0; we have 64 EEG channels in this experiment, i.e. indeces 0 to 63
print(list(enumerate(raw.ch_names)))

# %% Plotting the power spectral density of unfiltered data

# this plot shows us, there is something wrong with P07
raw.plot_psd(fmax = 50, picks = range(0,63))

# %% Plotting µV over time of unfiltered data

# Make sure to mark the channel P07 as bad
raw.plot(duration = 5, n_channels = 30)

# %% Rereferencing the data

# https://mne.tools/dev/auto_examples/preprocessing/plot_rereference_eeg.html

picks = mne.pick_types(raw.info, eeg=True, exclude='bads')

fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, sharex=True)

evoked_no_ref = mne.Epochs(raw, **epochs_params).average()

raw.plot(axes=ax1, titles=dict(eeg='Original reference'), show=False,
                   time_unit='s')

raw.plot

# %% High-pass filtering

filt_raw = raw.copy()
filt_raw.load_data().filter(l_freq = 0.1, h_freq = None)

# %% Plotting psd of high-pass filtered data

filt_raw.plot_psd(fmax = 50, picks = range(0, 63)) 

# %% Plotting µV over time of high-pass filtered data

filt_raw.plot(duration = 5, n_channels = 30)

# %% Save the data

data_filepath_filtered = os.path.splitext(data_filename_raw)[0] + '_filt.fif'

raw.save(data_filepath_filtered, overwrite=True)


