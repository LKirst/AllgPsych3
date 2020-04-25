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

data_filename = 'LK_1_post1'
data_filepath_raw = os.path.join(data_folder_expanded, 
                                 data_filename + '_cropped_raw.fif')

raw = mne.io.read_raw_fif(data_filepath_raw, preload = True) 


# %% Some info about the dataset

print(raw.info, end = '\n\n')

# Channel names
print(raw.ch_names, end = '\n\n')

# Indeces in python start at 0; 
# We have 64 EEG channels in this experiment, i.e. indeces 0 to 63
print(list(enumerate(raw.ch_names)))

# %% Tell mne about the sensor locations

# We have a biosemi system
biosemi64_montage = mne.channels.make_standard_montage('biosemi64')
raw.set_montage(biosemi64_montage, raise_if_subset = False)

# Plot the montage 2D
# biosemi64_montage.plot(kind = 'topomap')

# Plot the montage 3D
# biosemi64_montage.plot(kind = '3d')

# %% Rereferencing the data to linked mastoids

raw.set_eeg_reference(['M1', 'M2'])

# %% Find events 

events = mne.find_events(raw, stim_channel = 'Status')
# 41 is the deviant
# 42 is the standard

# %% Plotting the power spectral density of unfiltered data

# raw.plot_psd(fmax = 70, picks = range(0,63))

# %% Plotting µV over time of unfiltered data

# raw.plot(duration = 5, n_channels = 30, events = events)

# %% Filtering

filt_raw = raw.copy()
filt_raw.load_data().filter(l_freq = 0.1, h_freq = None) # we only apply a high-pass filter here

# %% Plotting psd of filtered data

# filt_raw.plot_psd(fmax = 70, picks = range(0, 63)) 

# %% Plotting µV over time of filtered data

# filt_raw.plot(duration = 5, n_channels = 30, , events = events)

# %% Save the data

data_filepath_filtered = os.path.join(data_folder_expanded, data_filename + 
                                      '_filt_raw.fif')

raw.save(data_filepath_filtered, overwrite=True)


