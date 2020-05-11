# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 2020

@author: Lukas Kirst

"""


import os
import mne
from pathlib import Path

# Open plots in a dedicated matplotlib qt window:
get_ipython().run_line_magic('matplotlib', 'qt')

# Get the data folder (only works if you downloaded the entire project, 
# including the Data folder)
scripts_folder       = Path(__file__).parent.parent.parent
data_folder_expanded = os.path.join(scripts_folder, 'Data')
assert os.path.isdir(data_folder_expanded), ('There is no Data folder '
    'where the script assumes there should be one. You could try setting the '
    'data_folder_expanded variable manually to the folder where you saved the data.')

# %% Loading the raw data

data_filename = 'LK_1_post1'
data_filepath_raw = os.path.join(data_folder_expanded, 
                                 data_filename + '_cropped_raw.fif')

raw = mne.io.read_raw_fif(data_filepath_raw, preload = True) 

# %% Some info about the dataset

print(raw.info, end = '\n\n')

# Indeces in python start at 0; 
# We have 64 EEG channels in this experiment, i.e. indeces 0 to 63
print(list(enumerate(raw.ch_names)))

# %% Rereferencing the data to linked mastoids

raw_ref = raw.copy().set_eeg_reference(['M1', 'M2'])

# %% Tell mne about the sensor locations

# We have a biosemi system
raw_ref.drop_channels(['M1', 'M2']) # we don't need the M1 and M2 channels anymore
biosemi64_montage = mne.channels.make_standard_montage('biosemi64')
raw_ref.set_montage(biosemi64_montage)

# Plot the montage 
# biosemi64_montage.plot(kind = 'topomap') # in 2d
# biosemi64_montage.plot(kind = '3d') # in 3d

# %% Find events 

events = mne.find_events(raw_ref, stim_channel = 'Status')
# 41 is the deviant
# 42 is the standard

# %% Plotting the unfiltered data

# raw_ref.plot_psd(fmax = 70, picks = range(0,63)) # power spectral density
# raw_ref.plot(duration = 5, n_channels = 30, events = events) # µV over time

# %% Filtering

raw_filt = raw_ref.copy()
raw_filt.load_data().filter(l_freq = 0.1, h_freq = None) # we only apply a high-pass filter here

# %% Plotting the filtered data

# raw_filt.plot_psd(fmax = 70, picks = range(0, 63)) 
# raw_filt.plot(duration = 5, n_channels = 30, , events = events)

# %% Save the data

data_filepath_filtered = os.path.join(data_folder_expanded, data_filename + 
                                      '_filt_raw.fif')

raw_filt.save(data_filepath_filtered, overwrite=True)


